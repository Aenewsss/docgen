import firebase_admin
from firebase_admin import credentials, db
import os
import json
import tempfile

# URL do seu Realtime Database
DATABASE_URL = os.getenv("FIREBASE_DATABASE_URL", "https://SEU-PROJETO.firebaseio.com")

# String bruta do JSON
FIREBASE_CREDENTIAL_JSON = os.getenv("FIREBASE_CREDENTIAL_JSON")

if not firebase_admin._apps:
    if not FIREBASE_CREDENTIAL_JSON:
        raise ValueError("FIREBASE_CREDENTIAL_JSON não foi definido no ambiente")

    try:
        # Sanitize manual: substitui quebras reais de linha por escape
        sanitized_json_str = FIREBASE_CREDENTIAL_JSON.replace('\n', '\\n')

        # Agora sim faz o parse
        parsed_cred = json.loads(sanitized_json_str)

        # Cria um arquivo temporário com o conteúdo válido
        with tempfile.NamedTemporaryFile(mode="w+", delete=False, suffix=".json") as tmp_file:
            json.dump(parsed_cred, tmp_file)
            tmp_file.flush()
            cred = credentials.Certificate(tmp_file.name)

        firebase_admin.initialize_app(cred, {"databaseURL": DATABASE_URL})

    except json.JSONDecodeError as e:
        raise ValueError(f"Erro ao decodificar FIREBASE_CREDENTIAL_JSON: {e}")