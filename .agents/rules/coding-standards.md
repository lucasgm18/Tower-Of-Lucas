# Tower of Lucas — Coding Standards

## General

Match the existing project's style before introducing a new style.

Follow existing conventions for:
- naming
- imports
- formatting
- type annotations
- module organization
- error handling
- tests

## Naming

- Use clear, domain-oriented names.
- Avoid unnecessary abbreviations.
- Prefer names that communicate intent.

## Functions and Methods

- Keep functions focused.
- Prefer guard clauses/early returns where appropriate.
- Avoid deeply nested control flow.
- Avoid functions with unrelated responsibilities.
- Do not introduce premature generic helpers.

## Classes

- Keep classes cohesive.
- Give each class a clear responsibility.
- Prefer existing domain abstractions.
- Avoid god objects and generic manager classes.

## Error Handling

- Follow existing project conventions.
- Do not silently swallow errors.
- Avoid broad exception handling without a clear reason.
- Error messages should explain the relevant failure.

## Tests

Tests should:
- describe behavior clearly;
- follow the existing test framework;
- cover happy paths and relevant edge cases;
- avoid private implementation details.

## Comments

Prefer readable code over comments that restate the code.

Use comments for:
- non-obvious intent;
- architectural constraints;
- domain reasoning.

## Dependencies

Do not add a dependency when existing project functionality is sufficient.

For a necessary dependency:
1. explain why;
2. verify compatibility;
3. keep the change isolated;
4. update dependency files.

## Git Hygiene

- Keep changes focused.
- Do not modify generated files unless required.
- Never commit secrets, credentials, tokens, or local environment files.
- Do not rewrite Git history.
