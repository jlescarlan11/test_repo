# Philippines Topic Notes

A markdown-first knowledge repository for concise, evidence-oriented notes about Philippines-focused topics.

## Purpose

This repository contains short reference notes, not application code. Each note should answer one specific question with a clear conclusion and concise supporting rationale.

## Repository Structure

- [`best-cat-philippines.md`](./best-cat-philippines.md): Practical cat breed guidance for Philippine conditions.
- [`biggest-amphibian-philippines.md`](./biggest-amphibian-philippines.md): Largest amphibian comparison in native vs introduced context.
- [`test.md`](./test.md): Note on top-ranked university in Cebu City.
- [`README.md`](./README.md): Repository standards, workflow, and quality expectations.

## Authoring Standard

All notes must follow these requirements:

- State the short answer in the opening paragraph.
- Keep one primary question per file.
- Distinguish factual claims from opinion.
- Attribute factual claims to current, verifiable sources.
- Use direct, concise wording.

## Recommended Note Template

Use this structure for new files:

1. `#` Title with the exact question/topic.
2. Short answer (1-3 sentences).
3. Supporting rationale (bulleted).
4. Sources.
5. Optional caveats/scope limits.

## Contribution Workflow

1. Choose one note to add or update.
2. Validate claims and refresh sources where needed.
3. Run markdown quality checks.
4. Perform manual readability and rendering review.
5. Commit with a message that states what changed and why.

## Quality Gate (Production Readiness)

A change is ready to merge when all items below are true:

- Markdown renders correctly.
- Internal links resolve.
- Claims are either sourced or explicitly labeled as opinion.
- Scope is clear and not overstated.
- Only intentional files are modified.

### Suggested Local Checks

Run these if available in your environment:

```bash
markdownlint **/*.md
markdown-link-check README.md
```

If tools are unavailable, complete a manual pass for headings, links, and readability.

## Versioning

This repository currently does not use tagged releases. Production readiness is evaluated per-commit using the quality gate above.

## License

No `LICENSE` file is currently present. Add a license before public redistribution or external reuse.
