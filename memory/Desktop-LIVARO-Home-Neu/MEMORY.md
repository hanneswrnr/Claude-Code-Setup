# LIVARO Home Neu - Project Memory

## Tech Stack
- **Framework**: Next.js 14 (App Router) + TypeScript
- **Styling**: Tailwind CSS 3.4 + custom design system
- **Backend**: Supabase (PostgreSQL, Auth, Storage) - EU Frankfurt region
- **Hosting**: Vercel
- **Animations**: Framer Motion 12
- **State**: Zustand (wizard, catalog filter)
- **Forms**: React Hook Form + Zod v4
- **Icons**: Lucide React

## Key Design Decisions
- Dark theme: #121212 base, #6BD448 green accent
- Fonts: Inter (body) + Playfair Display (headlines) via next/font/google (DSGVO: switch to local in production)
- Glassmorphism with `glass`, `glass-light`, `glass-green` CSS classes
- Atomic Design: atoms/ molecules/ organisms/ templates/

## Known Issues
- Framer Motion v12 + TypeScript: `ease` arrays in Variants objects need `as const` suffix
- Zod v4: `z.literal(true, "error message")` syntax (not errorMap)
- `clsx` is installed for `cn()` utility (no tailwind-merge)

## Project Structure
- Source: `c:/Users/hanne/OneDrive/Desktop/LIVARO Home/` (old HTML site)
- Target: `c:/Users/hanne/Desktop/LIVARO Home Neu/` (new Next.js)
- Assets: `c:/Users/hanne/Desktop/LIVARO Home Unterlagen/`
- Build dir also at: `c:/Users/hanne/Desktop/livaro-home-neu/` (npm-friendly name copy)

## Pages (all build successfully)
/, /projekte, /katalog, /kuechenplaner, /kontakt, /ueberuns, /impressum, /datenschutz, /agb, /not-found

## Remaining Work
- Admin Dashboard (/admin) with Supabase Auth
- Connect Supabase: create project, run migration, update .env.local
- Copy images from old project to public/bilder/
- Production: switch Google Fonts to local fonts
- BeforeAfterSlider component
- MaterialBoard component
- CostCalculator component
- Chatbot component (port from chatbot.js)
