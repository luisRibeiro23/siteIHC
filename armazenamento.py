import json
import os
import tempfile


def diretorio():
    """Pasta dos dados. Pode ser trocada com a variável MVP_DADOS_DIR."""
    pasta = os.environ.get("MVP_DADOS_DIR") or os.path.join(
        os.path.dirname(os.path.abspath(__file__)), "dados"
    )
    os.makedirs(pasta, exist_ok=True)
    return pasta


def caminho(nome):
    return os.path.join(diretorio(), f"{nome}.json")


def carregar(nome):
    """Lê a lista salva. Se o arquivo não existe ou está corrompido, devolve []."""
    try:
        with open(caminho(nome), encoding="utf-8") as f:
            dados = json.load(f)
        return dados if isinstance(dados, list) else []
    except (FileNotFoundError, json.JSONDecodeError):
        return []


def salvar(nome, dados):
    """Grava de forma segura (arquivo temporário + substituição)."""
    destino = caminho(nome)
    fd, temporario = tempfile.mkstemp(dir=diretorio(), suffix=".tmp")

    with os.fdopen(fd, "w", encoding="utf-8") as f:
        json.dump(dados, f, ensure_ascii=False, indent=2)

    os.replace(temporario, destino)


def limpar(nome):
    try:
        os.remove(caminho(nome))
    except FileNotFoundError:
        pass