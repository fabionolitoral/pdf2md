"""
Extrator de tabelas de PDFs.
"""

import fitz
from typing import List, Dict, Tuple
from pdf2md.utils.logger import obter_logger

logger = obter_logger(__name__)


class ExtratorTabelas:
    """Extrai tabelas de PDFs com alta precisão."""

    def __init__(self, documento: fitz.Document, verbose: bool = False):
        """
        Inicializa o extrator de tabelas.

        Args:
            documento: Documento PDF aberto com fitz
            verbose: Modo verbose
        """
        self.documento = documento
        self.verbose = verbose

    def detectar_tabelas_pagina(self, numero_pagina: int) -> List[Dict]:
        """
        Detecta tabelas em uma página.

        Args:
            numero_pagina: Número da página (0-indexed)

        Returns:
            Lista de tabelas detectadas
        """
        try:
            pagina = self.documento[numero_pagina]

            # Usar a detecção nativa do PyMuPDF
            tabelas = pagina.find_tables()

            if self.verbose:
                logger.info(f"Página {numero_pagina + 1}: {len(tabelas)} tabelas detectadas")

            return tabelas

        except Exception as e:
            logger.error(f"Erro ao detectar tabelas: {e}")
            return []

    def extrair_tabela_para_markdown(self, tabela) -> str:
        """
        Converte uma tabela para formato Markdown.

        Args:
            tabela: Objeto de tabela do PyMuPDF

        Returns:
            Tabela em formato Markdown
        """
        try:
            # Obter dados da tabela
            dados = tabela.extract()

            if not dados or not dados[0]:
                return ""

            # Criar cabeçalho
            linhas_markdown = []

            # Primeira linha como cabeçalho
            cabecalho = [str(celula).strip() for celula in dados[0]]
            linhas_markdown.append("| " + " | ".join(cabecalho) + " |")

            # Separador
            separador = "|" + "|".join(["---"] * len(cabecalho)) + "|"
            linhas_markdown.append(separador)

            # Linhas de dados
            for linha in dados[1:]:
                celulas = [str(celula).strip() for celula in linha]
                linhas_markdown.append("| " + " | ".join(celulas) + " |")

            return "\n".join(linhas_markdown)

        except Exception as e:
            logger.error(f"Erro ao extrair tabela para Markdown: {e}")
            return ""

    def extrair_todas_tabelas(self) -> Dict[int, List[str]]:
        """
        Extrai todas as tabelas do documento.

        Returns:
            Dicionário com tabelas por página
        """
        tabelas_por_pagina = {}

        for numero_pagina in range(len(self.documento)):
            tabelas = self.detectar_tabelas_pagina(numero_pagina)

            if tabelas:
                tabelas_markdown = []
                for tabela in tabelas:
                    md = self.extrair_tabela_para_markdown(tabela)
                    if md:
                        tabelas_markdown.append(md)

                if tabelas_markdown:
                    tabelas_por_pagina[numero_pagina] = tabelas_markdown

        return tabelas_por_pagina
