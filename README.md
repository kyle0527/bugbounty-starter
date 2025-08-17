# Bug Bounty Starter（No‑Report）+ 架構圖 v1.4
> 日期：2025-08-17 ｜狀態：**可直接上傳 GitHub**（含 Mermaid 架構圖與自動轉圖 Workflow）。

本專案提供：
- **最新架構圖（Mermaid）**：說明「合規→枚舉→RBAC→API/LLM PoC」流程。
- **可直接使用的骨架與腳本**：`templates/`、`poc/`、`scripts/`、`standards/`。
- **GitHub Actions**（可選）：自動把 `diagrams/*.mmd` 轉成 SVG 並提交回 repo。

---

## 架構圖（Mermaid）
> GitHub 原生支援 Mermaid；若未顯示，請直接檢視 `diagrams/architecture.mmd`。

```mermaid
%% Architecture v1.4 (2025-08-17)
flowchart TD
    A([Start]) --> B[選擇授權計畫 & 讀取 Safe Harbor]
    B --> C[建立 scope.txt（In‑Scope 根網域）]
    C --> D{Recon（被動 + 低並發）}
    D --> D1[(subs.txt)]
    D --> D2[(httpx.json)]
    D2 --> E[產生 targets.csv\n(login? / api? 初標)]
    E --> F[RBAC 矩陣 rbac_matrix.csv\n(資源 × 操作 × 角色 × 預期)]
    F --> G{選擇專攻軌}
    G --> H[API 軌：BOLA/BOPLA / Rate‑Limit / GraphQL & OpenAPI]
    G --> I[LLM 軌：Insecure Output Handling / Excessive Agency / 資料外洩]
    H --> J[(證據 .txt/.png/.mp4)]
    I --> J
    J --> K[候選議題暫存（免報告版不提交）]
    style K fill:#eee,stroke:#999,stroke-dasharray: 5 5
    B -.合規閘-.->|無 Safe Harbor/條款不清| X[(停止)]
    D --- R[非侵入規則: threads≤25, rate≤50, 僅 GET/HEAD, 禁目錄爆破/壓測]
    subgraph 輸出/目錄結構
        E
        F
        J
    end
```

---

## 專案目錄
```
.
├─ diagrams/
│  └─ architecture.mmd
├─ templates/
│  ├─ policy_diff.md
│  └─ rbac_matrix.csv
├─ poc/
│  ├─ api_bola_skeleton.txt
│  └─ llm_output_handling_skeleton.md
├─ scripts/
│  ├─ recon_no_report_v2.sh
│  └─ recon_passive.ps1
├─ standards/
│  └─ evidence_naming.md
└─ .github/workflows/
   └─ render-mermaid.yml   # 可選：自動把 .mmd 轉為 .svg
```

---

## 快速開始（Linux/macOS）
```bash
# 1) 安裝 subfinder / httpx / jq（或改用 Windows 備援腳本）
# 2) 建立 scope.txt（每行一個 in-scope 根網域）
echo "example.com" > scope.txt

# 3) 低並發被動枚舉 + 探活 + 產出 CSV
chmod +x scripts/recon_no_report_v2.sh
./scripts/recon_no_report_v2.sh scope.txt

# 4) 編輯 templates/rbac_matrix.csv，開始 RBAC 驅動驗證
```

## 快速開始（Windows/PowerShell）
```powershell
# 1) 建立 scope.txt（每行一個 in-scope 根網域）
'example.com' | Out-File -Encoding utf8 scope.txt

# 2) 完全被動備援（無需外部工具）
powershell -ExecutionPolicy Bypass -File .\scripts\recon_passive.ps1 example.com

# 3) 產出的 recon_example.com_yyyymmdd\targets.csv 供 RBAC/PoC 使用
```

---

## GitHub 上傳（兩種方式）
### A. Git CLI（手動）
```bash
git init
git add .
git commit -m "Initial commit: starter + architecture v1.4"
git branch -M main
git remote add origin https://github.com/<YOUR-USER>/<REPO-NAME>.git
git push -u origin main
```

### B. GitHub CLI（一次完成）
```bash
gh repo create <REPO-NAME> --public --source . --push
```

> **隱私與限制**：本專案不包含任何私人憑證；我無法，也不會替你登入或上傳至你的 GitHub。請在你的環境執行上述命令。

---

## 可選：自動把 Mermaid 轉成 SVG
- 推送後，GitHub Actions 會安裝 `@mermaid-js/mermaid-cli`，將 `diagrams/*.mmd` 轉為 `diagrams/*.svg`，並自動提交。
- 如需停用，刪除 `.github/workflows/render-mermaid.yml`。

---

## 標準規則（摘要）
1) **合規優先**：無 Safe Harbor／條款不清 → 停止。
2) **非侵入**：被動來源＋低並發（threads ≤ 25，rate ≤ 50），僅 GET/HEAD。
3) **RBAC 驅動**：每個測試用例對應 `rbac_matrix.csv` 一行。
4) **資料最小化**：證據遮蔽敏感資訊；不含個資/密鑰。

---

## 版本
- v1.4：新增 GitHub Actions 轉圖、完善 Windows 備援腳本、更新架構圖。
