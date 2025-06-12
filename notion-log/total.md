# 2025-06-12 筆記

## 設計安全的工作附載和應用程式

### 🛡️ 防火牆與存取路徑設計

- 使用者的存取請求需經過兩道防線：

### 🌍 地端與雲端設計三大原則

隔離性（Isolation）

連通性（Connectivity）

安全性（Security）

### 🏗️ 子網路隔離策略（Subnet Design）

- Public Subnet：

- Private Subnet：

- Protected Subnet（或稱 "Isolated"）：

### 🔐 安全設計工具與策略

### ✅ 安全設計小結

- Security Group 是 EC2 的第一道防線。

- OS 防火牆是 EC2 內部的第二道防線。

- NACL 適合用來封鎖特定 IP 或開放大範圍的進出規則。

- WAF 適合保護 Web 層，對應 OWASP Top 10 攻擊。

問題二

A：NACL保護的對象是子網
B：安全權組保護ec2裡面的網卡
C
D：細膩度不夠

### ✅ 選項 B：使用安全群組設定存取權

- 正確

- 安全群組是 狀態導向（stateful） 防火牆，適用於每個 EC2 實例

- 可為 A 設定允許 port 80，為 B 設定允許 port 443

- 可細緻控制每個實例的入站流量

### ❌ 選項 A：使用網路 ACL 設定存取權

- 錯誤

- NACL 是 子網層級 的 stateless 防火牆

- 無法分辨子網內不同 EC2 實例的特定流量

- 若允許 port 80，則 B 無法阻擋；若允許 port 443，則 A 會被擋

- 無法同時達成 A、B 的不同流量控制需求

### ❌ 選項 C：使用 VPC 對等互連設定網路連線

- 與本題無關

- 用於 跨 VPC 連線，不解決流量過濾問題

### ❌ 選項 D：使用路由表設定網路連線

- 路由表是用來設定目的地網段的轉送

- 無法控制 port 或協定層級的存取權限

# 🧩 TypeScript + Yarn Workspace 問題整理

## 📁 專案架構

root/
├── package.json        # 設定 workspaces
├── tsconfig.json       # (可選) root tsconfig
├── server/             # 子專案 1
│   ├── package.json
│   └── src/
└── utils/              # 子專案 2 (被 server 引用)
    ├── package.json
    └── src/


## 🔧 問題 1：yarn dev 出現錯誤

### 錯誤訊息：

error Couldn't find a package.json file in "C:\\Users\\xxx\\Documents\\GitHub"


### 成因：

你在 root 專案中執行 yarn dev，但該資料夾沒有 package.json，無法辨識該命令。

### 解法：

- 確保 根目錄有一個 package.json，並定義好 workspaces，例如：

{
  "private": true,
  "workspaces": ["server", "utils"]
}


- 然後進入對應子專案執行指令：

cd server
yarn dev


## ⚠️ 問題 2：[DEP0128] Invalid 'main' field

### 錯誤訊息：

DeprecationWarning: Invalid 'main' field in 'utils/package.json' of 'index.js'.


### 成因：

TypeScript 專案實際編譯出來的是 dist/index.js，但你在 package.json 裡面寫的是：

"main": "index.js"  ❌


### 解法：

改成指向編譯後的檔案（通常放在 dist/）：

"main": "dist/index.js"
"types": "dist/index.d.ts" // 如果有型別檔的話


## ❓ 問題 3：使用 TS 開發時 main 寫錯不報錯？

### 原因：

TS 編譯不會檢查 package.json 的 main 欄位。只有當：

- 其他專案 import 該 module

- 或打包 / 執行該 module

時，Node 才會去解析 main。

## 📄 問題 4：什麼是型別檔？缺少型別檔會怎樣？

### 型別檔 .d.ts 的作用：

- 告訴 TS 編譯器「某個模組有哪些 API 和型別」

- 提供自動補全、錯誤提示、編譯安全性

### 沒有型別檔會導致：

- TS7016: Could not find a declaration file for module 'xxx'

- 編譯器把該模組推斷為 any

- 失去補全與靜態檢查，易出錯

## ✅ 建議工作流程（TS + Workspace）：

在 root 專案執行：

加入 package.json 中的 workspace 設定：

在每個子專案中執行：

在每個子專案執行：

設定 main、types 為 dist/ 資料夾：

編譯一次，生成型別檔：

---
# 2025-06-05 筆記

# 🛠️ TypeScript 開發過程問題整理筆記

## 1. ❌ ERR_UNKNOWN_FILE_EXTENSION: ".ts"

### 問題描述

使用 Node.js 執行 .ts 檔案會出現錯誤：

TypeError [ERR_UNKNOWN_FILE_EXTENSION]: Unknown file extension ".ts"


### 原因

Node.js 不支援直接執行 TypeScript (.ts) 檔案。

### 解法

### ✅ 方法一：使用 ts-node

yarn add -D ts-node typescript
npx ts-node src/index.ts


### ✅ 方法二：使用 tsx（推薦）

yarn add -D tsx typescript
npx tsx src/index.ts


### ✅ 方法三：先編譯再執行

npx tsc     # 編譯 ts -> js
node dist/index.js


## 2. ❌ 錯誤的 yarn 安裝指令

### 錯誤指令

yarn -i --save-dev @types/express


### 正確用法

yarn add -D @types/express


## 3. ❓ 是否可以使用 .tsx 作為執行工具？

### 回答

✅ 是的，這裡的 tsx 是指一個快速執行 TypeScript 的工具（esbuild-kit/tsx），它支援 .ts 和 .tsx 執行，且效能比 ts-node 更好。

### 安裝與使用

yarn add -D tsx
npx tsx src/index.ts


## 4. ✅ 使用 nodemon 搭配 TypeScript

### 安裝方式

yarn add -D nodemon tsx typescript


### 建立 nodemon.json

{
  "watch": ["src"],
  "ext": "ts",
  "exec": "tsx src/index.ts"
}


### package.json script

"scripts": {
  "dev": "nodemon"
}


### 執行方式

yarn dev


# 🧠 TypeScript 套件型別筆記（@types）

## ✅ 為什麼需要型別定義？

- TypeScript 是靜態型別語言，需要知道每個函式與物件的「型別」才能正確編譯。

- 有些 JavaScript 套件（如 express、ws）沒有內建型別資訊，所以 TypeScript 需要額外的型別定義檔案來理解它們。

## 🔍 如何判斷一個套件是否需要安裝 @types/xxx？

### ✅ 不需要安裝（內建型別）

這些套件本身就支援 TypeScript，安裝主套件即可。

- 判斷方法：

### 範例：

yarn add axios         # ✅ 不需要 @types/axios
yarn add dayjs         # ✅ 不需要 @types/dayjs


### ❌ 需要安裝 @types/xxx

這些是 JavaScript 套件，沒有型別描述，要透過社群提供的 DefinitelyTyped 安裝型別。

- 安裝方式：

yarn add lodash
yarn add -D @types/lodash


- D 代表開發階段使用（devDependencies）

### 常見範例：

## 🛠 快速判斷方式

### 方法一：用 yarn 查型別支援

yarn info axios types       # ✅ 有型別 => 不需額外安裝
yarn info express types     # ❌ 無型別 => 需要 @types/express


### 方法二：查 npm 頁面說明

- 搜尋關鍵字 typescript support 或 types

- 看是否提到型別內建、還是需要另外安裝

## 🧾 小提醒

- 型別定義只在 開發階段使用，所以應放在 devDependencies

- 如果你部署後還會用 ts-node 直接執行 .ts 檔，這時 @types/xxx 可能需要進 dependencies

# 🧠 TypeScript / Node.js 開發筆記：Port 被佔用 & app vs server 差異

## 🔧 一、當 Port 被佔用時怎麼辦？

### ✅ 問題描述：

當你啟動伺服器時出現錯誤：

Error: listen EADDRINUSE: address already in use 127.0.0.1:3000


表示 3000 port 已被其他程式佔用。

### ✅ 解法步驟：

### 1️⃣ 查出是誰佔用了該 port

### Windows：

netstat -ano | findstr :3000


會看到一行類似這樣的結果，最後的數字是 PID：

TCP    127.0.0.1:3000     0.0.0.0:0     LISTENING     12345


### macOS / Linux：

lsof -i :3000


### 2️⃣ 終止該程式（使用 PID）

### Windows：

taskkill /PID 12345 /F


### macOS / Linux：

kill -9 12345


### 3️⃣ 或改用其他 port（開發中建議）

const PORT = process.env.PORT || 3001;
server.listen(PORT);


啟動時改用不同 port：

PORT=3001 yarn dev


## 🚦 二、Express 中 app 和 server 的差異

### ✅ app 是什麼？

- app = express();

---
# 2025-06-03 筆記

# GitHub Actions 問題筆記

### 📌 問題一：Docker container 每次都重新安裝依賴（如 Go modules）

## 現象


在 GitHub Actions 的 CI/CD pipeline 中，後端服務使用 `go run` 或 `go build` 指令執行時，Go modules 每次都會重新下載，導致 workflow 時間變長。

## 解決方案


- 使用 [actions/cache](https://github.com/actions/cache) 儲存 `$GOPATH/pkg/mod` 和 `go.sum` 的快取。

 範例：


  - name: Cache Go modules
    uses: actions/cache@v3
    with:
      path: |
        ~/.cache/go-build
        ~/go/pkg/mod
      key: ${{ runner.os }}-go-${{ hashFiles('**/go.sum') }}
      restore-keys: |
        ${{ runner.os }}-go-


## 📌 問題二：Docker Compose 執行失敗或找不到 volume 目錄

### 現象

在 GitHub Actions 執行 docker-compose up 時出現 volume mount 錯誤，或報錯找不到某些目錄。

### 解決方案

- 確保專案資料夾結構正確，並且所有 volume 指的資料夾（如 ./pgadmin）在 repo 中存在，否則預設會掛載空資料夾。

- 若為暫時資料，可考慮使用 ephemeral volume，例如：

## 📌 問題三：Container 啟動但無法連線（如 ECONNREFUSED）

### 現象

前端在 proxy API 時無法連到後端，如 connect ECONNREFUSED 或 getaddrinfo ENOTFOUND dashboard-be

### 解決方案

- 確認 docker-compose.yml 中的 container name、port 和 service name 是否一致。

- 在本地開發時，若手動啟動某些服務，建議使用 Docker network 檢查連線：

## 📌 問題四：pgAdmin 儲存目錄無權限或未掛載成功

### 現象

啟動 pgAdmin container 後，發現設定無法保存，或資料夾權限錯誤。

### 解決方案

- 掛載的本機目錄需確保擁有者為容器中的 pgadmin 用戶（通常為 UID 5050）

- 使用以下指令修正權限：

## 📌 備註

- 每次部署完可用 docker compose down 清掉服務，但記得資料 volume 若沒保留會清空資料。

- 若 workflow 卡住建議加上 debug log 或使用 -verbose 查原因。

# 📘 GitHub Actions 常見錯誤與解法整理

## 📦 任務背景

透過 GitHub Actions 自動執行 sync_notion.py 並將每日筆記推送到 GitHub 上，常見錯誤如下：

## 🚫 Permission denied to github-actions[bot]

### ❗ 錯誤訊息：

remote: Permission to <repo>.git denied to github-actions[bot].
fatal: unable to access 'https://github.com/<repo>.git/': The requested URL returned error: 403


### ✅ 原因與解法：

- 原因：預設 github-actions[bot] 無權 push 到私人或特定 repo。

- 解法：建立 Personal Access Token（PAT），並新增為 secrets：

## 🔁 Updates were rejected because the remote contains work

### ❗ 錯誤訊息：

Updates were rejected because the remote contains work that you do not have locally.

### ✅ 原因與解法：

- 原因：遠端分支有更新，但本地分支尚未同步。

- 解法 1：若可接受覆蓋：

- 解法 2：若需保留遠端變更：

## 🧪 No upstream branch

### ❗ 錯誤訊息：

fatal: The current branch main has no upstream branch.

### ✅ 解法：

git push --set-upstream origin main

## 🔐 無法驗證 remote URL 有套用 Token

### 🔍 驗證方法：

git remote -v


正確結果應類似：

origin  https://x-access-token:<GH_PAT>@github.com/<user>/<repo> (fetch)
origin  https://x-access-token:<GH_PAT>@github.com/<user>/<repo> (push)


## 🔑 Token 開頭格式

- Fine-grained Token 一般為 github_pat_ 開頭，這是正常的。

- 若格式為 ghp_ 則為 classic token。

## 🔍 Debug 建議

你可以安全印出部分變數值協助 debug：

echo "GH_PAT starts with: ${GH_PAT:0:6}******"
echo "REPO is $GITHUB_REPOSITORY"


## ✅ 建議做法：重設 Remote + Force Push

git remote remove origin
git remote add origin https://x-access-token:${GH_PAT}@github.com/${GITHUB_REPOSITORY}
git push origin main --force


## 🧠 補充建議

- 強制 push 風險高，建議 每日筆記記錄專用 branch 使用。

- 若要避免 force，可在 CI 加入 git pull --rebase 或 fetch 再比對。

---
# 2025-06-01 筆記

待辦：

處理沒辦法重複上傳的問題

寫筆記

---
# 2025-05-30 筆記

# 5/30

# 📦 SCP 與解壓縮筆記整理

## 📁 壓縮與解壓縮指令

### `.tar.gz` 壓縮：

將資料夾壓縮成 `.tar.gz` 檔案：

tar -czvf output.tar.gz your_folder_name

- `-c`：建立壓縮檔  
- `-z`：透過 gzip 壓縮  
- `-v`：顯示過程資訊（可省略）  
- `-f`：指定壓縮檔名稱  

---

### `.tar.gz` 解壓縮：

tar -xzvf file.tar.gz

---

## 📤 SCP 傳輸指令

### ✅ 本機上傳到遠端：

scp -i your-key.pem /path/to/local/file ec2-user@<IP>:/path/to/remote/dir

- `-i`：指定 pem 憑證檔  
- `file`：要上傳的本地檔案  
- `ec2-user@<IP>`：遠端使用者與 IP  
- `:/path/...`：遠端目的地路徑  

---

### ✅ 遠端下載到本機：

scp -i your-key.pem ec2-user@<IP>:/path/to/remote/file /path/to/local/dir

---

### ✅ 遞迴傳整個資料夾：

scp -i your-key.pem -r ec2-user@<IP>:/remote/folder /local/folder

- `-r`：遞迴傳輸整個資料夾

---

## ⚠️ 常見錯誤與解法

🔒 Permissions 0644 for 'your-key.pem' are too open

chmod 400 your-key.pem

原因：`.pem` 檔權限過開，需限制為只有自己可讀。

---

❌ No such file or directory

原因：檔案或路徑名稱打錯，請確認路徑是否存在。

---

❗ SCP 下載時本地資料夾不存在

mkdir -p /path/to/local/dir

---

## 🧠 備註

- `.tar.gz` 是 tar 與 gzip 結合的格式，常用於 Linux 資料打包  
- SCP 基於 SSH，適合快速傳輸安全檔案，不適合大量資料（可考慮 rsync）

---
# 2025-05-30 筆記

# 5/30

# 📦 SCP 與解壓縮筆記整理

## 📁 壓縮與解壓縮指令

### `.tar.gz` 壓縮：

將資料夾壓縮成 `.tar.gz` 檔案：

tar -czvf output.tar.gz your_folder_name

- `-c`：建立壓縮檔  
- `-z`：透過 gzip 壓縮  
- `-v`：顯示過程資訊（可省略）  
- `-f`：指定壓縮檔名稱  

---

### `.tar.gz` 解壓縮：

tar -xzvf file.tar.gz

---

## 📤 SCP 傳輸指令

### ✅ 本機上傳到遠端：

scp -i your-key.pem /path/to/local/file ec2-user@<IP>:/path/to/remote/dir

- `-i`：指定 pem 憑證檔  
- `file`：要上傳的本地檔案  
- `ec2-user@<IP>`：遠端使用者與 IP  
- `:/path/...`：遠端目的地路徑  

---

### ✅ 遠端下載到本機：

scp -i your-key.pem ec2-user@<IP>:/path/to/remote/file /path/to/local/dir

---

### ✅ 遞迴傳整個資料夾：

scp -i your-key.pem -r ec2-user@<IP>:/remote/folder /local/folder

- `-r`：遞迴傳輸整個資料夾

---

## ⚠️ 常見錯誤與解法

🔒 Permissions 0644 for 'your-key.pem' are too open

chmod 400 your-key.pem

原因：`.pem` 檔權限過開，需限制為只有自己可讀。

---

❌ No such file or directory

原因：檔案或路徑名稱打錯，請確認路徑是否存在。

---

❗ SCP 下載時本地資料夾不存在

mkdir -p /path/to/local/dir

---

## 🧠 備註

- `.tar.gz` 是 tar 與 gzip 結合的格式，常用於 Linux 資料打包  
- SCP 基於 SSH，適合快速傳輸安全檔案，不適合大量資料（可考慮 rsync）

---
# 5/30

# SCP 與解壓縮筆記整理

## 📦 壓縮與解壓縮指令

### `.tar.gz` 壓縮：

```bash
# 將資料夾壓縮成 .tar.gz 檔案
 tar -czvf output.tar.gz your_folder_name
```

* `-c`：建立壓縮檔
* `-z`：透過 gzip 壓縮
* `-v`：顯示過程資訊（可省略）
* `-f`：指定檔名

### `.tar.gz` 解壓縮：

```bash
# 解壓縮 tar.gz
 tar -xzvf file.tar.gz
```

---

## 📤 SCP 傳輸指令

### ✅ 本機上傳到遠端：

```bash
scp -i your-key.pem /path/to/local/file ec2-user@<IP>:/path/to/remote/dir
```

* `-i`：指定 pem 憑證檔
* `file`：要上傳的本地檔案
* `ec2-user@<IP>`：遠端使用者與 IP
* `:/path/...`：遠端目的地路徑

### ✅ 遠端下載到本機：

```bash
scp -i your-key.pem ec2-user@<IP>:/path/to/remote/file /path/to/local/dir
```

### ✅ 遞迴傳整個資料夾：

```bash
scp -i your-key.pem -r ec2-user@<IP>:/remote/folder /local/folder
```

* `-r`：遞迴傳輸整個資料夾

---

## 常見錯誤與解法

### 🔒 權限錯誤：

```bash
Permissions 0644 for 'your-key.pem' are too open
```

➡ 解法：

```bash
chmod 400 your-key.pem
```

### ❌ 找不到目錄：

```bash
No such file or directory
```

➡ 檢查該路徑是否存在，或目錄拼錯。

### ❗ scp 下載時本地資料夾不存在：

➡ 解法：請確保 `/path/to/local/dir` 已存在，否則先 `mkdir` 建立。

# 5/29
# 🛠️ AWS EC2 快照（Snapshot）復原全攻略

## 📌 快照是什麼？

- 快照（Snapshot）是對 EBS 磁碟的完整區塊層級備份。
- 包含所有資料：Linux 作業系統、套件、設定檔、使用者資料等。
- 可用來：
  - **復原資料**
  - **重建系統**
  - **橫向擴展其他 EC2 機器**

---

## 🧠 快照會備份哪些內容？

| 項目                 | 是否包含 | 備註 |
|----------------------|----------|------|
| Linux 作業系統本身      | ✅        | kernel、shell、systemd |
| 已安裝的程式套件        | ✅        | 如 git、python、tmux |
| 使用者的家目錄 `/home` | ✅        | 包括資料、虛擬環境等 |
| 系統設定檔 `/etc/*`   | ✅        | SSH、時區等設定 |
| RAM 記憶體內容         | ❌        | 不包含記憶體中暫時資料 |
| 執行中的程式          | ❌        | 只保存磁碟內容，不含執行狀態 |

---

## 📦 快照如何還原？

有兩種方式：

### 方法一：掛載成資料磁碟（推薦用於讀資料或備份）

1. Snapshots → 選擇快照 → `Actions > Create Volume`
   - AZ 要與 EC2 相同
2. Volumes → `Attach Volume` 到你的 EC2
   - 裝置命名建議：`/dev/sdf`（Linux 上變成 `/dev/xvdf`）
3. SSH 進入 EC2 後掛載：
   ```bash
   lsblk
   sudo mkdir /mnt/old-data
   sudo mount /dev/xvdf1 /mnt/old-data
   ls /mnt/old-data
   ```
✅ 優點：不會干擾主系統，可用於資料檢查、復原設定等
❌ 不會啟動快照裡的作業系統（不會變成兩個 OS）

### 方法二：從快照建立 AMI → 啟動完整新機
Snapshots → Actions > Create Image

填好映像名稱（AMI）→ 建立

到 AMIs → 點選新建立的映像 → Launch 建立新 EC2

✅ 優點：整機還原原樣，OS、設定、資料都保留
✅ 可用於整機備份、異地轉移等需求

### ❓ 常見疑問
❓ 從快照建立 Volume 掛載到 EC2，會不會有兩個作業系統？
不會。

EC2 只從「根磁碟（通常是 /dev/xvda）」開機。

掛載的 Volume 即使來自完整 OS 快照，也只是「資料磁碟」。

不會主動啟用裡面的 OS，等於把舊系統當資料夾瀏覽而已。

🧭 比較表：兩種還原方式
用途	建議方式 是否會變 OS
資料還原／存取設定	掛載 Volume	❌ 否
整機重建／異地還原	建立 AMI → 新建 EC2	✅ 是
檢查舊機資料	掛載 Volume	❌ 否
快速重建環境	建立 AMI → 新建 EC2	✅ 是

🔧 附錄：相關指令參考

查看磁碟
```
lsblk
```

掛載磁碟
```
sudo mkdir /mnt/yourdir
sudo mount /dev/xvdf1 /mnt/yourdir
```
若不知道分割區
```
file -s /dev/xvdf
```
若有格式，可能是直接 mount /dev/xvdf
### 📝 建議命名規則
Volume 名稱建議標明用途（e.g. snapshot-data-vol-2025-05）

AMI 建議寫上來源快照與時間（e.g. recovery-ami-from-snap-xyz-2025-05-27）

📌 小提醒
快照不會自動加密，要手動加密 Volume 或用加密 AMI

掛載的 Volume 記得 Unmount 再 detach，避免資料損壞

同一個快照可以重複建立多顆 Volume，用於橫向擴展

# 5/28

## 📁 Linux 實用指令

### 檢查檔案大小

```bash
du -sh 檔案或資料夾路徑
```

### 統計檔案數量

```bash
ls | wc -l
```

### 解壓縮 `.tar.gz`

```bash
tar -xzvf 檔案.tar.gz
tar -xzvf 檔案.tar.gz -C 目標資料夾
```

---

## 🔄 檔案上傳與下載（scp）

### 從 EC2 下載到本機

什麼是 scp？
scp 是一個 Linux / macOS 常見的指令，用來在本機與遠端主機之間「安全地複製檔案」的工具，透過 SSH（加密通道） 傳輸，安全又方便。

📦 語法格式
```
scp [選項] 原始位置 目標位置
```

 常見用途
✅ 1. 從本機傳到遠端（上傳）
```
scp -i key.pem myfile.txt ec2-user@<遠端IP>:~
```
這會把 myfile.txt 上傳到遠端主機的使用者家目錄。

✅ 2. 從遠端傳回本機（下載）
```
scp -i key.pem ec2-user@<遠端IP>:~/data.csv .
```
這會把 data.csv 下載到目前所在的本機資料夾。

✅ 3. 傳整個資料夾（加 -r）
```
scp -i key.pem -r myfolder/ ec2-user@<遠端IP>:~/
```


### 常見錯誤

* `No such file or directory`: 本機路徑不存在，先建立資料夾。
* `Is a directory`: 指定目標為資料夾，應該明確指定檔案名或確認目錄存在。

---


# 05/27 學習筆記

## 1. GitHub Actions 基本結構與語法

一個 GitHub Action workflow 通常放在 repo 裡的：



.github/workflows/xxx.yml

````

### 範例 `.yml` 檔案：

```yaml
name: My Workflow

on:
  push:
    branches: [main]

jobs:
  build:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - run: echo "Hello GitHub Actions!"
````

## 2. vi 操作與刪除指令

### 🔁 vi 有三種主要模式：

| 模式   | 作用           | 進入方式          |
| ---- | ------------ | ------------- |
| 一般模式 | 瀏覽、移動、刪除、複製等 | 開啟時預設是這個      |
| 插入模式 | 編輯文字（可打字）    | 按 `i`、`a`、`o` |
| 命令模式 | 儲存、退出、搜尋、跳行等 | 按 `:` 進入命令列   |

---

### ✍️ 插入文字（進入插入模式）：

| 指令    | 意義       |
| ----- | -------- |
| `i`   | 在目前位置前插入 |
| `a`   | 在目前位置後插入 |
| `o`   | 在下一行新增插入 |
| `Esc` | 回到一般模式   |

---

### 🔀 游標移動：

| 鍵    | 意義      |
| ---- | ------- |
| `h`  | 左       |
| `l`  | 右       |
| `j`  | 下       |
| `k`  | 上       |
| `gg` | 移動到第一行  |
| `G`  | 移動到最後一行 |
| `:n` | 跳到第 n 行 |

---

### ❌ 刪除指令：

| 指令         | 意義             |
| ---------- | -------------- |
| `x`        | 刪除游標所在字元       |
| `dd`       | 刪除整行           |
| `d3d`      | 刪除往下 3 行       |
| `:78,461d` | 刪除第 78 到 461 行 |

---

### 💾 儲存與退出：

| 指令    | 意義      |
| ----- | ------- |
| `:w`  | 儲存      |
| `:q`  | 離開      |
| `:wq` | 儲存並離開   |
| `:q!` | 不儲存強制離開 |

---

### 🔍 搜尋與取代：

| 指令          | 意義            |
| ----------- | ------------- |
| `/文字`       | 向下搜尋          |
| `?文字`       | 向上搜尋          |
| `n` / `N`   | 下一個 / 上一個符合結果 |
| `:%s/舊/新/g` | 全文取代（g 表示全域）  |

---

### ✅ 快速三步操作流程：

1. `i` 進入插入模式打字，打完後 `Esc`
2. `:w` 儲存
3. `:q` 離開（或用 `:wq` 一次完成）



# 5/26

1.
tmux 用法

開啟新 session	tmux 或 tmux new -s 名稱
列出所有 session	tmux ls
進入某個 session	tmux attach -t 名稱或編號
離開（detach）session	Ctrl + b 然後按 d
結束 session（從內部）	exit 或 Ctrl + d
刪除 session（從外部）	tmux kill-session -t 名稱或編號



# 5/25

1.
設定虛擬機遇到的問題
    1. 沒有公有 IP，無法連線 SSH
        原因：建立 EC2 時，子網（Subnet）沒有開啟 Auto-assign public IP。
        解法：
        建立 EC2 時，在「Configure Instance」→ 啟用 Auto-assign Public IP
        或用 Elastic IP 手動綁定已建立的 EC2。
    2. EC2 有公有 IP，但仍無法連外/被連
        可能原因 1：VPC 沒有綁定 Internet Gateway（IGW）
        解法：
        到 VPC → Internet Gateways → 建立並 Attach 到 VPC。
        Route Table 加上 0.0.0.0/0 → igw-xxxxxx 路由。
        可能原因 2：Route Table 沒指向 IGW
        解法：編輯 Route Table → 加入 IGW 的預設路由。
        可能原因 3：安全群組沒開 Port 22
        解法：Security Group → Inbound Rule 加上 TCP/22 from 0.0.0.0/0
    3. ssh -i pem-file username@ip-addr

2.
創建虛擬環境
python3 -m venv venv

linux os/mac os
```
source venv/bin/activate
```

window 
```
venv\Scripts\activate
```

3.
ip 相關指令
ifconfig  顯示本機（區網）所有網卡的 IP，多為私有 IP

curl ifconfig.me 取得你對外的「公網 IP」（就是別人看到的你）



# 5/20
git log --graph --oneline --all --decorate
# 先回到f444c18
git reset --hard f444c18
# rebase自己這段分支到 1dac99a 後面
git rebase 1dac99a
# 回到最新版本 3bc9111
git reset --hard 3bc9111
# 將最新版本接到剛剛rebase的最新版  a84a465 這個hash每個人會不一樣
git rebase a84a465 
# 分支合拼完成 也可以用cherry-pick一個一個把commit撿回來到最新版

git reset --hard <commit> 會把 HEAD、目前分支指標，還有你工作目錄的檔案內容，全部都重設成某個 commit 的狀態。
    
git rebase <commit> 會把你的 commit「接到」另一個 base commit 之後，好像是你從那邊開始開發的一樣。



# 5/18

1.
vite.config.js

vite.config.js 是什麼？
這是一個 Vite 的組態檔（configuration file），預設位置在專案根目錄。

基本語法（ESM 模組格式）

// vite.config.js
export default {
  server: {
    port: 3000,
    open: true, // 啟動自動打開瀏覽器
  },
  build: {
    outDir: 'dist', // 打包輸出目錄
  },
};

2.
playcanvas

建立 pc.Application

const canvas = document.getElementById(
  "application-canvas"
) as HTMLCanvasElement;

const app = new pc.Application(canvas, {
  mouse: new pc.Mouse(canvas),
  touch: new pc.TouchDevice(canvas),
});

app.start();

設定 Canvas 畫布大小

app.setCanvasFillMode(pc.FILLMODE_FILL_WINDOW);
app.setCanvasResolution(pc.RESOLUTION_AUTO);

加上 Camera 與 Light

camera.addComponent("camera", {
  clearColor: new pc.Color(0.1, 0.1, 0.3),
});
camera.setPosition(0, 0, 5);
app.root.addChild(camera);

加一個模型進場景

const cube = new pc.Entity("cube");
cube.addComponent("model", {
  type: "box",
});
app.root.addChild(cube);

// 加一盞光
const light = new pc.Entity("light");
light.addComponent("light", {
  type: "directional",
});
light.setEulerAngles(45, 30, 0);
app.root.addChild(light);

在 app.on("update") 內處理動畫

app.on("update", (dt: number) => {
  cube.rotate(0, 30 * dt, 0); // 每秒旋轉 30 度
});

根據需要處理滑鼠鍵盤事件


app.mouse!.on(pc.EVENT_MOUSEDOWN, (e) => {
  console.log('點擊了座標', e.x, e.y);
});


# 5/17

1.
```
docker compose down 
```
可以關掉docker compose up 開的container

2.
container 掛載有兩種方式
    1.掛到docker裡的Volume
        優點：
            ✅ 權限自動處理（不需 chown）
            ✅ 清潔、安全，不會意外覆寫主機檔案
            ✅ 在多 container 中共用資料很方便
            ✅ 適合部署在伺服器或正式環境
        缺點：
            🔍 主機看不到檔案（比較難 debug）
            📦 資料在 Docker 裡面，不容易直接備份（需要額外命令或 volume plugin）
            🐣 初學者比較難理解發生什麼事
    2.掛到本機
        優點：
            ✅ 主機可直接看到資料（方便 debug）
            ✅ 可用本機工具編輯、備份資料（如 VSCode）
            ✅ 適合本地開發環境（local dev）
        缺點：
        ❗ 必須自己設定正確的目錄擁有者與權限（常見錯誤來源）
        ⚠️ 不同平台可能出現路徑或權限問題（尤其 macOS / WSL）
        ⛔ 若誤刪主機目錄，容器資料會消失
        😵 同步資料性能較差（尤其大量小檔案）
        
3.
權限管理

每個檔案與目錄都會有三組權限，分別對應三個對象：

欄位	意義
owner（擁有者）	建立者本人或指派的用戶
group（群組）	擁有者所屬群組
others（其他人）	系統中所有其他使用者

改變檔案擁有者

```
sudo chown vincent:vincent hello.txt         # 指定 user 與 group
sudo chown -R 999:999 ./pg-data              # 遞迴改資料夾擁有者（常用在 Docker）
```

改變檔案權限
 
```
chmod 755 run.sh          # rwx r-x r-x
chmod 644 file.txt        # rw- r-- r--
chmod 700 secret.sh       # rwx --- ---
```

4.
docker compose up airflow-init 的意思
它會從 docker-compose.yaml 裡只執行 airflow-init 這個 service，而不是全部的 container 一起啟動。


5.
使用 Docker 安裝 Airflow 的完整流程與理由
    1. 安裝docker
    2. 建立專案資料夾與結構
        ```
        mkdir airflow-test
        cd airflow-test
        mkdir dags logs plugins
        touch docker-compose.yaml
        touch .env
        ```
        dags/ 放置 DAG 工作流程檔案
        logs/ 用來記錄任務執行過程（Airflow log handler 預設寫這裡）
        plugins/ 可擴充 Airflow 功能（operator、hook...）
        .env：集中變數設定（如 image 版本、UID）
    3. 撰寫 .env 檔案 
        AIRFLOW_IMAGE_NAME=apache/airflow:2.4.2
        AIRFLOW_UID=50000
    4. 撰寫 docker-compose.yaml
        包含以下 4 個服務：
        postgres：資料庫（儲存 DAG、task metadata）
        airflow-init：負責 airflow db init + 建立 admin 使用者
        airflow-webserver：Airflow 的 UI 介面
        airflow-scheduler：排程器（負責執行 DAG 的任務）
    5. 修正 logs 權限問題（必做）
        ```
        sudo chmod -R 777 ./logs  
        chmod -R 755 ./dags  
        chmod -R 755 ./plugins  
        ```
        原因：
        容器中的 airflow 使用者無法寫入預設掛載的 logs/，會導致 log handler 報錯崩潰
        修改成正確 UID（50000）即可正常建立 log 子目錄
    6. 啟動服務
        第一次初始化（建議執行一次）：
        ```
        docker compose up airflow-init
        ```
        背景啟動服務：
        ```
        docker compose up -d
        ```
    7. 開啟瀏覽器登入 Airflow UI
        
6.
用docker開airflow時，如果不是掛到docker裡面的話，要記得改權限

./logs/ → Airflow 任務 log 儲存處
mkdir -p ./logs
chmod -R 777 ./logs

./dags/ → 放你自定義 DAG 的目錄
chmod -R 755 ./dags

mkdir -p ./plugins
chmod -R 755 ./plugins


待辦
常見會卡住的問題原因與對應解法(chatgpt)


# 5/16

待辦
docker compose down
權限設定
airflow



# 4/26
1.
強制改為原本的main
git fetch upstream
git checkout main
git reset --hard upstream/main
git push origin main --force

git fetch upstream
意思：
從 upstream（也就是原專案）下載最新的 commits、branches、tags

git checkout main
意思：
切換到你本地的 main 分支
因為你後面要 reset，所以要先確保「我現在在 main 上」

git reset --hard upstream/main
意思：
把你目前 main 分支的內容，強制改成 upstream/main 的內容
HEAD、index（staging）、工作目錄（檔案）都會一起變成跟 upstream/main 一模一樣
所有未 commit 的變更也會丟掉！


git push origin main --force
意思：
把你本地現在乾淨、同步過 upstream 的 main，推回自己的 GitHub 上（origin）
因為 reset --hard 改了歷史，所以必須用 --force 強制推送


2.
cherry-pick 之後遇到 conflict 怎麼辦？
git status 查看有哪些檔案有 conflict（通常是 U 開頭）

手動打開檔案，解決 <<<<<<<, =======, >>>>>>> 的標記

git add 解完的檔案

git cherry-pick --continue 繼續套用剩下的 cherry-pick

3.
如果 cherry-pick 時 conflict 很複雜，臨時不想繼續？
git cherry-pick --abort

4.
切換分支時 VS Code 出現的選項是什麼？
選項	意思	什麼時候用？
Stash & Checkout	把現在改動暫存起來再切分支	大部分情況
Migrate Changes	直接把改動搬到新分支	少數（要小心 conflict）
Force Checkout	丟掉所有未儲存改動	放棄當前改動時
Cancel	不切分支，自己手動處理	不確定要不要丟改動時

```
開始 cherry-pick
    ↓
是否出現 conflict？
    ↓
    是 ➔ 打開 conflicted 檔案
             ↓
       手動解決 conflict
             ↓
       git add 解決完的檔案
             ↓
       git cherry-pick --continue
             ↓
      （如果還有下一個 cherry-pick，繼續套用）
             ↓
       完成 cherry-pick 🎉

    否 ➔ 直接套用成功 🎉

```


5.
刪除分支的指令
想刪哪裡？	指令
刪本地分支	git branch -d 分支名（安全）或 -D（強制）
刪 GitHub 上的分支	git push origin --delete 分支名


6.
stash
你想做的事	指令	說明
暫存目前的變更	git stash	把目前沒 commit 的東西全部存起來
查看有哪些 stash	git stash list	看現在有多少筆 stash
看某個 stash 的內容	git stash show -p stash@{0}	比對 diff 內容
套用最新的 stash（不刪掉）	git stash apply	套用，但 stash 還在
套用最新的 stash（套完刪掉）	git stash pop	套用並刪除
刪掉一個 stash	git stash drop stash@{0}	刪掉指定 stash
清空所有 stash	git stash clear	全部砍掉

快速範例
改了一些檔案（還沒 commit）

突然要切去修緊急 bug

使用：
```
git stash
git checkout hotfix/urgent-bug
```
修完之後，回來：

```
git checkout my-feature
git stash pop
```

7.
修改repo的origin
```
git remote set-url origin https://github.com/company-name/project.git
```

# 4/25
1.
df -h 查看掛載磁碟的位置


2.
ls | wc -l 計算有多少筆資料 


# 4/24
1.
sudoers

sudoers 是 Linux 系統中一個用來**管理使用者權限的檔案

sudoers 的功能：
授權哪些使用者或群組可以執行 sudo

限制使用者能執行哪些指令

是否要輸入密碼（NOPASSWD）

指令執行記錄的方式（LOG）



2.
在為 APT 套件管理系統 添加 Docker 的 GPG 公鑰，確保從 Docker 官方來源下載的套件是「未被竄改且可以信任」的。

第一步：建立金鑰存放目錄
 
sudo install -m 0755 -d /etc/apt/keyrings
創建/etc/apt/keyrings

第二步：下載 Docker GPG 金鑰並轉為系統可用格式
curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo gpg --dearmor -o /etc/apt/keyrings/docker.gpg

curl -fsSL 是什麼？
這是 curl 的四個選項組合，用來靜默下載內容：

選項	意義
-f	出錯時不要輸出 HTML 頁面（fail silently）
-s	靜默模式（silent），不顯示進度條
-S	如果出錯時顯示錯誤（Silent + Show error）
-L	跟隨轉址（若 URL 重定向，照樣下載）

第三步：給所有人讀取權限
sudo chmod a+r /etc/apt/keyrings/docker.gpg
chmod a+r 所有人可讀

3.
安裝不在apt裡面的套件的方法

目的：讓你的系統信任這個來源，才能用 apt 安裝它的套件

第 1 步：下載 & 設定 GPG 金鑰
```
curl -fsSL https://xxx.com/gpg | gpg --dearmor -o /etc/apt/keyrings/xxx.gpg
chmod a+r /etc/apt/keyrings/xxx.gpg
```
必須先把金鑰下載，存到 /etc/apt/keyrings/，才能讓 APT 驗證來源「安全可信」


第 2 步：新增來源清單
```
echo "deb [arch=amd64 signed-by=/etc/apt/keyrings/xxx.gpg] https://xxx.com/linux/ubuntu stable main" \
  | sudo tee /etc/apt/sources.list.d/xxx.list > /dev/null
```

第 3 步：更新套件庫 & 安裝

```
sudo apt update
sudo apt install xxx
```

4.
確認有什麼外部套件被加入了
```
ls /etc/apt/sources.list.d/
```

5.
bashrc vs systemctl

工具	用途
systemctl	控管 系統服務（services）：啟動、關閉、開機自啟
.bashrc	設定 使用者 shell 的環境變數、別名、初始化命令

工具	什麼時候會執行
systemctl	系統啟動時、手動執行 systemctl start xxx.service 時
.bashrc	每次開啟一個互動式 shell（例如打開終端機或用 SSH 登入）時自動執行


工具	常見用途
systemctl	啟動 nginx、MySQL、Kubernetes、Docker 等服務；設定服務開機自啟
.bashrc	設定 alias（如 alias k=kubectl）、設定 PATH、顯示歡迎訊息、匯入虛擬環境等


總結一句話 💡
systemctl 是「幫你管理整個作業系統的服務」，而 .bashrc 是「幫你準備使用者自己的指令環境」。

待處理
k8s講義 p115



# 4/19

1.
docker 離開容器但不會刪掉的方法
    ctrl + p + q
    離開之後透過docker start container_id開啟


2.
想開一個沒網路的container
開一個有網路的container下載好套件，然後在打包成image，之後從這個image開container

3.
veth vs 網卡

veth 是什麼？為什麼成對？

veth 是 Linux 裡的一種虛擬網路裝置（virtual network device）。

特點：
veth 一定成對出現，你無法只創一端。

資料從一端送出，就會從另一端接收。

兩端可以被放到不同的 Network Namespace 裡，例如：

一端在宿主機

一端放進 container 裡

什麼是網卡（NIC）？
網卡（Network Interface Card）是一種讓電腦連接網路的硬體或虛擬設備。
不論是連接到乙太網路（Ethernet）、Wi-Fi，或是 Docker、VM 的虛擬網路，全部都需要透過某種網卡。

在 Linux 或 WSL 中，你可以用 ip link 或 ifconfig 看到所有網卡的資訊。

4.
硬連結 vs 軟連結

硬連結
檔案的另一個入口點，實體存在一份，但有多個名稱
ln 原始檔案 連結檔案

軟連結
類似「捷徑」，是一個指向原檔案的路徑檔案
ln -s 原始檔案 連結檔案


5.
私有ip

當你啟動一個 container（使用 --network=bridge 或自定義 bridge），Docker 會做以下事情：

在 host 上創建一個 veth pair（虛擬乙太網卡）

把一端綁到 host 的網橋（通常是 docker0）

把另一端放進 container 裡，命名為 eth0

給這個 eth0 分配一個私有 IP（預設是 172.17.0.X）

所以network=none的container沒有私有ip


6.
容器流量轉發

以一個 container 的封包來說，它的封包會：

透過 container 內部的 eth0 發送

對應到 veth pair（另一端掛在 bridge 上）

經由 bridge 轉發（跟交換機一樣轉發）

到 docker0 的 IP（172.17.0.1）這層，就是宿主機的「視窗」



# 4/18

1.
docker 網路 none, bridge, host, container_id

none：告訴 Docker Engine 不要幫我管理任何任何網路功能，只要建立一個隔離網路空間（Network namespace）就好。

![image](https://hackmd.io/_uploads/H1ecPQ11lg.png)

host：不要幫我創造 network namespace，我不需要網路隔離，和宿主機共用相同的網路模型即可。

![image](https://hackmd.io/_uploads/rJ06DQJylx.png)

birdge：幫我創造全新的 network namespace，然後我想要透過 Linux Bridge 來與原生網路有互動的能力

宿主機沒辦法跟container溝通的原因是因為他們的網段不同


![image](https://hackmd.io/_uploads/r1YNOQyyex.png)
![image](https://hackmd.io/_uploads/Syw3uXkklx.png)

container_id：告訴 Docker 不要幫我創造新的網路空間，取而代之，使用現有的 Container 的網路空間，和它共處於相同的網路環境中。因此，這兩個 Container 將會看到一樣的網路介面、路由表 ... 等網路相關資訊。

![image](https://hackmd.io/_uploads/H1WeFXkkxe.png)




reference 
https://www.hwchiu.com/docs/2020/docker-network-model
https://www.hwchiu.com/docs/2020/docker-network-model-lab

待完成
用手刻bridge network

2.
正向代理（Forward Proxy）：客戶端向代理伺服器發送請求，代理伺服器代替客戶端向目標伺服器發送請求。正向代理通常用於將客戶端請求轉發到外部網絡。

反向代理（Reverse Proxy）：客戶端向反向代理伺服器發送請求，反向代理再將請求轉發給內部的後端伺服器處理。客戶端並不直接與後端伺服器通信。


# 4/17

做到k8s講義p148

1. 
指令 systemctl

systemctl 是什麼？
systemctl 是 systemd 的控制指令，用來「啟動、停止、查看、啟用、停用」各種系統服務（service）、開機流程與系統狀態。

它的功能範圍非常大，最常見的用途就是：

✅ 管理各種在背景執行的系統服務（daemon）


在systemctl 建立一個 service(沒做完)


2. 
/etc/用戶名稱/.bashrc 是一開始進來會用到的bashrc\
可以修改~/.bashrc來修改一開始進來的位置
source ~/.bashrc可以更改變動

3. 
systemctl list-units --type=service 檢查正在運行的服務



待處理
建立service 
把k8s講義裡面的東西看懂



```
# 啟動 docker
sudo systemctl start docker

# 停止 docker
sudo systemctl stop docker

# 查看 docker 狀態
sudo systemctl status docker

# 設為開機自動啟動
sudo systemctl enable docker

# 取消開機啟動
sudo systemctl disable docker

```


# 4/16
/etc/sudoers 加上

```
vincent ALL=(ALL:ALL) ALL

<使用者> <主機>= (<執行者>:<群組>) <可執行指令>

```
代表讓使用者有root權限


# 更早之前的筆記們

npx 是 Node.js 附帶的一個 CLI 工具，功能是 「執行 node 套件而不用先全域安裝」。

# ts-node vs tsx

![image](https://hackmd.io/_uploads/BkefThNRdkx.png)

ts-node不支援esm，所以要用tsx來做直接運行ts

本地安裝tsx

yarn add tsx --dev

用yarn裡面安裝的tsx執行 

yarn tsx file.ts 

# yarn
npx的功能跟yarn dlx一樣，但要yarn 2+才能用

升級方法
yarn set version 3.x

回來yarn 1.x
yarn set version classic


# nvm功能

查看node版本
nvm list or nvm ls

安裝其他版本
nvm install 18

刪除版本
nvm uninstall 18

切換版本
nvm use 18

設定預設版本
nvm alias default 18

刪除預設
nvm unalias default


# nodemon
  
常用指令
nodemon --watch src --ext ts,js --exec tsx src/index.ts

--watch src 
告訴 nodemon 要監控（watch）哪個目錄。這裡指定 src

--ext ts,js
告訴 nodemon 要監控哪些檔案副檔名的變動。這裡包含 .ts 跟 .js。

--exec tsx
告訴 nodemon 在偵測到有檔案變動後，要執行哪個命令（executor）。這裡是 tsx。

# moongoose 
  
## create 
db.users.insertOne({ name: "Alice", age: 25, city: "Taipei" }) 
 
db.users.insertMany([
  { name: "Bob", age: 30, city: "Kaohsiung" },
  { name: "Charlie", age: 28, city: "Taichung" }
])

 
## read 

db.users.find() 
 
db.users.find({ city: "Taipei" }) 

db.users.findOne({ name: "Alice" })

// containerId 不為 null
db.sessions.find({ containerId: { $ne: null } })

## update 

db.users.updateOne(
  { name: "Alice" },              // 查詢條件
  { $set: { age: 26, city: "Taoyuan" } }  // 更新動作：設定 age 與 city 欄位
) 
 
db.users.updateMany(
  { city: "Taipei" },
  { $set: { city: "New Taipei" } }
)

# delete
 
db.users.deleteOne({ name: "Alice" }) 

db.users.deleteMany({ city: "Kaohsiung" })

# delete collection 

db.users.drop()

# delete database 

//先進入資料庫 

db.dropDatabase()

# tsconfig

選擇tsconfig  

```
tsc -p ./path/tsconfig.json
```
 
target：指定輸出的 ECMAScript 版本（哪一代語法標準），影響最終編譯後的 JavaScript 語法。  
module：指定使用哪種模組系統（CommonJS, AMD, ESNext 等），影響 import / export 如何被轉譯。  
moduleResolution：指定如何尋找並解析模組路徑（Node 模式、Classic、Node16、NodeNext），影響編譯器在檢查或匯入檔案時的搜尋邏輯。  


# netstat

netstat -ano：

netstat：顯示當前的網絡連接、路由表、埠監聽等網絡狀態。
-a：顯示所有連接（包括正在監聽的埠）。
-n：以數字格式顯示地址和埠（不解析為域名）。
-o：顯示與每個連接相關聯的進程 ID（PID）。

```
window
netstat -ano | findstr :3306

linux
netstat -ano | grep :3306
```  
  
  
tasklist：

顯示當前系統中所有正在運行的進程，包括進程名稱、PID、記憶體使用等信息。 

/FI：
指定一個篩選條件（Filter）。 

"PID eq <PID>"：  

PID：篩選條件中的進程 ID。  
eq：篩選條件的比較運算符，表示 "等於"。  
<PID>：需要查找的進程 ID（例如上面輸出的 1234）。  
    
    

```
window
tasklist /FI "PID eq <PID>
    
linux 
ps -p <PID>
```

# git
    
    
    
git stash 可以讓環境回復到上次commit的地方
git stash apply 可以回復成git stash前的環境

```
git stash
```
    
    
1. 恢復未暫存的更改
```
git restore .
```

2.恢復特定文件的更改
```
git restore <file>
```
3.恢復已暫存的更改
```
git reset 
git reset <file>
```
    

git rebase 是將一個分支上的提交重新放置到另一個分支的基礎上。
```
git rebase <base-branch>
```
    
Cherry-pick 是將另一個分支上的特定提交複製到當前分支。
```
git cherry-pick <commit-hash>
```    
    
git log 查看commit紀錄
```
git log
```

    
git reset 回到某個commit的點
```
git reset --hard <commit-hash>
```

git branch -d 刪除branch
```
git branch -d <branch name>
```

# prisma

遷移prisma的資料庫
```
npx prisma migrate dev --name init
```
    
    
檢查某個主機上的特定端口是否開放並可訪問的
```
netcat -zv 127.0.0.1 6379
```
    
    
重新生成 Prisma 客戶端
```
npx prisma generate
```
    
涉及資料庫結構變更時，執行 npx prisma migrate dev 生成遷移文件並同步資料庫。
```
npx prisma migrate dev
```
    
    
    
# ps 印出當前的process

a：顯示所有用戶的進程，而不僅僅是當前終端的進程。
u：以用戶友好的格式顯示進程資訊，包括用戶名、CPU 與內存使用率、啟動時間等。
x：包括那些沒有控制終端的進程。

```
ps aux
```

-u 查看用戶進程

```
ps -u name
```


# ubuntu使用者

創建使用者

-m 會在home下建使用者目錄
-s 指定shell

```
sudo useradd -m Name -s /bin/bash
```

增加密碼

```
sudo passwd Name 
```

更改使用者

```
su - Name
```


刪除進程

```
sudo kill -9 PID
```


# shell

執行腳本
```
./file.sh

sh ./file.sh
```


# docker 

建立docker file

```
docker build -t tagName
```


# readable & writable


## readable 

透過read stream可以實現流式讀取，讓一些需要時間的操作可以依序被執行，透過push來裝填輸出queue，而透過on('data')可以監聽queue裡面的資料，最後push null代表結束


ex 讀取檔案

```

import fs from "fs";

// 這邊會把檔案依序一塊一塊的存進stream裡面

const readableStream = fs.createReadStream("example.txt", { encoding: "utf-8" });


// 每存進一塊會呼叫data事件，被這段監聽到

readableStream.on("data", (chunk) => {
  console.log("📥 讀取到的數據:", chunk);
});


// 結束輸出

readableStream.on("end", () => {
  console.log("📌 檔案讀取完成");
});


```


ex 自製計時器

```

class timer extends Readable {
  private time = 0;
  private end = 10;
  constructor(end: number) {
    super();
    this.end = end;
  }
  async _read() {
    setTimeout(() => {
      if (this.time < this.end) {
        // push 指的是輸出data的意思
        this.push(String(this.time));
        this.time++;
      } else {
        this.push(null);
      }
    }, 1000);
  }
}

const testTimer = new timer(5);
// 上面push的會變成data事件
testTimer.on("data", (chunk) => {
  // 會一直執行_read函式直到push null
  console.log(chunk.toString());
});

```

## writable

寫入流，當執行write函數時，可以自定義功能，一樣會一塊一塊的輸入



ex 寫入檔案

```
import fs from "fs";
// 將資料存進stream裡面
const writableStream = fs.createWriteStream("output.txt");

writableStream.write("Hello, World!\n");
writableStream.write("這是一段測試文字。\n");

writableStream.end(() => {
  console.log("📌 資料寫入完成");
});

```

ex 記憶體緩存

```
import { Writable } from "stream";

class MemoryWritable extends Writable {
  private data: string = "";

  _write(chunk: any, encoding: string, callback: Function) {
    this.data += chunk.toString(); // 將寫入的內容存到變數
    console.log("寫入資料:", chunk.toString());
    callback(); // 告訴 Stream 已經寫入成功
  }

  getData() {
    return this.data;
  }
}

const memoryStream = new MemoryWritable();

memoryStream.write("Hello, ");
memoryStream.write("World!\n");

memoryStream.end(() => {
  console.log("📌 所有寫入資料:", memoryStream.getData());
});

```

## Duplex

同時有輸入輸出流的功能

```
import { Duplex } from "stream";

class EchoStream extends Duplex {
  _read(size: number) {
    this.push("📢 這是 EchoStream 傳回的資料\n");
  }

  _write(chunk: any, encoding: string, callback: Function) {
    console.log("📥 收到:", chunk.toString());
    callback();
  }
}

const echo = new EchoStream();
echo.write("Hello!\n");
echo.on("data", (chunk) => {
  console.log(chunk.toString());
});

```

# 再更早之前的筆記

netstat -ano：

netstat：顯示當前的網絡連接、路由表、埠監聽等網絡狀態。
-a：顯示所有連接（包括正在監聽的埠）。
-n：以數字格式顯示地址和埠（不解析為域名）。
-o：顯示與每個連接相關聯的進程 ID（PID）。

```
window
netstat -ano | findstr :3306

linux
netstat -ano | grep :3306
```  
  
  
tasklist：

顯示當前系統中所有正在運行的進程，包括進程名稱、PID、記憶體使用等信息。 

/FI：
指定一個篩選條件（Filter）。 

"PID eq <PID>"：  

PID：篩選條件中的進程 ID。  
eq：篩選條件的比較運算符，表示 "等於"。  
<PID>：需要查找的進程 ID（例如上面輸出的 1234）。  
    
    

```
window
tasklist /FI "PID eq <PID>
    
linux 
ps -p <PID>
```
    
    
    
git stash 可以讓環境回復到上次commit的地方
git stash apply 可以回復成git stash前的環境

```
git stash
```
    
    
1. 恢復未暫存的更改
```
git restore .
```

2.恢復特定文件的更改
```
git restore <file>
```
3.恢復已暫存的更改
```
git reset 
git reset <file>
```
    

git rebase 是將一個分支上的提交重新放置到另一個分支的基礎上。
```
git rebase <base-branch>
```
    
Cherry-pick 是將另一個分支上的特定提交複製到當前分支。
```
git cherry-pick <commit-hash>
```    
    
git log 查看commit紀錄
```
git log
```

    
git reset 回到某個commit的點
```
git reset --hard <commit-hash>
```

git branch -d 刪除branch
```
git branch -d <branch name>
```
    
    
遷移prisma的資料庫
```
npx prisma migrate dev --name init
```
    
    
檢查某個主機上的特定端口是否開放並可訪問的
```
netcat -zv 127.0.0.1 6379
```
    
    
重新生成 Prisma 客戶端
```
npx prisma generate
```
    
涉及資料庫結構變更時，執行 npx prisma migrate dev 生成遷移文件並同步資料庫。
```
npx prisma migrate dev
```