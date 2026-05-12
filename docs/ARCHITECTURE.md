# 系統架構文件 (Architecture)：活動報名系統

## 1. 技術架構說明

本系統採用傳統的伺服器端渲染 (Server-Side Rendering, SSR) 架構，以減少初期開發成本，並能快速達成專案目標。以下為選用的技術與原因：

*   **後端框架：Python + Flask**
    *   **原因：** Flask 是一個輕量級的 Web 框架，適合快速開發 MVP。它的設計簡單直覺，擴充性強，非常適合本專案中小型活動報名系統的規模。
*   **模板引擎：Jinja2**
    *   **原因：** Jinja2 內建於 Flask 中，這讓我們可以輕鬆將後端的資料透過變數注入到前端 HTML 中，進行動態頁面渲染，不需再另外架設前端 API 與建立複雜的前後端分離架構。
*   **資料庫：SQLite**
    *   **原因：** SQLite 是輕量的檔案型資料庫，不需要安裝和設定獨立的資料庫伺服器，對中小型專題與初期測試來說效能已完全足夠。未來若有需要擴展規模，也可以再考慮遷移至其他進階的關聯式資料庫。

### Flask MVC 模式說明

我們採用類似 MVC (Model-View-Controller) 的概念來組織 Flask 專案結構：
*   **Model (資料模型)：** 負責一切與資料庫相關的邏輯。定義如何儲存、查詢與修改活動紀錄與報名名單。
*   **View (視圖)：** 在這裡是指 HTML 模板 (Jinja2)。負責呈現資料與建構使用者介面。
*   **Controller (控制器)：** 即 Flask 的「路由 (Routes)」。它負責接收瀏覽器的請求 (Request)，向 Model 請求相關資料後，再呼叫 View（模板引擎）處理渲染，最後將結果回傳給瀏覽器。

---

## 2. 專案資料夾結構

本專案採用分類明確的資料夾結構，以確保各元件職責分離，提升後續維護的便利性。

```text
web_app_development/
├── app/                        # 主要應用程式的資料夾
│   ├── __init__.py             # 初始化 Flask 應用程式、載入設定
│   ├── models/                 # 資料庫模型 (Model)
│   │   └── database.py         # 定義資料表與類別 (例如：活動、報名者)
│   ├── routes/                 # 應用程式路由邏輯處理 (Controller)
│   │   ├── auth_routes.py      # 登入註冊相關路由
│   │   ├── event_routes.py     # 活動相關功能路由 (新增活動、瀏覽活動)
│   │   └── registration_routes.py # 報名與結果查詢相關路由
│   ├── templates/              # Jinja2 網頁 HTML 模板 (View)
│   │   ├── base.html           # 全站共用的佈局模板 (如 Navbar, Footer)
│   │   ├── index.html          # 首頁 / 活動列表頁
│   │   ├── create_event.html   # 新增活動表單頁
│   │   ├── event_detail.html   # 活動詳細資訊頁
│   │   └── my_registrations.html # 我的報名紀錄查詢頁
│   └── static/                 # 靜態資源 (CSS / JS / Images)
│       ├── css/
│       │   └── style.css       # 全站共用樣式表
│       ├── js/
│       │   └── scripts.js      # 前端互動邏輯腳本
│       └── images/             # 圖片存放區
├── instance/                   # 存放敏感或執行時產生的資料
│   └── application.db          # SQLite 本地資料庫檔案
├── docs/                       # 開發文件存放區
│   ├── PRD.md                  # 產品需求文件
│   └── ARCHITECTURE.md         # (本檔案) 系統架構文件
├── app.py                      # 程式進入點 (負責啟動應用程式)
├── requirements.txt            # Python 相依套件清單
└── README.md                   # 專案介紹及使用說明
```

---

## 3. 元件關係圖

以下展示使用者發起請求後，各系統元件之間的互動流程：

```mermaid
flowchart TD
    User([瀏覽器 Browser])

    subgraph "Flask Application (後端)"
        Router[Flask Route (Controller)]
        Template[Jinja2 Template (View)]
        Model[Database Model (Model)]
    end

    DB[(SQLite 資料庫)]

    %% 請求流程
    User -- "1. 發送 HTTP Request\n(如：GET /event/1)" --> Router
    Router -- "2. 查詢資料\n(取得活動與報名狀況)" --> Model
    Model -- "3. 執行 SQL 語法" --> DB
    DB -- "4. 回傳查詢結果" --> Model
    Model -- "5. 將資料回傳" --> Router
    Router -- "6. 傳遞資料與選擇模板" --> Template
    Template -- "7. 渲染出 HTML 結果" --> Router
    Router -- "8. 回傳 HTTP Response\n(顯示網頁)" --> User
```

---

## 4. 關鍵設計決策

1.  **不採用前後端分離開發模式**
    *   **原因：** 此系統為早期 MVP 階段，功能相對聚焦。不採用前後端分離（如使用 React / Vue），可以省掉複雜的 API 串接與跨域處理問題。交由 Flask + Jinja2 包辦能將所有邏輯集中，大幅降低開發時程與團隊合作的溝通成本。
2.  **依功能拆分路由模組 (Blueprints)**
    *   **原因：** 將路由依照業務邏輯分門別類放在 `routes/` 資料夾內（例如：會員認證 `auth`、活動 `event`、報名 `registration`），而不是全部塞入單一 `app.py` 中。這樣可確保程式碼可讀性，未來加入新功能時也不容易發生修改衝突。
3.  **資料庫模型採狀態標記處理候補機制**
    *   **原因：** 為滿足「滿額後轉候補、取消時自動遞補」的需求，在報名紀錄中加入狀態欄位（Status：如 `正取`, `候補`, `取消`）。當有人取消時，系統只需用 SQL 語法撈取狀態為 `候補` 且時間最早的一筆紀錄，變更為 `正取` 即可，無需複雜的資料表搬演程序，確保一致性與效能。
4.  **共用版面設計 (Base Template)**
    *   **原因：** 在 Jinja2 中建立 `base.html` 來管理所有的通用配置（包含標題欄位 Navbar、頁腳 Footer 以及 CSS / JS 檔案載入）。首頁或內頁只需繼承這個基礎模板即可，未來若想修改外觀，只需更動一個檔案便能套用全站。
