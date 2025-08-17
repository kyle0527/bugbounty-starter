# Burp Suite Professional – 規格包（Spec Pack）
版本標記：v2025-08-17　｜　產生日期（UTC）：2025-08-17

本 repo 收錄可讓 AI（例：ChatGPT Codex）直接工作的完整規格檔與任務配置，對齊「A–G 七大類」功能表。

---

## 目錄結構
- `burp_pro_spec.json`：**機器可讀規格**（含 feature IDs、依賴、輸入/輸出、Pro-only 標記等）。
- `PROMPT_Agent_Instructions.md`：**AI 建置指令稿**（放入 AI 的 system 指令區）。
- `ACCEPTANCE_Checklist.md`：**驗收清單**（全域 gate 與各模組測試要點）。
- `TASKS_Plan.csv`：**任務規劃**（feature_id、依賴、優先度、預估點數）。
- `README.md`：本說明。
- `codex_first_prompt.txt`：**在 Codex 中貼的第一段指令**（可直接複製）。

---

## 一、上傳到 GitHub（快速流程）
> 若你已在 GitHub 建好空 repo：直接把上述檔案上傳到 **repo 根目錄**（main 分支）。

### 方法 A：GitHub 網頁 UI（最簡單）
1. 進入新建的 repo → **Add file ▸ Upload files**。
2. 拖曳本機的 `burp_pro_spec.json`、`PROMPT_Agent_Instructions.md`、`ACCEPTANCE_Checklist.md`、`TASKS_Plan.csv`、`README.md`、`codex_first_prompt.txt`。
3. **Commit changes**。

### 方法 B：Git 命令列（選用）
```bash
git init -b main
git add .
git commit -m "Initial commit: Burp Pro spec pack"
git remote add origin https://github.com/<你>/burp-pro-spec.git
git push -u origin main
```

---

## 二、在 ChatGPT 內用 **Codex（雲端工程代理）** 連接此 repo
> 目的：讓 Codex 可載入 repo、讀取 `burp_pro_spec.json`，並依 `TASKS_Plan.csv` 開工。

1. **連接 GitHub**（只授權此 repo；建議 Private）。  
2. 開啟 **Codex** → **Create Environment** → 選此 repo 建立環境。  
3. 進入環境後，切到 *Ask* 或 *Code* 模式。  
4. **把 `codex_first_prompt.txt` 內容貼到 Codex 的對話輸入框**並送出（見下一節）。

---

## 三、第一個指令要貼哪裡、怎麼貼？
- **貼哪裡**：在 Codex 介面的輸入框（*Ask* 或 *Code* 模式皆可）。  
- **怎麼貼**：打開本 repo 的 `codex_first_prompt.txt`，**全選複製**，直接貼上後送出。  
- Codex 會：
  1) 讀取 `burp_pro_spec.json` 與 `TASKS_Plan.csv`；  
  2) 產生實作規劃與初始目錄骨架；  
  3) 建立測試腳手架與反向驗證報表（coverage.json/CSV）。

---

## 四、（選用）本機 **Codex CLI** 工作流
```bash
# 安裝
npm install -g @openai/codex

# 在 repo 根目錄啟動（建議先用建議模式）
codex            # 互動建議
# 或可寫檔
codex --auto-edit
# 或全自動（沙箱）
codex --full-auto
```
> 進入會話後，將 `codex_first_prompt.txt` 內容貼入 Codex CLI 的對話。

---

## 五、驗收與治理
- 遵循 `PROMPT_Agent_Instructions.md` 與 `ACCEPTANCE_Checklist.md` 的規則。  
- 強制**反向驗證**：每次提交需更新 feature 覆蓋對照表（mapping/coverage.json）。  
- 標準版本：`EvalRules_v2025-08-17`。

---

## 六、常見問題
- **看不到新 repo**：GitHub 授權與索引可能有延遲；確保只對此 repo 授權。  
- **PR 權限**：若要 Codex 自動開 PR，需在 GitHub 上賦予相應權限（最小範圍原則）。  
- **安全**：建議 Private repo；避免把密鑰放進版本庫。

---

## 七、後續建議
- 若只做 **Pro 專屬**模組，可在 `TASKS_Plan.csv` 內將非 Pro-only 先標記延後。  
- 若要多語言範本（Python/TypeScript），可新增 `/impl/` 資料夾，由 Codex 依計畫建立骨架。
