# Search feedback

The current MCP service requests a `score` for each successful `search` and each
successful `batch_search` member, including empty results. Failed searches, extraction
and domain discovery do not count. This is provider feedback, not a rating of the user.

Keep a task-local pending list. Copy each actual request_id from `_meta.request_id`,
the corresponding `_meta.request_ids` entry, or the result's trailing YAML block.
Never invent an ID or submit a private query, document, conversation, key or local path.
If no ID is available, record that feedback cannot be submitted for that result.

Submit at ten pending successful searches before starting another search. If more than
ten arrive together, send batches of at most ten. At the end of this interaction turn's
searching, submit every remainder before the final answer, even for one search. Later
searches create new pending entries. Do not carry unsent feedback into a later user turn.

Call shape: `score(feedbacks=[{request_id: actual_id, score: 3}])`.
Use 1–10 entries, with one integer score per ID. Judge against the actual information need:

| Score | Result quality |
| --- | --- |
| 5 | Fully answers; no additional search or extraction needed. |
| 4 | Mostly answers; minor gaps do not block the answer. |
| 3 | Partly answers; further search or extraction needed. |
| 2 | Largely insufficient; only a small part is usable. |
| 1 | Unusable, unrelated or empty. |

Do not default all searches to 5. Never resend IDs already acknowledged as queued.
`queued` means received for processing, not confirmed database persistence. Check rejection
counts and per-entry errors when returned. Feedback is documented as free.
Respect host permission decisions; feedback is a non-destructive write. On transport
failure, preserve the pending/unknown status and usable research. Do not blindly retry
a possibly received submission; one deliberate retry is appropriate only when a clearly
transient failure and the current idempotent contract justify it. Do not bypass a denial.
