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
BASE_DIR = Path(__file__).resolve().parent.parent
CONTENT_DIR = BASE_DIR / "content"
CONTENT_DIR.mkdir(exist_ok=True)

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
    """抓取頁面所有 block 並轉成 Markdown"""
    blocks = notion.blocks.children.list(block_id=block_id)["results"]
    return [block_to_markdown(b) for b in blocks if block_to_markdown(b)]

def find_child_page_block(parent_page_id, target_title):
    """在父頁面中找到子頁面"""
    blocks = notion.blocks.children.list(block_id=parent_page_id)["results"]
    for block in blocks:
        if block["type"] == "child_page":
            title = block["child_page"]["title"]
            if title == target_title:
                return block["id"]
    return None

# === 主程式 ===
if __name__ == "__main__":
    today_title = datetime.today().strftime("%y/%m/%d")  # 例如 "25/10/25"
    today_date = datetime.today().strftime("%Y-%m-%d")   # 例如 "2025-10-25"

    print(f"🗓️  正在處理日記：{today_title}")

    # 找出 Notion 的今日子頁面
    child_page_id = find_child_page_block(page_id, today_title)

    if not child_page_id:
        print(f"⚠️ 找不到子頁面：{today_title}")
        fallback_path = CONTENT_DIR / "daily-notes"
        fallback_path.mkdir(parents=True, exist_ok=True)
        file_path = fallback_path / f"{today_date}.md"
        with open(file_path, "w", encoding="utf-8") as f:
            f.write("今天沒有內容。")
        print(f"✅ 已寫入空白日記：{file_path.relative_to(BASE_DIR)}")
        exit()

    # 抓取 Notion 內容
    content_lines = fetch_blocks(child_page_id)
    if not content_lines:
        print("⚠️ 該頁面沒有內容。")
        exit()

    # 分析結構
    category = None
    title = None
    body_lines = []

    for line in content_lines:
        if line.startswith("# "):        # 第一個 heading_1
            category = line[2:].strip().replace(" ", "_")
        elif line.startswith("## "):     # 第一個 heading_2
            title = line[3:].strip().replace(" ", "_")
        else:
            body_lines.append(line)

    # 檢查資料是否完整
    if not category:
        category = "daily-notes"
    if not title:
        title = today_date

    # === 儲存分類檔案 ===
    category_dir = CONTENT_DIR / category
    category_dir.mkdir(parents=True, exist_ok=True)

    file_path = category_dir / f"{title}.md"
    with open(file_path, "w", encoding="utf-8") as f:
        f.write("\n\n".join(body_lines))

    print(f"✅ 已儲存分類筆記：{file_path.relative_to(BASE_DIR)}")

    # === 同步儲存原文 (完整版本) ===
    daily_dir = CONTENT_DIR / "daily-notes"
    daily_dir.mkdir(parents=True, exist_ok=True)

    full_path = daily_dir / f"{today_date}.md"
    with open(full_path, "w", encoding="utf-8") as f:
        f.write("\n\n".join(content_lines))

    print(f"📝 已儲存原始版本：{full_path.relative_to(BASE_DIR)}")
