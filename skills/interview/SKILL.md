---
name: interview
description: A relentless interview to sharpen a plan or design.
disable-model-invocation: true
---

Interview me relentlessly about every aspect of this until we reach a shared understanding. Walk down each branch of the decision tree, resolving dependencies between decisions one-by-one. For each question, provide your recommended answer.

If the arguments start with `brief`, run a brief interview instead: cover every branch of the decision tree, but only its upper levels (e.g., the structural forks such as approach, scope, and major tradeoffs). Do not descend into lower-level details. Leave them out of the questions and the final summary; they get settled later. Everything else below still applies.

Before the first question, explore the environment, then calibrate the session in one message:
- Open with one or two sentences restating the task, to show you understand it. Do not list what you found while exploring; raise each finding later, as a question, when its branch comes up.
- Then a numbered list of calibration questions, each with your recommended answer:
  1. Ambiguities in the request, or what prompted it.
  2. The criteria for judging options.
  3. How deep to grill me. Omit this in brief mode.
  4. What the deliverable is when we're done.
- Keep each item concise and focused

After calibration, ask the questions one at a time, waiting for feedback on each question before continuing. Asking multiple questions at once is bewildering.

If a _fact_ can be found by exploring the environment (filesystem, tools, etc.), look it up rather than asking me. The _decisions_, though, are mine — put each one to me and wait for my answer.

Do not act on it until I confirm we have reached a shared understanding.
