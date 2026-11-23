# Prompt: implement a story

Fill in the brackets and give this to your coding agent.

```
Implement <US-id> "<title>" for CareSlot, task <task-id> of epic <E00N>.

Read first: AGENTS.md; knowledge/rules/coding-standards.md; knowledge/patterns/implement-and-test.md;
docs/requirements/PRD.md (<US-id> and its AC ids); docs/arch-docs/careslot/<epic ADR file>;
docs/designs/careslot/Frame - <screen>.dc.html.

Do: follow implement-and-test.md step by step. Tests first, one per AC. Business numbers from core/rules.py.
All appointment writes through scheduling.services. Every patient-data view/change writes AuditLog.
Use only design-system components and token colours; keep every state from the frame.

Don't: add dependencies without asking; touch other epics' apps except through their services.py;
add inline styles/scripts; log patient data.

Finish with: ruff check, ruff format --check, mypy, pytest all green; list the AC ids covered.
```
