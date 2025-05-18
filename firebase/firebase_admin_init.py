import firebase_admin
from firebase_admin import credentials, db
import os
import json
import tempfile

# URL do seu Realtime Database (mantém como estava)
DATABASE_URL = os.getenv("FIREBASE_DATABASE_URL", "https://SEU-PROJETO.firebaseio.com")

# Pega o conteúdo do JSON como string do .env
FIREBASE_CREDENTIAL_JSON = os.getenv("FIREBASE_CREDENTIAL_JSON")

# Inicializa o app se ainda não estiver iniciado
if not firebase_admin._apps:
    if not FIREBASE_CREDENTIAL_JSON:
        raise ValueError("FIREBASE_CREDENTIAL_JSON não foi definido no ambiente")

    # Converte a string para dicionário Python
    parsed_cred = json.loads(FIREBASE_CREDENTIAL_JSON)

    # Cria um arquivo temporário para passar ao SDK
    with tempfile.NamedTemporaryFile(
        mode="w+", delete=False, suffix=".json"
    ) as tmp_file:
        json.dump(parsed_cred, tmp_file)
        tmp_file.flush()
        cred = credentials.Certificate(tmp_file.name)

    # Inicializa o Firebase
    firebase_admin.initialize_app(cred, {"databaseURL": DATABASE_URL})
