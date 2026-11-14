# Uso de inteligência artificial

## Ferramentas utilizadas

- [preencher: nome da ferramenta, por exemplo Claude, ChatGPT ou outra, e a versão usada]

## Onde a IA foi usada

- **Apoio à escrita dos modelos de instrução de resposta** (`docs/prompts.md`).
- **Revisão de clareza** das orientações da base.
- **Sugestões de perguntas de teste**, incluindo reformulações e casos fora da base.
- **Revisão de textos** do README e do relatório.

## Onde a IA não foi usada

- O programa (`src/sistema.py`, `src/logica.py`, `src/app.py`) não chama nenhum modelo de IA e não usa API. As respostas vêm exclusivamente de `data/base.json`.
- A base de orientações não foi gerada por IA. Cada registro foi escrito pela equipe a partir de uma fonte identificada.

## Validação crítica

Toda sugestão da IA passou por conferência antes de entrar no projeto:

- **Fatos e datas:** cada orientação da base foi conferida na referência indicada, e a data de verificação corresponde à consulta real da fonte. Sugestões da IA que não puderam ser confirmadas na fonte oficial foram descartadas.
- **Órgãos e leis:** nomes de órgãos, leis e números de artigos foram conferidos nos sites oficiais, porque a IA pode errar esses detalhes.
- **Perguntas de teste:** as perguntas sugeridas foram revisadas para evitar casos que o próprio grupo já sabia que funcionariam.
- **Textos:** trechos revisados foram reescritos pela equipe quando a IA deixava a linguagem técnica demais ou prometia mais do que o sistema faz (por exemplo, afirmar que uma mensagem "é golpe" com certeza).

## Prompts testados

| Data | Objetivo | Resultado | Decisão da equipe |
|---|---|---|---|
| [data] | [por exemplo: pedir revisão de clareza de uma orientação] | [o que a IA respondeu] | [o que foi mantido, alterado ou descartado, e por quê] |
| [data] | [sugerir reformulações de perguntas de teste] | [resultado] | [decisão] |

## Limitações do uso de IA

A IA pode gerar informações incorretas ou desatualizadas. Por isso, a fonte final de todas as orientações é a referência oficial indicada em cada registro, e não a resposta da IA.
