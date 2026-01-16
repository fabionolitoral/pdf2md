"""
Sistema de logging da aplicação.
"""

import logging
import sys
from pathlib import Path


def obter_logger(nome: str) -> logging.Logger:
    """
    Obtém um logger configurado para a aplicação.

    Args:
        nome: Nome do logger (geralmente __name__)

    Returns:
        Logger configurado
    """
    logger = logging.getLogger(nome)

    if not logger.handlers:
        # Criar diretório de logs se não existir
        log_dir = Path("logs")
        log_dir.mkdir(exist_ok=True)

        # Handler para arquivo
        arquivo_handler = logging.FileHandler(log_dir / "pdf2md.log", encoding="utf-8")
        arquivo_handler.setLevel(logging.DEBUG)

        # Handler para console
        console_handler = logging.StreamHandler(sys.stdout)
        console_handler.setLevel(logging.INFO)

        # Formato
        formato = logging.Formatter(
            "%(asctime)s - %(name)s - %(levelname)s - %(message)s",
            datefmt="%Y-%m-%d %H:%M:%S",
        )

        arquivo_handler.setFormatter(formato)
        console_handler.setFormatter(formato)

        logger.addHandler(arquivo_handler)
        logger.addHandler(console_handler)
        logger.setLevel(logging.DEBUG)

    return logger
