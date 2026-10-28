# Technical prior-art / 科技查新

## Evidence target

The user may seek one document disclosing all specified technical features. Treat that as
an evidence task, not a guarantee that a novelty-destroying document must exist.
Extract features without weakening numbers, component relationships or operating order.

Create feature IDs F1…Fn for the actual claim: structure, mechanism, sequence, thresholds,
conditions and claimed functional relationships. Keep comparative effect statements distinct
from an implemented mechanism. A matching title, shared purpose or keyword overlap is not
proof of a matching technical solution.

## Retrieval

Use general search for distinctive combinations and source types. For patent or academic
evidence, discover `ip` / `academic` routes; when both web context and specialist sources
are useful, combine one general query and selected vertical queries in a hybrid batch. Search patents and non-patent
sources as requested; do not treat either as universally sufficient. Chinese-only means a
Chinese publication or a verified Chinese-language family member, not an English result with
a translated snippet. For bilingual scope, use technical equivalents and different angles,
not only literal translations.

Retain the user's exclusions for this project. Do not hard-code exclusions from another job.
Keep a small query/evidence ledger in the current task. No background job, automatic upload,
external database write or persistent private-document cache.

## Verify the strongest candidates

For each candidate record: title; author/applicant; identifier; document type; source URL;
document date; verifiable public-availability date; read status; evidence for F1…Fn.
Each feature receives one of: 明确公开 / 有条件或表述不充分 / 未见公开 / 全文未核验.
Give the section/paragraph/claim/page when actually available. Quote only a short decisive
passage, or paraphrase faithfully. Never manufacture page numbers.

Do not combine unrelated embodiments within a document unless it actually teaches their
combination. Do not combine a parent's disclosure with a later family member's added material.
A patent filing or priority date is not automatically a publication date. An undated product
page does not establish pre-cutoff disclosure merely because it is retrievable today.
If no cutoff was given, say the date qualification remains unassessed.

## Report the conclusion before detail

Use these evidence categories:
- 单篇高度接近、待最终核验: all features appear supported, but date/fulltext checks may remain.
- 单篇明确覆盖所列技术特征: only when one inspected document supports every feature and any
  required date condition is substantiated. State the scope; avoid pretending to issue a binding legal ruling.
- 部分相关: name exactly which features are missing. Combining documents is not single-document coverage.
- 未检得符合条件的单篇文件: report the searched scope and gaps; do not assert that none exists anywhere.

Use a compact feature matrix when useful, followed by the user's preferred formal citations.
Do not inflate relevance, invent measured similarity percentages or keep searching indefinitely
just to turn an inconclusive result into a confident one.
