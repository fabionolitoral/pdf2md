"""
Conversor principal de PDF para Markdown.
"""

from pathlib import Path
from datetime import datetime
import fitz  # PyMuPDF
from pdf2md.core.text_extractor import ExtratorTexto
from pdf2md.core.table_extractor import ExtratorTabelas
from pdf2md.core.image_extractor import ExtratorImagens
from pdf2md.core.ocr_processor import ProcessadorOCR
from pdf2md.markdown.formatter import FormataadorMarkdown
from pdf2md.utils.logger import obter_logger

logger = obter_logger(__name__)


class PDFConverter:
    """Conversor completo de PDF → Markdown."""

    def __init__(
        self,
        caminho_pdf: Path,
        diretorio_saida: Path,
        ocr_habilitado: bool = False,
        extrair_imagens: bool = False,
        extrair_tabelas: bool = True,
        idioma_ocr: str = 'por',
        verbose: bool = False
    ):
        """
        Inicializa o conversor.

        Args:
            caminho_pdf: Caminho do PDF
            diretorio_saida: Diretório de saída
            ocr_habilitado: Ativar OCR
            extrair_imagens: Extrair imagens
            extrair_tabelas: Extrair tabelas
            idioma_ocr: Idioma para OCR
            verbose: Modo verbose

        Raises:
            FileNotFoundError: Se o arquivo PDF não existir
            ValueError: Se o caminho não for um arquivo PDF válido
        """
        self.caminho_pdf = Path(caminho_pdf)

        # ✅ VALIDAÇÃO ADICIONADA
        if not self.caminho_pdf.exists():
            raise FileNotFoundError(f"Arquivo não encontrado: {self.caminho_pdf}")

        if not self.caminho_pdf.is_file():
            raise ValueError(f"O caminho não é um arquivo: {self.caminho_pdf}")

        if self.caminho_pdf.suffix.lower() != '.pdf':
            raise ValueError(f"O arquivo não é um PDF: {self.caminho_pdf}")

        self.diretorio_saida = Path(diretorio_saida)
        self.ocr_habilitado = ocr_habilitado
        self.extrair_imagens = extrair_imagens
        self.extrair_tabelas = extrair_tabelas
        self.idioma_ocr = idioma_ocr
        self.verbose = verbose

        # Criar diretório de saída
        self.diretorio_saida.mkdir(parents=True, exist_ok=True)

        self.formatador = FormataadorMarkdown(
            titulo=self.caminho_pdf.stem,
            verbose=verbose
        )

        self.estatisticas = {
            'paginas_processadas': 0,
            'imagens_extraidas': 0,
            'tabelas_extraidas': 0,
            'caracteres_extraidos': 0,
            'tempo_conversao': 0,
            'tamanho_arquivo_saida': 0
        }

    def converter(self) -> Path:
        """
        Executa a conversão completa do PDF para Markdown.

        Returns:
            Caminho do arquivo Markdown gerado
        """
        inicio = datetime.now()

        try:
            logger.info(f"Iniciando conversão: {self.caminho_pdf.name}")

            # Adicionar título principal
            self.formatador.adicionar_titulo(self.caminho_pdf.stem, nivel=1)
            self.formatador.adicionar_quebra_pagina()

            # Abrir PDF
            documento = fitz.open(str(self.caminho_pdf))

            try:
                total_paginas = len(documento)
                logger.info(f"PDF aberto: {total_paginas} páginas")

                # Processar cada página
                for num_pagina in range(total_paginas):
                    self._processar_pagina(documento, num_pagina)
                    self.estatisticas['paginas_processadas'] += 1

                    if self.verbose:
                        print(f"Processada página {num_pagina + 1}/{total_paginas}")

            finally:
                documento.close()

            # Gerar arquivo Markdown
            arquivo_saida = self._gerar_arquivo_markdown()

            # Calcular estatísticas finais
            self.estatisticas['tempo_conversao'] = (
                datetime.now() - inicio
            ).total_seconds()

            if arquivo_saida.exists():
                self.estatisticas['tamanho_arquivo_saida'] = arquivo_saida.stat().st_size

            logger.info(f"Conversão concluída: {arquivo_saida}")
            return arquivo_saida

        except Exception as e:
            logger.error(f"Erro durante conversão: {e}")
            raise

    def _processar_pagina(self, documento: fitz.Document, numero_pagina: int) -> None:
        """
        Processa uma página do PDF.

        Args:
            documento: Documento PDF aberto
            numero_pagina: Número da página
        """
        if self.verbose:
            logger.info(f"Processando página {numero_pagina + 1}")

        # Adicionar separador de página
        if numero_pagina > 0:
            self.formatador.adicionar_linha_horizontal()

        # Extrair texto
        extrator_texto = ExtratorTexto(documento, self.verbose)

        # Processar OCR se habilitado
        if self.ocr_habilitado:
            processador_ocr = ProcessadorOCR(
                documento,
                self.idioma_ocr,
                self.verbose
            )
            texto_ocr = processador_ocr.processar_pagina_ocr(numero_pagina)
            if texto_ocr:
                self.formatador.adicionar_paragrafo(texto_ocr)
                self.estatisticas['caracteres_extraidos'] += len(texto_ocr)
        else:
            # Extrair texto normal
            blocos = extrator_texto.extrair_blocos_estruturados(numero_pagina)

            for bloco in blocos:
                texto = bloco['texto']
                self.formatador.adicionar_paragrafo(texto)
                self.estatisticas['caracteres_extraidos'] += len(texto)

        # Extrair tabelas
        if self.extrair_tabelas:
            extrator_tabelas = ExtratorTabelas(documento, self.verbose)
            tabelas = extrator_tabelas.detectar_tabelas_pagina(numero_pagina)

            for tabela in tabelas:
                md_tabela = extrator_tabelas.extrair_tabela_para_markdown(tabela)
                if md_tabela:
                    self.formatador.adicionar_tabela(md_tabela)
                    self.estatisticas['tabelas_extraidas'] += 1

        # Extrair imagens
        if self.extrair_imagens:
            extrator_imagens = ExtratorImagens(
                documento,
                self.diretorio_saida,
                self.verbose
            )
            imagens = extrator_imagens.extrair_imagens_pagina(numero_pagina)

            for imagem in imagens:
                self.formatador.adicionar_imagem(
                    caminho_relativo=imagem['caminho_relativo'],
                    titulo=f"Imagem {imagem['numero_pagina']}.{imagem['indice']}"
                )
                self.estatisticas['imagens_extraidas'] += 1

    def _gerar_arquivo_markdown(self) -> Path:
        """
        Gera o arquivo Markdown final.

        Returns:
            Caminho do arquivo gerado
        """
        # Obter conteúdo
        conteudo = self.formatador.obter_conteudo()

        # Salvar arquivo
        arquivo_saida = self.diretorio_saida / f"{self.caminho_pdf.stem}.md"

        with open(arquivo_saida, 'w', encoding='utf-8') as f:
            f.write(conteudo)

        logger.info(f"Arquivo Markdown salvo: {arquivo_saida}")

        return arquivo_saida

    def obter_estatisticas(self) -> dict:
        """Retorna as estatísticas da conversão."""
        return self.estatisticas.copy()
