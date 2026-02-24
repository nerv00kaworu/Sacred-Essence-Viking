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
        5. Trigger QMD Audit (Edge Case 2: Data Consistency)
        """
        report = {"scanned": 0, "downgraded_silver": 0, "marked_dust": 0, "trashed": 0, "cleaned_trash": 0, "qmd_audit": None}
        
        all_nodes = self.store.list_nodes()
        nodes_by_state = {s: [] for s in NodeState}
        
        # 1-4. Original GC logic...
        current_time = datetime.now()
        updated_nodes = []
        
        for node in all_nodes:
            report["scanned"] += 1
            score = calculate_importance(node, current_time)
            
            if node.state == NodeState.GOLDEN:
                pass 
            elif node.state == NodeState.SILVER:
                if score < THRESHOLD_SILVER:
                    if score < THRESHOLD_DUST:
                        node.state = NodeState.DUST
                        report["marked_dust"] += 1
                    else:
                        node.state = NodeState.BRONZE
                        report["downgraded_silver"] += 1
            elif node.state == NodeState.BRONZE:
                if score < THRESHOLD_DUST:
                     node.state = NodeState.DUST
                     report["marked_dust"] += 1
            
            nodes_by_state[node.state].append(node)
            updated_nodes.append(node)

        # Enforce Golden Soft Cap
        golden_nodes = nodes_by_state[NodeState.GOLDEN]
        if len(golden_nodes) > SOFT_CAP_GOLDEN:
            golden_nodes.sort(key=lambda x: x.last_access_date) 
            excess = len(golden_nodes) - SOFT_CAP_GOLDEN
            for i in range(excess):
                node = golden_nodes[i]
                
                # Evaluate score immediately to prevent delayed state transition
                score = calculate_importance(node, current_time)
                if score < THRESHOLD_DUST:
                    node.state = NodeState.DUST
                    report["marked_dust"] += 1
                elif score < THRESHOLD_SILVER:
                    node.state = NodeState.BRONZE
                    report["downgraded_silver"] += 1
                else:
                    node.state = NodeState.SILVER
                    report["downgraded_silver"] += 1
                    
                # Add to corresponding state list so it will be trashed if DUST
                nodes_by_state[node.state].append(node)

        # Safety Net Check
        active_count = len(all_nodes) - len(nodes_by_state[NodeState.DUST])
        if active_count < MIN_KEEP_NODES:
            print(f"WARNING: Safety Net Triggered! Active nodes ({active_count}) < Min ({MIN_KEEP_NODES}). Aborting GC.")
            return report

        # Move Dust to Trash
        if not dry_run:
            # 引入 QMD Bridge 以執行刪除
            bridge_instance = None
            try:
                from qmd_bridge import QMDBridge
                bridge_instance = QMDBridge("sacred-l2")
            except Exception as e:
                print(f"⚠️  Could not init QMD Bridge for GC deletion: {e}")
                
            for node in nodes_by_state[NodeState.DUST]:
                # Exclude nodes that were inherently DUST and trashed before to prevent duplicate trash moves
                # We assume store.move_to_trash handles if it doesn't exist anymore, but wait updated_nodes logic
                self.store.move_to_trash(node)
                report["trashed"] += 1
                
                # 防禦『資料幽靈』：同步從 QMD 中刪除
                if bridge_instance:
                    bridge_instance.delete_node(node.id)
            
            for node in updated_nodes:
                if node.state != NodeState.DUST:
                    # Optimize File I/O: Only save if changed state or interacted (is_dirty)
                    is_modified = getattr(node, 'is_dirty', False)
                    # We can't easily check state change here without tracking original.
                    # As a workaround, just save if is_dirty flag is True.
                    # Let's save unconditionally if it's dirty, OR if its score indicates a recent change.
                    # Better solution: Always save nodes whose state is not DUST and is dirty.
                    if getattr(node, 'is_dirty', True):
                        self.store.save_node(node)
                        if hasattr(node, 'is_dirty'):
                            node.is_dirty = False

            report["cleaned_trash"] = self._clean_trash()
            
            # 5. Trigger QMD Audit (Edge Case 2)
            try:
                from qmd_bridge import QMDBridge
                bridge = QMDBridge("sacred-l2")
                audit_report = bridge.audit_and_cleanup(dry_run=True)
                report["qmd_audit"] = {
                    "orphaned": len(audit_report["orphaned_in_qmd"]),
                    "missing": len(audit_report["missing_in_qmd"])
                }
            except Exception as e:
                report["qmd_audit"] = {"error": str(e)}
            
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
