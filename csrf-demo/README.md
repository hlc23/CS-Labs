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

留言板將在 http://localhost:5000 可用，攻擊者網站在 http://localhost:5001。

## 示範步驟

1. 訪問 http://localhost:5000 並註冊新帳戶。
2. 在留言板上發布一些訊息。
3. 在新分頁中訪問 http://localhost:5001。這將自動嘗試通過 CSRF 刪除您的帳戶。
4. 返回 http://localhost:5000；您應該已登出且帳戶已刪除。

注意：在真實場景中，攻擊者網站可以是任何誘騙使用者在登入易受攻擊網站時訪問的惡意網站。
