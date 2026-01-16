#!/usr/bin/env python3
"""Script para criar um PDF de teste simples."""

from pathlib import Path

def criar_pdf_teste():
    """Cria um PDF de teste básico."""
    try:
        from reportlab.pdfgen import canvas
        from reportlab.lib.pagesizes import letter

        # Garantir que o diretório existe
        fixtures_dir = Path(__file__).parent
        fixtures_dir.mkdir(parents=True, exist_ok=True)

        # Caminho do arquivo
        pdf_path = fixtures_dir / 'sample.pdf'

        # Criar PDF
        c = canvas.Canvas(str(pdf_path), pagesize=letter)

        # Adicionar conteúdo
        c.setFont("Helvetica", 12)
        c.drawString(100, 750, 'PDF de Teste - Conversor PDF → Markdown')
        c.drawString(100, 730, '')
        c.drawString(100, 710, 'Este é um documento de teste.')
        c.drawString(100, 690, 'Contém texto simples para validar a conversão.')
        c.drawString(100, 670, '')
        c.drawString(100, 650, 'Linha 1')
        c.drawString(100, 630, 'Linha 2')
        c.drawString(100, 610, 'Linha 3')

        c.save()

        print(f'✅ PDF criado com sucesso: {pdf_path}')
        return pdf_path

    except ImportError:
        print('❌ Erro: reportlab não está instalado')
        print('Execute: pip install reportlab')
        return None

if __name__ == '__main__':
    criar_pdf_teste()
