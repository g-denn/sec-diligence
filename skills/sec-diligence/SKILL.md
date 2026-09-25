---
name: sec-diligence
description: Review English-language US SEC filings into a source-first, dated evidence ledger for small and micro-cap due diligence; use to verify disclosures and open questions, not for valuation, screening, or investment recommendations.
metadata:
  short-description: Cited SEC small-cap diligence ledger
---

# SEC Diligence

Build a reproducible diligence ledger from US SEC filings. The outcome is a set of dated, source-linked observations that tells the requester what is disclosed, what can reasonably be inferred, and what remains unknown. It is not a stock pick, fraud label, valuation, screener, market-data workflow, or trading instruction.

## Start with identity and scope

1. Resolve the issuer from legal name plus CIK, or an SEC accession/filing URL. A ticker alone is insufficient. Stop and request clarification if the issuer, CIK, class, filing, or period is ambiguous.
2. State the reviewed filing set and cutoff/as-of date. Use English-language US SEC filings only. For a historical cutoff, include only evidence with an SEC accepted timestamp on or before that cutoff. Do not silently use later amendments, restatements, or subsequent events; list them only as clearly labeled post-cutoff context when the requester asks for it.
3. Retrieve the source document before forming material findings. If a needed filing or quoted passage cannot be verified, record it as unknown; do not fill the gap from memory or a secondary summary.

Read [source hierarchy](references/source-hierarchy.md) before collecting evidence. Read [diligence review areas](references/diligence-review-areas.md) when selecting review areas. Read [output contract](references/output-contract.md) before drafting the final ledger.

## Review method

Prioritize the latest annual report, subsequent quarterly reports, current reports, registration statements, proxy materials, and amendments that affect the cutoff. Search for both direct disclosures and changes across periods. For each material finding:

- quote or tightly paraphrase the relevant disclosure;
- cite the filing type, filed date, section/page or item, stable URL/accession, and the ledger as-of date;
- label the statement **Fact**, **Inference**, or **Unknown**;
- show every calculation as formula plus cited inputs and units; and
- state what source would resolve a material unknown.

Do not infer absence from silence. Do not use a secondary source as proof when an SEC, issuer, or exchange-regulator source is available. Do not call conduct fraud or a scam unless accurately quoting an official finding and citing it.

## Stop conditions

Stop the substantive review and ask for the missing item when identity or filing authenticity cannot be established. Do not produce an aggregate score, a buy/avoid conclusion, a price target, a valuation, a trade, or personalized advice. Keep facts, inferences, and unknowns separate even if that yields an incomplete ledger.

## Deliverable

Return the compact ledger in the exact shape in [output contract](references/output-contract.md). Put the most decision-relevant findings first, followed by open questions and source coverage. A short, well-cited ledger is preferable to exhaustive unsourced commentary.
