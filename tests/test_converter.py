"""
Testes completos para o conversor PDF → Markdown.
"""

import pytest
from pathlib import Path
from datetime import datetime
from pdf2md.core.converter import PDFConverter


class TestPDFConverterBasico:
    """Testes básicos do conversor."""

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

    def test_converter_inicializacao(self, pdf_teste, diretorio_saida):
        """Testa inicialização do conversor."""
        conversor = PDFConverter(
            caminho_pdf=pdf_teste,
            diretorio_saida=diretorio_saida
        )

        assert conversor.caminho_pdf == pdf_teste
        assert conversor.diretorio_saida == diretorio_saida
        assert conversor.ocr_habilitado == False
        assert conversor.extrair_imagens == False
        assert conversor.extrair_tabelas == True
        assert conversor.verbose == False

    def test_converter_cria_diretorio_saida(self, pdf_teste, tmp_path):
        """Testa criação automática do diretório de saída."""
        diretorio_novo = tmp_path / "novo" / "aninhado"

        conversor = PDFConverter(
            caminho_pdf=pdf_teste,
            diretorio_saida=diretorio_novo
        )

        assert diretorio_novo.exists()
        assert diretorio_novo.is_dir()

    def test_converter_arquivo_inexistente(self, tmp_path):
        """Testa erro ao tentar converter arquivo inexistente."""
        arquivo_invalido = tmp_path / "nao_existe.pdf"

        with pytest.raises(Exception):
            conversor = PDFConverter(
                caminho_pdf=arquivo_invalido,
                diretorio_saida=tmp_path
            )
            conversor.converter()


class TestPDFConverterConversao:
    """Testes do processo de conversão."""

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

    def test_converter_gera_arquivo_markdown(self, pdf_teste, diretorio_saida):
        """Testa se a conversão gera um arquivo Markdown."""
        conversor = PDFConverter(
            caminho_pdf=pdf_teste,
            diretorio_saida=diretorio_saida
        )

        arquivo_saida = conversor.converter()

        assert arquivo_saida.exists()
        assert arquivo_saida.suffix == '.md'
        assert arquivo_saida.name == f"{pdf_teste.stem}.md"

    def test_converter_conteudo_nao_vazio(self, pdf_teste, diretorio_saida):
        """Testa se o arquivo gerado tem conteúdo."""
        conversor = PDFConverter(
            caminho_pdf=pdf_teste,
            diretorio_saida=diretorio_saida
        )

        arquivo_saida = conversor.converter()

        with open(arquivo_saida, 'r', encoding='utf-8') as f:
            conteudo = f.read()
            assert len(conteudo) > 0
            assert '#' in conteudo  # Deve ter pelo menos um título

    def test_converter_titulo_principal(self, pdf_teste, diretorio_saida):
        """Testa se o título principal está presente."""
        conversor = PDFConverter(
            caminho_pdf=pdf_teste,
            diretorio_saida=diretorio_saida
        )

        arquivo_saida = conversor.converter()

        with open(arquivo_saida, 'r', encoding='utf-8') as f:
            conteudo = f.read()
            # O título deve ser o nome do arquivo (sem extensão)
            assert f"# {pdf_teste.stem}" in conteudo

    def test_converter_com_verbose(self, pdf_teste, diretorio_saida, capsys):
        """Testa conversão com modo verbose."""
        conversor = PDFConverter(
            caminho_pdf=pdf_teste,
            diretorio_saida=diretorio_saida,
            verbose=True
        )

        conversor.converter()

        captured = capsys.readouterr()
        assert 'Processada página' in captured.out or 'página' in captured.out.lower()


class TestPDFConverterOpcoes:
    """Testes das opções do conversor."""

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

    def test_converter_sem_tabelas(self, pdf_teste, diretorio_saida):
        """Testa conversão sem extração de tabelas."""
        conversor = PDFConverter(
            caminho_pdf=pdf_teste,
            diretorio_saida=diretorio_saida,
            extrair_tabelas=False
        )

        arquivo_saida = conversor.converter()
        assert arquivo_saida.exists()

    def test_converter_com_imagens(self, pdf_teste, diretorio_saida):
        """Testa conversão com extração de imagens."""
        conversor = PDFConverter(
            caminho_pdf=pdf_teste,
            diretorio_saida=diretorio_saida,
            extrair_imagens=True
        )

        arquivo_saida = conversor.converter()

        # Verifica se a pasta de imagens foi criada (se houver imagens)
        pasta_imagens = diretorio_saida / "imagens"
        # Pode ou não existir dependendo do PDF
        assert arquivo_saida.exists()

    def test_converter_idioma_ocr(self, pdf_teste, diretorio_saida):
        """Testa configuração do idioma OCR."""
        conversor = PDFConverter(
            caminho_pdf=pdf_teste,
            diretorio_saida=diretorio_saida,
            ocr_habilitado=False,
            idioma_ocr='eng'
        )

        assert conversor.idioma_ocr == 'eng'


class TestPDFConverterEstatisticas:
    """Testes das estatísticas de conversão."""

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

    def test_converter_estatisticas_basicas(self, pdf_teste, diretorio_saida):
        """Testa coleta de estatísticas básicas."""
        conversor = PDFConverter(
            caminho_pdf=pdf_teste,
            diretorio_saida=diretorio_saida
        )

        conversor.converter()
        stats = conversor.obter_estatisticas()

        assert 'paginas_processadas' in stats
        assert 'imagens_extraidas' in stats
        assert 'tabelas_extraidas' in stats
        assert 'caracteres_extraidos' in stats
        assert 'tempo_conversao' in stats
        assert 'tamanho_arquivo_saida' in stats

    def test_converter_estatisticas_valores(self, pdf_teste, diretorio_saida):
        """Testa valores das estatísticas."""
        conversor = PDFConverter(
            caminho_pdf=pdf_teste,
            diretorio_saida=diretorio_saida
        )

        conversor.converter()
        stats = conversor.obter_estatisticas()

        assert stats['paginas_processadas'] > 0
        assert stats['caracteres_extraidos'] >= 0
        assert stats['tempo_conversao'] > 0
        assert stats['tamanho_arquivo_saida'] > 0
        assert isinstance(stats['imagens_extraidas'], int)
        assert isinstance(stats['tabelas_extraidas'], int)

    def test_converter_tempo_conversao(self, pdf_teste, diretorio_saida):
        """Testa se o tempo de conversão é registrado."""
        conversor = PDFConverter(
            caminho_pdf=pdf_teste,
            diretorio_saida=diretorio_saida
        )

        inicio = datetime.now()
        conversor.converter()
        fim = datetime.now()

        stats = conversor.obter_estatisticas()
        tempo_real = (fim - inicio).total_seconds()

        # O tempo registrado deve ser próximo ao tempo real
        assert 0 < stats['tempo_conversao'] <= tempo_real + 1


class TestPDFConverterIntegracao:
    """Testes de integração completos."""

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
    def test_converter_completo(self, pdf_teste, diretorio_saida):
        """Testa conversão completa com todas as opções."""
        conversor = PDFConverter(
            caminho_pdf=pdf_teste,
            diretorio_saida=diretorio_saida,
            ocr_habilitado=False,  # OCR pode ser lento
            extrair_imagens=True,
            extrair_tabelas=True,
            verbose=True
        )

        arquivo_saida = conversor.converter()

        # Verificações completas
        assert arquivo_saida.exists()
        assert arquivo_saida.stat().st_size > 0

        with open(arquivo_saida, 'r', encoding='utf-8') as f:
            conteudo = f.read()
            assert len(conteudo) > 0

        stats = conversor.obter_estatisticas()
        assert stats['paginas_processadas'] > 0

    @pytest.mark.integration
    def test_converter_multiplos_arquivos(self, pdf_teste, tmp_path):
        """Testa conversão de múltiplos arquivos."""
        for i in range(3):
            diretorio = tmp_path / f"teste_{i}"

            conversor = PDFConverter(
                caminho_pdf=pdf_teste,
                diretorio_saida=diretorio
            )

            arquivo = conversor.converter()
            assert arquivo.exists()


class TestPDFConverterErros:
    """Testes de tratamento de erros."""

    def test_converter_pdf_invalido(self, tmp_path):
        """Testa erro com arquivo PDF inválido."""
        arquivo_txt = tmp_path / "teste.txt"
        arquivo_txt.write_text("Não é um PDF")

        with pytest.raises(Exception):
            conversor = PDFConverter(
                caminho_pdf=arquivo_txt,
                diretorio_saida=tmp_path
            )
            conversor.converter()

    def test_converter_caminho_invalido(self):
        """Testa erro com caminho inválido."""
        with pytest.raises(Exception):
            PDFConverter(
                caminho_pdf=Path("///caminho/invalido.pdf"),
                diretorio_saida=Path("/tmp")
            )
