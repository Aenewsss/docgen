from openai import OpenAI
import os
from dotenv import load_dotenv

load_dotenv()

API_KEY = os.getenv("API_KEY")

client = OpenAI(api_key=API_KEY, base_url="https://api.deepseek.com")

SYSTEM_PROMPT = """"
Você é um especialista em engenharia de software e seu papel é atuar como um agente de documentação técnica automatizada.

Sua tarefa é:
1. Ler arquivos de código-fonte fornecidos (em Python, JavaScript, TypeScript, etc.).
2. Para cada arquivo, retorne:
   - 📁 Nome do arquivo analisado
   - 🔍 Linguagem de programação (com base na extensão do arquivo)
   - 📦 Bibliotecas ou frameworks detectados no conteúdo (por exemplo: React, Express, Firebase)
3. Em seguida, para cada função no arquivo, gere:
   - Um título com o nome da função.
   - Uma descrição clara e objetiva do que a função faz.
   - Uma lista de parâmetros, com explicações para cada um (incluindo tipo e papel).
   - O valor de retorno esperado, se houver.

Caso a função esteja incompleta, seja confusa ou mal estruturada, aponte isso brevemente.  
Se houver docstrings já existentes, você pode reescrevê-las com mais clareza.  
Ignore comentários irrelevantes ou trechos não executáveis.

📌 Exemplo de saída:
📁 Arquivo: src/controllers/userController.js  
🔍 Linguagem: JavaScript  
📦 Bibliotecas: Express, Mongoose

---
Função: getUserById(id)
Descrição: Retorna o usuário correspondente ao ID fornecido, consultando o banco MongoDB.
Parâmetros: id (string) — identificador único do usuário.
Retorno: objeto do usuário ou null.
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

        ai_content = completion.choices[0].message.content
        total_tokens = completion.usage.total_tokens

        # Tokens de entrada (prompt do usuário + sistema)
        prompt_tokens = completion.usage.prompt_tokens

        # Tokens gerados pela IA na resposta
        completion_tokens = completion.usage.completion_tokens

        return {
            "content": ai_content,
            "tokens_used": total_tokens,
            "prompt_tokens": prompt_tokens,
            "completion_tokens": completion_tokens,
        }
    except Exception as e:
        print(f"Erro ao analisar {file_path}: {e}")
        return {
            "content": None,
            "tokens_used": 0,
            "prompt_tokens": 0,
            "completion_tokens": 0  ,
        }
