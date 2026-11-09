# P0 — Pedidos soltos viram registro

Um pequeno prestador de serviços domésticos (instalação, encanamento, pintura, dedetização) recebe pedidos por WhatsApp ou e-mail e precisa transformar cada mensagem livre em um registro estruturado:

| Campo | Significado |
| --- | --- |
| `nome` | quem pede o serviço |
| `contato` | telefone ou e-mail para retorno |
| `servico` | o que precisa ser feito |
| `data_desejada` | quando o cliente quer o atendimento |
| `urgencia` | `baixa`, `media` ou `alta` |

Hoje esses dados são copiados à mão. Campos trocam de lugar, datas somem e o pedido fica incompleto na agenda.

## Por que um LLM

Cada cliente escreve de um jeito. Tem abreviação (`hj`, `qq dia`, `n tem pressa`), data por extenso (`semana que vem`, `próxima quinta`, `sexta que vem`) e informação fora de ordem. Não existe um formulário: a mesma ideia aparece no começo, no meio ou no fim da frase.

Regex e um parser fixo quebram nesse texto. Uma expressão que acha telefone não decide se “amanhã cedo” é urgência alta, nem junta “fala com o João” com o serviço de encanador quando a frase está bagunçada. O modelo lê a mensagem inteira e devolve só o JSON dos cinco campos, com `null` quando o dado não veio.

## Exemplos

Mensagens fictícias, sem dados pessoais reais. Os arquivos estão em `exemplos/`.

**1. Completa** (`exemplos/01-completa.txt`)

> Oi, aqui é a Marina Souza. Meu zap é 11 98888-1234. Preciso de uma instalação de ar-condicionado no dia 20/11, de manhã. É urgente: o quarto do bebê está muito quente.

**2. Faltando campos** (`exemplos/02-faltando-campos.txt`) — sem nome e sem contato

> Boa tarde, queria agendar uma limpeza de sofá. Pode ser na próxima quinta?

**3. Bagunçada** (`exemplos/03-baguncada.txt`) — ordem solta, dois contatos, abreviação

> urgente!!! torneira pingando desde ontem na cozinha, se puder vir hj ou amanhã cedo melhor, fala com o João no (21)99999-0000 ou joao.teste@email.com, ele que vai estar em casa, servico de encanador

**4. Abreviada, data por extenso** (`exemplos/04-abreviada.txt`)

> e ai, semana que vem preciso de alguém pra pintar a sala, n tem pressa nao, pode ser qq dia dps das 14h. me chama no cel 31 97777-4321. abs, Carla

**5. Fora de ordem** (`exemplos/05-fora-de-ordem.txt`)

> Alta prioridade. Data: sexta que vem. Serviço: dedetização do apartamento. Contato: 85 91234-5678. Nome: Pedro Almeida.

## Como rodar no Mac

```bash
cd P0
python3.12 -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
python app.py
```

O `.env` (fora do Git) define o servidor e o modelo:

```bash
OLLAMA_HOST=https://llm-internal.softex:9001
OLLAMA_MODEL=qwen3.5:9b-q4_K_M
```

Sem terminal, o app lê `ENTRADA_TEXTO` em vez de perguntar a mensagem:

```bash
ENTRADA_TEXTO="$(cat exemplos/01-completa.txt)" python app.py
```

No Mac, sem essa variável, `python app.py` pede a mensagem com `input()`.

## Imagem para o portal

O `--platform linux/amd64` é necessário em Mac com Apple Silicon. Sem ele, a imagem não roda no servidor.

```bash
docker build --platform linux/amd64 -t weslleyfernando71609@gmail.com:latest .
docker save --output weslleyfernando71609@gmail.com.tar weslleyfernando71609@gmail.com:latest
```

O `.dockerignore` deixa de fora `.env`, `.venv` e `.git`. No portal, `OLLAMA_HOST`, `OLLAMA_MODEL` e `ENTRADA_TEXTO` entram pelo ambiente: a imagem não carrega o `.env`.
