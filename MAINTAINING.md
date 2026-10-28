# Maintaining this integration

Keep the stable plugin name. Use semantic versions and append an accurate changelog entry.
Run the offline checks and package mutation tests before uploading. Use Plugin Creator's
existing plugin ID and current release guard to update a saved plugin; do not create duplicates.
Preserve its existing audience and do not change permissions or sharing while updating content.

No backend fork is maintained. If AnySearch changes schemas, rediscover them through an approved
MCP client, update only the affected references, and run the corresponding real behavior tests.
Do not transform a documentation example into a presumed supported parameter.

Release evidence levels must remain distinct: package validation; remote discovery; real tool
operation; workflow quality; target-host end-to-end. Passing one does not prove the others.
Behavior-case JSON describes planned acceptance checks and is not proof they ran.
A public rollout requires target-host and credential-flow testing plus any platform review.
Do not fabricate publisher support contacts, policy URLs, official affiliation or approval.

Developer scripts are offline and do not auto-run during installation. Do not add heavy
runtime dependencies, a custom proxy or background agents merely to wrap the hosted tools.

On updates, preserve historical snapshots and point evidence/status.json at a new dated
contract_snapshot. Required tools are checked as a subset; additive tools are allowed.
Check annotation types per tool without demanding historical values. Keep behavior-case
definitions separate from dated executions. Any production acceptance claim must be
supported by the required live, authenticated and target-host results.
Update the feedback reference when the provider changes score semantics. Preserve all
default prompts and verify the same skills and connection remain present after saving.
