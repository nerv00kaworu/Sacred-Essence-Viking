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

    # QMD Integration
    qmd_parser = subparsers.add_parser("qmd", help="QMD Integration - Enhanced search and indexing")
    qmd_subparsers = qmd_parser.add_subparsers(dest="qmd_command", help="QMD commands")
    
    # qmd sync
    qmd_sync = qmd_subparsers.add_parser("sync", help="Sync Sacred Essence memories to QMD index")
    qmd_sync.add_argument("--collection", default="sacred-essence", help="QMD collection name")
    qmd_sync.add_argument("--force", action="store_true", help="Force re-index")
    
    # qmd query
    qmd_query = qmd_subparsers.add_parser("query", help="Query using QMD (hybrid search)")
    qmd_query.add_argument("text", help="Query text")
    qmd_query.add_argument("-n", type=int, default=5, help="Number of results")
    qmd_query.add_argument("--collection", default="sacred-essence", help="QMD collection name")
    
    # qmd vsearch
    qmd_vsearch = qmd_subparsers.add_parser("vsearch", help="Vector similarity search via QMD")
    qmd_vsearch.add_argument("text", help="Query text")
    qmd_vsearch.add_argument("-n", type=int, default=5, help="Number of results")
    qmd_vsearch.add_argument("--collection", default="sacred-essence", help="QMD collection name")
    
    # qmd status
    qmd_status = qmd_subparsers.add_parser("status", help="Check QMD index status")

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

    elif args.command == "qmd":
        # Lazy import QMD bridge
        try:
            from qmd_bridge import QMDBridge, sync_sacred_essence_to_qmd
        except ImportError as e:
            print(f"❌ QMD Bridge not available: {e}")
            print("💡 Tip: Ensure qmd_bridge.py is in the same directory")
            sys.exit(1)
        
        if args.qmd_command == "sync":
            success = sync_sacred_essence_to_qmd(collection_name=args.collection)
            if success:
                print(f"✅ Successfully synced to QMD collection: {args.collection}")
            else:
                print(f"❌ Sync failed")
                sys.exit(1)
        
        elif args.qmd_command == "query":
            bridge = QMDBridge(args.collection)
            results = bridge.query(args.text, n_results=args.n)
            print(f"🔍 QMD Query: '{args.text}'")
            print(f"📊 Found {len(results)} results\n")
            for i, r in enumerate(results, 1):
                score = r.get('score', 0)
                filepath = r.get('filepath', 'N/A')
                snippet = r.get('snippet', '')[:200]
                print(f"{i}. [{score:.3f}] {filepath}")
                print(f"   {snippet}...\n")
        
        elif args.qmd_command == "vsearch":
            bridge = QMDBridge(args.collection)
            results = bridge.vector_search(args.text, n_results=args.n)
            print(f"🔮 QMD Vector Search: '{args.text}'")
            print(f"📊 Found {len(results)} results\n")
            for i, r in enumerate(results, 1):
                score = r.get('score', 0)
                filepath = r.get('filepath', 'N/A')
                snippet = r.get('snippet', '')[:200]
                print(f"{i}. [{score:.3f}] {filepath}")
                print(f"   {snippet}...\n")
        
        elif args.qmd_command == "status":
            bridge = QMDBridge()
            status = bridge.status()
            print(f"QMD Status: {status['status']}")
            if status['status'] == 'ok':
                print(status['details'])
            else:
                print(f"Error: {status.get('error', 'Unknown')}")
        
        else:
            qmd_parser.print_help()

    else:
        parser.print_help()

if __name__ == "__main__":
    main()
