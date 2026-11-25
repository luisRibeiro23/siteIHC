from resultados import registrar_resultado


def cifrar_cesar(mensagem, deslocamento):
    resultado = ""

    for caractere in mensagem:
        if caractere.isalpha():
            inicio = ord("A") if caractere.isupper() else ord("a")

            novo_caractere = chr(
                (ord(caractere) - inicio + deslocamento) % 26 + inicio
            )

            resultado += novo_caractere
        else:
            resultado += caractere

    return resultado


def decifrar_cesar(mensagem, deslocamento):
    return cifrar_cesar(mensagem, -deslocamento)


def executar_jogo(mensagem, deslocamento, tentativa, grupo):
    mensagem_cifrada = cifrar_cesar(
        mensagem,
        deslocamento
    )

    mensagem_decifrada = decifrar_cesar(
        tentativa,
        deslocamento
    )

    acertou = mensagem_decifrada.lower() == mensagem.lower()

    registrar_resultado(
        1,
        grupo,
        {
            "mensagem_original": mensagem,
            "mensagem_cifrada": mensagem_cifrada,
            "tentativa": tentativa,
            "mensagem_decifrada": mensagem_decifrada,
            "decifrada_por_terceiros": acertou,
            "deslocamento": deslocamento
        }
    )

    return {
        "mensagem_cifrada": mensagem_cifrada,
        "mensagem_decifrada": mensagem_decifrada,
        "acertou": acertou
    }


if __name__ == "__main__":

    mensagem = "SEGURANCA"
    deslocamento = 3

    mensagem_cifrada = cifrar_cesar(
        mensagem,
        deslocamento
    )

    print("=== CRIPTO DESPLUGADA ===")
    print(f"Mensagem original: {mensagem}")
    print(f"Mensagem cifrada: {mensagem_cifrada}")

    tentativa = input("\nDigite uma tentativa de mensagem cifrada: ")

    resultado = executar_jogo(
        mensagem,
        deslocamento,
        tentativa,
        "Grupo 1"
    )

    print("\n=== RESULTADO ===")
    print(f"Mensagem decifrada: {resultado['mensagem_decifrada']}")

    if resultado["acertou"]:
        print("A mensagem foi decifrada corretamente.")
    else:
        print("A tentativa não corresponde à mensagem original.")