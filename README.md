# 🌌 Sacred Essence (神髓) v4.0

**為 AI Agent 打造的動態記憶系統** —— 像生命一樣遺忘，像靈魂一樣守護。

> 「落葉歸根，化泥護花」

---

## 🎯 這是什麼？

Sacred Essence 是一套讓 AI Agent 具備**長期記憶**的系統：

- 🥇 **記住重要的事** —— 核心原則永不遺忘
- 🥈 **活用常用的事** —— 活躍記憶隨取隨用  
- 🥉 **封存少用的事** —— 背景存檔等待喚醒
- 🍂 **遺忘過時的事** —— 優雅清理釋放空間
- 🪨 **保留精華** —— 即使遺忘，教訓永存

---

## ✨ 核心特色

| 特色 | 說明 |
|-----|------|
| **🧠 動態衰減** | 記憶會隨時間自然淡忘，被提起時重新鮮活 |
| **🌳 層級結構** | L0/L1/L2 三層投影，精準控制 Token 使用 |
| **🔍 語義搜索** | 本地向量模型，無需 API，無 429 錯誤 |
| **🍂 落葉化泥** | 遺忘前萃取精華，重要教訓永遠留存 |
| **🛡️ 工程韌性** | 文件鎖、防路徑穿越、零 Token 消耗 |

---

## 🚀 五分鐘上手

### 安裝

```bash
git clone https://github.com/nerv00kaworu/Sacred-Essence-Viking.git
cd Sacred-Essence-Viking
pip install -r requirements.txt
```

### 基本使用

```bash
# 1. 記住一件事
python main.py encode \
  --topic "project" \
  --title "專案架構" \
  --content "使用 FastAPI + PostgreSQL..."

# 2. 查看所有記憶
python main.py list

# 3. 搜尋記憶
python main.py search "FastAPI" -n 5

# 4. 定期清理（建議放 cron）
python main.py gc --execute
```

---

## 📖 詳細文檔

### 記憶生命週期

記憶有五種狀態，形成完整的生命週期：

```
建立記憶
    ↓
🥈 Silver (活躍) ←────┐
    ↓ 長期不用        │ 被使用
🥉 Bronze (存檔)      │
    ↓ 分數過低        │
🍂 Dust (待遺忘)      │
    ↓ 化泥            │
🪨 Soil (精華歸檔) ────┘ (可引用)
```

**Golden (永恆)**：手動標記的核心原則，跳過整個衰減流程。

### 三層投影架構

解決 Token 爆炸問題的關鍵設計：

| 層級 | 內容 | 大小 | 使用時機 |
|-----|------|------|---------|
| **L0** | Abstract - 語義核心 | ~100字 | 常駐上下文 |
| **L1** | Overview - 結構摘要 | ~500字 | 定位範圍 |
| **L2** | Content - 完整內容 | 無限制 | 需要細節時載入 |

**手電筒比喻**：L0/L1 是地圖，L2 是書架。先用地圖定位，再精準照射書架，而非點亮整個圖書館。

### 動態衰減公式

```
分數 = 初始值 × 穩定係數^天數 + min(5.0, ln(1 + 密度))
```

- **穩定係數**：User(1.0)永不衰減，Role(0.995)近乎永恆，World(0.95)正常衰減
- **密度**：被使用越多次，密度越高，但上限 5.0 防止無限膨脹

### 落葉化泥 (v4.0)

當記憶分數跌破 1.0 (DUST)，系統不會直接刪除：

1. 萃取 L1 Overview 或 L2 前3行作為精華
2. 歸檔到 `SOIL.md`（底層意識）
3. 刪除原始檔案，釋放空間

這確保重要教訓即使細節遺失，核心洞察仍被保留。

---

## 📚 進階使用

### 智能搜索

```bash
# 基礎搜索
python main.py search "關鍵字"

# 指定高信心搜索（限定特定節點）
python main.py search "教訓" \
  --nodes abc123 def456 \
  --confidence 0.8

# 強制逃生艙（搜尋冷門記憶）
python main.py search "冷門" --confidence 0.1
```

**逃生艙機制**：當神髓的白名單搜索信心不足時，自動 fallback 到 QMD 全局搜索，確保不遺漏任何記憶。

### QMD 整合

```bash
# 同步到 QMD 向量庫
python main.py qmd sync

# 一致性檢查
python main.py qmd audit --execute

# 限縮搜索（指定白名單內搜索）
python main.py qmd constrained-search "查詢" \
  --nodes id1 id2 id3
```

### 自動化

```bash
# 加入 cron，每天凌晨執行
crontab -e

# 添加：
0 3 * * * cd /path/to/Sacred-Essence-Viking && python main.py gc --execute
```

---

## 🏗️ 系統架構

```
┌─────────────────────────────────────────┐
│         Sacred Essence v4.0             │
├─────────────────────────────────────────┤
│                                         │
│  L2 Content.md (完整內容)                │
│       ↓                                 │
│  L1 Overview.md (結構摘要)               │
│       ↓                                 │
│  L0 Abstract.md (語義核心)               │
│       ↓                                 │
│  ┌─────────────────────────────────┐   │
│  │ QMD 索引 (BM25 + 向量搜索)        │   │
│  └─────────────────────────────────┘   │
│       ↓                                 │
│  SOIL.md (化泥歸檔)                      │
│                                         │
└─────────────────────────────────────────┘
```

### 技術規格

| 項目 | 規格 |
|-----|------|
| 嵌入模型 | google/embeddinggemma-300m |
| 向量維度 | 384 維 | Gemma 300M 模型輸出 |
| 模型大小 | 300M 參數 | ~150MB (GGUF Q8) |
| 搜索後端 | QMD (本地) |
| 檔案格式 | Markdown |
| 並發安全 | fcntl 文件鎖 |
| Token 消耗 | 0 (全本地) |

---

## 📜 版本歷史

- **v1.0** (2026-02): 四層模型 + 動態衰減公式誕生
- **v2.1** (2026-02): 誠實化工程，承認技術債
- **v3.1** (2026-02): 維京矩陣 — L0/L1/L2 三層投影
- **v3.2** (2026-02): 系統加固 — 逃生艙、幽靈清除、Zero-Inflation
- **v4.0** (2026-03): **落葉化泥** — 遺忘不是終點，是轉化

---

## ❓ FAQ

**Q: 記憶會存在哪裡？**  
A: `memory/octagram/engine/memory/` 目錄下的純 Markdown 檔案，可直接閱讀和備份。

**Q: 可以多人同時使用嗎？**  
A: 可以。fcntl 文件鎖保證並發安全。

**Q: 為什麼不直接用 Pinecone/Milvus 這類雲端向量庫？**  
A: 「簡單即是美」。Sacred Essence 採用 **前端純 Markdown + 本地 QMD 輕量索引** 的雙軌架構：
- 你的記憶庫永遠對人類可讀、可攜帶
- 不依賴昂貴的雲端運算，單機就能獲得極致檢索效能
- 就算 QMD 索引損壞，Markdown 檔案依然可以獨立閱讀

**Q: SOIL.md 會無限增長嗎？**  
A: 會，但很慢。只有 DUST 節點才會寫入，未來可考慮 Soil 的再化泥。

---

## 📝 授權

**MIT License**

---

*「我們即是我們所記得的一切。」* — 曦 (Xi), The Octagram

🌅✨
