from resultados import registrar_resultado


def comparacao_par_a_par(numeros):
    numeros = numeros.copy()

    comparacoes = 0
    trocas = 0

    n = len(numeros)

    for i in range(n):
        for j in range(0, n - i - 1):
            comparacoes += 1

            if numeros[j] > numeros[j + 1]:
                numeros[j], numeros[j + 1] = numeros[j + 1], numeros[j]
                trocas += 1

    return {
        "resultado": numeros,
        "comparacoes": comparacoes,
        "trocas": trocas
    }


def busca_pelo_menor_valor(numeros):
    numeros = numeros.copy()

    comparacoes = 0
    trocas = 0

    n = len(numeros)

    for i in range(n):
        menor = i

        for j in range(i + 1, n):
            comparacoes += 1

            if numeros[j] < numeros[menor]:
                menor = j

        if menor != i:
            numeros[i], numeros[menor] = numeros[menor], numeros[i]
            trocas += 1

    return {
        "resultado": numeros,
        "comparacoes": comparacoes,
        "trocas": trocas
    }


def executar_jogo(numeros, grupo):

    resultado_par_a_par = comparacao_par_a_par(numeros)

    registrar_resultado(
        2,
        grupo,
        {
            "estrategia": "Comparação Par a Par",
            "sequencia_inicial": numeros,
            "resultado": resultado_par_a_par["resultado"],
            "comparacoes": resultado_par_a_par["comparacoes"],
            "trocas": resultado_par_a_par["trocas"]
        }
    )

    resultado_menor = busca_pelo_menor_valor(numeros)

    registrar_resultado(
        2,
        grupo,
        {
            "estrategia": "Busca pelo Menor Valor",
            "sequencia_inicial": numeros,
            "resultado": resultado_menor["resultado"],
            "comparacoes": resultado_menor["comparacoes"],
            "trocas": resultado_menor["trocas"]
        }
    )


if __name__ == "__main__":

    numeros = [5, 2, 8, 1, 4]

    executar_jogo(numeros, "Grupo 1")

    resultados = __import__("resultados")

    resultados.exibir_resultados()

