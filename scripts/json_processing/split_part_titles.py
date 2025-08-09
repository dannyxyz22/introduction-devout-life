#!/usr/bin/env python3
"""
Split Part Titles
================
Divide part_title em part_title e part_subtitle usando o primeiro '-' como separador.
Aplica transformações específicas para numeração e capitalização.
"""

import json
import os
import re

def split_part_titles(json_file_path):
    """
    Processa o JSON para dividir part_title em part_title e part_subtitle
    """
    print("✂️  SPLIT PART TITLES")
    print("Divide part_title em part_title e part_subtitle")
    print("=" * 50)
    
    # Fazer backup
    backup_path = json_file_path.replace('.json', '_backup_split_titles.json')
    
    try:
        with open(json_file_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        # Fazer backup
        with open(backup_path, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
        print(f"💾 Backup: {backup_path}")
        
        print(f"📖 Carregando: {os.path.basename(json_file_path)}")
        
        modificacoes = 0
        
        # Processar cada parte
        for i, part in enumerate(data):
            original_part_title = part.get('part_title', '')
            
            # Pular DEDICATORY PRAYER e PREFACE (não têm hífen)
            if '-' not in original_part_title:
                continue
            
            # Dividir no primeiro hífen
            parts = original_part_title.split('-', 1)
            if len(parts) != 2:
                continue
                
            raw_part_title = parts[0].strip()
            raw_part_subtitle = parts[1].strip()
            
            # Transformar part_title
            part_title = raw_part_title
            part_title = part_title.replace("THE FIRST", "I")
            part_title = part_title.replace("THE SECOND", "II")
            part_title = part_title.replace("THE THIRD", "III")
            part_title = part_title.replace("THE FOURTH", "IV")
            part_title = part_title.replace("THE FIFTH", "V")
            
            # Transformar part_subtitle
            part_subtitle = capitalize_subtitle(raw_part_subtitle)
            
            # Atualizar o objeto com ordem correta
            data[i] = reorder_part_object(part, part_title, part_subtitle)
            
            print(f"   ✏️  '{original_part_title}' →")
            print(f"       part_title: '{part_title}'")
            print(f"       part_subtitle: '{part_subtitle}'")
            
            modificacoes += 1
        
        # Salvar resultado
        with open(json_file_path, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
        
        print(f"\n📊 RESULTADO:")
        print(f"   Modificações aplicadas: {modificacoes}")
        print(f"   Arquivo: {json_file_path}")
        print("✅ Part titles divididos com sucesso!")
        
        return True
        
    except Exception as e:
        print(f"❌ Erro: {str(e)}")
        return False

def reorder_part_object(part, new_part_title=None, new_part_subtitle=None):
    """
    Reorganiza um objeto part com a ordem: part_title, part_subtitle, chapters
    """
    ordered_part = {}
    
    # Definir part_title (usar novo valor se fornecido)
    if new_part_title is not None:
        ordered_part['part_title'] = new_part_title
    else:
        ordered_part['part_title'] = part.get('part_title', '')
    
    # Definir part_subtitle (usar novo valor se fornecido)
    if new_part_subtitle is not None:
        ordered_part['part_subtitle'] = new_part_subtitle
    elif 'part_subtitle' in part:
        ordered_part['part_subtitle'] = part['part_subtitle']
    
    # Definir chapters
    ordered_part['chapters'] = part.get('chapters', [])
    
    # Preservar outras chaves se existirem
    for key, value in part.items():
        if key not in ['part_title', 'part_subtitle', 'chapters']:
            ordered_part[key] = value
    
    return ordered_part

def capitalize_subtitle(subtitle):
    """
    Converte subtitle para capitalização adequada:
    - Primeira palavra sempre maiúscula
    - 'God' sempre maiúsculo
    - Demais palavras em minúsculo
    """
    # Palavras que devem permanecer sempre maiúsculas
    always_upper = {'GOD', 'JESUS', 'CHRIST', 'LORD', 'HOLY', 'SPIRIT', 'DIVINE'}
    
    # Converter tudo para minúsculo primeiro
    words = subtitle.lower().split()
    
    if not words:
        return subtitle
    
    # Primeira palavra sempre maiúscula
    words[0] = words[0].capitalize()
    
    # Verificar palavras que devem ser maiúsculas
    for i in range(len(words)):
        if words[i].upper() in always_upper:
            words[i] = words[i].capitalize()
        # Caso especial para "God"
        elif words[i].lower() == 'god':
            words[i] = 'God'
    
    return ' '.join(words)

def main():
    """Função principal"""
    # Caminhos dos arquivos
    base_dir = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
    json_file_path = os.path.join(base_dir, 'output', 'livro_en.json')
    
    # Verificar se arquivo existe
    if not os.path.exists(json_file_path):
        print(f"❌ Arquivo não encontrado: {json_file_path}")
        return
    
    # Dividir part titles
    split_success = split_part_titles(json_file_path)
    
    if split_success:
        print(f"\n✅ Processo concluído!")
    else:
        print(f"\n❌ Processo falhou!")

if __name__ == "__main__":
    main()
