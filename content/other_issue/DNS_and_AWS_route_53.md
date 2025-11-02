🌐 DNS 整體運作與 Route 53 權威伺服器流程總覽

🧭 一、整體角色架構

🪄 二、設定流程

步驟 1️⃣：購買網域（Domain Registration）

🔹 你要做的事：

到一家 Registrar（網域註冊商） 購買網域，例如：

- GoDaddy

- Google Domains

- Namecheap

- Cloudflare Registrar

假設你買的是：

mindechoserver.com

🔹 背後發生的事：

Registrar 會向 .com 的官方 Registry（註冊管理機構）（例如 Verisign）登記這個網域。

.com 的 TLD DNS 伺服器 會記錄這筆資料：

此時網域屬於你，但 DNS 管理可能還在 Registrar 的系統裡。

🧠 簡單說：

你擁有了「名字」，但還沒告訴世界「這個名字要指向哪台伺服器」。

步驟 2️⃣：在 Route 53 建立 Hosted Zone

- 在 AWS Route 53 console → 建立一個「Public Hosted Zone」
例如：mindechoserver.com

- Route 53 會自動產生一組 Name Server (NS)：

ns-123.awsdns-45.net.

ns-456.awsdns-78.com.

ns-789.awsdns-12.org.

ns-012.awsdns-34.co.uk.

- 這些 NS 就是「Route 53 權威伺服器的實際位置」。

🧠 意義：

AWS 已經幫你準備好一組權威伺服器，只等你把它註冊到全球 DNS 系統。

步驟 3️⃣：到網域註冊商（Registrar）修改 NS 記錄

- 登入你購買網域的地方（GoDaddy、Google Domains、Namecheap…）

- 將該網域的 Name Server 設定 改成上面 Route 53 提供的四組 NS。

- 儲存後，Registrar 會通知 .com（或對應的 TLD Registry），更新 zone 檔。

🧠 意義：

這一步是「把 DNS 管理權委派（delegate）」給 Route 53。

從此 .com 的 TLD 知道：「mindechoserver.com 是由 AWS Route 53 管的。」

⚙️ 三、查詢流程（使用者實際訪問時）

假設有人在瀏覽器輸入：

www.mindechoserver.com

整個解析過程如下：

1️⃣ 使用者的 Local DNS（例如中華電信）先查快取。

↓（沒找到）

2️⃣ 去問 Root DNS：

「.com 的伺服器在哪？」

↓

3️⃣ Root 回答：

「去問 .com TLD 伺服器。」

↓

4️⃣ .com TLD 查 zone file，發現：

mindechoserver.com → NS = ns-123.awsdns-45.net.

↓

5️⃣ 告訴 Local DNS：

「去問 AWS Route 53。」

↓

6️⃣ Local DNS 問 Route 53（你的權威伺服器）：

「www.mindechoserver.com 的 IP 是多少？」

↓

7️⃣ Route 53 回答：

「54.240.22.10」

↓

8️⃣ Local DNS 把結果回傳給使用者瀏覽器，

並快取以加速下次查詢。

🏁 四、整體資料流向圖

┌──────────────┐

│  User Client │

└──────┬───────┘

│ 查詢 www.mindechoserver.com

▼

┌──────────────┐

│ Local Resolver│  ← ISP 的 DNS

└──────┬───────┘

│

▼

┌──────────────┐

│ Root DNS     │  → 告訴你去問 .com

└──────┬───────┘

│

▼

┌──────────────┐

│ .com TLD DNS │  → 告訴你去問 AWS 的 NS

└──────┬───────┘

│

▼

┌────────────────────┐

│ Route 53 (Authoritative) │

│ ns-123.awsdns-45.net 等  │

└────────┬─────────────┘

│

▼

回傳 IP：54.240.22.10 ✅

🧠 五、重點總結