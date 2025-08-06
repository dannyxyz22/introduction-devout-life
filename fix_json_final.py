#!/usr/bin/env python3
"""
Script final para reorganizar o livro_en.json corretamente
Remove duplicações e organiza conforme o CSV
"""

import json
import csv
import re

def load_csv_structure():
    """Carrega a estrutura do CSV"""
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
    """Extrai o número do capítulo"""
    match = re.search(r'CHAPTER\s+([IVXLCDM]+)', chapter_title.upper())
    if match:
        try:
            return convert_roman_to_int(match.group(1))
        except:
            return None
    return None

def deduplicate_chapters(current_data):
    """Remove duplicações e cria lista única de capítulos"""
    seen_chapters = set()
    unique_chapters = []
    
    # Primeiro, coletar todos os capítulos evitando duplicações
    for part in current_data:
        for chapter in part['chapters']:
            title = chapter['chapter_title']
            
            # Pular capítulos "Content" que são apenas divisórias
            if title == 'Content':
                continue
            
            # Criar uma chave única baseada no título e conteúdo
            content_preview = ""
            if chapter['content']:
                content_preview = chapter['content'][0].get('content', '')[:100]
            
            chapter_key = f"{title}|{content_preview}"
            
            if chapter_key not in seen_chapters:
                seen_chapters.add(chapter_key)
                unique_chapters.append(chapter)
    
    return unique_chapters

def extract_special_content(current_data):
    """Extrai o conteúdo especial da primeira parte"""
    first_part = current_data[0]
    content_chapter = first_part['chapters'][0]
    
    # Extrair diferentes seções
    title_page_content = []
    dedicatory_prayer_content = []
    preface_content = []
    
    current_section = 'title'
    
    for paragraph in content_chapter['content']:
        content_text = paragraph.get('content', '')
        
        if 'DEDICATORY PRAYER' in content_text:
            current_section = 'prayer_marker'
            continue
        elif current_section == 'prayer_marker' and 'O SWEET JESUS' in content_text:
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
    
    return {
        'title_page': title_page_content,
        'dedicatory_prayer': dedicatory_prayer_content,
        'preface': preface_content
    }

def organize_by_csv_structure(unique_chapters, csv_structure):
    """Organiza os capítulos conforme a estrutura do CSV"""
    # Criar mapeamento de número do capítulo para informações do CSV
    chapter_map = {}
    
    for part_key, chapters in csv_structure.items():
        for chapter_info in chapters:
            try:
                chapter_num = convert_roman_to_int(chapter_info['chapter'])
                chapter_map[chapter_num] = {
                    'part': part_key,
                    'csv_title': chapter_info['title']
                }
            except Exception as e:
                print(f"Erro convertendo {chapter_info['chapter']}: {e}")
    
    # Organizar capítulos por parte
    organized = {
        'I': [], 'II': [], 'III': [], 'IV': [], 'V': []
    }
    
    unmatched = []
    
    for chapter in unique_chapters:
        chapter_num = extract_chapter_number(chapter['chapter_title'])
        
        if chapter_num and chapter_num in chapter_map:
            part_info = chapter_map[chapter_num]
            part_key = part_info['part']
            csv_title = part_info['csv_title']
            
            # Usar o título do CSV como título oficial
            new_chapter = {
                'chapter_title': f"CHAPTER {convert_int_to_roman(chapter_num)}. {csv_title}",
                'content': chapter['content']
            }
            
            organized[part_key].append(new_chapter)
        else:
            unmatched.append(chapter)
    
    if unmatched:
        print(f"⚠️  {len(unmatched)} capítulos não mapeados:")
        for ch in unmatched[:5]:
            print(f"  - {ch['chapter_title']}")
    
    return organized

def convert_int_to_roman(num):
    """Converte inteiro para romano"""
    values = [1000, 900, 500, 400, 100, 90, 50, 40, 10, 9, 5, 4, 1]
    symbols = ["M", "CM", "D", "CD", "C", "XC", "L", "XL", "X", "IX", "V", "IV", "I"]
    
    result = ""
    for i in range(len(values)):
        count = num // values[i]
        result += symbols[i] * count
        num -= values[i] * count
    return result

def create_final_structure(special_content, organized_chapters):
    """Cria a estrutura final do JSON"""
    part_titles = {
        'I': 'PART THE FIRST - INSTRUCTIONS AND EXERCISES FOR CONDUCTING THE SOUL FROM HER FIRST DESIRE FOR A DEVOUT LIFE TILL SHE IS BROUGHT TO A FULL RESOLUTION OF EMBRACING IT',
        'II': 'PART THE SECOND - INSTRUCTIONS FOR ELEVATING THE SOUL TO GOD BY PRAYER AND BY THE SACRAMENTS',
        'III': 'PART THE THIRD - INSTRUCTIONS CONCERNING THE PRACTICE OF THE VIRTUES',
        'IV': 'PART THE FOURTH - NECESSARY ADVICE AGAINST THE MOST ORDINARY TEMPTATIONS',
        'V': 'PART THE FIFTH - INSTRUCTIONS AND EXERCISES NECESSARY FOR RENEWING THE SOUL, AND CONFIRMING HER IN DEVOTION'
    }
    
    final_structure = []
    
    # 1. Title Page
    if special_content['title_page']:
        final_structure.append({
            'part_title': 'TITLE PAGE',
            'chapters': [{
                'chapter_title': 'TITLE PAGE',
                'content': special_content['title_page']
            }]
        })
    
    # 2. Dedicatory Prayer
    if special_content['dedicatory_prayer']:
        final_structure.append({
            'part_title': 'DEDICATORY PRAYER',
            'chapters': [{
                'chapter_title': 'DEDICATORY PRAYER',
                'content': special_content['dedicatory_prayer']
            }]
        })
    
    # 3. Preface
    if special_content['preface']:
        final_structure.append({
            'part_title': 'PREFACE',
            'chapters': [{
                'chapter_title': 'PREFACE',
                'content': special_content['preface']
            }]
        })
    
    # 4. As cinco partes principais
    for part_key in ['I', 'II', 'III', 'IV', 'V']:
        if organized_chapters[part_key]:
            final_structure.append({
                'part_title': part_titles[part_key],
                'chapters': organized_chapters[part_key]
            })
    
    return final_structure

def main():
    try:
        print("🔄 Iniciando reorganização final...")
        
        # Backup
        import shutil
        shutil.copy2('webapp/public/data/livro_en.json', 'webapp/public/data/livro_en.json.backup3')
        print("✅ Backup criado")
        
        # Carregar dados
        print("📖 Carregando estrutura do CSV...")
        csv_structure = load_csv_structure()
        
        print("📖 Carregando JSON atual...")
        current_data = load_current_json()
        
        # Extrair conteúdo especial
        print("✂️  Extraindo seções especiais...")
        special_content = extract_special_content(current_data)
        
        # Deduplificar capítulos
        print("🧹 Removendo duplicações...")
        unique_chapters = deduplicate_chapters(current_data)
        print(f"   {len(unique_chapters)} capítulos únicos encontrados")
        
        # Organizar por estrutura do CSV
        print("📚 Organizando por partes...")
        organized_chapters = organize_by_csv_structure(unique_chapters, csv_structure)
        
        # Mostrar estatísticas
        for part_key in ['I', 'II', 'III', 'IV', 'V']:
            print(f"   Parte {part_key}: {len(organized_chapters[part_key])} capítulos")
        
        # Criar estrutura final
        print("🏗️  Criando estrutura final...")
        final_structure = create_final_structure(special_content, organized_chapters)
        
        # Salvar
        print("💾 Salvando JSON reorganizado...")
        with open('webapp/public/data/livro_en.json', 'w', encoding='utf-8') as f:
            json.dump(final_structure, f, indent=2, ensure_ascii=False)
        
        print("🎉 Reorganização concluída!")
        print(f"📊 Total de seções: {len(final_structure)}")
        
        for i, section in enumerate(final_structure):
            print(f"   {i+1}. {section['part_title'][:50]}... ({len(section['chapters'])} capítulos)")
    
    except Exception as e:
        print(f"❌ Erro: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()
