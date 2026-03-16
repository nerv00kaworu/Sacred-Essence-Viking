# PUBLIC_NOTES.md

This repository snapshot was prepared as a **public-safe / de-sensitive** edition.

## What was changed

- README rewritten to remove private paths and deployment-specific claims
- hard-coded local paths replaced with environment-variable-based defaults where touched
- `.gitignore` expanded for local indexes, logs, caches, env files, and generated artifacts

## What to review before pushing

### 1. Existing tracked files that may still be too local
Check whether these belong in the public repo:

- `SOIL.md`
- `test_soil.py`
- any tracked generated artifacts
- any historical examples containing private memory text

### 2. Source files with historical comments
Some code comments may still reference older internal versions (`v3.1`, local workflows, internal assumptions). These are not necessarily secret, but may be outdated.

### 3. Tracked runtime artifacts
Ensure the repo is not tracking:

- generated memory markdown
- local index outputs
- machine-specific logs
- caches / compiled files

### 4. Secrets / credentials
Even if not obvious in README, verify no secrets are present in:

- shell scripts
- tests
- config examples
- helper scripts

## Recommended next step

Before push:

```bash
git status
git diff --stat
git ls-files | rg '__pycache__|\.log$|\.db$|\.sqlite$|\.env'
```

If needed, remove already-tracked junk from git history or current index before publishing.
