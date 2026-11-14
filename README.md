<p align="center">
  <img src="assets/logo-fiap.png" alt="FIAP - Faculdade de Informática e Administração Paulista" width="200">
</p>

<h1 align="center">CyberCidadão Assist</h1>
<p align="center"><b>Assistente de orientação em segurança digital para o cidadão</b></p>

<p align="center">Global Solution 2026.2 · Desafio CitizenTech · Case Citizen Assist AI</p>

---

## Nome do grupo

[Nome do grupo]

## 👨‍🎓 Integrantes

- Lisandra Araujo (RM: [RM])
- Eduardo Alves (RM: [RM])

## 👩‍🏫 Professores

- Tutor(a): [Nome do tutor]
- Coordenador(a): André Godoi Chiovato

---

## 📜 Descrição do problema

Cidadãos encontram com frequência informações dispersas, termos técnicos e instruções incompletas sobre golpes, proteção de dados, contas e senhas e cuidados ao usar serviços online. O **CyberCidadão Assist** organiza orientações verificadas, responde perguntas em texto ou por menu e mostra a fonte de cada orientação. Quando não há informação suficiente na base, ele avisa e sugere outros caminhos de consulta.

**Público beneficiado:** cidadãos comuns que usam serviços digitais e precisam de orientação clara antes de agir.

**Temas abordados:**

- **Golpes e fraudes:** golpe do Pix, falsa central de banco, phishing, boleto falso, prêmios que pedem pagamento.
- **Privacidade e LGPD:** direitos do titular, pedido de exclusão de dados, vazamento, dados desnecessários.
- **Contas e senhas:** autenticação em dois fatores, senhas fortes, gerenciadores de senha, conta invadida.
- **Serviços e documentos:** verificação de site oficial, envio de documentos, Wi-Fi público, atualizações.

**Limites do assistente:** ele orienta e não é canal oficial de nenhum órgão público. Ele não confirma com certeza se uma mensagem é golpe; mostra sinais de alerta e recomenda confirmar pelo canal oficial.

---

## 📁 Estrutura de pastas

```text
├── assets/
│   └── logo-fiap.png        Logo usada neste README
├── data/
│   ├── base.json            Base de orientações (17 registros em 4 temas)
│   └── testes.json          Perguntas de teste com o resultado esperado
├── docs/
│   ├── prompts.md           Modelos de instrução de resposta (fase 5) e comparação
│   ├── relatorio_roteiro.md Roteiro do relatório em PDF
│   ├── resultados_testes.md Resultados gerados por src/testes.py
│   ├── teste_usabilidade.md Roteiro e registro do teste de facilidade de uso
│   ├── uso_ia.md            Uso de IA e validação crítica
│   ├── link_video.txt       Link do vídeo no YouTube
│   └── relatorio.pdf        Relatório final (4 a 8 páginas)
├── src/
│   ├── logica.py            Lógica: validação, busca, grafo de temas, respostas e triagem
│   ├── sistema.py           Interface em linha de comando (CLI), comando principal
│   ├── app.py               Interface web opcional (Streamlit)
│   └── testes.py            Executa as perguntas de teste e calcula os indicadores
└── README.md
```

---

## 🧭 Organização da base de conhecimento

A base fica em `data/base.json`. Cada registro tem obrigatoriamente os campos:

| Campo | Conteúdo |
|---|---|
| `id` | Identificador único (por exemplo `G01`) |
| `tema` | Um dos temas: `golpes`, `privacidade`, `contas_senhas`, `servicos_documentos` |
| `palavras_chave` | Lista de expressões que aparecem nas perguntas |
| `orientacao` | Texto resumido e em linguagem simples |
| `referencia` | Fonte consultada, com o endereço |
| `data_verificacao` | Data em que a fonte foi conferida |

**Validação na leitura:** `carregar_base()` em `src/logica.py` verifica se o arquivo existe, se o JSON é válido, se a base não está vazia, se os campos obrigatórios estão preenchidos, se os temas são conhecidos e se os ids não se repetem. Em caso de erro, mostra uma mensagem clara e o programa não tenta responder.

**Como acrescentar ou corrigir registros:** basta editar `data/base.json`. Não é preciso mexer no código. Um novo tema exige apenas incluí-lo em `NOMES_TEMAS` e, se quiser, em `GRAFO_TEMAS`.

**Estruturas utilizadas:**

- **Listas e dicionários** para guardar os registros, as palavras-chave e os resultados dos testes.
- **Grafo simples de temas** (`GRAFO_TEMAS`): cada tema aponta para temas relacionados. Por exemplo, *golpes* se liga a *contas e senhas* e a *privacidade*, porque um golpe costuma envolver senha ou dados pessoais. O grafo é usado para sugerir a continuidade da consulta.

---

## 🔎 Estratégia de busca

1. A pergunta é normalizada: letras minúsculas, sem acentos e sem pontuação.
2. Palavras sem significado (stopwords, como "de", "o", "para") são descartadas.
3. Cada registro recebe uma pontuação:
   - **+2** quando uma expressão de palavra-chave aparece inteira na pergunta (por exemplo, "golpe do pix");
   - **+1** para cada palavra em comum entre a pergunta e as palavras-chave.
4. O registro de maior pontuação é escolhido. Se a pontuação máxima for zero, o sistema informa que não há resposta confiável.
5. **Empate:** se mais de um registro tiver a mesma pontuação máxima, o sistema mostra as opções e o usuário escolhe. Ele não escolhe sozinho entre candidatos empatados.

Consultas por tema filtram a base antes da busca.

---

## 💬 Regras de resposta e estratégias de prompts

O programa não usa IA para gerar texto. As respostas vêm do registro da base, formatadas por dois modelos de instrução documentados em `docs/prompts.md`:

- **Modelo A (completo):** papel do assistente, tema, orientação, fonte, data de verificação e aviso de confirmação. É o modelo padrão.
- **Modelo B (enxuto):** orientação, fonte e aviso em poucas linhas.

Em todas as respostas, valem as mesmas regras:

- a fonte é sempre citada;
- a resposta nunca afirma que a instituição é oficial;
- quando a informação não está na base, o assistente avisa, sugere reformular ou escolher um tema, e não inventa orientação;
- para mensagens suspeitas, o assistente mostra sinais de alerta e não diz com certeza se é golpe.

**Triagem de mensagens (lógica booleana):** o usuário responde quatro perguntas sobre a mensagem (pede dados, cria urgência, tem link, remetente desconhecido). Com as variáveis P, U, L e R, o alerta é dado pela expressão **P · U · (L + R)**. A forma implementada usa De Morgan: `sem_alerta = ¬P + ¬U + (¬L · ¬R)`. A função `tabela_verdade()` verifica as 16 combinações e confirma que as duas formas dão o mesmo resultado.

---

## 🧪 Plano de testes e resultados

**Plano:** 16 perguntas de teste em `data/testes.json`, divididas em:

- **Diretas** (T01 a T04): a pergunta usa as palavras-chave da base.
- **Reformulações** (T05 a T10): a mesma orientação, escrita com outras palavras.
- **Fora da base** (T11 a T13): assuntos que a base não cobre.
- **Casos limite** (T14 a T16): entrada vazia, consulta ambígua e tema sem correspondência.

**Como executar os testes:** `python src/testes.py`. O script compara o resultado obtido com o esperado, mede o tempo de cada consulta e grava `docs/resultados_testes.md`.

**Resultados obtidos na versão entregue:**

| Indicador | Valor |
|---|---|
| Perguntas testadas | 16 |
| Respostas corretas | 13 |
| Taxa de acerto | 81,2% |
| Tempo médio de consulta | 1.005 ms |
| Tabela-verdade da triagem consistente | sim (16 de 16) |

**Erros observados e o que eles mostram:**

- **T04, "quero excluir meus dados":** a palavra "dados" aparece em mais de uma orientação de privacidade, e o sistema pediu que o usuário escolhesse. O esperado era a orientação P02. Isso mostra que a busca por palavras em comum é sensível a palavras genéricas.
- **T10, "wifi de restaurante para acessar o banco":** a pergunta combina "wifi" com "banco", e o sistema encontrou empate entre a orientação sobre Wi-Fi público e a de golpes do Pix. Mostra a limitação de uma busca sem sinônimos e sem pesos por tipo de palavra.
- **T13, "quem ganhou a copa do mundo":** a palavra "ganhou" é uma palavra-chave da orientação sobre prêmios. O sistema respondeu com essa orientação, quando o esperado era dizer que o assunto não está na base. Este é um erro de falsa correspondência, o mais importante para um assistente de orientação.

**Teste de facilidade de uso:** realizado com [número] pessoa(s) de fora do grupo, com roteiro de quatro tarefas em `docs/teste_usabilidade.md`. Resultado: [resumo].

**Interpretação:** a taxa de acerto é boa para perguntas com as palavras da base, mas cai em perguntas com palavras genéricas, e o erro mais grave é a falsa correspondência (T13). A consulta é rápida o suficiente para uso interativo. A avaliação tem limitações: são 16 perguntas, uma base pequena e poucos participantes no teste de uso.

**Melhorias possíveis:**
1. Tratar palavras genéricas com peso menor (por exemplo, "dados" ou "ganhou" valer menos que expressões completas), e não contar palavras isoladas que aparecem em muitos registros.
2. Adicionar um limiar mínimo de pontuação, para que correspondências fracas sejam tratadas como "sem resposta" em vez de respondidas.
3. Incluir um dicionário de sinônimos (por exemplo "conta invadida" e "hackearam") para melhorar as reformulações.

---

## ▶️ Como executar

**Pré-requisito:** Python 3.10 ou superior. Não é preciso instalar bibliotecas nem ter chave de API.

**Interface em linha de comando (caminho principal):**

```bash
git clone [link do repositório]
cd [pasta do projeto]
python src/sistema.py
```

**Testes e indicadores:**

```bash
python src/testes.py
```

**Interface web (opcional):**

```bash
pip install streamlit
streamlit run src/app.py
```

A interface web usa a mesma lógica do CLI. Se ela não funcionar, a avaliação continua válida pelo CLI e pelos testes.

---

## 💡 Exemplos de uso

| Entrada | Resposta do sistema | Fonte |
|---|---|---|
| "golpe do pix" | Orientação G01: bancos não pedem Pix para proteger ou cancelar a conta. | Banco Central do Brasil |
| "como criar uma senha forte" | Orientação C02: senhas longas e diferentes para cada serviço. | Cartilha CERT.br |
| "o que é a LGPD" | Orientação P01: direitos do titular de dados. | Lei 13.709/2018 e ANPD |
| Entrada vazia | "Entrada vazia. Digite uma pergunta ou escolha um tema pelo menu." | — |
| Opção de menu "9" | "Opção inexistente. Escolha um número do menu." | — |
| "qual a previsão do tempo" | "Não encontrei uma orientação confiável para essa pergunta nesta base..." | — |
| "conta" | Mostra as opções G01 e C04 para o usuário escolher. | — |

---

## ⚠️ Cuidados com clareza, acessibilidade, privacidade e informação não oficial

- **Não coleta dados pessoais.** O programa não pede nome, CPF, e-mail ou senha. A triagem pergunta apenas sim ou não sobre a mensagem.
- **Não é canal oficial.** Toda resposta lembra que o assistente não representa órgão público.
- **Fontes à vista.** Cada orientação mostra a referência consultada e a data de verificação.
- **Linguagem simples.** As orientações evitam termos técnicos sem explicação.
- **Acessibilidade.** A interface é texto puro, com menus numerados, o que funciona com leitores de tela e em qualquer terminal. A versão web também usa textos e rótulos claros.
- **Informação pode mudar.** Regras de bancos, leis e serviços mudam. Sempre confirme nos canais oficiais.

---

## 🔗 Links do projeto

- **Vídeo de apresentação (Não Listado):** [link do YouTube]
- **Repositório modelo da coordenação:** https://github.com/equipe1ccon/FIAP-PORTFOLIO-1CCON

---

## 🧠 Decisões técnicas

- **JSON para a base:** é um formato estruturado que o Python lê sem bibliotecas externas, e fica fácil de revisar e corrigir.
- **Busca por palavras-chave, sem IA:** é rápida, previsível e funciona offline. Um modelo de linguagem poderia lidar melhor com reformulações, mas exigiria chave de API, internet e validação extra, e o enunciado não exige isso.
- **Separação entre lógica e interface:** a lógica não usa `input()` nem `print()`. Assim, o CLI, a web e os testes usam o mesmo código, e os indicadores não mudam conforme a interface.
- **Triagem por lógica booleana:** a simplificação por De Morgan mantém o código legível e a equivalência é verificada por tabela-verdade.

---

## 📢 Observações gerais

- **Participação na Competição:** [ ] Sim, aceitamos participar / [ ] Não vamos participar.

---

## 🏁 Conclusões, limitações e possibilidades de melhoria

O CyberCidadão Assist cumpre os requisitos de base, busca, navegação entre temas, tratamento de entradas inválidas, avisos de limitação, lógica booleana, testes automatizados e teste de facilidade de uso. Ele também evita afirmar com certeza que uma mensagem é golpe e não se apresenta como canal oficial.

**Limitações:** a busca depende das palavras da pergunta e tem falsos positivos com palavras genéricas (T13). A base tem 17 registros e ainda precisa de conferência das datas de verificação. O teste de uso envolveu poucas pessoas. As melhorias listadas na seção de testes tratam esses pontos.

---

## 📋 Licença

Conteúdo do modelo FIAP por FIAP, licenciado sob [CC BY 4.0](http://creativecommons.org/licenses/by/4.0/). Trabalho do grupo de autoria de Lisandra Araujo e Eduardo Alves.
