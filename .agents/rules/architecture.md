# Tower of Lucas — Architecture Rules

These rules are mandatory unless the user explicitly approves an architectural change.

## Source of Truth

Before making architectural decisions:
1. Read `README.md`.
2. Inspect relevant source code and tests.
3. Prefer established project patterns.
4. Do not choose a technically convenient solution if it violates the project's architecture.

## Core Principles

- Keep domain logic independent from UI, persistence, and infrastructure.
- Preserve existing module boundaries unless the task requires changing them.
- Prefer small, cohesive classes and functions.
- Prefer immutable domain objects where the current design expects immutability.
- Avoid primitive obsession when a meaningful domain type is appropriate.
- Avoid unnecessary abstractions, frameworks, patterns, and dependencies.
- Reuse existing abstractions before creating new ones.
- Do not duplicate domain rules across layers.
- Keep side effects at appropriate application/infrastructure boundaries.

## Object Calisthenics

The project uses Object Calisthenics as a design constraint.

Inspect the README and existing implementation for the project's exact interpretation.

In particular:
- Do not introduce `else` when prohibited by the project rules.
- Avoid deep nesting.
- Avoid large methods.
- Avoid classes with excessive responsibilities.
- Avoid primitive obsession where a domain abstraction is appropriate.
- Prefer explicit objects and polymorphism over growing conditional logic when consistent with the existing architecture.
- Preserve encapsulation and avoid exposing internal mutable state.

## Domain Design

- Business rules belong in the domain layer.
- Do not leak persistence models into domain logic unless the existing architecture explicitly does so.
- Do not make domain objects depend on UI concerns.
- Do not make gameplay rules depend directly on infrastructure details.
- Represent important domain concepts with meaningful types when appropriate.

## Extension Mechanisms

When adding skills, effects, character classes, races, or other gameplay behavior:
1. Find the existing extension mechanism.
2. Follow the established dispatch/polymorphism strategy.
3. Do not introduce a parallel mechanism for convenience.
4. Avoid expanding central conditionals into unmaintainable special-case chains.

## Testing

- Every behavior change should have appropriate automated tests.
- Prefer testing observable behavior over implementation details.
- Preserve existing tests.
- Do not weaken or delete tests simply to make an implementation pass.
- If an existing test must change because intended behavior changed, explain why.

## Change Discipline

- Make the smallest coherent change that solves the task.
- Do not refactor unrelated code.
- Do not rename or move files without a task-related reason.
- Do not change public APIs without checking affected callers.
- Do not add dependencies without explaining the need.

## Completion Criteria

Before declaring success:
- Relevant tests pass.
- The project still builds/runs as expected.
- Architectural rules remain satisfied.
- No unrelated files were changed.
- The final diff matches the approved plan.
