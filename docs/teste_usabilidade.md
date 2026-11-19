# Teste de facilidade de uso

## Formato da avaliação

- **Tipo:** avaliação por **roteiro de tarefas**, uma das formas previstas no enunciado ("pelo menos um usuário de teste ou roteiro de tarefas").
- **Quem executou:** a própria equipe, com apoio de IA (ver `docs/uso_ia.md`). **Não houve participante externo.**
- **Data:** 19/11/2026.
- **Interface avaliada:** CLI (`python src/sistema.py`), que é o caminho principal de execução.
- **Como foi feito:** cada tarefa foi executada no programa como um cidadão sem conhecimento técnico faria, usando frases do dia a dia em vez dos termos cadastrados na base. Foram contadas as entradas necessárias (números do menu e perguntas digitadas) e medido o tempo de resposta da busca com `time.perf_counter()`.

Como a equipe conhece o sistema, os resultados mostram se o fluxo funciona e onde há obstáculos visíveis. Eles **não substituem** um teste com uma pessoa de fora, que pode ter dificuldades que a equipe não percebe.

## Roteiro de tarefas

1. **Tarefa 1:** Descubra quais temas estão disponíveis no programa.
2. **Tarefa 2:** Encontre uma orientação sobre o que fazer se alguém pedir o seu Pix ou um código por ligação.
3. **Tarefa 3:** A partir da orientação anterior, abra um tema relacionado que o programa sugeriu.
4. **Tarefa 4:** Faça uma pergunta que a base não cobre (por exemplo, sobre o tempo) e observe a resposta.

## Registro

| Tarefa | Concluída pelo roteiro? | Entradas necessárias | Tempo de resposta do programa | Dificuldade observada |
|---|---|---|---|---|
| 1 | Sim | 1 (opção `1`) | imediato (não há busca) | A opção 1 apenas lista os temas. Para abrir um deles, é preciso voltar ao menu e escolher a opção 2. |
| 2 | Sim | 2 pela pergunta (opção `3` + frase) ou 3 pelo menu (`2` > tema > orientação) | cerca de 1 a 3 ms por busca | Pelo menu, o item se chama "Falsa central". Quem procura "ligação" ou "código" pode não reconhecer o nome. |
| 3 | Sim | 2 (tema relacionado + orientação) | imediato (não há busca) | Os temas relacionados aparecem logo abaixo da resposta, com números. Não houve obstáculo. |
| 4 | Sim | 2 (opção `3` + frase) | menos de 1 ms | O aviso de limite aparece e lista os temas, mas não leva direto a eles. É preciso voltar ao menu. |

### Variações de linguagem na tarefa 2

Para verificar se a tarefa 2 funciona com frases diferentes, a equipe digitou seis formas de perguntar a mesma coisa:

| Frase digitada | Resultado |
|---|---|
| "alguem me ligou pedindo um codigo" | Orientação G02 (falsa central) |
| "ligacao pedindo codigo do banco" | Orientação G02 |
| "o banco ligou e pediu o codigo que chegou por sms" | Orientação G02 |
| "me ligaram pedindo o pix" | Orientação G01 (golpe do Pix) |
| "pediram meu pix por telefone" | Orientação G01 |
| "golpe por ligacao" | Três opções empatadas: G01, G02 e **G05 (prêmio)** |

Cinco das seis frases levaram direto a uma orientação adequada. Na sexta, o sistema pediu que a pessoa escolhesse entre três opções. O comportamento é seguro, porque ele não decide sozinho, mas a opção sobre prêmio não tem relação com ligações e pode confundir.

## Observações da equipe

- Os rótulos da navegação por tema vêm da primeira palavra-chave de cada registro. Alguns ficam pouco claros para quem não conhece a base, como "Cpf", "Lgpd" e "Atualizar".
- Opções inválidas (letra, número fora da lista ou entrada vazia) geram mensagens compreensíveis e o programa não fecha.
- Toda resposta mostra a fonte, a data de verificação e o aviso de que o assistente não é canal oficial.

## Resumo

- **Tarefas concluídas pelo roteiro:** 4 de 4.
- **Média de entradas por tarefa (menor caminho):** 1,75.
- **Variações de linguagem resolvidas diretamente na tarefa 2:** 5 de 6 (83,3%).
- **Principal dificuldade:** nomes de alguns itens do menu por tema não descrevem a situação do cidadão (por exemplo, "Falsa central" para golpes por ligação).
- **Mudanças sugeridas:**
  1. criar um campo `titulo` em cada registro, com um nome descritivo (por exemplo, "Pediram código ou senha por ligação");
  2. após a mensagem de "sem resposta", oferecer a escolha de um tema ali mesmo, sem voltar ao menu;
  3. repetir este roteiro com pelo menos uma pessoa de fora da equipe e comparar os resultados.
