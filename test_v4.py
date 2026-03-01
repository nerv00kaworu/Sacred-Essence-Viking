import sys
from datetime import datetime, timedelta

# Mock Config if running outside
sys.path.append('/home/nerv0/.openclaw/workspace/Sacred-Essence-Viking')
from models import MemoryNode, NodeState
from algorithms import calculate_importance

def run_tests():
    print("🧪 Testing Sacred Essence V3 Math (with Soil Compression)")
    
    # 1. New Node (Grace Period)
    n1 = MemoryNode(
        id='test1', topic='test', title='Grace Period Test',
        creation_date=datetime.now(), last_access_date=datetime.now()
    )
    print(f"Test 1 - Score (0 days, Grace): {calculate_importance(n1)}")
    print("-" * 30)
    
    # 2. Decayed Node (past grace period, unused for 60 days)
    # v3 decays slowly. 0.95 ^ 60 = 0.046. Score = 10 * 0.046 = 0.46 (Should fall below DUST=1.0)
    past = datetime.now() - timedelta(days=60)
    n2 = MemoryNode(
        id='test2', topic='test', title='Decay Test',
        creation_date=past, last_access_date=past
    )
    score2 = calculate_importance(n2, current_date=datetime.now())
    print(f"Test 2 - Score after 60 days decay: {score2}")
    
    # 3. High Density Inflation Cap
    # Simulate a node being accessed 100 times (Ln(1 + 20) = 3)
    n2.access_count = 100
    score3 = calculate_importance(n2, current_date=datetime.now())
    print(f"Test 3 - Score after 100 access count (Bonus + Decay): {score3}")
    
    n2.access_count = 1000
    score4 = calculate_importance(n2, current_date=datetime.now())
    print(f"Test 4 - Score after 1000 access count (Should cap growth to +5.0): {score4}")

if __name__ == '__main__':
    run_tests()
