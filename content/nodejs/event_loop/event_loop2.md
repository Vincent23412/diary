# 🧠 Node.js 事件迴圈筆記總整理

## 📍 基本概念

Node.js 的事件迴圈（Event Loop）是非同步架構的核心，負責協調各種非同步任務的執行順序。每一輪事件迴圈稱為一個 **tick**，每個 tick 包含多個階段（phases）。

---

## 📊 事件迴圈階段（簡化版）

| 階段名稱             | 說明與用途                                     |
| ---------------- | ----------------------------------------- |
| **timers**       | 執行到期的 `setTimeout()` 和 `setInterval()` 回呼 |
| **pending**      | 某些錯誤延遲回呼（很少使用）                            |
| **idle/prepare** | Node.js 內部用                               |
| **poll**         | 等待 I/O 事件、執行 I/O 回呼（如 `fs.readFile`）      |
| **check**        | 執行 `setImmediate()`                       |
| **close**        | 執行 `close` 事件回呼（如 socket 被銷毀）             |

---

## 🧵 特殊機制（非屬於事件迴圈階段）

| 類型                                                    | 執行時機說明                       |
| ----------------------------------------------------- | ---------------------------- |
| `process.nextTick()`                                  | 在 **當前事件循環階段完成前** 執行（優先）     |
| **Microtasks**（如 `Promise.then()`、`queueMicrotask()`） | 在事件循環階段結束後執行，但比 macrotask 更早 |

---

## 🔼 任務優先順序（從快到慢）

1. `process.nextTick()` ✅（最高優先）
2. `Promise.then()` / `queueMicrotask()`（microtask queue）
3. `setTimeout(fn, 0)`（下一輪 timers 階段）
4. `setImmediate()`（下一輪 check 階段）

---

## 🔧 比較總表

| 特性           | `process.nextTick()` | `Promise.then()` | `setTimeout()`     | `setImmediate()`  |
| ------------ | -------------------- | ---------------- | ------------------ | ----------------- |
| 是否 microtask | ❌（特殊 queue）          | ✅ microtask      | ❌ macrotask        | ❌ macrotask       |
| 執行時機         | 當前 call stack 清空後    | microtask 隊列     | 下一輪事件循環的 timers 階段 | 下一輪事件循環的 check 階段 |
| 穩定性          | 會造成 starvation，請小心使用 | 穩定               | 容易延遲               | ✅ I/O 後推薦使用       |
| 適用場景         | 錯誤回傳、保證 callback 非同步 | 非同步流程控制          | 一般延遲               | I/O 回呼後的後續邏輯      |

---

## 🧪 例子解析

### 1️⃣ `nextTick` 與 `setImmediate` 比較：

```ts
process.nextTick(() => console.log("nextTick"));
setImmediate(() => console.log("setImmediate"));
```

➡️ 輸出順序：

```
nextTick
setImmediate
```

---

### 2️⃣ 建構函數中觸發事件（要延遲執行）

```ts
class MyEmitter extends EventEmitter {
  constructor() {
    super();
    process.nextTick(() => {
      this.emit('ready');
    });
  }
}
```

➡️ 確保使用者 `.on('ready')` 有時間註冊

---

### 3️⃣ I/O 中使用 `setImmediate`

```ts
fs.readFile(__filename, () => {
  setImmediate(() => console.log("immediate"));  // ✅ 穩定
  setTimeout(() => console.log("timeout"), 0);   // ❌ 時機可能延遲
});
```

➡️ `setImmediate` 比 `setTimeout(..., 0)` 更穩定地在 I/O 後執行

---

## ⚠️ 潛在問題：Starvation（飢餓）

```ts
function loop() {
  process.nextTick(loop);  // ❌ 無限卡在 nextTick queue，其他任務無法執行
}
loop();
```

➡️ 永遠無法進入下一階段 → ❌ I/O 無法觸發，效能被鎖死

---

## ✅ 最佳實務總結

| 你要做什麼？                        | 使用哪個？                            |
| ----------------------------- | -------------------------------- |
| 確保 callback 非同步、回傳錯誤前給使用者機會處理 | `process.nextTick()`             |
| 在 async 流程中排 microtask        | `Promise.then()` / `await`       |
| 處理 I/O 完後的任務                  | `setImmediate()`                 |
| 做定時排程                         | `setTimeout()` 或 `setInterval()` |

---

