#!/usr/bin/env python3
"""
Script para testar a compatibilidade dos EPUBs com leitores
"""

import zipfile
import os
import xml.etree.ElementTree as ET

def test_epub_compatibility(epub_path):
    """
    Testa compatibilidade do EPUB
    """
    print(f"\n📚 Testando: {os.path.basename(epub_path)}")
    print("=" * 50)
    
    issues = []
    
    try:
        with zipfile.ZipFile(epub_path, 'r') as epub:
            # 1. Verificar mimetype
            if 'mimetype' in epub.namelist():
                mimetype = epub.read('mimetype').decode('utf-8').strip()
                if mimetype == 'application/epub+zip':
                    print("✅ Mimetype correto")
                else:
                    issues.append(f"Mimetype incorreto: {mimetype}")
            else:
                issues.append("Arquivo mimetype não encontrado")
            
            # 2. Verificar container.xml
            if 'META-INF/container.xml' in epub.namelist():
                try:
                    container_content = epub.read('META-INF/container.xml').decode('utf-8')
                    container_root = ET.fromstring(container_content)
                    print("✅ Container.xml válido")
                except ET.ParseError as e:
                    issues.append(f"Container.xml inválido: {e}")
            else:
                issues.append("Container.xml não encontrado")
            
            # 3. Verificar content.opf
            if 'OEBPS/content.opf' in epub.namelist():
                try:
                    opf_content = epub.read('OEBPS/content.opf').decode('utf-8')
                    opf_root = ET.fromstring(opf_content)
                    
                    # Verificar metadados obrigatórios
                    metadata = opf_root.find('.//{http://www.idpf.org/2007/opf}metadata')
                    if metadata is not None:
                        title = metadata.find('.//{http://purl.org/dc/elements/1.1/}title')
                        identifier = metadata.find('.//{http://purl.org/dc/elements/1.1/}identifier')
                        language = metadata.find('.//{http://purl.org/dc/elements/1.1/}language')
                        
                        if title is not None and identifier is not None and language is not None:
                            print("✅ Metadados obrigatórios presentes")
                        else:
                            issues.append("Metadados obrigatórios ausentes")
                    
                    print("✅ Content.opf válido")
                except ET.ParseError as e:
                    issues.append(f"Content.opf inválido: {e}")
            else:
                issues.append("Content.opf não encontrado")
            
            # 4. Verificar toc.ncx
            if 'OEBPS/toc.ncx' in epub.namelist():
                try:
                    ncx_content = epub.read('OEBPS/toc.ncx').decode('utf-8')
                    ncx_root = ET.fromstring(ncx_content)
                    print("✅ Toc.ncx válido")
                except ET.ParseError as e:
                    issues.append(f"Toc.ncx inválido: {e}")
            else:
                issues.append("Toc.ncx não encontrado")
            
            # 5. Verificar licença
            if 'OEBPS/license.xhtml' in epub.namelist():
                try:
                    license_content = epub.read('OEBPS/license.xhtml').decode('utf-8')
                    license_root = ET.fromstring(license_content)
                    print("✅ License.xhtml válido")
                except ET.ParseError as e:
                    issues.append(f"License.xhtml inválido: {e}")
            else:
                issues.append("License.xhtml não encontrado")
            
            # 6. Testar alguns capítulos
            chapter_files = [f for f in epub.namelist() if f.startswith('OEBPS/text/chapter-')]
            valid_chapters = 0
            for i, chapter_file in enumerate(chapter_files[:5]):  # Testar 5 primeiros
                try:
                    chapter_content = epub.read(chapter_file).decode('utf-8')
                    chapter_root = ET.fromstring(chapter_content)
                    valid_chapters += 1
                except ET.ParseError as e:
                    issues.append(f"{chapter_file} inválido: {e}")
            
            print(f"✅ {valid_chapters}/{min(5, len(chapter_files))} capítulos testados são válidos")
            
    except Exception as e:
        issues.append(f"Erro ao abrir EPUB: {e}")
    
    # Resultado final
    if not issues:
        print(f"\n🎉 EPUB completamente compatível!")
        print(f"   📱 Deve funcionar em Calibre, Adobe Digital Editions, etc.")
    else:
        print(f"\n⚠️ Problemas encontrados:")
        for issue in issues:
            print(f"   ❌ {issue}")

def main():
    """
    Função principal
    """
    print("🔍 TESTE DE COMPATIBILIDADE EPUB")
    print("=" * 40)
    
    import sys
    
    # Se foi passado um arquivo como argumento, usar ele
    if len(sys.argv) > 1:
        epub_path = sys.argv[1]
        if os.path.exists(epub_path):
            test_epub_compatibility(epub_path)
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
    
    # Testar cada EPUB
    for epub_path in epub_files:
        test_epub_compatibility(epub_path)
    
    print(f"\n🎯 RESUMO:")
    print(f"   📚 {len(epub_files)} arquivo(s) EPUB testado(s)")
    print(f"   🔧 Se houver problemas, eles foram listados acima")

if __name__ == "__main__":
    main()
