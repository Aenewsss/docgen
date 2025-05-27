from firebase.firebase_admin_init import db

def update_user_after_checkout_credits(user_id: str, credits: str):
    try:
        user_ref = db.reference(f"users/{user_id}")
        current_data = user_ref.get()
        current_credits = current_data.get("credits", 0) if current_data else 0
        updated_credits = current_credits + int(credits)

        user_ref.update(
            {
                "credits": updated_credits,
                "showModalCongratsCredits": int(credits),
            }
        )
        print("✅ Firebase atualizado com sucesso.")
    except Exception as firebase_error:
        print("❌ Erro ao atualizar o Firebase:", str(firebase_error))