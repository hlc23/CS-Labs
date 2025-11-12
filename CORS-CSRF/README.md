# JSON-based CSRF Lab

## Challenge 
Send api request with JSON body from attacker to victim server.
And show the response from victim server.

## 設置
1. 運行 `docker-compose up --build` 啟動服務。
2. Victim API 在 http://localhost:8080
3. Attacker 上傳服務器在 http://localhost:8081

## 攻擊演示
1. 訪問 http://localhost:8081 上傳 payload.html（已預置在 payloads/ 文件夾）。
2. 打開上傳的 payload 頁面。
3. 點擊 "Send CSRF Request" 按鈕。
4. 觀察請求成功，因為 CORS 允許跨域 JSON POST。