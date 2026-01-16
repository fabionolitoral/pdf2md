"""
Testes para o conversor em lote.
"""

import pytest
from pathlib import Path
from pdf2md.core.batch_converter import BatchConverter


class TestBatchConverter:
    """Testes para conversão em lote."""

    @pytest.fixture
    def pasta_pdfs(self, tmp_path):
        """Cria pasta com PDFs de teste."""
        pasta = tmp_path / "pdfs"
        pasta.mkdir()

        # Criar PDFs fictícios (você pode copiar o sample.pdf)
        for i in range(3):
            pdf = pasta / f"teste_{i}.pdf"
            pdf.write_bytes(b"%PDF-1.4\n%fake")

        return pasta

    def test_batch_inicializacao(self, pasta_pdfs, tmp_path):
        """Testa inicialização do conversor em lote."""
        saida = tmp_path / "output"

        batch = BatchConverter(
            diretorio_entrada=pasta_pdfs,
            diretorio_saida=saida
        )

        assert batch.diretorio_entrada == pasta_pdfs
        assert batch.diretorio_saida == saida
        assert saida.exists()

    def test_batch_listar_pdfs(self, pasta_pdfs, tmp_path):
        """Testa listagem de PDFs."""
        batch = BatchConverter(
            diretorio_entrada=pasta_pdfs,
            diretorio_saida=tmp_path / "output"
        )

        pdfs = batch.listar_pdfs()

        assert len(pdfs) == 3
        assert all(pdf.suffix == '.pdf' for pdf in pdfs)

    def test_batch_diretorio_inexistente(self, tmp_path):
        """Testa erro com diretório inexistente."""
        with pytest.raises(FileNotFoundError):
            BatchConverter(
                diretorio_entrada=tmp_path / "nao_existe",
                diretorio_saida=tmp_path / "output"
            )
