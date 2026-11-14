"""CyberCidadão Assist: interface em linha de comando.

Execute com:  python src/sistema.py
Requer Python 3.10 ou superior. Não usa bibliotecas externas.
"""
import logica

AVISO_INICIAL = (
    "CyberCidadão Assist orienta sobre segurança digital.\n"
    "Não é canal oficial de nenhum órgão público e não confirma com certeza se uma mensagem é golpe."
)


def mostrar_resposta(registro, modelo="A"):
    print("\n" + logica.formatar_resposta(registro, modelo) + "\n")
    relacionados = logica.temas_relacionados(registro["tema"])
    if relacionados:
        print("Você também pode consultar:")
        for i, tema in enumerate(relacionados, start=1):
            print(f"  {i}. {logica.NOMES_TEMAS[tema]}")
        print()


def escolher_tema(registros):
    temas = logica.temas_disponiveis(registros)
    print("\nTemas disponíveis:")
    for i, tema in enumerate(temas, start=1):
        print(f"  {i}. {logica.NOMES_TEMAS[tema]}")
    print("  0. Voltar")
    escolha = input("Escolha um tema: ").strip()
    if not escolha.isdigit():
        print("Opção inválida. Digite apenas o número do tema.")
        return None
    numero = int(escolha)
    if numero == 0:
        return None
    if 1 <= numero <= len(temas):
        return temas[numero - 1]
    print("Opção inexistente. Escolha um número da lista.")
    return None


def consultar_pergunta(registros, tema=None):
    pergunta = input("Digite sua pergunta: ").strip()
    resultado = logica.buscar(pergunta, registros, tema)

    if resultado["status"] == "vazio":
        print("Entrada vazia. Digite uma pergunta ou escolha um tema pelo menu.")
    elif resultado["status"] == "sem_resposta":
        print("\n" + logica.mensagem_sem_resposta() + "\n")
    elif resultado["status"] == "ambiguo":
        print("\nSua pergunta corresponde a mais de uma orientação. Escolha a mais próxima:")
        for i, registro in enumerate(resultado["candidatos"], start=1):
            print(f"  {i}. {logica.NOMES_TEMAS[registro['tema']]}: {registro['orientacao'][:80]}...")
        escolha = input("Número da opção (Enter para cancelar): ").strip()
        if escolha.isdigit() and 1 <= int(escolha) <= len(resultado["candidatos"]):
            mostrar_resposta(resultado["candidatos"][int(escolha) - 1])
        elif escolha:
            print("Opção inexistente. Consulta cancelada.")
    else:
        mostrar_resposta(resultado["candidatos"][0])


def fluxo_triagem():
    print("\nTriagem de mensagem suspeita. Responda s (sim) ou n (não).")
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
            if resposta in ("s", "n"):
                respostas[chave] = resposta == "s"
                break
            print("Responda apenas s ou n.")

    resultado = logica.triagem(
        respostas["pede_dados"], respostas["cria_urgencia"],
        respostas["tem_link"], respostas["remetente"],
    )
    if resultado["alerta"]:
        print("\nSinais de alerta encontrados: " + ", ".join(resultado["sinais"]) + ".")
        print("Isto não confirma golpe. Não clique em links e confirme pelo canal oficial da instituição.\n")
    else:
        print("\nNenhuma combinação de sinais de alerta foi encontrada.")
        print("Isto não garante que a mensagem é segura. Em caso de dúvida, confirme pelo canal oficial.\n")


def menu(registros):
    while True:
        print("=" * 60)
        print("MENU")
        print("  1. Ver temas disponíveis")
        print("  2. Consultar por tema")
        print("  3. Fazer uma pergunta em texto")
        print("  4. Triagem de mensagem suspeita")
        print("  0. Sair")
        escolha = input("Opção: ").strip()

        if escolha == "1":
            print("\nTemas: " + ", ".join(logica.NOMES_TEMAS[t] for t in logica.temas_disponiveis(registros)))
        elif escolha == "2":
            tema = escolher_tema(registros)
            if tema:
                consultar_pergunta(registros, tema)
        elif escolha == "3":
            consultar_pergunta(registros)
        elif escolha == "4":
            fluxo_triagem()
        elif escolha == "0":
            print("Encerrando. Cuide das suas senhas!")
            break
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
