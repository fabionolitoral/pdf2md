#!/usr/bin/env python3
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter

c = canvas.Canvas('tests/fixtures/sample.pdf', pagesize=letter)
c.drawString(100, 750, 'Teste PDF - Conversor')
c.drawString(100, 730, 'Este é um documento de teste')
c.drawString(100, 710, 'Com múltiplas linhas')
c.showPage()
c.save()
print('PDF de teste criado: tests/fixtures/sample.pdf')
