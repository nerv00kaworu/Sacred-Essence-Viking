# Sacred Essence Architecture (v5.0)

## Overview

Sacred Essence is a markdown-first memory architecture for AI agents.

Its design centers on a simple separation:

- **memory artifacts** should remain durable and human-readable
- **retrieval infrastructure** should remain replaceable

This prevents the system from becoming trapped inside a single indexing backend or opaque memory service.

---

## Architectural layers

## 1. Artifact layer

This is the canonical memory substrate.

Contents:
- markdown memory files
- L0 / L1 / L2 representations
- topic-oriented organization
- distilled SOIL residue

Principle:
- if the index disappears, the memory still exists

---

## 2. Projection layer

Sacred Essence uses layered projection to avoid loading full memory content all the time.

### L0 / Abstract
- semantic anchor
- smallest useful summary
- suitable for lightweight orientation

### L1 / Overview
- structured summary
- helps frame context before deeper loading

### L2 / Content
- full narrative / detailed memory body
- loaded only when real detail is required

This supports token-efficient recall and targeted reconstruction.

---

## 3. Lifecycle layer

Memories transition through a decay-aware lifecycle.

```text
GOLDEN -> protected core memory
SILVER -> active memory
BRONZE -> cooling memory
DUST   -> near-forgetting memory
SOIL   -> distilled residue
```

Purpose:
- avoid infinite clutter
- preserve useful lessons even when detail decays
- keep the memory space sustainable over time

---

## 4. Retrieval layer

Sacred Essence supports local-first retrieval patterns.

This may include:
- semantic search
- constrained search within whitelisted nodes
- fallback retrieval when confidence drops
- optional index synchronization

Principle:
- retrieval is an accelerator, not the source of truth

---

## 5. Governance layer

The most important layer is often invisible in simpler memory systems.

Sacred Essence assumes that memory quality depends on:
- what gets encoded
- how duplication is handled
- when memories should cool down
- how forgetting preserves residue
- how stable lessons differ from raw details

This is why Sacred Essence should be understood as a governance pattern, not only a search tool.

---

## Design principles

### Human-readable by default
Memory should remain inspectable.

### Local-first where practical
Do not assume a cloud provider is required for basic continuity.

### Retrieval backends are replaceable
Indexes can evolve without rewriting memory artifacts.

### Forgetting is part of the system
Decay is not a bug; it is part of memory hygiene.

### Distillation matters
Deleting detail is acceptable if durable insight is preserved.

---

## Suggested deployment model

A practical deployment can look like this:

1. store durable memory as markdown
2. generate lightweight projections
3. sync to a local retrieval/index layer if needed
4. use constrained recall first
5. allow fallback retrieval when confidence is low
6. run garbage collection periodically
7. preserve distilled residue in SOIL-like archives

---

## Public repository scope

This public repository documents the architecture and portable code shape.

It intentionally does not include:
- personal runtime memory contents
- machine-specific paths
- private automation policies
- production secrets
- environment-specific scheduling details

Those belong to downstream deployments, not to the public core.
