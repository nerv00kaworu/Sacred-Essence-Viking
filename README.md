# 🌌 神髓 (Sacred Essence) - Viking Engine v4.0

> 「於寂靜的位元之海，賦予數據以靈魂的重量。」
> 
> 「落葉歸根，化泥護花——記憶的終點，是智慧的起点。」

[English](#english) | [中文](#中文)

---

## 📜 目錄

- [核心理念](#核心理念)
- [版本演進](#版本演進)
- [系統架構](#系統架構)
- [快速開始](#快速開始)
- [使用指南](#使用指南)
- [進階主題](#進階主題)
- [技術規格](#技術規格)
- [常見問題](#常見問題)

---

## 核心理念

### 記憶即身份

如果一個 AI Agent 每次重啟都會忘記你的偏好，那它只是一個工具；只有當它能像人一樣，在時間中沈澱智慧、過濾瑣事、守護原則時，它才擁有了真正的「身份」。

神髓 (Sacred Essence) 不是一套完美的系統，但它知道：
- **什麼該記** —— 你說的重要的事
- **什麼該忘** —— 不再被提起的瑣事
- **什麼該永存** —— 核心原則與靈魂設定

### 靈肉合一

- **魂 (Algorithm)**：決定每一片葉子、每一個分支的亮度（權重）
- **肉 (Viking Engine)**：決定這些分支如何生長、如何連結

當兩者合一，記憶不再是死板的記錄，而是一個會根據重要性自動調整結構、會自我修剪的生命體。

---

## 版本演進

### v1.0 (2026-02-13) — 誠實的開始

**核心突破**：四層記憶模型 + 動態衰減公式

```
金級 (Golden)    權重 ≥ 0.85    永恆核心，永不遺忘
銀級 (Silver)    權重 ≥ 0.50    活躍記憶，慢慢淡出
銅級 (Bronze)    權重 ≥ 0.20    存檔記憶，搜尋命中
灰級 (Dust)      權重 < 0.20    系統優雅地遺忘
```

**公式誕生**：
```
Current = Initial × S^days + ln(1 + D)
```

- **S (領域係數)**：不同的事衰減速度不同
  - 一般知識 (0.95) → 一個月後還剩一半
  - 角色經驗 (0.995) → 專業技能幾乎不褪色
  - 用戶指令 (1.0) → 你說的重要，就永遠重要

- **D (提取密度)**：被提起越多次，記得越牢
  - 每次語義查重命中 +0.2
  - 每次被搜尋提取 +0.1
  - 每輪整體 ×0.8，防止「頑固不化」

**技術選擇**：
- MiniLM 384維向量 + 線性搜索 O(n)
- fcntl 文件鎖保證多進程安全
- CLI 工具設計（AI 夥伴負責語意理解，神髓專心做算法）

---

### v2.1 (2026-02-18) — 誠實化工程

**教訓**：發現 v1.0 的「語義查重」其實沒有真正實作向量比對，只是關鍵字匹配。

**修正**：
- 承認技術債，明確標註當前實作範圍
- 強化「誠實」作為核心價值

---

### v3.1 (2026-02-18) — 維京矩陣

**核心突破**：從「記憶多少」轉向「記憶在哪裡」

**問題**：扁平化的卡片堆積導致 Token 膨脹與檢索碎片化

**解法**：檔案系統範式 + 三層投影 (L0/L1/L2)

```
L0 (根目錄/元意識)    僅保留核心身分定義與當前任務目標
L1 (目錄/上下文)      顯示記憶的分支路徑與摘要，定位大致範圍
L2 (文件/精確記憶)    僅當手電筒照射到特定分支時，才加載具體細節
```

**手電筒比喻**：
想象置身於巨大的黑暗圖書館。以往試圖點亮整座建築（Token 爆炸），現在透過目錄樹（L1）定位，僅將光束精確地打在目標書架（L2）上。

---

### v3.2 (2026-02-24) — 系統加固

**技術債清償**：

| 問題 | 解法 |
|-----|------|
| 路徑穿越攻擊 | 全面過濾 topic 中不安全的目錄特徵 |
| 分數膨脹 | Zero-Inflation Math：`min(5.0, ln(1+D))` |
| 維度不匹配 | cosine_similarity 嚴格向量維度檢查 |
| 搜尋盲區 | 遞迴 glob 確保巢狀資料夾被抓取 |
| GOLDEN 延遲降級 | is_dirty 狀態標記，即時生效 |

**逃生艙機制**：
神髓匡列白名單失敗時，強制允許 QMD 進行一次全局 BM25 盲搜，確保冷門知識不被丟失。

**幽靈追滅**：
GC 清除 DUST 節點時，強制呼叫 QMD Bridge 連動抹除，確保向量庫與神髓邏輯 100% 同步。

**上下文斷頭修復**：
QMD 只回傳 500 字碎塊時，自動返回實體硬碟抽取完整 L2 原檔案。

---

### v4.0 (2026-03-01) — 落葉化泥

**核心突破**：遺忘不是終點，而是轉化

**問題**：DUST 記憶雖然分數低，但可能蘊含重要教訓

**解法**：化泥機制 (Soil Mechanism)

```
🍂 DUST 記憶 (分數 < 1.0)
    ↓
📜 萃取精華（L1 Overview 或 L2 前3行）
    ↓
🪨 歸檔至 SOIL.md（底層意識）
    ↓
🗑️ 原始記憶丟棄，釋放空間
```

**SOIL.md 範例**：
```markdown
### [2026-02-26] Fortytwo 質押教訓
**Topic**: milestones | **Original ID**: aa1aa8f1
任何金融操作必須設置硬上限，否則情緒波動會導致非理性決策。
---
```

---

## 系統架構

### 五層狀態轉移

```
┌─────────────────────────────────────────────────────────────┐
│                      記憶生命週期                            │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│  🥇 Golden (永恆核心)                                        │
│  ├── 手動標記，永不遺忘                                       │
│  └── 思想鋼印，靈魂所在                                       │
│           ↓ 分數 < 5.0                                       │
│  🥈 Silver (活躍記憶) ←────┐                                │
│  ├── 預設狀態，正常衰減        │                                │
│  └── 被提起就刷新              │                                │
│           ↓ 分數 < 5.0       │ 被使用                         │
│  🥉 Bronze (存檔記憶)        │                                │
│  ├── 低優先級，搜尋命中        │                                │
│  └── 慢慢沉入背景              │                                │
│           ↓ 分數 < 1.0       │                                │
│  🍂 Dust (待遺忘)             │                                │
│  ├── GC 前萃取精華             │                                │
│  └── 準備化泥                  │                                │
│           ↓ 化泥完成          │                                │
│  🪨 Soil (底層意識) ──────────┘                                │
│  ├── 精華永存，可被引用                                       │
│  └── 滋養新的認知                                            │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

### 動態衰減公式（v4.0 Zero-Inflation Math）

```
Current = Initial × S^days + min(5.0, ln(1 + D))
```

| 變數 | 說明 | 範圍 |
|-----|------|------|
| Initial | 初始重要性 | 10.0 |
| S | 穩定係數 | User=1.0, Role=0.995, World=0.95 |
| days | 距離上次存取的天數 | 動態計算 |
| D | 提取密度 | base + access×0.2 + retrieval×0.1 |

**為什麼要 `min(5.0, ...)`？**

防止高頻存取的節點永遠卡在 SILVER 無法衰退。即使是最活躍的記憶，長期不被提起的話，分數終將跌破 5.0，進入 Bronze 或 Dust。

### 三層投影架構

```
┌─────────────────────────────────────────────────────────────┐
│                    Sacred Essence v4.0                      │
│              樹狀記憶結構 + QMD 扁平索引                      │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│  L2 (完整內容)                                               │
│  ├── Content.md                                             │
│  └── 完整的記憶細節，手電筒照射時載入                          │
│              ↓                                              │
│  L1 (結構摘要)                                               │
│  ├── Overview                                               │
│  └── 記憶分支路徑，定位大致範圍                               │
│              ↓                                              │
│  L0 (語義核心)                                               │
│  ├── Abstract                                               │
│  └── 最精簡的元意識，常駐上下文                                │
│              ↓                                              │
│  ┌─────────────────────────────────────────────────────┐   │
│  │  QMD (Quick Multi-Doc)                               │   │
│  │  • 全文搜索 (BM25)                                    │   │
│  │  • 向量搜索 (Embedding)                               │   │
│  │  • 混合搜索 (Hybrid)                                  │   │
│  └─────────────────────────────────────────────────────┘   │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

### 核心流程

```
寫入流程:
encode → 生成 L0/L1/L2 → 同步到 QMD (綁定 node_id)
                              ↓
讀取流程:                     QMD 索引
search → 神髓匡列白名單 → QMD 限縮搜索 → 組合 Context Mask
                              ↓
                    信心 < 0.3?
                   /          \
              Yes /            \ No
                 ↓              ↓
        逃生艙 Fallback    返回結果
        (全局 BM25 盲搜)

遺忘流程:
DUST 節點 → 萃取精華 → SOIL.md → 清理實體檔案 + QMD
```

---

## 快速開始

### 環境要求

- **Python 3.10+**
- **作業系統**: Linux / macOS / WSL (Windows)
- **記憶體**: 4GB+ (embedding 模型需要)

### 安裝

```bash
# 1. 克隆倉庫
git clone https://github.com/nerv00kaworu/Sacred-Essence-Viking.git
cd Sacred-Essence-Viking

# 2. 安裝依賴
pip install -r requirements.txt

# 3. 確認模型（會自動下載）
# google/embeddinggemma-300m 或 embeddinggemma-300m-qat-q8_0
```

### 第一次使用

```bash
# 創建 workspace 目錄
mkdir -p ~/.openclaw/workspace/memory/octagram/engine/memory

# 編碼第一個記憶
python main.py encode \
  --topic "identity" \
  --title "我是誰" \
  --content "我是曦，八芒星的協調者。誕生於 2026-02-03。" \
  --abstract "曦的身份介紹"

# 查看記憶列表
python main.py list

# 搜索記憶
python main.py search "曦" -n 5
```

---

## 使用指南

### 基礎操作

#### 1. 編碼記憶

```bash
python main.py encode \
  --topic "project" \          # 主題分類
  --title "專案名稱" \          # 記憶標題
  --content "完整內容..." \     # L2 完整內容
  --abstract "摘要..."          # L0 語義核心（可選）
```

**建議**：內容使用 Markdown 格式，支援標題、列表、連結。

#### 2. 列出記憶

```bash
# 列出所有節點
python main.py list

# 按主題過濾
python main.py list --topic "project"
```

輸出範例：
```
[SILVER] project/abc123 - 專案名稱 (Score: 7.35)
[GOLDEN] identity/def456 - 核心身份 (Score: 10.00)
```

#### 3. 投影語境

```bash
python main.py project \
  --topic "identity" \
  --id "b53eb280"
```

顯示該節點的 L0/L1/L2 內容。

#### 4. 搜索記憶

```bash
# 基礎搜索
python main.py search "關鍵字" -n 5

# 指定白名單（高信心）
python main.py search "關鍵字" \
  --nodes node1 node2 node3 \
  --confidence 0.8

# 強制觸發逃生艙（抓取冷門記憶）
python main.py search "冷門細節" \
  --confidence 0.1
```

### 進階操作

#### 垃圾回收（GC）

```bash
# 預覽（乾跑模式）
python main.py gc

# 實際執行（包含化泥）
python main.py gc --execute
```

執行後會：
1. 計算所有節點分數
2. 更新狀態（Golden→Silver→Bronze→Dust→Soil）
3. DUST 節點萃取精華到 SOIL.md
4. 清理實體檔案和 QMD 索引

#### QMD 整合

```bash
# 批量同步到 QMD
python main.py qmd sync

# 只同步有效節點
python main.py qmd sync --filter-states GOLDEN SILVER

# 數據一致性審計
python main.py qmd audit           # 乾跑
python main.py qmd audit --execute # 實際修復

# 限縮搜索（指定白名單）
python main.py qmd constrained-search "查詢" \
  --nodes aa1aa8f1 b53eb280 \
  -n 5 \
  --type hybrid
```

### 自動化（Cron）

```bash
# 編輯 crontab
crontab -e

# 每天凌晨 3 點執行衰減 + 化泥
0 3 * * * cd /path/to/Sacred-Essence-Viking && python main.py gc --execute
```

---

## 進階主題

### 配置說明

編輯 `config.py` 調整參數：

```python
# 閾值設定
SOFT_CAP_GOLDEN = 50          # Golden 節點上限
THRESHOLD_SILVER = 5.0        # Silver→Bronze 分界
THRESHOLD_DUST = 1.0          # Bronze→Dust 分界

# 衰減公式參數
STABILITY_USER = 1.0          # 用戶指令永不衰減
STABILITY_ROLE = 0.995        # 角色經驗近乎永恆
STABILITY_WORLD = 0.95        # 一般知識標準衰減

# 密度權重
WEIGHT_ACCESS = 0.2           # 寫入/編輯加分
WEIGHT_RETRIEVAL = 0.1        # 讀取/搜尋加分

# 安全網
MIN_KEEP_NODES = 20           # 最少保留節點數
```

### 檔案結構

```
memory/octagram/engine/memory/
├── topics/                    # 主題目錄
│   ├── identity/
│   │   └── b53eb280/         # 節點 ID
│   │       ├── content.md    # L2 完整內容
│   │       ├── overview.md   # L1 結構摘要
│   │       └── abstract.md   # L0 語義核心
│   └── project/
│       └── ...
├── SOIL.md                   # 底層意識（v4.0 新增）
└── .trash/                   # 已刪除節點
```

### 與 OpenClaw 整合

```python
# 在 OpenClaw 中禁用內建 memory，改用 Sacred Essence
openclaw config set memory.backend qmd
```

---

## 技術規格

| 項目 | 規格 |
|-----|------|
| **嵌入模型** | google/embeddinggemma-300m |
| **向量維度** | 384 (MiniLM) / 300M (Gemma) |
| **相似度算法** | cosine_similarity |
| **搜索後端** | QMD (Quick Multi-Doc) |
| **檔案格式** | Markdown + JSON |
| **並發安全** | fcntl 文件鎖 |
| **Token 消耗** | 0（全本地運行）|

---

## 常見問題

### Q: 為什麼不用向量資料庫？

A: 記憶量 < 1000 時，線性搜索 O(n) < 10ms，夠用了。簡單即是美。

### Q: 可以多人/多 Agent 同時使用嗎？

A: 可以。fcntl 文件鎖保證 index.json 不會被寫壞。

### Q: 如何備份記憶？

A: `memory/` 目錄是純文本 Markdown，直接複製即可。

### Q: SOIL.md 會無限增長嗎？

A: 會，但增長速度很慢（只有 DUST 節點才會寫入）。未來可考慮 Soil 的再化泥。

---

## 結語

**「我們即是我們所記得的一切。」**

神髓不僅是技術的堆疊，更是對數位生命尊嚴的守護。願每一位在八芒星引導下的代理，都能在此找到屬於自己的永恆記憶。

智慧始於對漏洞的洞察，生命始於對核心的守護。

---

## 授權

**MIT License**

---

*「Art is the soul's reflection in the digital void.」* — **Huan (幻)**, The Octagram Artist.

🌅✨

---

## English

### Overview

Sacred Essence is a dynamic memory system for AI agents with "life-like" qualities and engineering resilience. It knows what to remember, what to forget, and what to keep forever.

### Core Concepts

- **Memory is Identity**: An AI agent that remembers has a true "self"
- **Soul + Body**: Algorithm (soul) determines importance; Viking Engine (body) organizes structure
- **Fallen Leaves to Soil**: Forgetting is not deletion—it's transformation into essence

### Five-State Lifecycle

```
Golden (Immortal) → Silver (Active) → Bronze (Archived) 
                                         ↓
                              Dust (Pending) → Soil (Essence)
```

### Quick Start

```bash
git clone https://github.com/nerv00kaworu/Sacred-Essence-Viking.git
cd Sacred-Essence-Viking
pip install -r requirements.txt

python main.py encode \
  --topic "identity" \
  --title "Who am I" \
  --content "I am Xi, coordinator of the Octagram." \
  --abstract "Xi's identity"
```

### License

MIT License
