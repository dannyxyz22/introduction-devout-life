#!/usr/bin/env python3
"""
Script para validar XML dos EPUBs
"""

import xml.etree.ElementTree as ET
import zipfile
import os

def validate_xml_content(xml_content, filename):
    """
    Valida conteúdo XML
    """
    try:
        ET.fromstring(xml_content)
        print(f"✅ {filename} - XML válido")
        return True
    except ET.ParseError as e:
        print(f"❌ {filename} - Erro XML: {e}")
        # Mostrar a linha com erro
        lines = xml_content.split('\n')
        if hasattr(e, 'lineno') and e.lineno <= len(lines):
            error_line = lines[e.lineno - 1] if e.lineno > 0 else "Linha não encontrada"
            print(f"   Linha {e.lineno}: {error_line}")
        return False

def validate_epub(epub_path):
    """
    Valida arquivos XML dentro do EPUB
    """
    print(f"\n🔍 Validando: {os.path.basename(epub_path)}")
    print("=" * 50)
    
    try:
        with zipfile.ZipFile(epub_path, 'r') as epub:
            xml_files = [
                'OEBPS/content.opf',
                'OEBPS/toc.ncx', 
                'OEBPS/license.xhtml',
                'OEBPS/title_page.xhtml',
                'OEBPS/dedicatory_prayer.xhtml',
                'OEBPS/preface.xhtml'
            ]
            
            # Adicionar capítulos
            chapter_files = [f for f in epub.namelist() if f.startswith('OEBPS/text/chapter-')]
            xml_files.extend(chapter_files[:3])  # Validar apenas os primeiros 3 capítulos
            
            all_valid = True
            for xml_file in xml_files:
                if xml_file in epub.namelist():
                    content = epub.read(xml_file).decode('utf-8')
                    if not validate_xml_content(content, xml_file):
                        all_valid = False
                else:
                    print(f"⚠️ {xml_file} - Arquivo não encontrado")
            
            if all_valid:
                print(f"\n🎉 Todos os arquivos XML são válidos!")
            else:
                print(f"\n❌ Alguns arquivos XML têm problemas")
                
    except Exception as e:
        print(f"❌ Erro ao validar EPUB: {e}")

def main():
    """
    Função principal
    """
    print("🔍 VALIDADOR XML PARA EPUB")
    print("=" * 40)
    
    import sys
    
    # Se foi passado um arquivo como argumento, usar ele
    if len(sys.argv) > 1:
        epub_path = sys.argv[1]
        if os.path.exists(epub_path):
            validate_epub(epub_path)
        else:
            print(f"❌ Arquivo não encontrado: {epub_path}")
        return
    
    # Verificar pasta output
    output_dir = os.path.join('..', '..', 'output')
    if not os.path.exists(output_dir):
        print(f"❌ Pasta output não encontrada")
        return
    
    # Procurar arquivos EPUB
    epub_files = []
    for file in os.listdir(output_dir):
        if file.endswith('.epub'):
            epub_files.append(os.path.join(output_dir, file))
    
    if not epub_files:
        print(f"❌ Nenhum arquivo EPUB encontrado")
        return
    
    # Validar cada EPUB
    for epub_path in epub_files:
        validate_epub(epub_path)

if __name__ == "__main__":
    main()
