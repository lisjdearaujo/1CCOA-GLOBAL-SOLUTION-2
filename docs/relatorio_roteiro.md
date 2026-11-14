# Roteiro do relatório (converter para docs/relatorio.pdf, entre 4 e 8 páginas)

1. **Problema e público:** cidadãos com informações dispersas sobre golpes, privacidade, contas e documentos. Público: cidadãos comuns que usam serviços digitais.
2. **Arquitetura:** separação entre lógica (`logica.py`), interface CLI (`sistema.py`), interface web opcional (`app.py`) e testes (`testes.py`). Explicar por que a lógica não depende da interface.
3. **Fontes:** lista das referências usadas na base, com datas de verificação. Explicar o cuidado de não afirmar mais do que a fonte diz.
4. **Estruturas de dados e algoritmos:** listas e dicionários para os registros; grafo de temas (`GRAFO_TEMAS`) e as relações entre eles; busca por pontuação com expressões exatas e palavras em comum; comportamento em empate (status "ambiguo").
5. **Estratégias de prompt:** modelos A e B (`docs/prompts.md`) e a comparação feita.
6. **Lógica booleana (fase 6):** variáveis P, U, L, R; expressão original P·U·(L+R); simplificação por De Morgan; tabela-verdade de 16 linhas mostrando equivalência.
7. **Resultados dos testes:** taxa de acerto, tempo médio, tabela de perguntas, e os erros observados (T04, T10 e T13). Explicar cada erro.
8. **Teste de usabilidade:** resumo do roteiro e do que foi observado.
9. **Interpretação:** o que os números significam, limitações da avaliação (16 perguntas, um participante, base pequena) e pelo menos duas melhorias possíveis (por exemplo: tratar sinônimos com um dicionário de termos; reduzir a ambiguidade com pesos por tipo de palavra-chave).
10. **Impacto social e cuidados:** clareza, acessibilidade, privacidade (o sistema não pede dados pessoais) e a não substituição de canais oficiais.
11. **Conclusão.**
