# P0 - Pedidos soltos viram registro

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

Mensagens fictícias, em `exemplos/`.

**1. Completa** (`exemplos/01-completa.txt`)

> Oi, aqui é a Marina Souza. Meu zap é 11 98888-1234. Preciso de uma instalação de ar-condicionado no dia 20/11, de manhã. É urgente: o quarto do bebê está muito quente.

**2. Faltando campos** (`exemplos/02-faltando-campos.txt`) — sem nome e sem contato

> Boa tarde, queria agendar uma limpeza de sofá. Pode ser na próxima quinta?

**3. Bagunçada** (`exemplos/03-bagunçada.txt`) — ordem solta, dois contatos, abreviação

> urgente!!! torneira pingando desde ontem na cozinha, se puder vir hj ou amanhã cedo melhor, fala com o João no (21)99999-0000 ou joao.teste@email.com, ele que vai estar em casa, servico de encanador

**4. Abreviada, data por extenso** (`exemplos/04-abreviada.txt`)

> e ai, semana que vem preciso de alguém pra pintar a sala, n tem pressa nao, pode ser qq dia dps das 14h. me chama no cel 31 97777-4321. abs, Carla

**5. Fora de ordem** (`exemplos/05-fora-de-ordem.txt`)

> Alta prioridade. Data: sexta que vem. Serviço: dedetização do apartamento. Contato: 85 91234-5678. Nome: Pedro Almeida.

**LOCAL**, arquivo `P0/.env`:

```bash
OLLAMA_HOST=http://localhost:11434
OLLAMA_MODEL=qwen3.5:9b
```

**Portal Devel**, env:

```bash
OLLAMA_HOST=https://llm-internal.softex:9001
OLLAMA_MODEL=qwen3.5:9b-q4_K_M
```

Os dois cenários estão comentados em `.env.example`.

Subir o modelo local. A tag `qwen3.5:9b` está em [ollama.com/library/qwen3.5](https://ollama.com/library/qwen3.5).

## Como rodar local

```bash
cd P0
python3.12 -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
python app.py
```
