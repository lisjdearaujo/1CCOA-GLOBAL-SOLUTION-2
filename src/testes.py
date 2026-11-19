"""Testes de consulta, lógica booleana e comparação de modelos.

Na raiz: python src/testes.py
Gera docs/resultados_testes.md com evidências, sem inventar teste com pessoas.
"""
import json
import os
import statistics
import time

import logica

RAIZ = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..")
CAMINHO_TESTES = os.path.join(RAIZ, "data", "testes.json")
CAMINHO_RESULTADOS = os.path.join(RAIZ, "docs", "resultados_testes.md")
STATUS_PERMITIDOS = {"ok", "ambiguo", "sem_resposta", "vazio"}


def carregar_testes(caminho=CAMINHO_TESTES):
    """Lê e valida perguntas de teste; não permite indicadores de uma lista vazia."""
    try:
        with open(caminho, encoding="utf-8") as arquivo:
            dados = json.load(arquivo)
    except (OSError, UnicodeError, json.JSONDecodeError) as erro:
        raise ValueError(f"não foi possível ler testes.json: {erro}") from erro
    if not isinstance(dados, dict) or not isinstance(dados.get("testes"), list) or not dados["testes"]:
        raise ValueError("testes.json deve conter uma lista 'testes' não vazia")
    testes = dados["testes"]
    ids = set()
    for indice, teste in enumerate(testes, start=1):
        if not isinstance(teste, dict):
            raise ValueError(f"teste {indice}: esperado um objeto")
        if not all(chave in teste for chave in ("id", "tipo", "pergunta", "esperado_status", "esperado_id")):
            raise ValueError(f"teste {indice}: campos obrigatórios ausentes")
        if not isinstance(teste["id"], str) or teste["id"] in ids:
            raise ValueError(f"teste {indice}: ID inválido ou repetido")
        ids.add(teste["id"])
        if not isinstance(teste["pergunta"], str) or not isinstance(teste["tipo"], str):
            raise ValueError(f"teste {indice}: pergunta e tipo devem ser textos")
        if teste["esperado_status"] not in STATUS_PERMITIDOS:
            raise ValueError(f"teste {indice}: status esperado desconhecido")
        if teste["esperado_status"] == "ok" and not isinstance(teste["esperado_id"], str):
            raise ValueError(f"teste {indice}: para status ok, informe esperado_id")
        if teste.get("tema") not in (None, *logica.NOMES_TEMAS.keys()):
            raise ValueError(f"teste {indice}: tema desconhecido")
    return testes


def avaliar(testes, registros):
    linhas = []
    por_id = {r["id"]: r for r in registros}
    for teste in testes:
        inicio = time.perf_counter()
        resultado = logica.buscar(teste["pergunta"], registros, teste.get("tema"))
        tempo_ms = (time.perf_counter() - inicio) * 1000
        id_obtido = resultado["candidatos"][0]["id"] if resultado["status"] == "ok" else None
        correto = resultado["status"] == teste["esperado_status"] and (
            teste["esperado_status"] != "ok" or id_obtido == teste["esperado_id"]
        )
        esperado = por_id.get(teste["esperado_id"]) if teste["esperado_id"] else None
        obtido = por_id.get(id_obtido) if id_obtido else None
        linhas.append({
            "id": teste["id"], "tipo": teste["tipo"], "pergunta": teste["pergunta"] or "(vazia)",
            "esperado_status": teste["esperado_status"], "esperado_id": teste["esperado_id"],
            "obtido_status": resultado["status"], "obtido_id": id_obtido,
            "esperado_texto": esperado["orientacao"] if esperado else "Não aplicável",
            "obtido_texto": obtido["orientacao"] if obtido else (
                "Seleção do usuário necessária" if resultado["status"] == "ambiguo"
                else logica.mensagem_sem_resposta() if resultado["status"] == "sem_resposta"
                else "Entrada vazia"),
            "correto": correto, "tempo_ms": tempo_ms,
            "registro_obtido": obtido,
        })
    return linhas


def comparar_modelos(linhas):
    """Aplica ambos os modelos a consultas de teste que encontraram resposta única."""
    textos = [(logica.formatar_resposta(l["registro_obtido"], "A"),
               logica.formatar_resposta(l["registro_obtido"], "B"))
              for l in linhas if l["obtido_status"] == "ok"]
    if not textos:
        return {"consultas": 0, "media_a": 0, "media_b": 0, "fontes_a": 0, "fontes_b": 0,
                "avisos_a": 0, "avisos_b": 0}
    return {
        "consultas": len(textos),
        "media_a": statistics.mean(len(a.split()) for a, b in textos),
        "media_b": statistics.mean(len(b.split()) for a, b in textos),
        "fontes_a": sum("Fonte consultada:" in a for a, b in textos),
        "fontes_b": sum("Fonte:" in b for a, b in textos),
        "avisos_a": sum("canal oficial" in a for a, b in textos),
        "avisos_b": sum("canal oficial" in b for a, b in textos),
    }


def escapar_tabela(texto):
    return str(texto).replace("|", "\\|").replace("\n", " ")


def gerar_relatorio(linhas, triagem_ok, comparacao, pendentes, total_registros):
    acertos = sum(1 for l in linhas if l["correto"])
    taxa = acertos / len(linhas) * 100
    media_ms = statistics.mean(l["tempo_ms"] for l in linhas)
    texto = [
        "# Resultados dos testes", "",
        "Arquivo gerado automaticamente por `python src/testes.py`.",
        "Os tempos são medições locais desta execução e variam por computador. Não são latências de rede.", "",
        "## Indicadores", "",
        f"- Consultas avaliadas: **{len(linhas)}**",
        f"- Consultas com resultado esperado: **{acertos}**",
        f"- Taxa de acerto neste conjunto fixo: **{taxa:.1f}%**",
        f"- Tempo médio de busca: **{media_ms:.3f} ms**",
        f"- Menor/maior tempo: {min(l['tempo_ms'] for l in linhas):.3f} / {max(l['tempo_ms'] for l in linhas):.3f} ms",
        f"- Equivalência booleana da triagem: **{'16/16 combinações' if triagem_ok else 'FALHOU'}**",
        f"- Base: **{total_registros} orientações**; datas pendentes: **{pendentes}**", "",
        "**Interpretação:** a porcentagem indica apenas o desempenho nessas perguntas, "
        "não a exatidão em qualquer pergunta real. Status 'sem_resposta', 'ambiguo' e "
        "'vazio' podem ser acertos quando são os comportamentos esperados.", "",
        "## Consultas e classificações", "",
        "| ID | Tipo | Pergunta | Esperado (status / ID) | Obtido (status / ID) | Classificação | Tempo (ms) |",
        "|---|---|---|---|---|---|---|",
    ]
    for linha in linhas:
        texto.append(
            f"| {linha['id']} | {linha['tipo']} | {escapar_tabela(linha['pergunta'])} | "
            f"{linha['esperado_status']} / {linha['esperado_id'] or '—'} | "
            f"{linha['obtido_status']} / {linha['obtido_id'] or '—'} | "
            f"{'acerto' if linha['correto'] else 'erro'} | {linha['tempo_ms']:.3f} |"
        )
    texto.extend(["", "## Orientações esperadas e retornadas", ""])
    for linha in linhas:
        texto.extend([
            f"### {linha['id']} — {escapar_tabela(linha['pergunta'])}",
            f"- **Esperado:** {linha['esperado_status']} / {linha['esperado_id'] or '—'}. "
            f"{linha['esperado_texto']}",
            f"- **Obtido:** {linha['obtido_status']} / {linha['obtido_id'] or '—'}. "
            f"{linha['obtido_texto']}",
            f"- **Resultado:** {'acerto' if linha['correto'] else 'erro'}.", "",
        ])
    texto.extend([
        "## Comparação dos modelos em perguntas de teste", "",
        f"Os dois formatos foram aplicados às mesmas **{comparacao['consultas']} consultas** "
        "que encontraram uma única orientação (incluindo suas reformulações).",
        "",
        "| Indicador | Modelo A (completo) | Modelo B (enxuto) |",
        "|---|---:|---:|",
        f"| Palavras por resposta (média) | {comparacao['media_a']:.1f} | {comparacao['media_b']:.1f} |",
        f"| Fonte exibida | {comparacao['fontes_a']}/{comparacao['consultas']} | "
        f"{comparacao['fontes_b']}/{comparacao['consultas']} |",
        f"| Aviso de confirmação | {comparacao['avisos_a']}/{comparacao['consultas']} | "
        f"{comparacao['avisos_b']}/{comparacao['consultas']} |", "",
        "**Escolha:** modelo A como padrão. Apesar de mais longo, separa tema, orientação, "
        "referência, data e limite de atuação. O modelo B é mais curto, mas apresenta "
        "menos contexto para conferir a origem da informação.", "",
        "## Limitações e melhorias", "",
        "- A base tem somente 17 orientações; reformulações diferentes das testadas podem falhar.",
        "- As palavras-chave e o limiar de correspondência são regras manuais, não análise semântica.",
        "- Melhorias propostas: ampliar paráfrases e sinônimos revisados; testar perguntas reais "
        "de outras pessoas e registrar erros novos; revisar periodicamente as referências.",
        "- **Teste de facilidade de uso:** não é inferido destes testes automatizados. A avaliação "
        "por roteiro de tarefas está registrada em `docs/teste_usabilidade.md`.",
        "",
    ])
    return "\n".join(texto), taxa, media_ms, acertos


def main():
    try:
        registros = logica.carregar_base()
        testes = carregar_testes()
    except (logica.ErroBase, ValueError) as erro:
        print(f"Erro de dados: {erro}")
        return 1
    linhas = avaliar(testes, registros)
    triagem_ok = all(l["iguais"] for l in logica.tabela_verdade())
    comparacao = comparar_modelos(linhas)
    pendentes = sum(r["data_verificacao"] == "PENDENTE" for r in registros)
    relatorio, taxa, media_ms, acertos = gerar_relatorio(
        linhas, triagem_ok, comparacao, pendentes, len(registros)
    )
    os.makedirs(os.path.dirname(CAMINHO_RESULTADOS), exist_ok=True)
    with open(CAMINHO_RESULTADOS, "w", encoding="utf-8") as arquivo:
        arquivo.write(relatorio)
    print(f"Perguntas testadas: {len(linhas)}")
    print(f"Acertos: {acertos} | Taxa de acerto: {taxa:.1f}%")
    print(f"Tempo médio de consulta: {media_ms:.3f} ms")
    print(f"Tabela-verdade da triagem: {'16/16 consistentes' if triagem_ok else 'FALHOU'}")
    print(f"Registros sem data de verificação: {pendentes}")
    print("Relatório gravado em docs/resultados_testes.md")
    for linha in linhas:
        if not linha["correto"]:
            print(f"  erro em {linha['id']}: esperado {linha['esperado_id'] or linha['esperado_status']}, "
                  f"obtido {linha['obtido_id'] or linha['obtido_status']}")
    return 0 if acertos == len(linhas) and triagem_ok and not pendentes else 1


if __name__ == "__main__":
    raise SystemExit(main())
