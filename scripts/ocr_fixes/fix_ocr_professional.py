import json
import re
import os
from typing import Dict, List, Tuple

def install_required_packages():
    """
    Instala as biblioteca        # 3. CamelCase quebrado APENAS quando são duas palavras ESPECÍFICAS grudadas
        # Lista de palavras que realmente costumam grudar no OCR
        likely_concatenated = [
            'withGod', 'toGod', 'ofGod', 'fromGod', 'forGod', 'beforeGod', 'inGod',
            'ourLord', 'ourSaviour', 'JesusChrist', 'HolySpirit', 'HolyGhost',
            'theChurch', 'theGospel', 'theBible', 'theScripture',
            'prayerto', 'devotedto', 'unitedto', 'attachedto', 'dedicatedto',
            'eternallife', 'spirituallife', 'devoutlife',
            'morethan', 'lessthan', 'ratherthan', 'otherthan'
        ]
        
        # Só separar palavras que estão na lista de concatenações conhecidas
        for concatenated in likely_concatenated:
            if concatenated.lower() in fixed_text.lower():
                # Encontrar a posição correta para separar
                for i in range(3, len(concatenated)-2):
                    part1 = concatenated[:i]
                    part2 = concatenated[i:]
                    if part1.lower() in ['with', 'to', 'of', 'from', 'for', 'before', 'in', 'our', 'the', 'more', 'less', 'rather', 'other', 'eternal', 'spiritual', 'devout', 'prayer', 'devoted', 'united', 'attached', 'dedicated'] and len(part2) > 2:
                        pattern = re.compile(re.escape(concatenated), re.IGNORECASE)
                        replacement = part1 + ' ' + part2
                        fixed_text = pattern.sub(replacement, fixed_text)
                        breakcessárias para correção de OCR
    """
    import subprocess
    import sys
    
    packages = [
        'symspellpy',
        'textblob', 
        'pyspellchecker',
        'autocorrect'
    ]
    
    for package in packages:
        try:
            __import__(package.replace('-', '_'))
            print(f"✅ {package} já instalado")
        except ImportError:
            print(f"📦 Instalando {package}...")
            subprocess.check_call([sys.executable, "-m", "pip", "install", package])

class OCRCorrector:
    def __init__(self):
        self.manual_corrections = {
            # Palavras específicas do livro
            'andCredoin': 'and Credo in',
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
            'JesusChrist': 'Jesus Christ',
            'HolyGhost': 'Holy Ghost',
            'HolySpirit': 'Holy Spirit',
            'BlessedVirgin': 'Blessed Virgin',
            'DivineMajesty': 'Divine Majesty',
            'DivineGoodness': 'Divine Goodness',
            'eternallife': 'eternal life',
            'spirituallife': 'spiritual life',
            'devoutlife': 'devout life',
            'theChurch': 'the Church',
            'theGospel': 'the Gospel',
            'theBible': 'the Bible',
            'PaterNoster': 'Pater Noster',
            'AveMaria': 'Ave Maria',
            
            # Problemas comuns de OCR
            'morethan': 'more than',
            'lessthan': 'less than',
            'ratherthan': 'rather than',
            'otherthan': 'other than',
            'everday': 'every day',
            'somethimes': 'sometimes',
            'sometmes': 'sometimes',
            'everythning': 'everything',
            'anythning': 'anything',
            'nothning': 'nothing',
            'sornething': 'something',
            
            # Correções de pontuação
            '.—': '. —',
            ',—': ', —',
            ';—': '; —',
            ':—': ': —',
        }
        
        # Tentar carregar bibliotecas de correção
        self.spell_checkers = self._initialize_spell_checkers()
    
    def _initialize_spell_checkers(self):
        """Inicializa os corretores ortográficos disponíveis"""
        checkers = {}
        
        # SymSpell - Muito rápido e eficaz
        try:
            from symspellpy import SymSpell, Verbosity
            import pkg_resources
            
            sym_spell = SymSpell(max_dictionary_edit_distance=2, prefix_length=7)
            dictionary_path = pkg_resources.resource_filename("symspellpy", "frequency_dictionary_en_82_765.txt")
            sym_spell.load_dictionary(dictionary_path, term_index=0, count_index=1)
            checkers['symspell'] = sym_spell
            print("✅ SymSpell carregado")
        except Exception as e:
            print(f"⚠️  SymSpell não disponível: {e}")
        
        # PySpellChecker
        try:
            from spellchecker import SpellChecker
            spell = SpellChecker(language='en')
            checkers['pyspell'] = spell
            print("✅ PySpellChecker carregado")
        except Exception as e:
            print(f"⚠️  PySpellChecker não disponível: {e}")
            
        # AutoCorrect
        try:
            from autocorrect import Speller
            spell = Speller(lang='en')
            checkers['autocorrect'] = spell
            print("✅ AutoCorrect carregado")
        except Exception as e:
            print(f"⚠️  AutoCorrect não disponível: {e}")
        
        return checkers
    
    def fix_concatenated_words(self, text: str) -> str:
        """
        Corrige palavras concatenadas usando padrões inteligentes
        """
        fixed_text = text
        
        # Aplicar correções manuais primeiro
        for wrong, correct in self.manual_corrections.items():
            fixed_text = fixed_text.replace(wrong, correct)
        
        # Padrões regex para separar palavras grudadas
        
        # 1. Palavras comuns que ficam grudadas no final
        common_endings = ['the', 'and', 'of', 'to', 'in', 'for', 'with', 'by', 'from', 'on', 'at']
        for word in common_endings:
            # "palavra" + word -> "palavra " + word
            pattern = r'([a-z]{3,})(' + word + r')(\s|$|[.,;:!?])'
            fixed_text = re.sub(pattern, r'\1 \2\3', fixed_text)
        
        # 2. Palavras comuns que ficam grudadas no início
        common_beginnings = ['the', 'and', 'of', 'to', 'in', 'for', 'with', 'by', 'from', 'that', 'this']
        for word in common_beginnings:
            # word + "Palavra" -> word + " Palavra"
            pattern = r'(\s|^)(' + word + r')([A-Z][a-z]{2,})'
            fixed_text = re.sub(pattern, r'\1\2 \3', fixed_text)
        
        # 3. CamelCase quebrado APENAS quando há duas palavras completas
        # Evita quebrar palavras como "Description" -> "Descripti on"
        # Só quebra quando há pelo menos 4 letras antes e 4 depois
        fixed_text = re.sub(r'([a-z]{4,})([A-Z][a-z]{4,})', r'\1 \2', fixed_text)
        
        # 4. Números grudados
        fixed_text = re.sub(r'([a-zA-Z])(\d+)([a-zA-Z])', r'\1 \2 \3', fixed_text)
        
        # 5. Pontuação grudada
        fixed_text = re.sub(r'([a-z])([.!?])([A-Z])', r'\1\2 \3', fixed_text)
        
        # 6. Limpar espaços múltiplos
        fixed_text = re.sub(r'\s+', ' ', fixed_text)
        
        return fixed_text.strip()
    
    def spell_check_word(self, word: str) -> str:
        """
        Verifica e corrige uma palavra usando os corretores disponíveis
        """
        # Se a palavra está nas correções manuais, usar ela
        if word.lower() in [k.lower() for k in self.manual_corrections.keys()]:
            for wrong, correct in self.manual_corrections.items():
                if word.lower() == wrong.lower():
                    return correct
        
        # Se a palavra parece correta (tem maiúsculas, números, etc), não mexer
        if (len(word) < 3 or 
            word.isupper() or 
            word.isdigit() or 
            any(c in word for c in '.,;:!?()[]{}"\'') or
            word[0].isupper() and len(word) > 8):  # Nomes próprios longos
            return word
        
        # Tentar corrigir com SymSpell (mais rápido e preciso)
        if 'symspell' in self.spell_checkers:
            try:
                from symspellpy import Verbosity
                suggestions = self.spell_checkers['symspell'].lookup(word, Verbosity.CLOSEST, max_edit_distance=2)
                if suggestions and suggestions[0].distance <= 2:
                    return suggestions[0].term
            except:
                pass
        
        # Fallback para PySpellChecker
        if 'pyspell' in self.spell_checkers:
            try:
                spell = self.spell_checkers['pyspell']
                if word.lower() not in spell:
                    correction = spell.correction(word.lower())
                    if correction and correction != word.lower():
                        # Preservar capitalização original
                        if word[0].isupper():
                            return correction.capitalize()
                        return correction
            except:
                pass
        
        return word
    
    def correct_text(self, text: str) -> Tuple[str, int]:
        """
        Corrige o texto completo e retorna o texto corrigido e número de mudanças
        """
        original_text = text
        
        # 1. Primeiro corrigir concatenações
        fixed_text = self.fix_concatenated_words(text)
        
        # 2. Depois fazer spell check palavra por palavra (opcional e mais lento)
        # Para textos muito longos, isso pode ser desabilitado
        
        # Contar mudanças
        changes = 0 if original_text == fixed_text else 1
        
        return fixed_text, changes

def fix_ocr_in_json_professional(input_file: str, output_file: str = None) -> int:
    """
    Corrige OCR no arquivo JSON usando métodos profissionais
    """
    if output_file is None:
        output_file = input_file
    
    # Fazer backup
    if output_file == input_file:
        backup_file = input_file.replace('.json', '_backup_professional.json')
        if os.path.exists(input_file):
            import shutil
            shutil.copy2(input_file, backup_file)
            print(f"📁 Backup criado: {backup_file}")
    
    # Inicializar corretor
    corrector = OCRCorrector()
    
    # Carregar JSON
    with open(input_file, 'r', encoding='utf-8') as f:
        book_data = json.load(f)
    
    corrections_made = 0
    total_items = 0
    
    print("🔍 Processando arquivo...")
    
    # Processar cada parte
    for part in book_data:
        if 'part_title' in part:
            total_items += 1
            original = part['part_title']
            corrected, changes = corrector.correct_text(original)
            if changes > 0:
                part['part_title'] = corrected
                corrections_made += 1
                print(f"📝 Título da parte corrigido")
        
        # Processar capítulos
        for chapter in part.get('chapters', []):
            if 'chapter_title' in chapter:
                total_items += 1
                original = chapter['chapter_title']
                corrected, changes = corrector.correct_text(original)
                if changes > 0:
                    chapter['chapter_title'] = corrected
                    corrections_made += 1
                    if corrections_made <= 5:  # Mostrar apenas os primeiros
                        print(f"📝 Capítulo: '{original}' → '{corrected}'")
            
            # Processar conteúdo
            for paragraph in chapter.get('content', []):
                if 'content' in paragraph:
                    total_items += 1
                    original = paragraph['content']
                    corrected, changes = corrector.correct_text(original)
                    if changes > 0:
                        paragraph['content'] = corrected
                        paragraph['word_count'] = len(corrected.split())
                        corrections_made += 1
    
    # Salvar arquivo corrigido
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(book_data, f, indent=2, ensure_ascii=False)
    
    print(f"\n📊 RESULTADO:")
    print(f"   Total de itens processados: {total_items}")
    print(f"   Correções aplicadas: {corrections_made}")
    print(f"   Taxa de correção: {corrections_made/total_items*100:.1f}%")
    print(f"   Arquivo salvo: {output_file}")
    
    return corrections_made

def main():
    """Função principal"""
    print("🚀 CORRETOR PROFISSIONAL DE OCR")
    print("=" * 50)
    
    # Verificar e instalar dependências
    try:
        install_required_packages()
    except Exception as e:
        print(f"⚠️  Erro ao instalar pacotes: {e}")
        print("Continuando com correções básicas...")
    
    print("\n🔧 Iniciando correções...")
    
    # Processar apenas o arquivo em inglês (o PT-BR é gerado pelo Google Translate)
    file_path = os.path.join('leitura-devota-app', 'public', 'data', 'livro_en.json')
    
    if os.path.exists(file_path):
        print(f"\n📖 Processando arquivo original em inglês: {os.path.basename(file_path)}")
        print("ℹ️  Nota: O arquivo PT-BR não precisa de correção OCR pois é gerado pelo Google Translate")
        
        corrections = fix_ocr_in_json_professional(file_path)
        
        if corrections > 0:
            print(f"✅ {corrections} correções aplicadas!")
        else:
            print("ℹ️  Nenhuma correção necessária")
    else:
        print(f"❌ Arquivo não encontrado: {file_path}")
    
    print("\n🎉 Processo concluído com sucesso!")

if __name__ == "__main__":
    main()
