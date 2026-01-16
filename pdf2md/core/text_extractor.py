"""
Extrator de texto de PDFs com preservação de estrutura.
"""

from pathlib import Path

import fitz  # PyMuPDF
import re

from pdf2md.utils.logger import obter_logger

logger = obter_logger(__name__)


class ExtratorTexto:  # ✅ CORRIGIDO: Era "Extratortexto"
    """Extrai texto de PDFs preservando estrutura e formatação."""

    def __init__(self, documento: fitz.Document, verbose: bool = False):
        """
        Inicializa o extrator de texto.

        Args:
            documento: Documento PDF aberto com fitz
            verbose: Modo verbose para mais detalhes
        """
        self.documento = documento
        self.verbose = verbose
        self.blocos_texto = []

    def extrair_texto_pagina(self, numero_pagina: int) -> str:
        """
        Extrai texto de uma página específica.

        Args:
            numero_pagina: Número da página (0-indexed)

        Returns:
            Texto extraído da página
        """
        try:
            pagina = self.documento[numero_pagina]
            texto = pagina.get_text()

            if self.verbose:
                logger.info(
                    f"Página {numero_pagina + 1}: {len(texto)} caracteres extraídos"
                )

            texto = leitor_pdf.extrair_texto(pagina)
            texto = normalizar_texto(texto)
            return texto

        except Exception as e:
            logger.error(f"Erro ao extrair texto da página {numero_pagina}: {e}")
            return ""

    def limpar_linhas_vazias(texto_bruto: str) -> str:
        linhas = texto_bruto.split("\n")
        linhas_limpa = []
        for linha in linhas:
            if linha.strip() == "":
                # Evita múltiplas linhas vazias seguidas
                if len(linhas_limpa) == 0 or linhas_limpa[-1].strip() == "":
                    continue
            linhas_limpa.append(linha)
        return "\n".join(linhas_limpa)

    def normalizar_texto(texto: str) -> str:
        # Remove múltiplas quebras de linha
        texto = re.sub(r"\n\s*\n\s*\n+", "\n\n", texto)

        # Remove espaços duplicados
        texto = re.sub(r"[ \t]+", " ", texto)

        # Remove linhas contendo apenas símbolos
        texto = re.sub(r"^[^A-Za-z0-9]+$", "", texto, flags=re.MULTILINE)

        # Remove linhas muito curtas e sem contexto (< 3 chars)
        linhas = []
        for linha in texto.split("\n"):
            if len(linha.strip()) <= 2:
                continue
            linhas.append(linha)

        return "\n".join(linhas)

    def extrair_blocos_estruturados(self, numero_pagina: int) -> list:
        """
        Extrai blocos de texto estruturados (com posição e tipo).

        Args:
            numero_pagina: Número da página (0-indexed)

        Returns:
            Lista de blocos com informações de posição e tipo
        """
        try:
            pagina = self.documento[numero_pagina]
            blocos = pagina.get_text("blocks")

            blocos_processados = []

            for bloco in blocos:
                if len(bloco) >= 5:
                    x0, y0, x1, y1, texto = bloco[:5]

                    # Ignorar blocos vazios
                    if not texto or not texto.strip():
                        continue

                    blocos_processados.append(
                        {
                            "x0": x0,
                            "y0": y0,
                            "x1": x1,
                            "y1": y1,
                            "texto": texto.strip(),
                            "largura": x1 - x0,
                            "altura": y1 - y0,
                        }
                    )

            return blocos_processados

        except Exception as e:
            logger.error(f"Erro ao extrair blocos estruturados: {e}")
            return []

    def detectar_titulos(self, blocos: list) -> dict:
        """
        Detecta títulos baseado em tamanho e posição.

        Args:
            blocos: Lista de blocos estruturados

        Returns:
            Dicionário com blocos classificados por tipo
        """
        blocos_classificados = {"titulos": [], "subtitulos": [], "corpo": []}

        if not blocos:
            return blocos_classificados

        # Calcular altura média dos blocos
        alturas = [b["altura"] for b in blocos]
        altura_media = sum(alturas) / len(alturas) if alturas else 0

        for bloco in blocos:
            altura = bloco["altura"]

            # Heurística: títulos têm altura maior
            if altura > altura_media * 1.5:
                blocos_classificados["titulos"].append(bloco)
            elif altura > altura_media * 1.2:
                blocos_classificados["subtitulos"].append(bloco)
            else:
                blocos_classificados["corpo"].append(bloco)

        return blocos_classificados

    def extrair_todas_paginas(self) -> str:
        """
        Extrai texto de todas as páginas.

        Returns:
            Texto completo do documento
        """
        texto_completo = []

        for i in range(len(self.documento)):
            texto = self.extrair_texto_pagina(i)
            if texto:
                texto_completo.append(texto)

        return "\n\n".join(texto_completo)

    def limpar_texto(self, texto: str) -> str:
        """
        Limpa o texto removendo caracteres desnecessários.

        Args:
            texto: Texto a ser limpo

        Returns:
            Texto limpo
        """
        # Remover espaços em branco excessivos
        linhas = [linha.strip() for linha in texto.split("\n")]
        linhas = [linha for linha in linhas if linha]

        return "\n".join(linhas)
