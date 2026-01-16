"""
Processador OCR para PDFs escaneados.
"""

from pathlib import Path
import fitz
from PIL import Image
from io import BytesIO
from pdf2md.utils.logger import obter_logger

logger = obter_logger(__name__)


class ProcessadorOCR:
    """Processa OCR em PDFs escaneados."""

    def __init__(
        self,
        documento: fitz.Document,
        idioma: str = 'por',
        verbose: bool = False
    ):
        """
        Inicializa o processador OCR.

        Args:
            documento: Documento PDF aberto com fitz
            idioma: Idioma para OCR (por, eng, spa, fra)
            verbose: Modo verbose
        """
        self.documento = documento
        self.idioma = idioma
        self.verbose = verbose

        # Tentar importar pytesseract
        try:
            import pytesseract
            self.pytesseract = pytesseract
            self.ocr_disponivel = True
        except ImportError:
            logger.warning("pytesseract não instalado. OCR desabilitado.")
            self.ocr_disponivel = False

    def processar_pagina_ocr(self, numero_pagina: int) -> str:
        """
        Processa OCR em uma página específica.

        Args:
            numero_pagina: Número da página (0-indexed)

        Returns:
            Texto extraído via OCR
        """
        if not self.ocr_disponivel:
            logger.warning("OCR não disponível")
            return ""

        try:
            pagina = self.documento[numero_pagina]

            # Renderizar página como imagem
            pix = pagina.get_pixmap(matrix=fitz.Matrix(2, 2))
            img_data = pix.tobytes("png")

            # Converter para PIL Image
            imagem = Image.open(BytesIO(img_data))

            # Executar OCR
            texto = self.pytesseract.image_to_string(
                imagem,
                lang=self._mapear_idioma()
            )

            if self.verbose:
                logger.info(f"Página {numero_pagina + 1}: OCR processado")

            return texto

        except Exception as e:
            logger.error(f"Erro ao processar OCR na página {numero_pagina}: {e}")
            return ""

    def _mapear_idioma(self) -> str:
        """Mapeia código de idioma para código do Tesseract."""
        mapeamento = {
            'por': 'por',
            'eng': 'eng',
            'spa': 'spa',
            'fra': 'fra'
        }
        return mapeamento.get(self.idioma, 'eng')

    def processar_todas_paginas(self) -> str:
        """
        Processa OCR em todas as páginas.

        Returns:
            Texto completo via OCR
        """
        texto_completo = []

        for numero_pagina in range(len(self.documento)):
            texto = self.processar_pagina_ocr(numero_pagina)
            if texto:
                texto_completo.append(texto)

        return "\n\n".join(texto_completo)
