"""
Testes para os validadores de argumentos.
"""

import pytest
from pathlib import Path
from pdf2md.cli.arguments import VALIDADOR_PDF, VALIDADOR_DIRETORIO


class TestValidadorPDF:
    """Testes para o validador de PDF."""

    def test_validador_pdf_arquivo_valido(self, tmp_path):
        """Testa validador com arquivo PDF válido."""
        # Criar um arquivo PDF fake para teste
        arquivo_pdf = tmp_path / "teste.pdf"
        arquivo_pdf.write_bytes(b"%PDF-1.4\n")

        resultado = VALIDADOR_PDF.convert(str(arquivo_pdf), None, None)
        assert resultado == arquivo_pdf

    def test_validador_pdf_arquivo_inexistente(self):
        """Testa validador com arquivo inexistente."""
        with pytest.raises(Exception):
            VALIDADOR_PDF.convert("arquivo_inexistente.pdf", None, None)

    def test_validador_pdf_arquivo_nao_pdf(self, tmp_path):
        """Testa validador com arquivo que não é PDF."""
        arquivo_txt = tmp_path / "teste.txt"
        arquivo_txt.write_text("Não é um PDF")

        with pytest.raises(Exception):
            VALIDADOR_PDF.convert(str(arquivo_txt), None, None)


class TestValidadorDiretorio:
    """Testes para o validador de diretório."""

    def test_validador_diretorio_valido(self, tmp_path):
        """Testa validador com diretório válido."""
        resultado = VALIDADOR_DIRETORIO.convert(str(tmp_path), None, None)
        assert resultado == tmp_path

    def test_validador_diretorio_criacao(self, tmp_path):
        """Testa criação de diretório inexistente."""
        novo_dir = tmp_path / "novo_diretorio"

        resultado = VALIDADOR_DIRETORIO.convert(str(novo_dir), None, None)

        assert resultado.exists()
        assert resultado.is_dir()
