# Sacred Essence v3.1 Data Models

from enum import Enum
from dataclasses import dataclass, field, asdict
from datetime import datetime
from typing import Optional, List, Dict, Any
import json

class NodeState(str, Enum):
    GOLDEN = "GOLDEN"
    SILVER = "SILVER"
    BRONZE = "BRONZE"
    DUST = "DUST"
    
    # Helper for serialization
    def __str__(self):
        return self.value

@dataclass
class MemoryNode:
    id: str  # Unique ID (e.g. UUID or Sanitized Title)
    topic: str
    title: str
    content_path: str # Path to L2 raw content file
    
    # Metadata
    creation_date: datetime
    last_access_date: datetime
    
    # Logic Stats
    access_count: int = 0
    retrieval_count: int = 0
    stability_factor: float = 0.95
    state: NodeState = NodeState.SILVER
    
    # Content Cache (L0/L1 are stored in JSON metadata usually, or small files)
    L0_abstract: str = ""
    L1_overview: str = ""
    
    # Internal Tracking (GC Performance)
    is_dirty: bool = False
    
    # Embedding (Cached in object or loaded on demand)
    # Stored as None to avoid memory bloat, loaded when needed
    embedding: Optional[List[float]] = field(default=None, repr=False)

    def update_access(self):
        """Update access stats."""
        self.access_count += 1
        self.last_access_date = datetime.now()
        self.is_dirty = True

    def update_retrieval(self):
        """Update retrieval stats."""
        self.retrieval_count += 1
        # Retrieval doesn't necessarily reset decay date, but usually "interaction" does.
        # Strategy says "Effective interaction" updates days. 
        # Usually retrieval implies we saw it, so it refreshes the memory.
        self.last_access_date = datetime.now()
        self.is_dirty = True

    def to_dict(self) -> Dict[str, Any]:
        """Serialize to dictionary."""
        data = asdict(self)
        data.pop('is_dirty', None)  # Don't serialize transient tracking flag
        data['creation_date'] = self.creation_date.isoformat()
        data['last_access_date'] = self.last_access_date.isoformat()
        data['state'] = self.state.value
        return data

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'MemoryNode':
        """Deserialize from dictionary."""
        data.pop('is_dirty', None)
        # Handle Date parsing
        data['creation_date'] = datetime.fromisoformat(data['creation_date'])
        data['last_access_date'] = datetime.fromisoformat(data['last_access_date'])
        # Handle Enum
        data['state'] = NodeState(data['state'])
        return cls(**data)
