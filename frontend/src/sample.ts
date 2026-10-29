// Fictional, reproducible input; never presented as current reporting.
export const sampleSources=[
  {
    "title": "Sample · Cedar Labs release note",
    "url": "https://example.com/cedar/release",
    "kind": "article",
    "reliability": "unverified",
    "content": "FICTIONAL DEMO SOURCE. Cedar Labs released a small language model for local document classification. The release note says the model can run on a laptop with 16 GB of memory. The team reports a benchmark result but has not published a reproducible evaluation. Commercial licensing has not yet been clarified."
  },
  {
    "title": "Sample · Independent evaluation",
    "url": "https://example.com/cedar/evaluation",
    "kind": "report",
    "reliability": "unverified",
    "content": "FICTIONAL DEMO SOURCE. A small independent test compared the Cedar model on 200 synthetic support tickets. The evaluator reported that the model handled short labels more consistently than long explanations. The test used one laptop and should not be generalized to every workload. The test did not evaluate privacy or licensing."
  },
  {
    "title": "Sample · Developer field note",
    "url": "https://example.com/cedar/field-note",
    "kind": "tweet",
    "reliability": "unverified",
    "content": "FICTIONAL DEMO SOURCE. A developer described a local prototype that sorts sample documents before human review. The developer said setup required manual configuration. This is a personal observation, not a controlled benchmark. Production performance and legal suitability remain untested."
  }
];
export const sampleDraft="A smaller model, a more careful decision\n\nThis is a fictional editorial sample for testing the workspace. Cedar Labs, its model, and the evaluation described here are invented. The example links are placeholders, not evidence of real announcements.\n\nCedar Labs says its new language model can classify documents on a laptop with 16 GB of memory. That is an interesting starting point for teams exploring local tools, but it does not establish that the model is ready for production. The release note describes a benchmark without a reproducible evaluation, and commercial licensing remains unclear. Those gaps matter as much as the headline capability.\n\nAn independent evaluator tested 200 synthetic support tickets on one laptop. Short labels appeared more consistent than long explanations. The test was conducted on a limited dataset. A single setup cannot tell us how the model will behave with a different language, document format, or hardware configuration. It is important to note that the test did not assess privacy or licensing.\n\nA developer field note adds another perspective: a local prototype sorted sample documents before human review. Setup required manual configuration. That observation suggests a possible workflow, but it remains a personal account rather than a controlled measurement. It should not be used to promise production performance.\n\nFor builders, the practical next step is a small, reversible trial. Use non-sensitive documents in order to compare classification quality with an existing baseline, record latency and memory use, and inspect the errors before making a decision, and keep a person in the loop when a wrong label could have consequences. Teams should also check the license and understand what data leaves the machine during installation and operation.\n\nOur editorial angle is simple: local availability is a reason to investigate, not a substitute for evidence. The useful question is whether the tool improves one specific workflow under conditions a team can reproduce. Until the missing evaluation and licensing details are available, any broader recommendation would go beyond these sources.\n\nSources: Sample Cedar release note; sample independent evaluation; sample developer field note. All three inputs are fictional and supplied only to demonstrate the research-to-editing workflow.";
