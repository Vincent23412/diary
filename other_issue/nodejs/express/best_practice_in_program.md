以下是完整整理的 Express 生產環境最佳實踐筆記，包含 Gzip 壓縮、同步非同步使用、日誌記錄、例外處理，搭配你剛剛問的 req.locals 補充說明：

---

# Node.js Express 生產環境最佳實踐整理

## 1️⃣ Gzip 壓縮：減少流量、提升速度

### ✅ 概念

* Gzip 壓縮可顯著減少回應體積，提升 Web 和 API 響應速度。

### ✅ Express 實作

```javascript
const compression = require('compression');
const express = require('express');
const app = express();

app.use(compression());
```

### ✅ 生產環境推薦做法

* 高流量網站建議交給 Nginx 處理 Gzip：

```nginx
gzip on;
gzip_types text/plain application/json text/css application/javascript;
```

---

## 2️⃣ 避免同步函數：保持非同步、避免堵塞

### ✅ 核心概念

* 同步函數（例如 `fs.readFileSync()`）會阻塞整個事件迴圈，影響效能。
* 在 **非同步為主的 Node.js** 環境，應該盡可能避免同步操作。

### ✅ 開發檢查方法

```bash
node --trace-sync-io app.js
```

* 使用該指令可追蹤同步 API 使用位置。

### ✅ 正確做法

* **只在啟動時用同步 API**（例如讀取設定檔）。
* **非同步為主**：

```javascript
const fs = require('fs/promises');
const data = await fs.readFile('./test.txt', 'utf-8');
```

---

## 3️⃣ 正確日誌記錄：區分除錯 log 與活動 log

### ✅ 常見問題

* `console.log()`、`console.error()` 是同步的，不建議用於高併發生產環境。

### ✅ 推薦方案

| 用途   | 工具      | 說明                           |
| ---- | ------- | ---------------------------- |
| 除錯   | `debug` | 開發用除錯 log，不影響正式環境            |
| 活動日誌 | `pino`  | 高效能非同步 log，支援 log 等級、JSON 輸出 |

### ✅ Debug 使用方式

```javascript
const debug = require('debug')('app:api');
debug('API called');
```

執行：

```bash
$env:DEBUG="app:*"; node app.js # Windows PowerShell
```

### ✅ Pino 使用方式

```javascript
const pino = require('pino');
const logger = pino();
logger.info('server started');
```

---

## 4️⃣ 正確例外處理：防止程式崩潰

### ✅ 核心觀念

* Node.js 不處理例外時，應用會崩潰，**正確捕捉例外是穩定性關鍵**。

### ✅ 同步錯誤處理

```javascript
app.get('/search', (req, res) => {
  setImmediate(() => {
    try {
      const json = JSON.parse(req.query.params);
      res.send('OK');
    } catch (e) {
      res.status(400).send('Invalid JSON');
    }
  });
});
```

### ✅ 非同步錯誤處理 (async/await)

```javascript
app.get('/', async (req, res, next) => {
  try {
    const data = await userData();
    res.send(data);
  } catch (err) {
    next(err);
  }
});
```

全局錯誤處理中間件：

```javascript
app.use((err, req, res, next) => {
  res.status(err.status ?? 500).send({ error: err.message });
});
```

---

## 5️⃣ req.locals 實戰用法：跨 middleware 傳遞資料

### ✅ 說明

* Express 預設有 `res.locals`，但 `req.locals` 是開發者自定義的屬性，用來在多個 middleware 傳遞資料（例如 user 資訊）。

### ✅ 範例

```javascript
app.use(async (req, res, next) => {
  req.locals = { user: await getUser(req) };
  next();
});

app.get('/', (req, res) => {
  res.json({ user: req.locals.user });
});
```

---

## 🎁 總結

| 項目         | 核心重點                                      |
| ---------- | ----------------------------------------- |
| Gzip 壓縮    | Express 小專案用 `compression()`，大專案建議用 Nginx |
| 避免同步       | 生產環境應盡可能全非同步；用 `--trace-sync-io` 查漏       |
| 日誌記錄       | `debug` 控制除錯 log，`pino` 處理正式日誌            |
| 例外處理       | sync 用 try-catch，async 用 `next(err)`      |
| req.locals | 用來跨 middleware 存取 user、traceId 等資訊        |

---
