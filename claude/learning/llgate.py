"""Prüf-Gate: a deterministic verification loop.

While a gate is armed for a project, the Stop hook runs its checks after every turn and keeps Claude working
until all of them pass or the round limit is reached. The checks, not the model, decide when work is done.
The Stop hook runs checks outside Claude Code's permission system, so problem() only admits fixed per-tool
argument forms, script_problem() inspects the package.json scripts a check reaches, and _run() executes exactly
the validated tokens without searching the current folder.
"""
import fnmatch
import os
import re
import signal
import subprocess
import sys
import tempfile
import time
from pathlib import Path

import llcore as core

GATES = core.HOME / "gates"
LOG = core.HOME / "gate-log.jsonl"
TAIL_CHARS = 1800
READ_BYTES = 64 * 1024
TTL = 24 * 3600
BIND_WINDOW = 2 * 3600
WIN = sys.platform == "win32"

HINT = ("diese Form ist als Prüfung nicht erlaubt (je Werkzeug gelten feste Optionen; komplexe Schritte als npm-Skript "
        "hinterlegen und mit npm run <skript> prüfen; der Skriptinhalt wird auf Deploy-, Nachlade- und Einzeiler-Befehle geprüft, "
        "nicht auf alles, was eigener Projektcode tut)")
FORBIDDEN = re.compile(r"[&|;<>^%!$()`'\x00-\x1f\x7f]")
LAYOUT = re.compile(r'(?:(?:"[^"]+"|[^\s"]+)(?:\s+|$))+')
TOKEN = re.compile(r'"([^"]+)"|([^\s"]+)')
RISKY = re.compile(r"(?<![a-z])(deploy|publish|push|submit|upload|promote|rollback|login|logout|exec|dlx|install|uninstall|"
                   r"seed|migrate|drop|destroy|reset|prod)(?![a-z])", re.I)
PRELOAD = re.compile(r"(?<!\S)--?(script-shell|shell|node-options|require|import|loader|experimental-loader|userconfig|"
                     r"globalconfig)(=|\s|$)", re.I)
# drive paths, rooted or UNC paths and ".." segments point outside the check folder
OUTSIDE = re.compile(r"^[A-Za-z]:|^[/\\]|(^|[\\/])\.\.([\\/]|$)")
SCRIPT = re.compile(r"^[A-Za-z0-9][A-Za-z0-9:_.-]{0,60}$")
CHECK_NAME = re.compile(r"^(test|tests|lint|typecheck|type-check|check|build|e2e|smoke|verify|validate|gate|format:check|fmt:check)"
                        r"([:_.-][a-z0-9:_.-]+)?$", re.I)
TASK = re.compile(r"^(:?[A-Za-z0-9_-]+:)*(test|check|build|lint|assemble)[A-Za-z0-9]*$")
DURATION = re.compile(r"(\d+(\.\d+)?(ns|us|ms|s|m|h))+")
SCRIPT_DANGER = re.compile(r"(?<![a-z])(deploy|publish|push|submit|upload|promote|rollback|migrate|seed|drop|destroy|login|logout)"
                           r"(?![a-z])|--prod(?![a-z])|\b(vercel|netlify|firebase|wrangler|flyctl|eas|supabase|gh|curl|wget|"
                           r"scp|rsync|ssh|pnpx|bunx|dlx)\b|docker\s+push|\bnpm\s+(exec|x)\b|"
                           r"\bnpx\s+(-y|--yes|-p|--package|-c|--call)(?![\w-])|"
                           r"\bnode(\.exe)?\s+(-e|--eval|-p|--print|-pe|-ep)(?![\w-])|"
                           r"\bpy(thon[0-9.]*)?(\.exe)?\s+(-3(\.\d+)?\s+)?-c(?![\w-])", re.I)
PMS = ("npm", "pnpm", "yarn", "bun")
PY_TOOLS = {"pytest", "mypy", "pyright", "ruff", "python", "python3", "py"}
NODE_FLAGS = {"--no-warnings", "--enable-source-maps", "--experimental-strip-types", "--experimental-test-coverage"}
NODE_REPORTERS = ("spec", "tap", "dot", "junit", "lcov")
NODE_SCRIPT = (".js", ".mjs", ".cjs", ".ts", ".mts")
GIT_DIFF = {"--check", "--exit-code", "--quiet", "--stat", "--name-only", "--name-status", "--cached", "--staged",
            "--no-ext-diff", "--no-color"}
GIT_STATUS = {"--porcelain", "--short", "-s", "--untracked-files=no"}
GRADLE_SWITCHES = {"--offline", "--no-daemon", "--stacktrace", "-q", "--quiet", "--info", "--console=plain", "--continue",
                   "--parallel"}
MARKERS = {"package.json", "pyproject.toml", "requirements.txt", "setup.cfg", "Cargo.toml", "go.mod", "pom.xml",
           "build.gradle", "build.gradle.kts", "settings.gradle", "settings.gradle.kts"}


def outside(value):
    parts = [value] + re.split(r"[=,]", value) + re.split(r"[=,:]", value)
    return any(OUTSIDE.search(part) for part in parts)


def is_rel(value):
    return bool(value) and not value.startswith("-") and not outside(value)


def is_num(value):
    return bool(re.fullmatch(r"\d{1,6}", value))


def is_name(value):
    return bool(re.fullmatch(r"[A-Za-z0-9@][A-Za-z0-9@._/+-]{0,80}", value)) and not outside(value)


def is_pattern(value):
    return 0 < len(value) <= 120 and not value.startswith("-")  # a leading "-" would be parsed as another option


def is_module(value):
    return bool(re.fullmatch(r"[A-Za-z_][A-Za-z0-9_.]{0,100}", value))


def choice(*options):
    return lambda value: value in options


def _args(args, switches=(), values=None, positional=is_rel, patterns=()):
    """Every argument must be a listed switch, a listed flag with a valid value (=value or next token) or a valid positional."""
    values = values or {}
    i = 0
    while i < len(args):
        arg = args[i]
        if arg.startswith("-") and len(arg) > 1:
            flag, eq, value = arg.partition("=")
            if arg in switches or any(re.fullmatch(p, arg) for p in patterns):
                i += 1
                continue
            if flag not in values:
                return False
            if not eq:
                i += 1
                if i >= len(args):
                    return False
                value = args[i]
            if not values[flag](value):
                return False
        elif positional is None or not positional(arg):
            return False
        i += 1
    return True


def _tsc(a):
    return _args(a, {"--noEmit", "--pretty", "--incremental", "--skipLibCheck", "-b", "--build"}, {"-p": is_rel, "--project": is_rel})


def _eslint(a):
    return _args(a, {"--quiet", "--cache", "--no-cache"}, {"--max-warnings": is_num})


def _jest(a):
    return _args(a, {"--ci", "-i", "--runInBand", "--silent", "--passWithNoTests", "--coverage"},
                 {"-t": is_pattern, "--testNamePattern": is_pattern, "--maxWorkers": is_num, "--selectProjects": is_name})


def _vitest(a):
    return a[:1] == ["run"] and _args(a[1:], {"--silent", "--coverage", "--passWithNoTests"}, {
        "-t": is_pattern, "--testNamePattern": is_pattern, "--project": is_name,
        "--shard": lambda v: bool(re.fullmatch(r"\d{1,3}/\d{1,3}", v)),
        "--reporter": choice("default", "verbose", "dot", "json", "junit", "tap")})


def _playwright(a):
    return a[:1] == ["test"] and _args(a[1:], (), {"--project": is_name, "-g": is_pattern, "--grep": is_pattern,
                                                   "--workers": is_num, "--reporter": choice("list", "line", "dot", "json", "junit")})


def _next(a):
    return a in (["build"], ["lint"]) or a[:1] == ["lint"] and _args(a[1:], (), {"--dir": is_rel}, positional=None)


DEVTOOLS = {"tsc": _tsc, "eslint": _eslint, "jest": _jest, "vitest": _vitest, "playwright": _playwright,
            "prettier": lambda a: "--check" in a and _args(a, {"--check"}),
            "biome": lambda a: a[:1] in (["check"], ["lint"], ["ci"]) and _args(a[1:]),
            "next": _next, "astro": lambda a: a in (["check"], ["build"]), "expo-doctor": lambda a: not a}


def _pytest(a):
    return _args(a, {"-q", "-qq", "-v", "-vv", "-x", "-s", "--exitfirst", "--lf", "--ff", "--no-header", "--strict-markers"},
                 {"--maxfail": is_num, "-k": is_pattern, "-m": is_pattern,
                  "--tb": choice("auto", "long", "short", "line", "native", "no"), "-n": lambda v: v == "auto" or is_num(v),
                  "--color": choice("yes", "no", "auto"), "--durations": is_num},
                 patterns=(r"-r[fEsxXpPaA]+",))


def _ruff(a):
    if a[:1] == ["check"]:
        return _args(a[1:], {"--no-fix", "--quiet", "--statistics"}, {"--output-format": choice("concise", "full", "json", "grouped")})
    return a[:1] == ["format"] and "--check" in a and _args(a[1:], {"--check"})


def _unittest(a):
    switches = {"-v", "-q", "-f", "--failfast"}
    if a[:1] == ["discover"]:
        return _args(a[1:], switches, {"-s": is_rel, "-t": is_rel, "-p": is_rel})
    return _args(a, switches, positional=is_module)


PY_MODULES = {"pytest": _pytest, "ruff": _ruff, "unittest": _unittest,
              "mypy": lambda a: _args(a, {"--strict", "--pretty", "--no-error-summary"}, {"-p": is_module, "-m": is_module}),
              "pyright": lambda a: _args(a, {"--outputjson"}, {"--level": choice("error", "warning")}),
              "compileall": lambda a: any(not x.startswith("-") for x in a) and _args(a, {"-q"}),
              "py_compile": lambda a: bool(a) and all(is_rel(x) and x.lower().endswith(".py") for x in a)}


def _python(tool, args):
    if tool in ("pytest", "mypy", "pyright", "ruff"):
        return PY_MODULES[tool](args)
    i = 0
    while i < len(args):
        if re.fullmatch(r"-3(\.\d+)?", args[i]) or args[i] == "-B":
            i += 1
        elif args[i] == "-X" and i + 1 < len(args) and args[i + 1].lower() == "utf8":
            i += 2
        else:
            break
    rest = args[i:]
    if rest[:1] == ["-m"]:
        return len(rest) >= 2 and rest[1] in PY_MODULES and PY_MODULES[rest[1]](rest[2:])
    return bool(rest) and is_rel(rest[0]) and rest[0].lower().endswith(".py")  # a project script; its args follow R1


def _uv(args):
    if args[:1] != ["run"]:
        return False
    i = 1
    while i < len(args) and args[i] in ("--frozen", "--locked", "--no-sync"):
        i += 1
    inner = tool_name(args[i]) if i < len(args) else ""
    return inner in PY_TOOLS and _python(inner, args[i + 1:])


def _node(args):
    if "--test" in args:
        return _args(args, NODE_FLAGS | {"--test"}, {"--test-reporter": choice(*NODE_REPORTERS), "--test-concurrency": is_num,
                                                     "--test-name-pattern": is_pattern})
    i = 0
    while i < len(args) and args[i] in NODE_FLAGS:
        i += 1
    return i < len(args) and is_rel(args[i]) and args[i].lower().endswith(NODE_SCRIPT)


def _git(args):
    if args[:1] == ["diff"]:
        rest, paths = args[1:], []
        if "--" in rest:
            cut = rest.index("--")
            rest, paths = rest[:cut], rest[cut + 1:]
        return all(a in GIT_DIFF for a in rest) and all(is_rel(p) for p in paths)
    return args[:1] == ["status"] and all(a in GIT_STATUS for a in args[1:])


def _pm(tool, args):
    tail = lambda rest: not rest or rest[0] == "--"  # script arguments only after --
    if args[:1] == ["test"]:
        return tail(args[1:])
    if args[:1] == ["run"]:
        return len(args) >= 2 and bool(SCRIPT.match(args[1])) and tail(args[2:])
    return tool in ("pnpm", "yarn") and bool(args) and bool(SCRIPT.match(args[0]) and CHECK_NAME.match(args[0])) and tail(args[1:])


def _npx(args):
    tool = "biome" if args[:1] == ["@biomejs/biome"] else (args[0] if args else "")
    return tool in DEVTOOLS and DEVTOOLS[tool](args[1:])


HANDLERS = {
    "uv": _uv, "node": _node, "git": _git,
    "cargo": lambda a: a[:1] in (["test"], ["check"], ["build"], ["clippy"]) and _args(
        a[1:], {"--release", "--workspace", "--all-targets", "--locked", "--offline", "-q"}, {"-p": is_name}, positional=None),
    "go": lambda a: a[:1] in (["test"], ["vet"], ["build"]) and _args(
        a[1:], {"-race", "-v", "-short"}, {"-count": is_num, "-run": is_pattern, "-timeout": lambda v: bool(DURATION.fullmatch(v))}),
    "gradle": lambda a: any(not x.startswith("-") for x in a) and _args(a, GRADLE_SWITCHES, positional=lambda v: bool(TASK.match(v))),
    "dotnet": lambda a: a in (["test"], ["build"]),
    "mvn": lambda a: a in (["test"], ["verify"]),
}
HANDLERS["gradlew"] = HANDLERS["gradle"]


def _allowed(tool, args):
    """True/False for known tools, None for unknown ones."""
    if tool in PMS:
        return _pm(tool, args)
    if tool == "npx":
        return _npx(args)
    if tool in DEVTOOLS:
        return DEVTOOLS[tool](args)
    if tool in PY_TOOLS:
        return _python(tool, args)
    return HANDLERS[tool](args) if tool in HANDLERS else None


def tool_name(first):
    if first.lower() in ("./gradlew", ".\\gradlew"):
        return "gradlew"
    if "/" in first or "\\" in first or re.match(r"^[A-Za-z]:", first):
        return ""
    name = first.lower()
    for suffix in (".cmd", ".exe", ".bat", ".ps1"):
        if name.endswith(suffix):
            name = name[:-len(suffix)]
            break
    return name if re.fullmatch(r"[a-z0-9][a-z0-9._-]*", name) else ""


def parse(check):
    """Validated tokens of a check with quotes removed, or None when quoting is ambiguous. _run executes exactly these."""
    check = (check or "").strip()
    if not check or '\\"' in check or not LAYOUT.fullmatch(check):
        return None
    return [quoted or plain for quoted, plain in TOKEN.findall(check)]


def problem(check):
    """Return why a check command is not allowed (German), or an empty string."""
    check = (check or "").strip()
    if not check:
        return "leere Prüfung"
    if len(check) > 300:
        return "Prüfung ist länger als 300 Zeichen"
    if FORBIDDEN.search(check):
        return "Sonderzeichen wie & | ; < > ^ % ! $ ( ) ' oder Backticks sind nicht erlaubt"
    tokens = parse(check)
    if not tokens:
        return "Anführungszeichen stimmen nicht oder stehen mitten in einem Wort"
    tool = tool_name(tokens[0])
    if not tool:
        return "%s: Werkzeug ohne Pfad und ohne Laufwerk angeben (z. B. npm, pytest)" % tokens[0]
    args = tokens[1:]
    plain = " ".join(args)
    if RISKY.search(plain):
        return "riskantes Wort in der Prüfung (%s): Prüfungen dürfen nichts veröffentlichen, installieren oder verändern" % RISKY.search(plain).group(0)
    if PRELOAD.search(plain):
        return "Optionen, die eine andere Shell oder vorab geladenen Code festlegen, sind nicht erlaubt"
    if any(outside(arg) for arg in args):
        return "Pfade außerhalb des Projektordners sind in Prüfungen nicht erlaubt"
    allowed = _allowed(tool, args)
    if allowed is None:
        return "%s ist kein erlaubtes Prüfwerkzeug (Tipp: als npm-Skript hinterlegen und mit npm run <skript> prüfen)" % tokens[0]
    if not allowed:
        if tool == "npx":
            return "npx nur mit tsc, eslint, vitest, jest, playwright, prettier, biome, next, astro oder expo-doctor und deren festen Optionen"
        return HINT
    if core.scan(check):
        return "Sicherheits-Scanner schlägt an"
    return ""


def _refs(text, scripts):
    """Scripts that a package.json command runs through npm/pnpm/yarn/bun, run-s/run-p/npm-run-all or npm:<name>."""
    names = []
    for segment in re.split(r"&&|\|\||[;|&]", text):
        words = segment.split()
        for i, word in enumerate(words):
            base = re.sub(r"\.(cmd|exe)$", "", os.path.basename(word.strip("\"'")).lower())
            rest = [w.strip("\"'") for w in words[i + 1:] if not w.startswith("-")]
            if base in PMS:
                key = "run" if "run" in rest else "run-script" if "run-script" in rest else ""
                if key:
                    names += rest[rest.index(key) + 1:rest.index(key) + 2]
                else:
                    names += ["test" for w in rest[:1] if w in ("test", "t")] + [w for w in rest[:2] if w in scripts]
            elif base in ("run-s", "run-p", "npm-run-all"):
                names += [n for pat in rest for n in scripts if fnmatch.fnmatchcase(n, pat)]
        names += [n for pat in re.findall(r"\bnpm:([A-Za-z0-9:_.*-]+)", segment) for n in scripts if fnmatch.fnmatchcase(n, pat)]
    return names


def script_problem(check, cwd):
    """For npm/pnpm/yarn/bun checks: why the package.json scripts the check reaches are not allowed, or ""."""
    tokens = parse(check) or []
    tool = tool_name(tokens[0]) if tokens else ""
    if tool not in PMS:
        return ""
    args = tokens[1:]
    start = "test" if args[:1] == ["test"] else args[1] if args[:1] == ["run"] and len(args) > 1 else (args[0] if args else "")
    package = Path(cwd) / "package.json"
    data = core.read_json(package, None)
    scripts = data.get("scripts") if isinstance(data, dict) else None
    if not isinstance(scripts, dict) or not isinstance(scripts.get(start), str):
        return "Skript nicht gefunden: %s in %s" % (start or "?", package)
    seen, queue = set(), [(start, 0)]
    while queue:
        current, depth = queue.pop(0)
        for script in ("pre" + current, current, "post" + current):
            text = scripts.get(script)
            if script in seen or not isinstance(text, str):
                continue
            seen.add(script)
            hit = SCRIPT_DANGER.search(text)
            if hit:
                return "npm-Skript %s enthält einen riskanten Befehl (%s)" % (script, hit.group(0))
            refs = [ref for ref in _refs(text, scripts) if ref not in seen]
            if refs and depth >= 4:
                return "npm-Skript %s ruft zu tief verschachtelt weitere Skripte auf (höchstens 4 Ebenen)" % script
            queue += [(ref, depth + 1) for ref in refs]
    return ""


def resolve(tool, cwd):
    """Absolute path of the tool: only absolute PATH folders, never the current folder."""
    if tool == "gradlew":
        path = os.path.join(cwd, "gradlew.bat" if WIN else "gradlew")
        return path if os.path.isfile(path) else ""
    exts = [""]
    if WIN:
        exts = [e for e in os.environ.get("PATHEXT", ".COM;.EXE;.BAT;.CMD").lower().split(";")
                if e in (".com", ".exe", ".bat", ".cmd")]
    for folder in os.environ.get("PATH", "").split(os.pathsep):
        folder = folder.strip().strip('"')
        if not folder or folder == "." or not os.path.isabs(folder):
            continue
        for ext in exts:
            path = os.path.join(folder, tool + ext)
            if os.path.isfile(path) and (WIN or os.access(path, os.X_OK)):
                return path
    return ""


def command_for(check, cwd):
    """(argv, "") with the resolved tool and the validated tokens (npx gets --no --), or (None, reason)."""
    tokens = parse(check)
    if not tokens:
        return None, "Prüfung konnte nicht zerlegt werden"
    tool = tool_name(tokens[0])
    exe = resolve(tool, cwd) if tool else ""
    if not exe:
        return None, "Werkzeug %s nicht gefunden (gesucht wird nur in absoluten PATH-Ordnern)" % (tool or tokens[0])
    return [exe] + (["--no", "--"] if tool == "npx" else []) + tokens[1:], ""


def windows_line(argv):
    """Command line for cmd.exe /s /c built from tokens only; tokens with spaces are double-quoted."""
    return ('"%s" %s' % (argv[0], subprocess.list2cmdline(argv[1:]))).strip()


def _kill_tree(proc):
    try:
        if WIN:
            taskkill = os.path.join(os.environ.get("SystemRoot", r"C:\Windows"), "System32", "taskkill.exe")
            subprocess.run([taskkill, "/F", "/T", "/PID", str(proc.pid)], stdin=subprocess.DEVNULL,
                           stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, timeout=30)
        else:
            os.killpg(proc.pid, signal.SIGKILL)
    except (OSError, subprocess.SubprocessError):
        pass
    try:
        proc.kill()
    except OSError:
        pass


def _run(check, cwd, seconds):
    argv, why = command_for(check, cwd)
    if why:
        return 127, why
    if WIN and re.search(r'[%!"]', argv[0]):
        return 127, "Pfad des Werkzeugs enthält Sonderzeichen: %s" % argv[0]
    env = dict(os.environ, NO_COLOR="1", FORCE_COLOR="0")
    with tempfile.TemporaryFile() as out:
        options = dict(cwd=cwd, stdin=subprocess.DEVNULL, stdout=out, stderr=subprocess.STDOUT, env=env, shell=False)
        if WIN:
            cmd = os.path.join(os.environ.get("SystemRoot", r"C:\Windows"), "System32", "cmd.exe")
            proc = subprocess.Popen('"%s" /d /s /c "%s"' % (cmd, windows_line(argv)), executable=cmd, **options)
        else:
            proc = subprocess.Popen(argv, start_new_session=True, **options)
        note = ""
        try:
            code = proc.wait(timeout=seconds)
        except subprocess.TimeoutExpired:
            _kill_tree(proc)
            try:
                proc.wait(timeout=15)
            except subprocess.TimeoutExpired:
                pass
            code, note = 124, "Zeitlimit von %d s überschritten, Prozessbaum beendet" % seconds
        out.seek(0, os.SEEK_END)
        out.seek(max(0, out.tell() - READ_BYTES))
        output = out.read().decode("utf-8", "replace")
    if note:
        output = output.strip()[-(TAIL_CHARS - len(note) - 1):] + "\n" + note
    return code, output


def run_checks(state):
    results, deadline = [], time.time() + state["timeout"]
    cwd = state.get("cwd") or state["root"]
    for check in state["checks"]:
        left = int(deadline - time.time())
        if left <= 5:
            results.append({"check": check, "code": 124, "seconds": 0, "tail": "Nicht ausgeführt: Zeitbudget aufgebraucht"})
            continue
        started = time.time()
        try:
            code, output = _run(check, cwd, left)
        except (OSError, ValueError, subprocess.SubprocessError) as exc:
            code, output = 127, "Start fehlgeschlagen: %s" % exc
        results.append({"check": check, "code": code, "seconds": round(time.time() - started, 1),
                        "tail": output.strip()[-TAIL_CHARS:]})
    return results


def path_for(project):
    return GATES / (re.sub(r"[^A-Za-z0-9_-]", "_", str(project)) + ".json")


def clamp(value, low, high, default):
    try:
        return max(low, min(int(value), high))
    except (TypeError, ValueError):
        return default


def has_marker(folder):
    try:
        names = os.listdir(folder)
    except OSError:
        return False
    return any(name in MARKERS or name.lower().endswith((".sln", ".csproj")) for name in names)


def _same(a, b):
    return os.path.normcase(os.path.abspath(str(a))) == os.path.normcase(os.path.abspath(str(b)))


def scope_problem(cwd):
    """Gates only live in a project folder: inside a git repo or next to a project file, never home or a drive root."""
    folder = Path(cwd)
    root = Path(core.checkout_key(cwd)[1])
    for candidate in (folder, root):
        if candidate.parent == candidate or _same(candidate, Path.home()):
            return "nicht im Benutzerordner oder direkt auf einem Laufwerk: im Projektordner ausführen"
    if (root / ".git").exists() or has_marker(folder):
        return ""
    return "kein Projektordner: hier gibt es weder git noch eine Projektdatei wie package.json, pyproject.toml oder go.mod"


def arm(checks, max_rounds=8, timeout=900, note=""):
    cwd = os.path.abspath(os.getcwd())
    scope = scope_problem(cwd)
    if scope:
        return None, [("", scope)]
    bad = [(check, problem(check) or script_problem(check, cwd)) for check in checks]
    bad = [(check, why) for check, why in bad if why]
    if bad or not checks:
        return None, bad or [("", "leere Prüfung")]
    project, root = core.checkout_key(cwd)  # per checkout: each git worktree has its own gate
    armed = time.time()
    state = {"project": project, "root": root, "cwd": cwd, "checks": [c.strip() for c in checks],
             "session": os.environ.get("CLAUDE_CODE_SESSION_ID", "")[:80], "armed_at": core.now(), "armed_ts": armed,
             "expires_ts": armed + TTL, "round": 0, "max_rounds": clamp(max_rounds, 1, 20, 8),
             "timeout": clamp(timeout, 30, 1500, 900), "note": (note or "")[:200], "history": [], "running_since": None}
    core.write_json(path_for(project), state)
    return state, []


def _stamp(state, key):
    try:
        return float(state[key])
    except (KeyError, TypeError, ValueError):
        armed = core.parse_ts(state.get("armed_at"))
        return armed.timestamp() + (TTL if key == "expires_ts" else 0) if armed else 0.0


def expired(state):
    return time.time() >= _stamp(state, "expires_ts")


def _int_in(value, low, high):
    return type(value) is int and low <= value <= high


def state_problem(state):
    """Why a stored gate must not run (German), or an empty string."""
    project = state.get("project")
    if not isinstance(project, str) or not state.get("_file") or Path(state["_file"]) != path_for(project):
        return "Gate-Datei passt nicht zum Projekt"
    if not isinstance(state.get("session"), str):
        return "Session ungültig"
    max_rounds = state.get("max_rounds")
    if not (_int_in(max_rounds, 1, 20) and _int_in(state.get("timeout"), 30, 1500)
            and _int_in(state.get("round"), 0, max_rounds if type(max_rounds) is int else 0)):
        return "Runden oder Zeitbudget ungültig"
    running = state.get("running_since")
    if running is not None and type(running) not in (int, float):
        return "Laufmarke ungültig"
    if not isinstance(state.get("history"), list) or not isinstance(state.get("checks"), list):
        return "Verlauf oder Prüfungen ungültig"
    cwd, root = state.get("cwd"), state.get("root")
    if not isinstance(cwd, str) or not isinstance(root, str) or not os.path.isabs(cwd) or not os.path.isdir(cwd):
        return "Prüfordner fehlt oder ist ungültig"
    try:
        inside = os.path.commonpath([os.path.normcase(cwd), os.path.normcase(root)]) == os.path.normcase(root)
    except ValueError:
        inside = False
    if not inside or core.checkout_key(cwd)[0] != project:
        return "Prüfordner liegt nicht im Projekt"
    return ""


def find(cwd=None, session_id=None, bind=True):
    """Gate for the git root of cwd, or for the nearest folder with a project file. session_id None = any session."""
    start = Path(os.path.abspath(cwd or os.getcwd()))
    project, root = core.checkout_key(start)
    keys = [project]
    if not (Path(root) / ".git").exists():
        for folder in [start, *start.parents]:
            if has_marker(folder):
                key = core.checkout_key(folder)[0]
                if key not in keys:
                    keys.append(key)
                break
    state = None
    for key in keys:
        data = core.read_json(path_for(key), None)
        if isinstance(data, dict):
            state = dict(data, _file=str(path_for(key)))
            break
    if not state:
        return None
    if expired(state):
        disarm(state, "expired")
        return None
    if session_id is None:
        return state
    owner = state.get("session") or ""
    if owner:
        return state if owner == session_id else None
    if time.time() - _stamp(state, "armed_ts") >= BIND_WINDOW:
        return None
    if bind and session_id and not state_problem(state):
        state["session"] = session_id
        save(state)
    return state


def sweep():
    """Silently end expired gates."""
    for path in GATES.glob("*.json"):
        state = core.read_json(path, None)
        if isinstance(state, dict) and expired(state):
            core.append_jsonl(LOG, dict(public(state), outcome="expired", ended_at=core.now()), rotate_bytes=core.ROTATE_BYTES)
            try:
                path.unlink()
            except OSError:
                pass


def public(state):
    return {key: value for key, value in state.items() if not str(key).startswith("_")}


def save(state):
    core.write_json(path_for(state["project"]), public(state))


def disarm(state, outcome):
    core.append_jsonl(LOG, dict(public(state), outcome=outcome, ended_at=core.now()), rotate_bytes=core.ROTATE_BYTES)
    target = Path(state["_file"]) if state.get("_file") else path_for(state.get("project", ""))
    if target.parent == GATES:
        try:
            target.unlink()
        except OSError:
            pass
