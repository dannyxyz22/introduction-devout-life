#!/usr/bin/env python3
"""
Script simplificado para reorganizar o livro_en.json 
"""

import json
import csv

def analyze_current_structure():
    """Analisa a estrutura atual para entender a duplicação"""
    with open('webapp/public/data/livro_en.json.backup2', 'r', encoding='utf-8') as f:
        current_data = json.load(f)
    
    print("=== ANÁLISE DA ESTRUTURA ATUAL ===")
    
    chapter_titles = []
    for i, part in enumerate(current_data):
        print(f"\nParte {i+1}: {part['part_title']}")
        print(f"Número de capítulos: {len(part['chapters'])}")
        
        for j, chapter in enumerate(part['chapters']):
            title = chapter['chapter_title']
            chapter_titles.append(title)
            if j < 5:  # Mostra apenas os primeiros 5
                print(f"  - {title}")
            elif j == 5:
                print(f"  - ... (e mais {len(part['chapters']) - 5} capítulos)")
    
    print(f"\nTotal de capítulos no JSON: {len(chapter_titles)}")
    
    # Verificar duplicações
    unique_titles = set(chapter_titles)
    print(f"Títulos únicos: {len(unique_titles)}")
    
    if len(chapter_titles) != len(unique_titles):
        print("⚠️  Há duplicações detectadas!")
        
        # Encontrar duplicações
        from collections import Counter
        title_counts = Counter(chapter_titles)
        duplicated = {title: count for title, count in title_counts.items() if count > 1}
        
        print(f"Títulos duplicados ({len(duplicated)}):")
        for title, count in list(duplicated.items())[:10]:  # Mostrar só os primeiros 10
            print(f"  - {title} ({count}x)")

def read_csv_structure():
    """Lê a estrutura do CSV"""
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
    
    print("\n=== ESTRUTURA DO CSV ===")
    for part_key, chapters in parts.items():
        print(f"Parte {part_key}: {len(chapters)} capítulos")
        for i, chapter in enumerate(chapters[:3]):  # Mostrar os primeiros 3
            print(f"  - Cap {chapter['chapter']}: {chapter['title']}")
        if len(chapters) > 3:
            print(f"  - ... (e mais {len(chapters) - 3} capítulos)")
    
    return parts

def main():
    # Analisar estrutura atual
    analyze_current_structure()
    
    # Ler estrutura do CSV
    read_csv_structure()

if __name__ == "__main__":
    main()
