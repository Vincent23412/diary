# Node.js / Express 生產環境效能優化完整整理

## ✅ 1. 設定 NODE\_ENV 為 production

* `NODE_ENV=production` 會：

  * 快取視圖模板
  * 快取 CSS 頁面資源
  * 減少錯誤訊息細節（更輕量）
  * 效能提升最高可達 3 倍 ✅
* **設定方式**：

```ini
Environment=NODE_ENV=production
```

* **systemd 範例**：`/etc/systemd/system/my-app.service`

```ini
[Service]
Environment=NODE_ENV=production
```

## ✅ 2. 確保應用程式崩潰自動重啟

| 情境          | 解法                       |
| ----------- | ------------------------ |
| Node app 崩潰 | **pm2 或 cluster 模組重啟** ✅ |
| 系統崩潰重啟      | **systemd** 自動重啟 ✅       |

### 🎁 systemd 範例：

```ini
[Service]
Restart=always
```

## ✅ 3. 使用流程管理器與 init 系統

* **流程管理器**：pm2，可 cluster、多 process、log 管理
* **init 系統**：systemd，讓 server 重開機後 pm2 自動啟動

### pm2 + systemd 範例：

```bash
pm2 start app.js --name my-app
pm2 save
pm2 startup systemd
```

## ✅ 4. 使用 Cluster 模式

| 工具          | 說明                   |
| ----------- | -------------------- |
| cluster 模組  | Node.js 內建多核心解法 ✅    |
| pm2 cluster | 一鍵 cluster，0 程式碼變動 ✅ |

### cluster API 範例：

```js
if (cluster.isPrimary) { cluster.fork() } else { app.listen(3000) }
```

### pm2 範例：

```bash
pm2 start app.js -i max
```

## ✅ 5. 快取請求結果

| 層級  | 工具                  |
| --- | ------------------- |
| 應用層 | Redis ✅             |
| 網路層 | Nginx Proxy Cache ✅ |

### Nginx Proxy Cache 範例：

```nginx
proxy_cache_path /cache keys_zone=my_cache:10m;
location /api/ {
    proxy_cache my_cache;
    proxy_pass http://app;
}
```

## ✅ 6. 使用負載平衡器 (Load Balancer)

| 層級          | 工具               |
| ----------- | ---------------- |
| 單台多 process | Nginx upstream   |
| 多台 server   | AWS ELB, HAProxy |

### Nginx upstream 範例：

```nginx
upstream backend {
  server 127.0.0.1:3001;
  server 127.0.0.1:3002;
}
location / { proxy_pass http://backend; }
```

## ✅ 7. 使用反向代理 (Reverse Proxy)

| 功能          | 反向代理貢獻                |
| ----------- | --------------------- |
| 壓縮          | gzip ✅                |
| 快取          | proxy\_cache ✅        |
| SSL Offload | HTTPS 由 Nginx 處理 ✅    |
| 靜態檔案服務      | 直接從 Nginx 回應 JS/CSS ✅ |

### Nginx Reverse Proxy 範例：

```nginx
server {
    gzip on;
    location /api/ { proxy_pass http://localhost:3000; proxy_cache my_cache; }
    location /static/ { root /var/www/static; }
}
```

## ✅ 8. Redis vs Nginx Cache 差異

| 特點    | Redis        | Nginx Cache   |
| ----- | ------------ | ------------- |
| 運作層級  | 應用層          | 網路層 ✅         |
| 粒度    | 單筆資料快取       | 整頁快取 ✅        |
| 個人化支援 | ✅ 適合個人化資料    | ❌ 不適合個人化頁面    |
| 常見用途  | 排行榜、API 查詢快取 | 熱門首頁、靜態頁面快取 ✅ |

## ✅ 9. ElastiCache vs EC2 自架 Redis

| 比較  | ElastiCache            | EC2 Redis   |
| --- | ---------------------- | ----------- |
| 維運  | AWS 託管 ✅               | 自己裝、維運 ❌    |
| HA  | Multi-AZ、自動 failover ✅ | 自己設計        |
| 擴展性 | Redis Cluster ✅        | 自己搭 cluster |
| 用法  | 跟本機 Redis 完全一樣 ✅       | 本機 Redis 用法 |

---

📌 **完整最佳實踐：**

> Node.js 應用：pm2 cluster ➡️ systemd 託管 ➡️ Nginx Proxy (壓縮 + 快取 + 分流) ➡️ Redis 輔助應用層快取 ➡️ AWS ELB 或 HAProxy 分流多台實例 ✅
