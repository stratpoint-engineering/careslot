# Prompt: write tests for acceptance criteria

```
Write pytest tests for CareSlot <US-id>, covering <AC-ids> from docs/requirements/PRD.md.

Rules: one test per AC, the AC id and its sentence in the docstring; pytest-django; use
`@pytest.mark.django_db` only where the DB is needed; sign in with the role the story names
(core/tests/test_shell.py `signed_in`); assert the exact inline error text from the design frame;
for slot and 2-appointment rules add a concurrent test marked to run on PostgreSQL.

Don't: mock the code under test; assert on CSS classes other than .ok/.warn/.err; depend on test order.
```
