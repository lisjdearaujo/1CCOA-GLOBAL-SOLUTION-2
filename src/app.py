"""Interface web opcional (Streamlit) que reutiliza a mesma lógica do CLI.

Instalação:  pip install streamlit
Execução:    streamlit run src/app.py

A interface web é opcional. O caminho principal de avaliação é o CLI:
python src/sistema.py
"""
import streamlit as st

import logica

st.set_page_config(page_title="CyberCidadão Assist", page_icon="🛡️")
st.title("CyberCidadão Assist")
st.caption(
    "Orientação de segurança digital. Não é canal oficial de nenhum órgão público "
    "e não confirma com certeza se uma mensagem é golpe."
)

try:
    registros = logica.carregar_base()
except logica.ErroBase as erro:
    st.error(f"Não foi possível carregar a base de orientações: {erro}")
    st.stop()

temas = logica.temas_disponiveis(registros)
opcoes = ["Todos os temas"] + [logica.NOMES_TEMAS[t] for t in temas]
escolha_tema = st.selectbox("Tema", opcoes)
tema = None if escolha_tema == "Todos os temas" else temas[opcoes.index(escolha_tema) - 1]

pergunta = st.text_input("Digite sua pergunta")

if st.button("Consultar"):
    resultado = logica.buscar(pergunta, registros, tema)
    if resultado["status"] == "vazio":
        st.warning("Entrada vazia. Digite uma pergunta ou escolha um tema.")
    elif resultado["status"] == "sem_resposta":
        st.info(logica.mensagem_sem_resposta())
    elif resultado["status"] == "ambiguo":
        st.write("Sua pergunta corresponde a mais de uma orientação:")
        for registro in resultado["candidatos"]:
            st.markdown(f"**{logica.NOMES_TEMAS[registro['tema']]}**: {registro['orientacao']}")
    else:
        registro = resultado["candidatos"][0]
        st.success(logica.formatar_resposta(registro, "A"))
        relacionados = logica.temas_relacionados(registro["tema"])
        if relacionados:
            st.write("Você também pode consultar: " + ", ".join(logica.NOMES_TEMAS[t] for t in relacionados))

st.divider()
st.subheader("Triagem de mensagem suspeita")
col1, col2 = st.columns(2)
with col1:
    pede_dados = st.checkbox("Pede dados pessoais, senhas ou códigos")
    cria_urgencia = st.checkbox("Cria urgência ou ameaça")
with col2:
    tem_link = st.checkbox("Contém link")
    remetente = st.checkbox("Remetente desconhecido")

if st.button("Analisar sinais"):
    triagem = logica.triagem(pede_dados, cria_urgencia, tem_link, remetente)
    if triagem["alerta"]:
        st.warning("Sinais de alerta: " + ", ".join(triagem["sinais"]) + ". Isto não confirma golpe; confirme pelo canal oficial.")
    else:
        st.info("Nenhuma combinação de sinais de alerta foi encontrada. Isto não garante que a mensagem é segura.")
