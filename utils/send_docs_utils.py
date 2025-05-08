import requests
import json
import os
from dotenv import load_dotenv

load_dotenv()

WEBHOOK_URL = os.getenv("WEBHOOK_URL")

def send_to_n8n_webhook(filename: str, content: str):
    """
    Envia a resposta da IA para um webhook do n8n.

    :param filename: Nome do arquivo a ser criado
    :param content: Texto da documentação gerado pela IA
    """
    try:
        payload = {"filename": filename, "content": content}
        headers = {"Content-Type": "application/json"}

        response = requests.post(WEBHOOK_URL, data=json.dumps(payload), headers=headers)
        response.raise_for_status()
        print(f"✅ Enviado com sucesso: {filename}")
        return True
    except requests.exceptions.RequestException as e:
        print(f"❌ Erro ao enviar para o n8n: {e}")
        return False
