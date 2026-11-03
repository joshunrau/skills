# Integrity Checklist

Report each violation with its location. The body is every section except Definitions.

## Terms and References

- A defined term that never appears in the body.
- A capitalized domain term in the body that is not defined.
- A term defined inline in one top-level section and used in another.
- A term in Definitions used in only one top-level section.
- A concept with two names, or a name used for two concepts.
- A cross-reference to a section that does not exist or no longer supports the claim it is cited for.
- A sentence that relies on a rule in an earlier section without that section's number, or a citation that is not a bare section number in parentheses at the end of the clause.
- A Blocking Decisions entry that cites no section, or cites a section that no longer exists or no longer depends on or presumes an answer to the decision.
- An Open Decisions entry that cites no section, or that text in the spec already depends on.

## Rules

- A rule whose wording admits two readings.
- Two rules that give different answers for the same case.
- A sentence in a behavior section or a Structural Technical Decision that does not change what is built.

## Axioms

- An axiom longer than one sentence or stating a mechanism.
- An axiom carrying an exception: a carve-out for a specific case, actor or situation. A boundary clause that limits scope by a general, uniform condition is allowed.
- Two axioms where fully honoring one requires limiting the other, with no boundary clause resolving it.
- An axiom that cites no core requirement, or cites one that does not exist.

## Proportion

- A section more precise than the decisions it depends on.
- A section accumulating special cases about another section.

## Style

- A rationale clause: "because", "so that", "therefore", "this serves", or a trade-off.
- A sentence in the body that restates an axiom or cites one.
- A core requirement cited outside Axioms.
- A rule written in two places.
- A consequence that follows from rules already stated.
- A closure clause: a clause whose only content is that nothing beyond the rule happens or exists ("and nothing else", "and no other"). Not a clause that gives everything outside the rule an outcome, and not a lead sentence stating that a set is closed.
- A bare citation to a later section. Not a sentence that says what the later section covers, such as "The authorization mechanism is described in 5.1."
- A paragraph of more than six sentences, not counting a case list that follows its lead sentence.
- A fixed set of cases written as prose rather than as a list with a bold label per case.
- A quantifier with no noun ("everything", "anything", "whatever") or a clause standing in for a set, with no enumeration of the set in that sentence or the one before.
- An example of a rule that is already exact in words.
- Bold anywhere but a term's definition or a list label; italics on anything but an enumerated value with no literal form; a code span on anything that is not literal text.
- The system being specified as the subject of a sentence whose rule governs a specific input, item or actor.
- An em dash, a table, or an RFC 2119 keyword.

## Deferred

- A Deferred entry that does not state what keeps it possible, or that text in the spec prevents.
