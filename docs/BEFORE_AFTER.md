# Before and after

**Assignment Part C ? Reproduced with the application's writing engine**

[Docs](README.md) ? [Final newsletter](SAMPLE_NEWSLETTER.md) ? [Requirements](REQUIREMENTS.md)

> [!NOTE]
> This is an actual deterministic service run, not Gemini output or a captured browser session. The editor chose two filler removals; the script calls the same analyze/decide functions used by the API and checks the result, original preservation, numeric values and citations.

## Feedback and editorial decisions

| Exact passage | Accepted change | Application feedback |
| --- | --- | --- |
| `really ` | Remove | Shorten this phrase. Check that the emphasis still matches your meaning. |
| `very ` | Remove | Shorten this phrase. Check that the emphasis still matches your meaning. |

The editor removes optional emphasis without changing the release, hardware claim, source attribution or proposed evaluation. Long-sentence flags remain for review: technical context is retained rather than shortened automatically. A lower word count alone is not evidence of better writing.

| Metric | Original | Revised |
| --- | ---: | ---: |
| Words (body only) | 344 | 342 |
| Average sentence words | 13.8 | 13.7 |
| Reading minutes | 1.7 | 1.7 |
| Saved revisions | 0 | 2 |

## Original draft

OpenAI released two open-weight language models, gpt-oss-120b and gpt-oss-20b, under the Apache 2.0 license. The announcement describes models that developers can run and customize on their own infrastructure. OpenAI also reports reasoning benchmark results, but those publisher-reported comparisons should not be mistaken for an independent evaluation of your application. [1]

For readers considering local inference, the smaller model is really the more immediate starting point. Its model card describes a 21-billion-parameter mixture-of-experts model with 3.6 billion active parameters. OpenAI says its quantized weights can fit within 16 GB of memory. Treat that as a deployment claim with conditions to investigate, rather than a promise about speed or reliability on every laptop. [3]

The repository adds a practical qualification: these models require the Harmony response format. A developer cannot assume that any existing plain-text prompt pipeline will work correctly without adaptation. The documentation also describes configurable reasoning effort, allowing teams to choose among low, medium and high settings. That gives evaluators another variable to hold constant when comparing results. [2]

**Our analysis:** access to model weights changes who controls deployment and customization. It does not automatically settle whether a model is the right choice. A useful pilot should begin with a very specific task and a clear baseline, rather than a broad claim that local models replace hosted services. For a document-labeling workflow, an editor or engineer could measure classification errors, memory use and response time using representative, non-sensitive inputs.

Keep the first experiment reversible. Record the model version, inference implementation, hardware and reasoning setting alongside the results. Inspect difficult examples and decide in advance what error rate would make the workflow unacceptable. These are proposed evaluation steps, not measurements performed for this article.

The editorial takeaway is to separate availability from suitability. The announcement, implementation repository and model card explain what the publisher released and how it expects developers to use it. All three come from the same organization, so they do not supply independent corroboration. Before making a production recommendation, seek outside evaluations and test the exact workflow readers care about.

## Revised draft

OpenAI released two open-weight language models, gpt-oss-120b and gpt-oss-20b, under the Apache 2.0 license. The announcement describes models that developers can run and customize on their own infrastructure. OpenAI also reports reasoning benchmark results, but those publisher-reported comparisons should not be mistaken for an independent evaluation of your application. [1]

For readers considering local inference, the smaller model is the more immediate starting point. Its model card describes a 21-billion-parameter mixture-of-experts model with 3.6 billion active parameters. OpenAI says its quantized weights can fit within 16 GB of memory. Treat that as a deployment claim with conditions to investigate, rather than a promise about speed or reliability on every laptop. [3]

The repository adds a practical qualification: these models require the Harmony response format. A developer cannot assume that any existing plain-text prompt pipeline will work correctly without adaptation. The documentation also describes configurable reasoning effort, allowing teams to choose among low, medium and high settings. That gives evaluators another variable to hold constant when comparing results. [2]

**Our analysis:** access to model weights changes who controls deployment and customization. It does not automatically settle whether a model is the right choice. A useful pilot should begin with a specific task and a clear baseline, rather than a broad claim that local models replace hosted services. For a document-labeling workflow, an editor or engineer could measure classification errors, memory use and response time using representative, non-sensitive inputs.

Keep the first experiment reversible. Record the model version, inference implementation, hardware and reasoning setting alongside the results. Inspect difficult examples and decide in advance what error rate would make the workflow unacceptable. These are proposed evaluation steps, not measurements performed for this article.

The editorial takeaway is to separate availability from suitability. The announcement, implementation repository and model card explain what the publisher released and how it expects developers to use it. All three come from the same organization, so they do not supply independent corroboration. Before making a production recommendation, seek outside evaluations and test the exact workflow readers care about.

## Sources and reproduction

Both versions use the three attributed links in [the final newsletter](SAMPLE_NEWSLETTER.md#sources-and-provenance). They are a dated retrospective, not current-week reporting. The first saved text remains original; each accepted edit stores its prior version.

~~~powershell
.\.venv\Scripts\python.exe scripts/build_sample_comparison.py
~~~

This command rewrites this document and checks the expected result. It makes no network/model calls and changes no workspace data. To inspect the same behavior visually, paste the original into a new project, Save & check writing, review each filler removal, then open Compare revisions.

