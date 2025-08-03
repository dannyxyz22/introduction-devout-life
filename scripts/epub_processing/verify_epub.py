#!/usr/bin/env python3
"""
Script para verificar a estrutura dos EPUBs gerados
"""

import zipfile
import os

def verify_epub_structure(epub_path):
    """
    Verifica a estrutura de um arquivo EPUB
    """
    print(f"\n📚 Verificando: {os.path.basename(epub_path)}")
    print("=" * 50)
    
    try:
        with zipfile.ZipFile(epub_path, 'r') as epub:
            files = epub.namelist()
            
            # Verificar arquivos essenciais
            essential_files = [
                'mimetype',
                'META-INF/container.xml',
                'OEBPS/content.opf',
                'OEBPS/toc.ncx',
                'OEBPS/license.xhtml'
            ]
            
            print("📂 Arquivos essenciais:")
            for file in essential_files:
                if file in files:
                    print(f"   ✅ {file}")
                else:
                    print(f"   ❌ {file} (não encontrado)")
            
            # Contar capítulos
            chapters = [f for f in files if f.startswith('OEBPS/text/chapter-') and f.endswith('.xhtml')]
            print(f"\n📖 Capítulos encontrados: {len(chapters)}")
            
            # Verificar se licença está no manifest
            try:
                content_opf = epub.read('OEBPS/content.opf').decode('utf-8')
                if 'id="license"' in content_opf and 'href="license.xhtml"' in content_opf:
                    print("   ✅ Licença no manifest")
                else:
                    print("   ❌ Licença não encontrada no manifest")
                
                if 'idref="license"' in content_opf:
                    print("   ✅ Licença no spine")
                else:
                    print("   ❌ Licença não encontrada no spine")
            except Exception as e:
                print(f"   ❌ Erro ao verificar content.opf: {e}")
            
            # Verificar se licença está no NCX
            try:
                toc_ncx = epub.read('OEBPS/toc.ncx').decode('utf-8')
                if 'src="license.xhtml"' in toc_ncx:
                    print("   ✅ Licença no índice de navegação")
                else:
                    print("   ❌ Licença não encontrada no índice")
            except Exception as e:
                print(f"   ❌ Erro ao verificar toc.ncx: {e}")
            
            # Tamanho do arquivo
            file_size = os.path.getsize(epub_path) / (1024 * 1024)
            print(f"\n📊 Tamanho: {file_size:.2f} MB")
            
    except Exception as e:
        print(f"❌ Erro ao verificar EPUB: {e}")

def main():
    """
    Função principal
    """
    print("🔍 VERIFICADOR DE ESTRUTURA EPUB")
    print("=" * 40)
    
    # Verificar pasta output
    output_dir = os.path.join('..', '..', 'output')
    if not os.path.exists(output_dir):
        print(f"❌ Pasta output não encontrada: {output_dir}")
        return
    
    # Procurar arquivos EPUB
    epub_files = []
    for file in os.listdir(output_dir):
        if file.endswith('.epub'):
            epub_files.append(os.path.join(output_dir, file))
    
    if not epub_files:
        print(f"❌ Nenhum arquivo EPUB encontrado em {output_dir}")
        return
    
    print(f"📂 Encontrados {len(epub_files)} arquivo(s) EPUB:")
    
    # Verificar cada EPUB
    for epub_path in epub_files:
        verify_epub_structure(epub_path)
    
    print(f"\n🎉 Verificação concluída!")

if __name__ == "__main__":
    main()
