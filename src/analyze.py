# analyze.py
import json, re
from pathlib import Path
from collections import Counter

ROOT = Path(__file__).resolve().parents[1]
TRANS_FILE = ROOT / "output" / "translations.json"

def tokenize(text):
    t = text.lower()
    t = re.sub(r"[^a-z0-9\s]", " ", t)
    return [w for w in t.split() if len(w) > 1]

def main():
    if not TRANS_FILE.exists():
        print("Run translate.py first.")
        return

    # FIX: ignore bad unicode characters
    raw = TRANS_FILE.read_text(encoding="utf-8", errors="replace")

    data = json.loads(raw)

    words = []
    for item in data:
        words += tokenize(item.get("translated", ""))

    counts = Counter(words)
    repeated = {w: c for w, c in counts.items() if c > 2}

    if repeated:
        print("Words repeated more than twice:")
        for w, c in sorted(repeated.items(), key=lambda x: -x[1]):
            print(f"{w} -> {c}")
    else:
        print("No words repeated more than twice.")

    print("\nTop 20 words:")
    for w, c in counts.most_common(20):
        print(f"{w} -> {c}")

if __name__ == "__main__":
    main()
