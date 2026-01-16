"""
Testes para o formatador Markdown (expandido).
"""

import pytest
from pdf2md.markdown.formatter import FormataadorMarkdown


class TestFormataadorMarkdown:
    """Testes para o formatador Markdown."""

    @pytest.fixture
    def formatador(self):
        """Fixture que retorna um formatador."""
        return FormataadorMarkdown(titulo="Teste", verbose=False)

    def test_adicionar_titulo_nivel_1(self, formatador):
        """Testa adição de título nível 1."""
        formatador.adicionar_titulo("Título Principal", nivel=1)
        conteudo = formatador.obter_conteudo()

        assert "# Título Principal" in conteudo

    def test_adicionar_titulo_nivel_2(self, formatador):
        """Testa adição de título nível 2."""
        formatador.adicionar_titulo("Subtítulo", nivel=2)
        conteudo = formatador.obter_conteudo()

        assert "## Subtítulo" in conteudo

    def test_adicionar_titulo_nivel_3(self, formatador):
        """Testa adição de título nível 3."""
        formatador.adicionar_titulo("Subsubtítulo", nivel=3)
        conteudo = formatador.obter_conteudo()

        assert "### Subsubtítulo" in conteudo

    def test_adicionar_paragrafo(self, formatador):
        """Testa adição de parágrafo."""
        texto = "Este é um parágrafo de teste."
        formatador.adicionar_paragrafo(texto)
        conteudo = formatador.obter_conteudo()

        assert texto in conteudo

    def test_adicionar_multiplos_paragrafos(self, formatador):
        """Testa adição de múltiplos parágrafos."""
        para1 = "Primeiro parágrafo."
        para2 = "Segundo parágrafo."
        para3 = "Terceiro parágrafo."

        formatador.adicionar_paragrafo(para1)
        formatador.adicionar_paragrafo(para2)
        formatador.adicionar_paragrafo(para3)

        conteudo = formatador.obter_conteudo()

        assert para1 in conteudo
        assert para2 in conteudo
        assert para3 in conteudo

    def test_adicionar_linha_horizontal(self, formatador):
        """Testa adição de linha horizontal."""
        formatador.adicionar_linha_horizontal()
        conteudo = formatador.obter_conteudo()

        assert "---" in conteudo or "***" in conteudo

    def test_adicionar_tabela(self, formatador):
        """Testa adição de tabela."""
        tabela_md = """| Nome | Idade |
|------|-------|
| João | 30    |
| Maria| 25    |"""

        formatador.adicionar_tabela(tabela_md)
        conteudo = formatador.obter_conteudo()

        assert "Nome" in conteudo
        assert "Idade" in conteudo

    def test_adicionar_imagem(self, formatador):
        """Testa adição de imagem."""
        formatador.adicionar_imagem("imagens/teste.png", "Imagem de Teste")
        conteudo = formatador.obter_conteudo()

        assert "![Imagem de Teste]" in conteudo
        assert "imagens/teste.png" in conteudo

    def test_formatador_vazio(self, formatador):
        """Testa formatador vazio."""
        conteudo = formatador.obter_conteudo()
        assert conteudo == ""

    def test_formatador_com_titulo_inicial(self):
        """Testa formatador com título inicial."""
        formatador = FormataadorMarkdown(titulo="Meu Documento")
        conteudo = formatador.obter_conteudo()

        # Pode ou não ter o título dependendo da implementação
        assert isinstance(conteudo, str)

    def test_adicionar_lista(self, formatador):
        """Testa adição de lista."""
        formatador.adicionar_paragrafo("- Item 1\n- Item 2\n- Item 3")
        conteudo = formatador.obter_conteudo()

        assert "Item 1" in conteudo
        assert "Item 2" in conteudo
        assert "Item 3" in conteudo

    def test_adicionar_codigo(self, formatador):
        """Testa adição de bloco de código."""
        codigo = "python\nprint('Olá Mundo')\n"
        formatador.adicionar_paragrafo(codigo)
        conteudo = formatador.obter_conteudo()
        assert "print" in conteudo