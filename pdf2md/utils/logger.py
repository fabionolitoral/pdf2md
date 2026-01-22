"""
Sistema de logging com cores e ícones.
"""

import logging
from colorama import Fore, Back, Style, init

# Inicializa colorama para Windows
init(autoreset=True)


class ColoredFormatter(logging.Formatter):
    """Formatter customizado com cores e ícones."""

    # Ícones para cada nível
    ICONS = {
        'DEBUG': '🔍',
        'INFO': 'ℹ️ ',
        'SUCCESS': '✅',
        'WARNING': '⚠️ ',
        'ERROR': '❌',
        'CRITICAL': '🔥'
    }

    # Cores para cada nível
    COLORS = {
        'DEBUG': Fore.CYAN,
        'INFO': Fore.BLUE,
        'SUCCESS': Fore.GREEN,
        'WARNING': Fore.YELLOW,
        'ERROR': Fore.RED,
        'CRITICAL': Fore.RED + Back.WHITE
    }

    def format(self, record):
        # Adiciona ícone e cor
        icon = self.ICONS.get(record.levelname, '')
        color = self.COLORS.get(record.levelname, '')

        # Formata a mensagem
        log_message = f"{color}{icon}  {record.getMessage()}{Style.RESET_ALL}"

        return log_message


def obter_logger(nome: str, nivel=logging.INFO):
    """
    Cria um logger customizado com cores e ícones.

    Args:
        nome: Nome do logger
        nivel: Nível de logging

    Returns:
        Logger configurado
    """
    logger = logging.getLogger(nome)
    logger.setLevel(nivel)

    # Remove handlers existentes
    logger.handlers.clear()

    # Cria handler para console
    console_handler = logging.StreamHandler()
    console_handler.setLevel(nivel)

    # Aplica o formatter customizado
    console_handler.setFormatter(ColoredFormatter())

    logger.addHandler(console_handler)

    # Adiciona nível SUCCESS customizado
    logging.SUCCESS = 25  # Entre INFO (20) e WARNING (30)
    logging.addLevelName(logging.SUCCESS, 'SUCCESS')

    def success(self, message, *args, **kwargs):
        if self.isEnabledFor(logging.SUCCESS):
            self._log(logging.SUCCESS, message, args, **kwargs)

    logging.Logger.success = success

    return logger


def log_separador(logger, char='─', length=60):
    """Imprime uma linha separadora."""
    logger.info(Fore.CYAN + char * length + Style.RESET_ALL)


def log_titulo(logger, titulo: str):
    """Imprime um título destacado."""
    separador = '═' * 60
    logger.info(Fore.MAGENTA + Style.BRIGHT + separador)
    logger.info(Fore.MAGENTA + Style.BRIGHT + f"  {titulo}")
    logger.info(Fore.MAGENTA + Style.BRIGHT + separador + Style.RESET_ALL)


def log_progresso(logger, atual: int, total: int, descricao: str = ""):
    """Imprime barra de progresso."""
    porcentagem = (atual / total) * 100
    barra_tamanho = 40
    preenchido = int((atual / total) * barra_tamanho)
    barra = '█' * preenchido + '░' * (barra_tamanho - preenchido)

    cor = Fore.GREEN if porcentagem == 100 else Fore.CYAN

    mensagem = f"{cor}[{barra}] {porcentagem:.1f}% {descricao}{Style.RESET_ALL}"
    logger.info(mensagem)


def log_estatisticas(logger, stats: dict):
    """Imprime estatísticas formatadas."""
    log_separador(logger)
    logger.info(Fore.YELLOW + Style.BRIGHT + "📊 ESTATÍSTICAS" + Style.RESET_ALL)
    log_separador(logger)

    for chave, valor in stats.items():
        logger.info(f"{Fore.WHITE}  • {chave}: {Fore.CYAN}{valor}{Style.RESET_ALL}")

    log_separador(logger)
