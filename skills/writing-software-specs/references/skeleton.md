# Spec Skeleton

Each heading below is followed by what belongs there. Behavior sections take domain names and their own numbers. Omit Operational Policy when nothing in it affects behavior. Omit Blocking Decisions or Open Decisions when it has no entries.

### **1. Overview.**

**1.1 Purpose.** What the software is, what it replaces, whom it serves, and the outcome it delivers. One short paragraph.

**1.2 Target Setting.** The people who use it, their roles, and the conditions that shape their needs, such as turnover, permissions or skill level. Describe people and conditions, never features.

**1.3 Core Requirements.** A short list of needs, numbered R1, R2 and onward, each stated as what a user can do or rely on. Every axiom cites one of these. A requirement that pulls against another is resolved here first.

**1.4 Out of Scope.** What the software does not serve, as a list.

### **2. Definitions.**

One bullet per term: the bold term, then what it means. Definitions name concepts and contain no behavior and no technical choices. A category is defined by a criterion, not by listing its members.

### **3. Axioms.**

One bullet per axiom, numbered A1, A2 and onward, each a bold short name followed by one sentence that ends by citing its core requirement. Expect three to seven.

### **4. {Behavior Area}.**

User-facing behavior for one area of the domain. Repeat as needed, ordered so that each area depends only on areas before it.

### **N. Structural Technical Decisions.**

Only decisions the implementation builds on and that are costly to reverse. Each states its choice, the behavior or constraint it serves, and the trade-off it accepts.

### **N. Operational Policy.**

Operational rules that affect user-facing behavior, such as retention or availability.

### **N. Blocking Decisions.**

Deferred decisions that text already in the spec conflicts with or depends on, most blocking first. Each entry is the question, then the sections it affects. While any entry exists, the spec changes only to resolve entries.

### **N. Open Decisions.**

Deferred decisions that no text in the spec depends on yet. Each entry is the question, then the sections it would affect. Text that would depend on an entry is not written until the entry is resolved.
