#!/usr/bin/env python3
"""
Script para adicionar word_count ao livro_extracted.json
Mantém compatibilidade com scripts existentes que esperam esse campo.
"""

import json
import os

def count_words(text):
    """
    Conta palavras em um texto, removendo espaços extras e caracteres especiais.
    
    Args:
        text (str): Texto para contar palavras
        
    Returns:
        int: Número de palavras
    """
    if not text or not isinstance(text, str):
        return 0
    
    # Remove espaços extras e quebras de linha
    cleaned_text = ' '.join(text.strip().split())
    
    # Conta palavras (divide por espaços)
    if cleaned_text:
        return len(cleaned_text.split())
    return 0

def add_word_counts_to_json(input_file, output_file):
    """
    Adiciona campo word_count a todos os itens de content no JSON.
    
    Args:
        input_file (str): Arquivo JSON de entrada
        output_file (str): Arquivo JSON de saída
    """
    print(f"📊 Adicionando word_count ao arquivo JSON...")
    print(f"   📂 Entrada: {input_file}")
    print(f"   📂 Saída: {output_file}")
    
    # Carrega arquivo JSON
    with open(input_file, 'r', encoding='utf-8') as f:
        book_data = json.load(f)
    
    total_content_items = 0
    total_words = 0
    
    # Processa cada parte do livro
    for part_idx, part in enumerate(book_data):
        print(f"   📖 Processando Parte {part_idx + 1}: {part.get('part_title', 'Sem título')}")
        
        # Processa capítulos
        for chapter_idx, chapter in enumerate(part.get('chapters', [])):
            chapter_title = chapter.get('chapter_title', 'Sem título')
            
            # Processa conteúdo do capítulo
            content_items = chapter.get('content', [])
            if content_items:
                print(f"      📝 Capítulo: {chapter_title} ({len(content_items)} itens)")
                
                for content_item in content_items:
                    if isinstance(content_item, dict) and 'content' in content_item:
                        # Conta palavras no conteúdo
                        text = content_item.get('content', '')
                        word_count = count_words(text)
                        
                        # Adiciona word_count ao item
                        content_item['word_count'] = word_count
                        
                        total_content_items += 1
                        total_words += word_count
    
    # Salva arquivo JSON com word_count
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(book_data, f, indent=2, ensure_ascii=False)
    
    print(f"\n✅ Word count adicionado com sucesso!")
    print(f"   📊 Total de itens processados: {total_content_items}")
    print(f"   📊 Total de palavras: {total_words:,}")
    print(f"   📂 Arquivo salvo: {output_file}")
    
    return True

def main():
    """Função principal"""
    print("📊 ADICIONANDO WORD COUNT AO LIVRO_EXTRACTED.JSON")
    print("=" * 60)
    
    # Arquivos
    input_file = os.path.join('webapp', 'public', 'data', 'livro_extracted.json')
    output_file = os.path.join('webapp', 'public', 'data', 'livro_en.json')
    
    # Verifica se arquivo de entrada existe
    if not os.path.exists(input_file):
        print(f"❌ Arquivo não encontrado: {input_file}")
        return False
    
    # Cria diretório de saída se não existir
    output_dir = os.path.dirname(output_file)
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
        print(f"📁 Diretório criado: {output_dir}")
    
    # Faz backup do arquivo original se existir
    if os.path.exists(output_file):
        backup_file = output_file.replace('.json', '_backup_before_word_count.json')
        with open(output_file, 'r', encoding='utf-8') as f:
            data = f.read()
        with open(backup_file, 'w', encoding='utf-8') as f:
            f.write(data)
        print(f"💾 Backup criado: {backup_file}")
    
    # Adiciona word count
    success = add_word_counts_to_json(input_file, output_file)
    
    if success:
        print(f"\n🎉 CONCLUÍDO!")
        print(f"   ✅ O arquivo {output_file} agora tem word_count em todos os itens")
        print(f"   ✅ Compatível com todos os scripts existentes")
        print(f"   ✅ Pronto para ser usado como livro_en.json padrão")
    else:
        print(f"\n❌ Erro ao processar arquivo")
        return False
    
    return True

if __name__ == "__main__":
    main()
