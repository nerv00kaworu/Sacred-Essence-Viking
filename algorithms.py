# Sacred Essence v3.1 Core Algorithms

import math
from datetime import datetime
import numpy as np
from typing import List, Union

# Import config
try:
    from config import (
        INITIAL_IMPORTANCE, 
        GRACE_PERIOD_DAYS, 
        DENSITY_BASE, 
        WEIGHT_ACCESS, 
        WEIGHT_RETRIEVAL
    )
    from models import MemoryNode
except ImportError:
    # Fallback or local dev
    pass

def calculate_density(node: 'MemoryNode') -> float:
    """
    Calculate Density (D) based on interaction frequency.
    D = base + (access * 0.2) + (retrieval * 0.1)
    """
    d = DENSITY_BASE + (node.access_count * WEIGHT_ACCESS) + (node.retrieval_count * WEIGHT_RETRIEVAL)
    return d

def calculate_importance(node: 'MemoryNode', current_date: datetime = None) -> float:
    """
    Calculate Current Importance Score.
    Current = Initial * S^days + ln(1 + D)
    """
    if current_date is None:
        current_date = datetime.now()
        
    # 1. Check Grace Period
    age_days = (current_date - node.creation_date).days
    if age_days <= GRACE_PERIOD_DAYS:
        # In grace period, return high score (Initial + Density bonus)
        # to ensure it's not GC'd immediately.
        # Returning just INITIAL_IMPORTANCE might be enough, 
        # but adding density allows it to grow even in grace period.
        d = calculate_density(node)
        return INITIAL_IMPORTANCE + math.log(1 + d)

    # 2. Calculate Decay Days (Distance from LAST INTERACTION)
    # The formula says `S^days`. If we use age, it decays too fast.
    # If we use `days since last access`, it resets on access.
    # Strategy: "days: 距離上次有效互動的天數"
    days_unused = (current_date - node.last_access_date).days
    if days_unused < 0: days_unused = 0
    
    # 3. Calculate Components
    s_factor = node.stability_factor
    density = calculate_density(node)
    
    # 4. Formula
    # Current = Initial * (S ^ days_unused) + min(MAX_DENSITY_BONUS, ln(1 + D))
    MAX_DENSITY_BONUS = 5.0 # Prevent infinite score growth
    decay_term = INITIAL_IMPORTANCE * (math.pow(s_factor, days_unused))
    growth_term = min(MAX_DENSITY_BONUS, math.log(1 + density))
    
    current_score = decay_term + growth_term
    return current_score

def cosine_similarity(vec1: List[float], vec2: List[float]) -> float:
    """
    Calculate Cosine Similarity between two vectors.
    """
    if not vec1 or not vec2:
        return 0.0
    
    v1 = np.array(vec1)
    v2 = np.array(vec2)
    
    if v1.shape != v2.shape:
        print(f"Warning: Vector dimension mismatch ({v1.shape} vs {v2.shape}).")
        return 0.0
    
    dot_product = np.dot(v1, v2)
    norm_v1 = np.linalg.norm(v1)
    norm_v2 = np.linalg.norm(v2)
    
    if norm_v1 == 0 or norm_v2 == 0:
        return 0.0
        
    return float(dot_product / (norm_v1 * norm_v2))

# Initializing embedding model is expensive, so we might do it in a class or lazy load
_model_cache = None

def get_embedding(text: str) -> List[float]:
    """
    Generate embedding for text using sentence-transformers.
    Lazy loads the model.
    """
    global _model_cache
    if _model_cache is None:
        try:
            from sentence_transformers import SentenceTransformer
            # Using the model specified in config or default
            _model_cache = SentenceTransformer('google/embeddinggemma-300m')
        except ImportError:
            print("Warning: sentence-transformers not installed. Returning dummy vector.")
            return [0.0] * 384 # Dummy 384-dim vector for testing without deps
            
    if not text or not text.strip():
        return [0.0] * 384
        
    embedding = _model_cache.encode(text)
    return embedding.tolist()
