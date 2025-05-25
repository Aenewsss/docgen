# Aenewsss_docgen - Documentação Viva

O projeto **Aenewsss_docgen** é uma plataforma de geração de documentação automatizada para projetos de software, utilizando inteligência artificial para analisar código-fonte e gerar documentação técnica. Ele integra-se com o GitHub para baixar repositórios, processar arquivos e enviar a documentação gerada para um webhook do n8n, além de gerenciar créditos de usuários via Firebase.

---

## 🚀 Funcionalidades Principais

### 📂 Processamento de Código
- **Análise de Arquivos**: Extrai e analisa arquivos de código de um diretório, ignorando extensões não suportadas.
- **Estimativa de Tokens**: Calcula estatísticas básicas como contagem de caracteres e estimativa de tokens para processamento.
- **Documentação por IA**: Utiliza o modelo Deepseek Chat para gerar documentação técnica com base no código analisado.

### 🔄 Integrações Externas
- **GitHub**: Baixa repositórios, lista projetos e autentica via OAuth.
- **Firebase**: Armazena e gerencia créditos/tokens de usuários, garantindo consistência nas operações de débito.
- **n8n**: Envia documentação gerada para um webhook com metadados do arquivo e informações do usuário.

### 🔒 Autenticação e Gerenciamento
- **Controle de Créditos**: Atualiza e verifica o saldo de créditos/tokens dos usuários no Firebase.
- **Métricas de Uso**: Armazena métricas de uso de tokens associadas a usuários e arquivos.

---

## 📁 Arquivos Principais

| Arquivo | Descrição |
|---------|-----------|
| `main.py` | Configura e inicia um servidor FastAPI para o backend da "Documentação Viva" com rota raiz e integração de rotas do GitHub. |
| `ai_utils.py` | Analisa o conteúdo de arquivos usando o modelo Deepseek Chat e retorna a resposta da IA com métricas de uso de tokens. |
| `send_docs_utils.py` | Envia documentação gerada por IA para um webhook do n8n com metadados do arquivo e informações do usuário. |
| `update_user_credits.py` | Atualiza e verifica o saldo de créditos/tokens de um usuário no Firebase. |
| `file_metadata.py` | Coleta e processa metadados de arquivos de código em um diretório, ignorando extensões não suportadas. |
| `set_file_tokens_analysis.py` | Processa e armazena métricas de uso de tokens em arquivos, associando-os a usuários no Firebase. |
| `collect_files.py` | Coleta arquivos de código válidos de um diretório e seus subdiretórios, calculando estatísticas básicas. |
| `firebase_admin_init.py` | Inicializa e configura o SDK do Firebase Admin para conexão com o Realtime Database. |
| `github.py` | Gerencia integração com GitHub para estimativa de tokens, download de repositórios e autenticação OAuth. |

---

## 🛠️ Instalação e Execução

### Pré-requisitos
- Python 3.8+
- Conta no Firebase com Realtime Database configurado.
- Token de acesso à API do GitHub.
- URL do webhook do n8n (opcional).

### Passos para Configuração
1. Clone o repositório:
   ```bash
   git clone https://github.com/seu-usuario/Aenewsss_docgen.git
   cd Aenewsss_docgen
   ```

2. Instale as dependências:
   ```bash
   pip install -r requirements.txt
   ```

3. Configure as variáveis de ambiente:
   - `FIREBASE_CREDENTIAL_JSON`: Credenciais do Firebase em formato JSON.
   - `FIREBASE_DATABASE_URL`: URL do Realtime Database.
   - `GITHUB_TOKEN`: Token de autenticação do GitHub.
   - `N8N_WEBHOOK_URL`: URL do webhook do n8n (opcional).

4. Execute o servidor FastAPI:
   ```bash
   uvicorn main:app --reload
   ```

---

## 🔗 Dependências Externas
- **Firebase**: Para armazenamento de créditos e métricas de usuários.
- **GitHub API**: Para integração com repositórios e autenticação OAuth.
- **n8n**: Para automação e envio de documentação gerada.

---

## 📜 Licença
Este projeto está licenciado sob a licença MIT. Consulte o arquivo `LICENSE` para mais detalhes.

---

## 🤝 Contribuição
Contribuições são bem-vindas! Sinta-se à vontade para abrir issues ou enviar pull requests.