#!/usr/bin/env python3
"""
Script melhorado para reorganizar o livro_en.json conforme a estrutura correta do summary.csv
"""

import json
import csv
import os
import re

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
    content_chapter = first_part['chapters'][0]
    
    # Dividir o conteúdo em seções
    title_page_content = []
    dedicatory_prayer_content = []
    preface_content = []
    
    current_section = 'title'
    
    for paragraph in content_chapter['content']:
        content_text = paragraph.get('content', '')
        
        if 'DEDICATORY PRAYER' in content_text:
            current_section = 'prayer_start'
            continue
        elif current_section == 'prayer_start' and 'O SWEET JESUS' in content_text:
            current_section = 'prayer'
            dedicatory_prayer_content.append(paragraph)
        elif current_section == 'prayer' and 'St. Francis de Sales' in content_text:
            dedicatory_prayer_content.append(paragraph)
            current_section = 'preface_start'
            continue
        elif current_section == 'preface_start' and 'Dear reader' in content_text:
            current_section = 'preface'
            preface_content.append(paragraph)
        elif current_section == 'title' and 'This is a digital copy' in content_text:
            title_page_content.append(paragraph)
        elif current_section == 'prayer':
            dedicatory_prayer_content.append(paragraph)
        elif current_section == 'preface':
            preface_content.append(paragraph)
    
    sections['title_page'] = {
        'chapter_title': 'TITLE PAGE',
        'content': title_page_content
    }
    
    sections['dedicatory_prayer'] = {
        'chapter_title': 'DEDICATORY PRAYER',
        'content': dedicatory_prayer_content
    }
    
    sections['preface'] = {
        'chapter_title': 'PREFACE',
        'content': preface_content
    }
    
    return sections

def collect_all_chapters(current_data):
    """Coleta todos os capítulos do JSON atual"""
    all_chapters = []
    
    for part in current_data:
        for chapter in part['chapters']:
            # Pular os capítulos "Content" que são apenas divisórias
            if chapter['chapter_title'] != 'Content':
                all_chapters.append(chapter)
    
    return all_chapters

def convert_roman_to_int(roman):
    """Converte número romano para inteiro"""
    roman_values = {
        'I': 1, 'V': 5, 'X': 10, 'L': 50, 'C': 100, 'D': 500, 'M': 1000
    }
    
    result = 0
    i = 0
    roman = roman.upper()
    
    while i < len(roman):
        if i + 1 < len(roman) and roman_values[roman[i]] < roman_values[roman[i + 1]]:
            result += roman_values[roman[i + 1]] - roman_values[roman[i]]
            i += 2
        else:
            result += roman_values[roman[i]]
            i += 1
    
    return result

def extract_chapter_number(chapter_title):
    """Extrai o número do capítulo do título"""
    # Procurar por "CHAPTER" seguido de número romano
    match = re.search(r'CHAPTER\s+([IVXLCDM]+)', chapter_title.upper())
    if match:
        roman_num = match.group(1)
        try:
            return convert_roman_to_int(roman_num)
        except:
            return None
    return None

def map_chapters_to_parts(all_chapters, parts_structure):
    """Mapeia os capítulos às partes corretas"""
    # Criar um mapa de número do capítulo para parte
    chapter_to_part = {}
    
    for part_key, chapters in parts_structure.items():
        for chapter_info in chapters:
            try:
                chapter_num = convert_roman_to_int(chapter_info['chapter'])
                chapter_to_part[chapter_num] = {
                    'part': f'Part {part_key}',  # Convertendo "I" para "Part I"
                    'title': chapter_info['title']
                }
            except:
                print(f"Erro convertendo capítulo {chapter_info['chapter']} da Part {part_key}")
    
    # Organizar capítulos por parte
    organized_parts = {
        'Part I': [],
        'Part II': [],
        'Part III': [],
        'Part IV': [],
        'Part V': []
    }
    
    for chapter in all_chapters:
        chapter_num = extract_chapter_number(chapter['chapter_title'])
        
        if chapter_num and chapter_num in chapter_to_part:
            part_info = chapter_to_part[chapter_num]
            part_key = part_info['part']
            
            # Atualizar o título do capítulo para incluir o título completo
            chapter_title = f"CHAPTER {part_info['title'].split('.', 1)[0]}. {part_info['title'].split('.', 1)[1].strip() if '.' in part_info['title'] else part_info['title']}"
            
            updated_chapter = {
                'chapter_title': chapter_title,
                'content': chapter['content']
            }
            
            organized_parts[part_key].append(updated_chapter)
        else:
            print(f"Capítulo não mapeado: {chapter['chapter_title']}")
    
    return organized_parts

def create_new_json_structure():
    """Cria a nova estrutura JSON"""
    print("Carregando estrutura do CSV...")
    parts_structure = read_summary_csv()
    
    print("Carregando JSON atual...")
    current_data = load_current_json()
    
    print("Extraindo seções especiais...")
    special_sections = extract_special_sections(current_data)
    
    print("Coletando todos os capítulos...")
    all_chapters = collect_all_chapters(current_data)
    print(f"Total de capítulos encontrados: {len(all_chapters)}")
    
    print("Mapeando capítulos às partes...")
    organized_parts = map_chapters_to_parts(all_chapters, parts_structure)
    
    # Mapear os títulos das partes
    part_titles = {
        'Part I': 'PART THE FIRST - INSTRUCTIONS AND EXERCISES FOR CONDUCTING THE SOUL FROM HER FIRST DESIRE FOR A DEVOUT LIFE TILL SHE IS BROUGHT TO A FULL RESOLUTION OF EMBRACING IT',
        'Part II': 'PART THE SECOND - INSTRUCTIONS FOR ELEVATING THE SOUL TO GOD BY PRAYER AND BY THE SACRAMENTS',
        'Part III': 'PART THE THIRD - INSTRUCTIONS CONCERNING THE PRACTICE OF THE VIRTUES',
        'Part IV': 'PART THE FOURTH - NECESSARY ADVICE AGAINST THE MOST ORDINARY TEMPTATIONS',
        'Part V': 'PART THE FIFTH - INSTRUCTIONS AND EXERCISES NECESSARY FOR RENEWING THE SOUL, AND CONFIRMING HER IN DEVOTION'
    }
    
    # Criar a nova estrutura
    new_structure = []
    
    # 1. Title Page
    if special_sections['title_page'] and special_sections['title_page']['content']:
        title_part = {
            'part_title': 'TITLE PAGE',
            'chapters': [special_sections['title_page']]
        }
        new_structure.append(title_part)
    
    # 2. Dedicatory Prayer
    if special_sections['dedicatory_prayer'] and special_sections['dedicatory_prayer']['content']:
        prayer_part = {
            'part_title': 'DEDICATORY PRAYER',
            'chapters': [special_sections['dedicatory_prayer']]
        }
        new_structure.append(prayer_part)
    
    # 3. Preface
    if special_sections['preface'] and special_sections['preface']['content']:
        preface_part = {
            'part_title': 'PREFACE',
            'chapters': [special_sections['preface']]
        }
        new_structure.append(preface_part)
    
    # 4. As cinco partes do livro
    for part_key in ['Part I', 'Part II', 'Part III', 'Part IV', 'Part V']:
        if organized_parts[part_key]:
            part_data = {
                'part_title': part_titles[part_key],
                'chapters': organized_parts[part_key]
            }
            new_structure.append(part_data)
    
    return new_structure

def main():
    """Função principal"""
    try:
        print("Iniciando reorganização do JSON...")
        
        # Backup do arquivo original
        print("Criando backup...")
        import shutil
        shutil.copy2('webapp/public/data/livro_en.json', 'webapp/public/data/livro_en.json.backup2')
        
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
            print(f"Parte {i+1}: {part['part_title'][:50]}... - {len(part['chapters'])} capítulos")
    
    except Exception as e:
        print(f"❌ Erro durante a reorganização: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()
