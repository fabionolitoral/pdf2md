"""
Extrator de imagens de PDFs.
"""

from pathlib import Path
import fitz
from PIL import Image
from io import BytesIO
from pdf2md.utils.logger import obter_logger

logger = obter_logger(__name__)


class ExtratorImagens:
    """Extrai imagens de PDFs."""

    def __init__(
        self,
        documento: fitz.Document,
        diretorio_saida: Path,
        verbose: bool = False
    ):
        """
        Inicializa o extrator de imagens.

        Args:
            documento: Documento PDF aberto com fitz
            diretorio_saida: Diretório para salvar as imagens
            verbose: Modo verbose
        """
        self.documento = documento
        self.diretorio_saida = Path(diretorio_saida)
        self.verbose = verbose
        self.contador_imagens = 0

        # Criar diretório de imagens
        self.diretorio_imagens = self.diretorio_saida / "imagens"
        self.diretorio_imagens.mkdir(parents=True, exist_ok=True)

    def extrair_imagens_pagina(self, numero_pagina: int) -> list:
        """
        Extrai imagens de uma página específica.

        Args:
            numero_pagina: Número da página (0-indexed)

        Returns:
            Lista com informações das imagens extraídas
        """
        imagens_extraidas = []

        try:
            pagina = self.documento[numero_pagina]
            imagens = pagina.get_images()

            if self.verbose:
                logger.info(f"Página {numero_pagina + 1}: {len(imagens)} imagens encontradas")

            for indice_img, img_ref in enumerate(imagens):
                try:
                    # Extrair imagem
                    xref = img_ref[0]
                    pix = fitz.Pixmap(self.documento, xref)

                    # Converter para RGB se necessário
                    if pix.n - pix.alpha < 4:  # RGB
                        pix_rgb = pix
                    else:  # CMYK ou outro
                        pix_rgb = fitz.Pixmap(fitz.csRGB, pix)

                    # Salvar imagem
                    self.contador_imagens += 1
                    nome_arquivo = f"imagem_{numero_pagina + 1}_{indice_img + 1}.png"
                    caminho_imagem = self.diretorio_imagens / nome_arquivo

                    pix_rgb.save(str(caminho_imagem))

                    imagens_extraidas.append({
                        'numero_pagina': numero_pagina + 1,
                        'indice': indice_img + 1,
                        'caminho': caminho_imagem,
                        'nome_arquivo': nome_arquivo,
                        'caminho_relativo': f"imagens/{nome_arquivo}"
                    })

                    if self.verbose:
                        logger.info(f"Imagem salva: {nome_arquivo}")

                except Exception as e:
                    logger.error(f"Erro ao extrair imagem {indice_img}: {e}")
                    continue

        except Exception as e:
            logger.error(f"Erro ao extrair imagens da página {numero_pagina}: {e}")

        return imagens_extraidas

    def extrair_todas_imagens(self) -> list:
        """
        Extrai todas as imagens do documento.

        Returns:
            Lista com informações de todas as imagens extraídas
        """
        todas_imagens = []

        for numero_pagina in range(len(self.documento)):
            imagens = self.extrair_imagens_pagina(numero_pagina)
            todas_imagens.extend(imagens)

        return todas_imagens

    def obter_estatisticas(self) -> dict:
        """Retorna estatísticas sobre as imagens extraídas."""
        return {
            'total_imagens': self.contador_imagens,
            'diretorio_imagens': str(self.diretorio_imagens)
        }
