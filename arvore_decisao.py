from resultados import registrar_resultado


def identificar_item(item, arvore):
    perguntas = 0
    no_atual = arvore

    while "item" not in no_atual:
        caracteristica = no_atual["caracteristica"]

        resposta = item[caracteristica] == no_atual["valor"]

        perguntas += 1

        if resposta:
            no_atual = no_atual["sim"]
        else:
            no_atual = no_atual["nao"]

    return no_atual["item"], perguntas


def executar_jogo(itens, arvore, item_escolhido, grupo):

    item_identificado, quantidade_perguntas = identificar_item(
        item_escolhido,
        arvore
    )

    acertou = item_identificado == item_escolhido["nome"]

    registrar_resultado(
        3,
        grupo,
        {
            "item_escolhido": item_escolhido["nome"],
            "item_identificado": item_identificado,
            "quantidade_perguntas": quantidade_perguntas,
            "acertou": acertou
        }
    )

    return {
        "item_identificado": item_identificado,
        "quantidade_perguntas": quantidade_perguntas,
        "acertou": acertou
    }


if __name__ == "__main__":

    itens = [
        {
            "nome": "Círculo",
            "forma": "círculo",
            "cor": "escura"
        },
        {
            "nome": "Quadrado",
            "forma": "quadrado",
            "cor": "clara"
        },
        {
            "nome": "Triângulo",
            "forma": "triângulo",
            "cor": "escura"
        }
    ]

    arvore = {
        "caracteristica": "cor",
        "valor": "clara",

        "sim": {
            "item": "Quadrado"
        },

        "nao": {
            "caracteristica": "forma",
            "valor": "círculo",

            "sim": {
                "item": "Círculo"
            },

            "nao": {
                "item": "Triângulo"
            }
        }
    }

    item_escolhido = itens[2]

    resultado = executar_jogo(
        itens,
        arvore,
        item_escolhido,
        "Grupo 1"
    )

    print("=== ÁRVORE DE DECISÃO ===")
    print(f"Item escolhido: {item_escolhido['nome']}")
    print(f"Item identificado: {resultado['item_identificado']}")
    print(f"Quantidade de perguntas: {resultado['quantidade_perguntas']}")

    if resultado["acertou"]:
        print("Identificação correta.")
    else:
        print("Identificação incorreta.")