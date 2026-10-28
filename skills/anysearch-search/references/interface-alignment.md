# Interface alignment — 2026-10-28

This package calls native MCP at https://api.anysearch.com/mcp. Its contract is the
current tools/list schema and observed return values, not a CLI example copied as JSON.

The current five tools are search, batch_search, get_sub_domains, extract and score.
The original four input structures still match the 2026-10-09 snapshot after excluding
description text. Search uses domain/sub_domain/sub_domain_params; max_results is used
as an integer 1–10. Batch members each carry their own fields, with at most five members.

The official standalone Skill v3.1.1 calls REST directly and documents tag/params,
zone/language and CLI conveniences. It is a separate distribution. Do not install its
Python/Node/Shell runtimes just to use this plugin or add its flags to native MCP calls.

Official standalone Skill routing emphasizes vertical search by default; the live MCP
description treats general and vertical search as first-class paths. Here use general
for ordinary lookups, discover specialized routes for specialized needs, and use hybrid
batches for ambiguity or cross-domain evidence. Always discover before passing domain
fields, and select only currently returned domain enums and route names. Even official
examples can be stale; examples containing unlisted domains or routes are not contracts.

Current extraction supports HTML/XHTML, plain text, JSON and Markdown. HTML/plain text
can truncate at 50,000 characters; oversized JSON/Markdown can error. The older public MCP
README says HTML-only; the current live contract and observed Markdown/JSON returns are
more specific. Unsupported binary formats require an appropriate authorized reader.

Sources:
- [Official MCP repository](https://github.com/anysearch-ai/anysearch-mcp-server)
- [Official standalone Skill](https://github.com/anysearch-ai/anysearch-skill/blob/main/SKILL.md)
- [Official interface specification](https://github.com/anysearch-ai/anysearch-skill/blob/main/scripts/shared/doc_spec.md)
- [Published standalone Skill release](https://github.com/anysearch-ai/anysearch-skill/releases/tag/v3.1.1)

Package, provider server and standalone Skill versions have separate meanings.
Preserve dated historical evidence; add a dated current snapshot on future updates.
