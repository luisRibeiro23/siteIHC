<<<<<<< HEAD
# siteIHC
=======
# Jogos Desplugados: MVP de apoio

Ferramenta de apoio às atividades de Computação Desplugada para o Ensino Médio (Projeto de Extensão, UFAM, Grupo 4). As dinâmicas são físicas; este software **registra e compara os resultados** das rodadas e controla a frequência.

Jogos cobertos: **Cripto Desplugada**, **Redes de Ordenação** e **Árvore de Decisão**.

## Requisitos

- Python 3.8 ou superior
- Nenhuma biblioteca externa

## Estrutura

```
jogos.py               catálogo dos jogos
resultados.py          registro e consulta de resultados
cripto_desplugada.py   Cifra de César
redes_ordenacao.py     ordenação (par a par e menor valor)
arvore_decisao.py      identificação por árvore de perguntas
frequencia.py          presença/falta e percentual
armazenamento.py       leitura e gravação em JSON
painel.py              painel e menu no terminal
servidor.py            painel e formulários no navegador
dados/                 arquivos JSON (criada automaticamente)
```

Mantenha todos os arquivos na **mesma pasta**.

## Como executar

### Painel no navegador

```bash
python servidor.py
```

Abre `http://localhost:8000` automaticamente. No Windows, se `python` não funcionar, use `py servidor.py`.

| Opção | Efeito |
|---|---|
| `--demo` | Carrega dados de exemplo em uma pasta temporária (não altera os dados reais) |
| `--sem-navegador` | Não abre o navegador automaticamente |

Para parar: `Ctrl+C`.

### Painel no terminal

```bash
python painel.py          # menu interativo
python painel.py --demo   # roda todos os jogos com dados de exemplo e mostra o painel
```

## Onde ficam os dados

Em `dados/resultados.json` e `dados/frequencia.json`, ao lado dos scripts. Para usar outra pasta, defina a variável de ambiente `MVP_DADOS_DIR`:

```bash
# Linux / macOS
MVP_DADOS_DIR=/tmp/teste python painel.py

# Windows (PowerShell)
$env:MVP_DADOS_DIR="C:\temp\teste"; python painel.py
```

Sugestão: adicionar `dados/` ao `.gitignore`.

Atenção: executar `python resultados.py` ou `python frequencia.py` diretamente roda os exemplos que ficam no final desses arquivos e grava dados de teste em `dados/`.

## Uso dos módulos

```python
import cripto_desplugada, redes_ordenacao, frequencia, resultados

# Cripto: cifra "SEGURANCA" com deslocamento 3 e registra a tentativa do grupo
cripto_desplugada.executar_jogo("SEGURANCA", 3, "VHJXUDQFD", "Grupo 1")

# Ordenação: executa as duas estratégias e registra comparações e trocas
redes_ordenacao.executar_jogo([5, 2, 8, 1, 4], "Grupo 1")

# Frequência
frequencia.registrar_frequencia("João", "1º Ano A", "02/10/2026", True)
frequencia.calcular_frequencia("João")   # 100.0

# Resultados
resultados.buscar_resultados(2)          # todos os resultados do jogo 2
```

Os IDs dos jogos são: `1` Cripto Desplugada, `2` Redes de Ordenação, `3` Árvore de Decisão.

## API do painel web

| Rota | Método | Corpo (JSON) |
|---|---|---|
| `/api/painel` | GET | |
| `/api/cripto` | POST | `grupo`, `tentativa`, `mensagem` (opcional), `deslocamento` (1 a 25, opcional) |
| `/api/ordenacao` | POST | `grupo`, `numeros` (de 2 a 20, separados por vírgula) |
| `/api/arvore` | POST | `grupo`, `item` (índice do item) |
| `/api/frequencia` | POST | `aluno`, `turma`, `data` (AAAA-MM-DD), `presente` (`"1"` ou `"0"`) |

As rotas POST exigem `Content-Type: application/json` e respondem `{"ok": true, "mensagem": "..."}` ou `{"erro": "..."}` com status 400.

## Limitações conhecidas

- A troca de chaves e a comparação de proteção da Cripto Desplugada ainda não estão implementadas.
- A Árvore de Decisão usa uma árvore fixa de 3 itens.
- O painel web não tem login e escuta apenas em `127.0.0.1`. Para expor na rede, altere o endereço em `servidor.py` e use somente em rede confiável.
- Não há testes automatizados.

## Equipe

Guilherme Kauê · Kaio Cavalcante · Luis Henrique Ribeiro · Luis Miguel
>>>>>>> 78a2b80 (commit fdss)
