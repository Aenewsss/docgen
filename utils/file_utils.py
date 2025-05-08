import os

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
    ".json"
]


def collect_code_files(directory: str):
    """
    Percorre recursivamente a pasta extraída e retorna uma lista de arquivos de código com seu conteúdo.
    """
    collected_files = []

    for root, _, files in os.walk(directory):
        for file in files:
            ext = os.path.splitext(file)[1]
            if ext not in UNSUPPORTED_EXTENSIONS and ext != "":
                file_path = os.path.join(root, file)
                try:
                    with open(file_path, "r", encoding="utf-8") as f:
                        content = f.read()

                    characters = len(content.strip())

                    collected_files.append(
                        {
                            "path": file_path,
                            "extension": ext,
                            "characters": characters,
                            "amount_tokens_approximately": characters / 4,
                            "content": content,
                        }
                    )
                except Exception as e:
                    print(f"Erro ao ler {file_path}: {e}")

    return collected_files
