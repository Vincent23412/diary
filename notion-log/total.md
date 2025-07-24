# 2025-07-24 筆記

當然可以，以下是不刪減的完整翻譯：

一個 Shell 腳本需要使用該實例的公有 IP 和私有 IP 地址。

哪一種方法是讓你的 Shell 腳本能夠獲取該實例關聯 IP 地址的最佳方式？

- 透過使用 CloudWatch 指標。
✅ 正確答案：

- 透過使用 Curl 或 Get 命令，從 http://169.254.169.254/latest/meta-data/ 取得最新的中繼資料資訊。
❌ 您的答案：

- 透過使用 Curl 或 Get 命令，從 http://169.254.169.254/latest/user-data/ 取得最新的使用者資料資訊。

- 透過使用 IAM。

總體解釋：

實例中繼資料 是關於你的 EC2 實例的資料，你可以用來配置或管理正在執行的實例。

因為你的實例中繼資料可直接從實例本身存取，

所以你不需要使用 Amazon EC2 控制台或 AWS CLI。

這在你撰寫要從實例中執行的腳本時會非常有幫助。

例如，你可以從實例中繼資料中存取實例的本地 IP 地址，以便用來管理與外部應用程式的連線。

若要從正在執行的實例中檢視私有 IPv4 位址、公有 IPv4 位址，

以及所有其他類別的實例中繼資料，請使用下列 URL：

👉 http://169.254.169.254/latest/meta-data/

以下是這題的完整翻譯與解析：

題目：

一家企業擁有一個全球性新聞網站，部署在多台 EC2 實例上。

近期由於網站的負載上升，導致讀者的回應時間變慢。

這造成了營收影響，因為有些使用者若等超過 10 秒仍無法開啟網站就會離開。

公司希望用具成本效益的方式解決這個問題。

請問下列哪兩項 AWS 服務可以用來解決這個問題？（請選兩項）

各選項解析：

✅ 正確答案：

使用 Amazon CloudFront，並將網站設為自訂來源（custom origin）
→ CloudFront 是 AWS 的 全球內容傳遞網路（CDN）服務，
可以將靜態或快取內容部署到邊緣位置，讓全球用戶從最近的位置載入內容，
大幅降低延遲，提高載入速度。

使用 Amazon ElastiCache 作為網站的記憶體資料儲存或快取系統
→ ElastiCache（支援 Redis 或 Memcached）可以快取常用的查詢結果、靜態內容或 session 資料，
降低對資料庫或應用伺服器的壓力，加快網站回應速度。

❌ 錯誤選項說明：

- ❌ 為了提升讀取吞吐量，使用 AWS Storage Gateway 將內容分散到多個區域
→ Storage Gateway 是混合雲儲存服務，用於連接 on-premises 和 AWS 儲存，不是用來加速網站內容傳遞。

- ❌ 將網站部署到不同區域中的所有 VPC 以加快處理速度
→ 雖然理論上部署到多個區域會縮短地理延遲，但這會大幅增加成本與複雜度，也不必要，
使用 CloudFront 就可以達成全球加速，不需要全區部署。

- ❌ 使用 Amazon RDS Multi-AZ 來提升資料庫讀取擴展性
→ Multi-AZ 是用來做高可用與備援，不是用來增加讀取效能。
若要擴展讀取效能，應該考慮使用 Read Replica 而不是 Multi-AZ。

✅ 正確答案總結：

- ✔ Use Amazon CloudFront with website as the custom origin

- ✔ Use Amazon ElastiCache for the website’s in-memory data store or cache

這是一題非常典型的網站加速設計題，關鍵是：

- CDN 解決全球使用者的地理延遲問題

- Cache 解決伺服器高負載造成的回應變慢

如果你想我幫你畫一張簡單的架構圖，說明這兩者如何在網站前端協作，也可以告訴我喔！

你這題答對了，很棒！來幫你完整翻譯與解析這題：

🧾 題目翻譯：

一家公司有一個 Application Load Balancer（ALB），

用來接收網站流量，分別在：

- 80 port（HTTP）

- 443 port（HTTPS）

最近公司為網站設定了一個新網域，

他們希望所有對這個新網域的 HTTP 請求都會自動轉導（redirect）到 HTTPS，以提升安全性。

❓ 要如何設定 ALB 才能達成這個目的？

✅ 正確答案：

設定現有的 HTTP listener（port 80）來將流量重導至 port 443。

✅ 詳細解釋：

Application Load Balancer 是 Layer 7 的負載平衡器，可以根據請求內容做細緻的路由。

對於 HTTP ➝ HTTPS 自動轉導的需求，最正確做法是：

使用既有的 HTTP Listener (port 80)

在該 Listener 上加一個 “Redirect” 動作

這樣只要有人用 http://yourdomain.com 存取，

就會被 ALB 自動導向到 https://yourdomain.com，強化安全性（加密傳輸）。

❌ 為什麼其他選項錯？

📌 小提醒：實務設定畫面（在 AWS Console）

當你點進 ALB 的 Listener 設定 > Port 80 > Actions > Redirect to…

就可以設定：

- Redirect protocol: HTTPS

- Port: 443

- Status code: HTTP_301（永久轉址）

如果你想要我幫你補一張 ALB HTTP → HTTPS redirect 的設定圖解，我也可以幫你產生！要嗎？

這題你雖然答錯了，但其實你已經很接近正確答案了，只是少了一個關鍵工具的理解：AWS Control Tower。以下是完整中文翻譯與解析，幫你鞏固這類多帳號治理與合規監控題型的思考方式。

🧾 題目翻譯：

一間新創公司準備啟動多個專案，打算在 AWS 上建立一個 安全、合規的多帳號環境。

IT Manager 要求以下功能：

- 能夠輕鬆設定多帳號環境（Landing Zone）

- 能持續追蹤帳號內資源是否違反政策或合規

- 有儀表板 Dashboard 可以觀察整個企業內所有帳號的狀況

- 符合 AWS 多帳號策略的最佳實務（Best Practices）

✅ 正確解法：

✅ 使用 AWS Control Tower 建立 Landing Zone，並透過 Account Factory 自動配置帳號。透過 Control Tower Dashboard 監控帳號狀況，並設置 Preventive 和 Detective Guardrails 進行政策治理。

✅ 為什麼選 AWS Control Tower？

Control Tower 是 AWS 官方推薦用來快速建立多帳號治理架構的工具，特別適合中大型組織或剛開始擴展的企業。

❌ 錯誤選項解析：

❌ 你選的：使用 AWS Organizations + Personal Health Dashboard

- AWS Organizations 確實可以用來建立多帳號架構，但沒有：

- 

- Personal Health Dashboard 是用來檢視 AWS 系統狀態（像是某區停機、某服務受影響），不是用來看政策合規狀況的工具。

❌ 其他選項錯誤原因：

✅ 總結重點：

需要我幫你畫一張 Control Tower 架構圖（OU + Account Factory + Guardrails + Dashboard）讓你更快記憶這整套機制嗎？這題是非常典型的企業 IT 架構治理案例。

當然可以！以下是對 AWS Control Tower 的完整介紹，幫你從原理、功能、架構到使用場景一次搞懂：

✅ 什麼是 AWS Control Tower？

AWS Control Tower 是一項由 AWS 提供的自動化治理工具，

---
# 2025-07-23 筆記

這題考的是 EC2 不同狀態下的計費規則，以下是題目翻譯與正確解釋：

📘 題目翻譯：

在 Amazon EC2 中，從啟動（launch）到終止（terminate），你可以靈活管理實例，並透過變更實例狀態來控制成本。

以下關於 EC2 計費的敘述哪些正確？（選兩項）

✅ 正確答案解析：

✅ 1.

You will be billed when your On-Demand instance is preparing to hibernate with a stopping state.

- 正確。當實例進入 stopping 狀態時，如果是為了 hibernate（休眠），你仍會被收費，因為 Amazon 會保留 RAM 內容與 EBS 卷等資源。

- 若只是一般的 stop，則不會繼續收費。

✅ 2.

You will be billed when your Reserved instance is in terminated state.

- 正確。即使你終止了 Reserved Instance 的 EC2 實例，只要合約還沒到期，你仍然會依照原本合約被收費（無論有沒有在使用）。

❌ 錯誤選項解析：

❌ You will not be billed for any instance usage while an instance is not in the running state.

- 錯誤。大多數情況下這是對的，但 準備 hibernate 時（stopping 狀態）仍會收費，因此這個說法過於絕對。

❌ You will be billed when your Spot instance is preparing to stop with a stopping state.

- 錯誤。若 Spot instance 只是進入 stopping（非 hibernation），通常不會收費。

❌ You will be billed when your On-Demand instance is in pending state.

- 錯誤。pending 表示實例在啟動中，但尚未進入 running，不會收費。

🔍 補充：EC2 計費時機與狀態一覽

✅ 結論：

正確答案為：

- ✅ You will be billed when your On-Demand instance is preparing to hibernate with a stopping state.

- ✅ You will be billed when your Reserved instance is in terminated state.

這題你答對了，對 EC2 狀態與計費理解得很準確 👍

這題考的是 如何防止開發人員修改 AWS Config 規則，同時要用最少的操作成本（least operational overhead）。

❓題目翻譯：

一家公司打算透過 AWS Organizations，給每位開發者一個個人的 AWS 帳號。為了符合法規，他們會在這些新帳號中預先設定 AWS Config 的規則。

Solutions Architect 必須確保開發人員無法移除或修改任何 AWS Config 的規則。

哪一種解法最符合需求，且操作負擔最小（least operational overhead）？

✅ 正確答案：

將開發者的 AWS 帳號加入一個 Organizational Unit（OU），並為該 OU 附加一個 Service Control Policy（SCP），用來限制 AWS Config 的存取。

✅ 為什麼這個方法對？

- SCP 是一種組織級的政策（policy），可以限制 OU 中所有帳號對特定服務（例如 AWS Config）的最大權限上限。

- 即使帳號裡的 IAM User 或 Role 有 admin 權限，只要 SCP 沒開放，他們就無法執行那些動作。

- SCP 可以防止使用者（包含 root user）存取 AWS Config。

- 最少操作成本：一次設定 OU 的 SCP，套用所有帳號，無須逐個帳號設定。

❌ 錯誤選項解析：

Use an IAM Role in the new accounts with an attached IAM trust relationship to disable the access of the root user to AWS Config.

- 錯誤原因：IAM policy 無法限制 root user。 IAM Role 的 trust policy 只是定義「誰能 assume 這個角色」，不代表能阻止 root 存取 Config。

Configure an AWS Config rule in the root account to detect if changes to the new account’s Config rules are made.

- 錯誤原因：這只是偵測變更（監控），不是限制權限（防止變更），無法達成題目要求。

Set up an AWS Control Tower in the root account to detect if there were any changes to the new account’s AWS Config rules...

- 錯誤原因：AWS Control Tower 是用來建立和管理多帳號架構的工具，而非用來限制特定服務（如 Config）的存取權限。

- 同時這方法還涉及 IAM trust policy，也無法限制 root。

🧠 小總結：SCP 與 IAM 的差異

如你想，我也可以幫你示範怎麼撰寫 SCP 來禁止修改 AWS Config！

這題問的是：要部署一個 容器映像（Docker image）打包的應用程式，它需要一個 完全受管的無伺服器運算服務（fully managed serverless compute service），並且在執行時需要 5GB 的暫存空間（ephemeral storage）。

✅ 正確答案翻譯與解析：

將應用程式部署在 AWS Lambda 上，使用容器映像支援（Container image support），並將函數的暫存空間設為 5GB。

✅ 為什麼這答案正確？

- Lambda 支援容器映像部署：你可以把應用打包成 Docker image，上傳到 Amazon ECR，然後直接部署到 AWS Lambda。

- Lambda 支援調整 ephemeral storage：預設是 512MB，但你可以設定從 512MB 到 10GB，滿足臨時資料處理需求。

- 無需管理伺服器或基礎設施：完全 serverless，自動擴展，符合「最少操作成本」與「serverless」的要求。

❌ 錯誤選項解析：

Deploy the application to an Amazon ECS cluster that uses AWS Fargate tasks

- 雖然 Fargate 是無需管理 EC2 的容器服務，但它仍然需要你設定 ECS cluster 和 task definition。

- 而且題目明確要求 fully managed serverless，Lambda 才是真正的「serverless」平台。

Deploy the application in an AWS Lambda function with Container image support. Attach an Amazon EFS volume to the function

- 這是 持久性儲存（persistent storage），不符合「ephemeral（暫存）」的需求。

- 使用 EFS 還需要額外設定 VPC 與 mount target，增加不必要的複雜性。

Deploy the application Amazon ECS cluster with Amazon EC2 worker nodes and attach a 5 GB Amazon EBS volume

- ECS + EC2 並不是 serverless 解法，要管理 EC2、EBS、AMI、Auto Scaling 等。

- 顯然不符合「fully managed serverless compute」的條件。

📌 補充：Lambda 的 ephemeral storage 設定方式

在 AWS Lambda 設定容器映像時，你可以在 Function configuration 裡設定：

"EphemeralStorage": {

"Size": 5120

}

這樣會讓 /tmp 目錄有 5GB 可用空間給函數運行中使用。

需要我幫你示範怎麼在 AWS CDK 或 SAM 裡設定這個 5GB 暫存空間嗎？

你這題的選擇是正確的，來幫你簡單整理重點回顧：

🎯 題目目標：

公司想要強制所有 AWS 資源都必須按照標準命名規則進行標籤（tagging），以便後續進行存取控制。解決方案架構師必須檢查未標記（untagged）或標記不合規的資源，而且要選擇操作負擔最小的解法。

✅ 正確解法：

使用 AWS Config rule 來偵測不符合標準的 tag（non-compliant tags）

優點：

- 最少操作負擔：內建 managed rule（如 required-tags）開箱即用。

- 自動偵測：會持續監控所有新建立或修改的資源。

- 視覺化儀表板：可以在 AWS Config 主控台直接檢視不合規的資源。

- 支援自訂 tag key/value 格式：可以自訂要哪些 tag key 是必要的。

❌ 常見錯誤選項：

使用 AWS Organizations 的 tag policy + S3 Object Lock 儲存 tag

- ✅ Tag policy 可以協助標準化 tag 的命名格式，例如大小寫規範。

- ❌ 但無法自動偵測/報告未被標記的資源。

- ❌ S3 Object Lock 在這裡沒有意義，它是用來防止檔案被刪改，不適合處理 tag 稽核。

建立 Lambda function 並搭配 EventBridge 定時檢查

- ✅ 可行，但你需要寫程式、維護排程，還要自己處理報表與警示。

- ❌ 比起 AWS Config，需要較高的操作成本與維護負擔。

使用 SCP 偵測未正確標記的資源

- ❌ SCP（Service Control Policy）是用來設限 IAM 最多能被授權什麼操作，不能用來「偵測」哪些資源有或沒有 tag。

- ✅ SCP 可以用來「防止未來創建未打 tag 的資源」，但無法稽核已存在的資源。

🔧 實作建議（若你想進一步操作）：

在 AWS Config 中啟用 managed rule：

---
# 2025-07-22 筆記

公司希望組織管理 AWS 資源的支出追蹤方式，並且需要在每月底生成一份報告，彙總每個部門的總計帳單費用。

以下哪一個方案能滿足需求？

正確答案 ✅

將資源加上部門名稱的標籤，並啟用成本分配標籤。

Tag resources with the department name and enable cost allocation tags.

其他選項：

❌ 建立 AWS 服務的成本與使用報告，分別針對每個部門使用的服務。

Create a Cost and Usage report for AWS services that each department is using.

❌ 使用 AWS Cost Explorer 查看花費，並根據資源篩選使用資料。

Use AWS Cost Explorer to view spending and filter usage data by Resource.

❌ 將資源加上部門名稱的標籤，並在 AWS Budget 設定預算動作。

Tag resources with the department name and configure a budget action in AWS Budget.

總體解釋：

AWS 的「標籤 (Tags)」是一種用來組織資源的標籤機制，由「鍵 (Key)」和「值 (Value)」組成，例如：

- Department = Marketing、Department = IT。

啟用 成本分配標籤 (Cost Allocation Tags) 後：

- AWS 會在 Billing 與 Cost Management 控制台中提供一份 成本分配報告（CSV 檔），可按照標籤分類追蹤每個部門的實際花費。

- 您可以按業務類別（如部門、專案、應用程式）來細分帳單。

這是最有效率、最官方推薦的跨部門成本追蹤方式。

為什麼其他選項錯誤：

- AWS Budgets 主要用來 設定預算限制和通知警示，不是用來生成每月報表。

- Cost Explorer 的「Resource」過濾器功能有限，尤其主要針對 EC2，無法跨多種服務完整追蹤部門成本。

- Cost and Usage Report (CUR) 雖然提供詳細帳單資訊，但預設是根據服務分類，不會針對「部門」分類；若要按部門分類仍須使用標籤。

📌 結論：

✅ 正確方案：為資源加上部門標籤，並啟用成本分配標籤 (Cost Allocation Tags)。

一間組織需要控管對數個 Amazon S3 bucket 的存取權限，該組織計畫使用 Gateway Endpoint 的方式來讓受信任的 bucket 可被存取。以下哪一個做法最適合滿足這個需求？

✅ 正確答案：

- 針對受信任的 S3 bucket 產生 endpoint policy (Generate an endpoint policy for trusted S3 buckets)

❌ 錯誤選項：

- 為受信任的 VPC 產生 bucket policy (Generate a bucket policy for trusted VPCs)

- 為受信任的 S3 bucket 產生 bucket policy (Generate a bucket policy for trusted S3 buckets)

- 為受信任的 VPC 產生 endpoint policy (Generate an endpoint policy for trusted VPCs)

📌 詳細說明：

Gateway Endpoint 是一種 VPC Endpoint，讓您的 VPC 裡的資源可以透過私有網路連接 Amazon S3 或 DynamoDB，不需要經過 Internet Gateway 或 NAT Gateway。

當您建立 Gateway Endpoint 時，可以附加一個 Endpoint Policy，用來控制透過該 endpoint 存取 AWS 服務的權限，尤其可以：

- 指定「哪些 S3 bucket 可以被存取」

- 限定「哪些 IAM 使用者或角色可以透過該 endpoint 存取資源」

在本案例中，需求是 只允許受信任的 S3 bucket 存取，最佳實踐是直接透過 endpoint policy 控制，而非逐個設定 S3 bucket policy。

🎯 總結：

- ✅ endpoint policy（針對 S3 bucket）：適合集中管理，減少維護成本。

- ❌ bucket policy：雖然可行，但需每個 bucket 單獨設定，管理負擔重。

- ❌ 針對 VPC 的 policy：與本需求不符，因為目標是「限制 bucket 存取權」，不是限制「哪個 VPC 可用」。

最省時且容易管理的方案：透過 endpoint policy 控制 S3 bucket 存取權限。

一間軟體公司在 AWS 和本地端（on-premises）伺服器上同時託管資源。您被要求為這些同時使用雲端與本地資源的應用程式設計一個「解耦式架構（decoupled architecture）」。

以下哪些選項是正確的？（請選擇兩個）

✅ 正確答案：

- 使用 SWF（Simple Workflow Service）來讓本地端伺服器和 EC2 執行個體共同參與解耦式應用程式。

- 使用 SQS（Simple Queue Service）來讓本地端伺服器和 EC2 執行個體共同參與解耦式應用程式。

❌ 錯誤選項：

- 使用 RDS 同時支援本地端伺服器和 EC2（RDS 是資料庫服務，並非訊息佇列，不具備解耦功能）

- 使用 VPC Peering 來連接本地端伺服器與 EC2（本地端應使用 Direct Connect 或 VPN，VPC Peering 無法連接 on-premises）

- 使用 DynamoDB 同時支援本地端伺服器和 EC2（DynamoDB 也是資料庫服務，不適用於解耦應用）

📌 詳細說明：

解耦式架構的核心目標是：

- 讓應用程式的不同部分彼此獨立運作，降低依賴性

- 透過「非同步通訊」來協調不同系統或服務的互動

🎯 總結：

如果你的目標是讓 on-premises 和 AWS 的應用程式彼此 非同步協作、彼此獨立解耦，最佳選擇是：

- SQS：做訊息緩衝、非同步溝通

- SWF：做跨系統工作流程管理

一家公司希望簡化在 AWS Organization 中建立多個 AWS 帳號的流程。每個組織單位（OU）都必須能夠建立新帳號，且這些帳號必須套用經安全團隊預先核准的標準化設定與網路配置，以確保整個組織的基礎環境一致。

以下哪一個方案最省力、最容易實作？

✅ 正確答案：

- 建立 AWS Control Tower Landing Zone，啟用預設的 guardrails（防護欄）來強制執行政策或偵測違規行為。

❌ 錯誤答案：

- 使用 AWS Config aggregator 來整合全組織的帳號與區域資料，佈署 conformance pack 來標準化基線與網路設定。
❌ 錯誤原因：AWS Config 是用來監控資源合規性，無法自動創建帳號或佈署網路設定，且 conformance pack 無法處理帳號建立流程。

- 使用 AWS Systems Manager OpsCenter 來集中創建 AWS 帳號，並使用 AWS Security Hub 強制執行政策與偵測違規行為。
❌ 錯誤原因：OpsCenter 主要用於事件與問題管理，無法建立帳號；Security Hub 用於安全檢測，不負責帳號佈署。

- 使用 AWS Resource Access Manager (RAM) 來建立新帳號並標準化組織單位的基線與網路設定。
❌ 錯誤原因：RAM 是用來跨帳號分享資源，不負責帳號建立與網路設定。

🎯

解析：

AWS Control Tower 是最省力的選擇，因為：

- 提供一站式帳號建立流程（Account Factory）

- 自動化設定最佳實踐（基線、VPC 架構、IAM 設定等）

- 內建 Guardrails：強制防止違規行為（SCP）、偵測非合規行為（AWS Config）、自動修正

- 可以跨 OU 與帳號套用標準化設定

- 只需一次性佈署 Landing Zone，後續新帳號自動繼承標準設定

✅ 結論：

如果你想用最少人力與操作時間管理多帳號架構，AWS Control Tower 是最佳選擇。

題目翻譯：

作為公司「營運持續計畫（Business Continuity Plan）」的一部分，IT 總監指示 IT 團隊儘快建立公司所有 Amazon EC2 執行個體之 EBS 磁碟區 的自動備份機制。

以下哪一個方案是最快速且最具成本效益的方式來自動備份所有 EBS 磁碟區？

正確答案：

✅ 使用 Amazon Data Lifecycle Manager (Amazon DLM) 來自動化建立 EBS snapshots。

選項翻譯：

- ❌ 錯誤： 為了實現自動化，建立一個排程任務，透過 AWS CLI 定期執行 create-snapshot 指令來定時對生產環境的 EBS 磁碟區建立快照。

- ❌ 錯誤： 使用 Amazon Storage Gateway，將 EBS 磁碟區作為資料來源，透過 storage gateway 將備份儲存到本地端伺服器。

- ✅ 正確： 使用 Amazon Data Lifecycle Manager (Amazon DLM) 來自動化 EBS snapshots 的建立。

- ❌ 錯誤： 在 Amazon S3 中使用 EBS-cycle policy 來自動備份 EBS 磁碟區。（此功能不存在）

中文總體解釋：

Amazon Data Lifecycle Manager (DLM) 是 AWS 提供的免費服務，可以幫助您自動化：

- EBS 快照的建立、

- 保留期限的設定、

- 過期自動刪除。

透過簡單設定策略，您不需要撰寫 Shell Script，也不需額外建立 Lambda、CLI 排程等額外維運流程，就能做到符合審計與備份需求的自動快照備份，最省時且免額外成本。

---
# 2025-07-21 筆記

問題 4

✅ 正確

一家製藥公司在內部資料中心和 AWS 雲端上都有資源。公司要求所有軟體架構師必須使用儲存在 Active Directory 的內部網路憑證來存取兩邊的資源。

在此情境下，下列哪一項可以滿足此需求？

❌ 使用 Amazon VPC

✅ 設定基於 Microsoft Active Directory Federation Service 的 SAML 2.0 聯邦認證

❌ 使用 IAM 使用者

❌ 設定基於 Web Identity Federation 的 SAML 2.0 聯邦認證

總體解釋

由於公司使用 Microsoft Active Directory，而其實作了 SAML（Security Assertion Markup Language），因此可以透過 SAML 聯邦認證方式來存取 AWS。這樣一來，使用者可以直接使用內部網路帳號來登入 AWS。

AWS 支援 SAML 2.0 的身分聯邦（identity federation），這是一種開放標準，許多身份提供者（IdP）皆支援。透過此功能，可以實現單一登入（SSO），讓使用者無需建立 IAM 使用者，即可登入 AWS 管理控制台或呼叫 AWS API。

設定 SAML 2.0 聯邦認證的一般流程如下：

公司內部必須有支援 SAML 2.0 的 IdP，例如 Microsoft Active Directory Federation Service (AD FS)、Shibboleth 或其他相容的 SAML 2.0 身份提供者，並將該 IdP 與 AWS 帳戶建立信任關係。

因此，正確答案是：設定基於 Microsoft Active Directory Federation Service 的 SAML 2.0 聯邦認證。

選項說明：

- 「設定基於 Web Identity Federation 的 SAML 2.0 聯邦認證」不正確，因為 Web Identity Federation 主要是讓使用者透過 Amazon、Facebook、Google 等外部 IdP 登入，並未使用 Active Directory。

- 「使用 IAM 使用者」不正確，因為題目要求使用現有的 Active Directory 憑證，而不是建立 IAM 使用者。

- 「使用 Amazon VPC」不正確，因為 VPC 是在 AWS 雲端內建立邏輯隔離網路，與使用者登入或身份認證無關。

一家軟體開發公司使用 AWS Lambda 的無伺服器運算來建構和執行應用程式，無需設定或管理伺服器。該公司有一個 Lambda 函數會連接到 MongoDB Atlas（常見的資料庫即服務平台 DBaaS），同時還會呼叫第三方 API 以取得應用程式所需的資料。公司指派一位開發人員為 DEV、SIT、UAT 和 PROD 環境建立 MongoDB 的資料庫主機名稱、使用者名稱、密碼，以及 API 憑證等環境變數。

考量到 Lambda 函數儲存了敏感的資料庫與 API 憑證，為了防止團隊內其他開發人員或任何人以明文形式看到這些憑證，以下哪個選項可以提供最佳安全性？

✅ 您答對了

建立新的 AWS KMS 金鑰，使用加密輔助工具（encryption helpers）透過 AWS Key Management Service 來儲存及加密敏感資訊。

❌ 啟用 SSL 加密，透過 AWS CloudHSM 來儲存與加密敏感資訊。

❌ 不需要做任何事情，因為 Lambda 預設會使用 AWS Key Management Service 來加密環境變數。

❌ Lambda 不會為環境變數提供加密功能，應該將程式碼部署至 Amazon EC2 instance。

總體解釋

當您在 Lambda 函數中建立或更新環境變數時，AWS Lambda 會自動使用 AWS KMS 來加密這些變數。在函數被觸發時，Lambda 會將這些值解密後提供給函數代碼使用。

第一次在某個區域內建立或更新 Lambda 函數且使用環境變數時，AWS 會自動為您建立一個預設的服務金鑰（default service key）。該金鑰用來加密環境變數。不過若您希望額外提高安全性，您可以自訂一把 AWS KMS 金鑰，並使用加密輔助工具來加密環境變數。自訂金鑰可以讓您有更高的管理靈活性，例如設定金鑰輪換、啟用或停用金鑰、定義存取控制，以及稽核加密金鑰的使用情況。

因此最佳答案是：

- 建立新的 AWS KMS 金鑰並使用加密輔助工具來加密敏感資訊。

選項說明：

- 「不需要做任何事情」錯誤，雖然 Lambda 預設會加密環境變數，但若團隊內有開啟 Lambda 控制台的權限，仍可能看到明文值，因此建議自訂 KMS 金鑰。

- 「啟用 SSL 加密」錯誤，SSL 只能保障資料在傳輸過程中的加密，但無法防止資料靜態儲存時被看見。AWS KMS 才是保護靜態資料的首選。

- 「Lambda 不提供加密功能，建議用 EC2」錯誤，因為 Lambda 本身就提供環境變數加密的功能。

一家電信公司計劃為開發人員提供 AWS Console 存取權限。根據公司政策，必須使用身份聯邦（identity federation）與基於角色的存取控制（role-based access control）。目前公司已經透過企業內部 Active Directory 的群組分配角色。

在此情境下，下列哪兩個服務可以提供開發人員 AWS Console 存取權限？（選兩個）

❌ AWS Lambda

❌ AWS Directory Service Simple AD

❌ IAM Groups

✅ IAM Roles

✅ AWS Directory Service AD Connector

總體解釋

AWS Directory Service 提供多種方式，讓您能夠將 Amazon Cloud Directory 與 Microsoft Active Directory (AD) 整合至 AWS 服務中。目錄服務用來儲存使用者、群組及裝置資訊，管理員透過這些服務來控管資訊與資源的存取權限。

由於公司已經使用內部 Active Directory，最佳解法是使用 AWS Directory Service AD Connector，這可以簡單整合 AWS 與本地端 Active Directory。另外，因為角色已經透過 Active Directory 群組分配，所以建議搭配 IAM Roles 使用。透過 AD Connector 與 VPC 整合之後，您可以將 IAM Role 指派給來自 Active Directory 的使用者或群組。

因此正確答案為：

- AWS Directory Service AD Connector

- IAM Roles

錯誤選項說明：

- 「AWS Directory Service Simple AD」不適用，因為它只提供部分 Managed Microsoft AD 的功能，且無法連接公司現有的 AD 環境。

- 「IAM Groups」僅用於管理 IAM 使用者的群組權限，無法對接 Active Directory。

- 「AWS Lambda」主要用於無伺服器運算，與身份驗證及 Console 存取無關。

一家公司將其電子商務網站託管在 Amazon EC2 的 Auto Scaling 群組上，並透過 Application Load Balancer (ALB) 分流。解決方案架構師發現該網站收到了大量來自不同系統、且 IP 位址頻繁變動的非法外部請求。為了解決效能問題，架構師必須實作一個方案來阻擋這些請求，同時盡量不影響合法流量。

以下哪個選項符合這個需求？

❌ 建立自訂的安全群組規則來封鎖 ALB 的惡意請求

❌ 建立自訂的網路 ACL，並將其關聯至 ALB 子網路來封鎖惡意請求

✅ 建立 AWS WAF 的速率限制規則，並將 web ACL 關聯至 ALB

❌ 建立 AWS WAF 的一般規則，並將 web ACL 關聯至 ALB

總體解釋

AWS WAF（Web Application Firewall）可以和 CloudFront、Application Load Balancer、API Gateway 以及 AWS AppSync 整合，來保護您的網站與應用程式。特別是在 ALB 上，WAF 規則可於區域層級執行，有效保護公開或內部資源。

速率限制規則（rate-based rule）可以追蹤每個來源 IP 的請求速率，當某個 IP 的請求速率超過指定限制時，自動對其觸發規則行為（例如封鎖）。您可以設定 5 分鐘內的請求次數上限，當惡意 IP 過度發送請求時，可以暫時封鎖該 IP，直到請求速率降低為止。

因此，正確答案是：

✅ 建立 AWS WAF 的速率限制規則，並將 web ACL 關聯至 ALB。

錯誤選項說明：

- 「建立一般 WAF 規則」錯誤，因為一般規則只能依據特定條件封鎖，無法依據請求速率自動暫時封鎖 IP。

- 「自訂 NACL」錯誤，雖然 NACL 可封鎖特定 IP，但無法根據請求次數動態調整，且 IP 會頻繁變動。

- 「安全群組」錯誤，安全群組僅允許流量，無法拒絕流量，也無法做速率限制。

一家公司需要部署至少兩台 Amazon EC2 執行個體來支援正常工作負載，並且在高峰期自動擴展至六台 EC2 執行個體。此架構需具備高可用性與容錯能力，因為系統負責處理關鍵任務型應用程式。

身為解決方案架構師，應該採取以下哪個方案來達成需求？

❌ 建立 Auto Scaling 群組，將最小容量設為 2，最大容量設為 6，在 2 個可用區部署，每個 AZ 1 台執行個體

❌ 建立 Auto Scaling 群組，將最小容量設為 2，最大容量設為 6，全部部署在可用區 A，部署 4 台

✅ 建立 Auto Scaling 群組，將最小容量設為 4，最大容量設為 6，可用區 A 和 B 各部署 2 台

❌ 建立 Auto Scaling 群組，將最小容量設為 2，最大容量設為 4，可用區 A 和 B 各部署 2 台

總體解釋

Amazon EC2 Auto Scaling 可確保您的應用程式始終擁有足夠的 EC2 執行個體來處理負載。透過 Auto Scaling 群組，您可以設定最小與最大執行個體數量，確保系統在這個範圍內自動調整資源。

要達成高可用與容錯，必須將執行個體跨多個可用區部署。這樣即使某一個可用區發生故障，您的應用程式仍有足夠的執行個體持續運作。為了確保即便一個 AZ 當機時仍有至少 2 台執行個體運行，建議：

- 最小容量設為 4（每個 AZ 2 台）

- 最大容量設為 6（高峰期可自動擴展）

正確答案：

✅ 建立 Auto Scaling 群組，最小 4 台、最大 6 台，可用區 A 和 B 各部署 2 台。

錯誤選項原因：

- 「最小 2 台，每個 AZ 1 台」：如果某個 AZ 當機，會只剩 1 台，無法保障高可用性。

- 「4 台集中在單一 AZ」：缺乏跨 AZ 部署，一旦 AZ 當機，所有執行個體會同時失效。

- 「最小 2、最大 4」：高峰期需求為 6 台，最大容量設 4 無法滿足流量。

一家公司在 AWS 上有由 Linux 和 Windows EC2 執行個體組成的雲端架構，全天候 24/7 處理大量財務資料。為確保系統高可用性，解決方案架構師需要建立一套方案，能夠監控所有執行個體的記憶體與磁碟使用率。

以下哪個方案最適合？

❌ 使用 Amazon Inspector 並安裝 Inspector agent 到所有 EC2 執行個體

❌ 使用 EC2 預設 CloudWatch 設定與 AWS Systems Manager (SSM) Agent

❌ 啟用 EC2 Enhanced Monitoring 並安裝 CloudWatch agent

✅ 安裝 Amazon CloudWatch agent 到所有 EC2 執行個體，收集記憶體與磁碟使用率資料，並在 CloudWatch 控制台查看自訂指標

總體解釋

- Amazon CloudWatch 預設指標：提供 CPU、網路、磁碟 I/O 基礎指標，但不包含記憶體與磁碟空間使用率。

- CloudWatch agent：是唯一能跨 Windows/Linux 收集記憶體與磁碟使用率的官方方案。

- Enhanced Monitoring：僅適用於 RDS，EC2 沒有此功能。

- Amazon Inspector：用於安全漏洞掃描，無法監控資源使用率。

- SSM Agent：提供管理與操作功能，並不監控資源指標。

---
# 2025-07-20 筆記

題目解析

這題的情境是：

- 一個全球性的影片教學平台，學生觀看影片，授權的內容開發者上傳影片

- 上傳的影片放在 S3（us-east-2）

- 公司額外建立了 S3 bucket 在 eu-west-2 與 ap-southeast-1

- 需求：減少開發者上傳與學生觀看的延遲，且對 application 做最少改動

這題考兩個概念：

S3 Replication (複寫)：幫助資料自動同步到其他 bucket

S3 Multi-Region Access Point (MRAP)：讓 application 自動存取「最近的」bucket，不用自己寫邏輯判斷

詳細解答

✅ 正確答案：

- A. Configure one-way replication from the us-east-2 S3 bucket to the eu-west-2 S3 bucket. Configure one-way replication from the us-east-2 S3 bucket to the ap-southeast-1 S3 bucket.

- D. Create an S3 Multi-Region Access Point. Modify the application to use the Amazon Resource Name (ARN) of the Multi-Region Access Point for video streaming. Do not modify the application for video uploads.

📝 解釋：

- A 選項理由：

- 

- D 選項理由：

- 

❌ 錯誤選項說明：

- B 錯：

- 

- C 錯：

- 

- E 錯：

- 

🟣 最終結論：

選擇 A + D：

- A：確保資料正確同步到其他地區

- D：讓學生自動存取最近的 bucket，不改動上傳邏輯

題目解析

這題情境是：

- 公司要提供一個RESTful API 的 web analytics 服務

- 數百萬使用者要透過驗證才能存取 API

- 重點是「最高的營運效率（MOST operational efficiency）」

關鍵要素：

- RESTful API

- 驗證需求

- 高流量、多用戶數

- 高營運效率 → 少維護、低成本、雲端託管最佳方案

詳細解答

✅

正確答案：A. Cognito user pool + API Gateway REST API + Cognito authorizer

📝 原因說明：

- Amazon Cognito user pool：專門用來做user authentication（登入驗證），支援社交登入、MFA、密碼管理，全託管 → 超省事

- API Gateway REST API：原生支援用 Cognito 作為 authorizer，驗證邏輯不用自己寫，IAM policies 自動整合

- Operational Efficiency：

- 

❌ 錯誤選項解析：

- B. Cognito identity pool + HTTP API：

- 

- C. Lambda function + Lambda authorizer：

- 

- D. IAM user + IAM authorizer：

- 

🟣

總結：

🎯

最推薦選擇：A

題目解析

這題是單一 EC2 instance 運行的 legacy system：

- 應用無法修改

- 無法水平擴展（只能單 instance 運行）

- 重點：提升 recovery time（縮短恢復時間）

詳細解答

✅ 正確答案：

C. CloudWatch alarm 恢復 EC2 instance

📝 解釋：

- CloudWatch EC2 recovery alarm：

- 

- ✅ 最符合需求：不可修改程式碼，又要縮短恢復時間

❌ 錯誤選項解析：

- A. Termination protection ❌

- 

- B. Multi-AZ ❌

- 

- D. RAID 配置 ❌

- 

🎁 最終總結：

🎯 正確答案：

C

題目解析

這題的前提是：

- 給了一段 IAM Policy JSON，範例權限是：

- 

- 問：可以將這份 identity-based policy 附加在哪些 IAM principal？

解釋：Identity-based policy 是什麼？

- Identity-based policies 可以附加到：

- 

它是針對「人或角色」來限制的，不是綁定在資源上（那是 resource-based policy）。

📝 各選項逐項分析

🎯 最佳答案：

✅ A. Role

✅ B. Group

如果你想，我可以順便整理一份：

---
# 2025-07-19 筆記

題目解釋

題目背景：

- 公司目前在資料中心使用 SMB 檔案伺服器。

- 需求分段：

- 

- 目標：用 AWS 儲存解法滿足這兩種存取需求。

題目關鍵點解析

選項詳解

✅ B. S3 File Gateway + S3 Glacier Deep Archive

- ✅ SMB 使用者可透過 File Gateway 存取最新資料（高頻資料）

- ✅ 7天後轉 S3 Glacier Deep Archive：可設定 LifeCycle Policy 完成

- ✅ Glacier Deep Archive 最大取回時間 24 小時，符合題目需求

- ✅ 管理成本低，不需改變使用者行為

- 結論：✅ 最佳答案

❌ A. DataSync 直接複製資料到 AWS

- ❌ DataSync 可用來搬遷資料，但：

- 

- 結論：❌ 不符合需求

❌ C. FSx File Gateway + S3 Lifecycle

- ❌ FSx File Gateway 是用來把 on-prem SMB 存取指向 FSx for Windows File Server（非 S3）

- ❌ FSx 不支援 S3 lifecycle rule

- 結論：❌ 架構錯誤，不符題目情境

❌ D. 每個使用者個別存取 S3 + S3 Glacier Flexible Retrieval

- ❌ 需改變使用者從 SMB 改成直接用 S3 存取

- ❌ 額外管理成本增加

- 結論：❌ 違反「低維護、現有 SMB 存取」需求

✅ 最佳答案

✅ B. Create an Amazon S3 File Gateway to increase the company’s storage space. Create an S3 Lifecycle policy to transition the data to S3 Glacier Deep Archive after 7 days.

📌 總結

題目解釋

題目背景：

- 公司每天透過 SFTP 接收報表檔案

- 需要每天晚上進行 批次處理

- 希望搬遷至 AWS Cloud

- 需求：

- 

各選項解析

❌ A. AWS Transfer for SFTP + EFS + EC2 Auto Scaling

- 優點：

- 

- 缺點：

- 

- 結論：❌ 非成本效益最佳

❌ B. EC2 + 自架 SFTP + EBS

- 優點：

- 

- 缺點：

- 

- 結論：❌ 高維運負擔

❌ C. EC2 + 自架 SFTP + EFS

- 優點：

- 

- 缺點：

- 

- 結論：❌ 維運高 + 成本高

✅ D. AWS Transfer for SFTP + S3 + EC2 Auto Scaling

- ✅ Transfer for SFTP：全託管 SFTP 服務

- ✅ S3：便宜、彈性儲存，具高可用性與韌性

- ✅ EC2 Auto Scaling：可設定 scheduled scaling，批次運算只在特定時間啟動 → 節省成本

- ✅ 零管理 SFTP server，零管理儲存空間

- 結論：✅ 最省管理成本且高度可用方案

最佳答案

✅ D. Deploy AWS Transfer for SFTP and an Amazon S3 bucket for storage. Modify the application to pull the batch files from Amazon S3 to an Amazon EC2 instance for processing. Use an EC2 instance in an Auto Scaling group with a scheduled scaling policy to run the batch operation.

📌 核心邏輯總結

題目解析

這題情境是：

- 公司網站透過 CloudFront → ALB → EC2 Auto Scaling Group 架構

- AWS WAF 已經用來防止 SQL injection

- 目標：封鎖特定外部惡意 IP，避免其存取整個網站

選項逐一解析

A. ❌

錯誤

- Network ACL (NACL) 是用於 VPC 子網路層級，但 CloudFront 屬於 AWS Edge 網路層級，不在 VPC 內，NACL 無法作用於 CloudFront。

✅ B.

正確答案

- AWS WAF 是專門設計來封鎖特定 IP，而且可以掛載在 CloudFront distribution 上面，可以直接在 AWS WAF 裡面新增 IP set rule 封鎖該 IP。

- 優勢：

- 

C. ❌

錯誤

- Network ACL 是針對 VPC 子網路層級，但流量已經先經過 CloudFront 與 ALB，不應該直接動 NACL，且管理不便。

D. ❌

錯誤

- Security Group 是 狀態型防火牆，通常只允許的流量 (不是用來做封鎖大量單一 IP 的用途)，管理性差、維護負擔大。

🎯 總結

最佳答案：

✅ B. Modify the configuration of AWS WAF to add an IP match condition to block the malicious IP address.

題目解析

題目情境：

- 公司有 NFS 伺服器在地端資料中心

- 要定期備份少量資料到 Amazon S3

- 要求：最具成本效益的方案

選項解析

A. ❌ AWS Glue

---
# 2025-07-18 筆記

題目說明

核心需求：

- 公司需要將資料從 on-premises 遷移到 Amazon S3

- ✅ 資料量持續增加

- ✅ 自動驗證資料完整性

- ✅ 線上遷移

選項解析

✅

B. AWS DataSync

- ✅ AWS DataSync 是針對 on-premise → S3/FSx/EFS 的線上同步遷移服務

- ✅ 內建資料完整性檢查：

- 

- ✅ 支援高速資料傳輸，專為大量資料設計

- ✅ 無須自行開發校驗機制，最小維運負擔

- 結論：✅ 最佳答案

A.

AWS Snowball Edge

- ❌ 適合離線大規模資料遷移

- ❌ 資料完整性校驗只在裝置回 AWS 時由 AWS 執行

- ❌ 題目指定 線上遷移，Snowball Edge 不符合需求

- 結論：❌ 不適用

C.

Amazon S3 File Gateway

- ❌ 適合小量資料做 hybrid access，並不適合大規模資料遷移

- ❌ 無自動資料校驗，且適用場景為檔案共享與同步而非完整遷移

- 結論：❌ 不符合大規模資料遷移需求

D.

S3 Transfer Acceleration

- ❌ Transfer Acceleration 是加速 S3 上傳速度的功能

- ❌ 不支援自動資料完整性檢查

- ❌ 適合用於全球加速小批量資料，不適合 on-premises 大量資料遷移

- 結論：❌ 不符合完整性驗證與大量遷移需求

✅ 最佳答案

✅ B. Deploy an AWS DataSync agent on premises. Configure the DataSync agent to perform the online data transfer to an S3 bucket.

📌 理由總結：

- ✅ DataSync 內建 checksum 完整性校驗

- ✅ 線上高速遷移

- ✅ 最小維運負擔，適合資料量持續增加的情境

題目說明

核心需求：

- CloudTrail logs 來自多個 AWS account

- 集中儲存在一個 S3 bucket

- ✅ 必須長期保存

- ✅ 隨時可查詢

選項解析

✅

A. S3 + Athena 查詢

- ✅ CloudTrail logs 儲存在 S3

- ✅ Amazon Athena 可以直接查詢 S3 上的 CloudTrail log（Parquet/JSON 格式皆可）

- ✅ 最低維運負擔：

- 

- ✅ 官方 AWS 最佳實踐架構

- 結論：✅ 最佳答案

❌ B. Amazon Neptune

- ❌ Neptune 是圖形資料庫，適用於 social graph、知識網絡等結構

- ❌ CloudTrail logs 是 結構化 log 資料，不適用圖形資料庫

- 結論：❌ 不符合使用情境

❌ C. DynamoDB + QuickSight

- ❌ CloudTrail 不直接發送到 DynamoDB

- ❌ QuickSight 適合可視化報表，不是最佳查詢歷史 logs 工具

- 結論：❌ 不適合查詢大量 log 檔

❌ D. Athena Notebook

- ❌ Athena Notebook 是開發輔助功能，不是儲存或查詢 CloudTrail log 的主要方案

- ❌ CloudTrail 無法直接發送 logs 到 Athena notebook

- 結論：❌ 錯誤方案

✅ 最佳答案

✅ A. Use the CloudTrail event history in the centralized account to create an Amazon Athena table. Query the CloudTrail logs from Athena.

📌 總結說明：

- ✅ CloudTrail logs → S3

- ✅ Athena + Glue Table → 即時 SQL 查詢

- ✅ 按查詢次數付費，無需額外搬資料，維運成本最低

題目解析

題目情境：

- 一家公司有 5 個 OU，每個 OU 代表一個子公司。

- 其中 R&D 業務要獨立出去，成立新的 AWS Organization。

- 已經為 R&D 建立了新的 management account（新組織的 root 帳戶）。

任務：

- 如何讓 R&D 的 AWS account 正確從原公司轉移到新成立的 AWS Organization。

選項逐一解析

❌ A. 同時加入兩個 organization

- ❌ AWS account 不可能同時存在於兩個 Organizations：

- 

- 結論：❌ 技術上不可行

✅ B.

先離開舊 organization → 再加入新 organization

- ✅ 正確流程：

- 

- ✅ AWS 官方建議：account 轉移需先脫離現有 org，才能被其他 org 邀請

- 結論：✅ 最佳答案

❌ C. 新建 account + 遷移資源

- ❌ 遷移 account ≠ 創新 account：

- 

- ❌ 建新帳戶會涉及大量人工 資源遷移（EC2、S3、IAM policy 等），維運負擔極大

- 結論：❌ 不符合最少維運原則

❌ D. Management account 加入另一個 organization

- ❌ Management account (root account) 不能被其他 org 邀請成為 member account

- ❌ 根據 AWS 結構設計：

- 

---
# 2025-07-17 筆記

題目解釋

- 情境：

- 

詳細解析

A.

購買 Reserved Instance + 放大 RDS instance

- ✅ Reserved Instance 可節省 40%-70% 長期成本

- ✅ 單一 DB instance 升級 可增加 CPU、記憶體與 IOPS，不增加額外基礎設施

- ✅ 最符合「不加基礎設施，提升容量並省錢」的條件

- 結論：✅ 最佳選擇

B.

開啟 Multi-AZ

- ✅ 提升 可用性（HA）

- ❌ 不會提升效能，無法處理更大 workload（只做同步複製）

- 結論：❌ 不解決性能問題

C.

Reserved Instance + 增加 RDS instance

- ❌ 增加另一個 DB instance = 新增基礎設施，題目禁止

- 結論：❌ 不符條件

D.

改用 On-Demand

- ❌ On-Demand 比 Reserved Instance 昂貴許多

- ❌ 無法提供「成本效益最佳」解法

- 結論：❌ 最不成本效益

最佳答案

✅ A. Buy reserved DB instances for the total workload. Make the Amazon RDS for PostgreSQL DB instance larger.

📌 理由：

- 不增加額外基礎設施

- 提升效能，同時透過 Reserved Instance 控制成本

題目解釋

這題考點是：

- 遊戲網站，多人即時競賽

- 三層架構（Web、應用層、RDS for MySQL 資料層）

- 需求：

- 

詳解

逐一分析選項：

A.

ElastiCache for Memcached

- ✅ 快速記憶體快取，可加速排行榜查詢

- ❌ Memcached 無持久化功能，資料存在 RAM，重啟資料會遺失

- ❌ 無內建排序結構，排行榜邏輯需額外實作

- 結論：❌ 不符合持久性與排行榜即時計算需求

B. ✅

ElastiCache for Redis

- ✅ Redis 支援 sorted set，天生適合排行榜需求

- ✅ 支援持久化（RDB, AOF），即使暫停或重啟也能保留分數

- ✅ 即時更新、快速查詢，有效減輕資料庫壓力

- ✅ 支援多種資料結構與快速查詢

- 結論：✅ 最佳方案

C.

CloudFront 快取

- ❌ 適合靜態內容，不適合頻繁更新的排行榜（即時性需求）

- ❌ CloudFront 更新延遲通常數秒至數分鐘

- 結論：❌ 不適合

D.

RDS Read Replica

- ❌ read replica 雖可分散讀取壓力，但：

- 

- 結論：❌ 不推薦

最佳答案

✅ B. Set up an Amazon ElastiCache for Redis cluster to compute and cache the scores for the web application to display.

📌 原因說明：

- Redis 支援持久化與即時排行榜更新

- 效能高、延遲低，可同時滿足即時性與可恢復性需求

題目解釋

情境說明：

- Web 應用，資料庫目前在北美單一資料中心

- 全球用戶需求，需部署至多個 AWS 區域

- 關鍵需求：

- 

詳解

A.

DynamoDB Global Tables

- ❌ DynamoDB Global Tables 使用最終一致性（eventual consistency）

- ❌ 無法保證 strong consistency 與單一 primary 資料庫

- ❌ 不符合「單一主資料庫 + 全域一致性」需求

- 結論：❌ 不符合需求

B. ✅

Aurora Global Database（Aurora MySQL + 跨區讀取）

- ✅ Aurora Global Database 支援 單一 primary、全域同步

- ✅ 跨區域讀副本 讀取延遲 <1 秒

- ✅ 主資料庫 位於一個區域，其他區域部署讀取副本，滿足全域讀取與同步需求

- ✅ 適合全域應用 + 單一主資料庫架構

- 結論：✅ 最佳答案

C.

RDS for MySQL + Read Replica

- ❌ 跨區域 RDS Read Replica 延遲較高，通常秒級至數十秒

- ❌ 無「global database」功能

- ❌ 資料同步延遲無法保證 1 秒內

- 結論：❌ 不符合延遲與一致性需求

D.

Aurora Serverless + Lambda 同步

- ❌ Aurora Serverless 不支援 Global Database 模式

- ❌ Lambda event-driven 同步資料庫無法保證 全域一致性與低延遲

- ❌ 跨區資料庫同步需自建邏輯，管理與延遲風險高

- 結論：❌ 不推薦

最佳答案

---
# 2025-07-16 筆記

這題的重點在於：

- EC2 有 IPv6 位址

- EC2 需要主動對外連線

- 外部服務不得主動連回 EC2 (禁止 inbound traffic initiated externally)

選項分析：

A. ❌ NAT Gateway

- 適用於 IPv4 流量；

- 不支援 IPv6；

- 結論：不適用。

B. ❌ Internet Gateway

- 雙向流量（允許 inbound/outbound），不符合 “禁止外部連入” 的需求；

- 結論：不適合。

C. ❌ Virtual Private Gateway

- 適用於 VPN / Direct Connect；

- 不涉及一般 Internet 存取；

- 結論：不適合。

D. ✅ Egress-Only Internet Gateway

- 專門為 IPv6 設計的出口閘道；

- 只允許 EC2 主動發起 outbound 連線；

- 外部無法主動發起 inbound 連線；

- 完全符合題目條件。

🎯 最佳答案：

✅ D. Create an egress-only internet gateway and make it the destination of the subnet’s route table.

這題的情境是：

- SaaS 應用程式：Salesforce ↔️ Amazon S3 傳輸資料

- 需求：

- 

選項分析：

A.

AWS Lambda

- 雖然可以透過 Lambda API 呼叫來實作資料同步，但需要自訂程式邏輯、認證流程、錯誤處理；

- 開發與維運負擔高；

- ❌ 不符最少開發工作量。

B.

AWS Step Functions

- Step Functions 主要用來串聯多個 Lambda 任務或 AWS 服務；

- 還是需要額外寫 Lambda 或 API 呼叫來搬資料；

- ❌ 不符最少開發工作量。

C.

Amazon AppFlow

✅

- AppFlow 支援 Salesforce 與 S3 之間的安全資料流轉；

- 原生支援 KMS 加密 (CMK)、預設 TLS 傳輸加密；

- 幾乎 零開發負擔，在控制台幾步設定即可完成；

- ✅ 最符合需求與最低開發工作量。

D.

Custom connector

- 開發 Custom Connector 需要程式開發、除錯與維運；

- ❌ 開發負擔最高。

🎯 最佳答案：

✅ C. Create Amazon AppFlow flows to transfer the data securely from Salesforce to Amazon S3.

✅ 正確答案：B 和 C

詳細解析：

需求重點：

- EKS 自動擴展（pod 層級 + node 層級）

- 最少運維負擔

A. 用 Lambda function 來擴縮 EKS 集群

- ❌ 需要自訂邏輯與排程、維護 Lambda 程式碼

- 不是最少運維的標準作法

B. Kubernetes Metrics Server + Horizontal Pod Autoscaler ✅

- ✅ Pod 層級的自動擴展

- HPA 根據 CPU/記憶體或自訂指標自動調整 Pod 數量

- Kubernetes 原生方案，EKS 官方支援，低維運成本

C. Kubernetes Cluster Autoscaler ✅

- ✅ Node 層級的自動擴展

- 根據 Pod 排程需求自動增加/減少 EC2 node 數量

- 與 Auto Scaling Group 整合，無需額外維護

- EKS 官方推薦的自動擴展方案

D. API Gateway 與 EKS

- ❌ API Gateway 主要用來暴露 API，與 EKS 擴縮無直接關係

E. AWS App Mesh

- ❌ App Mesh 主要處理服務間流量路由與可觀察性，不負責擴縮

🟣

最佳答案：

- ✅ B. 使用 Kubernetes Metrics Server 啟用 HPA

- ✅ C. 使用 Kubernetes Cluster Autoscaler 管理 node 數量

這題考的是 多帳號管理 + 中央身分驗證 的設計方案，以下是詳細解析：

題目重點：

- 公司從「多個獨立 AWS 帳號」轉成「集中式、多帳號架構」。

- 未來會持續創建新帳號。

- 需求：透過公司內部的中央目錄服務（如 Active Directory）來做 AWS 帳號登入管理。

✅ 正確選項解析：

A. ✅

建立 AWS Organizations，開啟 All features，並用來統一管理 AWS 帳號。

- AWS Organizations 是官方建議的多帳號管理方式，可以集中帳單、管理 SCP、建立帳號，符合題目需求。

E. ✅

使用 AWS IAM Identity Center (前稱 AWS SSO)，並整合公司內部的身分驗證服務。

- IAM Identity Center 是 AWS 官方整合公司 LDAP/AD/SSO 的推薦方案，可用來統一管理多個 AWS 帳號的登入權限與使用者權限，最低運維負擔。

❌ 其他選項解析：

B. ❌

Amazon Cognito 用於應用程式的身分驗證，不適合用來管理 AWS 帳號存取。

- Cognito 適合 web/mobile app 身分驗證，與題目需求無關。

C. ❌

SCP 是用來限制帳號權限的，不能直接處理身份驗證或與 Directory 整合。

- SCP 是授權控管工具，並不是身分驗證工具。

D. ❌

AWS Organizations 本身不支援直接用 AWS Directory Service 作為登入來源，一定要透過 IAM Identity Center。

---
# 2025-07-15 筆記

✅ 題目解析：

公司使用三層架構：

- 流量流程：

- 

- 需求：改善「資料傳輸過程」（data in transit）的安全性

✅ 最佳答案：

A. Configure a TLS listener. Deploy the server certificate on the NLB

✅ 詳細解析：

為什麼選 A：

- ✅ TLS (傳輸層加密) 是最佳實踐來保護 data in transit。

- ✅ NLB 支援 TLS listener (Layer 4 TLS termination)：

- 

- ✅ 適合 sensor data 使用 TCP/UDP 協定的應用場景，維持低延遲 + 加密傳輸。

❌ 其他選項解析：

📝 小總結：

🎯

總結建議

：

✅ 選 A 是最小變更、高安全性、最適合的方案：透過 NLB 加 TLS listener 保護資料在傳輸途中的安全性。

✅ 題目解析：

公司需求：

- ✅ 每小時執行一次批次任務（batch job）

- ✅ CPU 密集型，on-premises 環境約用 64 vCPU、512 GiB RAM，平均 15 分鐘內完成

- ✅ 目標：維持效能（15分鐘完成）+ 最少維運負擔

✅ 最佳答案：

B. Use Amazon Elastic Container Service (Amazon ECS) with AWS Fargate

✅ 詳細解析：

為什麼選 B（ECS + Fargate）：

- ✅ Fargate 完全 serverless：

- 

- ✅ Fargate 可支援高效能批次處理：

- 

- ✅ 適合 批次作業（batch job）+ 低頻次觸發（每小時一次）。

- ✅ 自動按需計費，運行期間付費，結束後自動關閉，不浪費資源。

簡單流程：

使用 Amazon ECS Fargate Task 包裝原本應用邏輯。

使用 EventBridge 排程 每小時啟動任務。

自動擴展 & 簡單維護。

❌ 為什麼其他選項不適合：

📝 總結建議：

🎯

結論：

✅ 最佳選擇是 B — ECS Fargate 支援彈性擴展、高效能且免維運，最適合這類批次運算場景。

📖

題目解析

公司場景：

- ✅ EC2 instance 在 public subnet 並有 Elastic IP

- ✅ 預設 security group：沒有明確開 port

- ✅ Network ACL 被修改為 block all traffic

- ✅ 目標：開放 port 443 (HTTPS) 讓全世界可以存取 Web Server

✅

最佳答案：A 和 E

✅

詳解說明：

為什麼選 A：

- ✅ Security Group 是 Stateful（有回應流量自動允許）

- ✅ 需要在 security group 設定允許入站 port 443 (TCP) 來自 0.0.0.0/0（全球來源）

- 正確做法：

- 

為什麼選 E：

- ✅ Network ACL 是 Stateless，需同時開放 inbound 和 outbound

- ✅ 標準做法：

- 

- ✅ E 是符合 AWS 官方最佳實踐 的 NACL 設定方式

❌

為什麼其他選項不正確：

📝

總結表：

🎯

結論：

✅ 最佳答案：A + E，符合 AWS 實作規範，透過 SG + NACL 雙層設計開放 HTTPS 服務。

✅ 題目解析：

公司需求：

- ✅ 資料在傳輸過程中加密 (in transit)

- ✅ 資料在儲存時加密 (at rest)，且在上傳 S3 前即需加密

- ✅ 集中帳戶儲存 log

✅

最佳答案：C. Create bucket policies that require the use of server-side encryption with S3 managed encryption keys (SSE-S3) for S3 uploads.

✅

詳解說明：

為什麼選 C：

- ✅ SSE-S3（Server-Side Encryption with S3 managed keys）：

- 

- ✅ Bucket Policy 強制要求加密：

- 

- ✅ 傳輸加密：

- 

❌

為什麼其他選項不推薦：

📝

---
# 2025-07-14 筆記

✅ 正確答案：B. Use a Multi-AZ deployment of an Amazon RDS for MySQL DB instance with a General Purpose SSD (gp2) EBS volume.

✅ 解釋：

核心需求：

- 最小化中斷：RDS Multi-AZ 提供高可用性與故障容錯（failover），滿足這項需求。

- 穩定效能：gp2 提供穩定效能，且對於你需求的 ~1000 IOPS 峰值，性價比最佳。

- 降低成本：從 自管 EC2 + io2（高價位） 遷移到 RDS + gp2（便宜） 可顯著減少管理與儲存成本。

gp2 IOPS 說明

：

- gp2 提供 baseline IOPS = 3 IOPS/GB，1TB = 3000 IOPS。

- burst 模式 可短時間內達到更高 IOPS（最大 3000 IOPS），你的需求（1000 IOPS）完全能涵蓋。

- 若未來需求上升，也可改用 gp3（更靈活的 IOPS 設定）或 io1/io2，但目前不需要額外花費。

❌ 其他選項解析：

- A. io2 Block Express：適合數萬 IOPS 等極端負載，你只需要 1000 IOPS，不划算。

- C. S3 Intelligent-Tiering：這是物件儲存解法，不適合資料庫。

- D. EC2 active-passive：仍是自管解法，無法達成 最低管理負擔 的目標，且 failover 複雜。

📌 總結：

✅ 最佳答案：B

✅ 正確答案：C. Request an Amazon issued public certificate from AWS Certificate Manager (ACM) in the us-east-1 Region

✅

解釋：

- CloudFront 僅能與 ACM public certificates 在 us-east-1（N. Virginia）區域 搭配使用來設定自訂網域的 SSL/TLS。

- ACM 公開憑證（public certificate） 在 us-east-1 簡單申請，免費，無需額外成本。

- 這樣即可使用自訂網域（例如 mydomain.com）綁定 CloudFront distribution。

❌

其他選項解析

：

- A. private certificate：需要 ACM Private CA，會產生額外成本，且無法用於 CloudFront。

- B. private certificate in us-west-1：同樣為 private CA，不僅會產生費用，且 CloudFront 不支援 us-west-1 憑證。

- D. public certificate in us-west-1：CloudFront 只支援 us-east-1 的公開憑證，us-west-1 憑證 無法掛載至 CloudFront。

📌

總結：

✅ 正確選擇：C — ACM 公開憑證（us-east-1）

✅ 正確答案：C. Migrate the MySQL database to an Amazon Aurora global database. Host the primary DB cluster in the primary Region. Host the secondary DB cluster in the DR Region.

✅

解釋：

核心需求：

- 多區域災難復原（Multi-Region DR）

- 最少維運負擔（Least operational overhead）

為什麼選 C：

- Aurora Global Database 支援：

- 

❌

其他選項解析

：

- A. EC2 replication：

- 

- B. RDS Multi-AZ + Read Replica：

- 

- D. S3 CRR + 手動恢復：

- 

📌

總結建議

：

✅ 最佳答案：C — Aurora Global Database，低維運，高可用，多區域快速災難恢復

✅ 正確答案：A. Dedicated Reserved Hosts

✅

解釋：

- 關鍵需求：

- 

為什麼選 A（Dedicated Reserved Hosts）：

- Dedicated Hosts 允許：

- 

- Reserved Hosts：

- 

❌

為什麼其他選項不適合：

- B. Dedicated On-Demand Hosts：

- 

- C. Dedicated Reserved Instances：

- 

- D. Dedicated On-Demand Instances：

- 

📌

總結建議

：

✅ 最佳選擇：A - Dedicated Reserved Hosts

📖

題目說明：

這是一家電商公司，網站流量正在增加。他們的系統是典型的兩層架構（web tier + database tier），架設於 EC2 上。問題是隨著流量成長，發送行銷郵件和訂單確認信的速度變慢，而且常常會遇到寄信相關的技術問題。公司希望縮短寄信延遲，同時降低維運負擔。

核心需求：

- 快速穩定的發信

- 不想投入太多人力去處理寄信問題

✅

最佳答案：B. Configure the web instance to send email through Amazon Simple Email Service (Amazon SES).

✅

詳解：

Amazon SES 是 AWS 提供的 全託管型發信服務，解決以下問題：

- ✅ 高可用、高可靠性：可輕鬆擴展以處理高流量的 email 發送。

- ✅ 簡單整合：直接從 EC2 instance 呼叫 API 或 SMTP 發送郵件，不需要自建寄信伺服器。

- ✅ 降低維運負擔：不需要管理發信 IP、處理退信（bounce）、垃圾郵件（spam）等繁雜事務。

- ✅ 提升 deliverability：支援 SPF/DKIM/DMARC，可有效避免進垃圾信件夾。

結果：

---
# 2025-07-06 筆記

正確答案是：

✅ A. Update the route table for the private subnet to route the outbound traffic to an AWS Network Firewall. Configure domain list rule groups

✅ 解題重點分析：

❗需求整理：

- EC2 放在 private subnet

- 必須可以 連到特定軟體來源（第三方 URL）下載更新

- 其他所有網際網路流量都要封鎖

- EC2 裡面有 敏感資料 → 高安全性要求

✅ 為什麼選 A 是正確解：

AWS Network Firewall 提供以下功能：

- 支援 FQDN（domain name）filtering（可設定允許的網域名稱）

- 可作為 private subnet 的 NAT 出口點

- 可建立 domain list rule groups，只允許特定 URL/domain 的連線（如 *.trustedrepo.com）

- 其他所有網際網路流量則會被預設規則封鎖

✅ 完整解法流程：

在 private subnet 所在的 VPC 中部署 AWS Network Firewall

在 route table 中設定 0.0.0.0/0 的出站流量 要通過 AWS Network Firewall

在 Network Firewall 設定 只允許特定 FQDN（URL domain）的連線

所有非白名單的流量自動被封鎖

這種方式可最小化允許網路存取範圍，又避免在 EC2 上開放過多流量出口，符合最小權限原則與安全性最佳實踐。

❌ 其他選項錯誤原因：

✅ 小補充：Domain-based outbound control 的選項

- ✅ AWS Network Firewall（支援 FQDN allowlist）

- ❌ NAT Gateway + Security Group（不支援 URL）

- ❌ VPC Route Table 本身不能控 URL

- ✅ 可搭配 DNS Firewall（Route 53 Resolver DNS Firewall） 做進一步防護

✅ 總結：

要讓 private subnet 的 EC2 只連到特定網址並封鎖其他流量，最合適的方式是使用

AWS Network Firewall + FQDN allowlist →

選項 A 完全符合這個需求。

這題要解決的需求有四個：

✅ 題目需求：

以階層結構儲存員工資料（hierarchical structured relationship）

在高流量查詢下仍保持低延遲

保護敏感資料

每月若有財務資料出現時，自動 email 通知

✅ 正確答案是：

B. Use Amazon DynamoDB to store the employee data in hierarchies. Export the data to Amazon S3 every month.

E. Configure Amazon Macie for the AWS account. Integrate Macie with Amazon EventBridge to send monthly notifications through an Amazon Simple Notification Service (Amazon SNS) subscription.

✅ 解題說明：

B. Amazon DynamoDB 儲存階層資料 + 低延遲

- DynamoDB 是 key-value / document 類型的資料庫，支援儲存階層式結構（nested JSON）

- 提供毫秒等級的延遲，非常適合高併發存取

- 可搭配定期導出至 Amazon S3 供分析或備份（如使用 AWS Data Pipeline、Glue Export、DynamoDB Streams）

E. Amazon Macie + SNS + EventBridge

- Amazon Macie 可掃描 S3 中是否包含敏感資料（例如財務資訊）

- EventBridge 可設定規則，讓 Macie 每月掃描報告產生事件

- 將事件透過 SNS 發送 email 通知

✅ 完美滿足「發現財務資料 → 每月寄 email 通知」的需求

❌ 為何其他選項不正確？

✅ 總結：

✅ 正確答案：B 和 E

這題的關鍵在於設計非同步架構來滿足以下需求：

✅ 題目需求重點：

使用者從行動裝置上傳圖片

系統需「立刻」告知使用者圖片已收到（即時回應）

圖片縮圖（thumbnail）最多需 60 秒，這部分可以非同步處理

✅ 正確答案是：

C. Create an Amazon Simple Queue Service (Amazon SQS) message queue. As images are uploaded, place a message on the SQS queue for thumbnail generation. Alert the user through an application message that the image was received

✅ 解題說明：

這是一個標準的非同步任務解耦模式，流程如下：

前端使用者上傳圖片 → API 層接收

API 回應「圖片已收到」給前端（不用等縮圖）

API 將圖片資訊放入 SQS queue

後端縮圖服務從 SQS queue 拉任務進行圖片處理

✅ 這樣能確保使用者迅速收到成功訊息，縮圖處理則交由後端非同步處理，實作簡單且彈性高

❌ 為什麼其他選項不合適？

✅ 延伸補充：為什麼選 SQS？

- 解耦 upload 與處理邏輯：提高可維護性與擴展性

- 支援重試與冪等設計：減少資料遺失風險

- 與 Lambda 或 EC2 相容性高：後端縮圖服務可根據負載水平擴展

✅ 結論：

選項 C（SQS） 提供最佳的非同步任務處理架構，讓使用者立即收到回應，而後端可彈性擴展處理任務，符合需求與最佳實踐。

✅ 正確答案：C

這題的關鍵在於選出一個「最具操作效率（MOST operationally efficient）」的方式，來部署一個使用 Go 1.x 撰寫的 AWS Lambda function，並且提供一個：

- ✅ 支援 HTTPS 呼叫 的 endpoint

- ✅ 使用 IAM 驗證（AWS IAM authentication）

✅ 正確答案是：

B. Create a Lambda function URL for the function. Specify AWS_IAM as the authentication type.

✅ 原因解析：

Lambda Function URLs：

- 是 AWS 提供的一種最簡單方式，可以直接透過 HTTPS URL 呼叫 Lambda。

- 可以開啟 AWS_IAM 驗證模式：

- 

- 無需部署 API Gateway 或 CloudFront，極大簡化操作與維護成本。

🔍 各選項分析：

A.

Amazon API Gateway + IAM 驗證

- 雖然符合需求，但 需要額外設定 REST API、方法、整合、IAM 權限等，會增加操作與部署複雜度。

- ❌ 不是最有效率的做法（不符題意）

B. ✅

Lambda function URL + AWS_IAM 驗證

- 最簡潔的架構：

---
# 2025-07-05 筆記

在 AWS 的災難復原（Disaster Recovery, DR）策略中，我們通常會根據 備援資源的啟動程度與即時性，將 DR 架構分為 4 個常見等級：

🧊 1. Cold Standby（冷備援）🌡️最慢、最便宜

- 備援環境完全不啟動

- 僅備份資料（例如 S3、RDS snapshot）

- 災難發生後才開始建立基礎設施（如 EC2、RDS）

- ❌ RTO 高（從幾小時到幾天）

- ✅ 成本最低

🔦 2. Pilot Light（點火備援）🔥微啟動

- 關鍵資源（例如資料庫）已啟動且持續更新，但其他資源未啟動

- 災難發生時再啟動應用伺服器、負載平衡器等

- ✅ RPO 低（資料即時備援）

- ✅ 成本低，因為只保留最小關鍵資源

- ⚠️ RTO 還是較高（需要啟動應用）

♨️ 3. Warm Standby（溫備援）🌡️中間值

- 備援區有一套完整但縮小規模的系統（包含應用伺服器與資料庫）

- 定期同步資料與程式碼

- 災難發生時，只需升級規模即可接手生產流量

- ✅ 快速接手（低 RTO）

- ⚠️ 成本中等（有雙份系統但規模小）

🔥 4. Hot Standby / Active-Active（熱備援／雙活）⚡最快、最貴

- 兩區域都運行完整系統，並同時處理流量（流量可做 Geo DNS 或跨區分流）

- ✅ 最快切換（近乎零 RTO、零 RPO）

- ❌ 成本最高（雙份完整架構持續運作）

✅ 總結表格

✅ 正確答案：D.

Extend the application to add an attribute that has a value of the current timestamp plus 30 days to each new item that is created in the table. Configure DynamoDB to use the attribute as the TTL attribute.

🔍 為什麼選 D？

這題的核心是：

- 資料只需要保留 30 天

- 要省錢（minimize cost）

- 要省力（minimize development effort）

而 DynamoDB TTL（Time to Live） 是 AWS 提供的內建功能，專門用來做這種「自動刪除過期資料」的需求。

你只需要：

在新增資料時，寫入一個 timestamp 欄位（例如 expireAt）。

設定 DynamoDB 使用這個欄位當作 TTL。

到時間後，DynamoDB 會自動刪除該筆資料，無需手動清理。

✅ 零維護、零伺服器、低成本！

❌ 為什麼其他選項不如 D？

A. 使用 CloudFormation 每 30 天重建表格

- 毫無效率、而且會 清空整個資料表，不符合「只刪除 30 天以前資料」的需求

- 高維護成本

B. 用 EC2 + Marketplace + 自建刪除機制

- 多了 EC2 成本與運維

- 還要設計刪除邏輯，開發成本高

C. 用 DynamoDB Streams + Lambda 去找舊資料刪掉

- Streams 只能觸發當前新增的資料，你無法從中獲得舊資料列表

- 邏輯複雜，需要定時掃描整表 ➜ 成本與開發 effort 高

✅ TTL 設計範例（選項 D）

{

"orderId": "1234",

"createdAt": 1725405600,

"expireAt": 1727997600 // 30 天後的 Unix timestamp

}

然後在 DynamoDB 中設定 expireAt 為 TTL 欄位即可。

📌 小提醒：

- TTL 是非即時的：刪除可能會延遲幾分鐘到幾小時，但最終會刪掉。

- 不會產生 DynamoDB Streams 記錄（如果你要 audit，要額外設計）。

✅ 正確答案：D.

Use Amazon Elastic Kubernetes Service (Amazon EKS) with AWS Fargate for compute and Amazon DocumentDB (with MongoDB compatibility) for data storage.

🔍 題目重點：

- 應用程式目前是 容器化、跑在 Kubernetes 上，並使用 MongoDB

- 不能修改程式碼或部署方式

- 希望搬到 AWS 且減少運維成本

✅ 為什麼選 D？

✅ 全部需求都符合，且運維壓力最低。

❌ 為什麼其他選項不行？

A. ECS + EC2 + MongoDB on EC2

- 要手動維護 MongoDB（沒託管服務）

- 使用 ECS 會改變部署方式（不是 Kubernetes）

- ➜ ❌ 不符合部署與運維條件

B. ECS + Fargate + DynamoDB

- DynamoDB 是 key-value/NoSQL ➜ 不支援 MongoDB 查詢語法

- 同樣 ECS 不是 Kubernetes ➜ ❌ 不符現有部署方式

C. EKS + EC2 + DynamoDB

- EKS 有符合 Kubernetes，但 DynamoDB 不支援 MongoDB 語法 ➜ ❌ 不符資料庫條件

✅ 補充：什麼是 Amazon DocumentDB？

- 是 AWS 提供的 MongoDB 相容資料庫服務

- 提供託管式、高可用性、備份、修補等功能

- 可以無痛遷移 MongoDB 應用程式（若不使用 MongoDB 4.4+ 特有語法）

正確答案是：

✅ B. Use Amazon Transcribe for multiple speaker recognition. Use Amazon Athena for transcript file analysis

✅ 解題說明：

🎤

Amazon Transcribe

- 是 AWS 提供的語音轉文字服務。

- 支援 多說話者識別（speaker diarization），能自動辨識誰說了什麼。

- 能生成含時間戳記與說話者標記的 transcript 檔案（例如 JSON 或 TXT 格式）。

🔎

Amazon Athena

- 是一個互動式查詢服務，可以使用標準 SQL 查詢儲存在 Amazon S3 上的檔案（例如 transcript）。

- 無伺服器，無需事先載入資料，適合分析日誌、轉錄文件等。

🗃️

Amazon S3

- 提供高耐久性（99.999999999%）的儲存方案，可用來保存轉錄資料長達 7 年。

---
# 2025-07-04 筆記

正確答案是：

👉 C. Use Reserved Instances for the baseline capacity and use Spot Instances to handle additional capacity

💡 解釋：

這題的關鍵是要找出一個 高可用、具成本效益（MOST cost-effective） 的 EC2 運行模式，來應對：

- 持續性處理需求（no downtime）

- 不穩定的訊息流量（intermittent traffic）

- 可併行處理任務（parallel processing）

✅ 最佳解法：

Reserved + Spot 組合

- Reserved Instances (RI)：

- 

- Spot Instances：

- 

若 Spot 被回收，Reserved 仍可保底維持服務不中斷，成本效益與可用性兼具

❌ 其他選項為什麼不適合？

✅ 正確答案：C. Use Reserved Instances for the baseline capacity and use Spot Instances to handle additional capacity

正確答案是：

👉 C. Create an Amazon EventBridge (Amazon CloudWatch Events) rule for the Createlmage API call. Configure the target as an Amazon Simple Notification Service (Amazon SNS) topic to send an alert when a Createlmage API call is detected.

✅ 解釋：

為什麼選 C？

- Amazon EventBridge（原名 CloudWatch Events） 可以即時監聽特定的 AWS API 呼叫事件（例如 EC2 的 CreateImage）。

- 你可以設定規則來偵測這個 API 事件，並將事件傳送給 Amazon SNS，發出通知（例如 Email、SMS、Lambda 等）。

- 不需要自己查 CloudTrail log、寫 Lambda 分析程式或排程任務，自動且零維運負擔。

這是 AWS 官方推薦的最輕量、最即時的事件監控方案。

❌ 為什麼其他選項不適合？

🧩 小補充：EventBridge + SNS 的好處

- ⏱ 即時偵測 CreateImage

- 📉 最小運算成本

- 🔧 幾乎無須程式碼

- 📬 支援多種通知方式（Email、Lambda、HTTP 等）

✅ 正確答案：C. 使用 EventBridge 設定監聽 Createlmage，並透過 SNS 發送警報。

正確答案是：

👉 B. Create a gateway VPC endpoint for Amazon S3 in the Availability Zone where the EC2 instance is located. Attach appropriate security groups to the endpoint. Attach a resource policy to the S3 bucket to only allow the EC2 instance’s IAM role for access.

✅ 解釋：

問題核心需求：

資料上傳不能經過公網（No public internet routes）

只有 EC2 instance 才能上傳

目標服務是 Amazon S3

🧩 最適解：

Gateway VPC Endpoint + IAM Role 限制

- Gateway VPC Endpoint 是 S3 與 DynamoDB 專用的 VPC Endpoint，允許 EC2 與 S3 間的通訊走內部 AWS 網路（無需 NAT Gateway 或 Internet Gateway）。

- 搭配 S3 Bucket Policy 限定只有特定 IAM Role（也就是 EC2 的 instance profile）能上傳。

這種設計：

- 不經過公網

- 成本最低（不用 NAT）

- 易於管控與維運

❌ 為什麼其他選項不對？

🔐 安全性補充建議：

- 在 S3 Bucket Policy 加入：

- 

✅ 正確答案：B. 使用 Gateway VPC Endpoint 搭配 IAM Role 限制，確保安全與私有通訊。

🌉 Gateway Endpoint vs. Interface Endpoint 差異總覽

🔎 更具體範例比較

Gateway Endpoint

（如 S3）：

- 你建立一個 Gateway Endpoint

- 它會幫你在 Route Table 中自動加入一條路由：

Destination: pl-xxxx (S3 Prefix List) → Target: vpce-xxxx

- 

- 只要 EC2 在這個 Subnet 中，請求 s3.amazonaws.com 會自動走私網。

Interface Endpoint

（如 SQS）：

- 建立時會在 Subnet 中生成一個 ENI（彈性網卡）

- 所有請求會導向這個 ENI，例如：

sqs.ap-northeast-1.vpce.amazonaws.com → 10.0.2.35（ENI IP）

- 

- 可以用 Security Group 控管誰可以存取它

✅ 什麼時候用哪個？

📌 總結

正確答案是：

👉 A. Configure the Lambda function to run in the VPC with the appropriate security group.

✅ 解釋：

問題關鍵：

- Lambda 要存取 在公司資料中心（on-premises）內部私有子網中的資料庫

- AWS 與資料中心之間已透過 Direct Connect 建立連線

- 要求 Lambda 可以透過私有網路（非公網）存取資料庫

✅ 為什麼選 A？

- Lambda 預設運行在 AWS 公網中，如果要存取私有網段（VPC 子網、或透過 Direct Connect 連到 on-prem），必須配置 Lambda 運行在 VPC 中

- 設定 Lambda 的 VPC 子網與安全群組，就能讓 Lambda：

- 

- 完全符合無伺服器 + 私網存取的架構需求

❌ 其他選項為什麼不適合？

🧩 補充建議：

若 Lambda 是存取 資料中心內部的私有資料庫，你需要：

讓 Lambda 加入 VPC（選定有路由到 VGW 的私有子網）

設定 Lambda 使用的 security group → 開啟對資料庫的連線權限（例如 TCP 3306 for MySQL）

確保 VPC route table 有指向 Virtual Private Gateway（VGW）

確保對方資料中心的防火牆與路由設定也允許 Lambda 的 VPC IP 範圍進入

---
# 2025-07-01 筆記

這題考的是：

- 根據需求選擇合適的資料庫解決方案

- 重點條件有：

- 

✅ 正確答案：

A. Use Amazon DynamoDB with auto scaling. Use on-demand backups and Amazon DynamoDB Streams

🔍 題目解析：

✅ 為什麼選 A：

❌ 為什麼其他選項不適合：

B.

Amazon Redshift

- 用於 OLAP（分析型）工作負載，不適合以事務為主的應用程式

- 不保證 < 5 小時的 RPO，且成本與運維較高

C.

Amazon RDS with Provisioned IOPS

- 固定 IOPS 難以隨季節性變動自動調整，成本高

- 雖可做 snapshot，但快照間隔太寬會風險過高；無內建 Streams 類似機制處理稽核紀錄

D.

Amazon Aurora MySQL with auto scaling

- Aurora auto scaling 指的是讀取節點（Aurora Replica），寫入節點仍需固定設定

- 雖支援稽核與備份，但沒有 DynamoDB 的高彈性與低維運特性

- 不如 DynamoDB 更適合處理不穩定流量

✅ 補充 DynamoDB 優勢：

- Auto scaling 支援根據使用量自動擴展/收縮

- On-demand backup 可隨時快照整張表

- Streams 可以串接 AWS Lambda 實現自動稽核、異動追蹤

- 無伺服器管理，低運維

正確答案是：A. Use a cluster placement group. Attach a single Provisioned IOPS SSD Amazon Elastic Block Store (Amazon EBS) volume to all the instances by using Amazon EBS Multi-Attach

✅ 題目關鍵需求重點：

✅ 為什麼選 A 正確？

- Cluster Placement Group

- 

- Amazon EBS Multi-Attach

- 

- Provisioned IOPS SSD (io1/io2)

- 

❌ 其他選項為什麼不對？

B. Cluster placement + EFS

- ❌ Amazon EFS 是 NFS 檔案系統（file-level storage）

- ❌ 雖然可以共用，但效能不及 EBS + 多掛載，且延遲較高，不符合 最低 latency 要求

C. Partition placement group + EFS

- ❌ Partition PG 是針對大規模分區隔離的部署策略，不保證節點之間低延遲

- ❌ 同樣 EFS 不符共享高效 block volume 要求

D. Spread placement group + EBS Multi-Attach

- ❌ Spread PG 強調 高可用性與容錯，將實例盡可能分開部署，會增加節點延遲

- ❌ 不適用於 HPC 需要超低延遲通信的場景

🧠 延伸補充

若進一步追求 HPC 的極致效能，也可以考慮：

- 使用 EC2 instances with Elastic Fabric Adapter (EFA)：提供 RDMA-like 通信能力

- 配合 Amazon FSx for Lustre：提供 HPC 儲存系統選擇，比 EFS 更快的共享檔案存取效能

✅ 總結：

當我們討論 雲端與本地環境中的儲存系統 時，常見的三種主要儲存類型是：

# 📦 儲存系統類型總覽

# 🔹 Block Storage（區塊儲存）

🔧 原理：

- 將儲存設備分成「固定大小的區塊（block）」。

- 沒有檔名、資料夾；由作業系統建立檔案系統（如 ext4, NTFS）來管理。

💡 典型代表：

- AWS：Amazon EBS

- 本地：HDD、SSD、SAN

✅ 優點：

- 非常快的隨機讀寫速度（低延遲）

- 適合資料庫、VM 映像檔、交換區、OS

❌ 缺點：

- 不支援多主機共享（除非特殊設計）

- 儲存需要手動管理與格式化

# 🔸 File Storage（檔案儲存 / NFS）

🔧 原理：

- 像傳統作業系統的檔案系統，有路徑與檔名結構。

- 支援共享與協作使用。

💡 典型代表：

- AWS：Amazon EFS（NFS v4.1）、Amazon FSx

- 本地：NAS（Network Attached Storage）

✅ 優點：

- 可多台機器同時掛載（共享存取）

- 使用熟悉的 ls, cd, cp, mv 操作方式

❌ 缺點：

- 效能受限於網路延遲

- 不適合大量隨機 I/O、高併發需求

# 🟢 Object Storage（物件儲存）

🔧 原理：

- 將資料包裝成「物件」，每個物件有：

- 

- 不存在傳統的資料夾層級。

💡 典型代表：

- AWS：Amazon S3

- GCP：Cloud Storage

- Azure：Blob Storage

✅ 優點：

- 幾乎無限擴充、設計給網路存取

- 適合備份、媒體、資料湖

- 成本效益高，有 lifecycle 與冷儲存選項

❌ 缺點：

- 無檔案系統，不能用 ls, cat 操作

---
# 2025-06-30 筆記

這題目考的是如何保護 S3 資源不被直接存取，同時又要能透過 CloudFront 發佈內容。

❓ 題目解析

- 使用者上傳檔案到 S3。

- 所有檔案要經由 CloudFront 提供。

- 不允許使用者透過 S3 原始 URL 直接存取。

✅ 正確答案：

D. Create an origin access identity (OAI). Assign the OAI to the CloudFront distribution. Configure the S3 bucket permissions so that only the OAI has read permission.

🔍 詳解

✅ 為什麼選 D？

- OAI（Origin Access Identity） 是一種特殊的身份，讓 CloudFront 可以存取 S3，但其他人無法直接透過 S3 URL 存取。

- 當你設定了 OAI：

- 

- 這樣達成「只能透過 CloudFront 看檔案」的需求。

❌ 為什麼其他選項錯？

- A. 「寫個別的 S3 存取政策給 CloudFront」這不是最佳作法，CloudFront 本身沒有 IAM 身份可以直接給權限。

- B. IAM 使用者無法指派給 CloudFront 作為授權來源，也無法限制 S3 URL 被讀取。

- C. S3 bucket policy 並不支援直接把 CloudFront Distribution ID 當成 Principal，這不是合法的 IAM 寫法。

📝 延伸補充（若你使用 CloudFront OAC）

AWS 推出新的方式叫做 OAC（Origin Access Control），可以替代 OAI，但 OAI 仍然是考題中常見選項。

這題問的是：網站提供下載報告的功能，要全球擴展、高效能、低成本，且要盡量少維運基礎設施資源（infrastructure）。

✅ 正確答案：

A. Amazon CloudFront and Amazon S3

🔍 題目分析關鍵點：

❌ 錯誤選項解析：

- B. AWS Lambda and Amazon DynamoDB
適合處理動態請求、事件觸發，但這題是靜態報告檔案下載，非最佳選擇。

- C. Application Load Balancer with Amazon EC2 Auto Scaling
雖然能擴展，但會增加維運成本（要管理 EC2 + 負載平衡器），不是最 cost-effective。

- D. Amazon Route 53 with internal Application Load Balancers
Internal Load Balancer 無法給公開使用者使用；Route 53 只是 DNS，無法提供實際內容。

✅ 小結

這樣組合最符合「全球擴展 + 高效能 + 最小維運 + 成本效益」的要求。

題目解析：

公司需求如下：

升級 Oracle 至最新版本

設立災難復原（DR）機制，跨區更佳

維持對底層 OS 的存取權限（通常代表要能自訂資料庫設定）

盡量降低日常營運和 DR 的操作負擔

✅ 正確答案：

C. Migrate the Oracle database to Amazon RDS Custom for Oracle. Create a read replica for the database in another AWS Region.

原因解析：

❌ 錯誤選項分析：

- A. EC2 + replication

- 

- B. RDS for Oracle + Cross-Region Backup

- 

- D. RDS for Oracle + Multi-AZ standby

- 

🧠 延伸補充：

- RDS for Oracle ➤ 管理簡單，但限制較多（無法存取 OS、版本受限）

- RDS Custom for Oracle ➤ 管理與彈性之間取得平衡，適合需要較細節控制（如自訂 patch、agent）的使用者

- EC2 + Oracle ➤ 彈性最高，但管理成本與維運負擔最大

✅ 結論：

若你需要「自訂版本 + 存取作業系統 + 跨區備援 + 降低日常管理成本」，選擇 RDS Custom for Oracle + Cross-region read replica（選項 C）最合適。

題目解析：

公司需求如下：

- 搬移應用程式到 Serverless 架構

- 分析 既有與新增的資料

- 資料儲存在 Amazon S3

- 資料需 加密

- 必須 跨區複製（Cross-Region Replication, CRR）

- 要求 最低操作負擔（Least operational overhead）

✅ 正確答案：

A. Create a new S3 bucket. Load the data into the new S3 bucket. Use S3 Cross-Region Replication (CRR) to replicate encrypted objects to an S3 bucket in another Region. Use server-side encryption with AWS KMS multi-Region keys (SSE-KMS). Use Amazon Athena to query the data.

原因解析：

❌ 其他選項為何不行：

B. 使用 Amazon RDS 查詢資料 ❌

- RDS 不是 serverless。

- RDS 不能直接查詢 S3 上的資料，還要先匯入 ➜ 操作負擔高

C. 使用 SSE-S3 加密 ❌

- SSE-S3 不支援 CRR（AWS 限制）

- CRR 複製加密資料時，若使用 SSE-S3，無法跨區複製

D. 同上，也使用了 RDS + SSE-S3 ❌

- 一樣面臨 CRR 不支援 SSE-S3、RDS 非 serverless 的兩個問題

✅ 補充知識：

- SSE-KMS + Multi-Region Keys (MRK)：支援加密資料的跨區複製，是設計來搭配 CRR 使用的。

- Athena：直接查詢儲存在 S3 的資料，支援多種格式（CSV、Parquet、JSON 等），不需建資料庫。

- S3 CRR：支援自動、持續地將資料從一個 bucket 複製到另一個區域的 bucket。

✅ 結論：

若要達成 serverless 查詢 + 加密 + 跨區複製 + 最少管理負擔，

正確解答為：A

這題的關鍵在於以下幾點需求：

- 連線必須是私有的（private）

- 只允許連線到指定服務（restricted to the target service）

- 只能由公司 VPC 主動發起（initiated only from the company’s VPC）

✅ 正確答案是：

D. Ask the provider to create a VPC endpoint for the target service. Use AWS PrivateLink to connect to the target service.

📘 解題解析：

為什麼選 D？

- AWS PrivateLink 是專門設計來提供 私有、點對點、僅針對特定服務 的連線方式。

- 連線是透過 Interface VPC Endpoint 建立，會在你的 VPC 中建立一個 ENI (彈性網路介面)。

- 公司端主動發起連線，提供方被動接收。

- 私有流量僅限該服務，不會開放整個 VPC。

❌ 其他選項錯在哪：

A. VPC Peering ❌

---
# 2025-06-29 筆記

✅ 正確答案為：B. 安裝 AWS DataSync agent 在 on-premises 資料中心 和 E. 使用 AWS DataSync 建立 on-premises SFTP server 的 location 設定

✅ 題目重點拆解：

- 原始資料儲存在 on-prem SFTP server 上，並使用 NFS 檔案系統

- 要遷移至 AWS 上的 EC2 + EFS 架構中

- 要 自動化遷移資料

- 資料量為 200 GB

✅ 正確答案解析：

B. Install an AWS DataSync agent in the on-premises data center

- DataSync 可用於從 on-prem NFS/SFTP 來源自動遷移資料至 AWS（例如 EFS）

- 它透過安裝在本地的 agent 來處理與 AWS 的連線與資料搬移

E. Use AWS DataSync to create a suitable location configuration for the on-premises SFTP server

- 在使用 DataSync 時，你需要設定來源與目的地的 Location，例如：

- 

這兩步搭配即可讓 DataSync 自動搬移資料到 EC2 掛載的 EFS 檔案系統。

❌ 錯誤選項解析：

✅ 結論：

使用 AWS DataSync 是最佳且官方推薦的方式來自動從 on-prem NFS 或 SFTP 系統將資料遷移到 AWS EFS。這可以確保安全性、效率與最低的操作負擔。

✔️ 正確答案：B 和 E

✅ 正確答案：A. Edit the job to use job bookmarks.

✅ 題目重點：

- AWS Glue 每天執行一次 ETL Job，處理 S3 中的 XML 檔案

- 每天都有新增資料

- 問題是：每次都重新處理全部資料

- 目標是：避免重複處理舊資料

✅ 解法解析：

A. 使用 Glue Job Bookmarks

- Job Bookmarks 是 AWS Glue 的一個功能，會追蹤上一個 job 執行時所處理的資料集。

- 下次執行時只會處理 新增加或修改的資料。

- 非常適合這種每天跑、資料會累積但舊資料不需要重處理的情境。

❌ 錯誤選項解析：

✅ 結論：

若想讓 AWS Glue 每次只處理新增資料，最有效、最符合 AWS 實務的做法就是 開啟 Job Bookmarks。

✔️ 正確答案：A. Edit the job to use job bookmarks.

當然，我來幫你詳細說明一下選項 C. Edit the job by setting the NumberOfWorkers field to 1.

🔹 選項 C 的意思

在 AWS Glue 中：

- NumberOfWorkers 是設定 Glue Job 執行時要啟用的 DPU（Data Processing Units）數量 或 工作執行緒數量（視 Glue 的版本和模式而定）。

- 把 NumberOfWorkers 設成 1，代表只用 一個執行單位 處理資料，會讓 Glue job 的處理速度變慢，但也可以節省成本。

⚠️ 為什麼這不是正確答案？

這個設定只會：

- 影響 job 執行的 資源數量和執行速度

- 不會改變資料的處理邏輯

也就是說：

Glue 還是會處理 所有 S3 中的 XML 檔案，只是變成一個 worker 慢慢處理而已。

🧠 額外補充：那什麼情況要調整

NumberOfWorkers

？

你可以根據以下狀況調整它：

- 如果資料量不大、執行時間允許，可降低 NumberOfWorkers 來節省費用。

- 如果資料量大，處理時間過長，則可以提高 NumberOfWorkers 來加快處理速度。

但這與「避免重複處理舊資料」無關。

✅ 結論：

- NumberOfWorkers 是資源設定，不會影響處理哪些資料

- 因此，選項 C 不能解決每次重複處理資料的問題

正確做法還是使用 Glue 的 Job Bookmarks（選項 A） 來追蹤和跳過已處理過的資料。

正確答案是：

✅ A. Use AWS Shield Advanced to stop the DDoS attack.

✅ C. Configure the website to use Amazon CloudFront for both static and dynamic content.

✅ A. Use AWS Shield Advanced

- AWS Shield Advanced 提供針對 大規模 DDoS 攻擊 的進階保護功能，例如 TCP SYN floods、UDP reflection、HTTP floods。

- 它可與 CloudFront、ALB、EC2、Route 53 整合。

- 具備自動偵測、自動緩解、大量 IP 封鎖、以及 DDoS 攻擊事件通知。

➡ 這是針對 DDoS 的首選解決方案。

✅ C. Configure the website to use Amazon CloudFront

- CloudFront 是 AWS 的 CDN，可作為網站的前置代理（edge layer）：

- 

- CloudFront 也整合了 AWS Shield Standard（免費），提供額外的 DDoS 保護。

➡ CloudFront 作為前線防禦，可減少 EC2 直接面對攻擊。

❌ B. Amazon GuardDuty

- GuardDuty 是一種 威脅偵測服務，可以識別惡意行為（如可疑 IP）。

- 但 不會自動封鎖攻擊，需要手動處理或搭配 Lambda automation。

- 適合用來 警示與後續調查，但無法即時自動防禦 DDoS。

❌ D. Lambda function 自動加黑名單

- 雖然技術上可用 Lambda 自動更新 NACL，但：

❌ E. 使用 EC2 Spot Instances 和 Auto Scaling

- Spot instances 雖然便宜，但並 不適合用在重要的、高可用的網站前台

- 而且 Auto Scaling 不能緩解 DDoS 攻擊本身，只能被動擴容應對高流量。

✅ 結論

若要對抗大型 DDoS 且確保零停機：

- 使用 AWS Shield Advanced 提供 DDoS 防護（A）

- 配置 CloudFront 作為前線防禦與快取加速器（C）

📘 題目說明：

一家公司準備部署一個無伺服器（serverless）工作負載。

解決方案架構師需要依照「最小權限原則」來設定 AWS Lambda 函數的權限。

這個 Lambda 函數會被一個 Amazon EventBridge（或 CloudWatch Events）規則觸發。

問題是：應該怎麼設置權限才能符合這個需求？

🔍 題目關鍵點拆解：

- 使用 Lambda 函數。

- Lambda 會被 EventBridge 規則觸發（也就是 EventBridge 要能「呼叫 Lambda」）。

- 必須遵守「最小權限原則（Least Privilege Principle）」。

- 問題核心是「如何正確地授權 EventBridge 觸發 Lambda」。

✅ 正確答案：

D.

在 Lambda 函數上加入資源型政策（resource-based policy），

授權動作為 lambda:InvokeFunction，principal 為 events.amazonaws.com。

---
# 2025-06-28 筆記

✅ 正確答案：B. Use AWS Backup to create backup schedules and retention policies for the table.

✅ 題目解析：

目標：

- 保留 使用者交易資料（transaction data） 在 DynamoDB 中

- 保存期限為 7 年

- 追求最低營運負擔（Most operationally efficient）

🧠 各選項分析：

A. 使用 DynamoDB 的 Point-in-time recovery (PITR)

- PITR 可以讓你復原到最近 35 天的任意時間點

- ✅ 適合短期復原用

- ❌ 無法滿足 7 年保存需求

✅ B. 使用 AWS Backup 設定備份排程與保留原則

- 支援 DynamoDB table 的定期備份與自訂保留期

- 可以設定每天/每週/每月備份並自動保存 7 年 ✅

- 完全 無需自訂 Lambda 或 EventBridge ✅

- 最符合 operationally efficient 的條件

C. 使用 DynamoDB Console 手動備份 + S3 儲存

- 需要手動操作，無法 scale

- 雖然搭配 S3 Lifecycle 可達 7 年保留

- ❌ 不是「自動化」或「高效率」的營運方式

D. 使用 EventBridge + Lambda 自動備份到 S3

- 可以達成需求，但要你自己維護：

- 雖然有效，但比起 AWS Backup 仍多出不少維運負擔 ❌

✅ 總結比較：

✅ 正解：

B. Use AWS Backup to create backup schedules and retention policies for the table.

✅ 正確答案：B. Modify the launchPermission property of the AMI. Share the AMI with the MSP Partner’s AWS account only. Modify the CMK’s key policy to allow the MSP Partner’s AWS account to use the key.

🧠 題目解析：

這題的重點在於：

AMI 是加密的，而且：

使用的是 自定義的 KMS CMK（Customer Master Key）

需要與 MSP Partner 的 AWS 帳戶共享

強調要 最安全的方式

✅ 為什麼選 B？

- launchPermission 可用來指定哪些帳號可使用 AMI 啟動 EC2。

- 但因為該 AMI 背後的 EBS Snapshot 是 使用 CMK 加密的：

- 

- 這是 AWS 官方建議的做法，安全又直接。

❌ 其他選項為何錯？

A.

公開 AMI 和 snapshot？

- ❌ 風險極高！不該將加密資源公開，即使有金鑰保護。

- 不符合「最安全方式」這個題目重點。

C.

信任對方的 KMS 金鑰？

- ❌ KMS 金鑰不支援「信任另一個金鑰」的設定。

- 你不能用 CMK 直接信任另一個帳號的金鑰來重加密已存在的 snapshot。

- 而且複雜、易錯，不是最直接或安全的選項。

D.

透過 S3 匯出再重建？

- 這是可行的技術方式，但：

- 

- 題目說明：「最安全，最低風險方式」→ ❌ 不符合。

✅ 正解方式說明：

使用以下命令設定共享 AMI：

aws ec2 modify-image-attribute \

--image-id ami-xxxxxxxx \

--launch-permission "Add=[{UserId=MSP_ACCOUNT_ID}]"

然後更新加密 snapshot 所使用的 KMS CMK 金鑰策略，加入 MSP 帳號：

{

"Sid": "Allow use of the key",

"Effect": "Allow",

"Principal": { "AWS": "arn:aws:iam::MSP_ACCOUNT_ID:root" },

"Action": [

"kms:Decrypt",

"kms:DescribeKey",

"kms:ReEncrypt*",

"kms:GenerateDataKey*"

],

"Resource": "*"

}

✅ 總結

✅ 正解：

B. Modify the launchPermission property of the AMI. Share the AMI with the MSP Partner’s AWS account only. Modify the CMK’s key policy to allow the MSP Partner’s AWS account to use the key.

✅ 正確答案：D. Create an Amazon EventBridge (Amazon CloudWatch Events) rule to detect any certificates that will expire within 30 days. Configure the rule to invoke an AWS Lambda function. Configure the Lambda function to send a custom alert by way of Amazon Simple Notification Service (Amazon SNS).

🔍 題目解析：

目標：

在 SSL/TLS 憑證過期前 30 天發出通知。

情境：

- 憑證是從 ACM (AWS Certificate Manager) 匯入的。

- 用於 Elastic Load Balancers。

- 需要 自動通知（30天前） → 符合 event-driven alerting 概念。

✅ 為什麼選 D？

AWS Certificate Manager 本身無法自動通知憑證即將過期，但它會將這些資訊發佈到 Amazon EventBridge（以前叫 CloudWatch Events）。

你可以：

建立一個 EventBridge 規則來篩選出 ACM 憑證過期的事件（ACM Certificate Approaching Expiration）。

觸發 AWS Lambda。

Lambda 發送通知到 SNS topic。

這樣可以滿足：

- ⏰ 30天前通知

- 📩 自動通知 via SNS

- 🔁 無需手動監控

❌ 錯誤選項解析：

A. ❌「Add a rule in ACM」

ACM 不支援自訂規則或排程通知，也不能直接 publish SNS 通知。

---
# 2025-06-27 筆記

題目解析：

公司正在開發一個應用程式，透過 REST API 提供訂單運送統計資料。目標是：

- 每天早上固定時間

- 從應用的 API 提取資料

- 整理成 可讀的 HTML 報告

- 用 email 寄送 給多人

選項分析：

A. Configure the application to send the data to Amazon Kinesis Data Firehose.

- ❌ 不適合

- Kinesis Firehose 適合用於持續的資料串流輸出到 S3、Redshift 等目的地，非用來每日定時產生報告。

- 不符合「每天早上一次性提取 + email 報告」的需求。

B. Use Amazon Simple Email Service (Amazon SES) to format the data and to send the report by email.

- ✅ 部分正確

- Amazon SES 能用來 發送 email，但不負責「格式化」資料。格式化通常是 Lambda 處理。

- 不過在整體流程中，用 SES 發送 HTML 報告 非常合適。

C. Create an Amazon EventBridge (Amazon CloudWatch Events) scheduled event that invokes an AWS Glue job to query the application’s API for the data.

- ❌ 不適合

- AWS Glue 是為資料處理（如 ETL 或從資料湖中分析）設計的，不適合用來呼叫 REST API 並處理 HTML 格式資料。

- 呼叫 API 並格式化輸出報告，應由 Lambda 處理。

D. Create an Amazon EventBridge (Amazon CloudWatch Events) scheduled event that invokes an AWS Lambda function to query the application’s API for the data.

- ✅ 正確

- EventBridge 可設定 每日定時觸發

- Lambda 可負責：

- 

E. Store the application data in Amazon S3. Create an Amazon Simple Notification Service (Amazon SNS) topic as an S3 event destination to send the report by email.

- ❌ 不適合

- S3 的 SNS 通知通常是「檔案上傳時自動通知」，不適合每日定時產出報告後發送。

- 而且 SNS 也無法寄送 HTML 郵件內容（只能通知訊息，不是報告形式）。

✅ 正確組合：

- B. 用 Amazon SES 寄送報告 email

- D. 用 EventBridge 定時呼叫 Lambda，從 API 抓資料並整理 HTML 報告

額外提示：

完整流程如下：

EventBridge 設定每日定時事件

Lambda function：

這題考的是如何使用自定網域名 (custom domain name) 和 HTTPS 憑證 (SSL/TLS) 來公開 Amazon API Gateway 的 Regional endpoint，並透過 Route 53 設定對應的 DNS 記錄。

✅ 題目需求解析：

- API Gateway 在 ca-central-1。

- 需要讓第三方服務透過自家網域 HTTPS 存取 API Gateway。

- 已經有自己的 domain name 註冊在 Route 53。

- 想使用公司的 domain name + HTTPS 憑證。

✅ 正確做法的步驟是：

在 API Gateway 中建立 Regional endpoint（這題指定了在 ca-central-1）。

在 ACM（同一個區域）中匯入或建立與公司網域對應的公有憑證。

在 API Gateway 建立 Custom Domain Name 並綁定憑證。

使用 Route 53 建立 DNS 記錄，指向這個 Custom Domain Name 所對應的 API Gateway endpoint。

❌ 選項錯誤分析：

A. 使用 stage variables 並匯入憑證

- ✖️ stage variables 是用來控制 Lambda alias 或 endpoint path，不是設計來變更 domain name。

- ✖️ 不會影響 API Gateway endpoint 的 URL。

- ➤ 錯誤用法。

B. 將憑證匯入 us-east-1，並用 alias 指向 API Gateway Regional endpoint

- ✖️ Regional API Gateway 必須要在「相同區域」內使用 ACM 憑證（也就是 ca-central-1），us-east-1 只對 edge-optimized endpoint 有用。

- ➤ 錯誤區域，會導致憑證無法綁定。

D. 憑證在 us-east-1，指向自己的 domain name

- ✖️ 一樣問題：ACM 憑證區域錯誤（只適用於 CloudFront / edge-optimized API）。

- ✖️ 建立 A 記錄並不會直接指向 API Gateway 的 custom domain。

- ➤ 邏輯混亂、設定錯誤。

✅ 正確答案：

C. Create a Regional API Gateway endpoint. Associate the API Gateway endpoint with the company’s domain name. Import the public certificate associated with the company’s domain name into AWS Certificate Manager (ACM) in the same Region. Attach the certificate to the API Gateway endpoint. Configure Route 53 to route traffic to the API Gateway endpoint.

- ✅ 使用 Regional API Gateway endpoint。

- ✅ ACM 憑證在正確的區域：ca-central-1。

- ✅ 綁定 custom domain name。

- ✅ Route 53 設定對應 alias record。

✅ 正解：

C.

這題是關於如何過濾圖片中的不當內容，需求如下：

- 圖片由使用者上傳。

- 需偵測是否有不當內容。

- 希望最小化開發成本與工作量（minimize development effort）。

各選項說明：

A. Use Amazon Comprehend to detect inappropriate content.

- ❌ 錯誤。Amazon Comprehend 是用來做文字自然語言處理（NLP），無法處理圖片。

B. Use Amazon Rekognition to detect inappropriate content. Use human review for low-confidence predictions.

- ✅ 正確。Amazon Rekognition 是專門的影像與影片分析服務，可以直接偵測出不當內容（例如暴力、裸露等）。

- 它提供一個預先訓練好的模型，能夠辨識是否包含不適當內容。

- 並且可與 Amazon Augmented AI (A2I) 整合，在辨識信心不足時呼叫人工審查。

- 符合最小開發工作量的需求。

C. Use Amazon SageMaker to detect inappropriate content.

- ❌ 錯誤。SageMaker 是訓練與部署自訂機器學習模型的服務，需要自行準備訓練資料與模型架構，開發成本高。

D. Use AWS Fargate to deploy a custom machine learning model…

- ❌ 錯誤。使用 Fargate 與自建模型開發與部署會增加系統設計與維運負擔，與最小開發工作量的需求相違。

✅ 正確答案：

B. Use Amazon Rekognition to detect inappropriate content. Use human review for low-confidence predictions.

這題的目標是：強制所有網站流量都使用 HTTPS，也就是將 HTTP 請求自動導向 HTTPS。

各選項分析：

A. Update the ALB’s network ACL to accept only HTTPS traffic

- ❌ 錯誤：Network ACL 是針對 VPC 子網的低層防火牆控制，不能自動重導 URL，也無法提供「轉址」功能。

B. Create a rule that replaces the HTTP in the URL with HTTPS

- ❌ 錯誤：沒有這種在 ALB 層級直接修改 URL protocol 的規則。URL protocol (http://) 是在 client-side 被指定的。

C. Create a listener rule on the ALB to redirect HTTP traffic to HTTPS

- ✅ 正確：這是最常見且推薦的方式：

- 

D. Replace the ALB with a Network Load Balancer configured to use Server Name Indication (SNI)

- ❌ 錯誤：NLB 是第 4 層（L4）負載平衡器，不支援重導，也不支援 SNI 的應用層重導控制。

✅ 正確答案：

C. Create a listener rule on the ALB to redirect HTTP traffic to HTTPS.

---
# 2025-06-26 筆記

✅ 題目重點：

- 公司 EC2 成本上升

- 發現有幾台 EC2 出現 不必要的垂直擴展（vertical scaling）

- 需求：

- 

✅ 各選項解析：

A. Use AWS Budgets

- ❌ AWS Budgets 是用來設定預算與通知，不提供深入歷史分析或按 Instance Type 的視覺化工具

- 不適合用來「追查成本異常」

B. ✅ Use Cost Explorer’s granular filtering feature to perform an in-depth analysis of EC2 costs based on instance types

- ✅ Cost Explorer 支援按 EC2 服務 → instance type → month/day 維度分析

- ✅ 內建圖表功能，可視覺化近 2 個月成本變化

- ✅ 操作簡單，不需額外設定或寫程式

- ✅ 最低操作負擔的選項

C. Use AWS Billing and Cost Management dashboard

- ❌ 此功能提供的是整體成本摘要

- 雖有圖表，但過於粗略，不支援深入 drill down 到 instance type 層級

- ✘ 不足以找出根因（root cause）

D. Use Cost and Usage Reports (CUR) + S3 + QuickSight

- ✅ 能做到非常深入的自定義分析

- ❌ 需要設定：

- 

- 操作負擔高，不符合「最小操作負擔」的要求

✅ 正確答案：

B. Use Cost Explorer’s granular filtering feature to perform an in-depth analysis of EC2 costs based on instance types

📌 補充：Cost Explorer 可進行的分析維度

- Service（Amazon EC2）

- Instance Type（如 t3.large, m5.xlarge）

- Linked Account

- Usage Type（按小時計費）

- Time (monthly, daily)

- Region

AWS 成本相關服務總整理

🎯 建議用途地圖

✅ A. Turn on AWS Config with the appropriate rules.

✅ 為什麼選 A：AWS Config + 規則

- AWS Config 可以持續追蹤資源的設定變更，並記錄歷史狀態。

- 對於 Amazon S3，你可以設定以下 Config 規則，例如：

- 

🔍 用途：當 S3 bucket 的設定被未經授權的變更（如開放 public read、關閉加密），Config 會偵測並標示為「non-compliant」，可搭配 SNS、EventBridge 發警告。

❌ B. AWS Trusted Advisor

- Trusted Advisor 是用來檢查常見的設定最佳化（如安全性、成本、可用性等）。

- 不會持續監控設定變化，而且很多安全檢查僅開放給 Business/Enterprise 支援等級帳戶。

- 不適合用來審查持續變動的資源配置變更

❌ C. Amazon Inspector

- Inspector 是做 漏洞掃描與安全評估，主要針對：

- 

- 與 S3 設定無關

❌ D. S3 Server Access Logging + EventBridge

- Access Logging 是記錄誰「存取 S3 物件」，不是「修改設定」

- EventBridge 無法直接觸發設定變更事件（Config 才能追蹤設定歷史）

✅ 結論

🔍 AWS 設定與安全審查類型服務一覽

🧩 實際應用場景舉例

✅ S3 Bucket 安全監控與合規

- 使用 AWS Config：

- 

✅ 檢查是否有安全風險資源

- 使用 Trusted Advisor (免費項目)：

- 

✅ 檢查 EC2 是否存在漏洞

- 使用 Amazon Inspector：

- 

✅ 自動修正策略（Auto Remediation）

- 組合：AWS Config + Systems Manager Automation

- 

✅ 哪些服務免費？

❓ 題目重述與需求解析

A company is migrating applications to AWS. The applications are deployed in different accounts. The company manages the accounts centrally by using AWS Organizations. The company’s security team needs a single sign-on (SSO) solution across all the company’s accounts. The company must continue managing the users and groups in its on-premises self-managed Microsoft Active Directory.

✅ 題目要點拆解：

多個 AWS 帳號（Accounts）：表示未來登入操作需支援跨帳號。

使用 AWS Organizations 管理：代表帳號已統一控管，可以與 SSO 整合。

希望有 SSO（Single Sign-On）解決方案：即一個登入入口可以操作多個帳號。

使用者與群組維持在本地的 Microsoft Active Directory（on-prem AD）管理：身份來源（identity source）不在 AWS，需要整合。

🎯 關鍵需求總結：

- 要跨帳號 SSO

- 要與 AWS 原生整合（因為已用 Organizations）

- 要沿用現有的本地 AD 身份系統

- 要選擇維運負擔最小的方式

✅ 正確答案：

A. Enable AWS Single Sign-On (AWS SSO) from the AWS SSO console. Create a one-way forest trust or a one-way domain trust to connect the company’s self-managed Microsoft Active Directory with AWS SSO by using AWS Directory Service for Microsoft Active Directory.

🔍 為什麼選 A？

- AWS SSO（現在叫 AWS IAM Identity Center） 是提供跨帳號單一登入的最佳原生工具。

- 要從本地 Active Directory 同步身份資訊進 AWS，需要透過：

- 

- 一旦信任建立，AWS SSO 就可以讀取 on-prem AD 的使用者和群組，並授予他們跨帳號的訪問權限。

❌ 其他選項錯誤解析：

---
# 2025-06-25 筆記

這題目要找的是：

- 最快速（FASTEST） 聚合方式

- 每個地點每天產生 500 GB 資料

- 全球多個站點、但分析應用只在單一 AWS Region

- 各地點都有高速網路

各選項分析：

A. ✅ S3 Transfer Acceleration + Multipart Uploads

- Transfer Acceleration：

- 

- Multipart Upload：

- 

- ✅ 此選項直接將大量資料上傳至目標 S3 bucket，最快、最直接、全自動

B. 上傳到鄰近 Region，再用 S3 跨區複製

- S3 跨區複製是異步操作，通常會有延遲（幾分鐘～小時）

- 雖然可以分散流量、提升區域寫入效率，但增加了中轉等待時間

- ❌ 不是最快速的聚合方式

C. 每天用 AWS Snowball + 跨區複製

- Snowball 是為了 低網速 or 離線傳輸（數 TB～PB） 設計

- 題目明說有 高速網路，不需要用 Snowball

- ❌ 傳輸時間包含寄送、上架、處理等作業，絕對不是最快方式

D. 上傳至 EC2 → 存 EBS → 快照 → 複製快照 → 還原分析

- 流程太長（至少 4 個步驟），操作複雜且時間拖延

- EBS snapshot 跨區複製也不是即時操作

- ❌ 不是最快，也不是推薦的做法

✅ 最佳選項：

A. Enable Amazon S3 Transfer Acceleration on the destination bucket. Use multipart uploads to directly upload site data to the destination bucket.

💡 簡要理由：

- Transfer Acceleration 能透過最近的 Edge Location 傳送到 S3 原區域，減少網路延遲與封包丟失

- Multipart Upload 能有效處理 大檔案（>100 MB~數百 GB），加速上傳速度

- 無需中轉、無需實體設備、無需手動流程

這題要找的是：

- 對儲存在 Amazon S3 中的 JSON logs 進行查詢

- 查詢為 簡單的 SQL 語句

- 為了 即時需求（on-demand）

- 重點：最少的操作負擔（LEAST operational overhead）

各選項分析：

A. Amazon Redshift

- 屬於資料倉儲服務，需先將資料 ETL 匯入 Redshift

- 適合處理結構化資料與大型查詢，但導入需要：

- 

- ❌ 相對複雜，不符合「最少改動」與「on-demand」需求

B. CloudWatch Logs + SQL 查詢

- CloudWatch Logs 本身不提供 SQL 查詢功能

- 可以做搜尋或過濾，但無法針對 JSON 結構執行完整 SQL 分析

- ❌ 不支援這種 JSON 結構化查詢，功能不符

C. ✅ Amazon Athena 直接查詢 S3 JSON

- Athena 是基於 Presto 的 serverless SQL 查詢服務

- 可直接查詢 S3 上的 JSON、CSV、Parquet 等檔案

- 搭配 AWS Glue Data Catalog 可更容易管理 schema（也可手動定義）

- ✅ 不需移動資料、不需 ETL、serverless、操作負擔極低

- ✅ 非常適合用來對 logs 做 on-demand SQL 分析

D. AWS Glue + Amazon EMR + Spark SQL

- Spark 本身查詢效能高，但：

- 

- ❌ 成本高、維運負擔重，不符合「最少操作」條件

✅ 正確答案：

C. Use Amazon Athena directly with Amazon S3 to run the queries as needed

🔎 加分補充：

- 若 logs 儲存在像這樣的結構化 JSON 檔：

{

"timestamp": "2025-06-24T12:00:00Z",

"level": "INFO",

"message": "User login success",

"userId": "abc123"

}

- 

- 你只需要：

- 

SELECT userId, COUNT(*)

FROM logs

WHERE level = 'ERROR'

GROUP BY userId;

這題的關鍵需求是：

- 公司透過 AWS Organizations 管理多個 AWS 帳號

- 有一個 S3 bucket 在管理帳號中，用來存放報告

- 想要 限制只有 AWS Organizations 內部的帳號能存取這個 bucket

- 強調：最少的操作負擔（LEAST operational overhead）

各選項分析：

A. ✅ 使用 aws:PrincipalOrgID 條件鍵設在 S3 Bucket Policy

- aws:PrincipalOrgID 是 AWS 提供的 全域條件鍵

- 可用於 IAM policy 或 S3 bucket policy 中，限制只有來自指定 AWS Organizations 的帳號才能存取資源

- ✅ 無需針對每個帳號、每個使用者逐一設定

- ✅ 組織中有新帳號加入也會自動套用條件

- ✅ 最少維運成本，最簡單實作

📌 範例 Bucket Policy 範本：

{

"Version": "2012-10-17",

"Statement": [

{

"Sid": "AllowAccessToMyOrg",

"Effect": "Allow",

"Principal": "*",

"Action": "s3:*",

"Resource": [

"arn:aws:s3:::my-org-bucket",

"arn:aws:s3:::my-org-bucket/*"

],

"Condition": {

---
# 2025-06-24 筆記

📘 題目整理：公開文件不可修改/刪除

❓ 題目：

一間律師事務所需向大眾公開數百個檔案。這些檔案必須在指定的未來日期前「不能被修改或刪除」，且「所有人都可以讀取」。哪一個方案最安全、符合需求？

各選項分析：

🅰️ 選項 A

Upload all files to an Amazon S3 bucket that is configured for static website hosting. Grant read-only IAM permissions to any AWS principals that access the S3 bucket until the designated date.

❌ 錯誤原因：

- ✅ Static website hosting 可公開資料。

- ❌ 僅用 IAM 權限 無法保證資料不被刪除或改寫。

- 

- ❌ 沒有使用 S3 Object Lock，無法符合「不可修改/刪除」的需求。

🅱️ 選項 B ✅✅✅（正確）

Create a new Amazon S3 bucket with S3 Versioning enabled. Use S3 Object Lock with a retention period in accordance with the designated date. Configure the S3 bucket for static website hosting. Set an S3 bucket policy to allow read-only access to the objects.

✅ 為什麼正確：

- ✅ S3 Object Lock + Versioning 可以設定保留期，在此期間禁止修改/刪除。

- ✅ 可用 Bucket Policy 設定所有人皆可讀取（public read）。

- ✅ 達成題目要求的「最安全、不可修改、可公開讀取」條件。

- ✅ 使用 static website hosting，可公開提供檔案。

🅲 選項 C

Create a new Amazon S3 bucket with S3 Versioning enabled. Configure an event trigger to run an AWS Lambda function in case of object modification or deletion. Configure the Lambda function to replace the objects with the original versions from a private S3 bucket.

❌ 錯誤原因：

- ❌ 此方法是事後修補，而非事前預防。

- ❌ Lambda 事件觸發有延遲風險，可能來不及恢復資料。

- ❌ 若資料遭到刪除並完全覆蓋，Lambda 無法恢復已遺失資料。

- ❌ 操作與維護成本高（需維護觸發器 + Lambda 邏輯 + 備份機制）。

🅳 選項 D

Upload all files to an Amazon S3 bucket that is configured for static website hosting. Select the folder that contains the files. Use S3 Object Lock with a retention period in accordance with the designated date. Grant read-only IAM permissions to any AWS principals that access the S3 bucket.

❌ 錯誤原因：

- ❌ S3 Object Lock 只能針對「個別物件」設定，不能針對整個 folder。

- ❌ 選定 folder 無法鎖定其中所有物件，可能遺漏或未涵蓋。

- ❌ 使用 IAM read-only 權限雖然限制了大多數存取，但仍無法像 Object Lock 一樣保障不可刪改。

- ❌ 依賴 folder 層級設定會產生誤區，非 AWS 支援的控制範圍。

📝 小結比較表：

## ❓ 題目：三層式 Web 應用程式的快取策略選擇

一家公司在 AWS 上託管一個三層式 Web 應用程式，使用 Multi-AZ Amazon RDS for MySQL 作為資料庫層，Amazon ElastiCache 作為快取層。公司希望在「客戶將項目新增到資料庫時」，快取也會同時新增或更新資料。要求快取中的資料必須永遠與資料庫資料一致。

### ✅ 正確答案：

B. Implement the write-through caching strategy

### ✅ 為什麼選 B（Write-through Caching Strategy）？

- 寫入資料庫時，同步將資料寫入快取。

- 保證快取和資料庫的資料一致性。

- 最適合需要即時同步資料的情境（如本題）。

### ❌ 其他選項錯誤原因

### A. Lazy loading caching strategy（惰性載入）

- 僅在快取未命中（cache miss）時，才從資料庫讀取並寫入快取。

- 不會在資料新增時自動更新快取。

- ❌ 無法保證資料一致性。

### C. Adding TTL caching strategy

- 快取資料會設定有效時間（Time to Live），過期後再查詢資料庫。

- 無法立即反映資料庫的變動。

- ❌ 不能確保快取資料同步更新。

### D. AWS AppConfig caching strategy

- AppConfig 主要用於應用程式設定的動態管理與部署。

- 並非用於資料快取的策略。

- ❌ 不適合本題要求的快取更新需求。

### 📌 策略比較表

👉 選擇 B 能確保資料在資料庫與快取中一致，是本題最佳解。

## ❓ 題目：將 100 GB 歷史資料加密傳輸到 Amazon S3，選擇最低操作負擔的方式

一家公司要從本地端搬移 100 GB 歷史資料到 Amazon S3，並確保「傳輸過程中資料加密」。本地網路為 100 Mbps。新資料將直接儲存於 S3。需選出 最少操作負擔（LEAST operational overhead） 的方法。

### ✅ 正確答案：

B. Use AWS DataSync to migrate the data from the on-premises location to an S3 bucket

### ✅ 為什麼選 B（AWS DataSync）？

- 內建加密傳輸（TLS），符合「加密傳輸」要求。

- 完全托管、支援增量同步與錯誤重試，可最小化人工作業。

- 不需手動建立 VPN、硬碟寄送或管理 CLI 工具與腳本。

- 適合資料量中等（如 100 GB）的遷移任務，操作簡單，維護負擔低。

### ❌ 其他選項錯誤原因

### A. Use s3 sync in AWS CLI

- 雖然可加密（因為使用 HTTPS 上傳），但：

### C. Use AWS Snowball

- 適用於 TB~PB 級資料遷移。

- 運送裝置成本高、流程較繁瑣。

- ❌ 對 100 GB 而言過度複雜，不符合「最少操作負擔」。

### D. 建立 IPsec VPN + 使用 s3 cp

- VPN 建立與維運需較多設定與監控。

- 還要自己處理 CLI 傳輸與錯誤處理。

- 雖符合加密要求，但 ❌ 操作負擔更高。

### 📝 總結

👉 選擇 B 可兼顧安全與操作簡便，是最佳選項。

使用 AWS CLI（如 aws s3 cp 或 aws s3 sync）與使用 AWS DataSync 在移動資料到 Amazon S3 時有以下幾個 關鍵差異，這些差異影響操作負擔、安全性、效能、彈性與錯誤處理能力：

✅ 1.

操作自動化與錯誤處理

✅ 2.

效能與最佳化

✅ 3.

安全性與管理簡便性

---
# 2025-06-22 筆記

🏢 AWS Organizations：讓 R&D 部門脫離母企業建立新組織的正確遷移方式

📌 題目重點

- 公司目前在 AWS Organizations 中有 5 個 OU

- R&D 單位即將獨立，需擁有自己的新 AWS Organization

- 已為 R&D 建立新的 管理帳號（management account）

✅ 正確答案

B. Invite the R&D AWS account to be part of the new organization after the R&D AWS account has left the prior organization

🔍 選項解析

🧭 正確流程補充說明

要讓某個 AWS 帳號從 A 組織遷移到 B 組織，應遵循以下步驟：

從原組織移除帳號

從新組織的管理帳號發出邀請

在 R&D 帳號中接受邀請

✅ 結論

選項 B 符合 AWS Organizations 的設計與限制，且是最簡單、合法且低風險的遷移方式。

🧱 [CloudFormation & IAM] EC2 安全存取 DynamoDB 的最佳方式

📌 題目背景

- 使用 CloudFormation 建立三層式應用（Web Tier / App Tier / DynamoDB）

- Web/App Tier 部署在 EC2 上

- DynamoDB 層不可公開存取

- 要讓 EC2 讀寫 DynamoDB，但 不能暴露 API 金鑰

✅ 正確答案：

B. Create an IAM role that has the required permissions to read and write from the DynamoDB tables. Add the role to the EC2 instance profile, and associate the instance profile with the application instances

🧠 詳細解析

🏁 結論

選項 B 符合最佳實踐：EC2 使用 IAM Role 搭配 Instance Profile 來安全存取 DynamoDB，不需管理金鑰，也避免資訊外洩風險。

📦 [S3 Access Control] 多個 Vendor 存取 S3 Bucket 需最小權限設計

📌 題目需求

- 有多個 vendor AWS 帳號要下載公司存在 S3 的物件

- 公司希望這些帳號擁有最小必要權限（minimum access）

- 要有最低操作負擔（least operational overhead）

✅ 正確答案：

C. Create a cross-account IAM role that has a read-only access policy specified for the IAM role

🧠 詳細解析

🛠 Cross-Account IAM Role 架構

Vendor AWS Account

↓ assume role

Company AWS Account (S3 bucket 所在)

↳ IAM Role (with S3 read-only policy)

↳ S3 Bucket (with trust policy allowing assumeRole)

☑ 步驟概要：

公司端建立 IAM Role

Vendor 使用 STS AssumeRole 存取資源

🏁 結論

選項 C 是最佳實務做法，符合以下條件：

- 安全性高：只允許指定 vendor assume role

- 最小權限：只給 GetObject

- 操作負擔低：集中管理角色與政策即可

☁️ [EC2 DR Strategy] 在 Failover 區域中確保 EC2 容量的災難復原策略

📌 題目需求

- 設計 Disaster Recovery（DR）策略

- 要在 Failover AWS Region 中確保有足夠的 EC2 容量

- 必須保證容量（must meet capacity）

✅ 正確答案：

D. Purchase a Capacity Reservation in the failover Region

🧠 詳細解析

🧾 Capacity Reservation 是什麼？

- 預先保留 EC2 實體容量

- 可與 On-Demand / RI / Savings Plan 並用

- 避免 failover 時高峰期啟動失敗

🔐 關鍵特性：

- 保留指定 AZ、instance type 的 實體資源

- 確保需要時可以立即啟動 EC2 實例

- 適合用於災難復原、HPC 等場景

🏁 結論

若企業要求 failover region 一定要有可用的 EC2 資源，則：

- 只有 Capacity Reservation 能保證容量可用

- 是設計災難復原策略的 唯一正確選擇

✅ 選項 D 是正確答案。

☁️ [S3 Global Secure Sharing] 公司全球員工資料收集與分享的安全解法

📌 題目需求

- 公司需將研究資料收集並存至 Amazon S3

- 全球員工可安全存取資料

- 解法必須是安全、低操作負擔（minimal operational overhead）

✅ 正確答案：

A. Use an AWS Lambda function to create an S3 presigned URL. Instruct employees to use the URL

🧠 詳細解析

🧾 為何選 A？

🔐 S3 Presigned URL 優點：

- 時效性：可設定過期時間

- 最小權限：僅限特定物件、操作（如上傳、下載）

- 低維運：無需建 IAM 帳號與密碼

- 適合全球用戶：透過 HTTPS 存取即可，不受平台限制

⚙️ Lambda 實作方式：

- 使用 IAM 角色給 Lambda 存取 S3 權限

- 依需求產生 getObject 或 putObject 的預簽網址

- 透過前端系統或 API 傳送 URL 給用戶

🏁 結論

若公司想用最低維運成本、高安全性方式將 S3 資料分享給全球員工：

- S3 Presigned URL + Lambda 自動產生 是最佳選擇

✅ 選項 A 為正確答案。

---
# 2025-06-21 筆記

## ✅ RDS PostgreSQL 提供資料科學家近即時唯讀存取的高可用架構

### 題目摘要：

公司想讓資料科學家能 近即時、唯讀存取生產用的 Amazon RDS for PostgreSQL 資料庫。目前資料庫為 Single-AZ 部署。資料科學家的查詢複雜，但不影響主業務。需求是：

- ✅ 唯讀

- ✅ 近即時存取

- ✅ 高可用性

- ✅ 成本效益最佳

### ✅ 正確答案：D. Change the setup from a Single-AZ to a Multi-AZ cluster deployment with two readable standby instances. Provide read endpoints to the data scientists.

### 為什麼選 D？

- Multi-AZ cluster（特別是 Aurora 或新的 RDS Multi-AZ DB cluster）允許部署多個 readable standby instances。

- 可透過 cluster endpoint 給資料科學家 低延遲、近即時的唯讀查詢能力。

- 比起單純的 Multi-AZ standby（無法讀取）或單純 scale-up，更具可用性與成本效益。

- 不會影響主庫效能，且具有 failover 保護。

### ❌ 錯誤選項解析：

### A. Scale the existing production database

- 僅提升主庫效能（e.g. CPU、記憶體）

- ✅ 沒有提供唯讀分流

- ❌ 資料科學家的查詢仍會影響生產主庫

- ❌ 非高可用架構

### B. Multi-AZ with larger secondary standby

- Multi-AZ standby 是 無法用來查詢的，只做故障接手用（❌ 非 readable）

- 提供唯讀存取會失敗

- ❌ 不符合唯讀查詢需求

### C. Multi-AZ + 兩個 read replica

- 雖然符合唯讀需求，但：

- ❌ 成本效益低於 D

### 🔍 小知識補充：

- RDS Multi-AZ DB Cluster（支援 PostgreSQL）：

## ✅ 問題：CloudFront 分區內容發布限制

一間全球影片串流公司使用 Amazon CloudFront 作為 CDN，並希望分階段將內容推出至不同國家。

### 📌 要求：

- 限制內容觀看區域

- 未在推出國家的使用者 不能存取該內容

## 🎯 正確答案：A

Add geographic restrictions to the content in CloudFront by using an allow list. Set up a custom error message.

## ✅ 解釋

- CloudFront 支援地理限制（Geo restriction）

## ❌ 錯誤選項解析

- B. Signed URL 和 Cookies

- C. 加密內容

- D. Time-restricted Signed URLs

## 📘 補充知識：CloudFront 地理限制（Geo Restriction）

- 設定方式：

- 適用場景：

## ✅ 問題：使用 AWS 改善 on-prem 災難復原 (DR)

- 應用程式運行在 VM 上，使用 Microsoft SQL Server Standard

- RPO ≤ 30 秒（資料遺失最多 30 秒）

- RTO ≤ 60 分鐘（1 小時內必須恢復）

- 需求：盡可能降低成本

## 🎯 正確答案：C

Use AWS Elastic Disaster Recovery configured to replicate disk changes to AWS as a pilot light.

## ✅ 解釋：

- AWS Elastic Disaster Recovery (AWS DRS)：

## ❌ 錯誤選項解析

- A. Always On Availability Groups（Enterprise 版）

- B. Warm standby + DMS CDC

- D. 每晚備份 → S3

## 📘 補充：Pilot Light 架構說明

- Pilot Light 架構：

## ✅ 問題：建置一個具有會員登入的 Web 應用程式，訪問模式不可預期且可能長時間 idle，需成本效益高

### 🎯 需求關鍵點：

- 使用者訪問 不穩定且可能 idle → 適合無伺服器架構（serverless）

- 只有 付費用戶才能登入使用

- 需 登入驗證功能

- 要求 成本效益高（MOST cost-effective）

## ✅ 正確答案（3 選項）：

- A. AWS Lambda + API Gateway + DynamoDB

- C. Amazon Cognito User Pool for authentication

- E. AWS Amplify + CloudFront for static frontend hosting

## ✅ 解釋：

### A. Lambda + API Gateway + DynamoDB ✅

- 適合應對不穩定且間歇性訪問（只在需要時觸發）

- 按次計費、免管理伺服器，成本效益高

- DynamoDB 適合低延遲、無伺服器的 key-value 存取

### C. Cognito User Pool ✅

- 提供 會員註冊與登入驗證（authentication） 的完整方案

- 可搭配 API Gateway + Lambda 驗證授權，保護資源

- 支援 OAuth2、MFA、第三方登入等，免自建登入機制

### E. AWS Amplify ✅

- 適合前端 static web hosting（HTML、CSS、JS）

- 預設整合 CloudFront，提供高效能 CDN 傳遞

- 成本低、部屬簡便，適合快速建置網站

## ❌ 錯誤選項解析：

### B. ECS + RDS ❌

- ECS 需長期運行 container，成本較高

---
# 2025-06-20 筆記

## ❓ 題目：會計資料遷移至 AWS 受管服務（需支援不可變與加密驗證記錄）

情境：

公司現有會計系統部署於 EC2，自建環境成本高，需遷移至 AWS 受管服務，並滿足以下條件：

- ✅ 低維運負擔（managed service）

- ✅ 資料不可修改（immutable）

- ✅ 可驗證變更記錄（cryptographically verifiable）

- ✅ 成本效益考量

### ✅ 正確選項解析：

D. Amazon QLDB (Quantum Ledger Database)

- AWS 管理型分類帳型資料庫（ledger DB）

- 支援 不可變資料寫入記錄（immutable append-only journal）

- 支援 加密驗證（cryptographic hashing）確保歷史資料完整性

- 適用於會計、審計、金融交易記錄

- 不需自行管理底層基礎設施 → 維運負擔低

### ❌ 錯誤選項解析：

A. Amazon Redshift

- 是數據倉儲（data warehouse），非用於記錄不可變交易

- 適用於 OLAP 分析用途，不是專為 immutable logs 設計

- 不具原生的加密驗證或 append-only log 設計

B. Amazon Neptune

- 圖形資料庫（graph DB），適用於處理節點/關係分析（如社交網絡）

- 不具不可變 append-only journal 或加密驗證特性

C. Amazon Timestream

- 時間序列資料庫，適用於 IoT、監控資料等時間序列紀錄

- 無法提供 cryptographic verifiability 與 immutable log 設計

### ✅ 總結建議：

📌 推薦使用 Amazon QLDB 作為符合會計應用需求的最佳選擇

## ❓ 題目：在 AWS 上安全管理應用設定與憑證，且維運負擔最小

情境說明：

公司開發應用程式連接到 Amazon RDS，需達成以下目標：

- 管理應用程式設定（AppConfig or equivalent）

- 安全儲存並擷取資料庫及服務憑證（如帳號密碼）

- 維運負擔低（如自動輪替、集中控管、整合 IAM）

### ✅ 正確選項解析：

A. AWS AppConfig + AWS Secrets Manager

- AWS AppConfig：用於集中管理應用程式設定（包含部署版本控制、環境差異、rollout 控制）

- AWS Secrets Manager：

- ✅ 完全受管服務

- ✅ 最小維運負擔（不需自行開發加密與權限系統）

### ❌ 錯誤選項解析：

B. AWS Lambda + SSM Parameter Store

- Lambda 並不是設定管理工具，用來儲存與管理設定不符合設計意圖

- Systems Manager Parameter Store 雖支援密鑰儲存，但：

C. Encrypted config file in S3

- 雖可用 S3 儲存加密檔案，但需：

- 缺乏設定版本控制、變更管理、自動輪替等原生支援

D. AWS AppConfig + Amazon RDS for credentials

- ❌ Amazon RDS 並不是用來儲存應用程式憑證

- 資料庫不適合作為 secrets 儲存來源，缺乏加密、輪替與 IAM 整合能力

### ✅ 結論建議

📌 最推薦解法：使用 AppConfig 配置應用程式設定 + Secrets Manager 管理與存取密碼或 API 金鑰

## ❓ 題目：如何最省成本與最少設定地標準化 EBS Volume 加密檢查

情境說明：

- 公司想要標準化 EBS 加密策略

- 並希望可以自動檢查所有 volume 是否都有加密

- 同時要 成本低 且 設定步驟少（Low configuration effort）

### ✅ 正確選項解析：

D. AWS Config + EBS encryption rule

- AWS Config：是一個受管服務，可自動評估 AWS 資源的設定是否符合規則。

- 你可以使用 Config 內建的管理規則（managed rule）：

- ✅ 無需自建 Lambda、撰寫程式或排程機制

- ✅ 自動監控與報告，不需定期手動觸發

### ❌ 錯誤選項解析：

A. Lambda + EventBridge + DescribeVolumes

- 雖然可達成目的，但：

B. Fargate Task + DescribeVolumes

- 同樣需自己開發檢查邏輯

- 還需配置 Fargate Task 定期執行 + IAM 權限

- 成本高於 Lambda，維護複雜度更高

C. 用 IAM 限制 + Cost Explorer 檢查

- 無法直接評估 EBS 是否加密

- 依靠 tags 與人工識別成本高且容易出錯

- ❌ 不適合作為加密策略標準化手段

### ✅ 總結建議

📌 最佳解法：使用 AWS Config 內建規則 encrypted-volumes 自動檢查 EBS 加密狀況，無需撰寫程式碼或排程

## ❓ 題目：自動化執行多個並行與串行資料預處理工作，並具備錯誤處理與狀態管理

需求摘要：

- 多來源資料上傳至 Amazon S3

- 資料預處理工作需：

- 希望最小化 錯誤處理、重試與狀態管理的維運負擔

### ✅ 正確選項解析

C. AWS Glue DataBrew + AWS Step Functions

- Glue DataBrew：可視化無程式碼的資料清理與轉換服務，適合 ETL 前處理

- Step Functions：

✅ 滿足：

- 並行 + 有順序的任務流程需求

---
# 2025-06-19 筆記

# 📘 AWS 錯題整理筆記

❌ Q1: 跨帳號給 SQS 權限

題目：

A development team is collaborating with another company to create an integrated product. The other company needs to access an Amazon Simple Queue Service (Amazon SQS) queue that is contained in the development team’s account. The other company wants to poll the queue without giving up its own account permissions to do so.

選項：

- A. Create an instance profile that provides the other company access to the SQS queue.

- B. Create an IAM policy that provides the other company access to the SQS queue.

- C. ✅ Create an SQS access policy that provides the other company access to the SQS queue.

- D. Create an Amazon SNS access policy that provides the other company access to the SQS queue.

解釋：

- ✅ C 是正解：SQS queue 屬於支援資源型 policy 的 AWS 服務，可以透過 SQS access policy 授權其他帳號的角色或使用者來存取 queue。

- ❌ A 是 EC2 專用的機器角色 profile，與 SQS 沒關。

- ❌ B 是 identity-based policy，無法給別人帳號的使用者權限。

- ❌ D 是 SNS 的權限設定，無法用來控制 SQS 存取權限。

❌ Q2: 適合備份 NFS 資料的最低成本方案

題目：

A company has NFS servers in an on-premises data center that need to periodically back up small amounts of data to Amazon S3.

選項：

- A. Set up AWS Glue to copy the data from the on-premises servers to Amazon S3.

- B. ✅ Set up an AWS DataSync agent on the on-premises servers, and sync the data to Amazon S3.

- C. Set up an SFTP sync using AWS Transfer for SFTP to sync data from on premises to Amazon S3.

- D. Set up an AWS Direct Connect connection between the on-premises data center and a VPC, and copy the data to Amazon S3.

解釋：

- ✅ B 是正解：AWS DataSync 專為高效搬移資料而設計，支援 NFS 且能安全快速地同步資料到 S3，並能控制頻率與排程，是最省成本與最低管理負擔的方案。

- ❌ A：Glue 是 ETL 工具，不適合做簡單檔案備份。

- ❌ C：AWS Transfer for SFTP 適合與使用者互動式檔案傳輸，不適合備份用途且維運成本較高。

- ❌ D：Direct Connect 適合大流量資料中心對雲端的專線連接，不適合小量備份。

❌ Q3: RDS 效能瓶頸，如何改善位置追蹤服務

題目：

A company has deployed a multiplayer game for mobile devices. The game requires live location tracking of players based on latitude and longitude. The data store for the game must support rapid updates and retrieval of locations. Currently using Amazon RDS for PostgreSQL with read replicas, but under peak load, performance drops.

選項：

- A. Take a snapshot of the existing DB instance. Restore the snapshot with Multi-AZ enabled.

- B. Migrate from Amazon RDS to Amazon Elasticsearch Service (Amazon ES) with Kibana.

- C. Deploy Amazon DynamoDB Accelerator (DAX) in front of the existing DB instance. Modify the game to use DAX.

- D. ✅ Deploy an Amazon ElastiCache for Redis cluster in front of the existing DB instance. Modify the game to use Redis.

解釋：

- ✅ D 是正解：ElastiCache for Redis 可用於儲存快取資料（如即時位置），提供毫秒級延遲，大幅降低 DB 負載。

- ❌ A：Multi-AZ 是為了高可用性設計，無法改善效能瓶頸。

- ❌ B：ES 是全文索引與分析服務，不適合快速寫入與查詢的即時遊戲位置追蹤。

- ❌ C：DAX 是給 DynamoDB 用的快取，不適用於 RDS。

# 🔐 AWS 登入驗證機制整理

## 一、身份驗證（Authentication）與授權（Authorization）

- Authentication（驗證）：你是誰？（帳號密碼、OTP、多因子）

- Authorization（授權）：你能做什麼？（角色、權限、資源訪問）

## 二、AWS 提供的身份驗證機制一覽

## 三、Amazon Cognito 詳解

### ✅ Cognito User Pools

- 管理 App 使用者帳號與登入

- 支援：

- 可整合到前端 Web / App / API Gateway

### ✅ Cognito Identity Pools

- 將登入的使用者映射為 IAM Role

- 可訪問 S3、DynamoDB 等 AWS 資源

- 通常搭配 User Pools 使用

## 四、IAM Identity Center（AWS SSO）

- 提供跨 AWS Account 的統一登入入口

- 可連接：

- 功能：

## 五、選擇建議

## ❌ 錯題整理：EKS + Fargate 儲存方案

題目：

A company is deploying a new application to Amazon EKS with an AWS Fargate cluster. The application needs a storage solution for data persistence. The solution must be highly available and fault tolerant. The solution also must be shared between multiple application containers. Which solution will meet these requirements with the LEAST operational overhead?

選項：

- A. Create Amazon EBS volumes in the same AZs where EKS worker nodes are placed. Register the volumes in a StorageClass object on an EKS cluster. Use EBS Multi-Attach to share the data between containers.

- B. ✅ 正確答案：Create an Amazon EFS file system. Register the file system in a StorageClass object on an EKS cluster. Use the same file system for all containers.

- C. Create an Amazon EBS volume. Register the volume in a StorageClass object on an EKS cluster. Use the same volume for all containers.

- D. Create Amazon EFS file systems in the same AZs where EKS worker nodes are placed. Register the file systems in a StorageClass object on an EKS cluster. Create an AWS Lambda function to synchronize the data between file systems.

解析：

- EFS 是一種共享型、高可用、橫向擴展的檔案系統，支援跨 AZ 並與 Fargate 搭配使用，最適合做為容器的共享儲存。

- EBS 不支援跨多容器共享或 Fargate。

- 建立多個 EFS 並用 Lambda 同步是額外負擔，非最佳解。

## ❌ 錯題整理：行動 App 上傳內容最低延遲策略

題目：

A company has a new mobile app. Users access content often in the first minutes after the content is posted. 90% of the content is consumed within the AWS Region where it is uploaded. Which solution will optimize the user experience by providing the LOWEST latency for content uploads?

選項：

- A. Upload and store content in Amazon S3. Use Amazon CloudFront for the uploads.

- B. Upload and store content in Amazon S3. Use S3 Transfer Acceleration for the uploads.

- C. Upload content to Amazon EC2 instances in the Region that is closest to the user. Copy the data to Amazon S3.

- D. ✅ 正確答案：Upload and store content in Amazon S3 in the Region that is closest to the user. Use multiple distributions of Amazon CloudFront.

解析：

- 選 D 是最佳策略，直接將內容上傳到最接近使用者的 S3，再透過多個 CloudFront distribution 加速內容傳送。

- A 錯在 CloudFront 是用來做下載內容快取，不能上傳。

- B 的 Transfer Acceleration 適合跨區域上傳，不適合大多為單一區域的內容。

- C 把資料繞到 EC2 會增加延遲與複雜度。

## ❌ 錯題整理：需風險感知 MFA 的登入系統設計

題目：

A solutions architect is designing a user authentication solution. The solution must invoke two-factor authentication for users logging in from inconsistent geo-locations, IPs, or devices. It must scale to millions of users.

選項：

- A. ✅ 正確答案：Configure Amazon Cognito user pools for user authentication. Enable the risk-based adaptive authentication feature with multi-factor authentication (MFA)

- B. Configure Amazon Cognito identity pools for user authentication. Enable multi-factor authentication (MFA)

- C. Configure AWS IAM users for user authentication. Attach an IAM policy that allows the AllowManageOwnUserMFA action

---
# 2025-06-18 筆記

# 📦 npx 與 tsx 比較與使用筆記

## 🧠 什麼是 npx？

`npx` 是 Node.js 附帶的工具（來自 `npm`），用來**執行 Node 套件**而不需要全域安裝它們。

### 📌 特點：

- 可以執行本地或遠端的 npm 套件
- 預設會**優先執行專案內的套件**
- 若本地不存在，會**臨時從 npm 下載**後執行
- 適合用於**一次性執行工具命令**

---

## 🧪 使用範例

```bash
npx create-react-app my-app
npx tsx src/index.ts


## ⚠️ npx 的潛在問題

## 🧰 本地安裝 vs 使用 npx

## 🛠️ 建議用法：搭配 tsx 使用

### ✅ 推薦做法（專案內安裝 tsx）

npm install --save-dev tsx


在 package.json 中加入：

"scripts": {
  "dev": "tsx src/index.ts"
}


執行：

npm run dev


✅ 這樣可以確保使用本地版本的 tsx，且開發過程穩定、快速。

## 🧪 要怎麼確認執行的是本地的 tsx？

你可以這樣寫：

"scripts": {
  "dev": "which tsx && tsx src/index.ts"
}


輸出應該會是：

./node_modules/.bin/tsx


## ✅ 總結

- npx 適合「一次性執行工具」

- tsx 建議「本地安裝 + npm script 執行」

- 開發與部署流程中應避免用 npx 呼叫 tsx

### 🔄 使用 nodemon 自動重啟（開發環境）

### 建議建立 nodemon.json：


{
  "watch": ["src"],
  "ext": "ts,tsx",
  "ignore": ["node_modules", "dist"],
  "exec": "npx tsx src/index.ts",
  "legacyWatch": true}



✅ legacyWatch: true 對於 WSL 或 Docker 特別重要！

### 加入 package.json script：


{
  "scripts": {
    "dev": "nodemon"
  }
}



### 執行：


npm run dev



## ✅ 常見問題與解法

## 📝 延伸推薦

- 可搭配 dotenv 處理 .env 環境變數

- 可搭配 tsconfig.json 使用 "module": "esnext" + "target": "es2020"，最佳化 tsx 效能

- 可用 pm2 管理正式部署（nodemon 僅供開發）

你目前的 types.d.ts 是用來放 函式簽名（declaration） 的，屬於 TypeScript 的「宣告型別檔案」格式，通常會這樣用：

// types.d.ts
declare function myGlobalFn(x: number): string


這是給 全域函數或沒有模組的第三方函式庫補型別 用的。

### ✅ 建議做法：不要把 report 型別放進 types.d.ts

因為：

- types.d.ts 主要是宣告 global 或補第三方函式型別，不適合放業務邏輯用的 model。

- 放在那邊可能會讓 Report 型別變成全域的，增加維護成本。

- 你之後會有越來越多 model（例如 User, Post, Comment），分開會更清楚。

### ✅ 建議目錄結構：

src/
├── types/
│   ├── db.ts         # 放各種資料表 model，例如 Report
│   └── types.d.ts    # 放 declare function / global types


### ✅ 建議內容（src/types/db.ts）：

export interface Report {
  cid: string
}


然後你在使用的地方匯入：

import { Report } from '../types/db'


### ✅ 加分技巧：index.ts 整合所有型別（可選）

// src/types/index.ts
export * from './db'


這樣其他地方可以這樣引入：

import { Report } from '../types'


### ✅ 使用方式

import { Report } from '../types/db'


### ✅ 可選：使用 types/index.ts 整合

// index.ts
export * from './db'


## 📌 型別檔（Declaration File）是什麼？

TypeScript 的型別檔（副檔名為 .d.ts）是用來描述一個函數、物件、模組或全域變數的型別，但不包含實作邏輯。常用於：

- 為沒有型別定義的 JS 套件提供型別提示（如 @types/xxx）

- 描述全域變數或全域函式的型別

- 在專案中集中管理型別定義

## 📁 為什麼放在 types.d.ts 就能被找到？

### ✅ TypeScript 編譯器會自動載入 .d.ts：

專案中任何位置的 .d.ts 檔案 都會被自動載入，只要：

不需要顯式 import，只要是全域型別就能生效

例如你的 tsconfig.json 包含：

"include": ["src", "types.d.ts"]


就會把 types.d.ts 自動編入整個專案的型別上下文。

## 🔍 為什麼 func.ts 不行？

因為 .ts 是一般模組程式碼檔案，不會被當作全域型別檔處理，具體行為有差：

### ✅ 正確用法：

- 想要全域型別生效：請寫在 .d.ts 裡

- 若是模組型別或具體邏輯，請使用 .ts 並搭配 import

## 🧠 延伸建議：如何組織大型專案型別？

src/
  types/
    global.d.ts         # 全域型別定義
    report.d.ts         # 特定功能模組的型別
  controllers/
  db/
  index.ts
tsconfig.json


tsconfig.json 內：

{
  "include": ["src"]
}


---
# 2025-06-17 筆記



---

## 📦 套件安裝

```bash
npm install @web3-storage/w3up-client @web3-storage/file


## 📁 專案結構建議

project-root/
├── .w3up/                      # 儲存 Agent 身份與 delegation 憑證
├── example.txt                # 要上傳的測試檔
└── upload.ts                  # 主程式入口


## ✨ 完整範例：從登入到上傳

import { create } from '@web3-storage/w3up-client'
import { File } from '@web3-storage/file'
import fs from 'fs'

async function main() {
  const client = await create()

  // 1. 使用 Email 登入（只需執行一次）
  const email = 'you@example.com'
  console.log(`📨 Sending login link to ${email}...`)
  const account = await client.login(email)

  // 2. 等待驗證與選擇方案
  console.log('⏳ Waiting for login confirmation...')
  await account.plan.wait()
  console.log('✅ Email verified and plan active!')

  // 3. 建立 Space
  const space = await client.createSpace('my-space', { account })
  await client.setCurrentSpace(space.did())
  console.log('🪐 Space created:', space.did())

  // 4. 上傳本地檔案
  const buffer = fs.readFileSync('example.txt')
  const file = new File([buffer], 'example.txt')
  const result = await client.uploadFile(file)

  console.log('📦 Uploaded CID:', result.cid.toString())
  console.log(`🔗 View on IPFS: https://${result.cid}.ipfs.w3s.link`)
}

main().catch(console.error)


## 📌 login 流程說明

## 🔐 檢查是否已登入

可用 client.hasAccount() 判斷是否需要再次登入：

if (!(await client.hasAccount())) {
  const account = await client.login('you@example.com')
  await account.plan.wait()
}


## 🗂 多次使用 Space

await client.setCurrentSpace('<space-did>')


你可以在多個 Space 間切換，只要之前有建立過或 addSpace() 進來的 delegation。

## 📂 上傳相關 API

## 🔗 預覽網址格式

https://${cid}.ipfs.w3s.link


## 🧠 補充說明

- 登入與 Space 建立只需執行一次，除非：

- 若部署在 Lambda/Docker，請使用 delegation 模式（BYOD）

---
# 2025-06-13 筆記

# 🧠 AWS 錯題整理筆記（含選項與解析）

❌ 題目一：EC2 + RDS 要防 SQL Injection

題目敘述：

公司將應用部署在 Amazon EC2，資料庫為 Amazon RDS，已實作最小權限。安全團隊希望防範 SQL injection 與其他 Web 攻擊，請選擇操作負擔最小的解法。

✅ 正確答案：B. 使用 AWS WAF 保護應用程式，使用 RDS parameter group 強化設定

- AWS WAF 可即時防禦 SQL injection、XSS 等 Web 攻擊

- 搭配 RDS 的 parameter group 可強化安全設定（如強制 SSL、啟用 log）

- 屬於低操作負擔、易於維運的解法

🔍 選項比較：

❌ 題目二：跨帳號微服務 HTTPS 溝通與 Service Registry

題目敘述：

每個微服務由不同團隊在不同 AWS 帳號中維運，需跨帳號/VPC 溝通（使用 HTTPS），並具備服務註冊與發現能力。要求「最少的管理負擔」。

✅ 正確答案：B. 建立 VPC Lattice Service Network，提供 HTTPS 與服務註冊

- AWS VPC Lattice 為新服務，支援跨帳號/跨 VPC 的 service-to-service 溝通

- 支援服務註冊、自動解析與 IAM 控制權限

- 可設定 HTTPS listener，操作簡單、彈性強

🔍 選項比較：

❌ 題目三：LDAP 不支援 SAML，但要登入 AWS Console

題目敘述：

公司內部使用 LDAP 驗證身份，但該 LDAP 不支援 SAML，仍希望讓使用者透過 LDAP 驗證登入 AWS Console。

✅ 正確答案：D. 開發自訂 Identity Broker，透過 AWS STS 獲取短期憑證

- 建立公司內部的身份中介系統，驗證 LDAP 後呼叫 AWS STS AssumeRole

- 回傳的臨時憑證可登入 AWS Console 或使用 CLI / API

- 此方式為 AWS 官方建議，適用於非 SAML 系統整合

🔍 選項比較：

# 🧠 AWS 錯題整理筆記（含選項與解析）

❌ 題目一：禁止 Security Group 開放 SSH (22) 到 0.0.0.0/0，並觸發通知

題目需求：

- 偵測是否有 EC2 Security Group 對全世界開放 SSH

- 違規時自動通知

- 最少操作負擔（least operational overhead）

✅ 正確解法：

B. Enable the restricted-ssh AWS Config managed rule and generate an Amazon SNS notification

- AWS Config 可偵測不合規資源設定

- restricted-ssh 是官方提供的規則，專門用來偵測 22 port 開到 0.0.0.0/0

- 搭配 SNS 可自動發出通知

- ✅ 最低維運、立即上線、最安全

🔍 錯誤選項分析：

❌ 題目二：了解 AWS Config vs AWS Trusted Advisor 差異

你的問題： Tag 與安全性監控用 AWS Config 和 Trusted Advisor 有什麼差異？

✅ 關鍵比較整理：

❌ 題目三：多區域 EC2 + HTTP 應用，需支援固定 IP + 防 Web 攻擊 + 高效能存取

題目需求：

- 多區域 EC2 HTTP 應用

- ✅ 要有固定 IP（Static IP）

- ✅ 要防禦 Web 攻擊（如 SQL Injection）

- ✅ 要全球高效能路由與高可用

✅ 正確解法：

B. EC2 → ALB + AWS WAF → Global Accelerator

- ALB 支援 Layer 7 路由，可套用 WAF

- Global Accelerator 提供全球 static IP，支援跨區健康檢查與路由

- ✅ 同時滿足：固定 IP、高效能、可用性與安全性

🔍 錯誤選項分析：

❌ 題目四：防止 EC2 建立時未加上指定 tag，且不得刪除 tag（使用 AWS Organizations）

題目需求：

- EC2 必須加上 data-sensitivity tag（值為 sensitive / nonsensitive）

- 不可建立未標記資源，也不可刪除該 tag

- 使用 AWS Organizations 內的 OU 管理策略

✅ 正確組合解法：

🔍 錯誤選項分析：

# 🧠 AWS 錯題整理筆記（Markdown 版）

❌ 題目一：Textract 處理 PDF 並分析內容與情緒（sentiment）

題目需求：

- 處理過去 5 年的 PDF 新聞資料

- 必須使用 Amazon Textract

- 需分析內容與情緒（sentiment）

- ✅ 要求 最低操作負擔（least operational overhead）

✅ 正確解法：

C. Provide the extracted insights to Amazon Comprehend for analysis. Save the analysis to an Amazon S3 bucket.

- Textract：OCR 擷取 PDF 內容

- Comprehend：情緒分析與 NLP（全託管，免訓練模型）

- S3：存放結果，方便後續處理或可視化

- ✅ 符合最低操作負擔

❌ 錯誤選項分析：

❌ 題目二：DynamoDB 讀不到最新資料

題目需求：

- 應用使用 DynamoDB

- 觀察到讀取結果不是最新資料

- ✅ 延遲 acceptable，效能正常

- 需找出解決辦法以讀到「最新資料」

✅ 正確解法：

C. Request strongly consistent reads for the table

- DynamoDB 預設是 eventually consistent，會導致讀取到舊資料

- 開啟 ConsistentRead=True 可保證讀取到最新寫入資料

- ✅ 不需改變資料結構或配置，低風險又立即生效

❌ 錯誤選項分析：

# 📦 AWS Storage Gateway - Volume Gateway 筆記整理

AWS Storage Gateway 的 Volume Gateway 提供兩種模式，用於在本地資料中心與 AWS 雲端之間整合儲存與備份需求：

## 🧰 模式比較表

---
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