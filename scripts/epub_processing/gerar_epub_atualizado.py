#!/usr/bin/env python3
"""
Script para gerar arquivo EPUB atualizado a partir do JSON corrigido.
Suporta tanto versão em inglês quanto português.
"""

import json
import os
import zipfile
import shutil
from datetime import datetime
from xml.etree.ElementTree import Element, SubElement, tostring, ElementTree
import xml.etree.ElementTree as ET
from xml.dom import minidom
import html

def prettify_xml(elem):
    """Formata XML de forma legível"""
    rough_string = tostring(elem, 'unicode')
    reparsed = minidom.parseString(rough_string)
    return reparsed.toprettyxml(indent="  ")

def create_xhtml_content(chapter_data, chapter_num, part_num, lang='en'):
    """
    Cria conteúdo XHTML para um capítulo
    """
    # Namespace XHTML
    html = Element('html', xmlns="http://www.w3.org/1999/xhtml")
    head = SubElement(html, 'head')
    
    # Título da página
    title = SubElement(head, 'title')
    if lang == 'pt':
        title.text = f"Parte {part_num} - Capítulo {chapter_num}"
    else:
        title.text = f"Part {part_num} - Chapter {chapter_num}"
    
    # CSS básico
    style = SubElement(head, 'style', type="text/css")
    style.text = """
        body { font-family: serif; line-height: 1.6; margin: 2em; }
        h1 { text-align: center; font-size: 1.8em; margin-bottom: 1em; }
        h2 { text-align: center; font-size: 1.4em; margin: 1.5em 0 1em 0; }
        p { text-align: justify; margin: 1em 0; }
        .chapter-title { font-weight: bold; text-align: center; margin: 2em 0; }
    """
    
    # Corpo do documento
    body = SubElement(html, 'body')
    
    # Título do capítulo
    if chapter_data.get('chapter_title'):
        h1 = SubElement(body, 'h1', {'class': 'chapter-title'})
        h1.text = chapter_data['chapter_title']
    
    # Conteúdo do capítulo
    for content_item in chapter_data.get('content', []):
        content_text = content_item.get('content', '').strip()
        if not content_text:
            continue
            
        content_type = content_item.get('type', 'p')
        
        if content_type == 'h1':
            elem = SubElement(body, 'h1')
        elif content_type == 'h2':
            elem = SubElement(body, 'h2')
        elif content_type == 'h3':
            elem = SubElement(body, 'h3')
        else:
            elem = SubElement(body, 'p')
        
        elem.text = content_text
    
    return prettify_xml(html)

def create_opf_file(book_data, output_dir, lang='en', has_prayer_in_json=False, has_preface_in_json=False):
    """
    Cria arquivo OPF (Open Packaging Format)
    """
    # Namespace
    package = Element('package', 
                     xmlns="http://www.idpf.org/2007/opf",
                     version="2.0",
                     attrib={'unique-identifier': 'BookId'})
    
    # Metadados
    metadata = SubElement(package, 'metadata',
                         attrib={'xmlns:dc': 'http://purl.org/dc/elements/1.1/',
                                'xmlns:opf': 'http://www.idpf.org/2007/opf'})
    
    # Informações do livro
    if lang == 'pt':
        title = SubElement(metadata, 'dc:title')
        title.text = "Filotéia - Introdução à Vida Devota"
        language = SubElement(metadata, 'dc:language')
        language.text = "pt-BR"
        identifier_text = "devout-life-pt-br"
    else:
        title = SubElement(metadata, 'dc:title')
        title.text = "Introduction to the Devout Life"
        language = SubElement(metadata, 'dc:language')
        language.text = "en"
        identifier_text = "devout-life-en"
    
    # Outros metadados
    creator = SubElement(metadata, 'dc:creator', attrib={'opf:role': 'aut'})
    creator.text = "St Francis De Sales"
    
    publisher = SubElement(metadata, 'dc:publisher')
    publisher.text = "Digital Edition"
    
    identifier = SubElement(metadata, 'dc:identifier', attrib={'id': 'BookId'})
    identifier.text = identifier_text
    
    date = SubElement(metadata, 'dc:date')
    date.text = datetime.now().strftime('%Y-%m-%d')
    
    # Metadados da capa (apenas para português)
    if lang == 'pt':
        meta_cover = SubElement(metadata, 'meta', name="cover", content="cover-image")
    
    # Manifest (lista de arquivos)
    manifest = SubElement(package, 'manifest')
    
    # NCX (navegação)
    SubElement(manifest, 'item',
              id="ncx",
              href="toc.ncx",
              attrib={'media-type': 'application/x-dtbncx+xml'})
    
    # Página de licença
    SubElement(manifest, 'item',
              id="license",
              href="license.xhtml",
              attrib={'media-type': 'application/xhtml+xml'})
    
    # Página de título
    SubElement(manifest, 'item',
              id="title-page",
              href="title_page.xhtml",
              attrib={'media-type': 'application/xhtml+xml'})
    
    # Imagem da capa (apenas para português)
    if lang == 'pt':
        SubElement(manifest, 'item',
                  id="cover-image",
                  href="cover.png",
                  attrib={'media-type': 'image/png'})
    
    
    # Arquivos de conteúdo
    file_counter = 1
    file_list = []
    
    for part_idx, part in enumerate(book_data):
        for chapter_idx, chapter in enumerate(part.get('chapters', [])):
            file_id = f"chapter-{file_counter:03d}"
            file_name = f"chapter-{file_counter:03d}.xhtml"
            file_list.append((file_id, file_name))
            
            SubElement(manifest, 'item',
                      id=file_id,
                      href=f"text/{file_name}",
                      attrib={'media-type': 'application/xhtml+xml'})
            file_counter += 1
    
    # Spine (ordem de leitura)
    spine = SubElement(package, 'spine', toc="ncx")
    
    # Adicionar página de título primeiro
    SubElement(spine, 'itemref', idref="title-page")
    
  
    # Depois todos os capítulos
    for file_id, _ in file_list:
        SubElement(spine, 'itemref', idref=file_id)
    
    # Adicionar página de licença no final
    SubElement(spine, 'itemref', idref="license")
    
    return prettify_xml(package), file_list

def create_ncx_file(book_data, lang='en', has_prayer_in_json=False, has_preface_in_json=False):
    """
    Cria arquivo NCX (Navigation Control for XML)
    CORRIGIDO: Sincroniza corretamente play_order com numeração de arquivos
    """
    
    # Define o identificador baseado no idioma
    if lang == 'pt':
        identifier_text = "devout-life-pt-br"
    else:
        identifier_text = "devout-life-en"
    
    ncx = Element('ncx', 
                  xmlns="http://www.daisy.org/z3986/2005/ncx/",
                  version="2005-1")
    
    # Cabeçalho
    head = SubElement(ncx, 'head')
    SubElement(head, 'meta', name="dtb:uid", content=identifier_text)
    SubElement(head, 'meta', name="dtb:depth", content="2")
    SubElement(head, 'meta', name="dtb:totalPageCount", content="0")
    SubElement(head, 'meta', name="dtb:maxPageNumber", content="0")
    
    # Título
    doc_title = SubElement(ncx, 'docTitle')
    text_elem = SubElement(doc_title, 'text')
    if lang == 'pt':
        text_elem.text = "Introdução à Vida Devota"
    else:
        text_elem.text = "Introduction to the Devout Life"
    
    # Mapa de navegação
    nav_map = SubElement(ncx, 'navMap')
    
    play_order = 1
    chapter_file_counter = 1  # Contador separado para arquivos de capítulo
    
    # Adicionar página de título no índice (primeiro item)
    title_nav = SubElement(nav_map, 'navPoint', 
                          id="title-page",
                          playOrder=str(play_order))
    
    title_label = SubElement(title_nav, 'navLabel')
    title_text = SubElement(title_label, 'text')
    if lang == 'pt':
        title_text.text = "Página de Título"
    else:
        title_text.text = "Title Page"
    
    SubElement(title_nav, 'content', src="title_page.xhtml")
    
    play_order += 1
    
    
    for part_idx, part in enumerate(book_data):
        part_title = part.get('part_title', f'Part {part_idx + 1}')
        
        # Navpoint para a parte
        part_nav = SubElement(nav_map, 'navPoint', 
                             id=f"part-{part_idx + 1}",
                             playOrder=str(play_order))
        
        part_label = SubElement(part_nav, 'navLabel')
        part_text = SubElement(part_label, 'text')
        part_text.text = part_title
        
        # Primeiro capítulo da parte como conteúdo
        if part.get('chapters'):
            first_chapter_file = f"text/chapter-{chapter_file_counter:03d}.xhtml"
            SubElement(part_nav, 'content', src=first_chapter_file)
        
        # Capítulos da parte
        for chapter_idx, chapter in enumerate(part.get('chapters', [])):
            chapter_title = chapter.get('chapter_title', f'Chapter {chapter_idx + 1}')
            
            chapter_nav = SubElement(part_nav, 'navPoint',
                                   id=f"chapter-{play_order}",
                                   playOrder=str(play_order))
            
            chapter_label = SubElement(chapter_nav, 'navLabel')
            chapter_text = SubElement(chapter_label, 'text')
            chapter_text.text = chapter_title
            
            # CORREÇÃO: Usar chapter_file_counter para nome do arquivo
            chapter_file = f"text/chapter-{chapter_file_counter:03d}.xhtml"
            SubElement(chapter_nav, 'content', src=chapter_file)
            
            play_order += 1
            chapter_file_counter += 1  # Incrementar contador de arquivo separadamente
    
    # Adicionar página de licença no final do índice
    license_nav = SubElement(nav_map, 'navPoint', 
                            id="license-page",
                            playOrder=str(play_order))
    
    license_label = SubElement(license_nav, 'navLabel')
    license_text = SubElement(license_label, 'text')
    if lang == 'pt':
        license_text.text = "Licença"
    else:
        license_text.text = "License"
    
    SubElement(license_nav, 'content', src="license.xhtml")
    
    return prettify_xml(ncx)

def create_container_xml():
    """
    Cria arquivo container.xml
    """
    container = Element('container',
                       version="1.0",
                       xmlns="urn:oasis:names:tc:opendocument:xmlns:container")
    
    rootfiles = SubElement(container, 'rootfiles')
    SubElement(rootfiles, 'rootfile',
              attrib={'full-path': 'OEBPS/content.opf',
                     'media-type': 'application/oebps-package+xml'})
    
    return prettify_xml(container)

def generate_epub(json_file, output_epub, lang='en'):
    """
    Gera arquivo EPUB a partir do JSON
    """
    print(f"📚 Gerando EPUB em {'português' if lang == 'pt' else 'inglês'}...")
    print(f"   📂 Fonte: {json_file}")
    print(f"   📂 Destino: {output_epub}")
    
    # Carrega dados do JSON
    with open(json_file, 'r', encoding='utf-8') as f:
        book_data = json.load(f)
    
    # Detecta se o JSON já contém oração dedicatória e prefácio
    has_prayer_in_json = False
    has_preface_in_json = False
    
    # Verifica se há oração dedicatória no conteúdo
    for part_idx, part in enumerate(book_data):
        # Verifica no título da parte
        part_title = part.get('part_title', '').upper()
        if ('ORAÇÃO' in part_title and 'DEDICATÓRIA' in part_title) or \
           ('DEDICATORY' in part_title and 'PRAYER' in part_title):
            has_prayer_in_json = True
            print(f"   ✅ Oração dedicatória detectada no JSON (título da parte)")
        
        if ('PREFÁCIO' in part_title) or ('PREFACE' in part_title):
            has_preface_in_json = True
            print(f"   ✅ Prefácio detectado no JSON (título da parte)")
            
        for chap_idx, chapter in enumerate(part.get('chapters', [])):
            # Verifica no título do capítulo
            chapter_title = chapter.get('chapter_title', '').upper()
            if ('ORAÇÃO' in chapter_title and 'DEDICATÓRIA' in chapter_title) or \
               ('DEDICATORY' in chapter_title and 'PRAYER' in chapter_title):
                has_prayer_in_json = True
                print(f"   ✅ Oração dedicatória detectada no JSON (título do capítulo)")
                
            if ('PREFÁCIO' in chapter_title) or ('PREFACE' in chapter_title):
                has_preface_in_json = True
                print(f"   ✅ Prefácio detectado no JSON (título do capítulo)")
                
            # Verifica no conteúdo dos itens
            for cont_idx, content_item in enumerate(chapter.get('content', [])):
                content_text = content_item.get('content', '').upper()
                
                if ('ORAÇÃO' in content_text and 'DEDICATÓRIA' in content_text) or \
                   ('DEDICATORY' in content_text and 'PRAYER' in content_text):
                    has_prayer_in_json = True
                    print(f"   ✅ Oração dedicatória detectada no JSON (conteúdo)")
                    
                if ('PREFÁCIO' in content_text) or ('PREFACE' in content_text):
                    # Certifica que não é apenas menção do prefácio em outro contexto
                    if len(content_text.strip()) < 200:  # Se for uma linha curta, provavelmente é um título
                        has_preface_in_json = True
                        print(f"   ✅ Prefácio detectado no JSON (conteúdo)")
                        
                if has_prayer_in_json and has_preface_in_json:
                    break
            if has_prayer_in_json and has_preface_in_json:
                break
        if has_prayer_in_json and has_preface_in_json:
            break
    
    # Diretório temporário
    temp_dir = f"temp_epub_{lang}"
    if os.path.exists(temp_dir):
        shutil.rmtree(temp_dir)
    
    os.makedirs(temp_dir)
    os.makedirs(os.path.join(temp_dir, 'META-INF'))
    os.makedirs(os.path.join(temp_dir, 'OEBPS'))
    os.makedirs(os.path.join(temp_dir, 'OEBPS', 'text'))
    
    try:
        # 1. Cria mimetype
        with open(os.path.join(temp_dir, 'mimetype'), 'w') as f:
            f.write('application/epub+zip')
        
        # 2. Cria container.xml
        container_xml = create_container_xml()
        with open(os.path.join(temp_dir, 'META-INF', 'container.xml'), 'w', encoding='utf-8') as f:
            f.write(container_xml)
        
        # 3. Cria arquivo OPF
        opf_content, file_list = create_opf_file(book_data, temp_dir, lang, has_prayer_in_json, has_preface_in_json)
        with open(os.path.join(temp_dir, 'OEBPS', 'content.opf'), 'w', encoding='utf-8') as f:
            f.write(opf_content)
        
        # 4. Cria arquivo NCX
        ncx_content = create_ncx_file(book_data, lang, has_prayer_in_json, has_preface_in_json)
        with open(os.path.join(temp_dir, 'OEBPS', 'toc.ncx'), 'w', encoding='utf-8') as f:
            f.write(ncx_content)
        
        # 5. Copia arquivo de licença
        script_dir = os.path.dirname(os.path.abspath(__file__))
        license_source = os.path.join(script_dir, 'license.xhtml')
        license_dest = os.path.join(temp_dir, 'OEBPS', 'license.xhtml')
        
        if os.path.exists(license_source):
            shutil.copy2(license_source, license_dest)
            print(f"   📄 Licença adicionada: license.xhtml")
        else:
            print(f"   ⚠️ Arquivo de licença não encontrado: {license_source}")
        
        # 6. Copia arquivo de página de título
        if lang == 'pt':
            title_source = os.path.join(script_dir, 'title_page_pt-BR.xhtml')  # Usar versão portuguesa
        else:
            title_source = os.path.join(script_dir, 'title_page_en.xhtml')
        
        title_dest = os.path.join(temp_dir, 'OEBPS', 'title_page.xhtml')
        
        if os.path.exists(title_source):
            shutil.copy2(title_source, title_dest)
            print(f"   📖 Página de título adicionada: title_page.xhtml")
        else:
            print(f"   ⚠️ Arquivo de página de título não encontrado: {title_source}")
        
        # 7. Copia arquivo de capa (apenas para português)
        if lang == 'pt':
            # Localizar o arquivo de capa
            covers_dir = os.path.join(os.path.dirname(os.path.dirname(script_dir)), 'covers')
            cover_source = os.path.join(covers_dir, 'cover_pt-BR.png')
            cover_dest = os.path.join(temp_dir, 'OEBPS', 'cover.png')
            
            if os.path.exists(cover_source):
                shutil.copy2(cover_source, cover_dest)
                print(f"   🖼️ Capa adicionada: cover.png")
            else:
                print(f"   ⚠️ Arquivo de capa não encontrado: {cover_source}")
        
        # 8. Cria arquivos XHTML para cada capítulo
        file_counter = 1
        chapters_created = 0
        
        for part_idx, part in enumerate(book_data):
            for chapter_idx, chapter in enumerate(part.get('chapters', [])):
                file_name = f"chapter-{file_counter:03d}.xhtml"
                file_path = os.path.join(temp_dir, 'OEBPS', 'text', file_name)
                
                xhtml_content = create_xhtml_content(chapter, chapter_idx + 1, part_idx + 1, lang)
                
                with open(file_path, 'w', encoding='utf-8') as f:
                    f.write(xhtml_content)
                
                file_counter += 1
                chapters_created += 1
        
        print(f"   📝 Capítulos criados: {chapters_created}")
        
        # 9. Cria arquivo EPUB (ZIP)
        if os.path.exists(output_epub):
            os.remove(output_epub)
        
        with zipfile.ZipFile(output_epub, 'w', zipfile.ZIP_DEFLATED) as epub:
            # Adiciona mimetype sem compressão (primeiro arquivo)
            epub.write(os.path.join(temp_dir, 'mimetype'), 'mimetype', compress_type=zipfile.ZIP_STORED)
            
            # Adiciona outros arquivos
            for root, dirs, files in os.walk(temp_dir):
                for file in files:
                    if file == 'mimetype':
                        continue  # Já adicionado
                    
                    file_path = os.path.join(root, file)
                    arcname = os.path.relpath(file_path, temp_dir)
                    epub.write(file_path, arcname)
        
        # 10. Limpa diretório temporário
        shutil.rmtree(temp_dir)
        
        # Verifica arquivo criado
        file_size = os.path.getsize(output_epub)
        file_size_mb = file_size / (1024 * 1024)
        
        print(f"\n✅ EPUB criado com sucesso!")
        print(f"   📂 Arquivo: {output_epub}")
        print(f"   📊 Tamanho: {file_size_mb:.2f} MB")
        print(f"   📚 Capítulos: {chapters_created}")
        
        return True
        
    except Exception as e:
        print(f"\n❌ Erro na criação do EPUB:")
        print(f"   {str(e)}")
        
        # Limpa diretório temporário em caso de erro
        if os.path.exists(temp_dir):
            shutil.rmtree(temp_dir)
        
        return False

def main():
    """
    Função principal
    """
    import sys
    
    print("📚 GERADOR DE EPUB ATUALIZADO")
    print("=" * 40)
    
    # Detectar diretório base do projeto
    script_dir = os.path.dirname(os.path.abspath(__file__))
    project_root = os.path.dirname(os.path.dirname(script_dir))
    output_dir = os.path.join(project_root, 'output')
    
    # Garantir que o diretório output existe
    os.makedirs(output_dir, exist_ok=True)
    
    # Arquivos disponíveis
    json_files = {
        'en': os.path.join(output_dir, 'livro_en.json'),
        'pt': os.path.join(output_dir, 'livro_pt-BR.json')
    }
    
    # Verificar arquivos disponíveis
    available_files = {}
    for lang, file_path in json_files.items():
        if os.path.exists(file_path):
            available_files[lang] = file_path
            lang_name = 'Inglês' if lang == 'en' else 'Português'
            print(f"✅ {lang_name}: {file_path}")
        else:
            lang_name = 'Inglês' if lang == 'en' else 'Português'
            print(f"❌ {lang_name}: {file_path} (não encontrado)")
    
    if not available_files:
        print(f"\n❌ Nenhum arquivo JSON encontrado!")
        return
    
    # Se executado com argumento --auto, gera automaticamente ambos os EPUBs disponíveis
    if len(sys.argv) > 1 and sys.argv[1] == '--auto':
        print(f"\n🔄 Gerando EPUBs automaticamente...")
        success_count = 0
        
        if 'en' in available_files:
            if generate_epub(available_files['en'], os.path.join(output_dir, 'Introduction_to_the_Devout_Life_EN.epub'), 'en'):
                success_count += 1
        
        if 'pt' in available_files:
            if generate_epub(available_files['pt'], os.path.join(output_dir, 'Filotéia - Introdução à vida devota pt-BR.epub'), 'pt'):
                success_count += 1
        
        print(f"\n🎉 {success_count} arquivo(s) EPUB gerado(s) com sucesso!")
        return
    
    # Modo interativo
    print(f"\n📋 OPÇÕES:")
    print(f"1. Gerar EPUB em inglês")
    print(f"2. Gerar EPUB em português") 
    print(f"3. Gerar ambos os EPUBs")
    print(f"4. Sair")
    
    choice = input(f"\nEscolha uma opção (1-4): ").strip()
    
    if choice == '1' and 'en' in available_files:
        output_file = os.path.join(output_dir, 'Introduction_to_the_Devout_Life_EN.epub')
        generate_epub(available_files['en'], output_file, 'en')
        
    elif choice == '2' and 'pt' in available_files:
        output_file = os.path.join(output_dir, 'Filotéia - Introdução à vida devota pt-BR.epub')
        generate_epub(available_files['pt'], output_file, 'pt')
        
    elif choice == '3':
        success_count = 0
        
        if 'en' in available_files:
            if generate_epub(available_files['en'], os.path.join(output_dir, 'Introduction_to_the_Devout_Life_EN.epub'), 'en'):
                success_count += 1
        
        if 'pt' in available_files:
            if generate_epub(available_files['pt'], os.path.join(output_dir, 'Filotéia - Introdução à vida devota pt-BR.epub'), 'pt'):
                success_count += 1
        
        print(f"\n🎉 {success_count} arquivo(s) EPUB gerado(s) com sucesso!")
        
    elif choice == '4':
        print("👋 Até logo!")
        
    else:
        print("❌ Opção inválida ou arquivo não disponível!")

if __name__ == "__main__":
    main()
