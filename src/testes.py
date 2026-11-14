"""Executa as perguntas de teste e calcula os indicadores.

Execute com:  python src/testes.py
Gera também docs/resultados_testes.md.
"""
import json
import os
import time

import logica

RAIZ = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..")
CAMINHO_TESTES = os.path.join(RAIZ, "data", "testes.json")
CAMINHO_RESULTADOS = os.path.join(RAIZ, "docs", "resultados_testes.md")


def carregar_testes(caminho=CAMINHO_TESTES):
    with open(caminho, encoding="utf-8") as arquivo:
        return json.load(arquivo)["testes"]


def obter_resultado(teste, registros):
    """Executa uma consulta e devolve (status, id_obtido, tempo em ms)."""
    inicio = time.perf_counter()
    resultado = logica.buscar(teste["pergunta"], registros, teste.get("tema"))
    tempo_ms = (time.perf_counter() - inicio) * 1000
    id_obtido = None
    if resultado["status"] == "ok":
        id_obtido = resultado["candidatos"][0]["id"]
    return resultado["status"], id_obtido, tempo_ms


def avaliar(testes, registros):
    linhas = []
    for teste in testes:
        status, id_obtido, tempo_ms = obter_resultado(teste, registros)
        correto = status == teste["esperado_status"] and (
            teste["esperado_id"] is None or teste["esperado_id"] == id_obtido
        )
        linhas.append({
            "id": teste["id"],
            "tipo": teste["tipo"],
            "pergunta": teste["pergunta"] or "(vazia)",
            "esperado": teste["esperado_id"] or teste["esperado_status"],
            "obtido": id_obtido or status,
            "correto": correto,
            "tempo_ms": tempo_ms,
        })
    return linhas


def comparar_modelos(registros):
    """Compara os modelos A e B nas consultas que retornam uma orientação."""
    palavras_a, palavras_b, fonte_a, fonte_b, total = 0, 0, 0, 0, 0
    for registro in registros:
        texto_a = logica.formatar_resposta(registro, "A")
        texto_b = logica.formatar_resposta(registro, "B")
        palavras_a += len(texto_a.split())
        palavras_b += len(texto_b.split())
        fonte_a += "Fonte consultada:" in texto_a
        fonte_b += "Fonte:" in texto_b
        total += 1
    return {
        "modelo_a_media_palavras": palavras_a / total,
        "modelo_b_media_palavras": palavras_b / total,
        "modelo_a_com_fonte": fonte_a,
        "modelo_b_com_fonte": fonte_b,
        "total": total,
    }


def gerar_relatorio(linhas, triagem_ok, comparacao, pendentes, total_registros):
    acertos = sum(1 for l in linhas if l["correto"])
    taxa = acertos / len(linhas) * 100
    media_ms = sum(l["tempo_ms"] for l in linhas) / len(linhas)

    texto = [
        "# Resultados dos testes",
        "",
        "Gerado automaticamente por `src/testes.py`.",
        "",
        "## Indicadores",
        "",
        f"- Perguntas testadas: {len(linhas)}",
        f"- Respostas corretas: {acertos}",
        f"- Taxa de acerto: {taxa:.1f}%",
        f"- Tempo médio de consulta: {media_ms:.3f} ms",
        f"- Tabela-verdade da triagem consistente: {'sim' if triagem_ok else 'não'}",
        f"- Registros da base: {total_registros} (com data de verificação pendente: {pendentes})",
        "",
        "## Perguntas de teste",
        "",
        "| ID | Tipo | Pergunta | Esperado | Obtido | Resultado | Tempo (ms) |",
        "|---|---|---|---|---|---|---|",
    ]
    for l in linhas:
        resultado = "acerto" if l["correto"] else "erro"
        texto.append(
            f"| {l['id']} | {l['tipo']} | {l['pergunta']} | {l['esperado']} | "
            f"{l['obtido']} | {resultado} | {l['tempo_ms']:.3f} |"
        )
    texto += [
        "",
        "## Comparação dos modelos de resposta",
        "",
        f"- Modelo A (completo): média de {comparacao['modelo_a_media_palavras']:.1f} palavras, "
        f"com campo de fonte em {comparacao['modelo_a_com_fonte']} de {comparacao['total']} orientações.",
        f"- Modelo B (enxuto): média de {comparacao['modelo_b_media_palavras']:.1f} palavras, "
        f"com fonte em {comparacao['modelo_b_com_fonte']} de {comparacao['total']} orientações.",
        "",
    ]
    return "\n".join(texto), taxa, media_ms, acertos


def main():
    registros = logica.carregar_base()
    testes = carregar_testes()
    linhas = avaliar(testes, registros)

    triagem_ok = all(l["iguais"] for l in logica.tabela_verdade())
    comparacao = comparar_modelos(registros)
    pendentes = sum(1 for r in registros if r["data_verificacao"] == "PENDENTE")

    relatorio, taxa, media_ms, acertos = gerar_relatorio(
        linhas, triagem_ok, comparacao, pendentes, len(registros)
    )
    os.makedirs(os.path.dirname(CAMINHO_RESULTADOS), exist_ok=True)
    with open(CAMINHO_RESULTADOS, "w", encoding="utf-8") as arquivo:
        arquivo.write(relatorio)

    print(f"Perguntas testadas: {len(linhas)}")
    print(f"Acertos: {acertos}  |  Taxa de acerto: {taxa:.1f}%")
    print(f"Tempo médio de consulta: {media_ms:.3f} ms")
    print(f"Tabela-verdade da triagem consistente: {'sim' if triagem_ok else 'não'}")
    if pendentes:
        print(f"Atenção: {pendentes} registros ainda com data_verificacao PENDENTE.")
    print(f"Resultados gravados em {os.path.relpath(CAMINHO_RESULTADOS, RAIZ)}")
    for l in linhas:
        if not l["correto"]:
            print(f"  erro em {l['id']}: esperado {l['esperado']}, obtido {l['obtido']}")


if __name__ == "__main__":
    main()
