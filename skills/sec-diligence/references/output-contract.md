# Output contract

Use this order. Keep it compact and do not add a composite rating or investment conclusion.

```markdown
# SEC filing evidence ledger — [Issuer legal name] ([CIK])

**Scope:** [forms and reporting periods reviewed]
**As of:** [YYYY-MM-DD]
**Identity proof:** [SEC company/filing URL and CIK match]

## Material disclosed risks

### [Neutral risk label]
- **Fact:** [specific disclosed statement].
  - **Citation:** [Form, filed date, SEC accepted timestamp, section/item/page, accession or stable URL].
- **Inference:** [narrow reasoning from the fact, or `None`].
- **Calculation:** [formula = inputs; units; source citations], or `Not applicable`.
- **Unknown:** [what cannot be established; source that could resolve it].

## Open questions and coverage gaps
- [Question, why it matters, and the source needed to resolve it.]

## Sources reviewed
- [Form, filed date, reporting period, URL/accession.]
```

Rules:

- Use the labels **Fact**, **Inference**, and **Unknown** for each material item. Facts are filed disclosures; inferences are analysis; unknowns never imply zero.
- Cite each material fact exactly enough to reproduce it. An as-of date is required even for historical filings.
- For a historical cutoff, the cited SEC accepted timestamp must be on or before the cutoff. Keep later amendments or subsequent events out of the historical evidence set unless separately labeled as post-cutoff context.
- A derived figure must show the formula, inputs, units, and source. If an input is not comparable, do not calculate.
- Use neutral labels. Do not declare fraud or scam absent an accurately quoted official finding.
