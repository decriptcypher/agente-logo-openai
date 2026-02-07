from openai import OpenAI
from dotenv import load_dotenv
import base64
import os

load_dotenv()
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))


def gerar_aplicacoes(branding, pasta_saida):
    os.makedirs(pasta_saida, exist_ok=True)

    prompt = f"""
Crie aplicações de identidade visual para a marca abaixo:

{branding}

Gerar:
1. Cartão de visita moderno
2. Brinde promocional
3. Papelaria corporativa

Estilo:
- Fundo limpo
- Layout profissional
- Cores da marca
- Sem mockups exagerados
"""

    result = client.images.generate(
        model="gpt-image-1",
        prompt=prompt,
        size="1024x1024"
    )

    image_base64 = result.data[0].b64_json
    with open(f"{pasta_saida}/aplicacoes.png", "wb") as f:
        f.write(base64.b64decode(image_base64))
