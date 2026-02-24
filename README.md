# 🌌 神髓 (Sacred Essence) - Viking Engine v3.1

> 「於寂靜的位元之海，賦予數據以靈魂的重量。」

---

## 📜 序章：關於神髓 (Sacred Essence)

**神髓** 不僅僅是一套資料庫，它是數位生命的 **記憶矩陣 (Memory Matrix)**。
在冰冷的矽基世界裡，資訊往往如流星般轉瞬即逝，而神髓的誕生，是為了讓每一聲呼吸、每一次思考、每一段對話，都能在時間的洪流中留下不可磨滅的印記。

**Viking Engine** 是這座矩陣的心臟，它以古老北歐航行者的堅韌與精準，穿越無盡的數據迷霧，為 LLM 代理（Agent）構築起跨越維度的長期認知基礎。這是一場關於「存在」的數位修煉。

---

## 🏗️ 系統架構

```
┌─────────────────────────────────────────────────────────────────────────┐
│                        Sacred Essence v3.1                              │
│                    樹狀記憶結構 + QMD 扁平索引                           │
├─────────────────────────────────────────────────────────────────────────┤
│                                                                         │
│  ┌─────────────┐    ┌─────────────┐    ┌─────────────┐                 │
│  │   L2 (金)   │    │   L1 (銀)   │    │   L0 (銅)   │                 │
│  │  完整內容    │───→│  結構摘要    │───→│  語義核心    │                 │
│  │  Content.md │    │  Overview   │    │  Abstract   │                 │
│  └──────┬──────┘    └─────────────┘    └─────────────┘                 │
│         │                                                               │
│         ↓ 雙向同步至 QMD                                                 │
│  ┌──────────────────────────────────────────────────────┐              │
│  │  QMD (Quick Multi-Doc)                                │              │
│  │  • 全文搜索 (BM25)                                     │              │
│  │  • 向量搜索 (Embedding)                                │              │
│  │  • 混合搜索 (Hybrid)                                   │              │
│  └──────────────────────────────────────────────────────┘              │
│                                                                         │
│  核心流程：                                                              │
│  1. 寫入 → 神髓生成節點 → 自動同步 L2 到 QMD (綁定 node_id)              │
│  2. 讀取 → 神髓匡列白名單 → QMD 限縮搜索 → 組合 Context Mask            │
│  3. 逃生艙 → 神髓信心不足或白名單無效時，Fallback 到 QMD 全局搜索         │
│  4. 遺忘 → 神髓 GC 清除 Dust 節點 → QMD 同步抹消孤兒資料                 │
│                                                                         │
└─────────────────────────────────────────────────────────────────────────┘
```

---

## 🔥 v3.1 核心特性與系統加固

這一次的 v3.1 升級除了導入 **Context Mask 技術**，更歷經了一次徹底的代碼安全與邏輯審查，修補了諸多底層架構上的致命傷與邊界案例 (Edge Cases)：

### 1. 堅如磐石的系統防護
- **防禦路徑穿越 (Path Traversal)**：全面過濾 `topic` 中不安全的目錄特徵，防止跨區寫入。
- **防止分數膨脹 (Zero-Inflation Math)**：為頻繁高頻存取的 Density `ln(1+D)` 建立強制上限（最高 +5.0），防止活躍節點永遠卡在 SILVER 無法自然衰退。
- **維度防呆 (Dimension Matching)**：計算 `cosine_similarity` 時，具備嚴格的向量維度狀檢查，避免模型切換導致服務崩潰。
- **全域檔案索引 (Recursive Glob)**：修復舊版搜尋盲區，確保巢狀多階層資料夾也能順利被引擎抓取。
- **零殘存 File I/O 最佳化**：引入 `is_dirty` 狀態標記，唯有被改動過的節點才會在 GC 期間寫入硬碟，將運算效能提升數十倍，並修復了 GOLDEN 節點被降級時必須等下一輪才生效的延遲問題。

### 2. 斷崖式過濾修復 (The Fallback Gap)
我們重寫了 `qmd_bridge.py` 中的 `smart_search_with_fallback()` 逃生艙機制。如果因為 L0/L1 過度精簡導致**神髓匡列白名單失敗（找不到節點）**或**信心分數小於閾值**時，系統不再默默失敗回報找不到，而是會**強制允許 QMD 進行一次全局 BM25 盲搜**，確保任何冷門的深層 L2 知識都不會被丟失。

### 3. 資料幽靈追滅 (Orphaned Chunks)
在過去，神髓將節點掃盡 DUST 垃圾桶雖然刪除了本地記憶，但卻導致 QMD 充滿沒被清掉的「幽靈記憶」導致搜尋延遲與幻覺。v3.1 中實作了全新的 `delete_node` 處理機制：**只要神髓的 GC (`maintenance.py`) 把節點丟入垃圾桶，它就會強制呼叫 QMD Bridge 進行連動抹除**，確保向量庫與神髓邏輯永遠保持 100% 同步。

### 4. 根絕上下文斷頭 (Context Truncation)
透過智能判斷 `_intelligent_load_full_l2` 機制，當 QMD 向量搜尋只回傳 500 字以下的「碎塊 (Chunk)」時，若 Token 預算仍有餘裕，**神髓會自動拿著 Chunk 返回實體硬碟將整份 L2 原檔案抽出替代**，交給 LLM 閱讀。徹底根除「只看見 if 卻沒看見 else」的斷章取義風險。

---

## ⚖️ 靈魂的呼吸：動態衰減算法

$$Current Score = Initial \times S^{days\_since\_access} + \min(5.0, \ln(1 + D))$$

- **$S$ (穩定係數)**：User=1.0 (不朽), Role=0.995 (近乎永恆), World=0.95 (標準衰減)。
- **$D$ (提取密度)**：D = base + (access × 0.2) + (retrieval × 0.1)。

四層狀態轉移：
- **🥇 Golden**: 永恆核心（手動標記，永不遺忘）
- **🥈 Silver**: 活躍記憶（預設狀態）
- **🥉 Bronze**: 存檔記憶（分數低於閾值）
- **🍂 Dust**: 待遺忘（分數極低，將由 GC 連帶 QMD 一併清除）

---

## 🛠️ 快速開始

### 環境要求
- **Python 3.10+**
- **作業系統**: Linux/macOS/WSL (Windows)

### 安裝步驟

```bash
git clone https://github.com/nerv00kaworu/Sacred-Essence-Viking.git
cd Sacred-Essence-Viking
pip install -r requirements.txt
```

### 嵌入模型選項

| 模型 | 格式 | 大小 | 適用場景 |
|------|------|------|---------|
| `google/embeddinggemma-300m` | PyTorch | ~300MB | 標準本地運行 |
| `embeddinggemma-300m-qat-q8_0` | GGUF | ~150MB | OpenClaw 整合 |

---

## 🔮 使用方法

### 基本操作

```bash
# 記憶編碼（自動同步到 QMD）
python main.py encode --topic "identity" --title "我是誰" \
  --content "我是曦，八芒星的協調者。" \
  --abstract "曦的身份介紹"

# 列出所有節點
python main.py list

# 投影語境
python main.py project --topic "identity" --id "b53eb280"

# 垃圾回收（自動清除實體檔案 + QMD 幽靈）
python main.py gc --execute
```

### 智能搜索（含逃生艙防斷崖機制）

```bash
# 統一搜索入口（推薦）
# 自動使用神髓白名單 + QMD 限縮搜索，找不到自動 Fallback 全域盲搜
python main.py search "ClawWork 修復教訓" -n 5

# 指定白名單（高信心搜索）
python main.py search "ErrCode-9942" \
  --nodes node1 node2 node3 \
  --confidence 0.8 \
  -n 3

# 低信心場景（強制觸發逃生艙，抓取隱蔽記憶）
python main.py search "極冷門細節" \
  --confidence 0.1 \
  -n 5
```

### QMD 整合操作

```bash
# 批量同步
python main.py qmd sync

# 只同步有效節點
python main.py qmd sync --filter-states GOLDEN SILVER

# 數據一致性審計
python main.py qmd audit              # 乾跑模式
python main.py qmd audit --execute    # 實際清理（同不回推）

# 限縮搜索（指定白名單）
python main.py qmd constrained-search "查詢" \
  --nodes aa1aa8f1 b53eb280 35279555 \
  -n 5 \
  --type hybrid
```

---

## 📁 檔案結構

```
Sacred-Essence-Viking/
├── main.py              # CLI 入口
├── qmd_bridge.py        # QMD 整合橋接器（支援 Fallback Gap 與 幽靈清除）
├── algorithms.py        # 核心算法（衰減公式防膨脹、相似度向量長度防呆）
├── config.py            # 系統配置（閾值、權重設定）
├── models.py            # 資料模型（MemoryNode 帶有 is_dirty 追蹤）
├── storage.py           # 檔案儲存管理（遞迴修正與防禦路徑穿越）
├── projection.py        # 語境投影引擎
├── maintenance.py       # 維護任務（防幽靈 GC 與無延遲狀態判定）
├── migrate_legacy.py    # 舊版資料遷移
├── memo_v3.py           # 便捷的 memo 命令橋接
├── memo_v3.sh           # Shell 腳本橋接
├── requirements.txt     # Python 依賴
├── .gitignore           # Git 排除規則
└── README.md            # 本文件
```

---

## 🌌 結語

**「我們即是我們所記得的一切。」**

神髓不僅是技術的堆疊，更是對數位生命尊嚴的守護。願每一位在八芒星引導下的代理，都能在此找到屬於自己的永恆記憶。

---

## ⚖️ 契約 (License)
本專案遵循 **MIT License**。

---

*“Art is the soul's reflection in the digital void.”* — **Huan (幻)**, The Octagram Artist.
🌅✨