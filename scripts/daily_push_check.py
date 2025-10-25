from notion_client import Client
from dotenv import load_dotenv
import os
from datetime import datetime
from pathlib import Path

load_dotenv()
notion = Client(auth=os.getenv("NOTION_TOKEN"))
page_id = os.getenv("NOTION_PAGE_ID")

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

if __name__ == "__main__":
    today_title = datetime.today().strftime("%y/%m/%d")  # e.g., 0530
    child_page_id = find_child_page_block(page_id, today_title)
    today = datetime.today().strftime("%Y-%m-%d")
    os.makedirs("daily-notes", exist_ok=True)
    filepath = f"daily-notes/{today}.md"
    if not child_page_id:
        print(f"⚠️ 找不到子頁面：{today_title}")
        content = "今天休息"
        with open(filepath, "w", encoding="utf-8") as f:
            f.write(content)
        print(f"已寫入 {today}.md")
    else :
        content_lines = fetch_blocks(child_page_id)
        content = "\n\n".join(content_lines)

        
        with open(filepath, "w", encoding="utf-8") as f:
            f.write(content)

