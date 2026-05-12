# 流程圖文件 (Flowchart)：活動報名系統

## 1. 使用者流程圖 (User Flow)

這個流程圖展示了「學生」與「主辦方」兩種角色在系統中的主要操作路徑。

```mermaid
flowchart LR
    Start([使用者進入網站]) --> Auth{是否登入?}
    
    Auth -->|未登入| Login[前往登入/註冊頁面]
    Login --> Start
    
    Auth -->|已登入| Home[首頁 - 活動清單]
    
    %% 主辦方路徑
    Home -->|主辦方| CreateBtn[點擊建立活動]
    CreateBtn --> CreateForm[填寫活動資訊表單]
    CreateForm --> SubmitEvent{送出}
    SubmitEvent -->|成功| EventDetail[活動詳細資訊頁]
    
    %% 學生路徑
    Home -->|學生| Browse[瀏覽活動清單]
    Browse --> ClickEvent[點擊進入特定活動]
    ClickEvent --> EventDetail
    
    EventDetail --> CheckReg{是否已報名?}
    CheckReg -->|是| CancelBtn[點擊取消報名]
    CancelBtn --> UpdateStatus[系統取消資格並自動遞補候補]
    UpdateStatus --> EventDetail
    
    CheckReg -->|否| RegBtn[點擊我要報名]
    RegBtn --> CheckFull{名額是否額滿?}
    
    CheckFull -->|否| RegSuccess[報名成功 - 正取]
    CheckFull -->|是| RegWait[報名登記 - 轉入候補]
    
    RegSuccess --> MyList[我的報名紀錄頁]
    RegWait --> MyList
    EventDetail -->|導覽列進入| MyList
    
    MyList --> ViewStatus[查看當前狀態：正取/候補/已取消]
```

## 2. 系統序列圖 (Sequence Diagram)

這張圖展示了本系統最核心的機制：「**學生報名活動及自動判定候補**」的資料流向。

```mermaid
sequenceDiagram
    actor User as 學生
    participant Browser as 瀏覽器 (Browser)
    participant Route as Flask Route (Controller)
    participant Model as DB 模型 (Model)
    participant DB as SQLite 資料庫
    
    User->>Browser: 點擊「我要報名」
    Browser->>Route: POST /event/1/register
    
    Route->>Model: 查詢該活動正取名額狀況
    Model->>DB: SELECT COUNT(*) 取得目前正取人數
    DB-->>Model: 回傳目前人數
    Model-->>Route: 回傳可否直接正取 (True / False)
    
    alt 尚有名額
        Route->>Model: 建立報名紀錄 (Status = 'Confirmed')
    else 已滿額
        Route->>Model: 建立報名紀錄 (Status = 'Waitlist')
    end
    
    Model->>DB: INSERT INTO Registrations
    DB-->>Model: 寫入成功
    Model-->>Route: 報名手續完成
    
    Route-->>Browser: HTTP 302 重導向
    Browser->>User: 顯示「我的報名紀錄」頁面 (可見狀態結果)
```

## 3. 功能清單對照表

本表列出系統主要功能對應的 URL 路徑與 HTTP 方法，作為後續實作路由 (Routes) 的參考：

| 功能項目 | HTTP 方法 | URL 路徑 | 功能說明 |
| :--- | :--- | :--- | :--- |
| **首頁 / 活動列表** | GET | `/` | 顯示所有開放中的活動清單 |
| **使用者登入** | GET / POST | `/login` | 顯示登入表單與執行登入認證 |
| **使用者註冊** | GET / POST | `/register` | 顯示註冊表單與建立新帳號 |
| **建立活動表單** | GET | `/event/create` | 顯示新增活動的頁面 (需主辦方權限) |
| **送出建立活動** | POST | `/event/create` | 接收資料並將新活動寫入 SQLite |
| **活動詳細資訊** | GET | `/event/<event_id>` | 顯示特定活動的詳細內容與報名人數 |
| **報名活動** | POST | `/event/<event_id>/register` | 執行報名邏輯，系統自動判定正取或候補 |
| **取消報名** | POST | `/event/<event_id>/cancel` | 取消報名，系統將自動依序遞補候補者 |
| **報名紀錄查詢** | GET | `/my_registrations` | 查詢登入者所有報名過的活動與目前狀態 |
| **登出** | POST | `/logout` | 清除 Session 並登出當前帳號 |
