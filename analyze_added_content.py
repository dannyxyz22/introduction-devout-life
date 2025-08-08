#!/usr/bin/env python3
"""
Script para identificar conteúdo que está na versão em inglês mas não na original
"""

import os
import zipfile
import re
from xml.etree import ElementTree as ET
from html import unescape
from difflib import SequenceMatcher

def extract_text_from_xhtml(content):
    """
    Extrai texto de conteúdo XHTML, removendo tags HTML
    """
    try:
        # Remove namespace declarations que podem causar problemas
        content = re.sub(r'xmlns[^=]*="[^"]*"', '', content)
        
        # Parse XML/HTML
        root = ET.fromstring(f'<root>{content}</root>')
        
        # Extrai todo o texto
        text = ET.tostring(root, encoding='unicode', method='text')
        
        # Limpa e normaliza
        text = unescape(text)  # Decodifica entidades HTML
        text = re.sub(r'\s+', ' ', text)  # Normaliza espaços
        text = text.strip()
        
        return text
    except Exception as e:
        # Fallback: usa regex para remover tags
        text = re.sub(r'<[^>]+>', '', content)
        text = unescape(text)
        text = re.sub(r'\s+', ' ', text)
        return text.strip()

def extract_full_text_from_epub(epub_path):
    """
    Extrai todo o texto de um arquivo EPUB
    """
    if not os.path.exists(epub_path):
        return None, f"Arquivo não encontrado: {epub_path}"
    
    try:
        extracted_texts = []
        
        with zipfile.ZipFile(epub_path, 'r') as epub:
            # Lista todos os arquivos
            file_list = epub.namelist()
            
            # Procura por arquivos de conteúdo
            content_files = []
            for file_name in file_list:
                if (file_name.endswith('.xhtml') or file_name.endswith('.html') or file_name.endswith('.xml')) and \
                   not file_name.endswith('toc.html') and \
                   not file_name.endswith('container.xml') and \
                   not file_name.endswith('_page_map_.xml') and \
                   not file_name.endswith('_toc_ncx_.ncx') and \
                   not file_name.endswith('volume.opf') and \
                   'META-INF' not in file_name:
                    content_files.append(file_name)
            
            # Ordena arquivos para manter ordem consistente
            content_files.sort()
            
            for file_name in content_files:
                try:
                    with epub.open(file_name) as f:
                        content = f.read().decode('utf-8', errors='ignore')
                        text = extract_text_from_xhtml(content)
                        
                        if text:  # Só adiciona se há texto
                            extracted_texts.append(text)
                        
                except Exception as e:
                    print(f"   ⚠️ Erro ao processar {file_name}: {e}")
            
            # Junta todo o texto
            full_text = ' '.join(extracted_texts)
            
            return full_text, "OK"
            
    except Exception as e:
        return None, f"Erro ao abrir EPUB: {e}"

def normalize_text(text):
    """
    Normaliza texto para comparação
    """
    if not text:
        return ""
    
    # Remove CSS e estilos
    text = re.sub(r'\{[^}]*\}', ' ', text)
    text = re.sub(r'[.#][a-zA-Z_-]+\s*\{[^}]*\}', ' ', text)
    
    # Remove espaços múltiplos
    text = re.sub(r'\s+', ' ', text)
    
    # Remove caracteres especiais desnecessários
    text = re.sub(r'[^\w\s.,;:!?()"-]', ' ', text)
    
    return text.strip().lower()

def find_segments_in_english_not_in_original(original_text, english_text):
    """
    Encontra segmentos que estão no inglês mas não no original
    """
    # Normaliza os textos
    original_norm = normalize_text(original_text)
    english_norm = normalize_text(english_text)
    
    # Divide em palavras
    original_words = set(original_norm.split())
    english_words = set(english_norm.split())
    
    # Palavras que estão no inglês mas não no original
    unique_words = english_words - original_words
    
    # Divide o texto inglês em sentenças para buscar contexto
    sentences = re.split(r'[.!?]+', english_text)
    
    unique_segments = []
    
    for sentence in sentences:
        sentence_norm = normalize_text(sentence)
        sentence_words = set(sentence_norm.split())
        
        # Se a sentença tem palavras únicas e é suficientemente longa
        if len(sentence_words & unique_words) > 0 and len(sentence_norm) > 20:
            # Verifica se a sentença não está no original
            if sentence_norm not in original_norm:
                unique_segments.append({
                    'text': sentence.strip(),
                    'length': len(sentence.strip()),
                    'unique_words': len(sentence_words & unique_words)
                })
    
    return unique_segments, unique_words

def identify_added_content_types(segments):
    """
    Identifica tipos de conteúdo adicionado
    """
    types = {
        'license': [],
        'metadata': [],
        'navigation': [],
        'formatting': [],
        'other': []
    }
    
    for segment in segments:
        text = segment['text'].lower()
        
        if any(word in text for word in ['licença', 'license', 'copyright', 'creative commons', 'domínio público']):
            types['license'].append(segment)
        elif any(word in text for word in ['google books', 'digitalizada', 'scanned', 'edition', 'tradução']):
            types['metadata'].append(segment)
        elif any(word in text for word in ['part', 'chapter', 'título', 'title page', 'página']):
            types['navigation'].append(segment)
        elif any(word in text for word in ['font-family', 'margin', 'padding', 'text-align', 'css']):
            types['formatting'].append(segment)
        else:
            types['other'].append(segment)
    
    return types

def main():
    """
    Função principal
    """
    print("🔍 ANÁLISE DE CONTEÚDO ADICIONADO NA VERSÃO EM INGLÊS")
    print("=" * 60)
    
    # Extrai texto completo dos EPUBs
    print("📖 Extraindo texto do EPUB original...")
    original_text, status = extract_full_text_from_epub('data/Introduction_to_the_Devout_Life.epub')
    if not original_text:
        print(f"❌ Erro: {status}")
        return
    print(f"✅ Original extraído: {len(original_text):,} caracteres")

    print("\n📖 Extraindo texto do EPUB em inglês...")
    english_text, status = extract_full_text_from_epub('output/Introduction_to_the_Devout_Life_EN.epub')
    if not english_text:
        print(f"❌ Erro: {status}")
        return
    print(f"✅ Inglês extraído: {len(english_text):,} caracteres")    # Encontra segmentos únicos
    print("\n🔍 Analisando diferenças...")
    unique_segments, unique_words = find_segments_in_english_not_in_original(original_text, english_text)
    
    print(f"📊 Segmentos únicos encontrados: {len(unique_segments)}")
    print(f"📊 Palavras únicas encontradas: {len(unique_words)}")
    
    # Classifica por tipo
    content_types = identify_added_content_types(unique_segments)
    
    print("\n📋 CONTEÚDO ADICIONADO POR CATEGORIA:")
    print("=" * 50)
    
    for category, segments in content_types.items():
        if segments:
            category_names = {
                'license': 'LICENÇA E DIREITOS AUTORAIS',
                'metadata': 'METADADOS E INFORMAÇÕES DA EDIÇÃO',
                'navigation': 'NAVEGAÇÃO E ESTRUTURA',
                'formatting': 'FORMATAÇÃO E CSS',
                'other': 'OUTROS'
            }
            
            print(f"\n🏷️ {category_names[category]} ({len(segments)} segmentos):")
            print("-" * 40)
            
            for i, segment in enumerate(segments[:5], 1):  # Mostra até 5 exemplos
                print(f"\n{i}. ({segment['length']} caracteres)")
                print(f"   \"{segment['text'][:200]}{'...' if len(segment['text']) > 200 else ''}\"")
            
            if len(segments) > 5:
                print(f"\n   [...e mais {len(segments) - 5} segmentos]")
    
    # Salva resultado detalhado
    with open('conteudo_adicionado_ingles.txt', 'w', encoding='utf-8') as f:
        f.write("CONTEÚDO ADICIONADO NA VERSÃO EM INGLÊS\n")
        f.write("=" * 50 + "\n\n")
        
        for category, segments in content_types.items():
            if segments:
                category_names = {
                    'license': 'LICENÇA E DIREITOS AUTORAIS',
                    'metadata': 'METADADOS E INFORMAÇÕES DA EDIÇÃO', 
                    'navigation': 'NAVEGAÇÃO E ESTRUTURA',
                    'formatting': 'FORMATAÇÃO E CSS',
                    'other': 'OUTROS'
                }
                
                f.write(f"\n{category_names[category]}\n")
                f.write("-" * 40 + "\n")
                
                for i, segment in enumerate(segments, 1):
                    f.write(f"\n{i}. ({segment['length']} caracteres)\n")
                    f.write(f"{segment['text']}\n")
                    f.write("-" * 20 + "\n")
    
    # Palavras únicas mais comuns
    print(f"\n📝 PALAVRAS ÚNICAS MAIS RELEVANTES:")
    print("-" * 30)
    
    # Filtra palavras relevantes (não muito curtas)
    relevant_words = [word for word in unique_words if len(word) > 3]
    relevant_words = sorted(relevant_words)[:20]  # Primeiras 20
    
    for word in relevant_words:
        print(f"   • {word}")
    
    print(f"\n💾 Relatório detalhado salvo em: conteudo_adicionado_ingles.txt")
    print(f"✅ Análise concluída!")

if __name__ == "__main__":
    main()
