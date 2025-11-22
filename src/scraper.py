# scraper.py
# Reads the article folders in ../articles, parses Title/Author/Date/Full Article Text,
# and writes a summary JSON and per-article text copies into ../output/

import os, json, re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]  # C:\selenium_assignment
ARTICLES_DIR = ROOT / "articles"
OUTPUT_DIR = ROOT / "output"
OUTPUT_DIR.mkdir(exist_ok=True)

def parse_article_txt(txt_path: Path):
    text = txt_path.read_text(encoding="utf-8").strip()
    # Expect format with metadata lines like:
    # Title: ...
    # Author: ...
    # Date: ...
    # (blank)
    # Full Article Text:
    # <paragraphs...>
    lines = text.splitlines()
    meta = {"title":"", "author":"", "date":"", "body":""}
    # find metadata lines
    for i, ln in enumerate(lines[:10]):  # metadata in first few lines
        if ln.lower().startswith("title:"):
            meta["title"] = ln.split(":",1)[1].strip()
        elif ln.lower().startswith("author:"):
            meta["author"] = ln.split(":",1)[1].strip()
        elif ln.lower().startswith("date:"):
            meta["date"] = ln.split(":",1)[1].strip()
    # find where "Full Article Text:" appears
    body_start = 0
    for i, ln in enumerate(lines):
        if ln.strip().lower().startswith("full article text"):
            body_start = i + 1
            break
    # body is everything after body_start
    meta["body"] = "\n".join(lines[body_start:]).strip()
    return meta

def main():
    summary = []
    if not ARTICLES_DIR.exists():
        print("No articles folder found at", ARTICLES_DIR)
        return
    for folder in sorted(ARTICLES_DIR.iterdir()):
        if not folder.is_dir():
            continue
        # find first .txt file in the folder
        txt_files = list(folder.glob("*.txt"))
        if not txt_files:
            print(f"[WARN] No txt file in {folder.name}")
            continue
        txt_path = txt_files[0]
        parsed = parse_article_txt(txt_path)
        parsed["folder"] = folder.name
        parsed["txt_file"] = str(txt_path)
        # find an image (any common extension)
        img = None
        for ext in ("*.jpg","*.jpeg","*.png","*.avif","*.webp"):
            found = list(folder.glob(ext))
            if found:
                img = str(found[0])
                break
        parsed["image_file"] = img
        summary.append(parsed)
        # also save a copy of the full body into output/article_<n>.txt
        safe_name = folder.name.replace(" ", "_")
        out_folder = OUTPUT_DIR / safe_name
        out_folder.mkdir(exist_ok=True)
        (out_folder / f"{safe_name}.txt").write_text(
            f"Title: {parsed['title']}\nAuthor: {parsed['author']}\nDate: {parsed['date']}\n\n{parsed['body']}",
            encoding="utf-8"
        )
        if img:
            # copy image path string to a small metadata file (we won't copy binary)
            (out_folder / "image_path.txt").write_text(str(img), encoding="utf-8")
        print(f"[OK] Parsed {folder.name}")

    # write summary.json
    (OUTPUT_DIR / "summary.json").write_text(json.dumps(summary, ensure_ascii=False, indent=2), encoding="utf-8")
    print("Saved summary to", OUTPUT_DIR / "summary.json")

if __name__ == "__main__":
    main()
