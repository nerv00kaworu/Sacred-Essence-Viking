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

Think of Sacred Essence as five layers:

1. **Memory artifact layer**  
   Markdown files that hold the actual memory.

2. **Projection layer**  
   L0 / L1 / L2 summaries for staged recall.

3. **Retrieval layer**  
   Search, constrained recall, optional local index support.

4. **Lifecycle layer**  
   Downgrade, decay, garbage collection, SOIL distillation.

5. **Governance layer**  
   The rules for what should stay, what should cool, and what should be reduced to residue.

That is why Sacred Essence is better described as a **memory system** than as a search feature.

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
