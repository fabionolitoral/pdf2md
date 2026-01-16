#!/usr/bin/env python3
"""
Ponto de entrada principal da aplicação CLI.
"""

import sys
from pdf2md.cli.commands import cli

def main():
    """Função principal de entrada."""
    try:
        cli()
    except KeyboardInterrupt:
        print("\n⚠️  Operação cancelada pelo usuário.")
        sys.exit(1)
    except Exception as e:
        print(f"❌ Erro fatal: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
