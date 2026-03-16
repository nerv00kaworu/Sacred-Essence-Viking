# 🌌 Sacred Essence (神髓) v5.0

**Sacred Essence is a long-term memory system for AI agents.**

It stores memories as Markdown, summarizes them into layered representations, lets you search and reconstruct context later, and gradually decays low-value memories into distilled residue instead of keeping everything forever.

In one sentence:

> **Sacred Essence helps an AI agent turn raw events into searchable, human-readable, long-term memory.**

---

## What problem does this system solve?

Most agents only have one of these:

- short chat history
- a vector database full of opaque chunks
- a notes folder that keeps growing forever

That creates four problems:

1. **No real long-term memory**  
   Important things get buried in old conversations.

2. **No human-readable memory source**  
   If memory only lives inside embeddings or a database, it becomes hard to inspect, edit, or trust.

3. **No memory lifecycle**  
   Everything is stored forever, so retrieval quality gets worse over time.

4. **No distillation**  
   Old memories are either kept forever or deleted entirely. There is no middle ground.

Sacred Essence is built to solve exactly that.

---

## What does Sacred Essence actually do?

Sacred Essence does five main things:

### 1. Store memories as Markdown
Every memory is kept as a readable file instead of disappearing into a black box.

### 2. Project memories into layers
Each memory can be represented as:

- **L0** — tiny semantic abstract
- **L1** — structured overview
- **L2** — full content

This lets an agent recall cheaply first, then load more detail only when needed.

### 3. Search and reconstruct context
You can search by meaning, keyword, or constrained scope, then project the relevant memory back into usable context.

### 4. Decay stale memories over time
Not every memory should remain equally important forever.
Sacred Essence gradually downgrades less useful memories.

### 5. Distill dying memories into SOIL
Before a weak memory disappears, the system can keep its final lesson as a distilled residue.

So instead of this:

- keep everything forever
- or delete everything brutally

it does this:

- keep what matters
- cool what fades
- distill what is still worth preserving

---

## How the system works

At a high level, Sacred Essence works like this:

```text
Raw event / note
   ↓
Encode into memory node
   ↓
Store as Markdown (human-readable source)
   ↓
Generate L0 / L1 / L2 projections
   ↓
Retrieve later by search / projection
   ↓
Decay over time if no longer useful
   ↓
Distill to SOIL before final removal
```

This gives you a memory system that is:

- readable
- searchable
- compactable
- decay-aware
- rebuildable if the retrieval layer changes

---

## Memory lifecycle

Sacred Essence uses a lifecycle model instead of infinite storage.

```text
GOLDEN  -> protected core memory
SILVER  -> active memory
BRONZE  -> cooling memory
DUST    -> near-forgetting memory
SOIL    -> distilled residue
```

### What these states mean

- **GOLDEN**  
  Core memories you want to preserve deliberately.

- **SILVER**  
  Active memories that are still useful in current work.

- **BRONZE**  
  Older memories that still exist but matter less.

- **DUST**  
  Memories close to being forgotten.

- **SOIL**  
  The final residue: not full detail, but the durable lesson.

This is one of the main differences between Sacred Essence and ordinary note storage.

---

## Why Markdown?

Sacred Essence chooses Markdown on purpose.

Because long-term memory should be:

- human-readable
- diffable
- easy to back up
- portable across tools
- not locked into one vendor or one index format

The Markdown files are the **source of truth**.

Any retrieval/index layer is secondary and can be rebuilt.

---

## Why layered memory?

If every recall always loads the full memory, token cost and noise go up quickly.

Layered memory fixes that.

### L0 — Abstract
A very small semantic anchor.
Good for orientation.

### L1 — Overview
A structured summary.
Good for deciding whether this memory matters.

### L2 — Content
The full original memory.
Good for deep reconstruction.

This lets an agent do staged recall instead of blindly dumping everything into context.

---

## How Sacred Essence fits into a larger memory stack

In practice, Sacred Essence works best as part of a broader agent memory workflow.

A common split looks like this:

- **Daily logs / raw notes**  
  Short-term event capture, rough notes, and session residue.

- **Handoff / operational memory**  
  The active workbench: what is in progress, what is blocked, what must be resumed next.

- **Sacred Essence**  
  Durable structured memory: distilled events, layered recall, long-term lessons, and decay-aware storage.

- **QMD or other local index layer**  
  Retrieval acceleration: semantic search, constrained search, and fallback lookup across the memory space.

That means Sacred Essence is not trying to replace every file in a workflow.
It plays the role of the **durable memory core**, while `handoff` handles active continuity and QMD handles faster retrieval.

---

## Where handoff fits

`handoff` is the operational layer.

It answers questions like:

- what is currently being worked on?
- what is blocked?
- what should the next agent/session resume first?
- what still needs validation?

This is different from Sacred Essence.

Sacred Essence stores the longer-lived memory artifact.
`handoff` stores the **active continuity state**.

A useful rule of thumb is:

- use **handoff** for immediate coordination
- use **Sacred Essence** for durable memory

---

## Where QMD fits

QMD is not the memory itself.
It is the **retrieval spine / index layer** that helps surface memory efficiently.

In a typical setup:

- Sacred Essence keeps the canonical memory artifacts in Markdown
- QMD syncs or indexes those artifacts for faster retrieval
- search can use QMD as an accelerator without changing the source of truth

This separation matters.

If the index changes, the memory still survives.
If the memory evolves, the index can be rebuilt.

That is why Sacred Essence and QMD work well together:

- **Sacred Essence** = memory truth
- **QMD** = retrieval acceleration

---

## Example use cases

Sacred Essence is useful when an agent needs to remember things like:

- project decisions
- technical lessons
- user preferences
- repeated mistakes
- distilled insights from long work sessions
- stable facts that should survive across sessions

Examples:

- “Why did we choose queue-first retries?”
- “What was the final lesson from that failed deployment?”
- “What matters from a month of research, without loading all raw logs?”
- “What should still remain after the detailed context has faded?”

---

## CLI usage

### Install

```bash
git clone https://github.com/nerv00kaworu/Sacred-Essence-Viking.git
cd Sacred-Essence-Viking
pip install -r requirements.txt
```

### Encode a memory

```bash
python main.py encode \
  --topic "project" \
  --title "Retry architecture" \
  --content "We chose queue-first retries to reduce partial failure risk."
```

### List memories

```bash
python main.py list
python main.py list --topic project
```

### Search memories

```bash
python main.py search "retry queue" -n 5
```

### Reconstruct a memory

```bash
python main.py project --topic project --id abc12345
```

### Preview garbage collection

```bash
python main.py gc
```

### Execute garbage collection

```bash
python main.py gc --execute
```

### Optional local index integration

```bash
python main.py qmd sync
python main.py qmd audit
python main.py qmd query "memory decay"
python main.py qmd constrained-search "retry" --nodes id1 id2 id3
```

---

## What makes Sacred Essence different?

### It is not just a notes folder
Because it has:

- memory states
- decay
- projection
- retrieval workflow
- distillation before deletion

### It is not just a vector DB wrapper
Because the memory itself remains:

- readable
- structured
- portable
- inspectable by humans

### It is not just RAG
Because it does more than retrieve chunks.
It manages **memory quality over time**.

That is the real point of the system.

---

## Architecture in plain English

Think of the full memory stack like this:

1. **Raw notes / daily logs**  
   Capture events, fragments, and rough session residue.

2. **Handoff layer**  
   Track active tasks, blocked work, and what must resume next.

3. **Sacred Essence memory layer**  
   Store durable Markdown memory with L0 / L1 / L2 structure.

4. **QMD / local retrieval layer**  
   Provide indexing, semantic retrieval, constrained search, and fallback lookup.

5. **Lifecycle and governance layer**  
   Decide what remains active, what decays, and what gets distilled into SOIL.

Within that stack, Sacred Essence is the durable memory core.
It is stronger than a simple notes folder, and broader than a pure search feature.

---

## Configuration

The public version avoids machine-specific hard-coded paths.

You can override paths with environment variables:

- `SACRED_ESSENCE_MEMORY_DIR`
- `SACRED_ESSENCE_TOPICS_DIR`
- `QMD_BIN`

If unset, the project falls back to local defaults where possible.

---

## Public repo scope

This public repository includes the portable architecture and public-safe code shape.

It intentionally excludes things like:

- private runtime memory contents
- machine-specific deployment details
- secrets and credentials
- private scheduler / automation state
- internal team-specific operational context

---

## In short

Sacred Essence is for people who want agent memory to be:

- long-term
- human-readable
- searchable
- layered
- decay-aware
- capable of graceful forgetting

If you want a system that turns raw events into durable memory instead of just piling up more text, that is what Sacred Essence is for.
