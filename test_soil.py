import sys
import os
from datetime import datetime, timedelta

sys.path.append('/home/nerv0/.openclaw/workspace/Sacred-Essence-Viking')
from models import MemoryNode, NodeState
from config import TRASH_DIR, MEMORY_DIR
from maintenance import MaintenanceManager

# Mocking the store
class MockStore:
    def __init__(self, nodes):
        self.nodes = nodes
    def list_nodes(self):
        return self.nodes
    def move_to_trash(self, node):
        print(f"🗑️ Trashed: {node.id}")
    def save_node(self, node):
        print(f"💾 Saved: {node.id}, state: {node.state.value}")

def test_soil():
    print("🧪 Testing SOIL Compression")
    n = MemoryNode(
        id='test_soil_node', topic='test', title='Dying Node',
        creation_date=datetime.now() - timedelta(days=200),
        last_access_date=datetime.now() - timedelta(days=200)
    )
    # The node is 200 days old, score should naturally decay well below 1.0
    
    # Bypass Safety Net by adding 25 dummy active nodes
    dummy_nodes = [
        MemoryNode(id=f'dummy_{i}', topic='test', title=f'Dummy {i}', 
                  creation_date=datetime.now(), last_access_date=datetime.now())
        for i in range(25)
    ]
    
    mock_store = MockStore([n] + dummy_nodes)
    manager = MaintenanceManager(mock_store)
    
    # Run GC
    report = manager.run_garbage_collection(dry_run=False)
    print(f"GC Report: {report}")
    
    # Check if SOIL.md was created
    soil_path = os.path.join(MEMORY_DIR, "SOIL.md")
    if os.path.exists(soil_path):
        with open(soil_path, 'r', encoding='utf-8') as f:
            print("--- SOIL.md Content ---")
            print(f.read())
            print("-----------------------")

if __name__ == '__main__':
    test_soil()
