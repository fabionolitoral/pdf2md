"""
Conversor em lote de múltiplos PDFs.
"""

from pathlib import Path
from typing import List, Dict
from pdf2md.core.converter import PDFConverter
from pdf2md.utils.logger import obter_logger

logger = obter_logger(__name__)


class BatchConverter:
    """Conversor em lote de PDFs para Markdown."""

    def __init__(
        self,
        diretorio_entrada: Path,
        diretorio_saida: Path,
        ocr_habilitado: bool = False,
        extrair_imagens: bool = True,
        extrair_tabelas: bool = True,
        idioma_ocr: str = 'por',
        verbose: bool = False
    ):
        """
        Inicializa o conversor em lote.

        Args:
            diretorio_entrada: Pasta contendo os PDFs
            diretorio_saida: Pasta onde salvar os Markdowns
            ocr_habilitado: Ativar OCR
            extrair_imagens: Extrair imagens
            extrair_tabelas: Extrair tabelas
            idioma_ocr: Idioma para OCR
            verbose: Modo detalhado
        """
        self.diretorio_entrada = Path(diretorio_entrada)
        self.diretorio_saida = Path(diretorio_saida)
        self.ocr_habilitado = ocr_habilitado
        self.extrair_imagens = extrair_imagens
        self.extrair_tabelas = extrair_tabelas
        self.idioma_ocr = idioma_ocr
        self.verbose = verbose

        # Validações
        if not self.diretorio_entrada.exists():
            raise FileNotFoundError(
                f"Diretório de entrada não encontrado: {self.diretorio_entrada}"
            )

        if not self.diretorio_entrada.is_dir():
            raise ValueError(
                f"Caminho não é um diretório: {self.diretorio_entrada}"
            )

        # Criar diretório de saída se não existir
        self.diretorio_saida.mkdir(parents=True, exist_ok=True)

        # Estatísticas
        self.resultados: List[Dict] = []

    def listar_pdfs(self) -> List[Path]:
        """
        Lista todos os arquivos PDF no diretório de entrada.

        Returns:
            Lista de caminhos dos PDFs encontrados
        """
        pdfs = list(self.diretorio_entrada.glob('*.pdf'))
        pdfs.extend(self.diretorio_entrada.glob('*.PDF'))

        # Remover duplicatas (case-insensitive)
        pdfs_unicos = {}
        for pdf in pdfs:
            pdfs_unicos[pdf.name.lower()] = pdf

        return sorted(pdfs_unicos.values())

    def converter_todos(self) -> Dict:
        """
        Converte todos os PDFs encontrados.
        Agora salva tudo diretamente na pasta de saída.
        """
        pdfs = self.listar_pdfs()

        if not pdfs:
            logger.warning(
                f"Nenhum PDF encontrado em: {self.diretorio_entrada}"
            )
            return {
                'total_pdfs': 0,
                'sucesso': 0,
                'falhas': 0,
                'resultados': []
            }

        logger.info(f"Encontrados {len(pdfs)} PDFs para conversão")

        sucesso = 0
        falhas = 0

        for i, pdf in enumerate(pdfs, start=1):
            logger.info(f"[{i}/{len(pdfs)}] Convertendo: {pdf.name}")

            try:
                # 👉 Agora o diretório de saída é sempre o mesmo (sem subpastas)
                pasta_saida = self.diretorio_saida

                conversor = PDFConverter(
                    caminho_pdf=pdf,
                    diretorio_saida=pasta_saida,
                    ocr_habilitado=self.ocr_habilitado,
                    extrair_imagens=self.extrair_imagens,
                    extrair_tabelas=self.extrair_tabelas,
                    idioma_ocr=self.idioma_ocr,
                    verbose=self.verbose
                )

                arquivo_md = conversor.converter()
                stats = conversor.obter_estatisticas()

                self.resultados.append({
                    'pdf': pdf.name,
                    'status': 'sucesso',
                    'markdown': arquivo_md,
                    'estatisticas': stats
                })

                sucesso += 1
                logger.info(f"✓ {pdf.name} convertido com sucesso")

            except Exception as e:
                self.resultados.append({
                    'pdf': pdf.name,
                    'status': 'falha',
                    'erro': str(e)
                })

                falhas += 1
                logger.error(f"✗ Erro ao converter {pdf.name}: {e}")

        return {
            'total_pdfs': len(pdfs),
            'sucesso': sucesso,
            'falhas': falhas,
            'resultados': self.resultados
        }

