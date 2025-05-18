from firebase.firebase_admin_init import db
import re

def sanitize_path(path: str) -> str:
    # Substitui todos os caracteres inválidos por "_"
    return re.sub(r'[.#$/\[\]]', '_', path)

def set_file_tokens_analysis(user_id: str, file_path:str, prompt_tokens: int, completion_tokens: int, total_tokens: int):
    sanitized_path = sanitize_path(file_path)
    file_ref = db.reference(f"files_analysis/{user_id}/{sanitized_path}")

    file_ref.set({
        "prompt_tokens":prompt_tokens,
        "completion_tokens":completion_tokens,
        "total_tokens":total_tokens,
    })