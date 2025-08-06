#!/usr/bin/env python3
"""
Script para reorganizar o livro_en.json conforme a estrutura correta do summary.csv
"""

import json
import csv
import os

def read_summary_csv():
    """Lê o summary.csv e organiza por partes"""
    parts = {}
    with open('data/summary.csv', 'r', encoding='utf-8') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            part_key = row['Part'].strip()
            if part_key not in parts:
                parts[part_key] = []
            parts[part_key].append({
                'chapter': row['Chapter'].strip(),
                'title': row['Title'].strip(),
                'page': row['Page'].strip()
            })
    return parts

def load_current_json():
    """Carrega o JSON atual"""
    with open('webapp/public/data/livro_en.json', 'r', encoding='utf-8') as f:
        return json.load(f)

def extract_special_sections(current_data):
    """Extrai seções especiais (title page, dedicatory prayer, preface)"""
    sections = {
        'title_page': None,
        'dedicatory_prayer': None,
        'preface': None
    }
    
    # Primeira parte contém title page, dedicatory prayer e preface
    first_part = current_data[0]
    
    # O primeiro capítulo "Content" tem informações gerais
    content_chapter = first_part['chapters'][0]
    
    # Procurar pela oração dedicatória
    for paragraph in content_chapter['content']:
        if 'DEDICATORY PRAYER' in paragraph.get('content', ''):
            # Esta seção contém a dedicatory prayer
            prayer_content = []
            start_collecting = False
            
            for p in content_chapter['content']:
                if 'DEDICATORY PRAYER' in p.get('content', ''):
                    start_collecting = True
                    continue
                if start_collecting and 'St. Francis de Sales' in p.get('content', ''):
                    prayer_content.append(p)
                    break
                if start_collecting:
                    prayer_content.append(p)
            
            sections['dedicatory_prayer'] = {
                'chapter_title': 'DEDICATORY PRAYER',
                'content': prayer_content
            }
            break
    
    # Extrair o preface (todo o resto até "PART THE FIRST")
    preface_content = []
    collecting_preface = False
    
    for paragraph in content_chapter['content']:
        content_text = paragraph.get('content', '')
        if 'Dear reader, I pray you to read this Preface' in content_text:
            collecting_preface = True
        if collecting_preface and 'PART THE FIRST' not in content_text:
            preface_content.append(paragraph)
        elif 'PART THE FIRST' in content_text:
            break
    
    sections['preface'] = {
        'chapter_title': 'PREFACE',
        'content': preface_content
    }
    
    # Title page - só a primeira parte antes da oração
    title_content = []
    for paragraph in content_chapter['content']:
        content_text = paragraph.get('content', '')
        if 'DEDICATORY PRAYER' in content_text:
            break
        if 'This is a digital copy' in content_text:
            title_content.append(paragraph)
    
    sections['title_page'] = {
        'chapter_title': 'TITLE PAGE',
        'content': title_content
    }
    
    return sections

def find_chapter_content(current_data, chapter_title):
    """Encontra o conteúdo de um capítulo no JSON atual"""
    for part in current_data:
        for chapter in part['chapters']:
            if chapter_title.upper() in chapter['chapter_title'].upper():
                return chapter
    return None

def organize_chapters_by_parts(current_data, parts_structure):
    """Organiza os capítulos conforme a estrutura das partes"""
    organized_parts = []
    
    # Mapear os títulos das partes
    part_titles = {
        'Part I': 'PART THE FIRST - INSTRUCTIONS AND EXERCISES FOR CONDUCTING THE SOUL FROM HER FIRST DESIRE FOR A DEVOUT LIFE TILL SHE IS BROUGHT TO A FULL RESOLUTION OF EMBRACING IT',
        'Part II': 'PART THE SECOND - INSTRUCTIONS FOR ELEVATING THE SOUL TO GOD BY PRAYER AND BY THE SACRAMENTS',
        'Part III': 'PART THE THIRD - INSTRUCTIONS CONCERNING THE PRACTICE OF THE VIRTUES',
        'Part IV': 'PART THE FOURTH - NECESSARY ADVICE AGAINST THE MOST ORDINARY TEMPTATIONS',
        'Part V': 'PART THE FIFTH - INSTRUCTIONS AND EXERCISES NECESSARY FOR RENEWING THE SOUL, AND CONFIRMING HER IN DEVOTION'
    }
    
    for part_key in ['Part I', 'Part II', 'Part III', 'Part IV', 'Part V']:
        if part_key in parts_structure:
            part_chapters = []
            
            for chapter_info in parts_structure[part_key]:
                chapter_num = chapter_info['chapter']
                chapter_title = chapter_info['title']
                
                # Buscar o capítulo correspondente no JSON atual
                found_chapter = None
                
                # Tentar diferentes formas de buscar o capítulo
                search_patterns = [
                    f"CHAPTER {chapter_num}",
                    f"Chapter {chapter_num}",
                    chapter_title[:30]  # Primeiras 30 palavras do título
                ]
                
                for pattern in search_patterns:
                    found_chapter = find_chapter_content(current_data, pattern)
                    if found_chapter:
                        break
                
                if found_chapter:
                    # Criar capítulo com título completo
                    chapter_data = {
                        'chapter_title': f"CHAPTER {chapter_num}. {chapter_title}",
                        'content': found_chapter['content']
                    }
                    part_chapters.append(chapter_data)
                else:
                    print(f"AVISO: Capítulo {chapter_num} da {part_key} não encontrado: {chapter_title}")
            
            # Criar a parte
            part_data = {
                'part_title': part_titles[part_key],
                'chapters': part_chapters
            }
            organized_parts.append(part_data)
    
    return organized_parts

def create_new_json_structure():
    """Cria a nova estrutura JSON"""
    print("Carregando estrutura do CSV...")
    parts_structure = read_summary_csv()
    
    print("Carregando JSON atual...")
    current_data = load_current_json()
    
    print("Extraindo seções especiais...")
    special_sections = extract_special_sections(current_data)
    
    print("Organizando capítulos por partes...")
    organized_parts = organize_chapters_by_parts(current_data, parts_structure)
    
    # Criar a nova estrutura
    new_structure = []
    
    # 1. Title Page
    if special_sections['title_page']:
        title_part = {
            'part_title': 'TITLE PAGE',
            'chapters': [special_sections['title_page']]
        }
        new_structure.append(title_part)
    
    # 2. Dedicatory Prayer
    if special_sections['dedicatory_prayer']:
        prayer_part = {
            'part_title': 'DEDICATORY PRAYER',
            'chapters': [special_sections['dedicatory_prayer']]
        }
        new_structure.append(prayer_part)
    
    # 3. Preface
    if special_sections['preface']:
        preface_part = {
            'part_title': 'PREFACE',
            'chapters': [special_sections['preface']]
        }
        new_structure.append(preface_part)
    
    # 4. As cinco partes do livro
    new_structure.extend(organized_parts)
    
    return new_structure

def main():
    """Função principal"""
    try:
        print("Iniciando reorganização do JSON...")
        
        # Backup do arquivo original
        print("Criando backup...")
        import shutil
        shutil.copy2('webapp/public/data/livro_en.json', 'webapp/public/data/livro_en.json.backup')
        
        # Criar nova estrutura
        new_structure = create_new_json_structure()
        
        # Salvar novo arquivo
        print("Salvando novo JSON...")
        with open('webapp/public/data/livro_en.json', 'w', encoding='utf-8') as f:
            json.dump(new_structure, f, indent=2, ensure_ascii=False)
        
        print("✅ JSON reorganizado com sucesso!")
        print(f"Total de partes criadas: {len(new_structure)}")
        
        # Mostrar resumo
        for i, part in enumerate(new_structure):
            print(f"Parte {i+1}: {part['part_title']} - {len(part['chapters'])} capítulos")
    
    except Exception as e:
        print(f"❌ Erro durante a reorganização: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()
