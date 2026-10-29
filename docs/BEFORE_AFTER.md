# Before / after with explicit editorial decisions

## Original

The model was tested by our team in order to understand whether it could label support tickets reliably, and we really wanted to retain every qualification about hardware, memory, licensing and evaluation coverage before recommending the system.

## Revised

Our team tested the model to understand whether it could label support tickets reliably. And we wanted to retain every qualification about hardware, memory, licensing and evaluation coverage before recommending the system.

## Decisions

| Check | Passage | Explanation | Decision |
| --- | --- | --- | --- |
| Filler phrase | in order to | Shorter phrasing | Accept: to |
| Filler phrase | really | Optional emphasis | Accept: remove |
| Long sentence | Original sentence | More than 25 words | Accept clause split after reliably; preserve all qualifications |
| Passive candidate | The model was tested by our team | Actor is explicitly present | Editor rewrite: Our team tested the model |

Apply filler edits first, then rerun checks because the long/passive suggestions overlap. Perform the long-sentence split, rerun checks, and provide the reviewed passive rewrite. The final second sentence deliberately retains And to preserve the rule's conservative split; an editor could subsequently remove it. The app does not claim this sample is a measured readability improvement or a real model evaluation.

The original persists in Compare Revisions, and every accepted/manual edit adds a prior saved version. A rejection leaves text unchanged. The UI also lets the editor change suggested text before accepting.
