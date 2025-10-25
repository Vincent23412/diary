#!/usr/bin/env python3
import os
import datetime

# === 路徑設定 ===
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CONTENT_DIR = os.path.join(BASE_DIR, "content")
SITE_DIR = os.path.join(BASE_DIR, "site")
NOTES_DIR = os.path.join(SITE_DIR, "notes")
TEMPLATE_PATH = os.path.join(NOTES_DIR, "_category.template.html")
NOTES_INDEX_PATH = os.path.join(NOTES_DIR, "index.html")
HOME_PATH = os.path.join(SITE_DIR, "index.html")

# === 基本工具 ===
def read_file(path):
    with open(path, "r", encoding="utf-8") as f:
        return f.read()

def write_file(path, content):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        f.write(content)

def get_categories(content_dir):
    """
    掃描 content 下的所有第一層資料夾，回傳 {category: [markdown files]}
    """
    categories = {}
    for category in os.listdir(content_dir):
        cat_path = os.path.join(content_dir, category)
        if not os.path.isdir(cat_path):
            continue
        md_files = [f for f in os.listdir(cat_path) if f.endswith(".md")]
        if md_files:
            categories[category] = sorted(md_files)
    return categories

# === 主程式 ===
def build_site():
    print("🚀 開始生成靜態網站...")
    if not os.path.exists(CONTENT_DIR):
        print(f"❌ 找不到 content 資料夾: {CONTENT_DIR}")
        return

    categories = get_categories(CONTENT_DIR)
    print(f"🔍 找到 {len(categories)} 個分類: {', '.join(categories.keys())}")

    if not categories:
        print("⚠️ 沒有找到任何分類資料夾。")
        return

    if not os.path.exists(TEMPLATE_PATH):
        print(f"❌ 找不到模板檔案: {TEMPLATE_PATH}")
        return

    template = read_file(TEMPLATE_PATH)
    date_str = datetime.date.today().isoformat()

    category_tiles = ""

    # === 依每個分類生成 HTML 頁 ===
    for category, files in categories.items():
        category_name = category.replace("_", " ").title()

        post_items = ""
        for filename in files:
            title = filename.replace(".md", "").replace("_", " ").title()
            raw_url = f"https://raw.githubusercontent.com/<你的使用者>/<你的repo>/main/content/{category}/{filename}"
            blob_url = f"https://github.com/<你的使用者>/<你的repo>/blob/main/content/{category}/{filename}"

            post_items += f"""
<li class="post-item">
  <a class="post-link" href="{blob_url}" target="_blank">{title}</a>
  <span class="post-meta">
    原文：<a href="{raw_url}" target="_blank" rel="noopener">raw</a>
  </span>
</li>
"""

        html = (
            template.replace("{{CATEGORY_NAME}}", category_name)
                    .replace("{{CATEGORY_SLUG}}", category)
                    .replace("<!-- AUTO-GENERATED: posts -->", post_items)
                    .replace("<!-- AUTO-GENERATED: last-updated -->", date_str)
        )

        output_path = os.path.join(NOTES_DIR, category, "index.html")
        write_file(output_path, html)
        print(f"✅ 已生成 {output_path}")

        category_tiles += f"""
<a class="tile" href="/notes/{category}/index.html">
  <div class="tile-title">{category_name}</div>
  <div class="tile-meta">{len(files)} 篇文章</div>
</a>
"""

    # === 更新 notes/index.html（分類總覽） ===
    if os.path.exists(NOTES_INDEX_PATH):
        notes_index_html = read_file(NOTES_INDEX_PATH)
        notes_index_html = (
            notes_index_html.replace("<!-- AUTO-GENERATED: categories -->", category_tiles)
                            .replace("<!-- AUTO-GENERATED: last-updated -->", date_str)
        )
        write_file(NOTES_INDEX_PATH, notes_index_html)
        print("✅ 已更新 notes/index.html")
    else:
        print(f"⚠️ 找不到 notes/index.html（略過）")

    # === 更新首頁的分類區 ===
    if os.path.exists(HOME_PATH):
        home_html = read_file(HOME_PATH)
        home_html = home_html.replace("<!-- AUTO-GENERATED: categories-mini -->", category_tiles)
        write_file(HOME_PATH, home_html)
        print("✅ 已更新首頁 index.html")
    else:
        print(f"⚠️ 找不到首頁 index.html（略過）")

    print("🎉 所有分類頁與索引已生成完成！")

if __name__ == "__main__":
    build_site()
