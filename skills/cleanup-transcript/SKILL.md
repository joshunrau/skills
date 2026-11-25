---
name: cleanup-transcript
description: Clean up a transcript the user provides, fixing speech-recognition errors and marking uncertain fixes with confidence tags.
disable-model-invocation: true
---

# Clean Up a Transcript

Produce a cleaned copy of a transcript. You orchestrate: delegate all reading and editing to Sonnet subagents, and do not read the transcript's content yourself.

## Ground Rules

- **Input:** an attached file, a file path, or pasted text. If there is none, ask for it and stop.
- **Output:** never modify the original (work on a copy of an upload). Write `<original-name>_cleaned.<ext>` next to it in the same format, or `transcript_cleaned.md` for pasted text.
- **Preserve:** the transcript's language (no translating) and its structure: headings, timestamps, speaker-label format, paragraph and turn breaks.

## Workflow

1. **Map.** A subagent samples the start, middle and end and reports the speaker-label format, the timestamp format, section boundaries, and any non-transcript content (summaries, notes, metadata).
2. **Glossary.** A subagent reads the whole input (in segments if large) and writes `glossary.md` next to the output: one canonical spelling per person, organization, place, product, technical term and acronym, with the variants found. It uses real-world knowledge for proper names. If it can't tell whether two variants are the same entity, it lists them separately and notes the doubt.
3. **Correct.** Up to about 30k words, use one subagent. Above that, split with a script at sections, then speaker turns (never mid-turn), into chunks of a few thousand words and correct them in parallel. Every corrector gets the structure map, the glossary and the correction rules below.
4. **Review.** A fresh subagent that did not do the correcting compares each corrected chunk with its original, assuming the corrector over-inferred. It may only revert a change or downgrade a tag (`likely` → `plausible`, adding `| orig: Y`). It never adds corrections, rewords, or deletes original text. Its output is final.
5. **Deliver** the cleaned file and the glossary.

## Correction Rules

Confidence tiers:

- **Fix silently:** typos, homophones, misspellings, glossary normalizations.
- **`[likely: X]`:** the original is clearly wrong, and context or domain knowledge makes X highly probable.
- **`[plausible: X | orig: Y]`:** a reasonable guess that context does not settle. Always keep the original Y.
- **`[UNINTELLIGIBLE]`:** no reasonable guess. Replace the garbled text with this tag.

Applying them:

- Between two tiers, choose the less confident one.
- If most of a sentence needs tags, tag the whole sentence once.
- Unusual is not wrong: slang, jargon, dialect and odd phrasing stay.
- Numbers, negations ("can" vs "can't") and names change meaning. Never fix them silently unless the glossary settles it; use `[likely]` or lower.

By content type:

- **Transcript:** also remove fillers (um, uh, filler "like" and "you know", and their equivalents in the transcript's language), stutters and false-start repeats. Fix punctuation and capitalization. Correct wrong speaker labels using the same tiers (e.g. `[likely: Interviewer]:`). Change no other wording: no smoothing, rephrasing or summarizing.
- **Other content** (summaries, notes, metadata): fix errors only. Keep its shorthand, fragments and formatting.
