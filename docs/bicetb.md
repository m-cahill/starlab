# Build It Clean Enough to Buy

## Core posture

The project should be built so that a serious acquirer could understand it, trust it, and diligence it without discovering structural messes that make a deal unattractive.

This does **not** mean building like a large company from day one. It means building so that the project is:

* ownable
* legible
* separable
* defensible
* maintainable
* low-friction to diligence

The standard is not “make it look corporate.”
The standard is:

> Make it clean enough that a diligence team can say yes without having to excuse avoidable chaos.

This posture should shape decisions around licensing, openness, provenance, contributor policy, documentation, branding, dependency hygiene, and public/private boundaries.

---

## The main principle

Optimize for **acquirability**, not just impressiveness.

A technically impressive system can still be unattractive to buy if it has:

* unclear IP ownership
* contaminated licensing
* weak data provenance
* messy contributor history
* undocumented boundaries
* inseparable core and non-core assets
* public claims that exceed evidence

A buyer can tolerate limited polish and incomplete scope far more easily than they can tolerate ambiguity about ownership, rights, obligations, and maintainability.

So the project should aim to be:

* technically strong
* strategically interesting
* legally clean
* operationally legible

---

## What “clean enough to buy” means in practice

A clean acquisition-ready posture means a buyer can answer the following questions quickly and confidently:

### Ownership

* Who created this?
* Who owns the code?
* Who owns the docs?
* Who owns the datasets, replays, labels, and weights?
* Are there any ambiguous contributions?

### Licensing

* What license governs the public surfaces?
* What third-party dependencies exist?
* What obligations do those dependencies impose?
* Is there any copyleft contamination?
* Are public and private components cleanly separated?

### Provenance

* Where did every important asset come from?
* What is first-party vs third-party?
* What is redistributed vs merely referenced?
* Are dataset/replay rights explicit?
* Are benchmark assets and generated artifacts tracked clearly?

### Maintainability

* Can a new team understand the system without the founder present?
* Are module boundaries clear?
* Are contracts explicit?
* Are artifacts, schemas, and outputs documented?
* Are known risks and non-goals recorded honestly?

### Separation

* What is the crown-jewel core?
* What is public signal surface?
* What is replaceable?
* What is downstream?
* What is optional vs required?

That is the standard the project should target.

---

## Licensing posture

Licensing is one of the earliest and most consequential decisions if acquisition is a desired outcome.

### Guiding rule

Acquirers do not primarily care whether something is open or closed.
They care whether it is **clean**.

### Clean options

These are generally the safest categories:

* Apache-2.0
* MIT
* fully private / closed
* carefully designed hybrid open/private posture

### Riskier options

These create more acquisition friction unless there is a very deliberate reason to use them:

* GPL
* AGPL
* copyleft-heavy dependency chains
* unusual custom licenses that create interpretive friction
* mixed or unclear licensing across major subsystems

### Recommended acquisition-aware default

Use one of two paths:

#### Option A — Open flagship

Best when the goal is:

* public credibility
* talent magnetism
* adoption
* strong external signal

Typical posture:

* Apache-2.0
* public docs
* public standards and formats
* public benchmark/eval framing
* high transparency

Tradeoff:

* less control over the core
* weaker direct leverage later

#### Option B — Hybrid open/private

Best when the goal is:

* acquisition optionality
* tighter IP control
* stronger negotiating position
* clean separation between public credibility and protected implementation

Typical posture:

* public moonshot, schemas, benchmark philosophy, artifact specs
* protected core implementation
* deliberate public/private boundaries
* standard licensing on the public side
* internal control over crown-jewel surfaces

Tradeoff:

* slower community traction
* more work to maintain boundary discipline

### Recommended principle

Do not choose a license because it feels idealistic or fashionable.
Choose a license posture that fits the desired outcome and does not create avoidable diligence friction.

---

## Public surface vs protected IP surface

This distinction should be explicit from the beginning.

### Public surface

The project can expose these without giving away the whole strategic asset:

* vision / moonshot
* governance posture
* benchmark philosophy
* artifact schemas
* replay or evaluation formats
* public interface documentation
* selected demos
* selected evidence reports
* non-core utilities
* standards that help ecosystem alignment

### Protected IP surface

This is where the differentiated value often lives:

* core runtime implementation
* environment stabilization internals
* proprietary orchestration logic
* internal adapter machinery
* private training/evaluation pipelines
* internal labeling/curriculum systems
* private heuristics
* crown-jewel workflow logic

### Why this matters

If everything is public by default, you may gain signal but lose leverage.
If everything is private by default, you may preserve leverage but lose credibility and momentum.

The correct move is not “open” or “closed.”
It is:

> Make the public surface useful and credible, while keeping the true core intentionally controlled if acquisition optionality is a priority.

---

## Documentation posture

Documentation should not just explain the project. It should make the project **diligence-friendly** and **maintainable by others**.

A buyer should be able to read the documentation and conclude:

> We understand what this is, what it does, what it depends on, what is original here, what is risky, and what we would actually be buying.

### Documentation should answer

* What is the project’s purpose?
* What is in scope and out of scope?
* What are the major surfaces and boundaries?
* What is public vs internal?
* What evidence exists that the system works?
* What rights govern the code and assets?
* What dependencies and restrictions exist?
* What are the major risks and deferrals?
* What would a new maintainer need to know first?

### Documentation should include

* moonshot / vision document
* project record / living ledger
* non-goals
* known risks
* licensing and provenance posture
* public/private boundary definitions
* dependency inventory
* artifact and schema definitions
* benchmark/evaluation philosophy
* contributor policy
* naming and branding rules
* maintenance posture

### Good test for documentation

A technically capable team that has never met you should be able to understand:

* what the project is
* how the pieces relate
* what is stable
* what is not yet stable
* what claims are proved
* what claims are explicitly not proved

If the answer is no, the documentation is not yet acquisition-ready.

---

## Provenance and IP hygiene

This is one of the highest-risk areas and one of the biggest silent deal-killers.

### Principle

Every meaningful asset should have a clear origin story.

That includes:

* source code
* docs
* datasets
* replays
* benchmark assets
* generated labels
* model weights
* screenshots/media
* imported parsers/utilities
* third-party templates or snippets

### You want clear answers to:

* Was this written in-house?
* Was it derived from a third party?
* Under what license?
* Is redistribution allowed?
* Is commercial use allowed?
* Is attribution required?
* Is sublicensing restricted?
* Is there any copyleft risk?
* Was anything copied from unclear sources?

### Red-flag sources

Avoid ambiguity from:

* forum snippets
* Stack Overflow code without clear license handling
* copied repository fragments
* unclear Kaggle/community assets
* random public datasets with vague rights
* “temporary” borrowed parsers
* untracked AI-generated content mixed into core assets without review

### Project rule

If provenance is unclear, it should not be part of the core asset.

---

## Rights register

The project should maintain a simple, living rights register.

This can start as part of the project record and later become its own file.

### It should track

* first-party assets
* third-party dependencies
* license of each dependency
* redistribution rules
* attribution obligations
* patent or copyleft concerns
* dataset/replay rights
* public/private status of major components
* anything that cannot be sublicensed cleanly

### Why this matters

This prevents late-stage confusion when someone asks:

* what exactly do we own?
* what exactly are we allowed to transfer?
* what are the downstream obligations?

A rights register turns guesswork into inventory.

---

## Data, replay, and model asset separation

Do not treat all assets as one undifferentiated mass.

Code, data, replays, derived labels, and weights may have very different rights and risk profiles.

### Keep separate governance for:

* source code
* replay assets
* datasets
* benchmark materials
* generated labels
* trained weights
* evaluation outputs
* third-party tools

### Why separation matters

A buyer may be comfortable with the code but uncomfortable with the data rights.
Or the reverse.

Keeping those surfaces separate preserves optionality and makes diligence easier.

---

## Contributor policy

Contributor ambiguity is a real acquisition risk.

### Ideal posture early on

* single primary contributor, or
* every contributor works under explicit terms

### Core rules

* authorship must be traceable
* contributions must be assignable
* no anonymous or vague-origin core contributions
* commit history should be attributable
* external help should not enter core IP surfaces casually

### Good policy shape

* contributions require explicit terms
* ownership status must be clear
* unclear-origin contributions are not accepted into the core
* material contributions should be documented

This is not about being closed for its own sake.
It is about avoiding ambiguous IP later.

---

## Dependency hygiene and SBOM mindset

Modern diligence increasingly expects dependency clarity.

### The project should know:

* what dependencies exist
* why each exists
* what license each carries
* whether each is optional or core
* which are high risk
* which are replaceable
* which are pinned and why

### Helpful posture

Maintain:

* dependency inventory
* license inventory
* secret hygiene
* pinned versions where appropriate
* environment capture for important artifacts
* reproducibility notes
* SBOM-friendly discipline

This is not only good engineering. It increases buyer trust.

---

## Branding and naming

Branding is not cosmetic if acquisition is a target outcome.

A buyer wants a project identity that is:

* distinct
* ownable
* memorable
* not obviously infringing
* extensible

### Good naming posture

* choose names early and consistently
* check for obvious trademark conflicts
* keep naming clean across repo, docs, and public materials
* avoid placeholder brand drift

A strong project name helps a buyer imagine the asset as something real and transferable.

---

## Evidence posture

A buyer will trust a system more if claims are bounded and evidence-backed.

### The project should prefer:

* tests
* artifact outputs
* milestone summaries
* recorded proof
* explicit non-proofs
* environment capture
* evaluation ledgers

### The project should avoid:

* inflated capability claims
* hand-wavy assertions
* undocumented leaps
* “works in practice” without proof surfaces
* unclear benchmark reporting

An evidence-first project is easier to trust and easier to buy.

---

## What should not change

Adopting this posture does **not** mean:

* burying the project in process
* pretending to be a big company
* over-lawyering everything immediately
* optimizing for monetization too early
* hiding all useful work behind secrecy
* slowing the project down with bureaucracy

The correct principle is:

> Build it so it could survive diligence later, without making today’s work miserable.

That is the balance.

---

## Operating summary

If acquisition is the best-case outcome, the project should aim to be:

### Legible

A new owner can understand it.

### Ownable

The rights situation is clear.

### Defensible

Licensing and provenance are clean.

### Separable

Core IP, public surfaces, and downstream assets are distinct.

### Maintainable

A new team could take it over.

### Trustworthy

Claims are evidence-backed and bounded.

### Optionality-preserving

The project can support public signal, strategic attention, partnership, or acquisition without needing to be rebuilt.

---

## Recommended project rules

These are good anchor rules to carry into the project:

1. **Do not ship ambiguity into the core.**
2. **Treat ownership, licensing, and provenance as first-class engineering concerns.**
3. **Define public surfaces and protected IP surfaces intentionally.**
4. **Document the project so a capable outsider can maintain it.**
5. **Keep code, data, replays, labels, and weights separately governable.**
6. **Use standard, low-friction licensing where public release exists.**
7. **Reject unnecessary copyleft or unclear license contamination in crown-jewel surfaces.**
8. **Make evidence and non-proofs explicit.**
9. **Favor clean boundaries over premature openness or premature secrecy.**
10. **Build the project so a buyer could say yes without having to forgive preventable mess.**

---

## One-sentence anchor

> The project should be built not merely to impress, but to be cleanly ownable, low-friction to diligence, and credible enough that a serious acquirer could understand exactly what it is, what it proves, what it depends on, and what they would be buying.
