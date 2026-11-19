"""CyberCidadão Assist: terminal, sem dependências externas.

Execute na raiz do projeto: python src/sistema.py
"""
import logica

AVISO_INICIAL = (
    "CyberCidadão Assist orienta sobre segurança digital.\n"
    "Não representa órgãos públicos e não confirma com certeza se uma mensagem é golpe."
)


def escolher_numero(mensagem, limite, permitir_voltar=True):
    """Valida opções; 0 volta e um número fora do intervalo não causa erro."""
    escolha = input(mensagem).strip()
    if not escolha.isdigit():
        print("Opção inválida. Digite somente um número.")
        return None
    numero = int(escolha)
    if numero == 0 and permitir_voltar:
        return 0
    if 1 <= numero <= limite:
        return numero
    print("Opção inexistente. Escolha um número da lista.")
    return None


def escolher_tema(registros):
    temas = logica.temas_disponiveis(registros)
    print("\nTemas disponíveis:")
    for indice, tema in enumerate(temas, start=1):
        print(f"  {indice}. {logica.NOMES_TEMAS[tema]}")
    print("  0. Voltar")
    numero = escolher_numero("Escolha um tema: ", len(temas))
    return temas[numero - 1] if numero else None


def mostrar_resposta(registro):
    """Exibe a fonte e permite seguir diretamente para um tema relacionado."""
    print("\n" + logica.formatar_resposta(registro, "A") + "\n")
    relacionados = logica.temas_relacionados(registro["tema"])
    if not relacionados:
        return None
    print("Você também pode consultar estes temas relacionados:")
    for indice, tema in enumerate(relacionados, start=1):
        print(f"  {indice}. {logica.NOMES_TEMAS[tema]}")
    print("  0. Voltar ao menu principal")
    numero = escolher_numero("Escolha um tema relacionado (0 para voltar): ", len(relacionados))
    return relacionados[numero - 1] if numero else None


def navegar_por_tema(registros, tema):
    """Fluxo iterativo: tema > orientação > tema relacionado, sem recursão."""
    while tema is not None:
        orientacoes = logica.registros_do_tema(registros, tema)
        print("\n" + logica.NOMES_TEMAS[tema] + ":")
        for indice, registro in enumerate(orientacoes, start=1):
            print(f"  {indice}. {logica.titulo_registro(registro)} ({registro['id']})")
        print("  0. Voltar ao menu")
        numero = escolher_numero("Selecione uma orientação: ", len(orientacoes))
        if not numero:
            return
        tema = mostrar_resposta(orientacoes[numero - 1])


def consultar_pergunta(registros, tema=None):
    pergunta = input("Digite sua pergunta: ").strip()
    resultado = logica.buscar(pergunta, registros, tema)
    if resultado["status"] == "vazio":
        print("Entrada vazia. Digite uma pergunta ou escolha um tema pelo menu.")
        return
    if resultado["status"] == "sem_resposta":
        print("\n" + logica.mensagem_sem_resposta() + "\n")
        return
    if resultado["status"] == "ambiguo":
        print("\nHá mais de uma orientação possível. Escolha uma opção:")
        for indice, registro in enumerate(resultado["candidatos"], start=1):
            print(f"  {indice}. {logica.NOMES_TEMAS[registro['tema']]}: {logica.titulo_registro(registro)}")
        print("  0. Cancelar")
        numero = escolher_numero("Escolha a orientação: ", len(resultado["candidatos"]))
        if not numero:
            return
        registro = resultado["candidatos"][numero - 1]
    else:
        registro = resultado["candidatos"][0]
    tema_relacionado = mostrar_resposta(registro)
    if tema_relacionado:
        navegar_por_tema(registros, tema_relacionado)


def fluxo_triagem():
    print("\nTriagem de mensagem suspeita (sem enviar ou copiar a mensagem).")
    perguntas = [
        ("pede_dados", "A mensagem pede dados pessoais, senhas ou códigos?"),
        ("cria_urgencia", "A mensagem cria urgência ou ameaça?"),
        ("tem_link", "A mensagem contém link?"),
        ("remetente", "O remetente é desconhecido para você?"),
    ]
    respostas = {}
    for chave, texto in perguntas:
        while True:
            resposta = input(f"{texto} (s/n): ").strip().lower()
            if resposta in {"s", "n"}:
                respostas[chave] = resposta == "s"
                break
            print("Responda apenas s ou n.")
    resultado = logica.triagem(
        respostas["pede_dados"], respostas["cria_urgencia"],
        respostas["tem_link"], respostas["remetente"],
    )
    print("\n" + logica.mensagem_triagem(resultado) + "\n")


def menu(registros):
    while True:
        print("=" * 56)
        print("MENU")
        print("  1. Ver temas disponíveis")
        print("  2. Navegar por tema e escolher uma orientação")
        print("  3. Fazer uma pergunta em texto")
        print("  4. Triagem de mensagem suspeita")
        print("  0. Sair")
        escolha = input("Opção: ").strip()
        if escolha == "1":
            print("\nTemas: " + ", ".join(logica.NOMES_TEMAS[t] for t in logica.temas_disponiveis(registros)))
        elif escolha == "2":
            tema = escolher_tema(registros)
            if tema:
                navegar_por_tema(registros, tema)
        elif escolha == "3":
            consultar_pergunta(registros)
        elif escolha == "4":
            fluxo_triagem()
        elif escolha == "0":
            print("Encerrando. Cuide das suas senhas!")
            return
        else:
            print("Opção inexistente. Escolha um número do menu.")


def main():
    print(AVISO_INICIAL + "\n")
    try:
        registros = logica.carregar_base()
    except logica.ErroBase as erro:
        print(f"Não foi possível carregar a base de orientações: {erro}")
        return 1
    try:
        menu(registros)
    except (EOFError, KeyboardInterrupt):
        print("\nEncerrando.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
