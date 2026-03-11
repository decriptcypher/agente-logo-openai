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

    # 🔹 PROMPT BASE (mantém identidade da marca)
    prompt_base = f"""
Crie imagens publicitárias profissionais para a marca "{nome_marca}".

IDENTIDADE DA MARCA:
{branding}

Use o LOGO fornecido como referência visual.

REGRAS IMPORTANTES:
- Usar SOMENTE as cores da paleta da marca
- Respeitar tipografia e estilo visual
- Manter consistência com o logo
- Estilo moderno e profissional
"""

    titulos = [
        "Cartão de visita minimalista",
        "Brinde promocional",
        "Material corporativo",
        "Post Instagram promocional",
        "Post Instagram institucional",
        "Embalagem do produto",
        "Embalagem propaganda",
        "Embalagem premium"
    ]

    # 🔹 abrir logo
    logo = open("logo_principal.png", "rb")

    # ==========================================
    # PRIMEIRA REQUISIÇÃO — PAPELARIA + SOCIAL
    # ==========================================

    prompt_papelaria_social = prompt_base + """
GERAR 5 IMAGENS DIFERENTES:

1. Cartão de visita minimalista sobre mesa de escritório elegante
2. Brinde promocional (caneca ou camiseta) com o logo aplicado
3. Papelaria corporativa organizada em flat lay (papel timbrado, cartão, envelope)
4. Post de Instagram promocional moderno com composição gráfica
5. Post de Instagram institucional com tipografia forte

IMPORTANTE:
Cada imagem deve ter um layout completamente diferente.
Use composições, enquadramentos e estilos visuais distintos.

Cada imagem deve ter:
- composição diferente
- enquadramento diferente
- layout distinto
"""

    result1 = client.images.edit(
        model="gpt-image-1",
        image=logo,
        prompt=prompt_papelaria_social,
        size="1024x1024",
        n=5
    )

    # ==========================================
    # SEGUNDA REQUISIÇÃO — PRODUTO + PACKAGING
    # ==========================================

    prompt_packaging = prompt_base + """
GERAR 3 IMAGENS:

1. Embalagem de produto em estúdio com iluminação profissional
2. Embalagem em perspectiva estilo propaganda premium
3. Embalagem premium minimalista em fundo elegante

IMPORTANTE:
Cada imagem deve ter um layout completamente diferente.
Use composições, enquadramentos e estilos visuais distintos.

Direção de arte:
- fotografia de produto
- iluminação dramática
- fundo limpo ou gradiente
- estética publicitária
"""

    result2 = client.images.edit(
        model="gpt-image-1",
        image=logo,
        prompt=prompt_packaging,
        size="1024x1024",
        n=3
    )

    # 🔹 juntar resultados
    resultados = result1.data + result2.data

    for i, img in enumerate(resultados):
        imagem = base64.b64decode(img.b64_json)
        imagens.append((titulos[i], imagem))

    return imagens