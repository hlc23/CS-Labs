# SSRF to RCE Lab

這個實驗示範「對外可控的 URL 抓取功能」(SSRF) 如何被用來呼叫僅限內網的管理 API，並最終導致遠端命令執行 (RCE)。

## 架構
- `victim` (5000/tcp): 對外提供「抓取任意 URL」的功能，存在 SSRF 弱點。
- `admin` (僅內網 5001/tcp): 內網管理服務，提供看似無害但可注入的端點 `/admin/ping?host=...`（命令注入），不對外開放。

預期攻擊流程：攻擊者將 `http://admin:5001/admin/run?cmd=...` 傳給 victim 的抓取功能，victim 會在伺服器端發出 HTTP 請求打到內網 `admin`，觸發指令執行並回傳結果。

## 快速開始

1) 啟動環境
```powershell
cd "c:\Users\lee\Documents\GitHub\CS-Labs\SSRF-to-RCE"
docker compose up -d --build
```

2) 確認服務
- Victim: http://localhost:5000/
- Admin 僅在 Docker 內網可見，無對外連接埠

3) 正常行為測試
- 在 Victim 頁面輸入 `http://example.com`，Victim 會直接回傳並渲染上游頁面（代理顯示）。

4) SSRF → RCE 利用
- 基本保護已加入，但僅檢查「初始 URL」，若先造訪可外部到達的網址，再由該站回傳 30x 跳轉到內網 `admin`，Victim 仍會跟隨跳轉（繞過檢查）。
- 目標端點（命令注入）範例：
```
http://admin:5001/admin/ping?host=1.1.1.1;id
```
- 若你手上有一個能 302 到上述內網 URL 的外部跳轉連結，把該「外部 URL」貼到 Victim，即可 SSRF → 命令注入 → RCE。

範例繞過思路（若你有一個可控制跳轉的外部站）：
```
https://你的外部站/redirect?to=http://admin:5001/admin/ping?host=1.1.1.1;id
```
Victim 只檢查最初 `https://你的外部站/...`，接著會跟隨 302 到內網 `admin`，於 `ping` 指令中注入 `; id`，達成 SSRF→RCE。

5) 關閉環境
```powershell
docker compose down -v
```

## 重點說明
- 這是教學用途的「刻意不安全」環境，請勿對外暴露。
- SSRF 防禦方向（僅供參考）：
  - 嚴格目的地 allowlist（僅允許明確、必要的主機/服務）。
  - 阻擋內網網段、Docker 服務名稱解析、metadata 服務等敏感目標。
  - 以非同步離線抓取、內容代理、URL 正規化與 IP 解析後再檢查。
  - 內網管理 API 移除危險動作或加入嚴格身份驗證與網路隔離。

## 目錄
- `victim_fetcher/`: Victim 抓取服務（Flask）
- `victim_admin/`: 內網管理服務（Flask，提供 RCE 端點）
- `docker-compose.yml`: 兩服務編排