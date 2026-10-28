---
name: anysearch-setup
description: Set up, verify, or troubleshoot the AnySearch Research plugin, its remote MCP connection, tool availability, anonymous access, or private API-key configuration. Use for connection and installation issues, not as a prerequisite for every search.
---

# AnySearch setup and connection verification

This independent plugin points to the provider's hosted endpoint:
`https://api.anysearch.com/mcp` using Streamable HTTP.
A saved plugin, an installed/enabled plugin, a connected MCP server and a successful search
are four different states. Report only the states actually observed.

## Verify the existing connection first

1. Discover the tools on the actual AnySearch connection using the host's supported tool
   discovery. Expect `search`, `batch_search`, `get_sub_domains`, `extract`, `score`; host prefixes vary.
   Read the live contract; missing feedback support is a capability gap, not proof that search failed.
2. If a safe public query was already supplied, reuse it. Otherwise, for a requested connection
   test, use `AnySearch MCP documentation` with `max_results: 1`. No unnecessary clarification. After a successful search, submit its real request ID
   and quality rating under the [feedback rules](../anysearch-search/references/feedback.md).
   Respect approvals; do not call through an unapproved transport.
3. Confirm a real non-error response and a usable result URL before reporting search success.
   An initialize/tools-list response alone is connection discovery, not successful searching.
4. On failure, follow the search skill's failure reference; never bypass a safety block.

## Installation

For a plugin saved to the account, use its returned plugin page; enable/install it and complete
any supported connection/risk confirmation there. Do not guess a plugin ID or URL.
A newly installed connection may need a fresh chat before tools are available.

If the host does not load portable `mcp.json`, explain that specific limitation. Use the
host's Add custom MCP server flow only when the user is connecting the service and that
flow is available. Register the same verified endpoint; do not create an unrelated replacement.
Connecting the MCP separately does not prove the packaged skills are loaded.
Never promise a universal menu path or a completed installation solely from a ZIP upload.

## Authentication and privacy

The provider documents anonymous access and optional Bearer authentication. Anonymous access
can be rate-limited or unavailable. Use actual connection errors rather than assuming the user's tier.
For a key, direct the user to `https://anysearch.com/console/api-keys` and the host's private
credential settings if supported. Never ask for the key in chat, put it in the package, attach
it to a URL, read a secret file, or forward it to another service. Do not invent an OAuth flow.
If that host cannot configure the required authentication, state the limitation instead of
writing the key into shared JSON or claiming support that has not been tested.

Queries and extraction URLs go to AnySearch. Its backend retention, quotas and availability
are outside this package. Do not claim verified zero retention or an SLA. No automatic account
creation, email access, subscription purchase, permission broadening or identity rotation.
