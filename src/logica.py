"""Lógica do CyberCidadão Assist.

Este módulo não usa input() nem print(). Ele é usado pela interface CLI
(sistema.py), pela interface web opcional (app.py) e pelos testes (testes.py).
"""
import json
import os
import unicodedata

CAMINHO_BASE = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "data", "base.json")

CAMPOS_OBRIGATORIOS = ("id", "tema", "palavras_chave", "orientacao", "referencia", "data_verificacao")

STOPWORDS = {
    "a", "o", "as", "os", "um", "uma", "de", "do", "da", "dos", "das", "e", "em", "no", "na",
    "para", "por", "com", "que", "se", "meu", "minha", "eu", "ao", "posso", "como", "ou",
}

# Grafo simples de temas: cada tema aponta para temas relacionados.
GRAFO_TEMAS = {
    "golpes": ["contas_senhas", "privacidade"],
    "privacidade": ["golpes", "servicos_documentos"],
    "contas_senhas": ["golpes", "servicos_documentos"],
    "servicos_documentos": ["privacidade", "contas_senhas"],
}

NOMES_TEMAS = {
    "golpes": "Golpes e fraudes",
    "privacidade": "Privacidade e LGPD",
    "contas_senhas": "Contas e senhas",
    "servicos_documentos": "Serviços e documentos",
}


class ErroBase(Exception):
    """Erro ao carregar ou validar a base de conhecimento."""


def normalizar(texto):
    """Minúsculas, sem acentos e sem pontuação."""
    texto = unicodedata.normalize("NFD", str(texto).lower())
    texto = "".join(c for c in texto if unicodedata.category(c) != "Mn")
    limpo = "".join(c if c.isalnum() else " " for c in texto)
    return " ".join(limpo.split())


def tokens(texto):
    """Palavras relevantes, sem stopwords e com ao menos 3 letras."""
    return {t for t in normalizar(texto).split() if t not in STOPWORDS and len(t) >= 3}


def validar_registro(registro, indice):
    """Retorna uma lista de erros do registro (vazia se estiver correto)."""
    erros = []
    if not isinstance(registro, dict):
        return [f"registro {indice} não é um objeto"]
    for campo in CAMPOS_OBRIGATORIOS:
        if campo not in registro or registro[campo] in ("", None, []):
            erros.append(f"registro {indice}: campo '{campo}' ausente ou vazio")
    if "palavras_chave" in registro and not isinstance(registro["palavras_chave"], list):
        erros.append(f"registro {indice}: 'palavras_chave' deve ser uma lista")
    if registro.get("tema") and registro["tema"] not in NOMES_TEMAS:
        erros.append(f"registro {indice}: tema '{registro['tema']}' desconhecido")
    return erros


def carregar_base(caminho=CAMINHO_BASE):
    """Lê e valida a base. Levanta ErroBase se o arquivo estiver ausente, vazio ou inconsistente."""
    if not os.path.exists(caminho):
        raise ErroBase(f"arquivo da base não encontrado: {caminho}")
    try:
        with open(caminho, encoding="utf-8") as arquivo:
            conteudo = json.load(arquivo)
    except json.JSONDecodeError as erro:
        raise ErroBase(f"base com JSON inválido: {erro}")
    if not isinstance(conteudo, dict) or not isinstance(conteudo.get("registros"), list):
        raise ErroBase("a base deve ser um objeto com a lista 'registros'")
    registros = conteudo["registros"]
    if not registros:
        raise ErroBase("a base está vazia")

    erros = []
    for i, registro in enumerate(registros):
        erros.extend(validar_registro(registro, i))
    ids = [r.get("id") for r in registros if isinstance(r, dict)]
    if len(ids) != len(set(ids)):
        erros.append("há ids repetidos na base")
    if erros:
        raise ErroBase("; ".join(erros))
    return registros


def temas_disponiveis(registros):
    """Temas presentes na base, na ordem definida em NOMES_TEMAS."""
    presentes = {r["tema"] for r in registros}
    return [t for t in NOMES_TEMAS if t in presentes]


def temas_relacionados(tema):
    """Vizinhos do tema no grafo, usados para sugerir continuidade."""
    return GRAFO_TEMAS.get(tema, [])


def pontuar(pergunta, registro):
    """Pontuação: 2 por expressão de palavra-chave encontrada na pergunta, 1 por palavra em comum."""
    consulta = " " + normalizar(pergunta) + " "
    pontos = 0
    tokens_chave = set()
    for expressao in registro["palavras_chave"]:
        expr = normalizar(expressao)
        tokens_chave |= tokens(expr)
        if expr and f" {expr} " in consulta:
            pontos += 2
    pontos += len(tokens(pergunta) & tokens_chave)
    return pontos


def buscar(pergunta, registros, tema=None):
    """Busca a orientação mais próxima.

    Retorna um dicionário com:
      status: "vazio", "ok", "ambiguo" ou "sem_resposta"
      candidatos: registros empatados na melhor pontuação
      pontuacao: a melhor pontuação encontrada
    """
    if not pergunta or not normalizar(pergunta):
        return {"status": "vazio", "candidatos": [], "pontuacao": 0}

    universo = [r for r in registros if tema is None or r["tema"] == tema]
    pontuados = [(pontuar(pergunta, r), r) for r in universo]
    melhor = max((p for p, _ in pontuados), default=0)
    if melhor == 0:
        return {"status": "sem_resposta", "candidatos": [], "pontuacao": 0}

    candidatos = [r for p, r in pontuados if p == melhor]
    status = "ok" if len(candidatos) == 1 else "ambiguo"
    return {"status": status, "candidatos": candidatos, "pontuacao": melhor}


def formatar_resposta(registro, modelo="A"):
    """Modelos de instrução de resposta documentados em docs/prompts.md.

    Modelo A: completo, com papel, formato, fonte obrigatória e aviso.
    Modelo B: enxuto, com orientação, fonte e aviso curto.
    """
    tema = NOMES_TEMAS.get(registro["tema"], registro["tema"])
    if modelo == "B":
        return (
            f"{registro['orientacao']}\n"
            f"Fonte: {registro['referencia']} (verificado em {registro['data_verificacao']}).\n"
            "Confirme requisitos atualizados no canal oficial."
        )
    return (
        "Orientação de segurança digital (não é canal oficial de nenhum órgão).\n"
        f"Tema: {tema}\n"
        f"Orientação: {registro['orientacao']}\n"
        f"Fonte consultada: {registro['referencia']}\n"
        f"Data de verificação: {registro['data_verificacao']}\n"
        "Aviso: confirme sempre as informações atualizadas no canal oficial da instituição."
    )


def mensagem_sem_resposta():
    """Aviso de limitação com alternativas de consulta."""
    sugestao = ", ".join(NOMES_TEMAS.values())
    return (
        "Não encontrei uma orientação confiável para essa pergunta nesta base. "
        f"Tente reformular a pergunta ou escolher um tema: {sugestao}."
    )


# ----- Triagem de mensagens suspeitas (fase 6: lógica booleana) -----
#
# Variáveis:
#   P = pede dados pessoais ou senhas
#   U = cria urgência ou ameaça
#   L = contém link
#   R = remetente desconhecido
#
# Expressão de alerta: alerta = P · U · (L + R)
# Forma implementada, obtida por De Morgan:
#   sem_alerta = ¬P + ¬U + (¬L · ¬R)
#   alerta = ¬sem_alerta
# A função triagem() usa a forma simplificada, e tabela_verdade() mostra
# que ela coincide com a expressão original nas 16 combinações possíveis.

def _alerta_expressao_original(p, u, l, r):
    return bool(p and u and (l or r))


def _alerta_forma_simplificada(p, u, l, r):
    sem_alerta = (not p) or (not u) or ((not l) and (not r))
    return not sem_alerta


def triagem(pede_dados, cria_urgencia, tem_link, remetente_desconhecido):
    """Indica sinais de alerta. Nunca afirma que a mensagem é golpe."""
    alerta = _alerta_forma_simplificada(pede_dados, cria_urgencia, tem_link, remetente_desconhecido)
    sinais = []
    if pede_dados:
        sinais.append("pede dados pessoais ou senhas")
    if cria_urgencia:
        sinais.append("cria urgência ou ameaça")
    if tem_link:
        sinais.append("contém link")
    if remetente_desconhecido:
        sinais.append("remetente desconhecido")
    return {"alerta": alerta, "sinais": sinais}


def tabela_verdade():
    """Lista das 16 linhas, com a expressão original e a simplificada."""
    linhas = []
    for p in (False, True):
        for u in (False, True):
            for l in (False, True):
                for r in (False, True):
                    original = _alerta_expressao_original(p, u, l, r)
                    simplificada = _alerta_forma_simplificada(p, u, l, r)
                    linhas.append({
                        "P": int(p), "U": int(u), "L": int(l), "R": int(r),
                        "original": int(original), "simplificada": int(simplificada),
                        "iguais": original == simplificada,
                    })
    return linhas
