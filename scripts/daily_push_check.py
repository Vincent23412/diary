from notion_client import Client
from dotenv import load_dotenv
import os
from datetime import datetime
from pathlib import Path

# === 初始化 ===
load_dotenv()
notion = Client(auth=os.getenv("NOTION_TOKEN"))
page_id = os.getenv("NOTION_PAGE_ID")

# === 專案根目錄與儲存路徑 ===
BASE_DIR = Path(__file__).resolve().parent.parent  # /scripts -> 回到專案根目錄
CONTENT_DIR = BASE_DIR / "content" / "daily-notes"
CONTENT_DIR.mkdir(parents=True, exist_ok=True)

# === Notion Block 處理 ===
def block_to_markdown(block):
    block_type = block["type"]
    text = block.get(block_type, {}).get("rich_text", [])
    content = "".join([t.get("plain_text", "") for t in text]) if text else ""
    if block_type == "heading_1":
        return f"# {content}"
    elif block_type == "heading_2":
        return f"## {content}"
    elif block_type == "heading_3":
        return f"### {content}"
    elif block_type == "bulleted_list_item":
        return f"- {content}"
    elif block_type == "paragraph":
        return content
    else:
        return content

def fetch_blocks(block_id):
    blocks = notion.blocks.children.list(block_id=block_id)["results"]
    return [block_to_markdown(b) for b in blocks if block_to_markdown(b)]

def find_child_page_block(parent_page_id, target_title):
    blocks = notion.blocks.children.list(block_id=parent_page_id)["results"]
    for block in blocks:
        if block["type"] == "child_page":
            title = block["child_page"]["title"]
            if title == target_title:
                return block["id"]
    return None

# === 主程式 ===
if __name__ == "__main__":
    today_title = datetime.today().strftime("%y/%m/%d")  # Notion 頁面名稱格式（例如 25/10/25）
    today = datetime.today().strftime("%Y-%m-%d")        # 檔名格式
    filepath = CONTENT_DIR / f"{today}.md"

    print(f"🗓️  今日頁面名稱: {today_title}")
    print(f"📁  儲存路徑: {filepath}")

    child_page_id = find_child_page_block(page_id, today_title)

    if not child_page_id:
        print(f"⚠️ 找不到子頁面：{today_title}")
        content = "今天休息。"
    else:
        content_lines = fetch_blocks(child_page_id)
        content = "\n\n".join(content_lines) or "（此頁面沒有內容）"

    with open(filepath, "w", encoding="utf-8") as f:
        f.write(content)

    print(f"✅ 已寫入 {filepath.relative_to(BASE_DIR)}")
