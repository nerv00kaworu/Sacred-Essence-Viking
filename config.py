# Sacred Essence v3.1 Configuration

import os
from pathlib import Path

# Base Directories
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
# 正確的記憶目錄在 workspace/memory/octagram/engine/
MEMORY_DIR = "/home/nerv0/.openclaw/workspace/memory/octagram/engine/memory"
TRASH_DIR = os.path.join(BASE_DIR, ".trash")

# Ensure directories exist (Implementation detail, but config is good place for definitions)
# Structure:
# memory/
#   topics/ (L0/L1)
#   storage/ (L2 raw files)
#   embeddings/ (.npy)

# Thresholds
SOFT_CAP_GOLDEN = 50
THRESHOLD_SILVER = 5.0   # Score < 5.0 -> Prune to Bronze (if not Golden)
THRESHOLD_DUST = 1.0     # Score < 1.0 -> Mark as Dust (or Soil extraction)
RETENTION_DAYS = 30      # Days to keep in Trash
MIN_KEEP_NODES = 20      # Safety Net: Minimum active nodes to preserve
GRACE_PERIOD_DAYS = 3    # Days before decay starts for new nodes

# Formula Constants
INITIAL_IMPORTANCE = 10.0

# Stability Factors (S)
STABILITY_USER = 1.0
STABILITY_ROLE = 0.995
STABILITY_WORLD = 0.95

# Density Weights (D)
# D = base + (access * 0.2) + (retrieval * 0.1)
DENSITY_BASE = 0.0
WEIGHT_ACCESS = 0.2      # Writing/Editing
WEIGHT_RETRIEVAL = 0.1   # Reading/Projecting

# Similarity Constants
SIMILARITY_THRESHOLD = 0.75  # > 0.75 -> Potential duplicate
MERGE_THRESHOLD = 0.85       # > 0.85 -> Auto-merge (increment access_count only)
EMBEDDING_MODEL = 'google/embeddinggemma-300m'
