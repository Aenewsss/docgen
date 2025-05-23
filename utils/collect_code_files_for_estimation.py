import os
import shutil

UNSUPPORTED_EXTENSIONS = [
    ".txt",
    ".bin",
    ".gltf",
    ".png",
    ".jpeg",
    ".jpg",
    ".webp",
    ".svg",
    ".lock",
    ".ico",
    ".mjs",
    ".md",
    ".json",
    ".git",
    ".gitignore",
    ".yaml",
    ".css"
]

def is_valid_file(filename):
    _, ext = os.path.splitext(filename)
    return ext.lower() not in UNSUPPORTED_EXTENSIONS

def collect_code_files_for_estimation(base_path):
    collected = []
    for root, _, files in os.walk(base_path):
        for file in files:
            if is_valid_file(file):
                file_path = os.path.join(root, file)
                try:
                    with open(file_path, "r", encoding="utf-8") as f:
                        content = f.read()
                        char_count = len(content)
                        token_estimate = round(char_count / 4)
                        collected.append({
                            "path": file_path,
                            "chars": char_count,
                            "estimated_tokens": token_estimate + 1000
                        })
                except Exception:
                    continue
    if os.path.exists(base_path):
        shutil.rmtree(base_path)
    return collected