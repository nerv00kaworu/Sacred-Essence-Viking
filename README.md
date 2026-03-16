# 🌌 Sacred Essence (神髓) v5.0

**A markdown-first, local-first memory architecture for AI agents.**

Sacred Essence is not just a storage layer, and not just a vector search wrapper.
It is a **memory system with structure, decay, distillation, and human readability built in**.

> Keep memories readable.
> Keep retrieval local when possible.
> Let forgetting become refinement instead of silent loss.

This repository is the **public / de-sensitive edition** of Sacred Essence.
It reflects the current architectural direction without exposing private deployment details, personal runtime data, or machine-specific paths.

---

## Why Sacred Essence exists

Most agent memory systems optimize for one thing:

- store more
- retrieve faster
- auto-capture harder

Sacred Essence was built around a different question:

> **How should an agent remember if memory is meant to stay useful, inspectable, and evolvable over time?**

That leads to a different design:

- **Markdown-first** instead of database-only
- **Layered projection** instead of full-context dumping
- **Lifecycle management** instead of infinite hoarding
- **Local-first retrieval** instead of API dependency by default
- **Distillation** instead of blunt deletion

---

## What Sacred Essence is

Sacred Essence is a memory architecture for agents that need:

- long-running continuity
- project memory
- stable lessons over time
- human-readable memory artifacts
- local retrieval with portable data ownership

It is especially useful when you want memory to be:

- **editable by humans**
- **searchable by machines**
- **resilient across sessions**
- **portable across environments**
- **capable of forgetting without losing all value**

---

## Core ideas

## 1. Markdown is the source of truth

Memories are stored as files, not hidden behind a black-box service.

That means:

- you can read them directly
- you can diff them
- you can back them up with normal tools
- you can rebuild indexes without losing the memory itself

This is a deliberate choice.

Sacred Essence assumes that long-term memory should remain inspectable.

---

## 2. Memory has layers

Not every recall needs the full document.

Sacred Essence uses a three-layer projection model:

- **L0 / Abstract** — the semantic core
- **L1 / Overview** — a structured summary
- **L2 / Content** — the full narrative or raw memory

This allows an agent to:

- keep only small memory anchors near the surface
- load broader context when needed
- fetch full detail only when necessary

In practice:

- **L0** is what helps orientation
- **L1** is what helps decision framing
- **L2** is what helps deep reconstruction

---

## 3. Memory has a lifecycle

Sacred Essence treats memory as something alive.

A memory should not stay equally important forever.
Some memories should remain core. Some should cool. Some should fade. Some should leave behind only their residue.

The canonical lifecycle is:

```text
GOLDEN  -> manually protected core memory
SILVER  -> active / recently useful memory
BRONZE  -> background / cooling memory
DUST    -> near-forgetting memory
SOIL    -> distilled residue before permanent loss
```

This model allows the system to do something most memory systems do badly:

> **forget with dignity**

---

## 4. Forgetting is refinement, not failure

When a memory falls toward irrelevance, Sacred Essence does not treat that as pure deletion.

Instead, it can distill the durable lesson into **SOIL**:

- the full detail can disappear
- the useful residue remains
- the system becomes lighter without becoming emptier

This is one of the philosophical cores of the project.

The point is not to preserve every sentence forever.
The point is to preserve what still matters.

---

## 5. Retrieval should be local-first and swappable

Sacred Essence is designed so the memory artifacts remain stable even if the retrieval layer changes.

That means:

- markdown stays the canonical record
- local indexing can be rebuilt
- retrieval backends can evolve over time
- the system is not locked to one SaaS provider

This repo includes an optional local bridge for index-assisted search workflows.

The larger principle is:

> **retrieval engines are replaceable; memory artifacts are not**

---

## 6. Memory is not only retrieval — it is governance

A lot of memory tools answer only one question:

- “How do I retrieve the most relevant chunk?”

Sacred Essence also cares about:

- what deserves to be remembered
- how memory should cool down over time
- how stable lessons differ from raw notes
- how to preserve continuity without preserving noise forever

So this project should be read as:

- a memory substrate
- a memory lifecycle model
- a memory governance pattern

—not merely a search utility.

---

## Feature overview

### Memory representation
- markdown-first storage
- L0 / L1 / L2 layered projection
- human-readable memory artifacts

### Lifecycle management
- decay-aware state transitions
- GOLDEN / SILVER / BRONZE / DUST / SOIL model
- garbage collection with dry-run support
- residue-preserving archival pattern

### Retrieval model
- local-first search workflow
- optional index bridge
- constrained search with fallback patterns
- duplicate detection / merge heuristics

### Operational philosophy
- portable memory ownership
- inspectable artifacts
- low dependency on remote APIs by default
- retrieval layer can evolve without rewriting memory itself

---

## Quick start

### Install

```bash
git clone https://github.com/nerv00kaworu/Sacred-Essence-Viking.git
cd Sacred-Essence-Viking
pip install -r requirements.txt
```

### Basic usage

```bash
# Encode a memory
python main.py encode \
  --topic "project" \
  --title "Retry architecture" \
  --content "We chose queue-first retries to reduce partial failure risk."

# List all memories
python main.py list

# Search
python main.py search "retry queue" -n 5

# Preview garbage collection
python main.py gc

# Execute garbage collection
python main.py gc --execute
```

---

## CLI

## Encode

```bash
python main.py encode \
  --topic "architecture" \
  --title "Schema decision" \
  --content "..."
```

## List

```bash
python main.py list
python main.py list --topic architecture
```

## Project / reconstruct context

```bash
python main.py project --topic architecture --id abc12345
```

## Search

```bash
python main.py search "migration strategy" -n 5
```

## Garbage collection

```bash
python main.py gc
python main.py gc --execute
```

## Optional local index integration

```bash
python main.py qmd sync
python main.py qmd audit
python main.py qmd query "memory decay"
python main.py qmd constrained-search "retry" --nodes id1 id2 id3
```

---

## Configuration

The public version removes machine-specific hard-coded paths.

Use environment variables when needed:

- `SACRED_ESSENCE_MEMORY_DIR` — base memory directory override
- `SACRED_ESSENCE_TOPICS_DIR` — topics directory override for the search bridge
- `QMD_BIN` — local QMD executable path override

If unset, the project falls back to local defaults where possible.

---

## Recommended mental model

Think of Sacred Essence as five layers working together:

1. **Memory artifact layer** — markdown files as the durable substrate
2. **Projection layer** — L0 / L1 / L2 for token-efficient recall
3. **Lifecycle layer** — decay, downgrade, distillation, cleanup
4. **Retrieval layer** — local search, constrained recall, optional indexing
5. **Governance layer** — deciding what should remain core versus what should cool and disappear

This is why Sacred Essence is stronger than a plain vector-memory demo.
It is designed for continuity, not just retrieval benchmarks.

---

## What this public repo intentionally excludes

This repository does **not** include private operational state such as:

- personal runtime memory contents
- deployment-specific automation
- private production paths
- secrets or credentials
- machine-specific scheduler setup
- internal team context unrelated to the public architecture

If you adapt Sacred Essence for your own environment, you should provide your own:

- memory directory layout
- scheduler / automation integration
- backup strategy
- retrieval backend runtime
- deployment safety policy

---

## Suggested usage pattern

A practical pattern is:

- use Sacred Essence to store durable memory artifacts
- use summaries / projections for lightweight recall
- use local indexing only as an accelerator
- let garbage collection reduce dead weight over time
- treat SOIL as distilled residue, not as clutter

This keeps the system readable and sustainable as it grows.

---

## What v5.0 means

Version 5.0 is less about adding one flashy mechanism and more about clarifying the project’s real identity:

> **Sacred Essence is a memory governance system with a local retrieval spine.**

That means the project is now described publicly in terms of:

- durable architecture
- inspectable memory artifacts
- lifecycle design
- de-sensitive portability
- separation between memory truth and retrieval machinery

In short:

- memory remains readable
- retrieval remains flexible
- forgetting becomes part of design
- the system stays portable and sane

---

## Repository hygiene

Before publishing or extending this project, keep these outside version control unless intentionally public:

- generated memory files
- local indexes / vector caches
- logs
- env files
- private notes
- runtime-produced SOIL contents

The included `.gitignore` assumes this workflow.

---

## Roadmap directions

Natural next steps for the public version could include:

- clearer schema docs for memory nodes
- pluggable retrieval backends
- promotion pipeline docs (raw → candidate → verified → core)
- better examples for multi-agent usage
- packaging improvements
- public test fixtures separated from runtime assumptions

---

## Final note

If you only want a fast auto-recall plug-in, Sacred Essence may feel unusually opinionated.
That is intentional.

Sacred Essence is for people who believe agent memory should be:

- durable
- inspectable
- local-first
- layered
- capable of graceful forgetting

If that tradeoff matches your values, this architecture will make sense.
