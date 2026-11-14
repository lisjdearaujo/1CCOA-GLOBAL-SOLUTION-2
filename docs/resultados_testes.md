# Resultados dos testes

Gerado automaticamente por `src/testes.py`.

## Indicadores

- Perguntas testadas: 16
- Respostas corretas: 13
- Taxa de acerto: 81.2%
- Tempo médio de consulta: 1.005 ms
- Tabela-verdade da triagem consistente: sim
- Registros da base: 17 (com data de verificação pendente: 17)

## Perguntas de teste

| ID | Tipo | Pergunta | Esperado | Obtido | Resultado | Tempo (ms) |
|---|---|---|---|---|---|---|
| T01 | direta | golpe do pix | G01 | G01 | acerto | 1.033 |
| T02 | direta | como criar uma senha forte | C02 | C02 | acerto | 1.133 |
| T03 | direta | o que é a LGPD | P01 | P01 | acerto | 1.106 |
| T04 | direta | quero excluir meus dados | P02 | ambiguo | erro | 1.019 |
| T05 | reformulacao | me roubaram dinheiro pelo pix, o que faço | G01 | G01 | acerto | 1.156 |
| T06 | reformulacao | ligaram dizendo ser do banco e pediram o token | G02 | G02 | acerto | 1.252 |
| T07 | reformulacao | recebi um email estranho com um link | G03 | G03 | acerto | 1.191 |
| T08 | reformulacao | perdi acesso à minha conta do Instagram | C04 | C04 | acerto | 1.261 |
| T09 | reformulacao | como confirmo que um site é do governo | S01 | S01 | acerto | 1.190 |
| T10 | reformulacao | posso usar wifi de restaurante para acessar o banco | S03 | ambiguo | erro | 1.334 |
| T11 | fora_da_base | qual a previsão do tempo para amanhã | sem_resposta | sem_resposta | acerto | 1.199 |
| T12 | fora_da_base | como fazer um bolo de chocolate | sem_resposta | sem_resposta | acerto | 1.101 |
| T13 | fora_da_base | quem ganhou a copa do mundo | sem_resposta | G05 | erro | 1.063 |
| T14 | limite_entrada_vazia | (vazia) | vazio | vazio | acerto | 0.001 |
| T15 | limite_ambiguidade | conta | ambiguo | ambiguo | acerto | 0.809 |
| T16 | limite_tema_sem_correspondencia | golpe do pix | sem_resposta | sem_resposta | acerto | 0.230 |

## Comparação dos modelos de resposta

- Modelo A (completo): média de 64.6 palavras, com campo de fonte em 17 de 17 orientações.
- Modelo B (enxuto): média de 41.6 palavras, com fonte em 17 de 17 orientações.
