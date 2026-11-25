import armazenamento

registros = armazenamento.carregar("frequencia")


def registrar_frequencia(aluno, turma, data, presente):
    registro = {
        "aluno": aluno,
        "turma": turma,
        "data": data,
        "presente": presente
    }

    registros.append(registro)
    armazenamento.salvar("frequencia", registros)

    return registro


def listar_frequencia():
    return registros


def buscar_aluno(aluno):
    return [
        registro
        for registro in registros
        if registro["aluno"] == aluno
    ]


def calcular_frequencia(aluno):
    registros_aluno = buscar_aluno(aluno)

    if not registros_aluno:
        return 0

    presencas = sum(
        1
        for registro in registros_aluno
        if registro["presente"]
    )

    total = len(registros_aluno)

    return (presencas / total) * 100


def exibir_frequencia():
    print("\n=== REGISTRO DE FREQUÊNCIA ===")

    if not registros:
        print("Nenhum registro encontrado.")
        return

    for registro in registros:
        status = "Presente" if registro["presente"] else "Falta"

        print(
            f"{registro['data']} | "
            f"{registro['turma']} | "
            f"{registro['aluno']} | "
            f"{status}"
        )


if __name__ == "__main__":

    registrar_frequencia(
        "João",
        "1º Ano A",
        "02/10/2026",
        True
    )

    registrar_frequencia(
        "Maria",
        "1º Ano A",
        "02/10/2026",
        True
    )

    registrar_frequencia(
        "Pedro",
        "1º Ano A",
        "02/10/2026",
        False
    )

    registrar_frequencia(
        "João",
        "1º Ano A",
        "03/10/2026",
        True
    )

    registrar_frequencia(
        "Maria",
        "1º Ano A",
        "03/10/2026",
        False
    )

    registrar_frequencia(
        "Pedro",
        "1º Ano A",
        "03/10/2026",
        True
    )

    exibir_frequencia()

    print("\n=== PERCENTUAL DE FREQUÊNCIA ===")

    for aluno in ["João", "Maria", "Pedro"]:
        percentual = calcular_frequencia(aluno)

        print(
            f"{aluno}: {percentual:.1f}%"
        )