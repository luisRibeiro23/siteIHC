jogos = [
    {
        "id": 1,
        "nome": "Cripto Desplugada",
        "tema": "Segurança da informação e criptografia",
        "conceitos": [
            "Cifragem",
            "Decifragem",
            "Troca de chaves"
        ],
        "status": "Em desenvolvimento"
    },
    {
        "id": 2,
        "nome": "Redes de Ordenação",
        "tema": "Comparação de algoritmos e eficiência",
        "conceitos": [
            "Ordenação",
            "Comparações",
            "Trocas",
            "Eficiência"
        ],
        "status": "Em desenvolvimento"
    },
    {
        "id": 3,
        "nome": "Árvore de Decisão",
        "tema": "Fundamentos de Inteligência Artificial",
        "conceitos": [
            "Classificação",
            "Árvore de decisão",
            "Perguntas",
            "Predição"
        ],
        "status": "Em desenvolvimento"
    }
]


def listar_jogos():
    return jogos


def buscar_jogo(id_jogo):
    for jogo in jogos:
        if jogo["id"] == id_jogo:
            return jogo

    return None


def exibir_jogos():
    print("\n=== JOGOS DISPONÍVEIS ===")

    for jogo in jogos:
        print(f"\nID: {jogo['id']}")
        print(f"Nome: {jogo['nome']}")
        print(f"Tema: {jogo['tema']}")
        print(f"Status: {jogo['status']}")
        print("Conceitos:")

        for conceito in jogo["conceitos"]:
            print(f"- {conceito}")


def exibir_jogo(id_jogo):
    jogo = buscar_jogo(id_jogo)

    if jogo is None:
        print("\nJogo não encontrado.")
        return

    print("\n=== JOGO ===")
    print(f"ID: {jogo['id']}")
    print(f"Nome: {jogo['nome']}")
    print(f"Tema: {jogo['tema']}")
    print(f"Status: {jogo['status']}")
    print("Conceitos:")

    for conceito in jogo["conceitos"]:
        print(f"- {conceito}")


if __name__ == "__main__":
    exibir_jogos()

    print("\n=== CONSULTA DE JOGO ===")
    exibir_jogo(2)