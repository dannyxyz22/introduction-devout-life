#!/usr/bin/env python3
"""
Script para converter arquivo EPUB para JSON estruturado.
Versão atualizada que lê diretamente do arquivo EPUB.
"""

import json
import re
import os
import zipfile
import tempfile
import shutil
from bs4 import BeautifulSoup

def count_words(text):
    """
    Conta palavras em um texto, removendo espaços extras e caracteres especiais.
    
    Args:
        text (str): Texto para contar palavras
        
    Returns:
        int: Número de palavras
    """
    if not text or not isinstance(text, str):
        return 0
    
    # Remove espaços extras e quebras de linha
    cleaned_text = ' '.join(text.strip().split())
    
    # Conta palavras (divide por espaços)
    if cleaned_text:
        return len(cleaned_text.split())
    return 0

def extract_epub(epub_path, extract_dir):
    """Extrai conteúdo do EPUB para diretório temporário"""
    with zipfile.ZipFile(epub_path, 'r') as epub:
        epub.extractall(extract_dir)
    return extract_dir

def find_content_files(extract_dir):
    """Encontra arquivos de conteúdo no EPUB extraído"""
    content_files = []
    
    # Procura por arquivos XML/XHTML de conteúdo
    for root, dirs, files in os.walk(extract_dir):
        for file in files:
            if file.endswith(('.xml', '.xhtml', '.html')):
                file_path = os.path.join(root, file)
                # Verifica se é um arquivo de conteúdo (não navegação)
                if 'content' in file.lower() or 'chapter' in file.lower():
                    content_files.append(file_path)
    
    # Ordena os arquivos por nome para manter ordem
    content_files.sort()
    return content_files

def process_epub_to_json(epub_path, output_json_path=None):
    """
    Converte arquivo EPUB para JSON estruturado com word_count automático
    """
    if not output_json_path:
        output_json_path = 'webapp/public/data/livro_en.json'  # Gera diretamente livro_en.json
    
    print(f"📚 Processando EPUB: {epub_path}")
    
    # Cria diretório temporário
    with tempfile.TemporaryDirectory() as temp_dir:
        # Extrai EPUB
        extract_dir = extract_epub(epub_path, temp_dir)
        print(f"   📂 EPUB extraído para: {extract_dir}")
        
        # Encontra arquivos de conteúdo
        content_files = find_content_files(extract_dir)
        print(f"   📄 Arquivos de conteúdo encontrados: {len(content_files)}")
        
        if not content_files:
            print("   ❌ Nenhum arquivo de conteúdo encontrado!")
            return False
        
        book_structure = []
        
        # Processa cada arquivo
        for i, file_path in enumerate(content_files):
            print(f"   📖 Processando: {os.path.basename(file_path)}")
            
            try:
                with open(file_path, 'r', encoding='utf-8') as f:
                    content = f.read()
                
                soup = BeautifulSoup(content, 'html.parser')
                
                # Determina título da parte
                part_title = f"Part {i + 1}"
                
                # Tenta encontrar título no conteúdo
                title_elem = soup.find(['h1', 'h2', 'title'])
                if title_elem:
                    potential_title = title_elem.get_text().strip()
                    if potential_title and len(potential_title) < 200:
                        part_title = potential_title
                
                current_part = {
                    "part_title": part_title,
                    "chapters": []
                }
                
                # Processa elementos do arquivo
                all_elements = soup.find_all(['p', 'div', 'h1', 'h2', 'h3'])
                current_chapter = None
                
                for element in all_elements:
                    text_content = element.get_text().strip()
                    if not text_content:
                        continue
                    
                    # Detecta títulos de capítulo
                    is_chapter_title = (
                        re.match(r'^CHAPTER\s+[IVXLCDM]+', text_content, re.IGNORECASE) or
                        re.match(r'^Chapter\s+\d+', text_content, re.IGNORECASE) or
                        element.name in ['h1', 'h2'] and len(text_content) < 100
                    )
                    
                    if is_chapter_title:
                        current_chapter = {
                            "chapter_title": text_content,
                            "content": []
                        }
                        current_part["chapters"].append(current_chapter)
                        continue
                    
                    # Adiciona conteúdo
                    if element.name == 'p' and text_content:
                        # Se não há capítulo atual, cria um
                        if not current_chapter:
                            current_chapter = {
                                "chapter_title": "Content",
                                "content": []
                            }
                            current_part["chapters"].append(current_chapter)
                        
                        # Limpa e adiciona texto
                        cleaned_text = re.sub(r'\s+', ' ', text_content).strip()
                        if cleaned_text and len(cleaned_text) > 10:  # Ignora textos muito curtos
                            # Conta palavras no texto
                            word_count = count_words(cleaned_text)
                            
                            current_chapter["content"].append({
                                "type": "p",
                                "content": cleaned_text,
                                "word_count": word_count
                            })
                
                # Só adiciona a parte se tiver conteúdo
                if current_part["chapters"]:
                    book_structure.append(current_part)
                    
            except Exception as e:
                print(f"   ⚠️ Erro ao processar {file_path}: {e}")
                continue
        
        # Salva JSON com word_count incluído
        # Final recomputation of word_count to guarantee consistency
        def _recompute_counts(struct):
            items = 0
            for part in struct:
                for ch in part.get('chapters', []):
                    for it in ch.get('content', []):
                        if isinstance(it, dict) and 'content' in it:
                            it['word_count'] = count_words(it.get('content', ''))
                            items += 1
            return items
        items_recomputed = _recompute_counts(book_structure)
        os.makedirs(os.path.dirname(output_json_path), exist_ok=True)
        with open(output_json_path, 'w', encoding='utf-8') as f:
            json.dump(book_structure, f, indent=2, ensure_ascii=False)
        print(f"   🔢 word_count recalculado em {items_recomputed} itens")
        
        print(f"\n✅ JSON criado com sucesso!")
        print(f"   📂 Arquivo: {output_json_path}")
        print(f"   📚 Partes processadas: {len(book_structure)}")
        
        # Estatísticas
        total_chapters = sum(len(part["chapters"]) for part in book_structure)
        total_content_items = sum(
            len(chapter["content"]) 
            for part in book_structure 
            for chapter in part["chapters"]
        )
        total_words = sum(
            item.get("word_count", 0) 
            for part in book_structure 
            for chapter in part["chapters"] 
            for item in chapter["content"]
        )
        
        print(f"   📖 Total de capítulos: {total_chapters}")
        print(f"   📝 Total de itens de conteúdo: {total_content_items}")
        print(f"   📊 Total de palavras: {total_words:,}")
        print(f"   ✅ Arquivo compatível com todos os scripts (inclui word_count)")
        
        return True

def main():
    """Função principal"""
    print("📚 CONVERSOR EPUB → JSON (com word_count automático)")
    print("=" * 55)
    
    # Procura arquivo EPUB
    epub_files = []
    for file in os.listdir('.'):
        if file.endswith('.epub'):
            epub_files.append(file)
    
    if not epub_files:
        print("❌ Nenhum arquivo EPUB encontrado na pasta atual!")
        return
    
    if len(epub_files) == 1:
        epub_file = epub_files[0]
        print(f"📖 Arquivo EPUB encontrado: {epub_file}")
    else:
        print("📖 Arquivos EPUB encontrados:")
        for i, file in enumerate(epub_files):
            print(f"   {i+1}. {file}")
        
        try:
            choice = int(input("\nEscolha o arquivo (número): ")) - 1
            epub_file = epub_files[choice]
        except (ValueError, IndexError):
            print("❌ Escolha inválida!")
            return
    
    # Processa o arquivo
    success = process_epub_to_json(epub_file)
    
    if success:
        print("\n🎉 Conversão concluída com sucesso!")
    else:
        print("\n❌ Erro na conversão!")

if __name__ == "__main__":
    main()
