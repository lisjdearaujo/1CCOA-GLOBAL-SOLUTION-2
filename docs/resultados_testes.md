# Resultados dos testes

Arquivo gerado automaticamente por `python src/testes.py`.
Os tempos são medições locais desta execução e variam por computador. Não são latências de rede.

## Indicadores

- Consultas avaliadas: **17**
- Consultas com resultado esperado: **17**
- Taxa de acerto neste conjunto fixo: **100.0%**
- Tempo médio de busca: **1.283 ms**
- Menor/maior tempo: 0.005 / 1.972 ms
- Equivalência booleana da triagem: **16/16 combinações**
- Base: **17 orientações**; datas pendentes: **0**

**Interpretação:** a porcentagem indica apenas o desempenho nessas perguntas, não a exatidão em qualquer pergunta real. Status 'sem_resposta', 'ambiguo' e 'vazio' podem ser acertos quando são os comportamentos esperados.

## Consultas e classificações

| ID | Tipo | Pergunta | Esperado (status / ID) | Obtido (status / ID) | Classificação | Tempo (ms) |
|---|---|---|---|---|---|---|
| T01 | direta | golpe do pix | ok / G01 | ok / G01 | acerto | 1.493 |
| T02 | direta | como criar uma senha forte | ok / C02 | ok / C02 | acerto | 1.618 |
| T03 | direta | o que é a LGPD | ok / P01 | ok / P01 | acerto | 1.972 |
| T04 | direta | quero excluir meus dados | ok / P02 | ok / P02 | acerto | 1.842 |
| T05 | reformulacao | me roubaram dinheiro pelo pix, o que faço | ok / G01 | ok / G01 | acerto | 1.612 |
| T06 | reformulacao | ligaram dizendo ser do banco e pediram o token | ok / G02 | ok / G02 | acerto | 1.591 |
| T07 | reformulacao | recebi um email estranho com um link | ok / G03 | ok / G03 | acerto | 1.381 |
| T08 | reformulacao | perdi acesso à minha conta do Instagram | ok / C04 | ok / C04 | acerto | 1.527 |
| T09 | reformulacao | como confirmo que um site é do governo | ok / S01 | ok / S01 | acerto | 1.651 |
| T10 | reformulacao | posso usar wifi de restaurante para acessar o banco | ok / S03 | ok / S03 | acerto | 1.536 |
| T11 | fora_da_base | qual a previsão do tempo para amanhã | sem_resposta / — | sem_resposta / — | acerto | 1.333 |
| T12 | fora_da_base | como fazer um bolo de chocolate | sem_resposta / — | sem_resposta / — | acerto | 1.310 |
| T13 | fora_da_base | quem ganhou a copa do mundo | sem_resposta / — | sem_resposta / — | acerto | 1.288 |
| T14 | limite_entrada_vazia | (vazia) | vazio / — | vazio / — | acerto | 0.005 |
| T15 | limite_ambiguidade | conta | ambiguo / — | ambiguo / — | acerto | 1.186 |
| T16 | limite_tema_sem_correspondencia | golpe do pix | sem_resposta / — | sem_resposta / — | acerto | 0.447 |
| T17 | consulta_por_identificador | s03 | ok / S03 | ok / S03 | acerto | 0.013 |

## Orientações esperadas e retornadas

### T01 — golpe do pix
- **Esperado:** ok / G01. Se alguém pedir um Pix para proteger ou desbloquear sua conta, interrompa o contato e confirme pelo canal oficial do banco. Se já enviou um Pix após um golpe, contate seu banco imediatamente para contestar a operação pelo Mecanismo Especial de Devolução (MED). A recuperação do valor não é garantida.
- **Obtido:** ok / G01. Se alguém pedir um Pix para proteger ou desbloquear sua conta, interrompa o contato e confirme pelo canal oficial do banco. Se já enviou um Pix após um golpe, contate seu banco imediatamente para contestar a operação pelo Mecanismo Especial de Devolução (MED). A recuperação do valor não é garantida.
- **Resultado:** acerto.

### T02 — como criar uma senha forte
- **Esperado:** ok / C02. Use senhas longas e diferentes para cada serviço. Frases longas são uma boa opção. Não reutilize a senha do e-mail em outros sites.
- **Obtido:** ok / C02. Use senhas longas e diferentes para cada serviço. Frases longas são uma boa opção. Não reutilize a senha do e-mail em outros sites.
- **Resultado:** acerto.

### T03 — o que é a LGPD
- **Esperado:** ok / P01. A LGPD prevê direitos como confirmar e acessar dados pessoais, corrigir informações e, nas hipóteses previstas na lei, solicitar anonimização ou eliminação. O exercício desses direitos depende da situação e das bases legais envolvidas.
- **Obtido:** ok / P01. A LGPD prevê direitos como confirmar e acessar dados pessoais, corrigir informações e, nas hipóteses previstas na lei, solicitar anonimização ou eliminação. O exercício desses direitos depende da situação e das bases legais envolvidas.
- **Resultado:** acerto.

### T04 — quero excluir meus dados
- **Esperado:** ok / P02. Para solicitar exclusão de dados, procure o canal de privacidade da organização e guarde o protocolo. O direito à eliminação depende das hipóteses previstas na LGPD e pode ter exceções legais. Se não houver atendimento adequado, consulte a ANPD sobre como apresentar uma petição de titular.
- **Obtido:** ok / P02. Para solicitar exclusão de dados, procure o canal de privacidade da organização e guarde o protocolo. O direito à eliminação depende das hipóteses previstas na LGPD e pode ter exceções legais. Se não houver atendimento adequado, consulte a ANPD sobre como apresentar uma petição de titular.
- **Resultado:** acerto.

### T05 — me roubaram dinheiro pelo pix, o que faço
- **Esperado:** ok / G01. Se alguém pedir um Pix para proteger ou desbloquear sua conta, interrompa o contato e confirme pelo canal oficial do banco. Se já enviou um Pix após um golpe, contate seu banco imediatamente para contestar a operação pelo Mecanismo Especial de Devolução (MED). A recuperação do valor não é garantida.
- **Obtido:** ok / G01. Se alguém pedir um Pix para proteger ou desbloquear sua conta, interrompa o contato e confirme pelo canal oficial do banco. Se já enviou um Pix após um golpe, contate seu banco imediatamente para contestar a operação pelo Mecanismo Especial de Devolução (MED). A recuperação do valor não é garantida.
- **Resultado:** acerto.

### T06 — ligaram dizendo ser do banco e pediram o token
- **Esperado:** ok / G02. Não informe senhas, tokens ou códigos recebidos por SMS durante ligações. Encerre a chamada e contate a instituição pelo canal oficial.
- **Obtido:** ok / G02. Não informe senhas, tokens ou códigos recebidos por SMS durante ligações. Encerre a chamada e contate a instituição pelo canal oficial.
- **Resultado:** acerto.

### T07 — recebi um email estranho com um link
- **Esperado:** ok / G03. Antes de clicar em um link recebido por e-mail ou SMS, confira o remetente e o endereço. Em caso de dúvida, digite o endereço do site diretamente no navegador.
- **Obtido:** ok / G03. Antes de clicar em um link recebido por e-mail ou SMS, confira o remetente e o endereço. Em caso de dúvida, digite o endereço do site diretamente no navegador.
- **Resultado:** acerto.

### T08 — perdi acesso à minha conta do Instagram
- **Esperado:** ok / C04. Use a recuperação oficial do serviço, troque a senha, encerre sessões em outros aparelhos e avise seus contatos sobre mensagens suspeitas enviadas em seu nome.
- **Obtido:** ok / C04. Use a recuperação oficial do serviço, troque a senha, encerre sessões em outros aparelhos e avise seus contatos sobre mensagens suspeitas enviadas em seu nome.
- **Resultado:** acerto.

### T09 — como confirmo que um site é do governo
- **Esperado:** ok / S01. O portal gov.br reúne serviços e informações do Governo Federal. Para conferir um serviço, entre pelo portal ou pelo site oficial do órgão e examine o domínio e o destino dos links. Desconfie de endereços parecidos e cobranças inesperadas.
- **Obtido:** ok / S01. O portal gov.br reúne serviços e informações do Governo Federal. Para conferir um serviço, entre pelo portal ou pelo site oficial do órgão e examine o domínio e o destino dos links. Desconfie de endereços parecidos e cobranças inesperadas.
- **Resultado:** acerto.

### T10 — posso usar wifi de restaurante para acessar o banco
- **Esperado:** ok / S03. Evite acessar o banco ou enviar documentos em redes Wi-Fi públicas. Prefira os dados móveis ou uma rede de confiança.
- **Obtido:** ok / S03. Evite acessar o banco ou enviar documentos em redes Wi-Fi públicas. Prefira os dados móveis ou uma rede de confiança.
- **Resultado:** acerto.

### T11 — qual a previsão do tempo para amanhã
- **Esperado:** sem_resposta / —. Não aplicável
- **Obtido:** sem_resposta / —. Não encontrei uma orientação confiável para essa pergunta nesta base. Tente reformular ou escolha um tema: Golpes e fraudes, Privacidade e LGPD, Contas e senhas, Serviços e documentos.
- **Resultado:** acerto.

### T12 — como fazer um bolo de chocolate
- **Esperado:** sem_resposta / —. Não aplicável
- **Obtido:** sem_resposta / —. Não encontrei uma orientação confiável para essa pergunta nesta base. Tente reformular ou escolha um tema: Golpes e fraudes, Privacidade e LGPD, Contas e senhas, Serviços e documentos.
- **Resultado:** acerto.

### T13 — quem ganhou a copa do mundo
- **Esperado:** sem_resposta / —. Não aplicável
- **Obtido:** sem_resposta / —. Não encontrei uma orientação confiável para essa pergunta nesta base. Tente reformular ou escolha um tema: Golpes e fraudes, Privacidade e LGPD, Contas e senhas, Serviços e documentos.
- **Resultado:** acerto.

### T14 — (vazia)
- **Esperado:** vazio / —. Não aplicável
- **Obtido:** vazio / —. Entrada vazia
- **Resultado:** acerto.

### T15 — conta
- **Esperado:** ambiguo / —. Não aplicável
- **Obtido:** ambiguo / —. Seleção do usuário necessária
- **Resultado:** acerto.

### T16 — golpe do pix
- **Esperado:** sem_resposta / —. Não aplicável
- **Obtido:** sem_resposta / —. Não encontrei uma orientação confiável para essa pergunta nesta base. Tente reformular ou escolha um tema: Golpes e fraudes, Privacidade e LGPD, Contas e senhas, Serviços e documentos.
- **Resultado:** acerto.

### T17 — s03
- **Esperado:** ok / S03. Evite acessar o banco ou enviar documentos em redes Wi-Fi públicas. Prefira os dados móveis ou uma rede de confiança.
- **Obtido:** ok / S03. Evite acessar o banco ou enviar documentos em redes Wi-Fi públicas. Prefira os dados móveis ou uma rede de confiança.
- **Resultado:** acerto.

## Comparação dos modelos em perguntas de teste

Os dois formatos foram aplicados às mesmas **11 consultas** que encontraram uma única orientação (incluindo suas reformulações).

| Indicador | Modelo A (completo) | Modelo B (enxuto) |
|---|---:|---:|
| Palavras por resposta (média) | 74.1 | 51.1 |
| Fonte exibida | 11/11 | 11/11 |
| Aviso de confirmação | 11/11 | 11/11 |

**Escolha:** modelo A como padrão. Apesar de mais longo, separa tema, orientação, referência, data e limite de atuação. O modelo B é mais curto, mas apresenta menos contexto para conferir a origem da informação.

## Limitações e melhorias

- A base tem somente 17 orientações; reformulações diferentes das testadas podem falhar.
- As palavras-chave e o limiar de correspondência são regras manuais, não análise semântica.
- Melhorias propostas: ampliar paráfrases e sinônimos revisados; testar perguntas reais de outras pessoas e registrar erros novos; revisar periodicamente as referências.
- **Teste de facilidade de uso:** não é inferido destes testes automatizados. A avaliação por roteiro de tarefas está registrada em `docs/teste_usabilidade.md`.
