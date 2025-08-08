import json
import re
import os

def fix_ocr_concatenations(text):
    """
    Corrige palavras concatenadas comuns do OCR
    """
    # Dicionário de correções específicas encontradas
    ocr_fixes = {
        # Palavras comuns concatenadas
        'andCredoin': 'and Credo in',
        'andCredo': 'and Credo',
        'MeeknesstowardsOurselves': 'Meekness towards Ourselves',
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
        'eternallife': 'eternal life',
        'spirituallife': 'spiritual life',
        'devoutlife': 'devout life',
        'prayerand': 'prayer and',
        'meditationand': 'meditation and',
        'communionand': 'communion and',
        'confessionand': 'confession and',
        
        # Palavras latinas comuns
        'PaterNoster': 'Pater Noster',
        'AveMaria': 'Ave Maria',
        'TeDeumLaudamus': 'Te Deum Laudamus',
        'VeniCreator': 'Veni Creator',
        
        # Problemas de pontuação
        'Philothea': 'Philothea',
        'theSacrament': 'the Sacrament',
        'theSacraments': 'the Sacraments',
        'theChurch': 'the Church',
        'theGospel': 'the Gospel',
        'theBible': 'the Bible',
        'theScripture': 'the Scripture',
        'theScriptures': 'the Scriptures',
        
        # Palavras compostas específicas
        'everday': 'every day',
        'somethimes': 'sometimes',
        'sometmes': 'sometimes',
        'morethan': 'more than',
        'lessthan': 'less than',
        'ratherthan': 'rather than',
        'otherthan': 'other than',
        'morethen': 'more than',
        'lessthen': 'less than',
        
        # Problemas de espaçamento em frases comuns
        'prayerto': 'prayer to',
        'devotedto': 'devoted to',
        'unitedto': 'united to',
        'attachedto': 'attached to',
        'subjectedto': 'subjected to',
        'dedicatedto': 'dedicated to',
        'consecrated to': 'consecrated to',
        
        # Problemas específicos do livro
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
        
        # Capítulos e títulos
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
        
        # Problemas de pontuação
        '.—': '. —',
        ',—': ', —',
        ';—': '; —',
        ':—': ': —',
        
        # Correções específicas mencionadas
        'fromthesoultoGod': 'from the soul to God',
        'tostrengthenit': 'to strengthen it',
        'inafirmresolutionto': 'in a firm resolution to',
        'thesoulto': 'the soul to',
        'mustbehavewith': 'must behave with',
        'wemustbehave': 'we must behave',
        'regardtothem': 'regard to them',
        'excellenceofoursoul': 'excellence of our soul',
        'excellenceofvirtue': 'excellence of virtue',
        'exampleoftheSaints': 'example of the Saints',
        'loveofGod': 'love of God',
        'eternalloveof': 'eternal love of',
        'Godtowardsus': 'God towards us',
        'Considerationssuitableforrenewingourgoodpurposes': 'Considerations suitable for renewing our good purposes',
        'sentimentswe': 'sentiments we',
        'mustpreserve': 'must preserve',
        'afterthis': 'after this',
        'exerciseOn': 'exercise. On',
        'lastthree': 'last three',
        'principalcounsels': 'principal counsels',
        'forthis': 'for this',
        'introduction': 'introduction'
    }
    
    # Aplicar correções específicas
    fixed_text = text
    for wrong, correct in ocr_fixes.items():
        fixed_text = fixed_text.replace(wrong, correct)
    
    # Padrões regex para correções mais gerais
    
    # Corrigir palavras que terminam com uma palavra comum em minúscula grudada
    # Exemplo: "wordthe" -> "word the"
    common_words = ['the', 'and', 'of', 'to', 'in', 'for', 'with', 'by', 'from', 'on', 'at', 'as', 'is', 'are', 'was', 'were', 'be', 'been', 'have', 'has', 'had', 'do', 'does', 'did', 'will', 'would', 'could', 'should', 'may', 'might', 'can', 'must', 'shall']
    
    for word in common_words:
        # Padrão para palavra grudada no final: "qualquercoisa" + word
        pattern = r'([a-zA-Z])(' + word + r')(\s|$|[.,;:!?])'
        replacement = r'\1 \2\3'
        fixed_text = re.sub(pattern, replacement, fixed_text)
        
        # Padrão para palavra grudada no início: word + "qualquercoisa"
        pattern = r'(\s|^)(' + word + r')([A-Z][a-z]+)'
        replacement = r'\1\2 \3'
        fixed_text = re.sub(pattern, replacement, fixed_text)
    
    # Corrigir sequências como "wordWord" -> "word Word" (CamelCase quebrado)
    # Mas só quando há duas palavras COMPLETAS grudadas, não dentro de uma palavra normal
    # Busca por padrões onde há uma palavra completa + outra palavra completa grudadas
    # Exemplo: "prayerGod" -> "prayer God", mas não "Description" -> "Descripti on"
    fixed_text = re.sub(r'([a-z]{3,})([A-Z][a-z]{3,})', r'\1 \2', fixed_text)
    
    # Corrigir números grudados com palavras: "word1word" -> "word 1 word"
    fixed_text = re.sub(r'([a-zA-Z])(\d+)([a-zA-Z])', r'\1 \2 \3', fixed_text)
    
    # Corrigir pontuação grudada: "word.Word" -> "word. Word"
    fixed_text = re.sub(r'([a-z])([.!?])([A-Z])', r'\1\2 \3', fixed_text)
    
    # Limpar espaços múltiplos
    fixed_text = re.sub(r'\s+', ' ', fixed_text)
    
    return fixed_text.strip()

def fix_ocr_in_json(input_file, output_file=None):
    """
    Corrige problemas de OCR no arquivo JSON do livro
    """
    if output_file is None:
        output_file = input_file
    
    # Fazer backup
    if output_file == input_file:
        backup_file = input_file.replace('.json', '_backup_ocr.json')
        if os.path.exists(input_file):
            with open(input_file, 'r', encoding='utf-8') as f:
                backup_data = f.read()
            with open(backup_file, 'w', encoding='utf-8') as f:
                f.write(backup_data)
            print(f"Backup criado: {backup_file}")
    
    # Carregar o JSON
    with open(input_file, 'r', encoding='utf-8') as f:
        book_data = json.load(f)
    
    corrections_made = 0
    total_paragraphs = 0
    
    # Processar cada parte do livro
    for part in book_data:
        if 'part_title' in part:
            # Corrigir título da parte
            original_title = part['part_title']
            fixed_title = fix_ocr_concatenations(original_title)
            if fixed_title != original_title:
                part['part_title'] = fixed_title
                corrections_made += 1
                print(f"Título corrigido: '{original_title}' -> '{fixed_title}'")
        
        # Processar capítulos
        for chapter in part.get('chapters', []):
            # Corrigir título do capítulo
            if 'chapter_title' in chapter:
                original_title = chapter['chapter_title']
                fixed_title = fix_ocr_concatenations(original_title)
                if fixed_title != original_title:
                    chapter['chapter_title'] = fixed_title
                    corrections_made += 1
                    print(f"Capítulo corrigido: '{original_title}' -> '{fixed_title}'")
            
            # Corrigir conteúdo dos parágrafos
            for paragraph in chapter.get('content', []):
                if 'content' in paragraph:
                    total_paragraphs += 1
                    original_content = paragraph['content']
                    fixed_content = fix_ocr_concatenations(original_content)
                    
                    if fixed_content != original_content:
                        paragraph['content'] = fixed_content
                        # Recalcular word count
                        paragraph['word_count'] = len(fixed_content.split())
                        corrections_made += 1
                        
                        # Mostrar apenas as primeiras correções para não flood o console
                        if corrections_made <= 10:
                            print(f"Parágrafo corrigido:")
                            print(f"  Antes: {original_content[:100]}...")
                            print(f"  Depois: {fixed_content[:100]}...")
                            print()
    
    # Salvar arquivo corrigido
    # Recompute word_count for every content item as the last step before saving
    def _recompute_counts(struct):
        items = 0
        for part in struct:
            for ch in part.get('chapters', []):
                for it in ch.get('content', []):
                    if isinstance(it, dict) and 'content' in it:
                        it['word_count'] = len((it.get('content') or '').split())
                        items += 1
        return items
    recomputed_items = _recompute_counts(book_data)
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(book_data, f, indent=2, ensure_ascii=False)
    
    print(f"\n=== RESUMO DAS CORREÇÕES ===")
    print(f"Total de parágrafos processados: {total_paragraphs}")
    print(f"Total de correções realizadas: {corrections_made}")
    print(f"Arquivo salvo: {output_file}")
    print(f"🔢 word_count recalculado em {recomputed_items} itens")
    
    return corrections_made

def main():
    """
    Função principal para executar as correções
    """
    print("=== CORRETOR DE PROBLEMAS DE OCR ===")
    print("Este script corrige palavras concatenadas e outros problemas de OCR no arquivo JSON.\n")
    
    # Arquivos para processar
    files_to_process = [
        os.path.join('leitura-devota-app', 'public', 'data', 'livro_en.json'),
        os.path.join('leitura-devota-app', 'public', 'data', 'livro_pt-BR.json')
    ]
    
    for file_path in files_to_process:
        if os.path.exists(file_path):
            print(f"\nProcessando: {file_path}")
            corrections = fix_ocr_in_json(file_path)
            
            if corrections > 0:
                print(f"✅ {corrections} correções aplicadas em {file_path}")
            else:
                print(f"ℹ️  Nenhuma correção necessária em {file_path}")
        else:
            print(f"❌ Arquivo não encontrado: {file_path}")
    
    print("\n🎉 Processo de correção de OCR concluído!")

if __name__ == "__main__":
    main()
