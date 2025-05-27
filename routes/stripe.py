from fastapi import APIRouter, Request, HTTPException
from pydantic import BaseModel
import os
import stripe
from utils.update_user_after_checkout import update_user_after_checkout
from utils.update_user_after_checkout_credits import update_user_after_checkout_credits
from dotenv import load_dotenv

load_dotenv()

router = APIRouter()

stripe.api_key = os.getenv("STRIPE_SECRET_KEY")
STRIPE_WEBHOOK_SECRET = os.getenv("STRIPE_WEBHOOK_SECRET")

# Preços cadastrados na Stripe
PRICE_MAP = {
    "starter:monthly": os.getenv("PRICE_STARTER_MONTHLY_ID"),
    "starter:annual": os.getenv("PRICE_STARTER_ANNUAL_ID"),
    "pro:monthly": os.getenv("PRICE_PRO_MONTHLY_ID"),
    "pro:annual": os.getenv("PRICE_PRO_ANNUAL_ID"),
    "enterprise:monthly": os.getenv("PRICE_ENTERPRISE_MONTHLY_ID"),
    "enterprise:annual": os.getenv("PRICE_ENTERPRISE_ANNUAL_ID"),
}


class CheckoutSessionInput(BaseModel):
    email: str
    user_id: str
    plan: str  # "starter", "pro", "enterprise"
    billing_cycle: str  # "monthly" ou "annual"


@router.post("/create-checkout-session")
async def create_checkout_session(data: CheckoutSessionInput):
    print("Endpoint called", data)
    try:
        price_id = PRICE_MAP.get(f"{data.plan}:{data.billing_cycle}")
        print("Price id:", price_id)
        if not price_id:
            raise HTTPException(status_code=400, detail="Plano inválido")

        session = stripe.checkout.Session.create(
            payment_method_types=["card"],
            mode="subscription",
            line_items=[
                {
                    "price": price_id,
                    "quantity": 1,
                }
            ],
            customer_email=data.email,
            metadata={
                "user_id": data.user_id,
                "plan": data.plan,
                "billing_cycle": data.billing_cycle,
            },
            success_url=os.getenv("FRONT_URL_CHECKOUT"),
            cancel_url=os.getenv("FRONT_URL_CHECKOUT") + "/pricing",
        )

        return {"checkout_url": session.url}

    except Exception as e:
        print(str(e))
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/webhook")
async def stripe_webhook(request: Request):
    print(os.getenv("STRIPE_WEBHOOK_SECRET"), os.getenv("STRIPE_SECRET_KEY"))
    payload = await request.body()
    sig_header = request.headers.get("stripe-signature")

    if not sig_header:
        raise HTTPException(status_code=400, detail="Header stripe-signature ausente")

    try:
        event = stripe.Webhook.construct_event(
            payload=payload, sig_header=sig_header, secret=STRIPE_WEBHOOK_SECRET
        )
    except ValueError:
        raise HTTPException(status_code=400, detail="Payload inválido")
    except stripe.error.SignatureVerificationError:
        raise HTTPException(status_code=400, detail="Assinatura inválida")

    print("📦 Evento recebido:", event["type"])

    if event["type"] == "checkout.session.completed":
        session = event["data"]["object"]
        print("session:", session)

        # Verifica se se trata de compra avulsa (payment em vez de subscription)
        if session.get("mode") == "payment" and "credits" in session.get("metadata", {}):
            customer_email = session.get("customer_details", {}).get("email")
            user_id = session.get("metadata", {}).get("user_id")
            credits = session.get("metadata", {}).get("credits")

            print(f"\n✅ Compra avulsa confirmada para {customer_email}")
            print(f"🎯 Créditos comprados: {credits}, UID: {user_id}")

            update_user_after_checkout_credits(user_id, credits)

        else:
            customer_email = session.get("customer_details", {}).get("email")
            plan = session.get("metadata", {}).get("plan")
            billing_cycle = session.get("metadata", {}).get("billing_cycle")
            user_id = session.get("metadata", {}).get("user_id")

            print(f"\n✅ Pagamento confirmado para {customer_email}")
            print(f"📋 Plano: {plan}, Ciclo: {billing_cycle}, UID: {user_id}")

            update_user_after_checkout(user_id, plan, billing_cycle)

    return {"status": "success"}

class CreditCheckoutSessionInput(BaseModel):
    email: str
    user_id: str
    credits: str


@router.post("/create-credits-checkout-session")
async def create_credits_checkout_session(data: CreditCheckoutSessionInput):
    print(os.getenv("FRONT_URL_CHECKOUT"))
    try:
        # Cria uma sessão de checkout para créditos avulsos
        session = stripe.checkout.Session.create(
            payment_method_types=["card"],
            mode="payment",
            line_items=[
                {
                    "price_data": {
                        "currency": "brl",
                        "product_data": {
                            "name": f"{data.credits} créditos avulsos",
                        },
                        "unit_amount": int(int(data.credits) * 0.05),  # 0,0005 por crédito (em centavos)
                    },
                    "quantity": 1,
                }
            ],
            customer_email=data.email,
            metadata={
                "user_id": data.user_id,
                "credits": data.credits,
            },
            success_url=os.getenv("FRONT_URL_CHECKOUT"),
            cancel_url=os.getenv("FRONT_URL_CHECKOUT") + "/meu-plano",
        )

        return {"checkout_url": session.url}

    except Exception as e:
        print(str(e))
        raise HTTPException(status_code=500, detail=str(e))