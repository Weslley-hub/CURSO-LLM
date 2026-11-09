import os, json
import requests, urllib3
from dotenv import load_dotenv

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)  # certificado autogerado do servidor
load_dotenv()

PROMPT = """Extraia da mensagem os campos: nome, contato, servico, data_desejada, urgencia (baixa|media|alta).
Use null para campos ausentes. Responda SOMENTE com JSON.

Mensagem:
{texto}"""


def main():
    host, model = os.environ["OLLAMA_HOST"], os.environ["OLLAMA_MODEL"]
    texto = os.environ.get("ENTRADA_TEXTO") or input("Cole a mensagem: ")
    r = requests.post(f"{host}/api/chat", json={
        "model": model,
        "messages": [{"role": "user", "content": PROMPT.format(texto=texto)}],
        "stream": False,
        "format": "json",
    }, verify=False, timeout=120)
    r.raise_for_status()
    print(json.dumps(json.loads(r.json()["message"]["content"]), ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
