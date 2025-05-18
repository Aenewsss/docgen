from firebase.firebase_admin_init import db


def update_user_credits(user_id: str, tokens_used: int):
    user_ref = db.reference(f"users/{user_id}")
    current_data = user_ref.get()

    if not current_data:
        print("Usuário não encontrado no Firebase.")
        return

    current_credits = current_data.get("credits", 0)
    updated_credits = current_credits - tokens_used

    user_ref.update({"credits": updated_credits})

    print(
        f"Usuário {user_id} usou {tokens_used} tokens. Créditos restantes: {updated_credits}"
    )
    if updated_credits < 0:
        return False

    return True
