# Node.js 事件迴圈與任務分類總整理

## 🔁 事件迴圈的 6 個階段（每一輪都會跑一次）

1. **timers**
   - 執行 `setTimeout`、`setInterval` 到期的回呼

2. **pending callbacks**
   - 處理某些 I/O 回呼（暫存回呼）

3. **idle, prepare**
   - 僅內部使用（你可以忽略）

4. **poll**
   - 等待新的 I/O 事件，並執行對應的 I/O 回呼（如 `fs.readFile`）
   - 沒有待處理 I/O 時，會嘗試移動到下一階段

5. **check**
   - 執行 `setImmediate` 的回呼

6. **close callbacks**
   - 處理如 `socket.on('close')` 的回呼

---

## 🔸 微任務（microtask）

- **定義：** 每個階段執行結束後，會「立刻執行」的任務
- **常見來源：**
  - `Promise.then/catch/finally`
  - `queueMicrotask`

📌 在每個階段「**結束前**」都會清空微任務佇列（queue）

---

## 🔹 宏任務（macrotask）

- **定義：** 被排入事件迴圈各階段的回呼
- **常見類型（依據所屬階段分類）：**

| 階段         | 任務類型                    | 範例                                      |
|--------------|-----------------------------|-------------------------------------------|
| timers       | `setTimeout`, `setInterval` | `setTimeout(fn, 0)`                       |
| poll         | I/O 回呼                    | `fs.readFile`, `net`, `HTTP` 等           |
| check        | `setImmediate`              | `setImmediate(fn)`                        |
| close        | 關閉資源回呼                | `socket.on('close')`                      |

---

## 🧠 執行順序總結（每輪事件迴圈）



🔁 每一輪事件迴圈順序如下：

1. timers 階段（到期的 setTimeout / setInterval）
   → 執行微任務（microtask queue）

2. pending callbacks
   → 執行微任務

3. idle, prepare
   → 執行微任務

4. poll（I/O 回呼）
   → 執行微任務

5. check（setImmediate）
   → 執行微任務

6. close callbacks
   → 執行微任務



✅ **微任務插隊原則：**
- 每個階段執行完主邏輯後 → 會清空微任務佇列
- 所以 `Promise.then` 常常比 `setTimeout(fn, 0)` 快

---

## 🔄 特例說明：setTimeout vs setImmediate

| 執行位置      | 誰比較早印？                          | 原因                                           |
|---------------|---------------------------------------|------------------------------------------------|
| **主程式中（CommonJS）** | `setTimeout` 先                           | timers 階段在 check 前                        |
| **主程式中（ESM 模組）** | `setImmediate` 可能先                    | Node ESM 初始化後直接進入 check 階段          |
| **I/O 回呼中**           | `setImmediate` 通常會比 `setTimeout` 早印 | I/O 回呼在 poll，setImmediate 直接進入 check 階段 |

---

## 📌 小結重點筆記

- `setTimeout(fn, 0)` ≠ 立即執行，它會排到下一輪的 `timers` 階段
- `Promise.then()` 是微任務，會「插隊」在同一輪階段結束時執行
- `setImmediate()` 排到 `check` 階段，**常常在 I/O 回呼後立即執行**
- **ESM 模組與 CommonJS 在事件迴圈初始化時有些差異**
# Node.js 事件迴圈與任務分類總整理

## 🔁 事件迴圈的 6 個階段（每一輪都會跑一次）

1. **timers**
   - 執行 `setTimeout`、`setInterval` 到期的回呼

2. **pending callbacks**
   - 處理某些 I/O 回呼（暫存回呼）

3. **idle, prepare**
   - 僅內部使用（你可以忽略）

4. **poll**
   - 等待新的 I/O 事件，並執行對應的 I/O 回呼（如 `fs.readFile`）
   - 沒有待處理 I/O 時，會嘗試移動到下一階段

5. **check**
   - 執行 `setImmediate` 的回呼

6. **close callbacks**
   - 處理如 `socket.on('close')` 的回呼

---

## 🔸 微任務（microtask）

- **定義：** 每個階段執行結束後，會「立刻執行」的任務
- **常見來源：**
  - `Promise.then/catch/finally`
  - `queueMicrotask`

📌 在每個階段「**結束前**」都會清空微任務佇列（queue）

---

## 🔹 宏任務（macrotask）

- **定義：** 被排入事件迴圈各階段的回呼
- **常見類型（依據所屬階段分類）：**

| 階段         | 任務類型                    | 範例                                      |
|--------------|-----------------------------|-------------------------------------------|
| timers       | `setTimeout`, `setInterval` | `setTimeout(fn, 0)`                       |
| poll         | I/O 回呼                    | `fs.readFile`, `net`, `HTTP` 等           |
| check        | `setImmediate`              | `setImmediate(fn)`                        |
| close        | 關閉資源回呼                | `socket.on('close')`                      |

---

## 🧠 執行順序總結（每輪事件迴圈）



🔁 每一輪事件迴圈順序如下：

1. timers 階段（到期的 setTimeout / setInterval）
   → 執行微任務（microtask queue）

2. pending callbacks
   → 執行微任務

3. idle, prepare
   → 執行微任務

4. poll（I/O 回呼）
   → 執行微任務

5. check（setImmediate）
   → 執行微任務

6. close callbacks
   → 執行微任務



✅ **微任務插隊原則：**
- 每個階段執行完主邏輯後 → 會清空微任務佇列
- 所以 `Promise.then` 常常比 `setTimeout(fn, 0)` 快

---

## 🔄 特例說明：setTimeout vs setImmediate

| 執行位置      | 誰比較早印？                          | 原因                                           |
|---------------|---------------------------------------|------------------------------------------------|
| **主程式中（CommonJS）** | `setTimeout` 先                           | timers 階段在 check 前                        |
| **主程式中（ESM 模組）** | `setImmediate` 可能先                    | Node ESM 初始化後直接進入 check 階段          |
| **I/O 回呼中**           | `setImmediate` 通常會比 `setTimeout` 早印 | I/O 回呼在 poll，setImmediate 直接進入 check 階段 |

---

## 📌 小結重點筆記

- `setTimeout(fn, 0)` ≠ 立即執行，它會排到下一輪的 `timers` 階段
- `Promise.then()` 是微任務，會「插隊」在同一輪階段結束時執行
- `setImmediate()` 排到 `check` 階段，**常常在 I/O 回呼後立即執行**
- **ESM 模組與 CommonJS 在事件迴圈初始化時有些差異**
