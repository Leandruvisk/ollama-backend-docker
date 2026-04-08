# 🚀 Ollama Backend com Suporte a GPU

Este projeto implementa um backend para interação com modelos LLM via Ollama, com suporte a aceleração por GPU usando Docker.

## 📌 Visão Geral
O sistema expõe uma API para comunicação com modelos de linguagem, permitindo:
* Geração de respostas via LLM
* Streaming de respostas (Tempo real)
* Integração com frontend ou outros serviços
* Execução otimizada com GPU (quando disponível)

## ⚙️ Tecnologias Utilizadas
* Python (FastAPI)
* Docker / Docker Compose
* Ollama
* NVIDIA Container Toolkit
* GPU NVIDIA (opcional)

## 🧠 Modelos
Os modelos são gerenciados via Ollama. Para baixar um modelo manualmente:
$ ollama run phi3

## 🐳 Como Executar
1. Clonar o projeto
   $ git clone <seu-repositorio>
   $ cd ollama-backend-docker

2. Subir os containers
   $ docker-compose up --build

3. Acessar o backend
   * Documentação (Swagger UI): http://localhost:8000/docs
   * Base URL: http://localhost:8000

## 🔌 Endpoints

### 📥 Chat (Resposta completa)
POST /chat

Exemplo de Body:
{
  "message": "Explique o que é Docker",
  "model": "phi3"
}

### 📡 Chat Streaming
POST /chat-stream
Retorna a resposta em tempo real via stream.

## 🚀 Suporte a GPU
Este projeto suporta aceleração com GPU NVIDIA via Ollama.

### ✅ Requisitos
* GPU NVIDIA
* Drivers NVIDIA instalados no host
* nvidia-container-toolkit configurado no Docker

### 🔧 Verificar GPU no Docker
$ docker run --rm --gpus all nvidia/cuda:12.2.0-base-ubuntu22.04 nvidia-smi

### 🐳 Docker Compose (Configuração GPU)
O serviço ollama deve conter a reserva de recursos:
deploy:
  resources:
    reservations:
      devices:
        - capabilities: [gpu]

Nota: Se a GPU não for detectada, o Ollama utilizará a CPU automaticamente (fallback).

## 🧪 Teste da API (cURL)
$ curl -X POST http://localhost:8000/chat \
-H "Content-Type: application/json" \
-d '{"message":"Explique o que é Docker","model":"phi3"}'

## 🛠️ Troubleshooting
* Erro: model not found -> Execute: docker exec -it ollama ollama pull phi3
* Erro: Connection refused -> Certifique-se de que o container ollama está rodando.
* GPU não detectada -> Verifique nvidia-smi no host e monitore com watch -n 1 nvidia-smi.

## 📂 Estrutura do Projeto
.
├── backend/           # API FastAPI
├── frontend/          # Interface (opcional)
├── docker-compose.yml # Orquestração de containers
├── Dockerfile         # Build da imagem Backend
└── README.md          # Documentação

## 📈 Melhorias Futuras
- [ ] Implementação de autenticação (JWT/API Key)
- [ ] Suporte a múltiplos modelos em paralelo
- [ ] Sistema de cache com Redis
- [ ] Dashboard de monitoramento de performance da GPU

---
👨‍💻 Autor: Leandro Henrique
Embedded Systems | IoT | AI Backend