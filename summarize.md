# Meeting Summarization Skill

## Task:
Create meeting notes from the attached chat log.
## Output format:
- Markdown (.md) suitable for direct cut-and-paste
- Chronological order (do not reorder discussion)
- One continuous document (no partial snippets)
## Content rules:
- Include all full URLs (no shortened or implied links)
- Include all code snippets, preserved exactly and wrapped in proper Markdown code fences
- Attribute links, ideas, questions, or observations to the person who shared them
- Summarize discussion clearly, but do not paraphrase code
## Filtering rules:
- Remove non-substantive chatter (e.g. “you’re on mute”, “I have to step away”)
- Keep only Swift-related or Swift-adjacent topics (Apple platforms, AI, tooling, compilers, languages, libraries, performance, etc.)
## Output requirements:
- The final result must be a downloadable Markdown file
- The file must be ready to paste into:
https://github.com/aflockofswifts/meetings/blob/main/README.md
- Do not use emojis in headers
- Do not omit attribution or links
- Do not invent context or fill in missing details
- Preserve inline Swift code exactly as written
- Dates must be formatted as yyyy.mm.dd