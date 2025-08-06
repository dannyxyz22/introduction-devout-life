#!/usr/bin/env python3
"""
Script para testar a detecção de oração dedicatória
"""

import json
import os

# Carregar JSON
json_file = 'webapp/public/data/livro_en.json'
with open(json_file, 'r', encoding='utf-8') as f:
    book_data = json.load(f)

# Testar detecção (igual ao script principal)
has_prayer_in_json = False
has_preface_in_json = False

# Verifica se há oração dedicatória no conteúdo
for part_idx, part in enumerate(book_data):
    # Verifica no título da parte
    part_title = part.get('part_title', '').upper()
    if ('ORAÇÃO' in part_title and 'DEDICATÓRIA' in part_title) or \
       ('DEDICATORY' in part_title and 'PRAYER' in part_title):
        has_prayer_in_json = True
        print(f"   ✅ Oração dedicatória detectada no JSON (título da parte): {part.get('part_title')}")
    
    if ('PREFÁCIO' in part_title) or ('PREFACE' in part_title):
        has_preface_in_json = True
        print(f"   ✅ Prefácio detectado no JSON (título da parte): {part.get('part_title')}")
        
    for chap_idx, chapter in enumerate(part.get('chapters', [])):
        # Verifica no título do capítulo
        chapter_title = chapter.get('chapter_title', '').upper()
        if ('ORAÇÃO' in chapter_title and 'DEDICATÓRIA' in chapter_title) or \
           ('DEDICATORY' in chapter_title and 'PRAYER' in chapter_title):
            has_prayer_in_json = True
            print(f"   ✅ Oração dedicatória detectada no JSON (título do capítulo): {chapter.get('chapter_title')}")
            
        if ('PREFÁCIO' in chapter_title) or ('PREFACE' in chapter_title):
            has_preface_in_json = True
            print(f"   ✅ Prefácio detectado no JSON (título do capítulo): {chapter.get('chapter_title')}")

print(f"\n📊 RESULTADO:")
print(f"   has_prayer_in_json: {has_prayer_in_json}")
print(f"   has_preface_in_json: {has_preface_in_json}")
