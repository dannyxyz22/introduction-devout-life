#!/usr/bin/env python3
"""
Script corrigido para mapear corretamente os capítulos sequenciais do JSON 
para as partes do CSV que reiniciam a numeração
"""

import json
import csv
import re

def load_csv_structure():
    """Carrega a estrutura do CSV organizando por ordem sequencial"""
    parts = {}
    sequential_chapters = []  # Lista de capítulos em ordem sequencial
    
    with open('data/summary.csv', 'r', encoding='utf-8') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            part_key = row['Part'].strip()
            chapter_info = {
                'part': part_key,
                'chapter': row['Chapter'].strip(),
                'title': row['Title'].strip(),
                'page': row['Page'].strip()
            }
            sequential_chapters.append(chapter_info)
            
            if part_key not in parts:
                parts[part_key] = []
            parts[part_key].append(chapter_info)
    
    return parts, sequential_chapters

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
    """Remove duplicações e ordena capítulos sequencialmente"""
    seen_chapters = {}
    unique_chapters = []
    
    # Coletar todos os capítulos evitando duplicações
    for part in current_data:
        for chapter in part['chapters']:
            title = chapter['chapter_title']
            
            # Pular capítulos "Content" que são apenas divisórias
            if title == 'Content':
                continue
            
            chapter_num = extract_chapter_number(title)
            if chapter_num is None:
                continue
            
            # Se já vimos este número de capítulo, pular duplicação
            if chapter_num in seen_chapters:
                continue
            
            seen_chapters[chapter_num] = chapter
            unique_chapters.append((chapter_num, chapter))
    
    # Ordenar por número do capítulo
    unique_chapters.sort(key=lambda x: x[0])
    
    return [chapter for _, chapter in unique_chapters]

def extract_special_content(current_data):
    """Extrai o conteúdo especial da primeira parte"""
    first_part = current_data[0]
    content_chapter = first_part['chapters'][0]
    
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

def map_chapters_sequentially(unique_chapters, sequential_csv_chapters):
    """Mapeia capítulos sequenciais do JSON aos capítulos do CSV"""
    organized = {
        'I': [], 'II': [], 'III': [], 'IV': [], 'V': []
    }
    
    print(f"📋 Mapeando {len(unique_chapters)} capítulos únicos do JSON")
    print(f"📋 Para {len(sequential_csv_chapters)} capítulos do CSV")
    
    # Mapear diretamente por posição sequencial
    for i, json_chapter in enumerate(unique_chapters):
        if i < len(sequential_csv_chapters):
            csv_info = sequential_csv_chapters[i]
            
            # Criar novo capítulo com título do CSV
            new_chapter = {
                'chapter_title': f"CHAPTER {csv_info['chapter']}. {csv_info['title']}",
                'content': json_chapter['content']
            }
            
            organized[csv_info['part']].append(new_chapter)
            
            if i < 10:  # Log dos primeiros mapeamentos
                print(f"   {i+1:2d}. JSON Cap {extract_chapter_number(json_chapter['chapter_title']):2d} → CSV Parte {csv_info['part']} Cap {csv_info['chapter']}")
        else:
            print(f"⚠️  Capítulo extra no JSON: {json_chapter['chapter_title']}")
    
    return organized

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
        print("🔄 Iniciando reorganização com mapeamento sequencial...")
        
        # Backup
        import shutil
        shutil.copy2('webapp/public/data/livro_en.json', 'webapp/public/data/livro_en.json.backup4')
        print("✅ Backup criado")
        
        # Carregar dados
        print("📖 Carregando estrutura do CSV...")
        csv_parts, sequential_csv_chapters = load_csv_structure()
        
        print("📖 Carregando JSON atual...")
        current_data = load_current_json()
        
        # Extrair conteúdo especial
        print("✂️  Extraindo seções especiais...")
        special_content = extract_special_content(current_data)
        
        # Deduplificar e ordenar capítulos
        print("🧹 Removendo duplicações e ordenando...")
        unique_chapters = deduplicate_chapters(current_data)
        print(f"   {len(unique_chapters)} capítulos únicos encontrados")
        
        # Mapear sequencialmente
        print("📚 Mapeando sequencialmente...")
        organized_chapters = map_chapters_sequentially(unique_chapters, sequential_csv_chapters)
        
        # Mostrar estatísticas
        total_mapped = 0
        for part_key in ['I', 'II', 'III', 'IV', 'V']:
            count = len(organized_chapters[part_key])
            total_mapped += count
            print(f"   Parte {part_key}: {count} capítulos")
        
        print(f"   Total mapeado: {total_mapped}")
        
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
