# Sacred Essence (神髓) v5.0 — Public Edition

Sacred Essence v5.0 is the first cleaned-up **public edition** of the project.

This release is not about turning Sacred Essence into a generic vector-memory demo.
It is about presenting the project for what it actually is:

> **a markdown-first memory governance system with a local retrieval spine**

---

## Highlights

### Public-safe rewrite
- rewrote the README as a true v5.0 public overview
- removed private deployment framing and machine-specific assumptions
- clarified the project around memory lifecycle, distillation, and local-first retrieval

### De-sensitive portability cleanup
- removed hard-coded local path assumptions where touched
- switched key path handling to environment-variable-based overrides
- improved portability for other users and environments

### Better repository hygiene
- expanded `.gitignore` for caches, logs, db files, env files, and local artifacts
- converted `SOIL.md` into a public-safe template
- added `PUBLIC_NOTES.md` as a pre-publish checklist

### Project documentation upgrades
- added `docs/architecture.md`
- added `CHANGELOG-v5.0.md`
- added `LICENSE`

---

## What Sacred Essence is

Sacred Essence is designed for people who want agent memory to be:

- human-readable
- locally inspectable
- layered
- decay-aware
- capable of graceful forgetting

It combines:

- **Markdown as source of truth**
- **L0 / L1 / L2 layered projection**
- **memory lifecycle management**
- **SOIL-style distillation before deletion**
- **local-first retrieval patterns**

---

## Why v5.0 matters

This version clarifies the project’s identity.

Sacred Essence is not just a storage format and not just a retrieval plugin.
It is a broader memory architecture that separates:

- durable memory artifacts
- retrieval/index infrastructure
- lifecycle and forgetting rules
- long-term memory quality concerns

That separation is the reason the system stays portable and auditable.

---

## Suggested GitHub release title

**Sacred Essence v5.0 — Public Edition**

## Suggested short subtitle

Markdown-first, local-first memory architecture for AI agents.

---

## Notes

This release focuses on:

- public presentation
- de-sensitive cleanup
- architecture clarity
- repository hygiene

It does **not** represent a total rewrite of the runtime engine.
Instead, it establishes a cleaner and more truthful public baseline for future iterations.
