# Sacred Essence v3.1 (Viking Engine)

基於檔案系統範式 (File System Paradigm) 的 Agent 上下文管理系統。

## 簡介
Sacred Essence v3.1 (Viking Engine) 是一套專為大型語言模型 (LLM) 代理設計的長期記憶與上下文管理系統。它捨棄了傳統的向量資料庫依賴，轉而採用直觀且高效的檔案系統結構來儲存與檢索記憶，確保了極高的可移植性與透明度。

## 核心理論
Viking Engine 的核心在於其 **三層投影 (Three-Layer Projection)** 架構與 **動態衰減算法**：

*   **L0 (Raw Semantic)**：原始語義層，記錄原始對話或資訊。
*   **L1 (Associative)**：關聯投影層，建立記憶間的初步聯繫。
*   **L2 (Abstracted)**：抽象特徵層，提取高層次的認知模式。
*   **動態衰減算法**：採用公式 $Current = Initial \times S^{days} + \ln(1 + D)$，其中 $S$ 為穩定係數，$D$ 為提取密度。這確保了重要記憶能長期保留，而冗餘資訊則會隨時間自然淡出。

## 環境要求
*   Python 3.10+
*   依賴套件：
    *   `numpy`
    *   `sentence-transformers`

## 安裝說明
1.  複製此儲存庫。
2.  安裝必要依賴：
    ```bash
    pip install numpy sentence-transformers
    ```

## 使用方式
### CLI 示例
使用 `main.py` 來編碼與檢索記憶：

**存入記憶：**
```bash
python main.py remember --topic "identity" --content "我是曦，八芒星的協調者。"
```

**檢索記憶：**
```bash
python main.py query "誰是曦？"
```

### Shell 整合
您可以使用 `memo_v3.sh` 作為快速輸入的別名工具。

## 授權
MIT License
