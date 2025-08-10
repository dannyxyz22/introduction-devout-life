#!/usr/bin/env python3
"""
Correções ad hoc específicas para problemas pontuais no JSON
"""

import json
import os
import shutil

def apply_ad_hoc_fixes(json_data):
    """
    Aplica correções ad hoc específicas ao JSON
    """
    fixes_applied = 0
    total_items = 0
    
    # Lista de correções específicas
    corrections = {
        "We must purify ourselves from our natural imper": "We must purify ourselves from our natural imperfections.",
        "Introduction to the Devout Life.": "",  # Remove duplicate book title from PREFACE
        "The choice we ought to make as to the practice":"The choice we ought to make as to the practice of the Virtues.",
        # Adicione mais correções aqui conforme necessário
        "theChurch": "the Church",
        "theGospel": "the Gospel", 
        "beforeGod": "before God",
        "toGod": "to God",
        "JesusChrist": "Jesus Christ",
        # "texto_problemático": "texto_corrigido",
    }
    
    print("🔧 Aplicando correções ad hoc...")
    
    for part in json_data:
        # Corrigir títulos de partes
        if 'part_title' in part:
            total_items += 1
            original = part['part_title']
            for wrong, correct in corrections.items():
                if wrong in original:
                    part['part_title'] = original.replace(wrong, correct)
                    fixes_applied += 1
                    print(f"   ✏️  Parte: '{wrong}' → '{correct}'")
        
        # Corrigir capítulos
        for chapter in part.get('chapters', []):
            if 'chapter_title' in chapter:
                total_items += 1
                original = chapter['chapter_title']
                for wrong, correct in corrections.items():
                    if wrong in original:
                        chapter['chapter_title'] = original.replace(wrong, correct)
                        fixes_applied += 1
                        print(f"   ✏️  Capítulo: '{wrong}' → '{correct}'")
            
            # Corrigir conteúdo
            for paragraph in chapter.get('content', []):
                if 'content' in paragraph:
                    total_items += 1
                    original = paragraph['content']
                    for wrong, correct in corrections.items():
                        if wrong in original:
                            paragraph['content'] = original.replace(wrong, correct)
                            # Recalcular word_count
                            paragraph['word_count'] = len(paragraph['content'].split())
                            fixes_applied += 1
                            print(f"   ✏️  Texto: '{wrong[:50]}...' → '{correct[:50]}...'")
    
    return fixes_applied, total_items

def main():
    """Função principal"""
    print("🔧 CORREÇÕES AD HOC")
    print("Aplica correções específicas para problemas pontuais")
    print("=" * 60)
    
    # Detectar diretório base do projeto
    script_dir = os.path.dirname(os.path.abspath(__file__))
    project_root = os.path.dirname(os.path.dirname(script_dir))
    input_file = os.path.join(project_root, 'output', 'livro_en.json')
    
    if not os.path.exists(input_file):
        print(f"❌ Arquivo não encontrado: {input_file}")
        return False
    
    # Backup
    backup_file = input_file.replace('.json', '_backup_ad_hoc.json')
    shutil.copy2(input_file, backup_file)
    print(f"💾 Backup: {backup_file}")
    
    # Carregar JSON
    print(f"📖 Carregando: {os.path.basename(input_file)}")
    with open(input_file, 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    # Aplicar correções
    fixes_applied, total_items = apply_ad_hoc_fixes(data)
    
    if fixes_applied > 0:
        # Recompute word_count for every content item as the final step before saving
        def _recompute_counts(struct):
            items = 0
            for part in struct:
                for ch in part.get('chapters', []):
                    for it in ch.get('content', []):
                        if isinstance(it, dict) and 'content' in it:
                            it['word_count'] = len((it.get('content') or '').split())
                            items += 1
            return items
        
        recomputed_items = _recompute_counts(data)
        
        # Salvar
        with open(input_file, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2, ensure_ascii=False)
        
        print(f"\n📊 RESULTADO:")
        print(f"   Itens processados: {total_items}")
        print(f"   Correções aplicadas: {fixes_applied}")
        print(f"   🔢 word_count recalculado em {recomputed_items} itens")
        print(f"   Arquivo: {input_file}")
        print(f"✅ Correções ad hoc aplicadas com sucesso!")
        
    else:
        print(f"\n📊 RESULTADO:")
        print(f"   Itens processados: {total_items}")
        print(f"   ✅ Nenhuma correção necessária")
    
    return True

if __name__ == "__main__":
    main()
