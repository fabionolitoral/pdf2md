"""
Parser de argumentos e configurações do CLI.
"""

from pathlib import Path

import click


class ValidarArquivoPDF(click.ParamType):
    """Validador customizado para arquivos PDF."""

    name = "pdf"

    def convert(self, value, param, ctx):
        """Valida se o arquivo existe e é um PDF."""
        if isinstance(value, Path):
            return value

        arquivo = Path(value)

        if not arquivo.exists():
            self.fail(f"Arquivo '{value}' não encontrado", param, ctx)

        if arquivo.suffix.lower() != ".pdf":
            self.fail(f"Arquivo '{value}' não é um PDF válido", param, ctx)

        return arquivo


class ValidarDiretorioSaida(click.ParamType):
    """Validador customizado para diretório de saída."""

    name = "diretorio"

    def convert(self, value, param, ctx):
        """Valida e cria o diretório se necessário."""
        if isinstance(value, Path):
            return value

        diretorio = Path(value)

        try:
            diretorio.mkdir(parents=True, exist_ok=True)
            return diretorio
        except PermissionError:
            self.fail(f"Sem permissão para criar diretório '{value}'", param, ctx)
        except Exception as e:
            self.fail(f"Erro ao criar diretório: {e}", param, ctx)


# Instâncias dos validadores
VALIDADOR_PDF = ValidarArquivoPDF()
VALIDADOR_DIRETORIO = ValidarDiretorioSaida()
