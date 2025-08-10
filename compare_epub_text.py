#!/usr/bin/env python3
"""
Script para extrair texto dos EPUBs e comparar contagem de caracteres
"""

import os
import zipfile
import re
from xml.etree import ElementTree as ET
from html import unescape
import sys

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

def extract_text_from_epub(epub_path):
    """
    Extrai todo o texto de um arquivo EPUB
    """
    if not os.path.exists(epub_path):
        return None, f"Arquivo não encontrado: {epub_path}"

    try:
        extracted_texts = []
        file_count = 0

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

            print(f"📁 Arquivos de conteúdo encontrados em {os.path.basename(epub_path)}:")

            for file_name in content_files:
                try:
                    with epub.open(file_name) as f:
                        content = f.read().decode('utf-8', errors='ignore')
                        text = extract_text_from_xhtml(content)

                        if text:  # Só adiciona se há texto
                            extracted_texts.append(text)
                            char_count = len(text)
                            print(f"   📄 {file_name}: {char_count:,} caracteres")
                            file_count += 1

                except Exception as e:
                    print(f"   ⚠️ Erro ao processar {file_name}: {e}")

            # Junta todo o texto
            full_text = ' '.join(extracted_texts)

            return full_text, f"✅ {file_count} arquivos processados"

    except Exception as e:
        return None, f"Erro ao abrir EPUB: {e}"

def count_characters(text):
    """
    Conta diferentes tipos de caracteres
    """
    if not text:
        return {
            'total': 0,
            'with_spaces': 0,
            'without_spaces': 0,
            'letters_only': 0,
            'words': 0
        }

    total_chars = len(text)
    chars_without_spaces = len(text.replace(' ', ''))
    letters_only = len(re.sub(r'[^a-zA-ZÀ-ÿ]', '', text))
    words = len(text.split())

    return {
        'total': total_chars,
        'with_spaces': total_chars,
        'without_spaces': chars_without_spaces,
        'letters_only': letters_only,
        'words': words
    }

def format_number(num):
    """
    Formata número com separadores de milhares
    """
    return f"{num:,}".replace(',', '.')

def main():
    """
    Função principal
    """
    print("📊 COMPARAÇÃO DE TEXTO DOS EPUBs")
    print("=" * 50)

    # Arquivos para analisar com suas localizações
    epub_files = {
        'Original': 'data/Introduction_to_the_Devout_Life.epub',
        'Inglês (Gerado)': 'output/Introduction to the Devout Life_EN.epub',
        'Português (Gerado)': 'output/Filoteia - Introdução à vida devota pt-BR.epub'
    }

    results = {}

    for name, filename in epub_files.items():
        print(f"\n🔍 Analisando: {name}")
        print("-" * 30)

        text, status = extract_text_from_epub(filename)
        print(f"   {status}")

        if text:
            char_counts = count_characters(text)
            results[name] = char_counts

            print(f"\n📈 Estatísticas de {name}:")
            print(f"   📝 Total de caracteres: {format_number(char_counts['total'])}")
            print(f"   🔤 Caracteres (sem espaços): {format_number(char_counts['without_spaces'])}")
            print(f"   🔡 Apenas letras: {format_number(char_counts['letters_only'])}")
            print(f"   📖 Palavras: {format_number(char_counts['words'])}")

            # Salva amostra do texto
            sample_file = f"sample_text_{name.lower().replace(' ', '_').replace('(', '').replace(')', '')}.txt"
            with open(sample_file, 'w', encoding='utf-8') as f:
                f.write(f"AMOSTRA DE TEXTO - {name}\n")
                f.write("=" * 50 + "\n\n")
                f.write(text[:2000])  # Primeiros 2000 caracteres
                if len(text) > 2000:
                    f.write("\n\n[...texto continua...]")
            print(f"   💾 Amostra salva em: {sample_file}")
        else:
            results[name] = None
            print(f"   ❌ Falha na extração")

    # Tabela comparativa
    print(f"\n📊 TABELA COMPARATIVA")
    print("=" * 80)

    # Cabeçalho
    print(f"{'Métrica':<25} {'Original':<15} {'Inglês':<15} {'Português':<15}")
    print("-" * 80)

    if all(results.values()):
        # Dados para comparação
        metrics = [
            ('Total de caracteres', 'total'),
            ('Sem espaços', 'without_spaces'),
            ('Apenas letras', 'letters_only'),
            ('Palavras', 'words')
        ]

        for metric_name, metric_key in metrics:
            row = f"{metric_name:<25}"
            for name in ['Original', 'Inglês (Gerado)', 'Português (Gerado)']:
                if results[name]:
                    value = format_number(results[name][metric_key])
                    row += f" {value:<14}"
                else:
                    row += f" {'N/A':<14}"
            print(row)

    # Análise de diferenças
    print(f"\n🔍 ANÁLISE DE DIFERENÇAS")
    print("=" * 40)

    if results['Original'] and results['Inglês (Gerado)']:
        original_chars = results['Original']['total']
        english_chars = results['Inglês (Gerado)']['total']
        diff_en = english_chars - original_chars
        percent_en = (diff_en / original_chars) * 100 if original_chars > 0 else 0

        print(f"📈 Inglês vs Original:")
        print(f"   Diferença: {diff_en:+,} caracteres ({percent_en:+.1f}%)")

    if results['Original'] and results['Português (Gerado)']:
        original_chars = results['Original']['total']
        portuguese_chars = results['Português (Gerado)']['total']
        diff_pt = portuguese_chars - original_chars
        percent_pt = (diff_pt / original_chars) * 100 if original_chars > 0 else 0

        print(f"📈 Português vs Original:")
        print(f"   Diferença: {diff_pt:+,} caracteres ({percent_pt:+.1f}%)")

    if results['Inglês (Gerado)'] and results['Português (Gerado)']:
        english_chars = results['Inglês (Gerado)']['total']
        portuguese_chars = results['Português (Gerado)']['total']
        diff_langs = portuguese_chars - english_chars
        percent_langs = (diff_langs / english_chars) * 100 if english_chars > 0 else 0

        print(f"📈 Português vs Inglês:")
        print(f"   Diferença: {diff_langs:+,} caracteres ({percent_langs:+.1f}%)")

    print(f"\n✅ Análise concluída!")

if __name__ == "__main__":
    main()
