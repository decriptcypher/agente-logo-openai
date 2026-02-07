from openai import OpenAI
import base64
from dotenv import load_dotenv
import os
import json
from datetime import datetime

# ----------------------------
# Configuração
# ----------------------------
load_dotenv()
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

# ----------------------------
# Agente de Branding
# ----------------------------
def brand_agent(ideia, publico, tom, nome_existente, feedback=""):
    nome_instrucao = ""
    if nome_existente.strip() != "":
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

Feedback do usuário (se houver):
{feedback}

Gere:
- Nome da marca
- Slogan curto
- Paleta de cores (3 a 4 cores com nome e HEX)
- Tipografia recomendada (estilo de fonte)

Responda de forma clara e objetiva.
"""

    response = client.responses.create(
        model="gpt-5-mini",
        input=prompt
    )

    return response.output_text


# ----------------------------
# Agente de Logo
# ----------------------------
def logo_agent(branding_text, version_folder):
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
  - versão compacta
  - monograma
  - variação horizontal
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

    main_path = f"{version_folder}/logo_principal.png"
    with open(main_path, "wb") as f:
        f.write(base64.b64decode(result_main.data[0].b64_json))

    # Logo secundário
    result_secondary = client.images.generate(
        model="gpt-image-1",
        prompt=prompt_secundario,
        size="1024x1024"
    )

    secondary_path = f"{version_folder}/logo_secundario.png"
    with open(secondary_path, "wb") as f:
        f.write(base64.b64decode(result_secondary.data[0].b64_json))

    return [main_path, secondary_path]


# ----------------------------
# Briefing inicial
# ----------------------------
print("=== Briefing de Marca ===")
ideia = input("Qual é a ideia geral do negócio? ")
publico = input("Quem é o público-alvo? ")
tom = input("Qual o tom de voz da marca? ")
nome_existente = input("A marca já tem nome? (deixe vazio se não) ")

# criar pasta do projeto
timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
project_folder = f"projeto_{timestamp}"
os.makedirs(project_folder, exist_ok=True)

approved = False
feedback = ""
version = 1

# ----------------------------
# Loop de aprovação
# ----------------------------
while not approved:
    version_folder = f"{project_folder}/versao_{version}"
    os.makedirs(version_folder, exist_ok=True)

    print(f"\n=== Gerando versão {version} ===")

    # Brand agent
    branding = brand_agent(ideia, publico, tom, nome_existente, feedback)

    print("\n=== Identidade de Marca ===\n")
    print(branding)

    # salvar branding
    with open(f"{version_folder}/branding.txt", "w") as f:
        f.write(branding)

    # Logo agent
    print("\nGerando logos...")
    logos = logo_agent(branding, version_folder)

    print("\nLogos gerados:")
    for path in logos:
        print(path)

    # Perguntar ao usuário
    print("\nDeseja aprovar ou refazer?")
    print("Digite: aprovar")
    print("ou: feedback: sua instrução")

    user_input = input(">> ")

    if user_input.lower() == "aprovar":
        approved = True
        print("\nMarca aprovada!")
    elif user_input.lower().startswith("feedback:"):
        feedback = user_input.split("feedback:", 1)[1].strip()
        version += 1
    else:
        print("Entrada não reconhecida. Tente novamente.")

# salvar resultado final
final_data = {
    "ideia": ideia,
    "publico": publico,
    "tom": tom,
    "nome_fornecido": nome_existente,
    "versao_aprovada": version
}

with open(f"{project_folder}/resultado_final.json", "w") as f:
    json.dump(final_data, f, indent=2)

print(f"\nProjeto salvo na pasta: {project_folder}")
