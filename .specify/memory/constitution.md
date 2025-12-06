<!-- Sync Impact Report
Version Change: (new file) → 1.0.0
Reason: Initial constitution establishment for Todo App CLI project
Principles Added:
  - Clean Code Standards (1 of 6)
  - Project Structure (2 of 6)
  - Development Methodology (3 of 6)
  - Data Management (4 of 6)
  - User Experience (5 of 6)
  - Code Quality Gates (6 of 6)
Additional Sections:
  - Constraints (non-negotiable project boundaries)
  - Success Criteria (definitive completion conditions)
  - Governance (amendment and compliance procedures)
Templates Requiring Updates: ✅ spec-template.md, ✅ plan-template.md, ✅ tasks-template.md
-->

# Todo App Constitution

## Core Principles

### 1. Clean Code Standards

Write readable, self-documenting code with meaningful variable and function names. Follow PEP 8 style guidelines strictly. Keep functions small and focused on a single responsibility. Use type hints for all function parameters and return values. Write docstrings for all public functions and classes.

**Rationale**: Clean, well-typed code reduces maintenance burden, improves onboarding, and prevents defects through explicitness.

### 2. Project Structure

Use UV as the package manager. Target Python 3.13+. Organize code into logical modules. Separate concerns: data models, business logic, and CLI interface. Keep the main entry point clean and minimal.

**Rationale**: Clear separation of concerns enables independent testing, reduces coupling, and makes the codebase maintainable as it grows. UV provides fast, reliable dependency management for modern Python projects.

### 3. Development Methodology

Follow spec-driven development principles. Write specifications before implementation. Each feature must be independently testable. Maintain clear boundaries between components.

**Rationale**: Specifying requirements upfront prevents scope creep, ensures alignment on acceptance criteria, and enables parallel work on independent features.

### 4. Data Management

Store all tasks in memory (no persistence required). Use appropriate data structures for efficient operations. Ensure data integrity for all CRUD operations. Use unique identifiers for task management.

**Rationale**: In-memory storage keeps the MVP simple while proper data structures and IDs ensure correctness. If persistence becomes needed later, a well-structured data layer makes migration straightforward.

### 5. User Experience

Provide clear, helpful CLI feedback. Handle errors gracefully with informative messages. Maintain consistent command patterns. Support intuitive task management workflow.

**Rationale**: A predictable, friendly CLI experience reduces user frustration and support burden. Consistent patterns make the application feel professional.

### 6. Code Quality Gates

No global mutable state outside of the main application class. All business logic must be unit testable. Input validation for all user-provided data. Explicit is better than implicit.

**Rationale**: Eliminating global state enables isolated testing and reasoning about code behavior. Input validation at system boundaries prevents data corruption. Explicit code is debuggable and maintainable.

## Constraints

The following constraints are **non-negotiable** and must be respected throughout development:

- **DO NOT** use external databases or file storage
- **DO NOT** add features beyond the 5 basic requirements (add, delete, update, view, complete)
- **DO NOT** use complex frameworks for the CLI (argparse or simple input is sufficient)
- **DO NOT** over-engineer the solution
- **ALWAYS** validate user input before processing
- **ALWAYS** provide feedback after each operation

## Success Criteria

The application is complete when:

- Users can add new tasks with descriptions
- Users can delete existing tasks by ID
- Users can update task descriptions
- Users can view all tasks with their status
- Users can mark tasks as complete
- All operations provide clear user feedback
- The code passes linting and type checking

## Governance

**Amendment Procedure**: Constitution amendments require written justification of the change (rationale, impact on existing code/practices). Changes are documented in a new Prompt History Record with stage `constitution`. Version bumps follow semantic versioning: MAJOR for backward-incompatible principle removals or redefinitions, MINOR for new principles or materially expanded guidance, PATCH for clarifications or non-semantic refinements.

**Compliance Review**: All pull requests and feature implementations must verify alignment with these principles. Violations require documented justification in the commit message or PR description explaining why the constraint is superseded.

**Runtime Guidance**: Developers should consult `CLAUDE.md` in the repository root for implementation-level guidance and tool usage. This constitution defines *what* we build; that file explains *how* we build it.

**Version**: 1.0.0 | **Ratified**: 2025-12-05 | **Last Amended**: 2025-12-05
