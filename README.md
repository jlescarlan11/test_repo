# Philippines Q&A Notes Repository

This repository stores standalone Markdown notes that answer specific questions, mainly about the Philippines. It is a content repository, not an application or library.

## What this repository does

- Keeps one question per file
- Gives a direct short answer first
- Adds concise supporting rationale
- Lists source links for factual claims
- Includes scope/date caveats when needed

## Current content

- [`best-cat-philippines.md`](./best-cat-philippines.md): Recommendation for the most practical cat choice for many Philippine households
- [`biggest-amphibian-philippines.md`](./biggest-amphibian-philippines.md): Largest amphibian answer with native-vs-introduced scope clarification
- [`test.md`](./test.md): Cebu City top-ranked university based on a specific ranking source
- [`why-do-monkeys-have-fur.md`](./why-do-monkeys-have-fur.md): Core biological reasons monkeys have fur

## File format standard

Each note should follow this structure:

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

## Editorial rules

- Keep wording neutral and concise.
- Separate facts from opinion.
- Use reliable references and working links.
- Add explicit date/scope qualifiers for ranking or time-sensitive claims.

## Maintenance workflow

1. Select one note to add or revise.
2. Re-check claims and refresh stale sources.
3. Verify Markdown rendering and links.
4. Confirm only intended files changed.
5. Commit with a message that states what changed and why.

## Validation checks

When available:

```bash
markdownlint **/*.md
markdown-link-check README.md
```

Manual fallback:

- Check Markdown heading hierarchy and readability.
- Verify each local README link opens the expected file.
- Spot-check external source links in changed notes.

## License

No `LICENSE` file exists in this repository yet.
