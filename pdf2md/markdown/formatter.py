"""
Formatador de Markdown - converte elementos extraídos para Markdown.
"""

from typing import Any, Dict, List

from pdf2md.utils.logger import obter_logger

logger = obter_logger(__name__)


class FormataadorMarkdown:
    """Formata elementos extraídos em Markdown bem estruturado."""

    def __init__(self, titulo: str = "", verbose: bool = False):
        """
        Inicializa o formatador.

        Args:
            titulo: Título do documento
            verbose: Modo verbose
        """
        self.titulo = titulo
        self.verbose = verbose
        self.conteudo = []

    def adicionar_titulo(self, texto: str, nivel: int = 1) -> None:
        """
        Adiciona um título ao documento.

        Args:
            texto: Texto do título
            nivel: Nível do título (1-6)
        """
        if not texto or not texto.strip():
            return

        nivel = max(1, min(6, nivel))  # Limitar entre 1 e 6
        marcador = "#" * nivel
        self.conteudo.append(f"{marcador} {texto.strip()}\n\n")

        if self.verbose:
            logger.info(f"Título nível {nivel} adicionado: {texto[:50]}")

    def adicionar_paragrafo(self, texto: str) -> None:
        """
        Adiciona um parágrafo ao documento.

        Args:
            texto: Texto do parágrafo
        """
        if not texto or not texto.strip():
            return

        # Limpar o texto
        texto_limpo = self._sanitizar_texto(texto)
        if texto_limpo:
            self.conteudo.append(f"{texto_limpo}\n\n")

    def adicionar_lista(self, itens: List[str], ordenada: bool = False) -> None:
        """
        Adiciona uma lista ao documento.

        Args:
            itens: Lista de itens
            ordenada: Se True, cria lista numerada
        """
        if not itens:
            return

        for i, item in enumerate(itens, start=1):
            if not item or not item.strip():
                continue

            if ordenada:
                self.conteudo.append(f"{i}. {item.strip()}\n")
            else:
                self.conteudo.append(f"- {item.strip()}\n")

        self.conteudo.append("\n")

    def adicionar_tabela(self, tabela_md: str) -> None:
        """
        Adiciona uma tabela ao documento.

        Args:
            tabela_md: Tabela em formato Markdown
        """
        if not tabela_md or not tabela_md.strip():
            return

        self.conteudo.append(f"{tabela_md}\n\n")

        if self.verbose:
            logger.info("Tabela adicionada ao documento")

    def adicionar_imagem(
        self, caminho_relativo: str, titulo: str = "", descricao: str = ""
    ) -> None:
        """
        Adiciona uma imagem ao documento.

        Args:
            caminho_relativo: Caminho relativo da imagem
            titulo: Título/alt text da imagem
            descricao: Descrição da imagem
        """
        if not caminho_relativo:
            return

        alt_text = titulo or "Imagem"
        markdown_img = f"![{alt_text}]({caminho_relativo})"

        if descricao:
            self.conteudo.append(f"{markdown_img}\n\n*{descricao}*\n\n")
        else:
            self.conteudo.append(f"{markdown_img}\n\n")

        if self.verbose:
            logger.info(f"Imagem adicionada: {caminho_relativo}")

    def adicionar_codigo(self, codigo: str, linguagem: str = "") -> None:
        """
        Adiciona um bloco de código ao documento.

        Args:
            codigo: Código a ser adicionado
            linguagem: Linguagem de programação
        """
        if not codigo:
            return

        self.conteudo.append(f"{linguagem}\n{codigo.strip()}\n```\n\n")

    def adicionar_citacao(self, texto: str) -> None:
        """
        Adiciona uma citação/blockquote ao documento.

        Args:
            texto: Texto da citação
        """
        if not texto or not texto.strip():
            return

        linhas = texto.strip().split("\n")
        for linha in linhas:
            if linha.strip():
                self.conteudo.append(f"> {linha}\n")

        self.conteudo.append("\n")

    def adicionar_linha_horizontal(self) -> None:
        """Adiciona uma linha horizontal (separador)."""
        self.conteudo.append("---\n\n")

    def adicionar_quebra_pagina(self) -> None:
        """Adiciona uma quebra de página."""
        self.conteudo.append("\n\n")

    def adicionar_link(self, texto: str, url: str) -> None:
        """
        Adiciona um link ao documento.

        Args:
            texto: Texto do link
            url: URL de destino
        """
        if not texto or not url:
            return

        self.conteudo.append(f"[{texto}]({url})\n\n")

    def adicionar_negrito(self, texto: str) -> str:
        """
        Formata texto em negrito.

        Args:
            texto: Texto a formatar

        Returns:
            Texto formatado
        """
        return f"**{texto}**"

    def adicionar_italico(self, texto: str) -> str:
        """
        Formata texto em itálico.

        Args:
            texto: Texto a formatar

        Returns:
            Texto formatado
        """
        return f"*{texto}*"

    def obter_conteudo(self) -> str:
        """
        Obtém o conteúdo completo formatado.

        Returns:
            String com todo o conteúdo em Markdown
        """
        return "".join(self.conteudo)

    def limpar(self) -> None:
        """Limpa o conteúdo acumulado."""
        self.conteudo = []

    def _sanitizar_texto(self, texto: str) -> str:
        """
        Sanitiza o texto removendo caracteres problemáticos.

        Args:
            texto: Texto a ser sanitizado

        Returns:
            Texto sanitizado
        """
        # Remover caracteres de controle (exceto \n e \t)
        texto_limpo = "".join(
            char for char in texto if ord(char) >= 32 or char in "\n\t"
        )

        # Normalizar espaços em branco excessivos
        linhas = [linha.strip() for linha in texto_limpo.split("\n")]
        linhas = [linha for linha in linhas if linha]

        return " ".join(linhas)

    def obter_estatisticas(self) -> Dict[str, int]:
        """
        Retorna estatísticas sobre o conteúdo formatado.

        Returns:
            Dicionário com estatísticas
        """
        conteudo_completo = self.obter_conteudo()

        return {
            "total_caracteres": len(conteudo_completo),
            "total_linhas": len(conteudo_completo.split("\n")),
            "total_palavras": len(conteudo_completo.split()),
            "total_elementos": len(self.conteudo),
        }
