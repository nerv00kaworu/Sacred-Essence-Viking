# Sacred Essence v3.1 Projection System

from typing import List, Dict
from models import MemoryNode, NodeState
from storage import MemoryStore
from algorithms import calculate_importance

class ProjectionEngine:
    def __init__(self, store: MemoryStore):
        self.store = store

    def project_context(self, topic: str, target_id: str) -> Dict[str, List[str]]:
        """
        Generate Context Mask based on v3.1 Protocol.
        Returns dictionary with keys: 'core', 'siblings', 'ancestors', 'golden'.
        """
        context = {
            "core": [],
            "siblings": [],
            "ancestors": [], # Ancestors not fully implemented as we have flat Topic/Node structure in generic MemoryNode
                             # But assuming hierarchical naming or metadata could support it.
                             # For now, we will assume generic "Global Golden" as ancestors.
            "golden": []
        }
        
        # 1. Target (Core)
        target = self.store.load_node(topic, target_id)
        if target:
            # Full L1 + L0
            # If we had L1 content loaded:
            core_content = f"Title: {target.title}\nTopic: {target.topic}\nAbstract: {target.L0_abstract}\nOverview: {target.L1_overview}"
            context["core"].append(core_content)
        else:
            return context # Empty if target not found
            
        # 2. Siblings (Neighbors)
        # Rule: Top 5 by Current Score
        all_siblings = self.store.get_siblings(target)
        # Calculate current importance for sorting
        scored_siblings = []
        for sib in all_siblings:
            score = calculate_importance(sib)
            scored_siblings.append((sib, score))
            
        scored_siblings.sort(key=lambda x: x[1], reverse=True)
        top_siblings = scored_siblings[:5]
        
        for sib, score in top_siblings:
            # Only L0 for siblings
            content = f"Sibling: {sib.title} (Score: {score:.2f})\nAbstract: {sib.L0_abstract}"
            context["siblings"].append(content)
            
        # 3. Global Golden (Ancestors/Roots)
        # We fetch all Golden nodes
        all_nodes = self.store.list_nodes()
        golden_nodes = [n for n in all_nodes if n.state == NodeState.GOLDEN and n.id != target_id]
        
        # Limit Golden to max 10 (as per formula example "Max 10")
        # Sort by importance or access? Usually importance.
        scored_golden = []
        for g in golden_nodes:
            score = calculate_importance(g)
            scored_golden.append((g, score))
            
        scored_golden.sort(key=lambda x: x[1], reverse=True)
        top_golden = scored_golden[:10]
        
        for g, score in top_golden:
            content = f"Global: {g.title}\nAbstract: {g.L0_abstract}"
            context["golden"].append(content)
            
        return context

    def render_context(self, context: Dict[str, List[str]]) -> str:
        """Render context to string for LLM injection."""
        output = []
        output.append("=== CONTEXT MASK ===")
        
        output.append("--- TARGET CORE ---")
        output.extend(context["core"])
        
        output.append("\n--- RELATED SIBLINGS ---")
        output.extend(context["siblings"])
        
        output.append("\n--- GLOBAL ANCHORS ---")
        output.extend(context["golden"])
        
        return "\n".join(output)
