#!/usr/bin/env python3
"""
Script final simplificado para reorganizar o JSON
Estratégia: coletar TODOS os capítulos únicos por conteúdo (não por número)
e mapear sequencialmente conforme o CSV
"""

import json
import csv
import re
import hashlib

def load_csv_chapters():
    """Carrega capítulos do CSV em ordem sequencial"""
    chapters = []
    with open('data/summary.csv', 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            chapters.append({
                'part': row['Part'].strip(),
                'chapter': row['Chapter'].strip(),
                'title': row['Title'].strip()
            })
    return chapters

def extract_special_sections(data):
    """Extrai title page, dedicatory prayer e preface da primeira parte"""
    first_part = data[0]
    content = first_part['chapters'][0]['content']
    
    title_page = []
    prayer = []
    preface = []
    
    section = 'title'
    for para in content:
        text = para.get('content', '')
        
        if 'DEDICATORY PRAYER' in text:
            section = 'prayer_start'
        elif section == 'prayer_start' and 'O SWEET JESUS' in text:
            section = 'prayer'
            prayer.append(para)
        elif section == 'prayer' and 'St. Francis de Sales' in text:
            prayer.append(para)
            section = 'preface_wait'
        elif section == 'preface_wait' and 'Dear reader' in text:
            section = 'preface'
            preface.append(para)
        elif section == 'title' and 'This is a digital copy' in text:
            title_page.append(para)
        elif section == 'prayer':
            prayer.append(para)
        elif section == 'preface':
            preface.append(para)
    
    return {
        'title_page': title_page,
        'prayer': prayer,
        'preface': preface
    }

def collect_all_chapters(data):
    """Coleta TODOS os capítulos, incluindo duplicatas, em ordem"""
    chapters = []
    
    for part in data:
        for chapter in part['chapters']:
            if chapter['chapter_title'] != 'Content':
                # Pular capítulos vazios - eles causam problemas de alinhamento
                if not chapter['content'] or len(chapter['content']) == 0:
                    print(f"⚠️  Pulando capítulo vazio: {chapter['chapter_title']}")
                    continue
                    
                # Criar hash do conteúdo para identificar duplicatas reais
                content_str = ""
                if chapter['content']:
                    content_str = str(chapter['content'][:2])  # Primeiros 2 parágrafos
                
                chapter_hash = hashlib.md5(content_str.encode()).hexdigest()
                
                chapters.append({
                    'title': chapter['chapter_title'],
                    'content': chapter['content'],
                    'hash': chapter_hash
                })
    
    return chapters

def deduplicate_by_content(chapters):
    """Remove duplicatas baseado no hash do conteúdo"""
    seen_hashes = set()
    unique = []
    
    for ch in chapters:
        if ch['hash'] not in seen_hashes:
            seen_hashes.add(ch['hash'])
            unique.append(ch)
    
    return unique

def match_content_to_chapters(json_chapters, csv_chapters):
    """Tenta fazer correspondência inteligente entre conteúdo JSON e títulos CSV"""
    matched_chapters = []
    
    print("🔍 Tentando correspondência inteligente de conteúdo...")
    
    for i, csv_ch in enumerate(csv_chapters):
        best_match = None
        best_score = 0
        
        # Para cada capítulo do CSV, procurar o melhor match no JSON
        for j, json_ch in enumerate(json_chapters):
            if not json_ch['content']:
                continue
                
            # Pegar as primeiras palavras do conteúdo para análise
            first_content = ""
            if json_ch['content'] and len(json_ch['content']) > 0:
                first_content = json_ch['content'][0].get('content', '')[:100].lower()
            
            # Calcular score de correspondência baseado no título do CSV
            csv_title_words = csv_ch['title'].lower().split()[:3]  # Primeiras 3 palavras
            score = 0
            
            for word in csv_title_words:
                if len(word) > 3 and word in first_content:  # Palavras com mais de 3 caracteres
                    score += 1
            
            # Bonus se o título está no início do conteúdo
            if csv_ch['title'].lower()[:20] in first_content:
                score += 2
                
            if score > best_score:
                best_score = score
                best_match = json_ch
        
        if best_match:
            matched_chapters.append(best_match)
            # Remover da lista para evitar reutilização
            json_chapters = [ch for ch in json_chapters if ch != best_match]
            print(f"   ✅ {csv_ch['title'][:40]}... → Match encontrado (score: {best_score})")
        elif json_chapters:
            # Se não encontrou match, usar o próximo disponível
            matched_chapters.append(json_chapters[0])
            json_chapters = json_chapters[1:]
            print(f"   ⚠️  {csv_ch['title'][:40]}... → Usando próximo disponível (sem match)")
        else:
            print(f"   ❌ {csv_ch['title'][:40]}... → Sem conteúdo disponível")
    
    return matched_chapters

def create_organized_structure(csv_chapters, json_chapters, special_sections):
    """Cria a estrutura final organizada"""
    
    # Começar com seções especiais
    structure = []
    
    # 1. Title Page
    if special_sections['title_page']:
        structure.append({
            'part_title': 'TITLE PAGE',
            'chapters': [{
                'chapter_title': 'TITLE PAGE',
                'content': special_sections['title_page']
            }]
        })
    
    # 2. Dedicatory Prayer  
    if special_sections['prayer']:
        structure.append({
            'part_title': 'DEDICATORY PRAYER',
            'chapters': [{
                'chapter_title': 'DEDICATORY PRAYER',
                'content': special_sections['prayer']
            }]
        })
    
    # 3. Preface
    if special_sections['preface']:
        structure.append({
            'part_title': 'PREFACE',
            'chapters': [{
                'chapter_title': 'PREFACE',
                'content': special_sections['preface']
            }]
        })
    
    # 4. Organizar capítulos por partes com correspondência inteligente
    part_titles = {
        'I': 'PART THE FIRST - INSTRUCTIONS AND EXERCISES FOR CONDUCTING THE SOUL FROM HER FIRST DESIRE FOR A DEVOUT LIFE TILL SHE IS BROUGHT TO A FULL RESOLUTION OF EMBRACING IT',
        'II': 'PART THE SECOND - INSTRUCTIONS FOR ELEVATING THE SOUL TO GOD BY PRAYER AND BY THE SACRAMENTS', 
        'III': 'PART THE THIRD - INSTRUCTIONS CONCERNING THE PRACTICE OF THE VIRTUES',
        'IV': 'PART THE FOURTH - NECESSARY ADVICE AGAINST THE MOST ORDINARY TEMPTATIONS',
        'V': 'PART THE FIFTH - INSTRUCTIONS AND EXERCISES NECESSARY FOR RENEWING THE SOUL, AND CONFIRMING HER IN DEVOTION'
    }
    
    parts = {'I': [], 'II': [], 'III': [], 'IV': [], 'V': []}
    
    # Fazer correspondência inteligente entre conteúdo e capítulos
    matched_chapters = match_content_to_chapters(json_chapters.copy(), csv_chapters)
    
    # Mapear capítulos matched aos capítulos do CSV
    for i, csv_ch in enumerate(csv_chapters):
        if i < len(matched_chapters):
            json_ch = matched_chapters[i]
            
            new_chapter = {
                'chapter_title': f"CHAPTER {csv_ch['chapter']}. {csv_ch['title']}",
                'content': json_ch['content']
            }
            
            parts[csv_ch['part']].append(new_chapter)
    
    # Adicionar partes que têm capítulos
    for part_key in ['I', 'II', 'III', 'IV', 'V']:
        if parts[part_key]:
            structure.append({
                'part_title': part_titles[part_key],
                'chapters': parts[part_key]
            })
    
    return structure, parts

def main():
    print("🔄 Reorganização final do JSON...")
    
    # Backup
    import shutil
    shutil.copy2('webapp/public/data/livro_en.json', 'webapp/public/data/livro_en_original.json')
    
    # Carregar dados
    print("📖 Carregando dados...")
    csv_chapters = load_csv_chapters()
    
    with open('webapp/public/data/livro_en.json', 'r', encoding='utf-8') as f:
        json_data = json.load(f)
    
    # Extrair seções especiais
    print("✂️  Extraindo seções especiais...")
    special_sections = extract_special_sections(json_data)
    
    # Coletar todos os capítulos
    print("📋 Coletando capítulos...")
    all_chapters = collect_all_chapters(json_data)
    print(f"   Total de capítulos: {len(all_chapters)}")
    
    # Remover duplicatas
    print("🧹 Removendo duplicatas...")
    unique_chapters = deduplicate_by_content(all_chapters)
    print(f"   Capítulos únicos: {len(unique_chapters)}")
    
    # Criar estrutura organizada
    print("🏗️  Organizando estrutura...")
    final_structure, parts_stats = create_organized_structure(csv_chapters, unique_chapters, special_sections)
    
    # Remover TITLE PAGE da estrutura final antes de salvar
    print("�️  Removendo TITLE PAGE...")
    final_structure = [section for section in final_structure if section.get('part_title') != 'TITLE PAGE']
    print(f"   TITLE PAGE removida. Seções restantes: {len(final_structure)}")
    
    # Mostrar estatísticas
    print("📊 Estatísticas:")
    for part in ['I', 'II', 'III', 'IV', 'V']:
        print(f"   Parte {part}: {len(parts_stats[part])} capítulos")
    
    # Salvar
    print("💾 Salvando...")
    with open('webapp/public/data/livro_en.json', 'w', encoding='utf-8') as f:
        json.dump(final_structure, f, indent=2, ensure_ascii=False)
    
    print("✅ Concluído!")
    print(f"   Total de seções: {len(final_structure)}")
    for i, section in enumerate(final_structure):
        title = section['part_title'][:50] + "..." if len(section['part_title']) > 50 else section['part_title']
        print(f"   {i+1}. {title} ({len(section['chapters'])} capítulos)")

if __name__ == "__main__":
    main()
