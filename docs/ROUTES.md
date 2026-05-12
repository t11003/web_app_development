# 路由與頁面設計文件 (Routes)：活動報名系統

## 1. 路由總覽表格

| 功能 | HTTP 方法 | URL 路徑 | 對應模板 | 說明 |
| :--- | :--- | :--- | :--- | :--- |
| 首頁 / 活動列表 | GET | `/` | `templates/index.html` | 顯示所有開放報名的活動 |
| 註冊頁面 | GET | `/auth/register` | `templates/auth/register.html` | 顯示註冊表單 |
| 執行註冊 | POST | `/auth/register` | — | 建立帳號並寫入 DB，成功後重導向至登入頁 |
| 登入頁面 | GET | `/auth/login` | `templates/auth/login.html` | 顯示登入表單 |
| 執行登入 | POST | `/auth/login` | — | 驗證帳號密碼，成功後設定 Session，重導向首頁 |
| 執行登出 | POST | `/auth/logout` | — | 清除 Session，重導向至首頁 |
| 建立活動頁面 | GET | `/events/create` | `templates/events/create.html` | 顯示新增活動表單 (需為 organizer) |
| 執行建立活動 | POST | `/events/create` | — | 接收資料建立活動，成功後重導向至活動詳細頁 |
| 活動詳細資訊 | GET | `/events/<int:id>` | `templates/events/detail.html` | 顯示活動內容、報名進度與報名按鈕 |
| 執行報名 | POST | `/events/<int:id>/register`| — | 依據目前報名人數處理正取/候補邏輯 |
| 執行取消報名 | POST | `/events/<int:id>/cancel` | — | 取消報名資格並觸發自動遞補機制 |
| 我的報名紀錄 | GET | `/my_registrations` | `templates/registrations/my_list.html` | 查詢登入者的所有活動報名狀態 |

---

## 2. 每個路由的詳細說明

### Auth 認證相關 (`/auth`)
*   **`GET /auth/register`**
    *   **輸入：** 無。
    *   **處理邏輯：** 單純渲染註冊表單。如果已經登入，則重導向回首頁。
    *   **輸出：** `auth/register.html`。
*   **`POST /auth/register`**
    *   **輸入：** 表單 (`username`, `email`, `password`)。
    *   **處理邏輯：** 驗證 email 是否已被註冊。若無，呼叫 `User.create()`，並將密碼加密後儲存。
    *   **輸出：** 成功則重導向 `/auth/login` 並閃現 (flash) 成功訊息；失敗則重新渲染註冊表單並顯示錯誤。
*   **`POST /auth/login`**
    *   **輸入：** 表單 (`email`, `password`)。
    *   **處理邏輯：** 驗證密碼是否正確，通過後將 `user_id` 存入 Flask Session。
    *   **輸出：** 成功重導向 `/` (首頁)；失敗重新渲染登入表單並顯示錯誤。
*   **`POST /auth/logout`**
    *   **處理邏輯：** 清除系統中的 Session 資料。重導向 `/` (首頁)。

### Main 首頁路徑 (`/`)
*   **`GET /`**
    *   **輸入：** 無。
    *   **處理邏輯：** 呼叫 `Event.get_all()` 取出以建立時間排序的活動列表。
    *   **輸出：** `index.html`。

### Events 活動相關 (`/events`)
*   **`GET /events/create`**
    *   **處理邏輯：** 確認目前 User 的 `role` 是否為 `organizer`，若不是則回傳 403 或重導回首頁。
    *   **輸出：** `events/create.html`。
*   **`POST /events/create`**
    *   **輸入：** 表單 (`title`, `description`, `event_date`, `location`, `capacity`)。
    *   **處理邏輯：** 確保輸入合法後，呼叫 `Event.create()`。
    *   **輸出：** 成功則重導向 `/events/<新增的 event_id>`。
*   **`GET /events/<int:id>`**
    *   **輸入：** URL 參數 `id`。
    *   **處理邏輯：** 呼叫 `Event.get_by_id(id)`。計算關聯的 `Registration` 中狀態為 `Confirmed` 的筆數，判斷是否已滿額。若目前使用者已登入，且已報名該活動，需一併取得其報名狀態，以便前端隱藏報名按鈕或顯示取消按鈕。
    *   **輸出：** `events/detail.html`。若找不到該 ID 則回傳 404。

### Registrations 報名相關
*   **`POST /events/<int:id>/register`**
    *   **輸入：** URL 參數 `id`，使用者必須登入。
    *   **處理邏輯：** 取得該活動資料。如果正取人數 `< capacity`，呼叫 `Registration.create(status='Confirmed')`；若正取已滿，則呼叫 `Registration.create(status='Waitlist')`。
    *   **輸出：** 重導向至 `/my_registrations`，並提示報名成功或進入候補。
*   **`POST /events/<int:id>/cancel`**
    *   **輸入：** URL 參數 `id`，使用者必須登入。
    *   **處理邏輯：** 找到該使用者對應的 `Registration`，將狀態改為 `Cancelled`。接著資料庫檢查該活動是否還有 `Waitlist` 的報名者。有的話，挑出 `created_at` 最早的那一筆，將其狀態更新為 `Confirmed`（自動遞補）。
    *   **輸出：** 重導向回活動頁 `/events/<id>` 或 `/my_registrations`，並提示成功取消。
*   **`GET /my_registrations`**
    *   **輸入：** 使用者必須登入。
    *   **處理邏輯：** 呼叫 `Registration.get_user_registrations(user_id)`，並透過關聯取得活動標題與時間等資訊供前端顯示。
    *   **輸出：** `registrations/my_list.html`。

---

## 3. Jinja2 模板清單

所有的模板將繼承自一個共用的 `base.html`，以保持視覺風格與導覽列的統一。

**基礎與共用模板:**
*   `templates/base.html` (包含 Navbar、Flash messages 區塊、Footer)
*   `templates/index.html` (首頁/活動列表卡片)

**認證相關:**
*   `templates/auth/login.html` (登入頁)
*   `templates/auth/register.html` (註冊頁)

**活動相關:**
*   `templates/events/create.html` (新增活動表單，主辦方專屬)
*   `templates/events/detail.html` (活動詳情頁，包含參加/取消按鈕)

**報名相關:**
*   `templates/registrations/my_list.html` (個人報名紀錄清單)
