---
name: code-review
description: 'Review the code a request names in a TypeScript project, or the uncommitted changes when it names none, along several axes, each in its own sub-agent. Writes a report; changes no code. Use when the user, or a plan the user wrote, asks for a code review by name.'
---

Code review along several axes, each in its own sub-agent so that no axis colors another:

- **Correctness**: does the code do what it evidently means to, safely?
- **Conformance**: does it do what the product specification asks?
- **Standards**: does it follow the rules the project writes down?
- **Complexity**: is it more complicated than its purpose justifies, and is the cause the code, a lint rule, a guideline or the product specification?

Each axis has a reference file that briefs its reviewer: `references/<axis>.md`, named for the axis in lower case.

Conformance and Standards take their sources as authorities. Complexity treats the same sources as suspects that can be wrong. When the two disagree about one piece of code, the report keeps both findings: the pair is evidence that a rule should change.

A second sub-agent then tries to refute each Correctness and Conformance finding, and marks the ones that should block a merge or a commit. Standards and Complexity findings are not verified and never block: they cost the next reader of the code, not a user.

The inspection changes no code. It runs no type check, linter or test, and assumes that all three have passed.

`<skill-dir>` below is this skill's directory, as an absolute path.

## Orchestration

### 1. Select the Files

The request is in plain words. Read it for what to inspect:

- **Code as it stands**: the request names code, such as a function, a module or a directory. Find the paths it means.
- **Changes**: the request asks about what changed. The base is the git ref it names. When it names none, the base is the default branch for a branch's changes and `HEAD` for the uncommitted changes.

A request that names nothing to inspect asks for the uncommitted changes. When you cannot tell which code or which changes a request means, ask.

The request may also name a plan document, which says what the code is meant to do.

Being asked for an inspection permits `git rev-parse`, `git merge-base` and `git diff` against the base, and no other reading of git history: no `git log`, no commit messages.

From the repository root, run the script with the paths, or with the base:

```sh
python3 <skill-dir>/scripts/select_files.py <path>...
python3 <skill-dir>/scripts/select_files.py --base <base> [<path>...]
```

It keeps the code files, which it recognizes by extension (`CODE_EXTENSIONS` in the script), under the paths, or those changed since `git merge-base <base> HEAD`, working tree included. When the request asks about the changes to one part of the codebase, pass that part's paths after the base. It drops three kinds of code file:

- **Tests**: a file whose name contains `.test.` or `.spec.`, and every file under a directory named `__tests__`, `__mocks__`, `test`, `tests`, `testing` or `e2e`.
- **Stories**: a file whose name contains `.stories.`.
- **Generated**: a file that `.gitattributes` marks `linguist-generated`.

To keep a dropped file, pass its own path, or for a file under a test directory, that directory or a path inside it, and only when the request asks for it. A file that is not code, such as a JSON config, is kept only by its own path. With a base, pass these paths alongside `.` or the part's paths, because every path after the base narrows the changes.

It prints JSON, with `base` in ref mode only, and with the number of code files it dropped under `excluded`:

```json
{
  "base": "<sha>",
  "mode": "ref",
  "fileCount": 2,
  "lineCount": 180,
  "excluded": { "tests": 3, "stories": 0, "generated": 1 },
  "files": ["src/index.ts", "src/parse.ts"]
}
```

Empty `files` ends the inspection: say so, with the `excluded` counts.

### 2. Find the Sources

`AGENTS.md` gives the path of each source under `## Reference Files`: the product specification, the coding guidelines, the lint rules, which describe what the project's linter enforces, and the scratch directory. A project that does not list one of the first three has none: never ask for it. Ask the user for the scratch directory when it is not listed.

Correctness and Complexity run in every inspection. The other two run only with an authority:

- **Conformance**: the project has a product specification, or the request names a plan.
- **Standards**: the project has an `AGENTS.md`.

### 3. Spawn the Reviewers

Spawn one sub-agent per axis that runs, all in one message so that they run in parallel. Each starts with no context but its prompt, and can read files and run commands: in Claude Code, a `general-purpose` agent on Opus. Each prompt reads:

> Follow "Reviewer Rules" in `<skill-dir>/SKILL.md` and `<skill-dir>/references/<axis>.md`. Mode: `<mode>`. Base: `<base>` (ref mode only). Specification: `<path>` (Conformance and Complexity only). Guidelines: `<path>`. Lint rules: `<path>` (Standards and Complexity only). Plan: `<path>` (Correctness and Conformance only). Files: `<files>`.

`<mode>`, `<base>` and `<files>` are the script's output: `<base>` is the commit it printed, not the ref the request named. Leave out the line of a source the project lacks, and the Plan line when the request names no plan.

### 4. Verify Correctness and Conformance

For Correctness and for Conformance, spawn one more sub-agent of the reviewers' kind to test that axis's findings, both in one message. Skip an axis that has no findings. Each prompt reads:

> Follow "Verifier Rules" in `<skill-dir>/SKILL.md`. Axis reference: `<skill-dir>/references/<axis>.md`. Mode: `<mode>`. `<the Specification, Guidelines and Plan lines of that axis's reviewer prompt>` Findings: `<the findings, exactly as the reviewer returned them>`.

### 5. Write the Report

Apply the verifiers' verdicts first. A Refuted finding leaves its axis's findings. Every other Correctness and Conformance finding gains, under its Recommended Fix, its `Verdict:` line and, when the verifier gave one, its `Blocking:` line.

Keep each axis's remaining findings in the order its reviewer returned them, and number them within their axis; for Complexity, within each cause group. Collect the reviewers' Noticed lines into one list.

Never merge or rank findings across axes; link them instead. When findings on different axes concern the same code, end each with a line naming the others, such as `See also: Standards 3, Complexity (Lint Rule) 2.`

Write the report to `code_inspection_<timestamp>.md` in the scratch directory, where `<timestamp>` is `date +%Y%m%d-%H%M%S`:

```markdown
# Code Inspection: <what was inspected>

<mode, file count, total lines of those files and the `excluded` counts>

Blocking: <the Blocking findings by axis and number, such as "Correctness 1, Conformance 3", or "None.">

## <Axis>

## Noticed, Out of Scope
```

The report has one `## <Axis>` section per axis, in the order of the list above. The section of an axis that did not run says "Not run:" and names the authority the inspection lacked. The Complexity section holds one `###` sub-section per cause group: Code, Lint Rule, Guideline and Specification, the last only when the project has a product specification. A Correctness or Conformance section with Refuted findings ends with a `### Refuted` sub-section: each finding's claim, followed by the verifier's reason. A section with no findings says "None." In paths mode, omit Noticed. Paths are relative to the repository root.

Reply with the report's path and one line: the number of findings per axis, the worst finding in each, and the Blocking findings.

## Reviewer Rules

You review one axis over the files listed in your prompt.

1. Read `AGENTS.md`, then the sources your axis's reference file names, at the paths your prompt gives. Skip a source your prompt gives no path for: the project lacks it.
2. Read every listed file in full. Read anything else you need for context, such as callers and the rest of the module.
3. Scope your findings by mode:
   - `paths`: any line of the listed files.
   - `ref`: run `git diff <base> -- <files>` (an untracked file is new in full). The request for this inspection permits this command and no other reading of git history. Findings concern changed code, and code the change makes wrong, wherever that code is. Under Noticed, write one line for each problem on your axis in the listed files that predates the change.
4. Stay on your axis; each of the others has a reviewer of its own. Test coverage is out of scope. Assume the type check, the linter and the tests have passed: a type error, a lint violation or a failing test is not a finding, and you run none of the three. Run nothing that changes files.
5. Verify every finding before returning it: re-read each location, trace the callers or data flow the claim rests on, and check every quote against its source word for word. Drop or correct what does not hold.
6. Return your findings in the format below, ordered as your axis's reference file says, followed by your Noticed lines.

### Finding Format

```markdown
**<n>. <The claim, in one sentence.>**

Location(s):

- `<path>:<line or range>`

Finding(s): <What the code does and why it matters, in a few sentences. Include one or two sentences of context, such as what the code is for and where it sits, so a reader unfamiliar with the code can follow. Name identifiers; leave line numbers to Location(s).>

Clause: <the section number and the quoted sentence of the product specification or the plan, when a clause applies.>

Rule: <the source file and the quoted rule, when a rule applies.>

Recommended Fix: <the change to make.>
```

Location(s) holds only `path:line` entries, always as a list. Omit Clause or Rule when none applies. The fix for a finding in a file that a tool generates from another, such as a migration generated from a schema, is a change to the source, never an edit to the generated file.

## Verifier Rules

You test one axis's findings, listed in your prompt. Their reviewer has checked them once; you did not write them, and your job is to find the ones that are wrong.

1. Read `AGENTS.md`, then the axis reference your prompt names and the sources it names, at the paths your prompt gives. Skip a source your prompt gives no path for: the project lacks it.
2. Try to refute each finding. Read every file it locates in full, trace the callers or data flow the claim rests on, and check every quote against its source word for word. For a Conformance finding, also search the product specification and the plan for a clause the finding overlooks.
3. Give each finding one verdict:
   - **Confirmed**: you followed the claim through the code and it holds.
   - **Refuted**: the claim is false, or the axis reference excludes it.
   - **Unverified**: you could neither confirm nor refute it.
4. Mark a Confirmed or Unverified finding **Blocking** when, taking its claim as true, shipping the code as it stands would harm a user or the data: a wrong result, data lost or corrupted, data reaching someone not permitted to see it, access wrongly granted, or behaviour a user would meet that contradicts the clause the finding quotes.
5. Add no findings of your own. Run nothing that changes files, run no type check, linter or test, and read no git history.
6. Return one entry per finding, in the order given and in the format below.

### Verdict Format

```markdown
**<n>.** Verdict: <Confirmed, Refuted or Unverified>. <What you checked and what it showed, in one or two sentences.>

Blocking: <The harm, in one sentence.>
```

Omit Blocking unless the finding is Blocking.
