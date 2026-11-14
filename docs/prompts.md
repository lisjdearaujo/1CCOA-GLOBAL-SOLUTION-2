# Modelos de instrução de resposta (fase 5)

O CyberCidadão Assist não gera texto com IA. A resposta é montada a partir do registro da base. Por isso, os "prompts" deste projeto são **modelos de instrução de resposta**: definem o papel do assistente, o formato e a obrigação de citar a fonte. Eles são implementados em `formatar_resposta()` em `src/logica.py`.

## Modelo A: completo

**Papel:** orientar sobre segurança digital, sem se apresentar como canal oficial.

**Instrução:**
1. Abrir com a ressalva de que não é canal oficial.
2. Mostrar tema, orientação, fonte consultada e data de verificação.
3. Terminar com um aviso para confirmar no canal oficial.
4. Nunca afirmar com certeza que uma mensagem é golpe ou segura.

**Exemplo de saída:**

```
Orientação de segurança digital (não é canal oficial de nenhum órgão).
Tema: Golpes e fraudes
Orientação: Bancos não pedem Pix ou transferência para proteger, cancelar ou desbloquear sua conta...
Fonte consultada: Banco Central do Brasil, orientações sobre golpes (https://www.bcb.gov.br)
Data de verificação: [data real da consulta à fonte]
Aviso: confirme sempre as informações atualizadas no canal oficial da instituição.
```

## Modelo B: enxuto

**Papel:** o mesmo, com menos texto.

**Instrução:** orientação, fonte e data em uma linha, seguidas de um aviso curto.

**Exemplo de saída:**

```
Bancos não pedem Pix ou transferência para proteger, cancelar ou desbloquear sua conta...
Fonte: Banco Central do Brasil, orientações sobre golpes (https://www.bcb.gov.br) (verificado em [data real]).
Confirme requisitos atualizados no canal oficial.
```

## Comparação

Os dois modelos foram aplicados às mesmas orientações da base. O script `src/testes.py` mede o tamanho médio das respostas e se a fonte aparece em cada uma. Os números ficam em `docs/resultados_testes.md`.

**Critérios de comparação:** clareza (a orientação aparece antes dos detalhes), consistência (a fonte e o aviso aparecem sempre) e tamanho (quantas palavras o usuário precisa ler).

**Conclusão:** [preencher após a execução dos testes. Sugestão de análise: o modelo A é mais longo, mas deixa explícitos a fonte, a data e a ressalva de que não é canal oficial. O modelo B é mais curto e cumpre a obrigação de citar a fonte, mas a ressalva fica mais fraca. Escolher e justificar o modelo usado como padrão.]
