import json
import re
import os

def fix_ocr_manual_only(text):
    """
    Corrige APENAS problemas de OCR através de correções manuais específicas.
    NÃO aplica nenhuma regex automática que possa quebrar palavras válidas.
    """
    # APENAS correções manuais específicas e verificadas
    manual_fixes = {
        # Problemas reais de concatenação religiosa
        'beforeGod': 'before God',
        'toGod': 'to God', 
        'ofGod': 'of God',
        'withGod': 'with God',
        'fromGod': 'from God',
        'forGod': 'for God',
        'inGod': 'in God',
        'ourLord': 'our Lord',
        'ourSaviour': 'our Saviour',
        'ourSavior': 'our Savior',
        'JesusChrist': 'Jesus Christ',
        'HolyGhost': 'Holy Ghost',
        'HolySpirit': 'Holy Spirit',
        'BlessedVirgin': 'Blessed Virgin',
        'DivineMajesty': 'Divine Majesty',
        'DivineGoodness': 'Divine Goodness',
        
        # Problemas de vida espiritual
        'eternallife': 'eternal life',
        'spirituallife': 'spiritual life', 
        'devoutlife': 'devout life',
        
        # Problemas comuns de OCR
        'morethan': 'more than',
        'lessthan': 'less than',
        'ratherthan': 'rather than',
        'otherthan': 'other than',
        'everday': 'every day',
        'somethimes': 'sometimes',
        'sometmes': 'sometimes',
        
        # Igreja e textos sagrados
        'theChurch': 'the Church',
        'theGospel': 'the Gospel',
        'theBible': 'the Bible',
        'theScripture': 'the Scripture',
        'theScriptures': 'the Scriptures',
        'theSacrament': 'the Sacrament',
        'theSacraments': 'the Sacraments',
        
        # Preposições grudadas
        'prayerto': 'prayer to',
        'devotedto': 'devoted to',
        'unitedto': 'united to',
        'attachedto': 'attached to',
        'subjectedto': 'subjected to',
        'dedicatedto': 'dedicated to',
        
        # Palavras latinas
        'PaterNoster': 'Pater Noster',
        'AveMaria': 'Ave Maria',
        'TeDeumLaudamus': 'Te Deum Laudamus',
        'VeniCreator': 'Veni Creator',
        
        # Problemas de pontuação
        '.—': '. —',
        ',—': ', —',
        ';—': '; —',
        ':—': ': —',
        
        # Capítulos - APENAS quando são realmente grudados
        'ChapterI': 'Chapter I',
        'ChapterII': 'Chapter II', 
        'ChapterIII': 'Chapter III',
        'ChapterIV': 'Chapter IV',
        'ChapterV': 'Chapter V',
        'ChapterVI': 'Chapter VI',
        'ChapterVII': 'Chapter VII',
        'ChapterVIII': 'Chapter VIII',
        'ChapterIX': 'Chapter IX',
        'ChapterX': 'Chapter X',
        
        # Problemas específicos encontrados no texto
        'andCredoin': 'and Credo in',
        'MeeknesstowardsOurselves': 'Meekness towards Ourselves',
        'plantsoftheChurch': 'plants of the Church',
        'loveofthe': 'love of the',
        'loveof': 'love of',
        'fearof': 'fear of',
        'desireof': 'desire of',
        'hopeof': 'hope of',
        'faithin': 'faith in',
        'trustin': 'trust in',
        'believein': 'believe in',
        'confidencein': 'confidence in',
    }
    
    # Aplicar APENAS as correções manuais
    fixed_text = text
    changes = 0
    
    for wrong, correct in manual_fixes.items():
        if wrong in fixed_text:
            # Usar replace simples, não regex
            before = fixed_text
            fixed_text = fixed_text.replace(wrong, correct)
            if before != fixed_text:
                changes += 1
    
    # NENHUMA regex automática! Apenas limpar espaços duplos
    fixed_text = re.sub(r'  +', ' ', fixed_text)
    
    return fixed_text.strip(), changes

def fix_json_manual_only(input_file, output_file=None):
    """
    Aplica correções APENAS manuais ao JSON
    """
    if output_file is None:
        output_file = input_file
    
    # Backup
    if output_file == input_file:
        backup_file = input_file.replace('.json', '_backup_manual.json')
        if os.path.exists(input_file):
            import shutil
            shutil.copy2(input_file, backup_file)
            print(f"💾 Backup: {backup_file}")
    
    # Carregar JSON
    with open(input_file, 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    total_corrections = 0
    total_items = 0
    examples_shown = 0
    
    # Processar dados
    for part in data:
        # Títulos de partes
        if 'part_title' in part:
            total_items += 1
            original = part['part_title']
            corrected, changes = fix_ocr_manual_only(original)
            if changes > 0:
                part['part_title'] = corrected
                total_corrections += changes
                if examples_shown < 3:
                    print(f"✏️  Parte: '{original}' → '{corrected}'")
                    examples_shown += 1
        
        # Capítulos
        for chapter in part.get('chapters', []):
            if 'chapter_title' in chapter:
                total_items += 1
                original = chapter['chapter_title']
                corrected, changes = fix_ocr_manual_only(original)
                if changes > 0:
                    chapter['chapter_title'] = corrected
                    total_corrections += changes
                    if examples_shown < 5:
                        print(f"✏️  Cap: '{original}' → '{corrected}'")
                        examples_shown += 1
            
            # Conteúdo
            for paragraph in chapter.get('content', []):
                if 'content' in paragraph:
                    total_items += 1
                    original = paragraph['content']
                    corrected, changes = fix_ocr_manual_only(original)
                    if changes > 0:
                        paragraph['content'] = corrected
                        paragraph['word_count'] = len(corrected.split())
                        total_corrections += changes
                        if examples_shown < 8:
                            print(f"✏️  Texto: '{original[:50]}...' → '{corrected[:50]}...'")
                            examples_shown += 1
    
    # Salvar
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=2, ensure_ascii=False)
    
    print(f"\n📊 RESULTADO MANUAL:")
    print(f"   Itens processados: {total_items}")
    print(f"   Correções aplicadas: {total_corrections}")
    print(f"   Arquivo: {output_file}")
    
    return total_corrections

def main():
    """Função principal - APENAS correções manuais"""
    print("✋ CORRETOR MANUAL DE OCR")
    print("Aplica SOMENTE correções manuais específicas")
    print("Não quebra palavras válidas como 'Description' ou 'Devotion'")
    print("=" * 60)
    
    # Processar apenas o arquivo em inglês (fonte original com problemas de OCR)
    # Detectar diretório base do projeto
    script_dir = os.path.dirname(os.path.abspath(__file__))
    project_root = os.path.dirname(os.path.dirname(script_dir))
    file_path = os.path.join(project_root, 'output', 'livro_en.json')
    
    if os.path.exists(file_path):
        print(f"\n📖 Arquivo: {os.path.basename(file_path)}")
        print("ℹ️  Nota: O arquivo PT-BR é gerado pelo Google Translate e não precisa de correção OCR")
        
        corrections = fix_json_manual_only(file_path)
        
        if corrections > 0:
            print(f"✅ {corrections} correções específicas aplicadas")
        else:
            print("✅ Nenhuma correção manual necessária")
    else:
        print(f"❌ Não encontrado: {file_path}")
    
    print(f"\n✋ Correção manual concluída!")
    print("Palavras válidas como 'Description' e 'Devotion' foram preservadas.")

if __name__ == "__main__":
    main()
