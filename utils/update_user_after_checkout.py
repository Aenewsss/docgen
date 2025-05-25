from firebase.firebase_admin_init import db

def update_user_after_checkout(user_id: str, plan: str, billing_cycle: str):
    credits = {
        "starter": 70000,
        "pro": 350000,
        "enterprise": 1050000
    }
    
    try:
        user_ref = db.reference(f"users/{user_id}")
        user_ref.update(
                {"plan": plan, "billingCycle": billing_cycle, "modalCongratsShowed": False,
                 "isTrial": False, "trialDateEnd": None, 
                 "credits": credits[plan] + 30000}
        )
        print("✅ Firebase atualizado com sucesso.")
    except Exception as firebase_error:
        print("❌ Erro ao atualizar o Firebase:", str(firebase_error))
