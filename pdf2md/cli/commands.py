"""
Comandos principais da aplicação CLI.
"""

from pathlib import Path

import click

from pdf2md.cli.arguments import VALIDADOR_DIRETORIO, VALIDADOR_PDF
from pdf2md.core.converter import PDFConverter
from pdf2md.utils.logger import obter_logger

logger = obter_logger(__name__)


@click.group(invoke_without_command=True)  # ✅ CORREÇÃO APLICADA
@click.pass_context  # ✅ CORREÇÃO APLICADA
@click.version_option(version="1.0.0", prog_name="pdf2md")
def cli(ctx):  # ✅ CORREÇÃO APLICADA
    """
    📄 PDF to Markdown Converter

    Conversor profissional de PDF para Markdown com suporte completo.

    Exemplos:

        # Conversão simples
        pdf2md converter arquivo.pdf

        # Com OCR e extração de imagens
        pdf2md converter arquivo.pdf --ocr --extract-images

        # Especificar pasta de saída
        pdf2md converter arquivo.pdf -o output/
    """
    if ctx.invoked_subcommand is None:  # ✅ CORREÇÃO APLICADA
        click.echo(ctx.get_help())  # ✅ CORREÇÃO APLICADA


@cli.command()
@click.argument("arquivo_pdf", type=VALIDADOR_PDF, required=True)
@click.option(
    "-o",
    "--output",
    type=VALIDADOR_DIRETORIO,
    default="./output",
    help="Diretório de saída para o arquivo Markdown",
)
@click.option(
    "--ocr", is_flag=True, default=False, help="Ativar OCR para PDFs escaneados"
)
@click.option(
    "--extract-images", is_flag=True, default=False, help="Extrair imagens do PDF"
)
@click.option(
    "--extract-tables", is_flag=True, default=True, help="Extrair tabelas do PDF"
)
@click.option(
    "-v", "--verbose", is_flag=True, default=False, help="Modo verbose (mais detalhes)"
)
@click.option(
    "--language",
    type=click.Choice(["por", "eng", "spa", "fra"]),
    default="por",
    help="Idioma para OCR",
)
def converter(
    arquivo_pdf: Path,
    output: Path,
    ocr: bool,
    extract_images: bool,
    extract_tables: bool,
    verbose: bool,
    language: str,
):
    """
    🔄 Converte um arquivo PDF para Markdown

    Extrai texto, tabelas, imagens e estrutura do PDF,
    gerando um arquivo Markdown bem formatado.
    """
    try:
        click.echo(
            click.style(
                f"\n📥 Iniciando conversão de: {arquivo_pdf.name}", fg="cyan", bold=True
            )
        )

        # Configurações de conversão
        config = {
            "ocr_habilitado": ocr,
            "extrair_imagens": extract_images,
            "extrair_tabelas": extract_tables,
            "idioma_ocr": language,
            "verbose": verbose,
        }

        # Criar conversor
        conversor = PDFConverter(
            caminho_pdf=arquivo_pdf, diretorio_saida=output, **config
        )

        # Executar conversão
        arquivo_saida = conversor.converter()

        click.echo(
            click.style(f"✅ Conversão concluída com sucesso!", fg="green", bold=True)
        )

        click.echo(click.style(f"📄 Arquivo salvo em: {arquivo_saida}", fg="green"))

        # Mostrar estatísticas
        if verbose:
            _exibir_estatisticas(conversor)

    except FileNotFoundError as e:
        click.echo(
            click.style(f"❌ Erro: Arquivo não encontrado - {e}", fg="red"), err=True
        )
        raise click.Exit(1)

    except Exception as e:
        click.echo(click.style(f"❌ Erro durante conversão: {e}", fg="red"), err=True)
        if verbose:
            import traceback

            traceback.print_exc()
        raise click.Exit(1)


@cli.command()
def info():
    """
    ℹ️  Exibe informações sobre a aplicação
    """
    click.echo(
        click.style(
            """
╔════════════════════════════════════════════════════════════╗
║         PDF to Markdown Converter v1.0.0                  ║
╚════════════════════════════════════════════════════════════╝

📋 Recursos:
  ✓ Extração completa de texto
  ✓ Preservação de tabelas
  ✓ Extração de imagens
  ✓ OCR para PDFs escaneados
  ✓ Estrutura hierárquica mantida

🛠️  Dependências:
  • PyMuPDF (fitz)
  • pdfplumber
  • pytesseract
  • Pillow
  • Click

📚 Documentação:
  Execute: pdf2md --help
            """,
            fg="cyan",
        )
    )


@cli.command()
@click.argument("arquivo_pdf", type=VALIDADOR_PDF)
def validar(arquivo_pdf: Path):
    """
    ✔️  Valida um arquivo PDF antes da conversão
    """
    try:
        click.echo(click.style(f"\n🔍 Validando: {arquivo_pdf.name}", fg="cyan"))

        from pdf2md.core.pdf_reader import LeitorPDF

        leitor = LeitorPDF(arquivo_pdf)
        info = leitor.obter_informacoes()

        click.echo(click.style(f"\n✅ PDF válido!", fg="green", bold=True))

        click.echo(
            f"""
📊 Informações do PDF:
  • Páginas: {info['total_paginas']}
  • Título: {info.get('titulo', 'N/A')}
  • Autor: {info.get('autor', 'N/A')}
  • Tamanho: {info.get('tamanho', 'N/A')}
  • Criptografado: {'Sim' if info.get('criptografado') else 'Não'}
            """
        )

    except Exception as e:
        click.echo(click.style(f"❌ Erro na validação: {e}", fg="red"), err=True)
        raise click.Exit(1)


def _exibir_estatisticas(conversor):
    """Exibe estatísticas da conversão."""
    stats = conversor.obter_estatisticas()

    click.echo(click.style("\n📊 Estatísticas da Conversão:", fg="cyan", bold=True))

    for chave, valor in stats.items():
        click.echo(f"  • {chave}: {valor}")

@cli.command()
@click.argument(
    'diretorio_entrada',
    type=VALIDADOR_DIRETORIO,
    required=True
)
@click.option(
    '-o', '--output',
    type=VALIDADOR_DIRETORIO,
    default='./output',
    help='Diretório de saída (padrão: ./output)'
)
@click.option(
    '--ocr',
    is_flag=True,
    help='Ativar OCR para PDFs escaneados'
)
@click.option(
    '--extract-images',
    is_flag=True,
    help='Extrair imagens do PDF'
)
@click.option(
    '--extract-tables',
    is_flag=True,
    default=True,
    help='Extrair tabelas (padrão: ativado)'
)
@click.option(
    '--language',
    default='por',
    help='Idioma para OCR (por, eng, spa, fra)'
)
@click.option(
    '-v', '--verbose',
    is_flag=True,
    help='Modo detalhado'
)
def batch(diretorio_entrada, output, ocr, extract_images, extract_tables, language, verbose):
    """
    🗂️  Converte TODOS os PDFs de uma pasta

    Exemplos:

        # Converter todos PDFs da pasta 'livros'
        pdf2md batch livros/

        # Com OCR e extração de imagens
        pdf2md batch livros/ --ocr --extract-images

        # Especificar pasta de saída
        pdf2md batch livros/ -o meus_markdowns/
    """
    from pdf2md.core.batch_converter import BatchConverter

    try:
        click.echo(
            click.style(
                f"\n🗂️  Conversão em Lote",
                fg='cyan',
                bold=True
            )
        )

        click.echo(f"📂 Entrada: {diretorio_entrada}")
        click.echo(f"📁 Saída: {output}\n")

        conversor = BatchConverter(
            diretorio_entrada=diretorio_entrada,
            diretorio_saida=output,
            ocr_habilitado=ocr,
            extrair_imagens=extract_images,
            extrair_tabelas=extract_tables,
            idioma_ocr=language,
            verbose=verbose
        )

        resultado = conversor.converter_todos()

        # Exibir resumo
        click.echo(
            click.style(
                "\n📊 Resumo da Conversão:",
                fg='cyan',
                bold=True
            )
        )

        click.echo(f"  • Total de PDFs: {resultado['total_pdfs']}")
        click.echo(
            click.style(
                f"  • Sucesso: {resultado['sucesso']}",
                fg='green'
            )
        )

        if resultado['falhas'] > 0:
            click.echo(
                click.style(
                    f"  • Falhas: {resultado['falhas']}",
                    fg='red'
                )
            )

        # Listar falhas se houver
        falhas = [r for r in resultado['resultados'] if r['status'] == 'falha']
        if falhas:
            click.echo(
                click.style(
                    "\n⚠️  PDFs com erro:",
                    fg='yellow',
                    bold=True
                )
            )
            for falha in falhas:
                click.echo(f"  • {falha['pdf']}: {falha['erro']}")

        click.echo(
            click.style(
                f"\n✅ Conversão concluída!",
                fg='green',
                bold=True
            )
        )

    except Exception as e:
        click.echo(
            click.style(
                f"❌ Erro: {e}",
                fg='red',
                bold=True
            ),
            err=True
        )
        raise click.Exit(1)
