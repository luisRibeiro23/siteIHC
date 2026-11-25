# UNIVERSIDADE FEDERAL DO AMAZONAS
## PROJETO DE EXTENSÃO
### Entrega 3: MVP e Integração dos Módulos
**Jogos Interativos de Computação Desplugada para o Ensino Médio**

**Grupo 4**
Guilherme Kauê Silva · Kaio Cavalcante · Luis Henrique Ribeiro · Luis Miguel Magalhães

---

## 1. Objetivo da entrega

Esta entrega apresenta o MVP (Produto Mínimo Viável) de apoio às três atividades de Computação Desplugada do projeto: **Cripto Desplugada**, **Redes de Ordenação** e **Árvore de Decisão**.

As dinâmicas continuam sendo realizadas com materiais físicos (cartões, fichas e folhas impressas), conforme definido na Entrega 2. O software **não substitui** as atividades: ele serve como ferramenta de apoio para **registrar, consolidar e comparar** os resultados obtidos pelos grupos em sala, além de controlar a frequência dos estudantes.

## 2. Escopo do MVP

| Módulo | Arquivo | O que faz |
|---|---|---|
| Jogos | `jogos.py` | Levantamento dos três jogos (tema, conceitos, status) e consulta por ID |
| Resultados | `resultados.py` | Registro e consulta dos resultados de cada rodada, por jogo e grupo |
| Cripto Desplugada | `cripto_desplugada.py` | Cifra de César: cifrar, decifrar e registrar a tentativa de um grupo |
| Redes de Ordenação | `redes_ordenacao.py` | Executa dois algoritmos (comparação par a par e busca pelo menor valor) e conta comparações e trocas |
| Árvore de Decisão | `arvore_decisao.py` | Identifica um item por perguntas sim/não e conta as perguntas usadas |
| Frequência | `frequencia.py` | Registro de presença/falta e cálculo do percentual por aluno |
| Armazenamento | `armazenamento.py` | Persistência em arquivos JSON (os dados sobrevivem ao fechar o programa) |
| Painel (terminal) | `painel.py` | Menu que integra todos os módulos e exibe o painel consolidado |
| Painel (web) | `servidor.py` | Interface em navegador com painel e formulários de registro |

## 3. Arquitetura

```
jogos.py ─────────────┐
cripto_desplugada.py ─┤
redes_ordenacao.py ───┼─► resultados.py ─┐
arvore_decisao.py ────┘                  ├─► armazenamento.py ─► dados/*.json
frequencia.py ───────────────────────────┘
        ▲
        │ usados por
 painel.py (terminal)  ◄──  servidor.py (web, navegador)
```

- Cada jogo registra seus resultados por meio de `registrar_resultado(jogo_id, grupo, dados)`.
- O `armazenamento.py` grava os dados em `dados/resultados.json` e `dados/frequencia.json`, de forma segura (arquivo temporário seguido de substituição).
- O painel consolida os dados e é oferecido em duas versões: terminal e web. As duas usam os mesmos módulos e os mesmos arquivos de dados, então um registro feito em uma aparece na outra.
- Tecnologia: Python 3, usando apenas a biblioteca padrão (sem dependências externas).

## 4. Funcionamento dos módulos

**Cripto Desplugada.** Cifra uma mensagem pela Cifra de César com deslocamento configurável (padrão +3, igual à Folha de Cifragem do Mockup 2). Registra a mensagem original, a cifrada, a tentativa do grupo e o resultado.

**Redes de Ordenação.** Recebe uma sequência de números e executa as duas estratégias previstas na ficha técnica. Para a sequência `[5, 2, 8, 1, 4]`, por exemplo:

| Estratégia | Comparações | Trocas |
|---|---|---|
| Comparação par a par | 10 | 6 |
| Busca pelo menor valor | 10 | 2 |

Os resultados mostram que as duas estratégias fazem o mesmo número de comparações, mas custos diferentes em trocas, que é o contraste que a atividade pretende discutir (BNCC EM13CO03).

**Árvore de Decisão.** Percorre uma árvore de perguntas sim/não até identificar o item escolhido, registrando o item identificado, se acertou e a quantidade de perguntas.

**Frequência.** Registra presença ou falta por aluno, turma e data, e calcula o percentual de frequência de cada aluno.

## 5. Painel de projetos

O painel reúne em um único ponto:

- um cartão por jogo, com seus indicadores (rodadas, acertos, médias de comparações e trocas, média de perguntas);
- a frequência de cada aluno;
- os 10 últimos resultados registrados.

A versão web atualiza automaticamente a cada 5 segundos e possui formulários para registrar rodadas de cada jogo e frequência diretamente pelo navegador. Os dados são validados antes de serem gravados (campos obrigatórios, limites numéricos, formato de data).

## 6. Atendimento aos requisitos da Entrega 2

| Requisito | Situação | Observação |
|---|---|---|
| RF-CD01 Duplas ou trios | Parcial | A participação ocorre na dinâmica física; o software registra por grupo |
| RF-CD02 Cifra simples | Atendido | Cifra de César |
| RF-CD03 Troca de chaves | Pendente | Ainda não implementado |
| RF-CD04 Registrar se foi decifrada por terceiros | Parcial | Registra, mas a lógica de verificação precisa de ajuste |
| RF-CD05 Comparar proteção | Pendente | Depende do RF-CD03 |
| RF-RO01 Grupo de 6+ estudantes | Parcial | Dinâmica física; o software aceita de 2 a 20 números |
| RF-RO02 Dois algoritmos | Atendido | Par a par e menor valor |
| RF-RO03 Registrar comparações e trocas | Atendido | |
| RF-RO04 Comparar eficiência | Atendido | Médias por estratégia no painel |
| RF-AD01 Conjunto de itens | Parcial | MVP usa 3 itens; a cartela do Mockup 3 tem 6 |
| RF-AD02 Montar árvore | Pendente | O MVP usa uma árvore fixa |
| RF-AD03 Usar a árvore para identificar | Atendido | |
| RF-AD04 Comparar árvores | Pendente | |

Os requisitos não funcionais de materiais (RNF-xx01 a RNF-xx04) dizem respeito às atividades físicas e continuam sendo atendidos pelos materiais impressos da Entrega 2.

## 7. Testes realizados

Foram realizados testes manuais:

- execução de cada jogo isoladamente e pelo menu integrado;
- persistência: dados registrados em uma sessão aparecem ao reabrir o programa;
- integração terminal e web: registro feito em um aparece no outro;
- entradas inválidas (deslocamento fora do intervalo, data inválida, lista com um único número, item inexistente) rejeitadas com mensagem de erro, sem gravar dados;
- arquivo JSON corrompido: o sistema inicia com lista vazia, sem travar;
- modo demonstração (`--demo`) isolado, sem alterar os dados reais.

Ainda não há testes automatizados.

## 8. Limitações e pendências

1. Implementar a troca de chaves e a comparação de proteção (RF-CD03 e RF-CD05).
2. Revisar a lógica de `decifrada_por_terceiros`: hoje ela confere se o texto cifrado digitado está correto, e não se a dupla descobriu a mensagem original.
3. Ampliar a Árvore de Decisão para os 6 itens da cartela (com a característica "borda") e permitir montar e comparar árvores.
4. Decidir se a frequência fará parte do escopo oficial, pois não consta nas fichas técnicas.
5. O painel web não possui login e escuta apenas no computador local.
6. Criar testes automatizados.

## 9. Conclusão

O MVP integra os três jogos, o registro de resultados, o controle de frequência e um painel consolidado, com persistência de dados e interface em terminal e navegador. Ele valida a arquitetura do projeto e deixa pronta a base para as próximas etapas: aplicação em sala, coleta de feedback e análise de resultados (etapas 4 e 5 do cronograma).