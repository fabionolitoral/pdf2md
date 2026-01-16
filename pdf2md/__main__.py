#!/usr/bin/env python3
"""
Ponto de entrada principal da aplicação CLI.
"""

import sys
print("DEBUG: __main__.py foi carregado")  # DEBUG

from pdf2md.cli.commands import cli

def main():
    """Função principal de entrada."""
    print("DEBUG: main() foi chamada")  # DEBUG
    try:
        cli()
    except KeyboardInterrupt:
        print("\n⚠️  Operação cancelada pelo usuário.")
        sys.exit(1)
    except Exception as e:
        print(f"❌ Erro fatal: {e}")
        import traceback
        traceback.print_exc()  # Mostra o stack trace completo
        sys.exit(1)

if __name__ == "__main__":
    print("DEBUG: Executando como __main__")  # DEBUG
    main()
