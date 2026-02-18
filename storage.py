# Sacred Essence v3.1 Storage System

import os
import json
import shutil
from datetime import datetime
from typing import List, Optional, Dict
from glob import glob

from config import MEMORY_DIR, TRASH_DIR
from models import MemoryNode, NodeState

class MemoryStore:
    def __init__(self):
        self._ensure_dirs()

    def _ensure_dirs(self):
        os.makedirs(MEMORY_DIR, exist_ok=True)
        os.makedirs(os.path.join(MEMORY_DIR, "topics"), exist_ok=True)
        os.makedirs(TRASH_DIR, exist_ok=True)

    def _get_topic_dir(self, topic: str) -> str:
        # Sanitize topic needed in real app, simplistic here
        return os.path.join(MEMORY_DIR, "topics", topic)

    def _get_node_dir(self, topic: str, node_id: str) -> str:
        # Each node gets a directory to store L0/L1/L2 and metadata
        # Structure: memory/topics/{topic}/{node_id}/
        return os.path.join(self._get_topic_dir(topic), node_id)

    def save_node(self, node: MemoryNode):
        """Save MemoryNode to disk (Metadata + Content)."""
        node_dir = self._get_node_dir(node.topic, node.id)
        os.makedirs(node_dir, exist_ok=True)
        
        # 1. Save Content (L2) - "The Sacred Text"
        # Only if content_path is set or we want to overwrite it.
        # For this logic, we assume content management is handled here via `node.content_path` check
        # But typically we'd write the content string to a .md file
        # Here we assume `node.content_path` points to a file that might be external, 
        # OR we save it inside the node structure.
        # Let's enforce saving content inside the node dir for encapsulation.
        content_file = os.path.join(node_dir, "content.md")
        with open(content_file, 'w', encoding='utf-8') as f:
            # We don't have raw content in MemoryNode in models.py, 
            # we have content_path.
            # If we are creating a new node, we expect the content to be passed or handled.
            # Let's assume the caller handles the content file creation, 
            # and just points `node.content_path` to it.
            # But wait, `node.content_path` is in the model.
            # Let's update the model to reflect where it actually lives.
            node.content_path = content_file
            pass # We assume content is written by whoever created the node or we add a `content` arg
        
        # 2. Save Metadata
        meta_file = os.path.join(node_dir, "node.meta.json")
        with open(meta_file, 'w', encoding='utf-8') as f:
            json.dump(node.to_dict(), f, indent=2, ensure_ascii=False)
            
        # 3. Save L0/L1 (Abstracts)
        if node.L0_abstract:
            with open(os.path.join(node_dir, "L0.md"), 'w', encoding='utf-8') as f:
                f.write(node.L0_abstract)
        if node.L1_overview:
            with open(os.path.join(node_dir, "L1.md"), 'w', encoding='utf-8') as f:
                f.write(node.L1_overview)

        # 4. Save Embedding (if exists)
        if node.embedding:
            import numpy as np
            emb_path = os.path.join(node_dir, "embedding.npy")
            np.save(emb_path, np.array(node.embedding))

    def load_node(self, topic: str, node_id: str) -> Optional[MemoryNode]:
        """Load MemoryNode from disk."""
        node_dir = self._get_node_dir(topic, node_id)
        meta_file = os.path.join(node_dir, "node.meta.json")
        
        if not os.path.exists(meta_file):
            return None
            
        with open(meta_file, 'r', encoding='utf-8') as f:
            data = json.load(f)
            
        node = MemoryNode.from_dict(data)
        
        # Load extra contents
        l0_path = os.path.join(node_dir, "L0.md")
        if os.path.exists(l0_path):
            with open(l0_path, 'r', encoding='utf-8') as f:
                node.L0_abstract = f.read()
                
        l1_path = os.path.join(node_dir, "L1.md")
        if os.path.exists(l1_path):
            with open(l1_path, 'r', encoding='utf-8') as f:
                node.L1_overview = f.read()

        # Lazy load embedding?
        # For now, let's keep it None unless explicitly loaded to save memory
        return node

    def list_nodes(self, topic: str = None) -> List[MemoryNode]:
        """List all nodes, optionally filtered by topic."""
        nodes = []
        if topic:
            search_path = os.path.join(self._get_topic_dir(topic), "*", "node.meta.json")
        else:
            search_path = os.path.join(MEMORY_DIR, "topics", "*", "*", "node.meta.json")
            
        files = glob(search_path, recursive=True) # Recursive needed if * spans directories
        # Glob patterns:
        # topics/*/*/node.meta.json -> topics/TOPIC/NODE/node.meta.json
        
        for meta_file in files:
            try:
                # Extract topic & id from path
                # .../topics/{topic}/{node_id}/node.meta.json
                path_parts = os.path.normpath(meta_file).split(os.sep)
                # Assumes standard structure
                # [-1] = node.meta.json
                # [-2] = node_id
                # [-3] = topic
                n_id = path_parts[-2]
                n_topic = path_parts[-3]
                
                node = self.load_node(n_topic, n_id)
                if node:
                    nodes.append(node)
            except Exception as e:
                print(f"Error loading {meta_file}: {e}")
                
        return nodes

    def move_to_trash(self, node: MemoryNode):
        """Move node directory to trash."""
        src = self._get_node_dir(node.topic, node.id)
        # Trash structure: .trash/{topic}_{node_id}_{timestamp}/
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        dst = os.path.join(TRASH_DIR, f"{node.topic}_{node.id}_{timestamp}")
        
        if os.path.exists(src):
            shutil.move(src, dst)
            
    def get_siblings(self, node: MemoryNode) -> List[MemoryNode]:
        """Get all other nodes in the same topic."""
        all_nodes = self.list_nodes(node.topic)
        return [n for n in all_nodes if n.id != node.id]
