# AnySearch Research 1.1.1

Independent integration using AnySearch's official hosted MCP endpoint and official
site symbol. This package is not an official AnySearch distribution or endorsement.

Five live tools: search, batch_search, get_sub_domains, extract and score. Ordinary lookups
use general search; specialized needs discover vertical routes first; ambiguous and
cross-domain research can combine general and vertical queries in batches of up to five.
Successful searches receive task-local feedback before the answer. No local CLI, server,
proxy or background process is needed for normal use.

See [中文说明](README_zh.md), [privacy](SECURITY.md), [verification](evidence/VERIFICATION.md)
and [release notes](CHANGELOG.md). Package, provider server and standalone Skill versions
are independent. This revision aligns with current MCP discovery and standalone Skill
v3.1.1 where applicable; REST/CLI flags are not native MCP parameters.

Public search, mixed general/academic/patent batch, discovery and text extraction have
usable results; three feedback entries were acknowledged queued with zero rejected.
Earlier transport errors did not recur in the latest checks. Authenticated access
and installation of this new release in the target host remain unverified. Consult the
dated execution records; package checks do not prove production acceptance.

## Install from GitHub

```sh
codex plugin marketplace add Minervaowl7/anysearch-research
codex plugin add anysearch-research@anysearch-research
```

Start a new chat after installation. Refresh the tracked source with
`codex plugin marketplace upgrade anysearch-research`.
The repository exposes `.agents/plugins/marketplace.json`; a release ZIP is available
for compatible plugin import workflows. GitHub publication does not mean approval by
or listing in the universal ChatGPT plugin directory. AnySearch controls service
availability, anonymous quotas and authentication.

## Related projects

- [Official Skill](https://github.com/anysearch-ai/anysearch-skill): standalone REST/CLI skill.
- [Official MCP](https://github.com/anysearch-ai/anysearch-mcp-server): hosted MCP setup.
- [spec-dev](https://github.com/FlameMida/spec-dev): a broader development plugin bundling a CLI-based AnySearch skill.
- [free-search-mcp](https://github.com/sweetcornna/free-search-mcp): local multi-engine server and plugin.

This focused package uses native hosted MCP with feedback handling and Chinese/English
prior-art comparison. Underlying search infrastructure belongs to the provider;
no originality or exclusivity is claimed.

## License

Integration code and original workflow text: MIT. Official brand assets are excluded
from that license grant; see [brand attribution](assets/README.md).
