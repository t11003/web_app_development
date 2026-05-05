# 路由設計文件 (API Design)

根據系統架構與流程圖，以下為個人記帳簿系統的路由與頁面規劃。

## 1. 路由總覽表格

| 功能 | HTTP 方法 | URL 路徑 | 對應模板 | 說明 |
| :--- | :--- | :--- | :--- | :--- |
| 首頁 (餘額與列表) | GET | `/` | `index.html` | 顯示總餘額與歷史紀錄列表 |
| 新增紀錄頁面 | GET | `/records/new` | `records/new.html` | 顯示新增收支的表單 |
| 送出新增紀錄 | POST | `/records` | — | 接收表單資料，寫入 DB，重導向至首頁 |
| 編輯紀錄頁面 | GET | `/records/<id>/edit`| `records/edit.html`| 顯示帶有既有資料的編輯表單 |
| 更新紀錄 | POST | `/records/<id>/update`| — | 接收表單資料，更新 DB，重導向至首頁 |
| 刪除紀錄 | POST | `/records/<id>/delete`| — | 從 DB 刪除該紀錄，重導向至首頁 |

## 2. 每個路由的詳細說明

### 首頁 (`GET /`)
- **輸入**：無
- **處理邏輯**：呼叫 `RecordModel.get_balance()` 與 `RecordModel.get_all()`
- **輸出**：渲染 `index.html`，傳入 `balance` 與 `records` 變數
- **錯誤處理**：若資料庫為空，顯示「目前尚無紀錄」的提示

### 新增紀錄頁面 (`GET /records/new`)
- **輸入**：無
- **處理邏輯**：無特殊資料處理
- **輸出**：渲染 `records/new.html`

### 送出新增紀錄 (`POST /records`)
- **輸入**：表單欄位 `type`, `amount`, `date`, `category`, `description`
- **處理邏輯**：呼叫 `RecordModel.create(...)`
- **輸出**：成功後重導向 (`redirect`) 到首頁 `/`
- **錯誤處理**：如果必填欄位缺失或格式錯誤（如金額非數字），flash 錯誤訊息並重導向回新增頁面。

### 編輯紀錄頁面 (`GET /records/<id>/edit`)
- **輸入**：URL 參數 `id`
- **處理邏輯**：呼叫 `RecordModel.get_by_id(id)`
- **輸出**：若找到紀錄，渲染 `records/edit.html` 並傳入 `record`；若找不到，回傳 404 頁面
- **錯誤處理**：無效的 ID 應直接觸發 404 Not Found

### 更新紀錄 (`POST /records/<id>/update`)
- **輸入**：URL 參數 `id` 與表單欄位 `type`, `amount`, `date`, `category`, `description`
- **處理邏輯**：呼叫 `RecordModel.update(...)`
- **輸出**：成功後重導向至首頁 `/`
- **錯誤處理**：資料驗證失敗則 flash 錯誤訊息，重導向回編輯頁面

### 刪除紀錄 (`POST /records/<id>/delete`)
- **輸入**：URL 參數 `id`
- **處理邏輯**：呼叫 `RecordModel.delete(id)`
- **輸出**：刪除成功後重導向至首頁 `/`

## 3. Jinja2 模板清單

所有模板皆預計繼承自 `base.html`，以保持網站版型與導覽列風格統一。

- **`base.html`**：共用外框（包含導覽列、Flash 訊息區塊、頁尾，以及 CSS 引入）。
- **`index.html`**：顯示「總餘額卡片」與「歷史收支表格」。
- **`records/new.html`**：顯示新增紀錄的 HTML 表單。
- **`records/edit.html`**：顯示修改紀錄的 HTML 表單。

## 4. 路由骨架程式碼

已在 `app/routes.py` 中建立對應的 Blueprint 路由骨架（目前僅包含定義與註解，未實作邏輯）。
