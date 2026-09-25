# SEC Red Flags

`sec-red-flags` is an Agent Skill for turning US SEC filings into a compact, cited diligence-risk ledger. It is designed for small and micro-cap research where the real question is often not "what is the price?" but "what must be proven before this deserves more work?"

It does not rank securities, estimate value, screen companies, use market-price data, or give investment or trading recommendations.

## Install

Copy [`skills/sec-red-flags`](skills/sec-red-flags) into a compatible Agent Skills directory, then invoke `$sec-red-flags` with an unambiguous US issuer name plus CIK, or a filing URL/accession number.

```text
Use $sec-red-flags to review Example Microcap Inc. (CIK 0000123456).
Use only the latest 10-K and subsequent 10-Qs. Produce a cited evidence ledger.
```

No API key is required. The workflow uses primary public filing sources; an agent/browser may be needed to retrieve them.

## What makes it useful

- Fails closed on an ambiguous issuer, ticker, CIK, reporting period, or missing source proof.
- Separates filed facts, analyst inferences, and unknowns instead of converting uncertainty into a confidence score.
- Makes every material flag traceable to a filing section/page or an exact SEC filing URL, with an as-of date.
- Covers the recurring small-cap failure modes: going concern and runway, dilution, financing terms, related parties, customer concentration, controls, contingencies, and regulatory disclosures.

Read the [skill](skills/sec-red-flags/SKILL.md), [source hierarchy](skills/sec-red-flags/references/source-hierarchy.md), [taxonomy](skills/sec-red-flags/references/red-flag-taxonomy.md), and [output contract](skills/sec-red-flags/references/output-contract.md).

## Example

The [synthetic sample input](examples/sample-input.md) and [synthetic sample output](examples/sample-output.md) show the expected shape. They are invented training material, not research about a real company.

## Limitations and safety boundary

SEC filings can be incomplete, stale, amended, or ambiguous. This skill is an evidence-organization aid, not an audit, legal opinion, forensic investigation, valuation, or financial advice. It reviews US SEC filings in English only. It must not call a company fraudulent or a scam unless it accurately quotes an official finding and cites that finding.

The output is deliberately a ledger, not an aggregate buy/avoid score. A missing disclosure is recorded as unknown, not treated as evidence that the condition is absent.

## Contributing and security

See [CONTRIBUTING.md](CONTRIBUTING.md) for bounded contributions and [SECURITY.md](SECURITY.md) for reporting security issues. This project is released under the [MIT License](LICENSE).

## Development

```powershell
python scripts/validate.py
python -m unittest discover -s tests -v
python C:\Users\Dell\.codex\skills\.system\skill-creator\scripts\quick_validate.py skills/sec-red-flags
```
