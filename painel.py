import os
import sys
import tempfile

if "--demo" in sys.argv:
    # a demonstração usa uma pasta temporária e não suja os dados reais
    os.environ["MVP_DADOS_DIR"] = tempfile.mkdtemp()

import armazenamento
import jogos
import resultados
import frequencia
import cripto_desplugada
import redes_ordenacao
import arvore_decisao


# ---------- DADOS DE DEMONSTRAÇÃO ----------

ITENS = [
    {"nome": "Círculo", "forma": "círculo", "cor": "escura"},
    {"nome": "Quadrado", "forma": "quadrado", "cor": "clara"},
    {"nome": "Triângulo", "forma": "triângulo", "cor": "escura"},
]

ARVORE = {
    "caracteristica": "cor",
    "valor": "clara",
    "sim": {"item": "Quadrado"},
    "nao": {
        "caracteristica": "forma",
        "valor": "círculo",
        "sim": {"item": "Círculo"},
        "nao": {"item": "Triângulo"},
    },
}


# ---------- EXECUÇÃO DOS JOGOS ----------

def rodar_cripto(grupo, mensagem="SEGURANCA", deslocamento=3, tentativa=None):
    if tentativa is None:
        cifrada = cripto_desplugada.cifrar_cesar(mensagem, deslocamento)
        print(f"Mensagem cifrada: {cifrada}")
        tentativa = input("Tentativa de mensagem cifrada: ")

    return cripto_desplugada.executar_jogo(
        mensagem, deslocamento, tentativa, grupo
    )


def rodar_ordenacao(grupo, numeros=None):
    numeros = numeros or [5, 2, 8, 1, 4]
    redes_ordenacao.executar_jogo(numeros, grupo)


def rodar_arvore(grupo, indice_item=2):
    return arvore_decisao.executar_jogo(
        ITENS, ARVORE, ITENS[indice_item], grupo
    )


def rodar_frequencia_demo():
    dados = [
        ("João", "1º Ano A", "02/10/2026", True),
        ("Maria", "1º Ano A", "02/10/2026", True),
        ("Pedro", "1º Ano A", "02/10/2026", False),
        ("João", "1º Ano A", "03/10/2026", True),
        ("Maria", "1º Ano A", "03/10/2026", False),
        ("Pedro", "1º Ano A", "03/10/2026", True),
    ]

    for aluno, turma, data, presente in dados:
        frequencia.registrar_frequencia(aluno, turma, data, presente)


def rodar_demo():
    """Executa todos os módulos de uma vez (teste de integração)."""
    rodar_cripto("Grupo 1", tentativa="VHJXUDQFD")
    rodar_cripto("Grupo 2", tentativa="ABCDEFGHI")
    rodar_ordenacao("Grupo 1")
    rodar_arvore("Grupo 1", 0)
    rodar_arvore("Grupo 2", 2)
    rodar_frequencia_demo()


# ---------- CONSOLIDAÇÃO ----------

def media(valores):
    return sum(valores) / len(valores) if valores else 0


def resumo_cripto():
    regs = resultados.buscar_resultados(1)
    decifradas = sum(1 for r in regs if r["dados"]["decifrada_por_terceiros"])

    return {
        "rodadas": len(regs),
        "decifradas": decifradas,
        "protegidas": len(regs) - decifradas,
    }


def resumo_ordenacao():
    regs = resultados.buscar_resultados(2)
    por_estrategia = {}

    for r in regs:
        d = r["dados"]
        por_estrategia.setdefault(d["estrategia"], []).append(d)

    return {
        nome: {
            "rodadas": len(lista),
            "media_comparacoes": media([d["comparacoes"] for d in lista]),
            "media_trocas": media([d["trocas"] for d in lista]),
        }
        for nome, lista in por_estrategia.items()
    }


def resumo_arvore():
    regs = resultados.buscar_resultados(3)
    acertos = sum(1 for r in regs if r["dados"].get("acertou"))

    return {
        "rodadas": len(regs),
        "acertos": acertos,
        "media_perguntas": media(
            [r["dados"]["quantidade_perguntas"] for r in regs]
        ),
    }


def resumo_frequencia():
    alunos = sorted({r["aluno"] for r in frequencia.listar_frequencia()})

    return {a: frequencia.calcular_frequencia(a) for a in alunos}


# ---------- EXIBIÇÃO ----------

def exibir_painel():
    print("\n" + "=" * 44)
    print("        PAINEL DE PROJETOS - MVP")
    print("=" * 44)

    for jogo in jogos.listar_jogos():
        print(f"\n[{jogo['id']}] {jogo['nome']} ({jogo['status']})")
        print(f"    Tema: {jogo['tema']}")

        if jogo["id"] == 1:
            r = resumo_cripto()
            print(f"    Rodadas: {r['rodadas']} | "
                  f"decifradas por terceiros: {r['decifradas']} | "
                  f"protegidas: {r['protegidas']}")

        elif jogo["id"] == 2:
            r = resumo_ordenacao()
            if not r:
                print("    Nenhuma rodada registrada.")
            for nome, d in r.items():
                print(f"    {nome}: {d['media_comparacoes']:.1f} comparações, "
                      f"{d['media_trocas']:.1f} trocas (média)")

        elif jogo["id"] == 3:
            r = resumo_arvore()
            print(f"    Rodadas: {r['rodadas']} | acertos: {r['acertos']} | "
                  f"média de perguntas: {r['media_perguntas']:.1f}")

    print("\n--- Frequência ---")
    freq = resumo_frequencia()

    if not freq:
        print("Nenhum registro de frequência.")
    for aluno, pct in freq.items():
        print(f"{aluno}: {pct:.1f}%")

    print()


def limpar_dados():
    if input("Apagar TODOS os dados salvos? (s/n): ").lower() != "s":
        print("Cancelado.")
        return

    resultados.resultados.clear()
    frequencia.registros.clear()
    armazenamento.limpar("resultados")
    armazenamento.limpar("frequencia")
    print("Dados apagados.")


def menu():
    opcoes = {
        "1": ("Ver painel geral", exibir_painel),
        "2": ("Listar jogos", jogos.exibir_jogos),
        "3": ("Jogar Cripto Desplugada",
              lambda: print(rodar_cripto(input("Grupo: ")))),
        "4": ("Jogar Redes de Ordenação",
              lambda: rodar_ordenacao(input("Grupo: "))),
        "5": ("Jogar Árvore de Decisão",
              lambda: print(rodar_arvore(input("Grupo: ")))),
        "6": ("Ver resultados detalhados", resultados.exibir_resultados),
        "7": ("Ver frequência", frequencia.exibir_frequencia),
        "8": ("Carregar dados de demonstração", rodar_demo),
        "9": ("Apagar dados salvos", limpar_dados),
        "0": ("Sair", None),
    }

    while True:
        print("\n=== MENU ===")
        for k, (nome, _) in opcoes.items():
            print(f"{k} - {nome}")

        escolha = input("Opção: ").strip()

        if escolha == "0":
            break

        if escolha in opcoes:
            opcoes[escolha][1]()
        else:
            print("Opção inválida.")


if __name__ == "__main__":
    if "--demo" in sys.argv:
        rodar_demo()
        exibir_painel()
    else:
        menu()