import json
import re
import os

def fix_ocr_conservative(text):
    """
    Corretor conservador que só aplica correções muito específicas
    """
    # Apenas correções manuais muito específicas e comprovadas
    specific_fixes = {
        # Problemas reais identificados
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
        
        # Vida espiritual
        'eternallife': 'eternal life',
        'spirituallife': 'spiritual life',
        'devoutlife': 'devout life',
        
        # Palavras compostas específicas
        'morethan': 'more than',
        'lessthan': 'less than',
        'ratherthan': 'rather than',
        'otherthan': 'other than',
        'everday': 'every day',
        'somethimes': 'sometimes',
        'sometmes': 'sometimes',
        
        # Problemas da Igreja
        'theChurch': 'the Church',
        'theGospel': 'the Gospel',
        'theBible': 'the Bible',
        'theScripture': 'the Scripture',
        'theScriptures': 'the Scriptures',
        'theSacrament': 'the Sacrament',
        'theSacraments': 'the Sacraments',
        
        # Palavras com preposições grudadas
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
        
        # Capítulos grudados (sem quebrar palavras válidas)
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
    }
    
    # Aplicar apenas correções manuais específicas
    fixed_text = text
    changes_made = 0
    
    for wrong, correct in specific_fixes.items():
        if wrong in fixed_text:
            fixed_text = fixed_text.replace(wrong, correct)
            changes_made += 1
    
    # APENAS uma regex muito conservadora para palavras comuns grudadas no final
    # Só para palavras muito comuns de 2-3 letras
    tiny_words = ['to', 'of', 'in', 'by', 'at', 'on', 'is', 'as', 'be', 'he', 'we', 'me', 'my', 'no', 'so', 'up', 'or']
    
    for word in tiny_words:
        # Só separar se a palavra grudada for muito óbvia: "alguma coisa" + word
        pattern = r'([a-z]{4,})(' + word + r')(\s|$|[.,;:!?])'
        replacement = r'\1 \2\3'
        before = fixed_text
        fixed_text = re.sub(pattern, replacement, fixed_text)
        if before != fixed_text:
            changes_made += 1
    
    # Limpar apenas espaços múltiplos
    fixed_text = re.sub(r'  +', ' ', fixed_text)
    
    return fixed_text.strip(), changes_made

def fix_json_conservative(input_file, output_file=None):
    """
    Aplica correções conservativas ao JSON
    """
    if output_file is None:
        output_file = input_file
    
    # Backup
    if output_file == input_file:
        backup_file = input_file.replace('.json', '_backup_conservative.json')
        if os.path.exists(input_file):
            import shutil
            shutil.copy2(input_file, backup_file)
            print(f"📁 Backup: {backup_file}")
    
    # Carregar JSON
    with open(input_file, 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    total_corrections = 0
    total_items = 0
    
    # Processar dados
    for part in data:
        # Títulos de partes
        if 'part_title' in part:
            total_items += 1
            original = part['part_title']
            corrected, changes = fix_ocr_conservative(original)
            if changes > 0:
                part['part_title'] = corrected
                total_corrections += changes
                print(f"✏️  Parte: '{original}' → '{corrected}'")
        
        # Capítulos
        for chapter in part.get('chapters', []):
            if 'chapter_title' in chapter:
                total_items += 1
                original = chapter['chapter_title']
                corrected, changes = fix_ocr_conservative(original)
                if changes > 0:
                    chapter['chapter_title'] = corrected
                    total_corrections += changes
                    print(f"✏️  Cap: '{original}' → '{corrected}'")
            
            # Conteúdo
            for paragraph in chapter.get('content', []):
                if 'content' in paragraph:
                    total_items += 1
                    original = paragraph['content']
                    corrected, changes = fix_ocr_conservative(original)
                    if changes > 0:
                        paragraph['content'] = corrected
                        paragraph['word_count'] = len(corrected.split())
                        total_corrections += changes
    
    # Salvar
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=2, ensure_ascii=False)
    
    print(f"\n📊 RESULTADO CONSERVADOR:")
    print(f"   Itens processados: {total_items}")
    print(f"   Correções aplicadas: {total_corrections}")
    print(f"   Arquivo: {output_file}")
    
    return total_corrections

def main():
    """Função principal conservadora"""
    print("🛡️  CORRETOR CONSERVADOR DE OCR")
    print("Aplica apenas correções muito específicas e comprovadas")
    print("=" * 55)
    
    files = [
        os.path.join('leitura-devota-app', 'public', 'data', 'livro_en.json'),
        os.path.join('leitura-devota-app', 'public', 'data', 'livro_pt-BR.json')
    ]
    
    for file_path in files:
        if os.path.exists(file_path):
            print(f"\n📖 Arquivo: {os.path.basename(file_path)}")
            corrections = fix_json_conservative(file_path)
            
            if corrections > 0:
                print(f"✅ {corrections} correções pontuais aplicadas")
            else:
                print("✅ Nenhuma correção necessária")
        else:
            print(f"❌ Não encontrado: {file_path}")
    
    print(f"\n🎯 Correção conservadora concluída!")
    print("Somente problemas específicos foram corrigidos.")

if __name__ == "__main__":
    main()
