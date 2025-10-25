#!/usr/bin/env python3
import os
import datetime

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))  # 回到專案根目錄

CONTENT_DIR = os.path.join(BASE_DIR, "content")
SITE_DIR = os.path.join(BASE_DIR, "site")
NOTES_DIR = os.path.join(SITE_DIR, "notes")
TEMPLATE_PATH = os.path.join(NOTES_DIR, "_category.template.html")
NOTES_INDEX_PATH = os.path.join(NOTES_DIR, "index.html")
HOME_PATH = os.path.join(SITE_DIR, "index.html")

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

    print(categories.items())

    # === 生成每個分類的 HTML 頁 ===
    POST_TEMPLATE_PATH = os.path.join(NOTES_DIR, "_post.template.html")

    for category, files in categories.items():
        category_name = category.replace("_", " ").title()
        category_dir = os.path.join(NOTES_DIR, category)
        os.makedirs(category_dir, exist_ok=True)

        # === 分類總覽 index.html ===
        category_index = os.path.join(category_dir, "index.html")

        # 讀取已存在的分類頁，或使用模板新建
        if os.path.exists(category_index):
            html = read_file(category_index)
            print(f"🧩 已存在 {category_index}，將更新條目列表。")
        else:
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
        html = html.replace("<!-- AUTO-GENERATED: posts -->", post_items)
        html = html.replace("<!-- AUTO-GENERATED: last-updated -->", date_str)
        write_file(category_index, html)
        print(f"✅ 更新/建立 {category_index}")

        # === 為每篇文章建立 HTML ===
        post_template = read_file(POST_TEMPLATE_PATH)
        for filename in files:
            title = filename.replace(".md", "").replace("_", " ").title()
            md_path = os.path.join(CONTENT_DIR, category, filename)
            raw_url = f"https://raw.githubusercontent.com/Vincent23412/diary/main/content/{category}/{filename}"
            blob_url = f"https://github.com/Vincent23412/diary/blob/main/content/{category}/{filename}"

            # 讀 Markdown 內容
            with open(md_path, "r", encoding="utf-8") as f:
                md_content = f.read()

            # 插入模板
            post_html = (
                post_template
                .replace("{{POST_TITLE}}", title)
                .replace("{{CATEGORY_SLUG}}", category)
                .replace("{{RAW_URL}}", raw_url)
                .replace("{{BLOB_URL}}", blob_url)
                .replace("{{LAST_UPDATED}}", date_str)
                .replace("<!-- AUTO-GENERATED: post-body -->", f"<pre>{md_content}</pre>")
            )

            output_path = os.path.join(category_dir, filename.replace(".md", ".html"))
            write_file(output_path, post_html)
            print(f"📝 已生成文章頁：{output_path}")


if __name__ == "__main__":
    build_site()
