# 路由與頁面設計文件 (Routes) - 個人記帳簿系統

基於 PRD、架構文件以及資料庫設計，本文件定義了 Flask 的所有端點路由，以供前端頁面進行資料綁定與操作。

## 1. 路由總覽表格

| 功能 | HTTP 方法 | URL 路徑 | 對應模板 | 說明 |
| --- | --- | --- | --- | --- |
| 首頁 (總餘額與最新紀錄) | GET | `/` | `templates/main/index.html` | 顯示目前總餘額，以及最近的幾筆收支紀錄。並隱性觸發自動扣款檢查。 |
| 收支查詢清單 | GET | `/transactions` | `templates/transactions/index.html`| 顯示所有紀錄，支援以日期過濾。 |
| 新增收支頁面 | GET | `/transactions/new` | `templates/transactions/form.html` | 顯示新增收入或支出的表單介面。 |
| 建立收支 | POST | `/transactions` | — | 接收使用者送出表單，寫入資料庫後重導至首頁。 |
| 刪除單筆收支 | POST | `/transactions/<id>/delete`| — | 刪除指定記錄，避免意外誤刪故採用 POST 實作，完畢後重導至列表頁。 |
| 固定扣款清單 | GET | `/fixed-deductions` | `templates/fixed_deductions/index.html`| 顯示與管理每月設定的固定支出。 |
| 新增固定扣款頁面| GET | `/fixed-deductions/new` | `templates/fixed_deductions/form.html` | 顯示建立新自動扣款的表單。 |
| 建立固定扣款 | POST | `/fixed-deductions` | — | 接收使用者送出表單，寫入設定並重導回清單。 |
| 刪除固定扣款 | POST | `/fixed-deductions/<id>/delete`| — | 取消該項目的後續每月自動扣款計算。 |

---

## 2. 每個路由的詳細說明

### 首頁模組
- `GET /`
  - **輸入**：無。
  - **處理邏輯**：觸發 FixedDeduction 自動扣款檢查邏輯；調用 `Transaction.get_total_balance()` 與 `Transaction.get_all()` (限制前幾筆) 來獲取基礎儀表板資料。
  - **輸出**：渲染 `main/index.html`。
  - **錯誤處理**：如果資料庫裡沒任何記錄，無影響，正常回傳預設的 0 或空陣列。

### 收支實體 (Transaction) 模組
- `GET /transactions`
  - **輸入**：URL 查詢參數 `start_date`, `end_date` (可選)。
  - **處理邏輯**：判斷是否有參數傳入，決定呼叫 `get_all()` 還是 `get_by_date_range()`。
  - **輸出**：渲染 `transactions/index.html`。
- `POST /transactions`
  - **輸入**：表單參數 `type`, `amount`, `category`, `transaction_date`。
  - **處理邏輯**：驗證 `amount` 是否為正整數、`date` 是否合法後，存入 DB。
  - **輸出**：Redirect 至 `/` (快速查看結果) 或是 `/transactions`。
  - **錯誤處理**：如果必填欄位空白，存回 flash message，重導回表單頁。

### 固定扣款 (Fixed Deduction) 模組
- `POST /fixed-deductions`
  - **輸入**：表單參數 `amount`, `category`, `deduct_day`。
  - **處理邏輯**：驗證 `deduct_day` 是否落於 1-31，並存入資料庫。
  - **輸出**：Redirect 至 `/fixed-deductions`。
  - **錯誤處理**：日期超出月份合理範圍時 flash 錯誤提示。

---

## 3. Jinja2 模板清單

所有的網頁模板都會共用 `base.html` 提供的導覽列結構與樣式。

* **共用版型**
  * `templates/base.html`：包含 HTML5 Skeleton、NavBar、全域共用 CSS。
* **首頁**
  * `templates/main/index.html`：儀表板 (Dashboard) 設計，繼承自 `base.html`。
* **收支頁面**
  * `templates/transactions/index.html`：含區間篩選器的歷史表格，繼承自 `base.html`。
  * `templates/transactions/form.html`：包含表單元素的新增頁面，繼承自 `base.html`。
* **固定扣款頁面**
  * `templates/fixed_deductions/index.html`：展示扣款設定清單，繼承自 `base.html`。
  * `templates/fixed_deductions/form.html`：固定扣款特定欄位的新增頁面，繼承自 `base.html`。

---

## 4. 路由骨架程式碼
相關定義已實作於 `app/routes/` 下的 `main.py`, `transaction.py`, 與 `fixed_deduction.py` 之中。
