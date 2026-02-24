# Sacred Essence v3.1 CLI
# 神髓記憶系統 - 整合 QMD 深度搜索（Edge Cases 修補版）

import argparse
import sys
import os
from datetime import datetime
from uuid import uuid4
from typing import Set

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
    
    # Search (新增：統一搜索入口)
    search_parser = subparsers.add_parser("search", help="Smart search with Sacred Essence + QMD + Fallback")
    search_parser.add_argument("text", help="Query text")
    search_parser.add_argument("--nodes", nargs="+", help="Optional node whitelist (if not provided, uses top nodes from Sacred Essence)")
    search_parser.add_argument("--confidence", type=float, default=0.5, help="Sacred Essence confidence threshold (0-1)")
    search_parser.add_argument("-n", type=int, default=5, help="Number of results")
    search_parser.add_argument("--no-fallback", action="store_true", help="Disable fallback mechanism")
    search_parser.add_argument("--no-full-l2", action="store_true", help="Disable loading full L2 content")
    search_parser.add_argument("--collection", default="sacred-l2", help="QMD collection name")

    # QMD Integration
    qmd_parser = subparsers.add_parser("qmd", help="QMD Integration - Enhanced search and indexing")
    qmd_subparsers = qmd_parser.add_subparsers(dest="qmd_command", help="QMD commands")
    
    # qmd sync
    qmd_sync = qmd_subparsers.add_parser("sync", help="Sync Sacred Essence memories to QMD index")
    qmd_sync.add_argument("--collection", default="sacred-l2", help="QMD collection name")
    qmd_sync.add_argument("--force", action="store_true", help="Force re-index")
    qmd_sync.add_argument("--filter-states", nargs="+", choices=["GOLDEN", "SILVER", "BRONZE", "DUST"],
                         help="Only sync nodes with specified states")
    
    # qmd audit (新增：數據一致性審計)
    qmd_audit = qmd_subparsers.add_parser("audit", help="Audit data consistency between Sacred Essence and QMD")
    qmd_audit.add_argument("--execute", action="store_true", help="Execute cleanup (default is dry-run)")
    qmd_audit.add_argument("--collection", default="sacred-l2", help="QMD collection name")
    
    # qmd query
    qmd_query = qmd_subparsers.add_parser("query", help="Query using QMD (hybrid search)")
    qmd_query.add_argument("text", help="Query text")
    qmd_query.add_argument("-n", type=int, default=5, help="Number of results")
    qmd_query.add_argument("--collection", default="sacred-l2", help="QMD collection name")
    
    # qmd vsearch
    qmd_vsearch = qmd_subparsers.add_parser("vsearch", help="Vector similarity search via QMD")
    qmd_vsearch.add_argument("text", help="Query text")
    qmd_vsearch.add_argument("-n", type=int, default=5, help="Number of results")
    qmd_vsearch.add_argument("--collection", default="sacred-l2", help="QMD collection name")
    
    # qmd constrained-search (限縮搜索)
    qmd_constrained = qmd_subparsers.add_parser("constrained-search", 
        help="Search within specified node whitelist (限縮搜索)")
    qmd_constrained.add_argument("text", help="Query text")
    qmd_constrained.add_argument("--nodes", nargs="+", required=True, 
        help="Node ID whitelist to search within")
    qmd_constrained.add_argument("-n", type=int, default=5, help="Number of results")
    qmd_constrained.add_argument("--type", choices=["hybrid", "vector", "keyword"], 
        default="hybrid", help="Search type")
    qmd_constrained.add_argument("--collection", default="sacred-l2", help="QMD collection name")
    
    # qmd status
    qmd_status = qmd_subparsers.add_parser("status", help="Check QMD index status")

    args = parser.parse_args()
    
    store = MemoryStore()
    maintenance = MaintenanceManager(store)
    projection = ProjectionEngine(store)

    if args.command == "encode":
        # Create new node
        node_id = str(uuid4())[:8]
        node = MemoryNode(
            id=node_id,
            topic=args.topic,
            title=args.title,
            content_path="",
            creation_date=datetime.now(),
            last_access_date=datetime.now(),
            state=NodeState.SILVER,
            L0_abstract=args.abstract,
            L1_overview=""
        )
        
        # Save content first
        node_dir = store._get_node_dir(node.topic, node.id)
        os.makedirs(node_dir, exist_ok=True)
        content_file = os.path.join(node_dir, "content.md")
        with open(content_file, 'w', encoding='utf-8') as f:
            f.write(args.content)
        
        node.content_path = content_file

        # Save node to Sacred Essence
        store.save_node(node)
        print(f"✅ Encoded to Sacred Essence: {node.topic}/{node.id} - {node.title}")
        
        # Auto-sync to QMD (方案 B: 自動同步)
        try:
            from qmd_bridge import QMDBridge
            print(f"🔄 Auto-syncing L2 content to QMD...")
            bridge = QMDBridge("sacred-l2")
            sync_success = bridge.sync_node_to_qmd(
                node_id=node_id,
                topic=args.topic,
                content=args.content,
                state="SILVER",
                parent_id=None
            )
            if sync_success:
                print(f"✅ Synced to QMD: {node_id}")
            else:
                print(f"⚠️  QMD sync failed (non-critical)")
        except Exception as e:
            print(f"⚠️  QMD sync skipped: {e}")

    elif args.command == "gc":
        print(f"Running Garbage Collection (Dry Run: {not args.execute})...")
        report = maintenance.run_garbage_collection(dry_run=not args.execute)
        print("Report:", report)
        
        # GC 後觸發 QMD 審計（修補 Edge Case 2）
        if args.execute:
            print("\n🔍 Triggering QMD audit after GC...")
            try:
                from qmd_bridge import QMDBridge
                bridge = QMDBridge("sacred-l2")
                audit_report = bridge.audit_and_cleanup(dry_run=False)
                if audit_report["orphaned_in_qmd"]:
                    print(f"⚠️  Found {len(audit_report['orphaned_in_qmd'])} orphaned entries in QMD")
                    print("💡 Run 'python main.py qmd sync --force' to rebuild QMD index if needed")
            except Exception as e:
                print(f"⚠️  QMD audit skipped: {e}")

    elif args.command == "project":
        ctx = projection.project_context(args.topic, args.id)
        print(projection.render_context(ctx))
        
    elif args.command == "list":
        nodes = store.list_nodes(args.topic)
        print(f"Found {len(nodes)} nodes.")
        for n in nodes:
            score = calculate_importance(n)
            print(f"[{n.state.value}] {n.topic}/{n.id} - {n.title} (Score: {score:.2f})")
    
    elif args.command == "search":
        # 新增：統一搜索入口（含逃生艙機制）
        try:
            from qmd_bridge import QMDBridge, SearchResult
        except ImportError as e:
            print(f"❌ QMD Bridge not available: {e}")
            sys.exit(1)
        
        bridge = QMDBridge(args.collection)
        
        # 如果沒有提供白名單，從神髓獲取相關節點
        node_whitelist: Set[str] = set(args.nodes) if args.nodes else set()
        sacred_confidence = args.confidence
        
        if not node_whitelist:
            print("🔍 No whitelist provided, retrieving relevant nodes from Sacred Essence...")
            # 簡化：列出所有節點作為白名單（實際應使用神髓的語義檢索）
            all_nodes = store.list_nodes()
            # 按重要性排序，取前 20
            scored_nodes = [(n, calculate_importance(n)) for n in all_nodes]
            scored_nodes.sort(key=lambda x: x[1], reverse=True)
            node_whitelist = {n.id for n, _ in scored_nodes[:20]}
            print(f"   Selected top {len(node_whitelist)} nodes as whitelist")
            sacred_confidence = 0.4  # 自動選擇時降低信心閾值
        
        # 執行智能搜索（含逃生艙）
        print(f"\n🔍 Smart Search: '{args.text}'")
        print(f"   Whitelist: {len(node_whitelist)} nodes")
        print(f"   Confidence: {sacred_confidence}\n")
        
        results, metadata = bridge.smart_search_with_fallback(
            query_text=args.text,
            node_whitelist=node_whitelist,
            sacred_confidence=sacred_confidence,
            n_results=args.n,
            load_full_l2=not args.no_full_l2
        )
        
        print(f"📊 Strategy: {metadata['strategy']}")
        print(f"   Fallback triggered: {metadata['fallback_triggered']}")
        print(f"   Results: {len(results)}\n")
        
        for i, r in enumerate(results, 1):
            chunk_marker = "📄" if r.is_chunk else "📑"
            print(f"{i}. {chunk_marker} [{r.score:.3f}] {r.node_id} ({r.source})")
            content_preview = r.content[:200].replace('\n', ' ')
            print(f"   {content_preview}...\n")

    elif args.command == "qmd":
        # Lazy import QMD bridge
        try:
            from qmd_bridge import QMDBridge, sync_sacred_essence_to_qmd
        except ImportError as e:
            print(f"❌ QMD Bridge not available: {e}")
            print("💡 Tip: Ensure qmd_bridge.py is in the same directory")
            sys.exit(1)
        
        if args.qmd_command == "sync":
            success = sync_sacred_essence_to_qmd(
                collection_name=args.collection,
                filter_states=args.filter_states
            )
            if success:
                print(f"✅ Successfully synced to QMD collection: {args.collection}")
            else:
                print(f"❌ Sync failed")
                sys.exit(1)
        
        elif args.qmd_command == "audit":
            # 新增：數據一致性審計
            bridge = QMDBridge(args.collection)
            print(f"🔍 Auditing data consistency (Dry Run: {not args.execute})...\n")
            
            report = bridge.audit_and_cleanup(dry_run=not args.execute)
            
            print(f"📊 Audit Report ({report['timestamp']})")
            print(f"   ✅ Correctly synced: {len(report['synced_correctly'])} nodes")
            print(f"   🗑️  Orphaned in QMD: {len(report['orphaned_in_qmd'])} nodes")
            if report['orphaned_in_qmd']:
                print(f"      {report['orphaned_in_qmd'][:5]}{'...' if len(report['orphaned_in_qmd']) > 5 else ''}")
            print(f"   ❌ Missing in QMD: {len(report['missing_in_qmd'])} nodes")
            if report['missing_in_qmd']:
                print(f"      {report['missing_in_qmd'][:5]}{'...' if len(report['missing_in_qmd']) > 5 else ''}")
            
            if report.get('actions_taken'):
                print(f"\n🔧 Actions taken: {report['actions_taken']}")
            
            if not args.execute and (report['orphaned_in_qmd'] or report['missing_in_qmd']):
                print(f"\n💡 Run with --execute to perform cleanup")
        
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
        
        elif args.qmd_command == "constrained-search":
            bridge = QMDBridge(args.collection)
            node_whitelist: Set[str] = set(args.nodes)
            
            print(f"🔍 Constrained Search: '{args.text}'")
            print(f"🎯 Node Whitelist: {len(node_whitelist)} nodes\n")
            
            results = bridge.constrained_search(
                query_text=args.text,
                node_whitelist=node_whitelist,
                n_results=args.n,
                search_type=args.type
            )
            
            print(f"📊 Found {len(results)} results within whitelist\n")
            for i, r in enumerate(results, 1):
                score = r.get('score', 0)
                node_id = r.get('node_id', 'N/A')
                content_preview = r.get('content', '')[:150].replace('\n', ' ')
                print(f"{i}. [{score:.3f}] Node: {node_id}")
                print(f"   {content_preview}...\n")
        
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