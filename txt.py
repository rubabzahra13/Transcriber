# json_to_txt.py

import json
import os
import glob

for json_file in glob.glob("*.json"):
    base = os.path.splitext(json_file)[0]
    txt_file = base + ".txt"

    # ✅ Skip if .txt already exists
    if os.path.exists(txt_file):
        print(f"[→] Skipping {json_file} — transcript already exists.")
        continue

    try:
        with open(json_file, "r", encoding="utf-8") as f:
            data = json.load(f)
            lines = data["captions"][0]["hash"]["lines"]
    except (KeyError, IndexError, json.JSONDecodeError):
        print(f"[ERROR] Skipping {json_file} — invalid structure.")
        continue

    with open(txt_file, "w", encoding="utf-8") as f:
        for line in lines:
            f.write(" ".join(line["text"]).strip() + "\n")

    print(f"[✓] {json_file} → {txt_file}")
