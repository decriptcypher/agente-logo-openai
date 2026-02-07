from openai import OpenAI
import base64
import os
from dotenv import load_dotenv

from agents.application_agent import gerar_aplicacoes
from agents.social_agent import gerar_posts
from agents.packaging_agent import gerar_embalagens

# ----------------------------
# Configuração
# ----------------------------
load_dotenv()
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))


# ----------------------------
# Agente de Branding
# ----------------------------
def gerar_branding(ideia, publico, tom, nome_existente="", feedback=""):
    if nome_existente.strip():
        nome_instrucao = f"O nome da marca deve ser: {nome_existente} (não altere)."
    else:
        nome_instrucao = "Crie um nome para a marca."

    prompt = f"""
Você é um especialista em branding.

Crie uma identidade de marca com base neste briefing:

Ideia: {ideia}
Público: {publico}
Tom: {tom}

{nome_instrucao}

Feedback do usuário:
{feedback}

Gere:
- Nome da marca
- Slogan curto
- Paleta de cores (3 a 4 cores com nome e HEX)
- Tipografia recomendada
"""

    response = client.responses.create(
        model="gpt-5-mini",
        input=prompt
    )

    branding_text = response.output_text

    # nome padrão simples
    nome_marca = "marca"
    for linha in branding_text.split("\n"):
        if "Nome" in linha:
            nome_marca = linha.split(":")[-1].strip().replace(" ", "_")
            break

    return branding_text, nome_marca


# ----------------------------
# Agente de Logo
# ----------------------------
def gerar_logos(branding_text):
    prompt_principal = f"""
Crie o LOGO PRINCIPAL da marca com base neste branding:

{branding_text}

REGRAS IMPORTANTES:
- Use SOMENTE as cores da paleta fornecida
- Não invente novas cores
- Estilo flat
- Fundo branco
- Visual profissional
- Design vetorial
- Sem mockups
- Logo centralizado
"""

    prompt_secundario = f"""
Crie o LOGO SECUNDÁRIO (variação) da marca com base neste branding:

{branding_text}

REGRAS IMPORTANTES:
- Deve ser visualmente diferente do logo principal
- Pode ser:
  - símbolo isolado
  - monograma
  - versão compacta
- Use SOMENTE as cores da paleta
- Estilo flat
- Fundo branco
- Design vetorial
- Sem mockups
"""

    # Logo principal
    result_main = client.images.generate(
        model="gpt-image-1",
        prompt=prompt_principal,
        size="1024x1024"
    )

    with open("logo_principal.png", "wb") as f:
        f.write(base64.b64decode(result_main.data[0].b64_json))

    # Logo secundário
    result_secondary = client.images.generate(
        model="gpt-image-1",
        prompt=prompt_secundario,
        size="1024x1024"
    )

    with open("logo_secundario.png", "wb") as f:
        f.write(base64.b64decode(result_secondary.data[0].b64_json))


# ----------------------------
# Kit de mídia
# ----------------------------
def gerar_kit_midia(branding, nome_marca):
    import base64

    imagens = []

    prompt_base = f"""
Crie uma imagem publicitária para esta marca:

{branding}

REGRAS IMPORTANTES:
- Use SOMENTE as cores da paleta
- Respeite o estilo tipográfico
- Visual consistente com o logo
- Estilo profissional
- Fundo limpo
"""

    prompts = [
        "Cartão de visita minimalista",
        "Brinde promocional com a marca",
        "Aplicação da marca em material corporativo",
        "Post de Instagram promocional",
        "Post de Instagram institucional",
        "Embalagem do produto",
        "Embalagem em perspectiva estilo propaganda"
    ]

    for p in prompts:
        result = client.images.generate(
            model="gpt-image-1",
            prompt=prompt_base + "\n\nCENA: " + p,
            size="1024x1024"
        )

        img = base64.b64decode(result.data[0].b64_json)
        imagens.append((p, img))

    return imagens
