"""
Testes avançados para o conversor.
"""

import pytest
from pathlib import Path
from pdf2md.core.converter import PDFConverter


class TestConversorAvancado:
    """Testes avançados para o conversor."""

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

    def test_conversor_sem_opcoes(self, pdf_teste, diretorio_saida):
        """Testa conversor com configuração mínima."""
        conversor = PDFConverter(
            caminho_pdf=pdf_teste,
            diretorio_saida=diretorio_saida
        )

        arquivo = conversor.converter()
        assert arquivo.exists()
        assert arquivo.suffix == '.md'

    def test_conversor_com_verbose(self, pdf_teste, diretorio_saida, capsys):
        """Testa conversor com modo verbose."""
        conversor = PDFConverter(
            caminho_pdf=pdf_teste,
            diretorio_saida=diretorio_saida,
            verbose=True
        )

        arquivo = conversor.converter()
        assert arquivo.exists()

    def test_conversor_estatisticas(self, pdf_teste, diretorio_saida):
        """Testa coleta de estatísticas."""
        conversor = PDFConverter(
            caminho_pdf=pdf_teste,
            diretorio_saida=diretorio_saida
        )

        conversor.converter()
        stats = conversor.obter_estatisticas()

        assert 'paginas_processadas' in stats
        assert 'caracteres_extraidos' in stats
        assert 'tempo_conversao' in stats
        assert stats['paginas_processadas'] > 0

    def test_conversor_arquivo_invalido(self, tmp_path):
        """Testa conversor com arquivo inválido."""
        arquivo_invalido = tmp_path / "nao_existe.pdf"

        with pytest.raises(Exception):
            conversor = PDFConverter(
                caminho_pdf=arquivo_invalido,
                diretorio_saida=tmp_path
            )
            conversor.converter()

    def test_conversor_diretorio_saida_criado(self, pdf_teste, tmp_path):
        """Testa criação automática do diretório de saída."""
        diretorio_novo = tmp_path / "novo_diretorio" / "aninhado"

        conversor = PDFConverter(
            caminho_pdf=pdf_teste,
            diretorio_saida=diretorio_novo
        )

        arquivo = conversor.converter()

        assert diretorio_novo.exists()
        assert arquivo.exists()

    def test_conversor_tamanho_arquivo_saida(self, pdf_teste, diretorio_saida):
        """Testa se o arquivo de saída tem tamanho válido."""
        conversor = PDFConverter(
            caminho_pdf=pdf_teste,
            diretorio_saida=diretorio_saida
        )

        arquivo = conversor.converter()
        tamanho = arquivo.stat().st_size

        assert tamanho > 0

    def test_conversor_conteudo_nao_vazio(self, pdf_teste, diretorio_saida):
        """Testa se o conteúdo do arquivo não está vazio."""
        conversor = PDFConverter(
            caminho_pdf=pdf_teste,
            diretorio_saida=diretorio_saida
        )

        arquivo = conversor.converter()

        with open(arquivo, 'r', encoding='utf-8') as f:
            conteudo = f.read()
            assert len(conteudo) > 0

    @pytest.mark.integration
    def test_conversor_com_todas_opcoes(self, pdf_teste, diretorio_saida):
        """Testa conversor com todas as opções ativadas."""
        conversor = PDFConverter(
            caminho_pdf=pdf_teste,
            diretorio_saida=diretorio_saida,
            ocr_habilitado=False,  # OCR pode ser lento
            extrair_imagens=True,
            extrair_tabelas=True,
            verbose=True
        )

        arquivo = conversor.converter()
        assert arquivo.exists()
