from firebase.firebase_admin_init import db

def toggle_repo_loading(user_id: str, repo_name: str, message: str, error: bool = False):
    user_ref = db.reference(f"users/{user_id}")
    current_data = user_ref.get()

    if not current_data:
        print("Usuário não encontrado no Firebase.")
        return

    current_loading_state = current_data.get("repo_loading", False)

    new_state = not current_loading_state

    update_payload = {
        "repo_loading": new_state,
        "repo_message": message,
        "repo_error": error
    }

    if new_state:  # só atualiza o nome se for iniciar carregamento
        update_payload["repo_name"] = repo_name

    try:
        user_ref.update(update_payload)
        print(f"repo_loading set to {new_state} para o usuário {user_id}")
    except Exception as e:
        print(f"Erro ao atualizar repo_loading: {e}")