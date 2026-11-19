<p align="center">
  <img src="assets/logo-fiap.png" alt="FIAP - Faculdade de Informática e Administração Paulista" width="200">
</p>

<h1 align="center">CyberCidadão Assist</h1>
<p align="center"><b>Assistente de orientação em segurança digital para o cidadão</b></p>

<p align="center">Global Solution 2026.2 · Desafio CitizenTech · Case Citizen Assist AI</p>

---

## Nome do grupo

Grupo 2

## 👨‍🎓 Integrantes

- Lisandra Jacinto de Araujo (RM: 574055)
- Eduardo Alves da Silva (RM: 568601)

## 👩‍🏫 Professores

### Tutor(a)

- Lucas Gomes Jorge Gonçalez

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
│   ├── fontes_conferidas.md Conferência das referências e datas
│   ├── teste_usabilidade.md Roteiro e resultados do teste de facilidade de uso
│   ├── uso_ia.md            Uso de IA e validação crítica
│   ├── link_video.txt       Link do vídeo no YouTube
│   └── relatorio.pdf        Relatório final do projeto
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

**Como acrescentar ou corrigir registros:** basta editar `data/base.json`. Não é preciso mexer nas regras de pontuação. Um novo tema exige incluí-lo em `NOMES_TEMAS` e em `GRAFO_TEMAS`. As referências consultadas estão também em `docs/fontes_conferidas.md` (conferidas em 19/11/2026).

**Fontes consultadas:**

| Instituição | O que fundamenta | Registros |
|---|---|---|
| Banco Central do Brasil | Golpe do Pix e Mecanismo Especial de Devolução (MED) | G01 |
| CERT.br / NIC.br (Cartilha de Segurança para Internet) | Golpes por ligação, links, prêmios, senhas, dois fatores, Wi-Fi público e atualizações | G02, G03, G05, P03, C01 a C04, S03, S04 |
| Procon-SP | Conferência de boletos | G04 |
| ANPD (Autoridade Nacional de Proteção de Dados) | Direitos do titular, exclusão de dados, vazamentos e princípio da necessidade | P01 a P04, S02 |
| Governo Digital (gov.br) | Conferência de sites governamentais | S01 |

Os endereços completos de cada página estão em `docs/fontes_conferidas.md` e no campo `referencia` de cada registro.

**Estruturas utilizadas:**

- **Listas e dicionários** para guardar os registros, as palavras-chave e os resultados dos testes. A função `indice_por_id()` monta um dicionário `id → registro`, que permite recuperar uma orientação diretamente pelo identificador (por exemplo, digitar `G01`).
- **Hierarquia tema → subtema:** cada tema reúne suas orientações, que funcionam como subtemas (por exemplo, *Golpes e fraudes* → *Golpe do Pix*, *Falsa central*, *Boleto*, *Phishing*, *Prêmio*). O menu por tema percorre essa hierarquia em dois níveis.
- **Grafo simples de temas** (`GRAFO_TEMAS`): cada tema aponta para temas relacionados. Por exemplo, *golpes* se liga a *contas e senhas* e a *privacidade*, porque um golpe costuma envolver senha ou dados pessoais. O grafo é usado para sugerir a continuidade da consulta.

---

## 🔎 Estratégia de busca

1. A pergunta é normalizada: letras minúsculas, sem acentos e sem pontuação. Se o texto for exatamente um identificador da base (por exemplo, `S03`), a orientação é recuperada direto pelo dicionário, sem pontuação.
2. Palavras sem significado (stopwords, como "de", "o", "para") são descartadas.
3. Cada registro recebe uma pontuação:
   - **+2 por palavra relevante** de uma expressão de palavra-chave encontrada inteira na pergunta (por exemplo, "golpe do pix");
   - **+1** para cada palavra relevante em comum entre a pergunta e as palavras-chave.
4. O registro de maior pontuação é escolhido. Se a pontuação for zero ou houver apenas uma coincidência fraca numa pergunta longa (3 ou mais palavras relevantes e pontuação de até 1), o sistema informa que não há resposta confiável.
5. **Empate:** se mais de um registro tiver a mesma pontuação máxima, o sistema mostra as opções e o usuário escolhe. Ele não decide sozinho entre candidatos empatados.

**Comparação das duas formas de recuperação:** a consulta por identificador usa um dicionário e encontra o registro em tempo constante, mas exige que o usuário conheça o código. A busca por pontuação percorre todos os registros e suas palavras-chave (custo proporcional ao tamanho da base), mas aceita frases do dia a dia. Com 17 registros, as duas respondem em cerca de 1 ms; a diferença só seria relevante em bases muito maiores.

As grafias `Wi-Fi`/`wifi` e `e-mail`/`email` são normalizadas da mesma forma. A busca é uma heurística de palavras-chave, não uma análise de intenção ou um modelo de IA.

**Consulta por tema:** a opção 2 do terminal permite escolher um assunto e uma orientação sem digitar uma pergunta. Após ler a resposta, o usuário pode selecionar um dos temas relacionados no grafo e continuar a navegação. A interface web também disponibiliza essa seleção. O filtro por tema na busca textual restringe os registros antes da pontuação.

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

**Mapa de Karnaugh da triagem** (1 = alerta):

| P·U \ L·R | 00 | 01 | 11 | 10 |
|---|:-:|:-:|:-:|:-:|
| **00** | 0 | 0 | 0 | 0 |
| **01** | 0 | 0 | 0 | 0 |
| **11** | 0 | 1 | 1 | 1 |
| **10** | 0 | 0 | 0 | 0 |

Os 1s formam dois agrupamentos de duas células na linha P·U = 11: um com R = 1 (P·U·R) e outro com L = 1 (P·U·L). A expressão mínima é **P·U·L + P·U·R = P·U·(L + R)**, a mesma usada no código.

---

## 🧪 Plano de testes e resultados

**Plano:** 17 perguntas em `data/testes.json`, organizadas em cinco tipos:

- 4 perguntas diretas (T01 a T04);
- 6 reformulações (T05 a T10);
- 3 perguntas fora da base (T11 a T13);
- 3 situações-limite (T14 a T16): entrada vazia, ambiguidade e filtro sem correspondência;
- 1 consulta por identificador (T17).

O script `python src/testes.py` mede o tempo real de cada consulta, compara status e identificador esperados com os retornados, valida a equivalência da tabela-verdade da triagem e compara os dois modelos de instrução nas perguntas com resposta única. O resultado é gravado em `docs/resultados_testes.md` com **resposta esperada, resposta obtida, classificação e tempo**.

**Resultados da execução local de 19/11/2026:**

| Indicador | Resultado |
|---|---|
| Perguntas avaliadas | 17 |
| Consultas corretas neste conjunto | 17 |
| Taxa de acerto observada | **100,0%** |
| Tempo médio observado | cerca de **1 ms** (1,28 ms na execução registrada; varia conforme o computador) |
| Equivalência da triagem | 16 de 16 combinações consistentes |
| Orientações com fonte e data conferidas | 17 de 17 |
| Comparação dos modelos | 11 consultas com resposta única: ambos citaram fonte e aviso |
| Facilidade de uso: tarefas concluídas pelo roteiro | **4 de 4** |
| Facilidade de uso: média de entradas por tarefa | **1,75** (menor caminho) |
| Facilidade de uso: variações de frase resolvidas na tarefa 2 | **5 de 6** (83,3%) |

**Correções realizadas após a avaliação inicial:**

- T04, "quero excluir meus dados": foram adicionadas reformulações sobre exclusão, permitindo selecionar a orientação P02;
- T10, "wifi de restaurante para acessar o banco": foram incluídas expressões compatíveis com Wi-Fi em locais públicos, resultando em S03;
- T13, "quem ganhou a copa do mundo": a palavra solta "ganhou" foi retirada das palavras-chave de golpes com prêmios e evitou a falsa orientação G05.

A avaliação anterior tinha **13/16 (81,2%)**; os resultados atuais são **16/16 (100,0%)** nas mesmas perguntas. A pergunta T17 foi incluída depois, para testar a consulta por identificador. Isso **não garante 100% de precisão** em perguntas desconhecidas: a amostra é pequena e os casos corrigidos pertencem à própria bateria de teste. Novos exemplos devem ser coletados para uma avaliação independente.

**Facilidade de uso:** a avaliação foi feita por **roteiro de tarefas**, executado pela equipe com apoio de IA, sem participante externo (detalhes em `docs/teste_usabilidade.md`). As quatro tarefas foram concluídas, com 1,75 entrada em média pelo menor caminho. Cinco de seis frases do dia a dia para a mesma dúvida levaram direto à orientação certa; a sexta ("golpe por ligacao") gerou um empate que incluía uma opção sem relação (prêmio). A principal dificuldade foi o nome de alguns itens do menu por tema, como "Falsa central", que não descreve a situação do cidadão. Como a equipe conhece o sistema, esse resultado tende a ser otimista.

**Interpretação e melhorias:** a busca por palavras-chave é rápida e reproduzível, mas depende de termos cadastrados. Recomenda-se (1) ampliar as paráfrases e sinônimos validados com consultas reais; (2) criar um campo `titulo` descritivo para os itens do menu por tema; (3) realizar testes com perguntas inéditas e usuários externos; (4) atualizar periodicamente a base documental. Os limites da avaliação e os tempos individuais estão em `docs/resultados_testes.md`.

---

## ▶️ Como executar

**Pré-requisito:** Python 3.10 ou superior. Não é preciso instalar bibliotecas nem ter chave de API.

**Interface em linha de comando (caminho principal):**

```bash
git clone https://github.com/lisjdearaujo/1CCOA-GLOBAL-SOLUTION-2.git
cd 1CCOA-GLOBAL-SOLUTION-2
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
| "golpe do pix" | Orientação G01: interromper contato suspeito e, se houve perda, contestar no banco pelo MED. | Banco Central do Brasil |
| "como criar uma senha forte" | Orientação C02: senhas longas e diferentes para cada serviço. | Cartilha CERT.br |
| "o que é a LGPD" | Orientação P01: direitos do titular de dados com os limites legais. | ANPD |
| Entrada vazia | "Entrada vazia. Digite uma pergunta ou escolha um tema pelo menu." | — |
| Opção de menu "9" | "Opção inexistente. Escolha um número do menu." | — |
| "qual a previsão do tempo" | "Não encontrei uma orientação confiável para essa pergunta nesta base..." | — |
| "G01" | Orientação G01, recuperada diretamente pelo identificador. | Banco Central do Brasil |
| "conta" | Mostra as orientações empatadas para o usuário escolher, com fonte após a escolha. | Conforme a opção selecionada |

---

## ⚠️ Cuidados com clareza, acessibilidade, privacidade e informação não oficial

- **Não solicita nem armazena dados pessoais.** O programa não pede nome, CPF, e-mail ou senha. O campo de pergunta é livre, por isso recomendamos não inserir informações pessoais nele. A triagem pergunta apenas sim ou não sobre sinais da mensagem.
- **Não é canal oficial.** Toda resposta lembra que o assistente não representa órgão público.
- **Fontes à vista.** Cada orientação mostra a referência consultada e a data de verificação.
- **Linguagem simples.** As orientações evitam termos técnicos sem explicação.
- **Acessibilidade.** A CLI usa textos e menus numerados, que podem facilitar o uso em leitores de tela compatíveis com o terminal. A web utiliza rótulos textuais. Ainda faltam testes formais de acessibilidade.
- **Informação pode mudar.** Regras de bancos, leis e serviços mudam. Sempre confirme nos canais oficiais.

---

## 🔗 Links do projeto

- **Vídeo de apresentação (YouTube, Não Listado):** [link do vídeo]
- **Relatório final:** [`docs/relatorio.pdf`](docs/relatorio.pdf)

---

## 🧠 Decisões técnicas

- **JSON para a base:** é um formato estruturado que o Python lê sem bibliotecas externas, e fica fácil de revisar e corrigir.
- **Busca por palavras-chave, sem IA:** é rápida, previsível e funciona offline. Um modelo de linguagem poderia lidar melhor com reformulações, mas exigiria chave de API, internet e validação extra, e o enunciado não exige isso.
- **Separação entre lógica e interface:** a lógica não usa `input()` nem `print()`. Assim, o CLI, a web e os testes usam o mesmo código, e os indicadores não mudam conforme a interface.
- **Triagem por lógica booleana:** a expressão foi minimizada por mapa de Karnaugh, a forma implementada usa De Morgan e a equivalência é verificada por tabela-verdade.

---

## 📢 Observações gerais

- **Participação na Competição:** [] Sim, aceitamos participar / [X] Não vamos participar.

---

## 🏁 Conclusões, limitações e possibilidades de melhoria

O CyberCidadão Assist implementa base, busca, navegação entre temas, tratamento de entradas inválidas, avisos de limitação, lógica booleana e testes automatizados. A facilidade de uso foi avaliada por roteiro de tarefas. O assistente também evita afirmar com certeza que uma mensagem é golpe e não se apresenta como canal oficial.

**Limitações:** a busca depende de palavras cadastradas e pode produzir falsas correspondências em novas consultas, mesmo com T13 corrigido. A base contém 17 registros documentados em 19/11/2026 e exigirá revisão periódica. A avaliação de facilidade de uso foi feita pela própria equipe, sem participante externo, e deve ser repetida com pessoas de fora. As melhorias estão na seção de testes.

---

## 📋 Licença

Conteúdo do modelo FIAP por FIAP, licenciado sob [CC BY 4.0](http://creativecommons.org/licenses/by/4.0/). Trabalho do grupo de autoria de Lisandra Araujo e Eduardo Alves.
