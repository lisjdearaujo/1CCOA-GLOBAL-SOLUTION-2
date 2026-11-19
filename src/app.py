"""Interface web opcional do CyberCidadão Assist.

Instale: pip install streamlit
Execute: streamlit run src/app.py
A versão CLI (python src/sistema.py) funciona sem instalar pacotes.
"""
import streamlit as st
import logica

st.set_page_config(page_title="CyberCidadão Assist", page_icon="🛡️")
st.title("CyberCidadão Assist")
st.caption(
    "Orientação em segurança digital. Não representa órgãos públicos nem confirma "
    "com certeza se uma mensagem é golpe. Não informe senhas ou dados pessoais."
)

try:
    registros = logica.carregar_base()
except logica.ErroBase as erro:
    st.error(f"Não foi possível carregar a base: {erro}")
    st.stop()


def exibir_orientacao(registro):
    st.text(logica.formatar_resposta(registro, "A"))
    relacionados = logica.temas_relacionados(registro["tema"])
    if relacionados:
        st.caption("Temas relacionados: " + ", ".join(logica.NOMES_TEMAS[t] for t in relacionados))


aba_pergunta, aba_temas, aba_triagem = st.tabs(["Perguntar", "Navegar por tema", "Triagem"])

with aba_pergunta:
    temas = logica.temas_disponiveis(registros)
    opcoes = ["Todos os temas"] + [logica.NOMES_TEMAS[t] for t in temas]
    filtro = st.selectbox("Filtrar por tema (opcional)", opcoes)
    tema_filtro = None if filtro == opcoes[0] else temas[opcoes.index(filtro) - 1]
    pergunta = st.text_input("Sua pergunta", placeholder="Ex.: como criar uma senha forte?")
    if st.button("Consultar", key="buscar"):
        st.session_state["consulta"] = logica.buscar(pergunta, registros, tema_filtro)
    resultado = st.session_state.get("consulta")
    if resultado:
        if resultado["status"] == "vazio":
            st.warning("Entrada vazia. Digite uma pergunta ou escolha um tema.")
        elif resultado["status"] == "sem_resposta":
            st.info(logica.mensagem_sem_resposta())
        elif resultado["status"] == "ambiguo":
            st.warning("Encontrei mais de uma orientação possível. Escolha a mais adequada:")
            candidato = st.selectbox(
                "Orientação encontrada",
                resultado["candidatos"],
                format_func=lambda r: f"{r['id']} · {logica.NOMES_TEMAS[r['tema']]} · {logica.titulo_registro(r)}",
            )
            exibir_orientacao(candidato)
        else:
            exibir_orientacao(resultado["candidatos"][0])

with aba_temas:
    st.write("Selecione um assunto e uma orientação. Não é necessário escrever uma pergunta.")
    temas = logica.temas_disponiveis(registros)
    selecionado = st.selectbox("Assunto", temas, format_func=lambda tema: logica.NOMES_TEMAS[tema])
    orientacoes = logica.registros_do_tema(registros, selecionado)
    registro = st.selectbox(
        "Orientação", orientacoes,
        format_func=lambda r: f"{logica.titulo_registro(r)} ({r['id']})",
    )
    exibir_orientacao(registro)
    # Este seletor usa o grafo real e permite continuar a consulta em outro tema.
    relacionados = logica.temas_relacionados(registro["tema"])
    if relacionados:
        proximo = st.selectbox(
            "Continuar por um assunto relacionado (opcional)",
            [None] + relacionados,
            format_func=lambda tema: "Não continuar" if tema is None else logica.NOMES_TEMAS[tema],
        )
        if proximo:
            escolhidos = logica.registros_do_tema(registros, proximo)
            proximo_registro = st.selectbox(
                "Orientação relacionada", escolhidos,
                format_func=lambda r: f"{logica.titulo_registro(r)} ({r['id']})",
            )
            exibir_orientacao(proximo_registro)

with aba_triagem:
    st.write("Marque somente os sinais observados. Não cole o texto de mensagens privadas.")
    col1, col2 = st.columns(2)
    with col1:
        pede_dados = st.checkbox("Pede dados pessoais, senhas ou códigos")
        cria_urgencia = st.checkbox("Cria urgência ou ameaça")
    with col2:
        tem_link = st.checkbox("Contém link")
        remetente = st.checkbox("Remetente desconhecido")
    if st.button("Analisar sinais"):
        resultado_triagem = logica.triagem(pede_dados, cria_urgencia, tem_link, remetente)
        if resultado_triagem["alerta"]:
            st.warning(logica.mensagem_triagem(resultado_triagem))
        else:
            st.info(logica.mensagem_triagem(resultado_triagem))
