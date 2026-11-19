# Uso de inteligência artificial

## Ferramentas utilizadas

- **Claude**, da Anthropic, pelo aplicativo claude.ai. Na revisão final (19/11/2026), foi usado o modelo Claude Opus 5.5.

Nenhuma outra ferramenta de IA foi usada no projeto.

## Onde a IA foi usada

- **Apoio à escrita dos modelos de instrução de resposta** (`docs/prompts.md`).
- **Revisão de clareza** das orientações da base.
- **Sugestões de perguntas de teste**, incluindo reformulações e casos fora da base.
- **Revisão de textos** do README e da documentação.
- **Conferência final do projeto contra os requisitos do enunciado**, apontando itens pendentes.
- **Execução do roteiro de facilidade de uso** (`docs/teste_usabilidade.md`): a IA executou as tarefas no programa, testou variações de frases e registrou as dificuldades observadas.

## Onde a IA não foi usada

- O programa (`src/sistema.py`, `src/logica.py`, `src/app.py`) não chama nenhum modelo de IA e não usa API. As respostas vêm exclusivamente de `data/base.json`.
- A base de orientações não foi gerada por IA. Cada registro foi escrito pela equipe a partir de uma fonte identificada.
- A IA **não substituiu um participante externo** no teste de facilidade de uso. O registro informa que a avaliação foi feita por roteiro, pela equipe, e que ainda falta um teste com uma pessoa de fora.

## Validação crítica

Toda sugestão da IA passou por conferência antes de entrar no projeto:

- **Fatos e datas:** cada orientação da base foi conferida na referência indicada, e a data de verificação corresponde à consulta real da fonte. Sugestões da IA que não puderam ser confirmadas na fonte oficial foram descartadas.
- **Órgãos e leis:** nomes de órgãos, leis e números de artigos foram conferidos nos sites oficiais, porque a IA pode errar esses detalhes.
- **Perguntas de teste:** as perguntas sugeridas foram revisadas para evitar casos que o próprio grupo já sabia que funcionariam.
- **Textos:** trechos revisados foram reescritos pela equipe quando a IA deixava a linguagem técnica demais ou prometia mais do que o sistema faz (por exemplo, afirmar que uma mensagem "é golpe" com certeza).
- **Resultados de testes:** os números do README e de `docs/resultados_testes.md` vêm da execução de `python src/testes.py`, e não de valores informados pela IA.

## Prompts testados

| Data | Objetivo | Resultado | Decisão da equipe |
|---|---|---|---|
| nov/2026 | Pedir dois formatos de resposta que sempre citassem a fonte e não se apresentassem como canal oficial | Sugestão de um formato completo e de um formato curto | Mantidos como modelos A e B; o grupo escolheu o A como padrão após a comparação em `docs/prompts.md` |
| nov/2026 | Sugerir reformulações e perguntas fora da base para a bateria de testes | Lista de frases do dia a dia e de perguntas sem relação com o tema | Selecionadas as que testavam casos diferentes; resultado em `data/testes.json` |
| nov/2026 | Revisar a clareza das orientações e do README | Sugestões de frases mais curtas e de troca de termos técnicos | Aceitas quando não mudavam o sentido da fonte; recusadas quando prometiam mais do que o sistema faz |
| 19/11/2026 | Verificar se o projeto atendia a todos os requisitos do enunciado | Lista de pendências: RMs, link do vídeo, teste de facilidade de uso e este arquivo | Pendências corrigidas nesta versão; o link do vídeo é incluído após a publicação |
| 19/11/2026 | Pedir à IA um teste de usabilidade com respostas fictícias de um participante | A IA recusou inventar um participante e propôs uma avaliação por roteiro de tarefas, com resultados reais do programa | Aceita a avaliação por roteiro, registrada como feita pela equipe, sem participante externo |

## Limitações do uso de IA

A IA pode gerar informações incorretas ou desatualizadas. Por isso, a fonte final de todas as orientações é a referência oficial indicada em cada registro, e não a resposta da IA. A avaliação por roteiro feita com apoio de IA também não reproduz as dificuldades de uma pessoa real usando o sistema pela primeira vez.
