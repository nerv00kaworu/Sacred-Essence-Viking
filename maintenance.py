# Sacred Essence v3.1 Maintenance System

from datetime import datetime, timedelta
import os
import shutil
from typing import List, Dict

from config import (
    SOFT_CAP_GOLDEN,
    THRESHOLD_SILVER,
    THRESHOLD_DUST,
    MIN_KEEP_NODES,
    TRASH_DIR,
    RETENTION_DAYS
)
from models import MemoryNode, NodeState
from storage import MemoryStore
from algorithms import calculate_importance

class MaintenanceManager:
    def __init__(self, store: MemoryStore):
        self.store = store

    def run_garbage_collection(self, dry_run: bool = False) -> Dict[str, int]:
        """
        Execute the Garbage Collection (GC) cycle.
        1. Update Scores & States
        2. Enforce Soft Caps
        3. Identify Dust & Move to Trash
        4. Clean old Trash
        """
        report = {"scanned": 0, "downgraded_silver": 0, "marked_dust": 0, "trashed": 0, "cleaned_trash": 0}
        
        all_nodes = self.store.list_nodes()
        nodes_by_state = {s: [] for s in NodeState}
        
        # 1. Update Scores & Categorize
        current_time = datetime.now()
        updated_nodes = []
        
        for node in all_nodes:
            report["scanned"] += 1
            score = calculate_importance(node, current_time)
            
            # State Transition Logic
            # Note: Golden nodes strictly stay Golden unless manually demoted or strictly via Cap?
            # Strategy: "Golden...永不衰減" (Never decays).
            # But "Soft Cap" can demote them.
            
            if node.state == NodeState.GOLDEN:
                # Golden nodes don't decay to Dust based on score, 
                # but we track them for Soft Cap later.
                pass 
            elif node.state == NodeState.SILVER:
                if score < THRESHOLD_SILVER: # < 5.0
                    if score < THRESHOLD_DUST: # < 1.0
                        node.state = NodeState.DUST
                        report["marked_dust"] += 1
                    else:
                        node.state = NodeState.BRONZE # Or just keep as Bronze equivalent?
                        # V3.1 Doc says: "Pruning: Current < 5.0 ... delete L0/L1, return Bronze"
                        # But wait, Bronze is "L2 Only".
                        # So < 5.0 -> Bronze.
                        # < 1.0 -> Dust.
                        node.state = NodeState.BRONZE
            elif node.state == NodeState.BRONZE:
                if score < THRESHOLD_DUST:
                     node.state = NodeState.DUST
                     report["marked_dust"] += 1
                elif score > THRESHOLD_SILVER:
                    # Upgrade path? usually manual or re-abstracting.
                    pass
            
            nodes_by_state[node.state].append(node)
            updated_nodes.append(node)

        # 2. Enforce Golden Soft Cap
        golden_nodes = nodes_by_state[NodeState.GOLDEN]
        if len(golden_nodes) > SOFT_CAP_GOLDEN:
            # Sort by last_access_date (Oldest first)
            # Strategy: "最久未訪問者"
            golden_nodes.sort(key=lambda x: x.last_access_date) 
            excess = len(golden_nodes) - SOFT_CAP_GOLDEN
            
            for i in range(excess):
                node = golden_nodes[i]
                node.state = NodeState.SILVER # Downgrade
                report["downgraded_silver"] += 1
                # Move to silver list for next pass? 
                # For simplicity, we just save the state change.

        # 3. Safety Net Check
        # Count remaining active nodes (Golden + Silver + Bronze)
        # Dust nodes are candidates for trash.
        active_count = len(all_nodes) - len(nodes_by_state[NodeState.DUST])
        
        if active_count < MIN_KEEP_NODES:
            print(f"WARNING: Safety Net Triggered! Active nodes ({active_count}) < Min ({MIN_KEEP_NODES}). Aborting GC.")
            return report

        # 4. Move Dust to Trash
        if not dry_run:
            for node in nodes_by_state[NodeState.DUST]:
                self.store.move_to_trash(node)
                report["trashed"] += 1
            
            # Save updated states for non-trashed nodes
            # (Trashed nodes are moved, so saving them in place is moot, 
            # but we should update the ones that just changed state like Silver/Bronze)
            for node in updated_nodes:
                if node.state != NodeState.DUST:
                    self.store.save_node(node)

        # 5. Clean Old Trash
        if not dry_run:
            report["cleaned_trash"] = self._clean_trash()
            
        return report

    def _clean_trash(self) -> int:
        """Permanently delete old files from trash."""
        cleaned = 0
        now = datetime.now()
        if not os.path.exists(TRASH_DIR):
            return 0
            
        for item in os.listdir(TRASH_DIR):
            item_path = os.path.join(TRASH_DIR, item)
            # Name format: {topic}_{id}_{timestamp}
            try:
                parts = item.split('_')
                ts_str = f"{parts[-2]}_{parts[-1]}" # YYYYMMDD_HHMMSS
                ts = datetime.strptime(ts_str, "%Y%m%d_%H%M%S")
                
                if (now - ts).days > RETENTION_DAYS:
                    if os.path.isdir(item_path):
                        shutil.rmtree(item_path)
                    else:
                        os.remove(item_path)
                    cleaned += 1
            except Exception:
                # Malformed name or error, skip
                continue
        return cleaned

    def count_active_nodes(self) -> int:
        all_nodes = self.store.list_nodes()
        return len([n for n in all_nodes if n.state != NodeState.DUST])
