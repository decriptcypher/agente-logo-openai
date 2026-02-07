import streamlit as st
from openai import OpenAI
import base64
import os
from dotenv import load_dotenv

load_dotenv()
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

st.set_page_config(page_title="Brand Agent", layout="centered")

st.title("Gerador de Marca com IA")

# ----------------------------
# Estado da sessão
# ----------------------------
if "branding" not in st.session_state:
    st.session_state.branding = None

if "logos" not in st.session_state:
    st.session_state.logos = None

if "feedback" not in st.session_state:
    st.session_state.feedback = ""

if "briefing" not in st.session_state:
    st.session_state.briefing = None


# ----------------------------
# Função de geração
# ----------------------------
def gerar_marca(ideia, publico, tom, nome_existente, feedback=""):
    nome_instrucao = ""
    if nome_existente.strip():
        nome_instrucao = f"O nome da marca deve ser: {nome_existente} (não altere)."
    else:
        nome_instrucao = "Crie um nome para a marca."

    branding_prompt = f"""
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

    branding_response = client.responses.create(
        model="gpt-5-mini",
        input=branding_prompt
    )

    branding_text = branding_response.output_text

    # Gerar logos
    image_prompt = f"""
Crie dois logos para esta marca:

{branding_text}

REGRAS:
- Use apenas as cores da paleta
- Estilo flat
- Fundo branco
- Design vetorial
- Sem mockups

Logo 1: principal
Logo 2: variação secundária
"""

    result = client.images.generate(
        model="gpt-image-1",
        prompt=image_prompt,
        size="1024x1024",
        n=2
    )

    logos = []
    for img in result.data:
        logos.append(base64.b64decode(img.b64_json))

    return branding_text, logos


# ----------------------------
# FORMULÁRIO DE BRIEFING
# ----------------------------
with st.form("briefing_form"):
    st.subheader("Briefing")

    ideia = st.text_input("Ideia do negócio")
    publico = st.text_input("Público-alvo")
    tom = st.text_input("Tom de voz")
    nome_existente = st.text_input("Nome da marca (opcional)")

    submit = st.form_submit_button("Gerar marca")

if submit:
    st.session_state.briefing = (ideia, publico, tom, nome_existente)
    st.session_state.feedback = ""

    with st.spinner("Criando identidade..."):
        branding, logos = gerar_marca(
            ideia, publico, tom, nome_existente
        )
        st.session_state.branding = branding
        st.session_state.logos = logos


# ----------------------------
# EXIBIÇÃO DOS RESULTADOS
# ----------------------------
if st.session_state.branding:
    st.subheader("Identidade de marca")
    st.text(st.session_state.branding)

if st.session_state.logos:
    st.subheader("Logos")

    col1, col2 = st.columns(2)
    col1.image(st.session_state.logos[0], caption="Logo principal")
    col2.image(st.session_state.logos[1], caption="Logo secundário")

    feedback = st.text_input(
        "Feedback para refazer",
        value=st.session_state.feedback
    )

    col_a, col_b = st.columns(2)

    if col_a.button("Aprovar marca"):
        st.success("Marca aprovada!")

    if col_b.button("Refazer com feedback"):
        if st.session_state.briefing:
            ideia, publico, tom, nome_existente = st.session_state.briefing
            st.session_state.feedback = feedback

            with st.spinner("Refazendo marca..."):
                branding, logos = gerar_marca(
                    ideia,
                    publico,
                    tom,
                    nome_existente,
                    feedback
                )
                st.session_state.branding = branding
                st.session_state.logos = logos

            st.rerun()

