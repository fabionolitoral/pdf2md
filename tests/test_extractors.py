"""
Testes para os extractors (extratores de dados do PDF).
"""

import pytest
from pathlib import Path
from pdf2md.core.text_extractor import ExtratorTexto
from pdf2md.core.table_extractor import ExtratorTabelas
from pdf2md.core.image_extractor import ExtratorImagens
import fitz


class TestExtratorTexto:
    """Testes para o extrator de texto."""

    @pytest.fixture
    def documento_pdf(self):
        """Fixture com um documento PDF aberto."""
        caminho = Path(__file__).parent / "fixtures" / "sample.pdf"
        if not caminho.exists():
            pytest.skip("Arquivo de teste não encontrado")

        doc = fitz.open(str(caminho))
        yield doc
        doc.close()

    def test_extrair_texto_pagina_valida(self, documento_pdf):
        """Testa extração de texto de uma página válida."""
        extrator = ExtratorTexto(documento_pdf)
        texto = extrator.extrair_texto_pagina(0)

        assert isinstance(texto, str)
        assert len(texto) > 0

    def test_extrair_texto_pagina_invalida(self, documento_pdf):
        """Testa extração de texto de uma página inválida."""
        extrator = ExtratorTexto(documento_pdf)
        texto = extrator.extrair_texto_pagina(999)

        assert texto == ""

    def test_extrair_blocos_estruturados(self, documento_pdf):
        """Testa extração de blocos estruturados."""
        extrator = ExtratorTexto(documento_pdf)
        blocos = extrator.extrair_blocos_estruturados(0)

        assert isinstance(blocos, list)
        # Cada bloco deve ter as chaves esperadas
        if blocos:
            bloco = blocos[0]
            assert 'x0' in bloco
            assert 'y0' in bloco
            assert 'x1' in bloco
            assert 'y1' in bloco
            assert 'texto' in bloco

    def test_detectar_titulos(self, documento_pdf):
        """Testa detecção de títulos."""
        extrator = ExtratorTexto(documento_pdf)
        blocos = extrator.extrair_blocos_estruturados(0)

        if blocos:
            classificados = extrator.detectar_titulos(blocos)

            assert 'titulos' in classificados
            assert 'subtitulos' in classificados
            assert 'corpo' in classificados

    def test_limpar_texto(self, documento_pdf):
        """Testa limpeza de texto."""
        extrator = ExtratorTexto(documento_pdf)

        texto_sujo = "  Linha 1  \n\n  Linha 2  \n\n\n  Linha 3  "
        texto_limpo = extrator.limpar_texto(texto_sujo)

        assert "Linha 1" in texto_limpo
        assert "Linha 2" in texto_limpo
        assert "Linha 3" in texto_limpo
        assert "\n\n\n" not in texto_limpo


class TestExtratorTabelas:
    """Testes para o extrator de tabelas."""

    @pytest.fixture
    def documento_pdf(self):
        """Fixture com um documento PDF aberto."""
        caminho = Path(__file__).parent / "fixtures" / "sample.pdf"
        if not caminho.exists():
            pytest.skip("Arquivo de teste não encontrado")

        doc = fitz.open(str(caminho))
        yield doc
        doc.close()

    def test_detectar_tabelas_pagina(self, documento_pdf):
        """Testa detecção de tabelas em uma página."""
        extrator = ExtratorTabelas(documento_pdf)
        tabelas = extrator.detectar_tabelas_pagina(0)

        assert isinstance(tabelas, list)

    def test_extrair_tabela_para_markdown_valida(self, documento_pdf):
        """Testa conversão de tabela para Markdown."""
        extrator = ExtratorTabelas(documento_pdf)

        # Criar uma tabela mock para teste
        tabela_mock = [
            ['Nome', 'Idade'],
            ['João', '30'],
            ['Maria', '25']
        ]

        # Simulando o método extract() de uma tabela real
        class TabelaMock:
            def extract(self):
                return tabela_mock

        resultado = extrator.extrair_tabela_para_markdown(TabelaMock())

        assert '|' in resultado
        assert 'Nome' in resultado
        assert 'Idade' in resultado
        assert 'João' in resultado
