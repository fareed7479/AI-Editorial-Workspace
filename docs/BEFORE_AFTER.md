# Before and after | Reviewed editorial decisions

**Purpose:** demonstrate how individual writing suggestions can improve clarity while retaining the original meaning and technical qualifications.

[Documentation guide](README.md) · [Product behavior](PRODUCT.md) · [Writing implementation](../backend/app/writing.py) · [Newsletter sample](SAMPLE_NEWSLETTER.md)

> **Example status:** illustrative text with explained editorial decisions. This is not a Gemini output, an automated replay of the exact decision sequence, or a measured model evaluation.

## Original

> The model was tested by our team in order to understand whether it could label support tickets reliably, and we really wanted to retain every qualification about hardware, memory, licensing and evaluation coverage before recommending the system.

## Reviewed revision

> Our team tested the model to understand whether it could label support tickets reliably. And we wanted to retain every qualification about hardware, memory, licensing and evaluation coverage before recommending the system.

## Decisions and rationale

| Check | Original passage | Reviewed change | Why / qualification |
| --- | --- | --- | --- |
| Filler phrase | in order to | to | Shorter phrasing without adding a claim |
| Filler phrase | really | Remove | Optional emphasis; keep it if the author intends it |
| Long sentence | Clause ending reliably, and… | Split after reliably | Separate the evaluation purpose from the qualifications |
| Passive candidate | The model was tested by our team | Our team tested the model | The actor is already identified; no actor is invented |

The second sentence retains **And** to show the conservative clause split used by the current rule. An editor may remove it in a subsequent manual edit. The example does not imply that every passive sentence should be rewritten.

## Try the example in the workspace

1. Create a project and paste the original into **Writing studio**.
2. Choose **Save & check writing**. The app preserves the first saved text as the original.
3. Review and accept the filler suggestions if their meaning suits the author.
4. Run checks again: accepting a filler inside a long/passive passage makes overlapping suggestions stale.
5. Review the sentence split. Run checks again, then supply a passive rewrite that uses the explicitly named team.
6. Open **Compare revisions** to inspect original/current text, counts, and previous saved versions.

Depending on edit order, the intermediate wording and number of saved versions can differ. The final paragraph can also be entered as a reviewed manual edit. Rejecting a suggestion changes its status without changing the text.

## Meaning-preservation checklist

- [x] The purpose remains evaluating support-ticket classification.
- [x] Reliability remains a question, not an established result.
- [x] Hardware, memory, licensing, and evaluation qualifications remain present.
- [x] A recommendation remains conditional on review.
- [x] The actor comes from the original text.

Metrics may change, but shorter prose alone does not prove editorial quality. Accepted/manual edits retain previous saved text; history is inspectable, with no automatic restore feature. Actual tested behaviors are recorded separately in [TESTING.md](TESTING.md).
