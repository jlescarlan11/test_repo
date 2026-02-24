# Philippines Q&A Notes Repository

A curated, source-backed Markdown knowledge base for concise Q&A notes focused on Philippines-related topics.

## Table of Contents

- [Overview](#overview)
- [Repository Contents](#repository-contents)
- [Getting Started](#getting-started)
- [Note Authoring Standard](#note-authoring-standard)
- [Editorial Policy](#editorial-policy)
- [Quality Checks](#quality-checks)
- [Contributing](#contributing)
- [Security](#security)
- [License](#license)

## Overview

This repository is a documentation-first project.
Each Markdown file contains one primary question and a direct answer with supporting rationale and sources.

Primary goals:

- Keep answers concise and accurate.
- Make claims verifiable with clear references.
- Preserve context for time-sensitive information.

## Repository Contents

- [`README.md`](./README.md): Project standards and contribution workflow.
- [`best-cat-philippines.md`](./best-cat-philippines.md): Practical household cat recommendation context.
- [`biggest-amphibian-philippines.md`](./biggest-amphibian-philippines.md): Largest amphibian note with scope caveat.
- [`test.md`](./test.md): Cebu City university ranking answer (source-specific).
- [`why-do-monkeys-have-fur.md`](./why-do-monkeys-have-fur.md): Biological explanation note.

## Getting Started

### Prerequisites

- A Markdown editor or IDE.
- Optional CLI tools for linting and link checks.

### Local workflow

1. Clone the repository.
2. Create or update one note per change set.
3. Verify factual claims and source links.
4. Run quality checks (see [Quality Checks](#quality-checks)).

## Note Authoring Standard

All notes should follow this baseline template:

```md
# <Question>

<Direct answer in 1-3 sentences.>

## Supporting rationale

- Fact: ...
- Fact: ...
- Caveat/Opinion: ...

## Sources

- <Source name> - <URL>
```

## Editorial Policy

- Use neutral, precise language.
- Separate factual statements from interpretation.
- Prefer authoritative, stable references.
- Add explicit date context for time-sensitive data (for example, rankings or changing statistics).
- Avoid broad claims without evidence.

## Quality Checks

### Automated (if available)

```bash
markdownlint **/*.md
markdown-link-check README.md
```

### Manual

- Validate heading hierarchy and readability.
- Verify local links in `README.md`.
- Spot-check external sources in modified files.
- Confirm date-sensitive claims include clear time context.

## Contributing

1. Select one note to add or revise.
2. Confirm the content follows the [Note Authoring Standard](#note-authoring-standard).
3. Validate sources and formatting.
4. Submit changes with a commit message that states what changed and why.

## Security

- Do not commit secrets, credentials, or private tokens.
- Keep sensitive operational scripts outside this repository.

### Local login helper

This repository now includes [`login.sh`](./login.sh) and [`login.py`](./login.py), local password gates to help secure repository files by tightening file permissions.

Basic usage:

```bash
./login.sh init
./login.sh login
./login.sh protect
```

```bash
./login.py init
./login.py login
./login.py protect
```

Notes:

- Password hash is stored in `.login_auth` (owner read/write only).
- `protect` sets directories to `700` and files to `600` (owner-only), excluding `.git` internals.
- For automated usage, set `LOGIN_PASSWORD` (and `LOGIN_PASSWORD_CONFIRM` for `init`).

## License

No `LICENSE` file is currently present.
Until a license is added, this repository should be treated as all rights reserved.
