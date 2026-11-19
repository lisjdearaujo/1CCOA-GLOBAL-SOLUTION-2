# Modelos de instrução de resposta (fase 5)

O CyberCidadão Assist **não chama modelo generativo nem API**. Neste projeto, "prompt" significa um **modelo determinístico de instruções para apresentar a orientação** que foi selecionada em `data/base.json`. O código está em `formatar_resposta()` em `src/logica.py`, usado pelo CLI e pelo Streamlit.

Os dois modelos usam o **mesmo registro** da base e não acrescentam recomendações geradas. A decisão de qual orientação usar é feita antes, pelo algoritmo de busca. Nenhum modelo afirma que mensagens suspeitas são golpes com certeza.

## Modelo A — completo (padrão)

**Papel:** orientar cidadãos sobre segurança digital sem se apresentar como órgão ou instituição oficial.

**Instruções:**

1. Informar explicitamente que o assistente não é canal oficial.
2. Exibir, em linhas separadas, tema, orientação, referência e data de verificação.
3. Terminar com aviso para conferir exigências atualizadas na instituição oficial.
4. Nunca transformar um indício em diagnóstico definitivo de fraude.

**Exemplo — consulta "golpe do pix":**

```text
Orientação de segurança digital (não é canal oficial de nenhum órgão).
Tema: Golpes e fraudes
Orientação: Se alguém pedir um Pix para proteger ou desbloquear sua conta, interrompa o contato e confirme pelo canal oficial do banco. Se já enviou um Pix após um golpe, contate seu banco imediatamente para contestar a operação pelo Mecanismo Especial de Devolução (MED). A recuperação do valor não é garantida.
Fonte consultada: Banco Central, orientação a vítimas de golpe por Pix (https://www.bcb.gov.br/meubc/faqs/p/vitima-fez-um-pix-e-caiu-em-um-golpe)
Data de verificação: 2026-11-19
Aviso: confirme sempre as informações atualizadas no canal oficial da instituição.
```

## Modelo B — enxuto

**Papel:** o mesmo do modelo A, priorizando concisão.

**Instruções:**

1. Mostrar a orientação sem título ou aviso inicial.
2. Mostrar fonte e data na mesma linha.
3. Encerrar com um aviso curto para verificar no canal oficial.

**Exemplo — mesma consulta:**

```text
Se alguém pedir um Pix para proteger ou desbloquear sua conta, interrompa o contato e confirme pelo canal oficial do banco. Se já enviou um Pix após um golpe, contate seu banco imediatamente para contestar a operação pelo Mecanismo Especial de Devolução (MED). A recuperação do valor não é garantida.
Fonte: Banco Central, orientação a vítimas de golpe por Pix (https://www.bcb.gov.br/meubc/faqs/p/vitima-fez-um-pix-e-caiu-em-um-golpe) (verificado em 2026-11-19).
Confirme requisitos atualizados no canal oficial.
```

## Comparação aplicada às perguntas de teste

A função `comparar_modelos()` em `src/testes.py` executa os dois formatos sobre as **10 consultas** de `data/testes.json` cujo resultado foi uma orientação única. São as mesmas consultas e os mesmos registros para A e B. O script contabiliza palavras e presença da fonte/aviso, mas **não mede compreensão humana**.

| Critério | Modelo A | Modelo B |
|---|---:|---:|
| Consultas formatadas | 10 | 10 |
| Média de palavras por resposta | 75,2 | 52,2 |
| Respostas com fonte | 10/10 | 10/10 |
| Respostas com aviso de canal oficial | 10/10 | 10/10 |
| Identifica explicitamente o papel não oficial | Sim, na abertura | Não, apenas recomenda confirmar |
| Separa tema e data em linhas próprias | Sim | Não |

**Conclusão:** o grupo adotou o **modelo A como padrão**, porque ele explicita melhor o papel do assistente, separa a data e a origem da orientação e facilita verificar se o conteúdo ainda é aplicável. O modelo B é útil para situações em que a resposta precisa ser curta, mas oferece menos contexto. Esta conclusão se refere à **consistência do formato**; o teste de facilidade de uso com uma pessoa deve ser registrado separadamente em `docs/teste_usabilidade.md`.

Para reproduzir os valores, execute `python src/testes.py`. Os números de palavras podem mudar se a equipe atualizar a redação dos registros.
