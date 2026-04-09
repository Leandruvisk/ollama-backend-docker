# Chat com Ollama

Aplicação de chat com IA rodando localmente via [Ollama](https://ollama.com), com backend em FastAPI, frontend em Streamlit e banco de dados PostgreSQL — tudo orquestrado com Docker.

---

## Arquitetura

```
┌─────────────┐      ┌─────────────┐      ┌─────────────┐
│  Frontend   │ ───► │   Backend   │ ───► │   Ollama    │
│  Streamlit  │      │   FastAPI   │      │  (LLM local)│
│  :8501      │      │   :8000     │      │   :11434    │
└─────────────┘      └──────┬──────┘      └─────────────┘
                            │
                     ┌──────▼──────┐
                     │  PostgreSQL │
                     │    :5432    │
                     └─────────────┘
```

| Serviço    | Tecnologia  | Porta |
|------------|-------------|-------|
| Frontend   | Streamlit   | 8501  |
| Backend    | FastAPI     | 8000  |
| LLM        | Ollama      | 11434 |
| Banco      | PostgreSQL  | 5432  |

---

## Pré-requisitos

- [Docker Desktop](https://www.docker.com/products/docker-desktop/) instalado e rodando
- [Git](https://git-scm.com/)

---

## Como rodar

### 1. Clone o repositório

```bash
git clone <url-do-repositorio>
cd ollama-backend-docker
```

### 2. Suba os containers

#### Sem GPU (CPU — funciona em qualquer máquina)

```bash
docker compose up --build
```

#### Com GPU NVIDIA

Antes, instale o NVIDIA Container Toolkit:

```bash
# No WSL2 ou Linux
curl -fsSL https://nvidia.github.io/libnvidia-container/gpgkey \
  | sudo gpg --dearmor -o /usr/share/keyrings/nvidia-container-toolkit-keyring.gpg

curl -s -L https://nvidia.github.io/libnvidia-container/stable/deb/nvidia-container-toolkit.list \
  | sed 's#deb https://#deb [signed-by=/usr/share/keyrings/nvidia-container-toolkit-keyring.gpg] https://#g' \
  | sudo tee /etc/apt/sources.list.d/nvidia-container-toolkit.list

sudo apt-get update && sudo apt-get install -y nvidia-container-toolkit
sudo nvidia-ctk runtime configure --runtime=docker
sudo systemctl restart docker
```

Depois, edite o `docker-compose.yml` e adicione no serviço `ollama`:

```yaml
ollama:
  ...
  deploy:
    resources:
      reservations:
        devices:
          - capabilities: [gpu]
  runtime: nvidia
```

E suba normalmente:

```bash
docker compose up --build
```

### 3. Baixe o modelo de IA

Com os containers rodando, execute:

```bash
docker exec -it ollama ollama pull llama3
```

> Isso baixa o modelo `llama3` (~4GB). Só precisa fazer uma vez.

### 4. Acesse a aplicação

| URL | Descrição |
|-----|-----------|
| `http://localhost:8501` | Interface de chat |
| `http://localhost:8000/docs` | Documentação da API |

---

## API — Endpoints

### `POST /chat`

Envia uma mensagem e recebe a resposta da IA.

**Body:**
```json
{
  "message": "Olá, como você pode me ajudar?",
  "model": "llama3",
  "session_id": "usuario-123"
}
```

**Resposta:**
```json
{
  "response": "Olá! Posso ajudar com..."
}
```

### `DELETE /chat/{session_id}`

Apaga o histórico de uma sessão.

```bash
curl -X DELETE http://localhost:8000/chat/usuario-123
```

---

## Estrutura do projeto

```
ollama-backend-docker/
├── backend/
│   ├── app.py                  # Entrada da API (FastAPI)
│   ├── config.py               # Configurações (temperatura, tokens)
│   ├── db/
│   │   ├── database.py         # Conexão com PostgreSQL
│   │   └── models.py           # Tabelas do banco
│   ├── models/
│   │   └── schemas.py          # Modelos de request/response
│   ├── routes/
│   │   └── chat.py             # Rotas /chat
│   ├── services/
│   │   ├── ollama_service.py   # Comunicação com o Ollama
│   │   └── memory_service.py   # Histórico de conversas
│   ├── utils/
│   │   └── prompt_builder.py   # Monta o prompt com contexto
│   └── Dockerfile
├── frontend/
│   ├── app.py                  # Interface Streamlit
│   └── Dockerfile
├── docker-compose.yml
└── requirements.txt
```

---

## Comandos úteis

```bash
# Subir os containers em background
docker compose up -d --build

# Ver logs em tempo real
docker compose logs -f

# Ver logs de um serviço específico
docker compose logs -f backend

# Parar tudo
docker compose down

# Parar e remover volumes (apaga banco de dados)
docker compose down -v

# Reiniciar um serviço
docker compose restart backend
```

---

## Variáveis de ambiente

| Variável | Serviço | Padrão | Descrição |
|----------|---------|--------|-----------|
| `DATABASE_URL` | backend | `postgresql://chatuser:chatpass@postgres:5432/chatdb` | Conexão com o banco |
| `OLLAMA_URL` | backend | `http://ollama:11434` | Endereço do Ollama |
| `BACKEND_URL` | frontend | `http://backend:8000` | Endereço do backend |
