#!/usr/bin/env python3
"""
Script wrapper para gerar livro_en.json com word_count automático.
Este script facilita a geração do JSON principal sempre com contagem de palavras.
"""

import os
import sys

# Adiciona o diretório do script ao path para imports
script_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.append(script_dir)

# Importa a classe processadora
try:
    from scripts.epub_processing.epub_to_json_processor import EpubToJsonProcessor
except ImportError:
    print("❌ Erro: Não foi possível importar o processador EPUB.")
    print("   Certifique-se de que o arquivo epub_to_json_processor.py existe em scripts/epub_processing/")
    sys.exit(1)

def main():
    """
    Função principal que sempre gera livro_en.json com word_count
    """
    print("📚 GERADOR LIVRO_EN.JSON COM WORD_COUNT AUTOMÁTICO")
    print("=" * 55)
    print("   ✅ Este script sempre inclui word_count no JSON gerado")
    print("   ✅ Compatível com todos os scripts existentes")
    print("   ✅ Gera diretamente livro_en.json")
    
    # Cria instância do processador
    processor = EpubToJsonProcessor()
    
    # Processa arquivo EPUB
    success = processor.process_from_file()
    
    if success:
        print("\n🎉 GERAÇÃO CONCLUÍDA!")
        print("   📂 Arquivo: webapp/public/data/livro_en.json")
        print("   ✅ Word count incluído automaticamente")
        print("   ✅ Pronto para usar em todos os scripts do pipeline")
    else:
        print("\n❌ Erro na geração do arquivo!")
        sys.exit(1)

if __name__ == "__main__":
    main()
