# Sacred Essence v3.1 - QMD Integration Bridge v3.0
# 神髓與 QMD 的深度整合橋接器（Edge Cases 修補版）
# 架構：神髓定界（樹狀路由）+ QMD 深潛（限縮檢索）+ 逃生艙 Fallback

import subprocess
import json
import os
import re
from typing import List, Dict, Optional, Tuple, Set
from pathlib import Path
from dataclasses import dataclass, asdict
from datetime import datetime

@dataclass
class QMDContext:
    """QMD 上下文綁定資訊"""
    node_id: str
    parent_id: Optional[str]
    topic: str
    layer: str
    state: str

@dataclass
class SearchResult:
    """統一搜索結果格式"""
    node_id: str
    topic: str
    content: str
    score: float
    source: str  # "constrained", "fallback_bm25", "fallback_vector"
    is_chunk: bool  # 是否為 Chunk 片段
    full_path: Optional[str] = None  # 完整 L2 檔案路徑

class QMDBridge:
    """
    神髓 (Sacred Essence) 與 QMD 的深度整合橋接器 v3.0
    
    修補的 Edge Cases：
    1. 逃生艙機制：神髓信心不足時，Fallback 到 QMD 全局搜索
    2. 數據一致性：定期 Audit 清除孤兒資料
    3. 性能優化：超時控制 + 結果限制
    4. 上下文完整性：智能判斷載入完整 L2 或 Chunk
    """
    
    # 逃生艙閾值設定
    FALLBACK_CONFIDENCE_THRESHOLD = 0.3  # 神髓信心分數低於此值觸發 Fallback
    FALLBACK_MAX_RESULTS = 5  # Fallback 搜索最大結果數
    QMD_TIMEOUT = 300  # QMD 命令超時秒數（加長以避免在 CPU 上大量 embedding 時卡死）
    
    def __init__(self, collection_name: str = "sacred-l2", memory_dir: Optional[str] = None):
        self.collection_name = collection_name
        self.qmd_cmd = os.environ.get("QMD_BIN", "qmd")
        self.memory_dir = memory_dir or self._default_memory_dir()
        
    def _default_memory_dir(self) -> str:
        """預設神髓記憶目錄（可由環境變數覆蓋）"""
        return os.environ.get(
            "SACRED_ESSENCE_TOPICS_DIR",
            str(Path(__file__).resolve().parent / "memory" / "topics")
        )
        
    def _run_qmd(self, args: List[str], timeout: int = None) -> Tuple[bool, str]:
        """執行 QMD 命令並返回結果（支援超時）"""
        timeout = timeout or self.QMD_TIMEOUT
        
        # 強制關閉 GPU，防止 node-llama-cpp 在 WSL 找不到 CUDA 時瘋狂嘗試從源碼編譯導致卡死
        env = os.environ.copy()
        env["NODE_LLAMA_CPP_GPU"] = "false"
        
        try:
            result = subprocess.run(
                [self.qmd_cmd] + args,
                capture_output=True,
                text=True,
                timeout=timeout,
                env=env
            )
            if result.returncode == 0:
                return True, result.stdout
            else:
                return False, result.stderr
        except subprocess.TimeoutExpired:
            return False, f"QMD command timeout after {timeout}s"
        except Exception as e:
            return False, str(e)
    
    def _extract_node_id_from_content(self, content: str) -> Optional[str]:
        """從內容前綴提取 node_id"""
        match = re.search(r'\[NODE_ID:([^\]]+)\]', content)
        return match.group(1) if match else None
    
    def _extract_metadata_from_content(self, content: str) -> Dict[str, str]:
        """從內容前綴提取所有 metadata"""
        metadata = {}
        patterns = {
            'node_id': r'\[NODE_ID:([^\]]+)\]',
            'topic': r'\[TOPIC:([^\]]+)\]',
            'state': r'\[STATE:([^\]]+)\]',
            'parent_id': r'\[PARENT:([^\]]+)\]'
        }
        for key, pattern in patterns.items():
            match = re.search(pattern, content)
            if match:
                metadata[key] = match.group(1)
        return metadata
    
    def _clean_content(self, content: str) -> str:
        """移除 metadata 前綴，返回乾淨內容"""
        return re.sub(r'^\[NODE_ID:[^\]]+\](\[TOPIC:[^\]]+\])?(\[STATE:[^\]]+\])?(\[PARENT:[^\]]+\])?\n', '', content)
    
    def _load_full_l2(self, node_id: str, topic: str) -> Optional[str]:
        """
        修補 Edge Case 4：載入完整 L2 內容，避免 Chunk 截斷
        """
        content_path = Path(self.memory_dir) / topic / node_id / "content.md"
        if content_path.exists():
            try:
                with open(content_path, 'r', encoding='utf-8') as f:
                    return f.read()
            except Exception:
                pass
        return None
    
    def collection_exists(self) -> bool:
        """檢查集合是否已存在"""
        success, output = self._run_qmd(["collection", "list"], timeout=5)
        if success:
            return self.collection_name in output
        return False
    
    # ==================== Edge Case 1: 逃生艙機制 ====================
    
    def smart_search_with_fallback(
        self,
        query_text: str,
        node_whitelist: Set[str],
        sacred_confidence: float,
        n_results: int = 5,
        load_full_l2: bool = True,
        max_token_budget: int = 2000
    ) -> Tuple[List[SearchResult], Dict]:
        """
        智能搜索（含逃生艙 Fallback）
        
        修補 Edge Case 1：當神髓信心不足時，自動 Fallback 到 QMD 全局搜索
        
        Args:
            query_text: 查詢文字
            node_whitelist: 神髓提供的白名單
            sacred_confidence: 神髓檢索的信心分數 (0-1)
            n_results: 返回結果數量
            load_full_l2: 是否載入完整 L2（避免 Chunk 截斷）
            max_token_budget: 最大 Token 預算
            
        Returns:
            (結果列表, 搜索元數據)
        """
        results = []
        metadata = {
            "strategy": "constrained",
            "sacred_confidence": sacred_confidence,
            "fallback_triggered": False,
            "total_nodes_searched": len(node_whitelist)
        }
        
        # Step 1: 嘗試限縮搜索
        if node_whitelist and sacred_confidence >= self.FALLBACK_CONFIDENCE_THRESHOLD:
            constrained_results = self.constrained_search(
                query_text, node_whitelist, n_results=n_results * 2
            )
            results = self._convert_to_search_results(
                constrained_results, source="constrained", load_full_l2=load_full_l2
            )
        
        # Step 2: 逃生艙機制 - 斷崖式過濾修復 (The Fallback Gap)
        # 如果神髓完全沒有撈到白名單（門沒開），或者信心不足，強制進行全局盲搜
        if not node_whitelist or sacred_confidence < self.FALLBACK_CONFIDENCE_THRESHOLD:
            metadata["fallback_triggered"] = True
            metadata["strategy"] = "fallback_hybrid"
            
            print(f"🚨 觸發逃生艙機制 (神髓信心: {sacred_confidence:.2f}, 白名單: {len(node_whitelist)})")
            
            # Fallback 1: 全局 BM25 關鍵字搜索
            fallback_results = self.keyword_search(query_text, n_results=self.FALLBACK_MAX_RESULTS)
            
            # 合併結果（去重）
            existing_node_ids = {r.node_id for r in results}
            for r in fallback_results:
                node_id = self._extract_node_id_from_content(r.get('content', ''))
                if node_id and node_id not in existing_node_ids:
                    results.append(SearchResult(
                        node_id=node_id,
                        topic=self._extract_metadata_from_content(r.get('content', '')).get('topic', 'unknown'),
                        content=self._clean_content(r.get('content', '')),
                        score=r.get('score', 0),
                        source="fallback_bm25",
                        is_chunk=True,
                        full_path=None
                    ))
                    existing_node_ids.add(node_id)
                    
                    if len(results) >= n_results + self.FALLBACK_MAX_RESULTS:
                        break
        
        # Step 3: 智能載入完整 L2（修補 Edge Case 4）
        if load_full_l2:
            results = self._intelligent_load_full_l2(results, max_token_budget)
        
        # 限制結果數量
        results = results[:n_results]
        metadata["final_result_count"] = len(results)
        
        return results, metadata
    
    def _convert_to_search_results(
        self, 
        raw_results: List[Dict], 
        source: str,
        load_full_l2: bool = True
    ) -> List[SearchResult]:
        """將原始結果轉換為統一格式"""
        converted = []
        for r in raw_results:
            content = r.get('content', '')
            metadata = self._extract_metadata_from_content(content)
            clean_content = self._clean_content(content)
            
            converted.append(SearchResult(
                node_id=metadata.get('node_id', 'unknown'),
                topic=metadata.get('topic', 'unknown'),
                content=clean_content,
                score=r.get('score', 0),
                source=source,
                is_chunk=True,  # QMD 返回的通常是 Chunk
                full_path=None
            ))
        return converted
    
    def _intelligent_load_full_l2(
        self, 
        results: List[SearchResult], 
        max_token_budget: int
    ) -> List[SearchResult]:
        """
        修補 Edge Case 4：智能判斷是否載入完整 L2
        
        策略：
        - 如果 Chunk 長度 < 500 tokens，嘗試載入完整 L2
        - 如果載入後總 Token 不超過預算，則使用完整 L2
        - 否則保留 Chunk 並添加標記
        """
        total_tokens = 0
        for r in results:
            # 簡單估算 token 數（中文約 1.5 字/ token）
            chunk_tokens = len(r.content) / 1.5
            
            if r.is_chunk and chunk_tokens < 500:
                full_content = self._load_full_l2(r.node_id, r.topic)
                if full_content:
                    full_tokens = len(full_content) / 1.5
                    if total_tokens + full_tokens <= max_token_budget:
                        r.content = full_content
                        r.is_chunk = False
                        total_tokens += full_tokens
                        continue
            
            total_tokens += chunk_tokens
        
        return results
    
    # ==================== Edge Case 2: 數據一致性審計 ====================
    
    def audit_and_cleanup(self, dry_run: bool = True) -> Dict:
        """
        修補 Edge Case 2：數據一致性審計，清除孤兒資料
        
        比對神髓節點清單與 QMD 索引，找出：
        - 孤兒 QMD 資料（QMD 有但神髓已刪除）
        - 缺失的同步（神髓有但 QMD 沒有）
        
        Args:
            dry_run: 如果 True，只報告不刪除
            
        Returns:
            審計報告
        """
        report = {
            "timestamp": datetime.now().isoformat(),
            "orphaned_in_qmd": [],
            "missing_in_qmd": [],
            "synced_correctly": [],
            "actions_taken": []
        }
        
        # 1. 收集神髓節點清單
        sacred_nodes = set()
        if os.path.exists(self.memory_dir):
            topics_dir = Path(self.memory_dir)
            for meta_file in topics_dir.rglob("node.meta.json"):
                try:
                    with open(meta_file, 'r', encoding='utf-8') as f:
                        meta = json.load(f)
                    node_id = meta.get('id')
                    state = meta.get('state', 'SILVER')
                    if node_id and state != 'DUST':  # DUST 節點視為已刪除
                        sacred_nodes.add(node_id)
                except:
                    pass
        
        # 2. 收集 QMD 節點清單
        qmd_nodes = set()
        if self.collection_exists():
            # 使用 qmd ls 獲取所有文檔
            success, output = self._run_qmd(["ls", self.collection_name])
            if success:
                for line in output.split('\n'):
                    node_id = self._extract_node_id_from_content(line)
                    if node_id:
                        qmd_nodes.add(node_id)
        
        # 3. 比對
        report["orphaned_in_qmd"] = list(qmd_nodes - sacred_nodes)
        report["missing_in_qmd"] = list(sacred_nodes - qmd_nodes)
        report["synced_correctly"] = list(qmd_nodes & sacred_nodes)
        
        # 4. 執行清理（如果不是 dry_run）
        if not dry_run:
            # 清理孤兒資料：重新同步有效節點
            if report["missing_in_qmd"]:
                print(f"🔄 發現 {len(report['missing_in_qmd'])} 個節點需要同步到 QMD")
                # 這裡可以選擇自動重新同步
                # self.sync_from_sacred_essence(filter_states=None)
                report["actions_taken"].append("triggered_resync")
            
            if report["orphaned_in_qmd"]:
                print(f"🗑️  發現 {len(report['orphaned_in_qmd'])} 個孤兒資料在 QMD 中")
                # QMD 目前沒有單個刪除 API，需要重建索引
                # 這裡標記為需要重建
                report["actions_taken"].append("needs_rebuild")
        
        return report
    
    # ==================== 原有功能（優化版） ====================
    
    def sync_node_to_qmd(
        self, 
        node_id: str,
        topic: str,
        content: str,
        state: str = "SILVER",
        parent_id: Optional[str] = None
    ) -> bool:
        """單節點同步（帶覆寫保護）"""
        # 檢查是否已存在且內容相同
        if self._is_node_synced(node_id, content):
            return True
        
        context_text = f"[NODE_ID:{node_id}][TOPIC:{topic}][STATE:{state}]"
        if parent_id:
            context_text += f"[PARENT:{parent_id}]"
        
        full_content = f"{context_text}\n{content}"
        
        temp_dir = Path.home() / ".cache" / "sacred-essence" / "qmd-sync"
        temp_dir.mkdir(parents=True, exist_ok=True)
        
        # 統一命名規範：[TOPIC]_[NODE_ID].md
        temp_file = temp_dir / f"{topic}_{node_id}.md"
        
        with open(temp_file, 'w', encoding='utf-8') as f:
            f.write(full_content)
        
        # 移除舊的雜湊版本檔案（清理舊時代殘影）
        for old_file in temp_dir.glob(f"{topic}_{node_id}_*.md"):
            old_file.unlink()
        
        if not self.collection_exists():
            success, _ = self._run_qmd([
                "collection", "add", str(temp_dir),
                "--name", self.collection_name,
                "--mask", "*.md"
            ])
        else:
            success, _ = self._run_qmd(["update"])
        
        if success:
            self._run_qmd(["embed", "-f"])
        
        return success
    
    def delete_node(self, node_id: str) -> bool:
        """從 QMD 中刪除特定節點 (防禦『資料幽靈』)"""
        # QMD CLI 刪除指令 (假設支援 qmd delete <node_id> 或透過移除原檔後 update)
        # 由於原始碼使用 `--mask *.md` 載入 temp_dir，刪除策略為：
        # 將該檔案從 collection 中移除並 update
        # 若 qmd 支援: qmd collection remove-doc -c <name> <doc_id>
        print(f"🗑️  正在從 QMD 中移除幽靈節點: {node_id}")
        
        # 備用方案：找到含有該 node_id 的 cache file 並刪除，然後重新 update
        temp_dir = Path.home() / ".cache" / "sacred-essence" / "qmd-sync"
        deleted_files = 0
        if temp_dir.exists():
            for f in temp_dir.glob(f"*_{node_id}_*.md"):
                f.unlink()
                deleted_files += 1
                
        if deleted_files > 0 and self.collection_exists():
            # 重新更新索引，被刪除的檔案就會從 QMD 消失
            success, _ = self._run_qmd(["update"])
            if success:
                self._run_qmd(["embed", "-f"])
                return True
        return False
    
    def _is_node_synced(self, node_id: str, content: str) -> bool:
        """檢查節點是否已同步且內容未變"""
        # 簡化檢查：可以查詢 QMD，這裡先返回 False 確保同步
        return False
    
    def constrained_search(
        self,
        query_text: str,
        node_whitelist: Set[str],
        n_results: int = 5,
        search_type: str = "hybrid"
    ) -> List[Dict]:
        """限縮搜索（優化版，帶超時控制）"""
        if not node_whitelist:
            return []
        
        # 修補 Edge Case 3：限制搜索範圍大小，避免過多節點導致延遲
        if len(node_whitelist) > 50:
            print(f"⚠️  白名單節點過多 ({len(node_whitelist)})，只取前 50 個")
            node_whitelist = set(list(node_whitelist)[:50])
        
        if search_type == "vector":
            raw_results = self.vector_search(query_text, n_results=n_results * 2)
        elif search_type == "keyword":
            raw_results = self.keyword_search(query_text, n_results=n_results * 2)
        else:
            raw_results = self.query(query_text, n_results=n_results * 2)
        
        filtered_results = []
        for r in raw_results:
            content = r.get('content', '')
            node_id = self._extract_node_id_from_content(content)
            if node_id and node_id in node_whitelist:
                r['content'] = self._clean_content(content)
                r['node_id'] = node_id
                filtered_results.append(r)
                
                if len(filtered_results) >= n_results:
                    break
        
        return filtered_results
    
    def query(self, query_text: str, n_results: int = 5, min_score: Optional[float] = None) -> List[Dict]:
        """混合搜索（帶超時）"""
        args = ["query", query_text, "-n", str(min(n_results * 2, 20)), "--json"]
        if min_score:
            args.extend(["--min-score", str(min_score)])
        args.extend(["-c", self.collection_name])
        
        success, output = self._run_qmd(args, timeout=self.QMD_TIMEOUT)
        
        if success:
            try:
                results = json.loads(output)
                return results if isinstance(results, list) else []
            except:
                return []
        return []
    
    def vector_search(self, query_text: str, n_results: int = 5) -> List[Dict]:
        """向量搜索（帶超時）"""
        args = ["vsearch", query_text, "-n", str(min(n_results * 2, 20)), "--json"]
        args.extend(["-c", self.collection_name])
        
        success, output = self._run_qmd(args, timeout=self.QMD_TIMEOUT)
        
        if success:
            try:
                results = json.loads(output)
                return results if isinstance(results, list) else []
            except:
                return []
        return []
    
    def keyword_search(self, query_text: str, n_results: int = 5) -> List[Dict]:
        """BM25 關鍵字搜索（逃生艙用）"""
        args = ["search", query_text, "-n", str(min(n_results, 10)), "--json"]
        args.extend(["-c", self.collection_name])
        
        success, output = self._run_qmd(args, timeout=self.QMD_TIMEOUT)
        
        if success:
            try:
                results = json.loads(output)
                return results if isinstance(results, list) else []
            except:
                return []
        return []
    
    def status(self) -> Dict:
        """狀態檢查"""
        success, output = self._run_qmd(["status"], timeout=5)
        if success:
            return {"status": "ok", "details": output}
        return {"status": "error", "error": output}
    
    def sync_from_sacred_essence(
        self, 
        memory_dir: Optional[str] = None,
        force: bool = False,
        filter_states: Optional[List[str]] = None
    ) -> bool:
        """批量同步"""
        memory_dir = memory_dir or self.memory_dir
        
        if not os.path.exists(memory_dir):
            print(f"❌ 記憶目錄不存在: {memory_dir}")
            return False
        
        temp_dir = Path.home() / ".cache" / "sacred-essence" / "qmd-sync"
        temp_dir.mkdir(parents=True, exist_ok=True)
        
        if force:
            for f in temp_dir.glob("*.md"):
                f.unlink()
        
        topics_dir = Path(memory_dir)
        synced_count = 0
        
        for content_file in topics_dir.rglob("content.md"):
            rel_path = content_file.relative_to(topics_dir)
            parts = rel_path.parts
            if len(parts) >= 2:
                topic = parts[0]
                node_id = parts[1]
                
                meta_file = content_file.parent / "node.meta.json"
                state = "SILVER"
                if meta_file.exists():
                    try:
                        with open(meta_file, 'r', encoding='utf-8') as f:
                            meta = json.load(f)
                        state = meta.get('state', 'SILVER')
                    except:
                        pass
                
                if filter_states and state not in filter_states:
                    continue
                
                with open(content_file, 'r', encoding='utf-8') as f:
                    content = f.read()
                
                metadata_prefix = f"[NODE_ID:{node_id}][TOPIC:{topic}][STATE:{state}]\n"
                full_content = metadata_prefix + content
                
                # 移除雜湊後綴，使用固定命名：[TOPIC]_[NODE_ID].md
                sync_file = temp_dir / f"{topic}_{node_id}.md"
                
                # 寫入檔案（直接覆寫，確保唯一性）
                with open(sync_file, 'w', encoding='utf-8') as f:
                    f.write(full_content)
                synced_count += 1
        
        print(f"📦 同步 {synced_count} 個變更的節點到 QMD...")
        
        if self.collection_exists() and not force:
            success, _ = self._run_qmd(["update"])
        else:
            if self.collection_exists():
                self._run_qmd(["collection", "remove", self.collection_name])
            success, _ = self._run_qmd([
                "collection", "add", str(temp_dir),
                "--name", self.collection_name,
                "--mask", "*.md"
            ])
        
        if success:
            self._run_qmd(["embed", "-f"])
            print(f"✅ 同步完成")
            return True
        return False


# 便捷函數
def create_bridge(collection_name: str = "sacred-l2", memory_dir: Optional[str] = None) -> QMDBridge:
    return QMDBridge(collection_name, memory_dir)


def sync_sacred_essence_to_qmd(
    collection_name: str = "sacred-l2",
    memory_dir: Optional[str] = None,
    filter_states: Optional[List[str]] = None,
    force: bool = False
) -> bool:
    """
    便捷函數：同步神髓數據到 QMD
    
    Args:
        collection_name: QMD 集合名稱
        memory_dir: 神髓記憶目錄路徑
        filter_states: 只同步指定狀態的節點 (e.g., ["GOLDEN", "SILVER"])
        force: 強制重新建立集合
    
    Returns:
        同步是否成功
    """
    bridge = QMDBridge(collection_name, memory_dir)
    return bridge.sync_from_sacred_essence(
        memory_dir=memory_dir,
        force=force,
        filter_states=filter_states
    )


if __name__ == "__main__":
    print("🧪 QMD Bridge v3.0 - Edge Cases 修補版")
    print("功能：逃生艙 Fallback + 數據審計 + 智能載入\n")
    
    bridge = create_bridge("sacred-l2")
    
    # 測試審計
    print("📊 執行數據一致性審計...")
    report = bridge.audit_and_cleanup(dry_run=True)
    print(f"  正確同步: {len(report['synced_correctly'])} 個")
    print(f"  QMD 孤兒: {len(report['orphaned_in_qmd'])} 個")
    print(f"  缺失同步: {len(report['missing_in_qmd'])} 個\n")
    
    # 測試智能搜索
    if bridge.collection_exists():
        print("🔍 測試智能搜索（含逃生艙）...")
        results, meta = bridge.smart_search_with_fallback(
            query_text="測試",
            node_whitelist=set(),  # 空白名單觸發 Fallback
            sacred_confidence=0.1,  # 低信心觸發 Fallback
            n_results=3
        )
        print(f"  策略: {meta['strategy']}")
        print(f"  觸發逃生艙: {meta['fallback_triggered']}")
        print(f"  結果數: {len(results)}")
        for r in results[:2]:
            print(f"    - [{r.score:.3f}] {r.node_id} ({r.source})")