"""
Funções de validação para a aplicação.
"""

from pathlib import Path


def validar_arquivo_pdf(caminho: Path) -> bool:
    """
    Valida se um arquivo é um PDF válido.

    Args:
        caminho: Caminho do arquivo

    Returns:
        True se válido, False caso contrário
    """
    if not isinstance(caminho, Path):
        caminho = Path(caminho)

    if not caminho.exists():
        return False

    if caminho.suffix.lower() != '.pdf':
        return False

    # Verificar assinatura do PDF
    try:
        with open(caminho, 'rb') as f:
            assinatura = f.read(4)
            return assinatura == b'%PDF'
    except Exception:
        return False


def validar_diretorio_saida(caminho: Path) -> bool:
    """
    Valida se um diretório de saída é válido.

    Args:
        caminho: Caminho do diretório

    Returns:
        True se válido, False caso contrário
    """
    if not isinstance(caminho, Path):
        caminho = Path(caminho)

    try:
        caminho.mkdir(parents=True, exist_ok=True)
        return caminho.is_dir() and caminho.exists()
    except Exception:
        return False
