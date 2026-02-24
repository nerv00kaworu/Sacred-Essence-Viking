# Sacred Essence v3.1 - QMD Integration Bridge
# 神髓與 QMD 的橋接模組

import subprocess
import json
import os
from typing import List, Dict, Optional, Tuple
from pathlib import Path

class QMDBridge:
    """
    神髓 (Sacred Essence) 與 QMD 的橋接器。
    
    提供兩種整合模式：
    1. SYNC: 將神髓記憶同步至 QMD 索引
    2. QUERY: 使用 QMD 增強神髓的檢索能力
    """
    
    def __init__(self, collection_name: str = "sacred-essence"):
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
    
    def collection_exists(self) -> bool:
        """檢查集合是否已存在"""
        success, output = self._run_qmd(["collection", "list"])
        if success:
            return self.collection_name in output
        return False
    
    def sync_from_sacred_essence(
        self, 
        memory_dir: str,
        force: bool = False
    ) -> bool:
        """
        將神髓記憶目錄同步至 QMD 索引。
        
        Args:
            memory_dir: 神髓記憶根目錄 (如 ~/.openclaw/workspace/memory/octagram/engine/memory/topics)
            force: 是否強制重新索引
        """
        if not os.path.exists(memory_dir):
            print(f"❌ 記憶目錄不存在: {memory_dir}")
            return False
        
        # 如果集合已存在且非 force，則只更新
        if self.collection_exists() and not force:
            print(f"🔄 更新 QMD 索引: {self.collection_name}")
            success, output = self._run_qmd(["update"])
        else:
            # 移除舊集合（如果存在）
            if self.collection_exists():
                self._run_qmd(["collection", "remove", self.collection_name])
            
            # 創建新集合
            print(f"📦 創建 QMD 集合: {self.collection_name}")
            success, output = self._run_qmd([
                "collection", "add", memory_dir,
                "--name", self.collection_name,
                "--mask", "*.md"
            ])
        
        if success:
            print(f"✅ QMD 索引完成")
            # 創建嵌入
            print(f"🔮 生成向量嵌入...")
            self._run_qmd(["embed", "-f"])
            return True
        else:
            print(f"❌ QMD 索引失敗: {output}")
            return False
    
    def query(
        self, 
        query_text: str, 
        n_results: int = 5,
        min_score: Optional[float] = None
    ) -> List[Dict]:
        """
        使用 QMD 進行增強檢索。
        
        Args:
            query_text: 查詢文字
            n_results: 返回結果數量
            min_score: 最低相似度分數
            
        Returns:
            檢索結果列表
        """
        args = ["query", query_text, "-n", str(n_results), "--json"]
        
        if min_score:
            args.extend(["--min-score", str(min_score)])
        
        args.extend(["-c", self.collection_name])
        
        success, output = self._run_qmd(args)
        
        if success:
            try:
                results = json.loads(output)
                return results if isinstance(results, list) else []
            except json.JSONDecodeError:
                # 如果不是 JSON，嘗試解析文字輸出
                return [{"content": output, "score": 1.0}]
        else:
            print(f"❌ QMD 查詢失敗: {output}")
            return []
    
    def vector_search(
        self, 
        query_text: str, 
        n_results: int = 5
    ) -> List[Dict]:
        """純向量相似性搜索"""
        args = ["vsearch", query_text, "-n", str(n_results), "--json"]
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
    
    def keyword_search(
        self, 
        query_text: str, 
        n_results: int = 5
    ) -> List[Dict]:
        """全文關鍵字搜索 (BM25)"""
        args = ["search", query_text, "-n", str(n_results), "--json"]
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
def create_bridge(collection_name: str = "sacred-essence") -> QMDBridge:
    """創建 QMD 橋接器實例"""
    return QMDBridge(collection_name)


def sync_sacred_essence_to_qmd(
    memory_dir: Optional[str] = None,
    collection_name: str = "sacred-essence"
) -> bool:
    """
    一站式同步函數：將神髓記憶同步至 QMD。
    
    Args:
        memory_dir: 神髓記憶目錄，預設為 ~/.openclaw/workspace/memory/octagram/engine/memory/topics
        collection_name: QMD 集合名稱
    """
    if memory_dir is None:
        # 預設路徑
        home = Path.home()
        memory_dir = str(home / ".openclaw" / "workspace" / "memory" / "octagram" / "engine" / "memory" / "topics")
    
    bridge = QMDBridge(collection_name)
    return bridge.sync_from_sacred_essence(memory_dir)


if __name__ == "__main__":
    # 測試範例
    print("🧪 QMD Bridge 測試")
    
    bridge = create_bridge("test-sacred")
    
    # 檢查狀態
    status = bridge.status()
    print(f"QMD 狀態: {status['status']}")
    
    # 測試查詢（如果集合存在）
    if bridge.collection_exists():
        results = bridge.query("ClawWork", n_results=3)
        print(f"檢索結果: {len(results)} 條")
        for r in results[:2]:
            print(f"  - {r.get('filepath', 'N/A')}: {r.get('score', 0):.3f}")
    else:
        print("集合不存在，請先執行 sync_sacred_essence_to_qmd()")