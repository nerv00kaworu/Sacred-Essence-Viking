# Changelog — v5.0

## Sacred Essence (Public Edition)

Version 5.0 is a public-facing cleanup and architecture clarification release.

It does not try to present Sacred Essence as a generic “vector memory product”.
Instead, it clarifies the system as a **markdown-first memory architecture with lifecycle, distillation, and local-first retrieval design**.

---

## Highlights

### 1. README rewritten for the real architecture
- rewrote the README as a public-safe v5.0 overview
- removed machine-specific and private deployment framing
- emphasized memory lifecycle, layered projection, and governance
- clarified that retrieval is replaceable while memory artifacts remain canonical

### 2. De-sensitive path cleanup
- removed hard-coded local machine paths where touched
- replaced path assumptions with environment-variable-based overrides
- improved repo portability for other users and environments

### 3. Public-safe repository hygiene
- expanded `.gitignore` for caches, local indexes, db files, logs, and env files
- converted `SOIL.md` into a public template-style file
- added `PUBLIC_NOTES.md` as a pre-publish checklist

### 4. Test portability improvements
- removed hard-coded repository path assumptions in test files
- switched to repo-relative path handling where touched

---

## Positioning change in v5.0

The main conceptual clarification in v5.0 is this:

> Sacred Essence is a **memory governance system with a local retrieval spine**.

That means the project is now documented in terms of:

- durable memory artifacts
- layered recall
- decay and distillation
- local-first retrieval
- public-safe portability

rather than as a narrow search utility.

---

## Notes

This release focuses on **public representation and repository hygiene**, not on introducing a brand-new runtime engine.

If future versions evolve the runtime further, this v5.0 release should still serve as the baseline public description of what Sacred Essence fundamentally is.
