# Integrity Checklist

Report each violation with its location.

## Terms and References

- A defined term that never appears in the body.
- A capitalized domain term in the body that is not defined.
- A concept with two names, or a name used for two concepts.
- A cross-reference to a section that does not exist or no longer supports the claim it is cited for.
- A Blocking Decisions entry that cites no section, or cites a section that no longer exists or no longer depends on or presumes an answer to the decision.
- An Open Decisions entry that cites no section, or that text in the spec already depends on.
- An em dash, a table, or an RFC 2119 keyword.

## Rules

- A rule whose wording admits two readings.
- Two rules that give different answers for the same case.
- A structural technical decision without its justification or trade-off.
- A sentence that changes neither what is built nor why a rule exists.

## Axioms

- An axiom longer than one sentence or stating a mechanism.
- An axiom carrying an exception: a carve-out for a specific case, actor or situation. A boundary clause that limits scope by a general, uniform condition is allowed.
- Two axioms where fully honoring one requires limiting the other, with no boundary clause resolving it.
- An axiom that cites no core requirement, or cites one that does not exist.

## Proportion

- A section more precise than the decisions it depends on.
- A section accumulating special cases about another section.

## Deferred
- An Deferred entry that does not state what keeps it possible, or that text in the spec prevents.
