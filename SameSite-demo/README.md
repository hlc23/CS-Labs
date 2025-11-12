# SameSite Cookie 示範

這個實驗示範 SameSite Cookie 不同設定（Lax、Strict、None）對跨站請求是否會自動夾帶 Cookie 的影響。

組成：
- Victim：會設定登入 Cookie，並提供受保護的 `/transfer` 與像素 `/pixel`。
- Attacker：提供三種跨站觸發方式：
  1) 以表單自動發送 POST（頂層導覽），
  2) 以表單自動發送 GET（頂層導覽），
  3) 以 `<img>` 載入子資源。

> 注意：現代瀏覽器要求 SameSite=None 必須搭配 Secure，且在 HTTPS 下才會被接受。此示範預設為 HTTP 可直接觀察 Lax 與 Strict 差異；若要觀察 None，請參考下方「進階：啟用 HTTPS」說明。

## 如何運行

1. 確保已安裝 Docker 與 Docker Compose。
2. 在此資料夾執行：

```powershell
docker-compose up --build
```

3. 開啟（HTTP 預設）：
  - Victim: http://victim.127.0.0.1.sslip.io:6080
  - Attacker: http://attacker.127.0.0.1.nip.io:6001

### Important !
為了「跨站」(cross-site) 成立，兩站必須是不同「註冊型網域（eTLD+1）」。

僅用 nip.io 的兩個子網域（例如 `victim.127.0.0.1.nip.io` 與 `attacker.127.0.0.1.nip.io`）在多數瀏覽器會被視為同一個 site，無法達到跨站。

建議做法：
- 混用兩個 wildcard DNS 服務：一個用 nip.io、另一個用 sslip.io（本專案 docker-compose 已預設這樣做）。
- 或使用 `127.0.0.1` 與 `localhost` 各自存取兩站；
- 或自行在 hosts 設定兩個完全不同的網域名稱。

## 操作步驟

1. 先到 Victim，按「Login」設定 Cookie。
2. 在 Victim 頁面切換 SameSite 模式（Lax / Strict / None）。
3. 到 Attacker 頁面依序測試三種攻擊：
   - 「Launch POST attack」：跨站 POST 導覽到 `/transfer`。
   - 「Launch GET navigation」：跨站 GET 導覽到 `/transfer`。
   - 「Load pixel」：跨站以 `<img>` 載入 `/pixel`，頁面會以 onload/onerror 顯示是否成功（代表 Cookie 是否被送出）。

### 預期結果（HTTP 情境）
- SameSite=Lax（預設）：
  - GET 頂層導覽：Cookie 會送出（成功）。
  - POST 頂層導覽：Cookie 不會送出（失敗）。
  - 子資源（IMG）：Cookie 不會送出（失敗）。
- SameSite=Strict：
  - 無論 GET/POST 或子資源，跨站都不會送出 Cookie（全部失敗）。
- SameSite=None：
  - 在 HTTP 下，現代瀏覽器通常會拒絕沒有 Secure 的 None Cookie，行為可能等同無 Cookie（失敗）。

## 進階：啟用 HTTPS 觀察 SameSite=None

若要完整觀察 SameSite=None 行為，需滿足：
- Cookie 需附加 `Secure`；
- 透過 HTTPS 存取 Victim 與 Attacker；
- 兩站需屬不同「site」（不同註冊型網域）。

簡化選項：
- 使用自簽憑證反向代理（例如 Nginx/Traefik）或在瀏覽器信任自簽根憑證；
- 建立 hosts 對應（例如將 `victim.lab`、`attacker.lab` 指到 127.0.0.1），確保為跨站；
- 將 Victim 以 HTTPS 服務，Victim 在選擇 `None` 時已自動以 `Secure` 設定 Cookie。

提示：若想在本地用 nip.io/sslip.io 加上 HTTPS，可考慮安裝 mkcert 產生對應 FQDN 的憑證，或在容器前使用反向代理處理 TLS（需將瀏覽器信任根憑證）。

目前預設仍為 HTTP，足以觀察 Lax/Strict；要觀察 None，請依上方方式加上 HTTPS。

本示範已在程式中於 `mode=None` 時將 Cookie 的 `secure=True`，其餘模式為 `secure=False`。若要真的驗證 None，請自行加上 HTTPS 端點或反向代理。

## 檔案結構
- `victim/`：Flask 受害者網站（設定登入 Cookie、受保護資源）
- `attacker/`：Flask 攻擊者網站（觸發跨站請求）
- `docker-compose.yml`：啟動兩個服務

## 疑難排解
- 看不到差異？請先在 Victim 按下 Login 以設定 Cookie。
- 若瀏覽器套用了更嚴格的試驗旗標，SameSite 行為可能不同。
- 要測 `None`，務必改用 HTTPS，確保 `Secure` Cookie 能被接受並送出。
