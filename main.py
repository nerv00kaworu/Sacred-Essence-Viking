# Sacred Essence v3.1 CLI

import argparse
import sys
import os
from datetime import datetime
from uuid import uuid4

from storage import MemoryStore
from models import MemoryNode, NodeState
from maintenance import MaintenanceManager
from projection import ProjectionEngine
from algorithms import calculate_importance

def main():
    parser = argparse.ArgumentParser(description="Sacred Essence v3.1 Memory System")
    subparsers = parser.add_subparsers(dest="command", help="Command to execute")

    # Encode
    encode_parser = subparsers.add_parser("encode", help="Encode new memory")
    encode_parser.add_argument("--topic", required=True, help="Topic name")
    encode_parser.add_argument("--title", required=True, help="Memory title")
    encode_parser.add_argument("--content", required=True, help="Memory content (L2)")
    encode_parser.add_argument("--abstract", default="", help="L0 Abstract")

    # Decay / GC
    gc_parser = subparsers.add_parser("gc", help="Run Garbage Collection")
    gc_parser.add_argument("--execute", action="store_true", help="Execute changes (default is dry-run)")

    # Project
    proj_parser = subparsers.add_parser("project", help="Project Context for a node")
    proj_parser.add_argument("--topic", required=True)
    proj_parser.add_argument("--id", required=True)
    
    # List
    list_parser = subparsers.add_parser("list", help="List nodes")
    list_parser.add_argument("--topic", help="Filter by topic")

    args = parser.parse_args()
    
    store = MemoryStore()
    maintenance = MaintenanceManager(store)
    projection = ProjectionEngine(store)

    if args.command == "encode":
        # Create new node
        node_id = str(uuid4())[:8] # Simple ID
        node = MemoryNode(
            id=node_id,
            topic=args.topic,
            title=args.title,
            content_path="", # Will be set by store logic effectively
            creation_date=datetime.now(),
            last_access_date=datetime.now(),
            state=NodeState.SILVER, # Default new state
            L0_abstract=args.abstract,
            L1_overview="" # Optional
        )
        
        # Save content first
        node_dir = store._get_node_dir(node.topic, node.id)
        os.makedirs(node_dir, exist_ok=True)
        content_file = os.path.join(node_dir, "content.md")
        with open(content_file, 'w', encoding='utf-8') as f:
            f.write(args.content)
        
        node.content_path = content_file

        # Save node
        store.save_node(node)
        print(f"Encoded memory: {node.topic}/{node.id} - {node.title}")

    elif args.command == "gc":
        print(f"Running Garbage Collection (Dry Run: {not args.execute})...")
        report = maintenance.run_garbage_collection(dry_run=not args.execute)
        print("Report:", report)

    elif args.command == "project":
        ctx = projection.project_context(args.topic, args.id)
        print(projection.render_context(ctx))
        
    elif args.command == "list":
        nodes = store.list_nodes(args.topic)
        print(f"Found {len(nodes)} nodes.")
        for n in nodes:
            score = calculate_importance(n)
            print(f"[{n.state.value}] {n.topic}/{n.id} - {n.title} (Score: {score:.2f})")

    else:
        parser.print_help()

if __name__ == "__main__":
    main()
