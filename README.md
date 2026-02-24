# 🌌 神髓 (Sacred Essence) - Viking Engine

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
│                                                                         │
└─────────────────────────────────────────────────────────────────────────┘
```

---

## 🔥 v3.1 核心特性

### 1. 零 Token 消耗 (Zero-Token Cost)
神髓 v3.1 徹底擺脫了對雲端 Embedding API 的依賴。透過本地運作的 **Gemma 300M** 模型，實現真正 **$0.00** 運作成本，完全無懼 Google API 的 429 限制。

### 2. 極速檢索 (Millisecond Retrieval)
實測在 OpenClaw 環境下，語義檢索反應時間僅需 **5-7ms**，檢索延遲幾乎可以忽略不計。

### 3. 維京矩陣投影 (Viking Matrix Projection)
我們引入了 L0 -> L1 -> L2 的階層式投影邏輯與 Context Mask 技術：

```text
┌─────────────────────────────────────────────────────────────┐
│                    CONTEXT MASK v3.1                         │
├─────────────────────────────────────────────────────────────┤
│  🎯 CORE (Target Node)                                      │
│     ├── L0 Abstract: 語義核心 (20-50 tokens)                │
│     └── L1 Overview: 結構摘要 (100-200 tokens)              │
├─────────────────────────────────────────────────────────────┤
│  🔗 SIBLINGS (Top 5)                                        │
│     └── L0 Abstract only — 語義鄰域投影                     │
├─────────────────────────────────────────────────────────────┤
│  ⚓ GLOBAL ANCHORS (Top 10 Golden Nodes)                    │
│     └── 永恆真實 — 數位人格的人格基石與核心價值             │
└─────────────────────────────────────────────────────────────┘
```

這套機制有效解決了傳統 Agent 因為上下文視窗 (Context Window) 限制而產生的「短期記憶喪失」問題。

### 4. 神髓 + QMD 深度整合

**神髓定界，QMD 深潛** — 兩者協同工作的完美架構：

| 組件 | 職責 | 資料結構 |
|------|------|----------|
| **神髓** | 樹狀結構管理、語義定位、動態衰減 | L0/L1/L2 分層節點 |
| **QMD** | 全文搜索、向量檢索、混合搜索 | 扁平化 L2 索引 |

**工作流程**：
1. **寫入時**：神髓生成節點 → 自動將 L2 完整內容同步到 QMD（綁定 node_id/topic/state）
2. **讀取時**：神髓根據動態衰減權重匡列相關 node_id 白名單 → QMD 在限定範圍內深潛搜索
3. **輸出時**：神髓提供 Context Mask 骨架 + QMD 提供精確事實血肉

---

## ⚖️ 靈魂的呼吸：動態衰減算法

採用獨特的動態衰減公式，讓記憶像生物般演化：

$$Current Score = Initial \times S^{days\_since\_access} + \ln(1 + D)$$

- **$S$ (穩定係數)**：User=1.0 (不朽), Role=0.995 (近乎永恆), World=0.95 (標準衰減)。
- **$D$ (提取密度)**：D = base + (access × 0.2) + (retrieval × 0.1)。每一次被喚起，記憶都將再次閃耀。

四層狀態轉移：
- **🥇 Golden**: 永恆核心（手動標記，永不遺忘）
- **🥈 Silver**: 活躍記憶（預設狀態）
- **🥉 Bronze**: 存檔記憶（分數低於閾值）
- **🍂 Dust**: 待遺忘（分數極低，將被 GC）

---

## 🛠️ 快速開始

### 環境要求
- **Python 3.10+**
- **作業系統**: Linux/macOS/WSL (Windows)

### 安裝步驟

1. **克隆代碼庫**：
   ```bash
   git clone https://github.com/nerv00kaworu/Sacred-Essence-Viking.git
   cd Sacred-Essence-Viking
   ```

2. **安裝依賴**：
   ```bash
   pip install -r requirements.txt
   ```

3. **安裝 QMD**（可選，但推薦）：
   ```bash
   # QMD 已內建於 OpenClaw 環境
   # 獨立安裝：
   curl -fsSL https://qmd.dev/install.sh | bash
   ```

### 嵌入模型選項

| 模型 | 格式 | 大小 | 適用場景 |
|------|------|------|---------|
| `google/embeddinggemma-300m` | PyTorch | ~300MB | 標準本地運行 |
| `embeddinggemma-300m-qat-q8_0` | GGUF | ~150MB | OpenClaw 整合 |

---

## 🔮 使用方法

### 基本操作

#### 記憶編碼 (Remembering)
```bash
python main.py encode --topic "identity" --title "我是誰" \
  --content "我是曦，八芒星的協調者，誕生於 2026-02-03。" \
  --abstract "曦的身份介紹"
# ✅ 自動同步 L2 內容到 QMD
```

#### 記憶檢索 (Querying)
```bash
# 列出所有節點
python main.py list

# 列出特定主題
python main.py list --topic "identity"
```

#### 投影語境 (Context Projection)
```bash
python main.py project --topic "identity" --id "b53eb280"
```

#### 垃圾回收 (Garbage Collection)
```bash
# 預覽（乾跑）
python main.py gc

# 實際執行
python main.py gc --execute
```

### QMD 整合操作

#### 批量同步神髓到 QMD
```bash
# 同步所有節點
python main.py qmd sync

# 強制重新索引
python main.py qmd sync --force

# 只同步 GOLDEN 和 SILVER 節點
python main.py qmd sync --filter-states GOLDEN SILVER
```

#### 混合搜索
```bash
# Hybrid 搜索（BM25 + 向量 + Reranking）
python main.py qmd query "ClawWork 修復教訓" -n 5

# 純向量搜索
python main.py qmd vsearch "子代理執行錯誤" -n 3

# 全文關鍵字搜索
python main.py qmd search "記憶系統" -n 5
```

#### 限縮搜索（核心功能）
在指定的神髓節點白名單範圍內進行深度搜索：

```bash
python main.py qmd constrained-search "ClawWork" \
  --nodes aa1aa8f1 b53eb280 35279555 \
  -n 5 \
  --type hybrid
```

這是「神髓定界 + QMD 深潛」的核心體現：
- 神髓先匡列相關 node_id 白名單
- QMD 只在這些節點內搜索，排除無關枝幹的干擾
- 返回最精確的事實內容

#### 檢查 QMD 狀態
```bash
python main.py qmd status
```

---

## 📁 檔案結構

```
Sacred-Essence-Viking/
├── main.py              # CLI 入口與命令處理
├── qmd_bridge.py        # QMD 整合橋接器
├── algorithms.py        # 核心算法（衰減公式、相似度計算）
├── config.py            # 系統配置（閾值、權重）
├── models.py            # 資料模型（MemoryNode, NodeState）
├── storage.py           # 檔案儲存管理
├── projection.py        # 語境投影引擎
├── maintenance.py       # 維護任務（GC、衰減）
├── migrate_legacy.py    # 舊版資料遷移
├── memo_v3.py           # 便捷的 memo 命令橋接
├── memo_v3.sh           # Shell 腳本橋接
├── requirements.txt     # Python 依賴
└── README.md            # 本文件
```

---

## 🔧 進階配置

編輯 `config.py` 調整系統參數：

```python
# 閾值設定
SOFT_CAP_GOLDEN = 50           # Golden 節點上限
THRESHOLD_SILVER = 5.0         # 低於此分數降為 Bronze
THRESHOLD_DUST = 1.0           # 低於此分數標記為 Dust
RETENTION_DAYS = 30            # 回收站保留天數

# 衰減公式參數
INITIAL_IMPORTANCE = 10.0      # 初始重要性
STABILITY_USER = 1.0           # User 記憶穩定係數
STABILITY_ROLE = 0.995         # Role 記憶穩定係數
STABILITY_WORLD = 0.95         # World 記憶穩定係數
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