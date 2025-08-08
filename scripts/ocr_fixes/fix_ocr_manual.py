import json
import re
import os

def is_paragraph_continuation(text1, text2):
    """
    Detecta se o segundo parágrafo é uma continuação do primeiro.
    Critérios:
    1. Primeiro parágrafo termina sem pontuação final (. ! ? :)
    2. Segundo parágrafo não começa com maiúscula ou palavra de início de parágrafo
    3. Primeiro parágrafo não é muito curto (evitar títulos)
    4. Contexto semântico indica continuação
    """
    if not text1 or not text2:
        return False
    
    text1 = text1.strip()
    text2 = text2.strip()
    
    # Verifica se o primeiro parágrafo é muito curto (provável título)
    if len(text1.split()) < 8:
        return False
    
    # Verifica se o primeiro parágrafo termina sem pontuação final
    if text1[-1] in '.!?:':
        return False
    
    # Verifica se o segundo parágrafo começa com minúscula (indicação de continuação)
    if text2[0].islower():
        return True
    
    # Palavras que indicam continuação quando em maiúscula
    continuation_words = {
        'And', 'But', 'For', 'Or', 'Nor', 'So', 'Yet', 'However', 'Therefore',
        'Thus', 'Hence', 'Moreover', 'Furthermore', 'Nevertheless', 'Nonetheless',
        'Another', 'Others', 'These', 'Those', 'Such', 'Many', 'Some', 'All',
        'Both', 'Either', 'Neither', 'Each', 'Every', 'Any', 'No', 'None'
    }
    
    first_word = text2.split()[0] if text2.split() else ""
    
    # Se começa com palavra de continuação, provavelmente é continuação
    if first_word in continuation_words:
        return True
    
    # Verifica se termina com vírgula, ponto e vírgula, ou outros indicadores de continuação
    if text1[-1] in ',;-':
        return True
    
    # Verifica padrões específicos de quebra mid-sentence
    # Como no exemplo: "though he" seguido de "immediately afterwards"
    mid_sentence_endings = ['though', 'although', 'while', 'when', 'where', 'which', 'that', 'who', 'whom', 'whose', 'if', 'unless', 'until', 'since', 'because', 'as', 'before', 'after']
    last_word = text1.split()[-1].lower() if text1.split() else ""
    
    if last_word in mid_sentence_endings:
        return True
    
    return False

def merge_broken_paragraphs(chapters):
    """
    Mescla parágrafos que foram quebrados incorretamente pelo OCR.
    Retorna número de mesclagens realizadas.
    """
    merges_count = 0
    
    for chapter in chapters:
        if 'content' not in chapter:
            continue
            
        content = chapter['content']
        if len(content) < 2:
            continue
        
        # Processar de trás para frente para não afetar índices
        i = len(content) - 1
        while i > 0:
            # Ajustar i caso a lista tenha encolhido (por remoção anterior)
            if i >= len(content):
                i = len(content) - 1
                if i <= 0:
                    break
            if i - 1 < 0:
                break
                
            current = content[i]
            previous = content[i-1]
            
            # Apenas processar parágrafos de texto
            if (current.get('type') == 'p' and previous.get('type') == 'p' and 
                'content' in current and 'content' in previous):
                
                prev_text = previous['content']
                curr_text = current['content']
                
                if is_paragraph_continuation(prev_text, curr_text):
                    # Mesclar os parágrafos
                    merged_text = prev_text + " " + curr_text
                    previous['content'] = merged_text
                    previous['word_count'] = len(merged_text.split())
                    
                    # Remover o parágrafo atual
                    content.pop(i)
                    merges_count += 1
                    
                    # Continue verificando a mesma posição i (agora apontando para o próximo elemento)
                    # Se removemos o último elemento, o ajuste de i no topo do laço cuidará do limite
                    continue
            
            i -= 1
    
    return merges_count

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
    Aplica correções APENAS manuais ao JSON e mescla parágrafos quebrados
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
    
    # ETAPA 1: Mesclar parágrafos quebrados ANTES das correções de OCR
    print("🔗 Mesclando parágrafos quebrados...")
    all_chapters = []
    for part in data:
        all_chapters.extend(part.get('chapters', []))
    
    merges_count = merge_broken_paragraphs(all_chapters)
    if merges_count > 0:
        print(f"   ✅ {merges_count} parágrafos mesclados")
    else:
        print("   ℹ️ Nenhum parágrafo quebrado detectado")
    
    # ETAPA 2: Correções manuais de OCR
    print("🔧 Aplicando correções manuais de OCR...")
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
    recomputed_items = _recompute_counts(data)
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=2, ensure_ascii=False)
    
    print(f"\n📊 RESULTADO MANUAL:")
    print(f"   Parágrafos mesclados: {merges_count}")
    print(f"   Itens processados: {total_items}")
    print(f"   Correções OCR aplicadas: {total_corrections}")
    print(f"   🔢 word_count recalculado em {recomputed_items} itens")
    print(f"   Arquivo: {output_file}")
    
    return total_corrections + merges_count

def main():
    """Função principal - Correções manuais e mesclagem de parágrafos"""
    print("✋ CORRETOR MANUAL DE OCR")
    print("Aplica SOMENTE correções manuais específicas")
    print("Mescla parágrafos quebrados incorretamente pelo OCR")
    print("Não quebra palavras válidas como 'Description' ou 'Devotion'")
    print("=" * 70)
    
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
            print(f"✅ {corrections} correções totais aplicadas")
        else:
            print("✅ Nenhuma correção necessária")
    else:
        print(f"❌ Não encontrado: {file_path}")
    
    print(f"\n✋ Correção manual concluída!")
    print("Parágrafos quebrados foram mesclados automaticamente.")
    print("Palavras válidas como 'Description' e 'Devotion' foram preservadas.")

if __name__ == "__main__":
    main()

