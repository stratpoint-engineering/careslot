# CareSlot design system — for code

Source: `docs/designs/design-system/` (README, tokens.css, Design System.dc.html — read in full 2026-11-23)
and the 13 frames in `docs/designs/careslot/`. Code copy: `static/css/tokens.css` (hsl) and
`static/css/components.css`. `core/tests/test_design_tokens.py` fails if the code tokens drift from the source.

## Colour roles (hex in the design system → hsl in code)

| Role | Light hex | Light hsl | Dark hex | Dark hsl |
|---|---|---|---|---|
| --background | #ffffff | hsl(0 0% 100%) | #10161c | hsl(210 27.3% 8.6%) |
| --foreground | #1b2430 | hsl(214 28% 14.7%) | #e6ecf1 | hsl(207 28.2% 92.4%) |
| --surface | #f6f8fa | hsl(210 28.6% 97.3%) | #17202a | hsl(212 29.2% 12.7%) |
| --primary | #0f766e | hsl(175 77.4% 26.1%) | #2dd4bf | hsl(172 66% 50.4%) |
| --primary-foreground | #ffffff | hsl(0 0% 100%) | #06201d | hsl(173 68.4% 7.5%) |
| --muted | #eef2f5 | hsl(206 25.9% 94.7%) | #1f2a35 | hsl(210 26.2% 16.5%) |
| --muted-foreground | #4f5d6b | hsl(210 15.1% 36.5%) | #a7b4c1 | hsl(210 17.3% 70.6%) |
| --border | #d5dde5 | hsl(210 23.5% 86.7%) | #2c3946 | hsl(210 22.8% 22.4%) |
| --destructive | #b42318 | hsl(4 76.5% 40%) | #f97066 | hsl(4 92.5% 68.8%) |
| --success | #15803d | hsl(142 71.8% 29.2%) | #4ade80 | hsl(142 69.2% 58%) |
| --warning | #9a5b00 | hsl(35 100% 30.2%) | #fbbf24 | hsl(43 96.4% 56.3%) |

Radius `--radius` 0.5rem (8 px). Font `--font-sans` Inter (self-hosted 400 + 600), system-ui fallback.
Dark mode: tokens exist under `.dark`; nothing toggles it yet (not in the PRD).

Type sizes used by the frames: h1 20 px, h2 16 px, labels 14 px, Hint/err 13 px, body 16 px.
Spacing used: 8 / 12 / 14 / 16 / 20 px (no formal scale). No shadows. No icons except the logo.

## Components

| Component | Code | States |
|---|---|---|
| Card | `.card` (max 420 px, 20 px padding, 1 px border, radius 8) · `.card.wide` for staff toolbars | — |
| Button | `templates/components/button.html` | default · disabled (muted, not-allowed) · busy ("…ing", disabled, aria-busy) · as link (`href`) |
| Field | `templates/components/field.html` (text, email, password, date, time, tel, search, select, textarea) | error (message below, aria-invalid) · hint |
| Hint | `templates/components/hint.html` | loading pattern: "Loading…" with role=status |
| Status | `templates/components/status.html` kind ok / warn / err | err has role=alert |

## Patterns agreed with the designer (2026-11-23)

1. Staff day view: one Card per doctor, side by side, row scrolls sideways (`.cards`).
2. One Button style for every action; destructive actions (Cancel, Disable) confirm by a second click with a
   red `.err` question above "Yes, …".
3. Loading = Hint "Loading…" in place of the content; busy buttons say "…ing".
4. Header = logo, role links, user/role (Hint), Sign out — tokens only.
5. Errors inline next to their cause. No toasts.
6. Patient screens: one card, phones first; below 452 px the card gets 16 px margins. Staff: desktop.

## Added in code (not in the design system)

- `:focus-visible` outline 2 px `--primary` — required for WCAG 2.1 AA (NFR-004).
- `.link-button` in the header: the Sign out form button styled exactly as the link in the frames
  (sign-out is a POST for CSRF safety).

## Open for the designer

- **FIX NOW (NFR-004, WCAG 1.4.11):** the Field border `--border` on `--background` has contrast 1.37:1 (light)
  and 1.54:1 (dark); input boundaries need 3:1. Measured 2026-11-23. The designer chooses: darken `--border`,
  or give inputs a different existing token. Not changed in code (no colours outside the design system).

- Hover styles: the system defines none, so none are implemented.
- First-password flow for new staff (DES-003 note) and moving to another doctor (DES-011 note) — PO questions.
