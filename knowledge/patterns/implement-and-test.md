# Pattern: implement and test one story

Use for every dev task. Each step names the file it touches.

1. **Read** the story and its acceptance criteria in docs/requirements/PRD.md, its epic ADR file in
   docs/arch-docs/careslot/, and the screen frame (DES-…) in docs/designs/careslot/.
2. **Write the failing tests first**, one per AC: `<app>/tests/test_<feature>.py`, AC id in the docstring.
   Service rules → service tests; screens → view tests (status, template, the frame's text for each state);
   access → `role_required` and ownership tests.
3. **Model / migration** if the data model changes: `<app>/models.py`, then `makemigrations`. Constraints in the DB.
4. **Service**: `<app>/services.py` — the business rule, in a transaction, typed exceptions, Reminder and
   AuditLog writes where the ADRs require them. Numbers from `core/rules.py`.
5. **View-model**: extend `<app>/viewmodels.py` if the template needs new fields.
6. **View**: replace the `mock.*` call with the service/query; map typed exceptions to the frame's inline errors.
   Keep `@require_GET`/`@require_POST` and `@role_required`.
7. **Template**: keep the frame's states; remove the `?state=` branch only when real data drives that state.
8. **Run the gates**: ruff, ruff format, mypy, pytest. Then open the screen and check it against the frame.
9. **Commit** with Conventional Commits, PR cites the task, story and AC ids.
