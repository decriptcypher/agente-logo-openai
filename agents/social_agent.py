from openai import OpenAI
from dotenv import load_dotenv
import base64
import os

load_dotenv()
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))


def gerar_posts(branding, pasta_saida):
    os.makedirs(pasta_saida, exist_ok=True)

    for i in range(1, 3):
        prompt = f"""
Crie um post de Instagram para a marca:

{branding}

Estilo:
- Formato quadrado
- Visual moderno
- Cores da marca
- Tipografia consistente
- Sem mockup
"""

        result = client.images.generate(
            model="gpt-image-1",
            prompt=prompt,
            size="1024x1024"
        )

        image_base64 = result.data[0].b64_json
        with open(f"{pasta_saida}/post_{i}.png", "wb") as f:
            f.write(base64.b64decode(image_base64))
