#!/usr/bin/env python3
import os
import datetime
import re
import markdown
from pathlib import Path

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))  # 回到專案根目錄

CONTENT_DIR = os.path.join(BASE_DIR, "content")
SITE_DIR = os.path.join(BASE_DIR, "site")
NOTES_DIR = os.path.join(SITE_DIR, "notes")
TEMPLATE_PATH = os.path.join(NOTES_DIR, "_category.template.html")
NOTES_INDEX_PATH = os.path.join(NOTES_DIR, "index.html")
HOME_PATH = os.path.join(SITE_DIR, "index.html")


# TODO site 的主要 index 還沒自動增加筆記分類條目

# === 輔助函式 ===
def read_file(path):
    with open(path, "r", encoding="utf-8") as f:
        return f.read()

def write_file(path, content):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        f.write(content)

def get_categories():
    """回傳 {category: [markdown files]}"""
    categories = {}
    for root, dirs, files in os.walk(CONTENT_DIR):
        for d in dirs:
            folder = os.path.join(root, d)
            md_files = [f for f in os.listdir(folder) if f.endswith(".md")]
            if md_files:
                categories[d] = sorted(md_files)
    return categories

# === 主流程 ===
def build_site():
    print("🚀 開始生成靜態網站...")
    categories = get_categories()
    print(f"找到 {len(categories)} 個分類。")

    if not categories:
        print("⚠️ 沒有找到任何分類資料夾。")
        return

    template = read_file(TEMPLATE_PATH)
    date_str = datetime.date.today().isoformat()

    # === 生成每個分類的 HTML 頁 ===
    POST_TEMPLATE_PATH = os.path.join(NOTES_DIR, "_post.template.html")

    for category, files in categories.items():
        category_name = category.replace("_", " ").title()
        category_dir = os.path.join(NOTES_DIR, category)
        os.makedirs(category_dir, exist_ok=True)

        # === 分類總覽 index.html ===
        category_index = os.path.join(category_dir, "index.html")

        html = read_file(TEMPLATE_PATH)
        html = (
            html.replace("{{CATEGORY_NAME}}", category_name)
                .replace("{{CATEGORY_SLUG}}", category)
        )

        post_items = ""
        for filename in files:
            title = filename.replace(".md", "").replace("_", " ").title()
            html_name = filename.replace(".md", ".html")
            post_items += f"""
    <li class="post-item">
    <a class="post-link" href="{html_name}">{title}</a>
    </li>
    """
            # 用正則安全地替換多行註解區塊
        html = re.sub(
            r"<!-- AUTO-GENERATED: posts[\s\S]*?-->",
            post_items,
            html
        )

        # 更新最後更新日期（同樣安全替換）
        html = re.sub(
            r"<!-- AUTO-GENERATED: last-updated[\s\S]*?-->",
            date_str,
            html
        )

        write_file(category_index, html)
        print(f"✅ 更新/建立 {category_index}")

        # === 為每篇文章建立 HTML ===
        post_template = read_file(POST_TEMPLATE_PATH)
        for filename in files:
            title = filename.replace(".md", "").replace("_", " ").title()
            md_path = os.path.join(CONTENT_DIR, category, filename)
            raw_url = f"https://raw.githubusercontent.com/Vincent23412/diary/main/content/{category}/{filename}"
            blob_url = f"https://github.com/Vincent23412/diary/blob/main/content/{category}/{filename}"

            # 讀取 Markdown 內容
            with open(md_path, "r", encoding="utf-8") as f:
                md_content = f.read()

            # 轉換 Markdown → HTML
            html_body = markdown.markdown(
                md_content,
                extensions=[
                    "fenced_code",    # 支援 ``` 區塊
                    "tables",         # 支援表格
                    "codehilite",     # 支援語法高亮（需要 pygments）
                    "toc",            # 自動生成目錄
                    "sane_lists"      # 更接近 GitHub 的清單行為
                ]
            )

            # 插入模板
            post_html = (
                post_template
                .replace("{{POST_TITLE}}", title)
                .replace("{{CATEGORY_SLUG}}", category)
                .replace("{{RAW_URL}}", raw_url)
                .replace("{{BLOB_URL}}", blob_url)
                .replace("{{LAST_UPDATED}}", date_str)
                .replace("<!-- AUTO-GENERATED: post-body -->", html_body)
            )

            output_path = os.path.join(category_dir, filename.replace(".md", ".html"))
            write_file(output_path, post_html)
            print(f"📝 已生成文章頁：{output_path}")

if __name__ == "__main__":
    build_site()
