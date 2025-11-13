# CSRF 示範

Zip Download: [csrf-demo.zip](../build/csrf-demo.zip)

這是一個使用 Python 和 Docker 的簡單跨站請求偽造 (CSRF) 攻擊示範。

## 組件

- **留言板**：一個 Flask 應用程式，具有使用者帳戶和留言板。刪除帳戶功能容易受到 CSRF 攻擊，因為它沒有使用 CSRF 令牌。
- **攻擊者網站**：一個 Flask 應用程式，當已登入的使用者訪問時，會自動向留言板發送刪除使用者帳戶的請求。

## 如何運行

1. 確保已安裝 Docker 和 Docker Compose。
2. 導航到 `csrf-demo` 資料夾。
3. 運行 `docker-compose up --build`。

留言板將在 http://victim.127.0.0.1.sslip.io:6080 可用，攻擊者網站在 http://attacker.127.0.0.1.nip.io:6001。

### Important !
為了「跨站」(cross-site) 成立，兩站必須是不同「註冊型網域（eTLD+1）」。

僅用 nip.io 的兩個子網域在多數瀏覽器會被視為同一個 site，無法達到跨站。

建議做法：
- 混用兩個 wildcard DNS 服務：一個用 nip.io、另一個用 sslip.io（本專案 docker-compose 已預設這樣做）。
- 或使用 `127.0.0.1` 與 `localhost` 各自存取兩站；
- 或自行在 hosts 設定兩個完全不同的網域名稱。

## 示範步驟

1. 訪問 http://victim.127.0.0.1.sslip.io:6080 並註冊新帳戶。
2. 在留言板上發布一些訊息。
3. 在新分頁中訪問 http://attacker.127.0.0.1.nip.io:6001。這將自動嘗試通過 CSRF 刪除您的帳戶。
4. 返回 http://victim.127.0.0.1.sslip.io:6080；您應該已登出且帳戶已刪除。

注意：在真實場景中，攻擊者網站可以是任何誘騙使用者在登入易受攻擊網站時訪問的惡意網站。
