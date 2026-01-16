from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from reportlab.platypus import Table
from reportlab.platypus import TableStyle
from reportlab.lib import colors
from pathlib import Path

def criar_pdf_completo():
    output = Path(__file__).parent / "sample.pdf"

    c = canvas.Canvas(str(output), pagesize=letter)

    # Texto normal
    c.setFont("Helvetica", 14)
    c.drawString(100, 730, "PDF de Teste - Conversor PDF → Markdown")
    c.drawString(100, 710, "Este PDF contém texto, tabela e imagem.")
    c.drawString(100, 680, "Tabela abaixo:")

    # Criar tabela em texto
    data = [
        ["Nome", "Idade"],
        ["João", "30"],
        ["Maria", "25"],
    ]

    table = Table(data, colWidths=[150, 150])
    table.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), colors.gray),
        ('TEXTCOLOR',  (0,0), (-1,0), colors.white),
        ('ALIGN',      (0,0), (-1,-1), 'CENTER'),
        ('GRID',       (0,0), (-1,-1), 1, colors.black),
    ]))

    table.wrapOn(c, 100, 500)
    table.drawOn(c, 100, 600)

    # Criar imagem fake (um quadrado colorido)
    c.setFillColor(colors.red)
    c.rect(100, 500, 100, 100, fill=True)
    c.drawString(100, 480, "Imagem desenhada (simula imagem real)")

    c.save()
    print(f"PDF criado em: {output}")

if __name__ == "__main__":
    criar_pdf_completo()
