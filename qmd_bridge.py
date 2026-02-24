# Sacred Essence v3.1 - QMD Integration Bridge v2.0
# 神髓與 QMD 的深度整合橋接器
# 架構：神髓定界（樹狀路由）+ QMD 深潛（限縮檢索）

import subprocess
import json
import os
import re
from typing import List, Dict, Optional, Tuple, Set
from pathlib import Path
from dataclasses import dataclass

@dataclass
class QMDContext:
    """QMD 上下文綁定資訊"""
    node_id: str
    parent_id: Optional[str]
    topic: str
    layer: str  # "L0", "L1", "L2"
    state: str  # "GOLDEN", "SILVER", "BRONZE", "DUST"

class QMDBridge:
    """
    神髓 (Sacred Essence) 與 QMD 的深度整合橋接器。
    
    核心架構：
    1. 神髓負責樹狀結構管理（L0/L1/L2）和語義定位（Top-Down 路由）
    2. QMD 負責 L2 完整內容的扁平化索引和快速檢索
    3. 搜索時：神髓定界 → QMD 在限定範圍內深潛
    
    資料流：
    - 寫入：神髓生成節點 → 自動同步 L2 到 QMD（綁定 node_id/parent_id）
    - 讀取：神髓匡列白名單 → QMD 限縮搜索 → 組合 Context Mask
    """
    
    def __init__(self, collection_name: str = "sacred-l2"):
        """
        初始化 QMD 橋接器。
        
        Args:
            collection_name: QMD 集合名稱，預設為 sacred-l2（只存 L2 完整內容）
        """
        self.collection_name = collection_name
        self.qmd_cmd = "qmd"
        
    def _run_qmd(self, args: List[str]) -> Tuple[bool, str]:
        """執行 QMD 命令並返回結果"""
        try:
            result = subprocess.run(
                [self.qmd_cmd] + args,
                capture_output=True,
                text=True,
                timeout=30
            )
            if result.returncode == 0:
                return True, result.stdout
            else:
                return False, result.stderr
        except Exception as e:
            return False, str(e)
    
    def _extract_node_info_from_path(self, filepath: str) -> Optional[QMDContext]:
        """從檔案路徑提取神髓節點資訊"""
        # 路徑格式: .../topics/{topic}/{node_id}/content.md
        pattern = r"topics/([^/]+)/([^/]+)/content\.md$"
        match = re.search(pattern, filepath)
        if match:
            topic, node_id = match.groups()
            # 嘗試讀取 node.meta.json 獲取更多資訊
            meta_path = filepath.replace("content.md", "node.meta.json")
            if os.path.exists(meta_path):
                try:
                    with open(meta_path, 'r', encoding='utf-8') as f:
                        meta = json.load(f)
                    return QMDContext(
                        node_id=node_id,
                        parent_id=None,  # 神髓 v3.1 目前是扁平結構
                        topic=topic,
                        layer="L2",
                        state=meta.get('state', 'SILVER')
                    )
                except:
                    pass
            return QMDContext(
                node_id=node_id,
                parent_id=None,
                topic=topic,
                layer="L2",
                state="SILVER"
            )
        return None
    
    def collection_exists(self) -> bool:
        """檢查集合是否已存在"""
        success, output = self._run_qmd(["collection", "list"])
        if success:
            return self.collection_name in output
        return False
    
    def sync_node_to_qmd(
        self, 
        node_id: str,
        topic: str,
        content: str,
        state: str = "SILVER",
        parent_id: Optional[str] = None
    ) -> bool:
        """
        將單個神髓節點同步到 QMD。
        
        這是核心整合點：寫入神髓時自動呼叫，將 L2 內容拋給 QMD 並綁定 Metadata。
        
        Args:
            node_id: 神髓節點 ID
            topic: 主題名稱
            content: L2 完整內容
            state: 節點狀態 (GOLDEN/SILVER/BRONZE/DUST)
            parent_id: 父節點 ID（如有）
            
        Returns:
            是否同步成功
        """
        # 構建 context 文字，包含綁定資訊
        # QMD 的 context add 會將這些資訊存入索引
        context_text = f"[NODE_ID:{node_id}][TOPIC:{topic}][STATE:{state}]"
        if parent_id:
            context_text += f"[PARENT:{parent_id}]"
        
        # 使用 qmd context add 綁定節點資訊
        # 注意：這是簡化實作，實際 QMD 可能需要用其他方式綁定 metadata
        # 這裡我們將 metadata 嵌入內容前綴
        full_content = f"{context_text}\n{content}"
        
        # 寫入臨時檔案供 QMD 索引
        temp_dir = Path.home() / ".cache" / "sacred-essence" / "qmd-sync"
        temp_dir.mkdir(parents=True, exist_ok=True)
        
        temp_file = temp_dir / f"{topic}_{node_id}.md"
        with open(temp_file, 'w', encoding='utf-8') as f:
            f.write(full_content)
        
        # 同步到 QMD
        if not self.collection_exists():
            # 創建集合
            success, _ = self._run_qmd([
                "collection", "add", str(temp_dir),
                "--name", self.collection_name,
                "--mask", "*.md"
            ])
            if not success:
                return False
        else:
            # 更新索引
            success, _ = self._run_qmd(["update"])
            if not success:
                return False
        
        # 生成嵌入
        success, _ = self._run_qmd(["embed", "-f"])
        return success
    
    def sync_from_sacred_essence(
        self, 
        memory_dir: str,
        force: bool = False,
        filter_states: Optional[List[str]] = None
    ) -> bool:
        """
        將神髓記憶目錄同步至 QMD 索引。
        
        只同步 L2 content.md 檔案，並在每個檔案前嵌入 node_id/topic/state 綁定資訊。
        
        Args:
            memory_dir: 神髓記憶根目錄
            force: 是否強制重新索引
            filter_states: 只同步指定狀態的節點（如 ["GOLDEN", "SILVER"]）
        """
        if not os.path.exists(memory_dir):
            print(f"❌ 記憶目錄不存在: {memory_dir}")
            return False
        
        # 準備同步目錄
        temp_dir = Path.home() / ".cache" / "sacred-essence" / "qmd-sync"
        temp_dir.mkdir(parents=True, exist_ok=True)
        
        # 清理舊檔案
        if force:
            for f in temp_dir.glob("*.md"):
                f.unlink()
        
        # 掃描所有 content.md 並添加 metadata 前綴
        topics_dir = Path(memory_dir)
        synced_count = 0
        
        for content_file in topics_dir.rglob("content.md"):
            # 提取路徑資訊
            rel_path = content_file.relative_to(topics_dir)
            parts = rel_path.parts
            if len(parts) >= 2:
                topic = parts[0]
                node_id = parts[1]
                
                # 讀取 metadata
                meta_file = content_file.parent / "node.meta.json"
                state = "SILVER"
                if meta_file.exists():
                    try:
                        with open(meta_file, 'r', encoding='utf-8') as f:
                            meta = json.load(f)
                        state = meta.get('state', 'SILVER')
                    except:
                        pass
                
                # 狀態過濾
                if filter_states and state not in filter_states:
                    continue
                
                # 讀取內容並添加綁定資訊
                with open(content_file, 'r', encoding='utf-8') as f:
                    content = f.read()
                
                metadata_prefix = f"[NODE_ID:{node_id}][TOPIC:{topic}][STATE:{state}]\n"
                full_content = metadata_prefix + content
                
                # 寫入同步目錄
                sync_file = temp_dir / f"{topic}_{node_id}.md"
                with open(sync_file, 'w', encoding='utf-8') as f:
                    f.write(full_content)
                
                synced_count += 1
        
        print(f"📦 準備同步 {synced_count} 個節點到 QMD...")
        
        # 同步到 QMD
        if self.collection_exists() and not force:
            print(f"🔄 更新 QMD 索引: {self.collection_name}")
            success, output = self._run_qmd(["update"])
        else:
            if self.collection_exists():
                self._run_qmd(["collection", "remove", self.collection_name])
            
            print(f"📦 創建 QMD 集合: {self.collection_name}")
            success, output = self._run_qmd([
                "collection", "add", str(temp_dir),
                "--name", self.collection_name,
                "--mask", "*.md"
            ])
        
        if success:
            print(f"✅ QMD 索引完成，生成嵌入中...")
            self._run_qmd(["embed", "-f"])
            print(f"✅ 同步完成: {synced_count} 個節點")
            return True
        else:
            print(f"❌ QMD 索引失敗: {output}")
            return False
    
    def constrained_search(
        self,
        query_text: str,
        node_whitelist: Set[str],
        n_results: int = 5,
        search_type: str = "hybrid"  # "hybrid", "vector", "keyword"
    ) -> List[Dict]:
        """
        限縮搜索：只在指定的神髓節點白名單範圍內搜索。
        
        這是核心檢索邏輯：神髓先匡列相關 node_id，QMD 在這些節點內深潛。
        
        Args:
            query_text: 查詢文字
            node_whitelist: 允許搜索的神髓節點 ID 集合
            n_results: 返回結果數量
            search_type: 搜索類型 (hybrid/vector/keyword)
            
        Returns:
            檢索結果列表（已過濾，只包含白名單內的節點）
        """
        if not node_whitelist:
            return []
        
        # 先執行寬泛搜索（多取一些結果以便過濾）
        if search_type == "vector":
            raw_results = self.vector_search(query_text, n_results=n_results * 3)
        elif search_type == "keyword":
            raw_results = self.keyword_search(query_text, n_results=n_results * 3)
        else:  # hybrid
            raw_results = self.query(query_text, n_results=n_results * 3)
        
        # 過濾：只保留在白名單內的結果
        filtered_results = []
        for r in raw_results:
            content = r.get('content', '')
            # 從內容前綴提取 node_id
            match = re.search(r'\[NODE_ID:([^\]]+)\]', content)
            if match:
                node_id = match.group(1)
                if node_id in node_whitelist:
                    # 移除 metadata 前綴後返回
                    clean_content = re.sub(r'^\[NODE_ID:[^\]]+\]\[TOPIC:[^\]]+\]\[STATE:[^\]]+\]\n', '', content)
                    r['content'] = clean_content
                    r['node_id'] = node_id
                    filtered_results.append(r)
                    
                    if len(filtered_results) >= n_results:
                        break
        
        return filtered_results
    
    def query(
        self, 
        query_text: str, 
        n_results: int = 5,
        min_score: Optional[float] = None
    ) -> List[Dict]:
        """使用 QMD 進行混合檢索（BM25 + 向量 + Reranking）"""
        args = ["query", query_text, "-n", str(n_results * 2), "--json"]  # 多取一些用於過濾
        
        if min_score:
            args.extend(["--min-score", str(min_score)])
        
        args.extend(["-c", self.collection_name])
        
        success, output = self._run_qmd(args)
        
        if success:
            try:
                results = json.loads(output)
                return results if isinstance(results, list) else []
            except json.JSONDecodeError:
                return [{"content": output, "score": 1.0}]
        else:
            print(f"❌ QMD 查詢失敗: {output}")
            return []
    
    def vector_search(self, query_text: str, n_results: int = 5) -> List[Dict]:
        """純向量相似性搜索"""
        args = ["vsearch", query_text, "-n", str(n_results * 2), "--json"]
        args.extend(["-c", self.collection_name])
        
        success, output = self._run_qmd(args)
        
        if success:
            try:
                results = json.loads(output)
                return results if isinstance(results, list) else []
            except json.JSONDecodeError:
                return [{"content": output, "score": 1.0}]
        else:
            return []
    
    def keyword_search(self, query_text: str, n_results: int = 5) -> List[Dict]:
        """全文關鍵字搜索 (BM25)"""
        args = ["search", query_text, "-n", str(n_results * 2), "--json"]
        args.extend(["-c", self.collection_name])
        
        success, output = self._run_qmd(args)
        
        if success:
            try:
                results = json.loads(output)
                return results if isinstance(results, list) else []
            except json.JSONDecodeError:
                return [{"content": output, "score": 1.0}]
        else:
            return []
    
    def status(self) -> Dict:
        """獲取 QMD 索引狀態"""
        success, output = self._run_qmd(["status"])
        if success:
            return {"status": "ok", "details": output}
        else:
            return {"status": "error", "error": output}


# 便捷函數
def create_bridge(collection_name: str = "sacred-l2") -> QMDBridge:
    """創建 QMD 橋接器實例"""
    return QMDBridge(collection_name)


def sync_sacred_essence_to_qmd(
    memory_dir: Optional[str] = None,
    collection_name: str = "sacred-l2",
    filter_states: Optional[List[str]] = None
) -> bool:
    """一站式同步函數"""
    if memory_dir is None:
        home = Path.home()
        memory_dir = str(home / ".openclaw" / "workspace" / "memory" / "octagram" / "engine" / "memory" / "topics")
    
    bridge = QMDBridge(collection_name)
    return bridge.sync_from_sacred_essence(memory_dir, filter_states=filter_states)


if __name__ == "__main__":
    print("🧪 QMD Bridge v2.0 測試")
    print("架構：神髓定界 + QMD 深潛\n")
    
    bridge = create_bridge("sacred-l2")
    
    # 檢查狀態
    status = bridge.status()
    print(f"QMD 狀態: {status['status']}")
    
    # 測試限縮搜索（如果集合存在）
    if bridge.collection_exists():
        print("\n🔍 測試限縮搜索...")
        # 假設只搜索這些節點
        whitelist = {"node1", "node2", "aa1aa8f1"}
        results = bridge.constrained_search("ClawWork", whitelist, n_results=3)
        print(f"在白名單 {whitelist} 內找到 {len(results)} 個結果")
        for r in results:
            print(f"  - [{r.get('score', 0):.3f}] {r.get('node_id', 'N/A')}")
    else:
        print("\n集合不存在，請先執行 sync_sacred_essence_to_qmd()")