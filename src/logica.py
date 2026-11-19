"""Regras e consultas do CyberCidadão Assist (sem IA nem bibliotecas externas).

Este módulo é compartilhado pelo terminal, pela interface web e pelos testes.
"""
import json
import os
import re
import unicodedata
from datetime import date

CAMINHO_BASE = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "data", "base.json")
CAMPOS_OBRIGATORIOS = ("id", "tema", "palavras_chave", "orientacao", "referencia", "data_verificacao")
STOPWORDS = {
    "a", "o", "as", "os", "um", "uma", "de", "do", "da", "dos", "das", "e", "em", "no", "na",
    "para", "por", "com", "que", "se", "meu", "minha", "meus", "minhas", "eu", "ao", "posso",
    "como", "ou", "pelo", "pela", "pelos", "pelas", "pra", "quero", "qual", "quem", "onde",
}

# Relações explícitas entre assuntos: sugestões de continuidade, não respostas automáticas.
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
    """Erro legível ao carregar/validar os registros JSON."""


def normalizar(texto):
    """Converte para minúsculas, remove acentos e unifica algumas grafias."""
    if not isinstance(texto, str):
        return ""
    texto = unicodedata.normalize("NFD", texto.lower())
    texto = "".join(c for c in texto if unicodedata.category(c) != "Mn")
    texto = "".join(c if c.isalnum() else " " for c in texto)
    texto = re.sub(r"\bwi\s+fi\b", "wifi", texto)
    texto = re.sub(r"\be\s+mail\b", "email", texto)
    return " ".join(texto.split())


def tokens(texto):
    return {t for t in normalizar(texto).split() if len(t) >= 3 and t not in STOPWORDS}


def validar_registro(registro, indice):
    """Valida os tipos e o conteúdo essencial, sem gerar exceções em dados malformados."""
    if not isinstance(registro, dict):
        return [f"registro {indice} deve ser um objeto JSON"]
    erros = []
    for campo in CAMPOS_OBRIGATORIOS:
        if campo not in registro:
            erros.append(f"registro {indice}: campo '{campo}' ausente")

    for campo in ("id", "tema", "orientacao", "referencia", "data_verificacao"):
        if campo in registro and (not isinstance(registro[campo], str) or not registro[campo].strip()):
            erros.append(f"registro {indice}: '{campo}' deve ser um texto não vazio")

    palavras = registro.get("palavras_chave")
    if palavras is not None and (
        not isinstance(palavras, list) or not palavras
        or any(not isinstance(p, str) or not p.strip() for p in palavras)
    ):
        erros.append(f"registro {indice}: 'palavras_chave' deve ser lista de textos não vazios")

    tema = registro.get("tema")
    if isinstance(tema, str) and tema not in NOMES_TEMAS:
        erros.append(f"registro {indice}: tema '{tema}' desconhecido")

    data_verificacao = registro.get("data_verificacao")
    if isinstance(data_verificacao, str) and data_verificacao.strip() and data_verificacao != "PENDENTE":
        try:
            data = date.fromisoformat(data_verificacao)
            if data.isoformat() != data_verificacao:
                raise ValueError("formato diferente de AAAA-MM-DD")
        except ValueError:
            erros.append(f"registro {indice}: 'data_verificacao' deve ser AAAA-MM-DD ou PENDENTE")
    return erros


def carregar_base(caminho=CAMINHO_BASE):
    """Carrega o arquivo ou informa erro recuperável (inclusive arquivo ausente/vazio)."""
    try:
        with open(caminho, "r", encoding="utf-8") as arquivo:
            conteudo = json.load(arquivo)
    except OSError as erro:
        raise ErroBase(f"não foi possível abrir a base '{caminho}': {erro}") from erro
    except (UnicodeError, json.JSONDecodeError) as erro:
        raise ErroBase(f"arquivo de base inválido ou vazio: {erro}") from erro

    if not isinstance(conteudo, dict) or not isinstance(conteudo.get("registros"), list):
        raise ErroBase("o JSON deve conter um objeto com a lista 'registros'")
    registros = conteudo["registros"]
    if not registros:
        raise ErroBase("a lista de registros da base está vazia")
    erros = []
    for i, registro in enumerate(registros, start=1):
        erros.extend(validar_registro(registro, i))
    ids = [r["id"] for r in registros if isinstance(r, dict) and isinstance(r.get("id"), str)]
    if len(ids) != len(set(ids)):
        erros.append("existem identificadores repetidos na base")
    if erros:
        raise ErroBase("; ".join(erros))
    return registros


def temas_disponiveis(registros):
    presentes = {r["tema"] for r in registros}
    return [tema for tema in NOMES_TEMAS if tema in presentes]


def registros_do_tema(registros, tema):
    return [r for r in registros if r["tema"] == tema]


def indice_por_id(registros):
    """Dicionário para recuperar uma orientação pelo identificador em tempo constante."""
    return {registro["id"].upper(): registro for registro in registros}


def temas_relacionados(tema):
    return GRAFO_TEMAS.get(tema, [])


def titulo_registro(registro):
    """Rótulo curto para navegação sem duplicar uma fonte de dados."""
    return registro["palavras_chave"][0].replace("_", " ").capitalize()


def pontuar(pergunta, registro):
    """Expressão inteira: +2 por palavra relevante; sobreposição: +1 por palavra.

    As expressões longas são mais informativas do que uma palavra genérica isolada.
    A pontuação não significa grau de certeza e só é usada para selecionar opções.
    """
    consulta = f" {normalizar(pergunta)} "
    presentes = tokens(pergunta)
    chave_tokens = set()
    pontos = 0
    for expressao in registro["palavras_chave"]:
        expr = normalizar(expressao)
        chave_tokens.update(tokens(expr))
        if expr and f" {expr} " in consulta:
            pontos += 2 * max(1, len(tokens(expr)))
    return pontos + len(presentes & chave_tokens)


def buscar(pergunta, registros, tema=None):
    """Busca literal baseada em pontuação; retorna vazio/sem_resposta/ambiguo/ok.

    Pontua apenas o assunto escolhido, quando especificado. Em empate, não decide
    arbitrariamente: o usuário precisa selecionar entre as orientações encontradas.
    """
    if not normalizar(pergunta):
        return {"status": "vazio", "candidatos": [], "pontuacao": 0}
    universo = registros if tema is None else registros_do_tema(registros, tema)
    # Consulta direta por identificador (por exemplo "G01"), usando um dicionário id -> registro.
    por_id = indice_por_id(universo)
    identificador = normalizar(pergunta).upper()
    if identificador in por_id:
        return {"status": "ok", "candidatos": [por_id[identificador]], "pontuacao": None}
    pontuados = [(pontuar(pergunta, registro), registro) for registro in universo]
    melhor = max((p for p, _ in pontuados), default=0)
    # Uma única palavra casual em uma pergunta longa não é evidência suficiente.
    if melhor == 0 or (len(tokens(pergunta)) >= 3 and melhor <= 1):
        return {"status": "sem_resposta", "candidatos": [], "pontuacao": melhor}
    candidatos = [registro for pontos, registro in pontuados if pontos == melhor]
    return {
        "status": "ok" if len(candidatos) == 1 else "ambiguo",
        "candidatos": candidatos,
        "pontuacao": melhor,
    }


def formatar_resposta(registro, modelo="A"):
    """Dois modelos determinísticos documentados em docs/prompts.md."""
    if modelo not in {"A", "B"}:
        raise ValueError("modelo deve ser A ou B")
    tema = NOMES_TEMAS[registro["tema"]]
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
    return (
        "Não encontrei uma orientação confiável para essa pergunta nesta base. "
        "Tente reformular ou escolha um tema: " + ", ".join(NOMES_TEMAS.values()) + "."
    )


# Lógica booleana: P = dados; U = urgência; L = link; R = remetente desconhecido.
# Original: P · U · (L + R). Complemento, por De Morgan:
# sem_alerta = ¬P + ¬U + (¬L · ¬R); alerta = ¬sem_alerta.
def _alerta_expressao_original(p, u, l, r):
    return bool(p and u and (l or r))


def _alerta_forma_simplificada(p, u, l, r):
    sem_alerta = (not p) or (not u) or ((not l) and (not r))
    return not sem_alerta


def triagem(pede_dados, cria_urgencia, tem_link, remetente_desconhecido):
    """Identifica sinais e uma combinação definida, sem diagnosticar golpes."""
    alerta = _alerta_forma_simplificada(pede_dados, cria_urgencia, tem_link, remetente_desconhecido)
    sinais = []
    if pede_dados:
        sinais.append("pede dados pessoais, senhas ou códigos")
    if cria_urgencia:
        sinais.append("cria urgência ou ameaça")
    if tem_link:
        sinais.append("contém link")
    if remetente_desconhecido:
        sinais.append("remetente desconhecido")
    return {"alerta": alerta, "sinais": sinais}


def mensagem_triagem(resultado):
    """Mesmo sinais isolados exigem cautela; ausência de regra não é garantia."""
    if resultado["sinais"]:
        texto = "Sinais observados: " + ", ".join(resultado["sinais"]) + ".\n"
    else:
        texto = "Nenhum dos quatro sinais informados foi observado.\n"
    if resultado["alerta"]:
        texto += "A combinação definida no protótipo indica atenção reforçada. "
    else:
        texto += "A combinação de alerta definida no protótipo não foi atingida. "
    return texto + (
        "Isso não confirma que seja um golpe nem garante segurança. "
        "Não forneça senhas ou códigos; confirme a solicitação pelo canal oficial da instituição."
    )


def tabela_verdade():
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
