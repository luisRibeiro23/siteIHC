import armazenamento

resultados = armazenamento.carregar("resultados")


def registrar_resultado(jogo_id, grupo, dados):
    resultado = {
        "jogo_id": jogo_id,
        "grupo": grupo,
        "dados": dados
    }

    resultados.append(resultado)
    armazenamento.salvar("resultados", resultados)

    return resultado


def listar_resultados():
    return resultados


def buscar_resultados(jogo_id):
    return [
        resultado
        for resultado in resultados
        if resultado["jogo_id"] == jogo_id
    ]


def exibir_resultados():
    print("\n=== RESULTADOS DOS JOGOS ===")

    if not resultados:
        print("Nenhum resultado registrado.")
        return

    for resultado in resultados:
        print(f"\nJogo ID: {resultado['jogo_id']}")
        print(f"Grupo: {resultado['grupo']}")

        for chave, valor in resultado["dados"].items():
            print(f"{chave}: {valor}")

if __name__ == "__main__":

    registrar_resultado(
        1,
        "Grupo 1",
        {
            "mensagem_cifrada": "FDVD",
            "decifrada_por_terceiros": True,
            "nivel_protecao": "Baixo"
        }
    )

    registrar_resultado(
        2,
        "Grupo 2",
        {
            "estrategia": "Comparação Par a Par",
            "comparacoes": 12,
            "trocas": 5
        }
    )

    registrar_resultado(
        2,
        "Grupo 2",
        {
            "estrategia": "Busca pelo Menor Valor",
            "comparacoes": 9,
            "trocas": 3
        }
    )

    registrar_resultado(
        3,
        "Grupo 3",
        {
            "item_identificado": True,
            "quantidade_perguntas": 4
        }
    )

    exibir_resultados()