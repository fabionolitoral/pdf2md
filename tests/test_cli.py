"""
Testes para a interface CLI.
"""

import pytest
from click.testing import CliRunner
from pdf2md.cli.commands import cli
from pathlib import Path


class TestCLI:
    """Testes para a interface de linha de comando."""

    @pytest.fixture
    def runner(self):
        """Fixture que retorna um CliRunner."""
        return CliRunner()

    @pytest.fixture
    def pdf_teste(self):
        """Fixture com caminho do PDF de teste."""
        return Path(__file__).parent / "fixtures" / "sample.pdf"

    def test_cli_sem_argumentos(self, runner):
        """Testa CLI sem argumentos - deve mostrar ajuda."""
        result = runner.invoke(cli)
        assert result.exit_code == 0  # ✅ Click mostra ajuda automaticamente
        assert 'Usage:' in result.output or 'Commands:' in result.output  # ✅ Verifica se mostra ajuda

    def test_cli_help(self, runner):
        """Testa comando --help."""
        result = runner.invoke(cli, ['--help'])
        assert result.exit_code == 0
        assert 'PDF to Markdown Converter' in result.output or 'Usage:' in result.output

    def test_cli_version(self, runner):
        """Testa comando --version."""
        result = runner.invoke(cli, ['--version'])
        assert result.exit_code == 0
        assert '1.0.0' in result.output

    def test_converter_sem_arquivo(self, runner):
        """Testa converter sem especificar arquivo."""
        result = runner.invoke(cli, ['converter'])
        assert result.exit_code != 0  # ✅ Deve dar erro
        assert 'Error' in result.output or 'Missing argument' in result.output

    def test_converter_arquivo_inexistente(self, runner):
        """Testa converter com arquivo inexistente."""
        result = runner.invoke(cli, ['converter', 'inexistente.pdf'])
        assert result.exit_code != 0
        # A mensagem pode variar
        assert 'não encontrado' in result.output.lower() or 'not found' in result.output.lower() or 'does not exist' in result.output.lower()

    def test_converter_arquivo_nao_pdf(self, runner, tmp_path):
        """Testa converter com arquivo que não é PDF."""
        arquivo_txt = tmp_path / "teste.txt"
        arquivo_txt.write_text("teste")

        result = runner.invoke(cli, ['converter', str(arquivo_txt)])
        assert result.exit_code != 0
        # A mensagem pode variar
        assert 'PDF' in result.output or 'inválido' in result.output.lower() or 'invalid' in result.output.lower()

    def test_converter_sucesso(self, runner, pdf_teste, tmp_path):
        """Testa conversão bem-sucedida."""
        if not pdf_teste.exists():
            pytest.skip("Arquivo de teste não encontrado")

        result = runner.invoke(cli, [
            'converter',
            str(pdf_teste),
            '-o', str(tmp_path)
        ])

        assert result.exit_code == 0
        assert 'sucesso' in result.output.lower() or 'success' in result.output.lower()

    def test_converter_com_verbose(self, runner, pdf_teste, tmp_path):
        """Testa conversão com modo verbose."""
        if not pdf_teste.exists():
            pytest.skip("Arquivo de teste não encontrado")

        result = runner.invoke(cli, [
            'converter',
            str(pdf_teste),
            '-o', str(tmp_path),
            '--verbose'
        ])

        assert result.exit_code == 0
        # Em modo verbose, deve mostrar mais informações
        assert 'Processada página' in result.output or 'página' in result.output.lower()

    def test_info_command(self, runner):
        """Testa comando info."""
        result = runner.invoke(cli, ['info'])
        assert result.exit_code == 0
        assert 'PDF to Markdown Converter' in result.output or 'Versão' in result.output

    def test_validar_comando(self, runner, pdf_teste):
        """Testa comando validar."""
        if not pdf_teste.exists():
            pytest.skip("Arquivo de teste não encontrado")

        result = runner.invoke(cli, ['validar', str(pdf_teste)])
        assert result.exit_code == 0
        assert 'válido' in result.output.lower() or 'valid' in result.output.lower()
