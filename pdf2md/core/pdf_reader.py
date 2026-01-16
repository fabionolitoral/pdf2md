"""
Leitor de PDF - extração de informações básicas.
"""

from pathlib import Path

import fitz  # PyMuPDF


class LeitorPDF:
    """Classe para leitura e extração de informações de PDFs."""

    def __init__(self, caminho_pdf: Path):
        """
        Inicializa o leitor de PDF.

        Args:
            caminho_pdf: Caminho do arquivo PDF
        """
        self.caminho_pdf = Path(caminho_pdf)
        self.documento = None
        self._abrir()

    def _abrir(self):
        """Abre o documento PDF."""
        try:
            self.documento = fitz.open(str(self.caminho_pdf))
        except Exception as e:
            raise ValueError(f"Erro ao abrir PDF: {e}")

    def obter_informacoes(self) -> dict:
        """
        Obtém informações básicas do PDF.

        Returns:
            Dicionário com informações
        """
        return {
            "total_paginas": self.documento.page_count,
            "titulo": self.documento.metadata.get("title", ""),
            "autor": self.documento.metadata.get("author", ""),
            "tamanho": self.caminho_pdf.stat().st_size,
            "criptografado": self.documento.is_pdf and self.documento.is_encrypted,
        }

    def fechar(self):
        """Fecha o documento PDF."""
        if self.documento:
            self.documento.close()

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.fechar()
