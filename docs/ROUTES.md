# 路由設計文件 (ROUTES)

## 專案名稱：個人記帳簿 (Personal Expense Tracker)

### 1. 路由總覽表格

| 功能 | HTTP 方法 | URL 路徑 | 對應模板 | 說明 |
| --- | --- | --- | --- | --- |
| **首頁：財務總覽** | GET | `/` | `templates/index.html` | 首頁，顯示單月總收支與圖表 |
| **收支列表** | GET | `/expenses` | `templates/expenses/index.html` | 列出所有收支明細 |
| **新增收支頁面** | GET | `/expenses/new` | `templates/expenses/form.html` | 提供新增明細的表單 |
| **送出新增紀錄** | POST | `/expenses/new` | — | 接收新增表單並存入 DB，重導向到 `/expenses` |
| **編輯收支頁面** | GET | `/expenses/<id>/edit` | `templates/expenses/form.html` | 提供編輯明細的表單 |
| **送出更新紀錄** | POST | `/expenses/<id>/edit` | — | 接收編輯表單並更新 DB，重導向到 `/expenses` |
| **刪除紀錄** | POST | `/expenses/<id>/delete` | — | 刪除單筆明細，重導向到 `/expenses` |
| **分類列表** | GET | `/categories` | `templates/categories/index.html` | 列出所有分類 (包含預設與自訂) |
| **新增分類頁面** | GET | `/categories/new` | `templates/categories/form.html` | 提供新增自訂分類的表單 |
| **送出新增分類** | POST | `/categories/new` | — | 接收分類表單並存入 DB，重導向到 `/categories` |
| **編輯分類頁面** | GET | `/categories/<id>/edit` | `templates/categories/form.html` | 提供編輯自訂分類的表單 |
| **送出更新分類** | POST | `/categories/<id>/edit` | — | 接收分類更新並寫入 DB，重導向到 `/categories` |
| **刪除分類** | POST | `/categories/<id>/delete` | — | 刪除單筆自訂分類，重導向到 `/categories` |

### 2. 每個路由的詳細說明

各 Endpoint 的邏輯規劃、呼叫的 Models Methods、輸入以及錯誤處理 (Error Handling)，都已寫在 `app/routes/` 裡的各個 `.py` 檔案的 **Docstrings** 之中。詳細邏輯包括「不能刪除預設分類」、「表單漏填驗證的 Flash 提示」等。

### 3. Jinja2 模板清單

所有的視圖介面規劃如下，部分模板會共用：

1. **`templates/base.html`**: 共用全站骨架，定義 `{% block content %}`。包含頂部的 Navbar 和引入共用 CSS 的設置。
2. **`templates/index.html`**: 首頁總覽，繼承自 `base.html`，展示上方的 Dashboard 卡片與下方的 Chart 圖表。
3. **`templates/expenses/index.html`**: 收支明細列表表格，繼承自 `base.html`。
4. **`templates/expenses/form.html`**: 收支的「新增」與「編輯」共用表單版面，透過 Action URL 或變數切換狀態，繼承自 `base.html`。
5. **`templates/categories/index.html`**: 分類清單，展示收入/支出類別列表，繼承自 `base.html`。
6. **`templates/categories/form.html`**: 分類的「新增」與「編輯」共用表單版面，繼承自 `base.html`。

### 4. 路由骨架程式碼

基於模組化原則，我們為首頁、收支、與分類分別設立 Flask Blueprint (藍圖)：
- `app/routes/index.py`: 處理 `/`
- `app/routes/expense.py`: 處理 `/expenses/*`
- `app/routes/category.py`: 處理 `/categories/*`
