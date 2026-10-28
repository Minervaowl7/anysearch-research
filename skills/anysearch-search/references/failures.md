# Failure handling

These are workflow rules, not an HTTP middleware layer. The host and AnySearch implement
transport behavior. Report actual returned information; do not infer an HTTP status from tone.

| Observation | Correct response |
| --- | --- |
| Tool absent or connection disabled | Report unavailable; open the supported plugin connection flow. Never invent a connected state. |
| Permission denied or safety block | Stop. Do not repeat the same operation through a different transport to evade the decision. |
| 401 / 403 authentication or access failure | Explain the actual response. Use private host connection settings. Do not demand a key in chat, invent OAuth endpoints or promise anonymous access always works. |
| 429 / quota exhausted | Preserve successful results; show any retry-after or reset details actually returned. No key/account rotation, repeated probing, sleep loop or automatic paid upgrade. |
| Timeout / 5xx | State that completion and quota consumption may be unknown. If a transient failure is clear and host/user policy permits, at most one deliberate retry; otherwise stop. |
| Invalid tool input | Compare to the live schema; correct the input once. For a vertical route, refresh `get_sub_domains`. |
| Batch partially succeeds | Keep successful members, identify each failed angle. Retry only a failed member when justified, never the entire successful batch. |
| Zero results | Report zero results. Try a different mechanism/source angle when useful; do not equate absence with global novelty. |
| Extraction blocked, unsupported or truncated | Label as partial/unread. Use a separately authorized appropriate reader for content, or request the document. Do not claim the full source was verified. |
| Invalid JSON, missing expected fields or unrecognized structure | Preserve the error. Do not relabel it as an empty result or synthesize missing fields. |

Current discovery still observes contradictory `readOnlyHint: true` and
`destructiveHint: true` on the original four tools. The new score tool instead advertises
`readOnlyHint: false`, `destructiveHint: false`, `idempotentHint: true`. Preserve current
per-tool evidence; do not force all annotations to match or alter remote permissions.
For score transport errors, preserve results and distinguish failed/unknown/queued status;
do not repeat already acknowledged IDs. See [feedback](feedback.md).
