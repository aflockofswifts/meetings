---
name: swift-article-roundup
description: Collect and rank recent Swift/iOS articles from subscribed Gmail newsletters plus Reddit, LinkedIn, and X/Twitter/social web mentions, then write a deduplicated markdown report for the meetup. Use when asked to make a Swift article roundup, Swift newsletter digest, Flock of Swift article list, or social/newsletter article table with images, clean URLs, summaries, and ranking against `/Users/josh/Documents/Flock of Swift Topics.md`.
---

# Swift Article Roundup

## Overview

Build a dated markdown report of Swift/iOS articles from the last 7 days of Gmail newsletters and from Reddit, LinkedIn, and X/Twitter-oriented web searches. Write the final file to:

`/Users/josh/Developer/meetup/Swift Articles YYYY-MM-DD.md`

Replace `YYYY-MM-DD` with the local date the file is created.

## Workflow

1. Read `/Users/josh/Documents/Flock of Swift Topics.md` and use it as the ranking rubric.
2. Search Gmail for the last 7 days of Swift/iOS newsletters. Use exact local dates when practical, and include searches around `Swift`, `SwiftUI`, `iOS`, `Xcode`, `newsletter`, and `weekly`. Exclude spam/trash.
3. Identify subscribed Swift newsletters, such as iOS Dev Weekly, SwiftLee Weekly, Those Who Swift, Fatbobman's Swift Weekly, Point-Free Pointers, and any similar Swift/iOS newsletters found in the mailbox.
4. Read each newsletter message, extract article/video/project links, the article title, and the newsletter's nearby description or commentary.
5. Search Reddit, LinkedIn, and X/Twitter/social web results for additional Swift/iOS article mentions from the same period. Keep these in a separate table from newsletter results.
6. Deduplicate within each table by cleaned canonical URL. If the same newsletter article appears in multiple newsletters, keep one row and list all newsletters in `Seen in`.
7. Rank each article by fit against the topics file. Favor SwiftUI layout/state/animation, Swift concurrency and Swift 6, Swift Evolution, architecture, tooling, debugging/performance, persistence, AI-assisted development, testing, security, WWDC, and community learning when those appear in the rubric.
8. Write the report markdown to the meetup directory using the required dated filename.

## URL Cleaning

Remove article tracking and click-identification parameters. Preserve content-identifying parameters, especially for YouTube videos and playlists.

Use these rules:

- Resolve newsletter redirect/clickthrough URLs to the article URL when feasible.
- Remove common tracking parameters such as `utm_*`, `fbclid`, `gclid`, `msclkid`, `mc_*`, `mkt_tok`, `trk`, `li_*`, `ref`, `ref_src`, `source`, `campaign`, `publication_id`, `post_id`, `isFreemail`, `j`, `r`, and `token`.
- Preserve functional query parameters when they identify the content. For YouTube, keep parameters such as `v`, `list`, `t`, `start`, and `index`.
- Strip fragments unless the fragment is clearly necessary to identify the content.
- Do not invent canonical URLs. If a video or article cannot be resolved without a tracker/search page, say so briefly rather than linking to the tracker.

The helper script can clean URLs directly or rewrite markdown links:

```bash
python3 scripts/clean_article_urls.py "https://example.com/post?utm_source=newsletter&id=123"
python3 scripts/clean_article_urls.py --markdown "/path/to/report.md"
```

## Report Format

Use this structure:

```markdown
# Swift Articles YYYY-MM-DD

Scope: ...

Notes:

- Tracking query parameters were removed from article URLs. Functional parameters are retained when they identify the content, such as YouTube `v=` or playlist `list=`.
- Newsletter duplicates were collapsed.
- Images are site favicons linked with the article title.

## Newsletter Articles

| Rank | Fit | Article | Seen in | Topic match | Newsletter-derived summary |
|---:|---:|---|---|---|---|

## Additional Social Mentions

| Rank | Fit | Article | Mention source | Topic match | Summary |
|---:|---:|---|---|---|---|
```

For the article cell, use a favicon image and title link:

```markdown
[![domain.com](https://icons.duckduckgo.com/ip3/domain.com.ico) Article Title](https://domain.com/article)
```

Keep summaries to a few sentences. For newsletter articles, base the summary on the newsletter's description/commentary and only use article-page context to clarify obvious titles or canonical URLs. For social mentions, summarize what the social/search result says and note the source.

## Verification

Before finishing:

1. Confirm the output file exists in `/Users/josh/Developer/meetup/`.
2. Check that the filename uses the creation date: `Swift Articles YYYY-MM-DD.md`.
3. Check that non-video article URLs do not contain known tracking parameters.
4. Check that YouTube content parameters are preserved when present.
5. Tell the user the output file path and mention any source limitations, such as inaccessible X/Twitter results.
