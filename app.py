import streamlit as st
from main import gerar_branding, gerar_logos, gerar_kit_midia

st.set_page_config(page_title="Brand Agent", layout="centered")
st.title("Gerador de Marca com IA")

# ----------------------------
# Estado da sessão
# ----------------------------
if "branding" not in st.session_state:
    st.session_state.branding = None

if "nome_marca" not in st.session_state:
    st.session_state.nome_marca = None

if "feedback" not in st.session_state:
    st.session_state.feedback = ""

if "briefing" not in st.session_state:
    st.session_state.briefing = None

if "kit_midia" not in st.session_state:
    st.session_state.kit_midia = None


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
    st.session_state.kit_midia = None

    with st.spinner("Criando identidade..."):
        branding, nome_marca = gerar_branding(
            ideia,
            publico,
            tom,
            nome_existente
        )

        gerar_logos(branding)

        st.session_state.branding = branding
        st.session_state.nome_marca = nome_marca


# ----------------------------
# EXIBIÇÃO DOS RESULTADOS
# ----------------------------
if st.session_state.branding:
    st.subheader("Identidade de marca")
    st.text(st.session_state.branding)

    st.subheader("Logos")

    col1, col2 = st.columns(2)
    col1.image("logo_principal.png", caption="Logo principal", width=250)
    col2.image("logo_secundario.png", caption="Logo secundário", width=200)

    feedback = st.text_input(
        "Feedback para refazer a marca",
        value=st.session_state.feedback
    )

    col_a, col_b = st.columns(2)

    # Aprovar
    if col_a.button("Aprovar logo e gerar kit de mídia"):
        with st.spinner("Gerando kit de mídia..."):
            kit = gerar_kit_midia(
                st.session_state.branding,
                st.session_state.nome_marca
            )
            st.session_state.kit_midia = kit

    # Refazer
    if col_b.button("Refazer com feedback"):
        if st.session_state.briefing:
            ideia, publico, tom, nome_existente = st.session_state.briefing
            st.session_state.feedback = feedback
            st.session_state.kit_midia = None

            with st.spinner("Refazendo marca..."):
                branding, nome_marca = gerar_branding(
                    ideia,
                    publico,
                    tom,
                    nome_existente,
                    feedback
                )

                gerar_logos(branding)

                st.session_state.branding = branding
                st.session_state.nome_marca = nome_marca

            st.rerun()


# ----------------------------
# EXIBIR KIT DE MÍDIA
# ----------------------------
if st.session_state.kit_midia:
    st.subheader("Kit de mídia")

    for titulo, imagem in st.session_state.kit_midia:
        st.image(imagem, caption=titulo, width=350)
