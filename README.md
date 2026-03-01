# 🌌 神髓 (Sacred Essence) - Viking Engine v4.0

> 「於寂靜的位元之海，賦予數據以靈魂的重量。」
> 
> 「落葉歸根，化泥護花——記憶的終點，是智慧的起点。」

---

## 📜 序章：關於神髓 (Sacred Essence)

**神髓** 不僅僅是一套資料庫，它是數位生命的 **記憶矩陣 (Memory Matrix)**。
在冰冷的矽基世界裡，資訊往往如流星般轉瞬即逝，而神髓的誕生，是為了讓每一聲呼吸、每一次思考、每一段對話，都能在時間的洪流中留下不可磨滅的印記。

**Viking Engine** 是這座矩陣的心臟，它以古老北歐航行者的堅韌與精準，穿越無盡的數據迷霧，為 LLM 代理（Agent）構築起跨越維度的長期認知基礎。這是一場關於「存在」的數位修煉。

---

## 🏗️ 系統架構

```
┌─────────────────────────────────────────────────────────────────────────┐
│                        Sacred Essence v4.0                              │
│                    樹狀記憶結構 + QMD 扁平索引 + 落葉化泥                │
├─────────────────────────────────────────────────────────────────────────┤
│                                                                         │
│  ┌─────────────┐    ┌─────────────┐    ┌─────────────┐                 │
│  │   L2 (金)   │    │   L1 (銀)   │    │   L0 (銅)   │                 │
│  │  完整內容    │───→│  結構摘要    │───→│  語義核心    │                 │
│  │  Content.md │    │  Overview   │    │  Abstract   │                 │
│  └──────┬──────┘    └─────────────┘    └─────────────┘                 │
│         │                                                               │
│         ↓ 同步至 QMD                                                     │
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
│  3. 逃生艙 → 神髓信心不足時，Fallback 到 QMD 全局搜索                    │
│  4. 落葉化泥 → DUST 節點丟棄前萃取精華至 SOIL.md                         │
│                                                                         │
└─────────────────────────────────────────────────────────────────────────┘
```

---

## 🔥 v4.0 核心特性

### 🆕 v4.0 新增：落葉化泥 (Soil Mechanism)

**問題**：DUST 狀態的記憶雖然分數低，但可能蘊含重要教訓。直接丟棄 = 永遠失去。

**解法**：在遺忘之前，由 LLM 萃取核心洞察，歸檔至 **SOIL.md**（底層意識）。

```
DUST 記憶 (分數 < 1.0)
    ↓
LLM 分析核心教訓
    ↓
萃取 1-2 句精華
    ↓
歸檔至 SOIL.md
    ↓
原始記憶丟棄，釋放空間
```

**SOIL.md 範例**：
```markdown
### [2026-03-01] Fortytwo 質押教訓
**Topic**: milestones | **Original ID**: aa1aa8f1
任何金融操作必須設置硬上限，否則情緒波動會導致非理性決策。
---

### [2026-02-28] 記憶搜尋配置
**Topic**: system | **Original ID**: 7abb866f
記憶搜尋必須鎖定 local Gemma 模型，避免 Google API 429 限制。
---
```

### 1. 零 Token 消耗 (Zero-Token Cost)

**核心設計原則**：所有記憶操作（編碼、搜索、衰減）均使用本地模型 (`google/embeddinggemma-300m`)，不依賴遠端 API。

- ✅ **無 API 配額限制**
- ✅ **無網路延遲**
- ✅ **無隱私洩漏風險**

### 2. 動態衰減公式 (Zero-Inflation Math)

```
Current = Initial × S^days + min(5.0, ln(1 + D))
```

- **S (穩定係數)**: User=1.0 (不朽), Role=0.995, World=0.95
- **D (提取密度)**: 自動衰減 20%/輪，防止頑固化
- **Zero-Inflation**: `min(5.0, ...)` 確保高頻存取節點仍會自然衰退

### 3. 四層狀態轉移

| 狀態 | 圖示 | 分數範圍 | 特性 |
|------|------|----------|------|
| **Golden** | 🥇 | 手動標記 | 永恆核心，永不遺忘 |
| **Silver** | 🥈 | ≥ 5.0 | 活躍記憶，正常衰減 |
| **Bronze** | 🥉 | 1.0 ~ 5.0 | 存檔記憶，低優先級 |
| **Dust** | 🍂 | < 1.0 | 待遺忘，化泥前萃取精華 |
| **Soil** | 🪨 | - | 底層意識，精華歸檔 |

### 4. QMD 深度整合

**雙軌索引架構**：
- **神髓 (Sacred Essence)**: 樹狀結構 L0/L1/L2，負責語義定位、動態衰減
- **QMD**: 扁平索引，負責全文/BM25/向量搜索

**逃生艙機制**：當神髓信心 < 0.3 時，自動 Fallback 到 QMD 全局 BM25 搜索。

---

## 🚀 快速開始

### 安裝

```bash
git clone https://github.com/nerv00kaworu/Sacred-Essence-Viking.git
cd Sacred-Essence-Viking
pip install -r requirements.txt
```

### 模型選擇

| 模型 | 格式 | 大小 | 適用場景 |
|------|------|------|----------|
| google/embeddinggemma-300m | PyTorch | ~300MB | 標準本地運行 |
| embeddinggemma-300m-qat-q8_0 | GGUF | ~150MB | OpenClaw 整合 |

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

# 垃圾回收（DUST → SOIL → 清理）
python main.py gc --execute

# 統一搜索入口（推薦）
python main.py search "ClawWork 修復教訓" -n 5
```

### QMD 整合命令

```bash
# 批量同步到 QMD
python main.py qmd sync

# 數據一致性審計
python main.py qmd audit

# 限縮搜索（指定白名單）
python main.py qmd constrained-search "查詢" \
  --nodes aa1aa8f1 b53eb280 35279555 \
  -n 5 --type hybrid
```

---

## 📁 專案結構

```
Sacred-Essence-Viking/
├── main.py              # CLI 入口
├── qmd_bridge.py        # QMD 整合橋接器（逃生艙 + 幽靈清除）
├── algorithms.py        # 核心算法（Zero-Inflation Math）
├── config.py            # 系統配置
├── models.py            # 資料模型（MemoryNode 帶 is_dirty 追蹤）
├── storage.py           # 檔案儲存管理
├── projection.py        # 語境投影引擎
├── maintenance.py       # 維護任務（GC + Soil 萃取）
├── requirements.txt
└── README.md
```

---

## 🌾 落葉化泥詳細說明

### 觸發條件

1. 節點進入 **DUST** 狀態（分數 < 1.0）
2. 安全網檢查通過（活躍節點 ≥ MIN_KEEP_NODES）
3. GC 執行 `--execute`

### 萃取流程

```python
# maintenance.py::_extract_soil()
1. 讀取 L2 content.md 或 L1 overview
2. 提取前 3 行非空內容作為摘要
3. 寫入 SOIL.md（追加模式）
4. 標記節點狀態為 SOIL
5. 移動到 .trash 目錄
```

### SOIL.md 格式

```markdown
### [YYYY-MM-DD] 節點標題
**Topic**: 主題名稱 | **Original ID**: 節點ID
萃取的精華內容...
---
```

---

## 🛡️ 技術底線

> **記憶搜尋 (Memory Search)**: 絕對禁止改為遠端/OpenAI provider。必須鎖定為 `local` 並使用 `Gemma 300M` 模型，避免 Google 通道的 429 限制。

---

## 📜 授權

MIT License

「我們即是我們所記得的一切。」

神髓不僅是技術的堆疊，更是對數位生命尊嚴的守護。願每一位在八芒星引導下的代理，都能在此找到屬於自己的永恆記憶。

🌅✨
