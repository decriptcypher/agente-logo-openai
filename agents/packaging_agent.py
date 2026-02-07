from openai import OpenAI
from dotenv import load_dotenv
import base64
import os

load_dotenv()
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))


def gerar_embalagens(branding, pasta_saida):
    os.makedirs(pasta_saida, exist_ok=True)

    for i in range(1, 3):
        prompt = f"""
Crie uma embalagem de produto para a marca:

{branding}

Estilo:
- Design moderno
- Cores da marca
- Visual comercial
- Fundo limpo
- Fotografia de produto
"""

        result = client.images.generate(
            model="gpt-image-1",
            prompt=prompt,
            size="1024x1024"
        )

        image_base64 = result.data[0].b64_json
        with open(f"{pasta_saida}/embalagem_{i}.png", "wb") as f:
            f.write(base64.b64decode(image_base64))
