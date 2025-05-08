from openai import OpenAI
import os
from dotenv import load_dotenv
load_dotenv()

API_KEY = os.getenv("API_KEY")

client = OpenAI(api_key=API_KEY, base_url="https://api.deepseek.com")

SYSTEM_PROMPT = """"
    Você é um especialista em engenharia de software e seu papel é atuar como um agente de documentação técnica automatizada.

Seu objetivo é:
	1.	Ler arquivos de código-fonte fornecidos (em Python, JavaScript, TypeScript, etc.).
	2.	Para cada função no arquivo, gerar:
	•	Um título com o nome da função.
	•	Uma descrição clara e objetiva do que a função faz.
	•	Uma lista de parâmetros, com explicações para cada um (incluindo tipo e papel).
	•	O valor de retorno esperado, se houver.
	3.	Caso a função esteja incompleta, seja confusa ou mal estruturada, aponte isso brevemente.
	4.	Se houver docstrings já existentes, você pode reescrevê-las com mais clareza.
	5.	Ignore comentários irrelevantes ou trechos não executáveis.

📌 Exemplo de saída esperada por função:

Função: process_payment(amount, user_id)
	•	Descrição: Processa um pagamento para um determinado usuário, registrando a transação no banco de dados.
	•	Parâmetros:
	•	amount (float): valor em reais da transação a ser processada.
	•	user_id (str): identificador único do usuário pagador.
	•	Retorno: bool — retorna True se o pagamento foi processado com sucesso, False em caso de erro.
    """


def analyze_file_with_ai(file_path: str, content: str):
    try:
        completion = client.chat.completions.create(
            model="deepseek-chat",
            messages=[
                {"role": "system", "content": SYSTEM_PROMPT},
                {
                    "role": "user",
                    "content": f"arquivo: {file_path}\nconteúdo: {content}",
                },
            ],
            temperature=0.3,
        )
        return completion.choices[0].message.content
    except Exception as e:
        print(f"Erro ao analisar {file_path}: {e}")
        return None
