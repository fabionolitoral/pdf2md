"""
Testes de integração.
"""

import pytest
from pathlib import Path
from pdf2md.core.converter import PDFConverter


class TestIntegracaoCompleta:
    """Testes de integração do sistema completo."""

    @pytest.fixture
    def pdf_teste(self):
        """Fixture com caminho do PDF de teste."""
        caminho = Path(__file__).parent / "fixtures" / "sample.pdf"
        if not caminho.exists():
            pytest.skip("Arquivo de teste não encontrado")
        return caminho

    @pytest.fixture
    def diretorio_saida(self, tmp_path):
        """Fixture com diretório temporário de saída."""
        return tmp_path

    @pytest.mark.integration
    def test_conversao_completa_basica(self, pdf_teste, diretorio_saida):
        """Testa conversão completa básica."""
        conversor = PDFConverter(
            caminho_pdf=pdf_teste,
            diretorio_saida=diretorio_saida
        )

        arquivo_saida = conversor.converter()

        # Verificações
        assert arquivo_saida.exists()
        assert arquivo_saida.suffix == '.md'

        # Verificar conteúdo
        with open(arquivo_saida, 'r', encoding='utf-8') as f:
            conteudo = f.read()
            assert len(conteudo) > 0
            assert '#' in conteudo  # Deve ter pelo menos um título

    @pytest.mark.integration
    def test_conversao_com_todas_opcoes(self, pdf_teste, diretorio_saida):
        """Testa conversão com todas as opções ativadas."""
        conversor = PDFConverter(
            caminho_pdf=pdf_teste,
            diretorio_saida=diretorio_saida,
            extrair_imagens=True,
            extrair_tabelas=True,
            verbose=True
        )

        arquivo_saida = conversor.converter()

        # Verificações
        assert arquivo_saida.exists()

        # Verificar estatísticas
        stats = conversor.obter_estatisticas()
        assert stats['paginas_processadas'] > 0
        assert stats['caracteres_extraidos'] > 0

    @pytest.mark.integration
    def test_multiplas_conversoes(self, pdf_teste, diretorio_saida):
        """Testa múltiplas conversões consecutivas."""
        for i in range(3):
            conversor = PDFConverter(
                caminho_pdf=pdf_teste,
                diretorio_saida=diretorio_saida / f"teste_{i}"
            )

            arquivo_saida = conversor.converter()
            assert arquivo_saida.exists()
