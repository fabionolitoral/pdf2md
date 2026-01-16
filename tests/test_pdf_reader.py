"""
Testes para o leitor de PDF.
"""

import pytest
from pathlib import Path
from pdf2md.core.pdf_reader import LeitorPDF


class TestLeitorPDF:
    """Testes para a classe LeitorPDF."""

    @pytest.fixture
    def pdf_teste(self):
        """Fixture com caminho do PDF de teste."""
        caminho = Path(__file__).parent / "fixtures" / "sample.pdf"
        if not caminho.exists():
            pytest.skip("Arquivo de teste não encontrado")
        return caminho

    def test_abrir_pdf_valido(self, pdf_teste):
        """Testa abertura de um PDF válido."""
        with LeitorPDF(pdf_teste) as leitor:
            assert leitor.documento is not None

    def test_obter_informacoes(self, pdf_teste):
        """Testa obtenção de informações do PDF."""
        with LeitorPDF(pdf_teste) as leitor:
            info = leitor.obter_informacoes()

            assert 'total_paginas' in info
            assert 'titulo' in info
            assert 'autor' in info
            assert 'tamanho' in info
            assert 'criptografado' in info

            assert isinstance(info['total_paginas'], int)
            assert info['total_paginas'] > 0

    def test_abrir_pdf_inexistente(self):
        """Testa erro ao abrir PDF inexistente."""
        caminho_invalido = Path("arquivo_inexistente.pdf")

        with pytest.raises(ValueError):
            LeitorPDF(caminho_invalido)

    def test_context_manager(self, pdf_teste):
        """Testa uso do context manager."""
        with LeitorPDF(pdf_teste) as leitor:
            assert leitor.documento is not None

        # Após sair do contexto, o documento deve estar fechado
        assert leitor.documento is None or leitor.documento.is_closed


class TestLeitorPDFMetodos:
    """Testes para métodos específicos do LeitorPDF."""

    @pytest.fixture
    def leitor(self):
        """Fixture que retorna um leitor de PDF."""
        caminho = Path(__file__).parent / "fixtures" / "sample.pdf"
        if not caminho.exists():
            pytest.skip("Arquivo de teste não encontrado")

        leitor = LeitorPDF(caminho)
        yield leitor
        leitor.fechar()

    def test_total_paginas_positivo(self, leitor):
        """Testa que o total de páginas é positivo."""
        info = leitor.obter_informacoes()
        assert info['total_paginas'] > 0

    def test_tamanho_arquivo_positivo(self, leitor):
        """Testa que o tamanho do arquivo é positivo."""
        info = leitor.obter_informacoes()
        assert info['tamanho'] > 0
