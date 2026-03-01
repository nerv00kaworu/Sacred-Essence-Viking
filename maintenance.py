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
    RETENTION_DAYS,
    MEMORY_DIR
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
                if score < THRESHOLD_SILVER:
                    node.state = NodeState.SILVER
                    report["downgraded_silver"] += 1
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
                node.state = NodeState.SILVER
                report["downgraded_silver"] += 1

        # Safety Net Check
        active_count = len(all_nodes) - len(nodes_by_state[NodeState.DUST])
        if active_count < MIN_KEEP_NODES:
            print(f"WARNING: Safety Net Triggered! Active nodes ({active_count}) < Min ({MIN_KEEP_NODES}). Aborting GC.")
            return report

        # Process Dust (Soil Extraction -> Trash)
        if not dry_run:
            for node in nodes_by_state[NodeState.DUST]:
                # Phase 3 feature: Extract essence to SOIL
                self._extract_soil(node)
                node.state = NodeState.SOIL
                self.store.move_to_trash(node)
                report["trashed"] += 1
            
            for node in updated_nodes:
                if node.state != NodeState.DUST:
                    self.store.save_node(node)

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

    def _extract_soil(self, node: 'MemoryNode'):
        """Extract dying memory essence into a global SOIL.md file."""
        import json
        
        # Read the raw content if possible
        content = ""
        topic_path = os.path.join(MEMORY_DIR, "topics", node.topic, node.id, "content.md")
        try:
            if os.path.exists(topic_path):
                with open(topic_path, 'r', encoding='utf-8') as f:
                    content = f.read()
        except:
            if node.L1_overview:
                content = node.L1_overview
        
        # We will use the L1 overview or extract the first few lines as a fallback summary
        summary = node.L1_overview
        if not summary and content:
            lines = [line.strip() for line in content.split('\\n') if line.strip() and not line.startswith('[NODE_ID:')]
            summary = ' '.join(lines[:3]) + ('...' if len(lines) > 3 else '')
            
        if not summary:
            summary = "No content available."

        # Append to SOIL
        soil_path = os.path.join(MEMORY_DIR, "SOIL.md")
        timestamp = datetime.now().strftime("%Y-%m-%d")
        
        try:
            with open(soil_path, 'a', encoding='utf-8') as sf:
                sf.write(f"\\n### [{timestamp}] {node.title}\\n")
                sf.write(f"**Topic**: {node.topic} | **Original ID**: {node.id}\\n")
                sf.write(f"{summary}\\n")
                sf.write("---\\n")
        except Exception as e:
            print(f"WARNING: Failed to extract SOIL for {node.id}: {e}")

    def count_active_nodes(self) -> int:
        all_nodes = self.store.list_nodes()
        return len([n for n in all_nodes if n.state != NodeState.DUST])
