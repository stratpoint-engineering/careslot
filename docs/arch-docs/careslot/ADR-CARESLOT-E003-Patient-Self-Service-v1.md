Epic: E003 — Patient Self-Service
Covers: US-003, US-004, US-005, FR-BOOK-001, FR-BOOK-002, FR-APPT-001, FR-APPT-002

Patient pages on phone and desktop: clinic → doctor → date → slot, book with a reason, see my appointments, cancel
until 2 hours before the start. Booking rules come from the E002 booking service.

## ADR-CARESLOT-E003-001: Build the web client with Django templates and htmx; don't build on the designer's React export
### Status
Proposed
### Type
Decision
### Context
The designer may export a React version of the screens (team-constraints). Neither developer has run a React SPA in
production, and one has used htmx. Patients mostly use phones (PRD personas). Pages must load in ≤ 2 s p95 on 4G
(NFR-001), work in the latest 2 Chrome/Safari/Edge versions (NFR-003) and meet WCAG 2.1 AA (NFR-004). Every rule
must hold server-side (team pattern).
### Options Considered
1. Build on the React export, as a SPA + a Django API: two codebases, plus an API and client state the team hasn't
   run in production, inside ~10 weeks.
2. Django templates + htmx for partial updates (slot list, day grid), mobile-first CSS from the design-system
   `tokens.css`.
3. Plain Django templates with full page reloads only.
### Decision
Option 2. The React export, if delivered, is used as a **visual reference** (layout, spacing, states). Its code is
not built on. Styling comes from `docs/designs/design-system/tokens.css`.
### Rationale
It plays to the team's skills and has one codebase, where authorization and booking rules live in one place
(FR-AUTH-005, FR-BOOK-005/006). Small server-rendered pages help NFR-001. Semantic HTML forms help NFR-004. htmx
gives instant slot lists without a SPA.
### Consequences
Designs must be buildable as HTML + CSS + htmx. Very rich client-side interactions are out of scope unless an ADR
adds them. Front-end tests are Django view tests plus browser checks in CI (NFR-003/004).
### Affected Epics
E001, E003, E004
### Architecture Document Reference
ARCH-CARESLOT-v1 §4 "Web client", §8 NFR-001, NFR-003, NFR-004
