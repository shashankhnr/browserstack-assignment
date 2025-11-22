import json
import requests
from pathlib import Path
import urllib.parse

ROOT = Path(__file__).resolve().parents[1]
SUMMARY = ROOT / "output" / "summary.json"
TRANS_OUT = ROOT / "output" / "translations.json"

def translate_text(text):
    try:
        encoded = urllib.parse.quote(text)
        url = f"https://api.mymemory.translated.net/get?q={encoded}&langpair=es|en"
        r = requests.get(url, timeout=20)

        data = r.json()
        return data["responseData"]["translatedText"]
    except Exception as e:
        print("Translation error:", e)
        print("Raw:", r.text[:200])
        return ""

def main():
    if not SUMMARY.exists():
        print("Run scraper.py first.")
        return

    items = json.loads(SUMMARY.read_text(encoding="utf-8"))
    results = []

    for item in items:
        spanish = item["title"]
        print(f"\nTranslating: {spanish}")

        english = translate_text(spanish)

        print("Translated:", english)

        results.append({
            "folder": item["folder"],
            "original": spanish,
            "translated": english
        })

    TRANS_OUT.write_text(json.dumps(results, indent=2, ensure_ascii=False))
    print(f"\nSaved translations to {TRANS_OUT}")

if __name__ == "__main__":
    main()
