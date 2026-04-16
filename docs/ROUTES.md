# 祈福與算命占卜系統 - 路由設計 (Routing Design)

## 1. 路由規劃表 (Route Table)

| HTTP 方法 | URL 路徑 | Blueprint | 對應功能描述 | 對應模板視圖 (Template) |
|---|---|---|---|---|
| GET | `/` | `divination` | 系統首頁 (展示各類占卜功能卡片) | `divination/index.html` |
| GET / POST | `/auth/register` | `auth` | 會員註冊 | `auth/register.html` |
| GET / POST | `/auth/login` | `auth` | 會員登入 | `auth/login.html` |
| GET | `/auth/logout` | `auth` | 會員登出 | *重導向至首頁* |
| GET | `/divination/temple` | `divination` | 觀音靈籤/傳統廟宇抽籤頁面 | `divination/temple_draw.html` |
| POST | `/divination/temple` | `divination` | 處理抽籤與擲筊結果，儲存至 DB | *重新導向至結果頁* |
| GET | `/divination/tarot` | `divination` | 塔羅牌單張占卜頁面 | `divination/tarot_draw.html` |
| POST | `/divination/tarot` | `divination` | 處理塔羅牌抽牌結果，儲存至 DB | *重新導向至結果頁* |
| GET | `/divination/result/<id>` | `divination` | 查看專屬占卜結果與解析 | `divination/result.html` |
| GET | `/divination/history` | `divination` | 會員個人專屬占卜歷史紀錄 | `divination/history.html` |
| GET | `/donation/` | `donation` | 線上隨喜捐獻/捐香油錢表單 | `donation/donate.html` |
| POST | `/donation/process` | `donation` | 處理金流邏輯 (MVP先寫入DB) | *重導向至捐獻成功感謝頁* |
| GET | `/donation/thanks` | `donation` | 捐獻成功感謝狀展示 | `donation/thanks.html` |
