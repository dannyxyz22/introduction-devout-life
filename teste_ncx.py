#!/usr/bin/env python3
import json
import sys
import os

# Adicionar o caminho para os scripts
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'scripts', 'epub_processing'))

from gerar_epub_atualizado import create_ncx_file

# Carregar dados do JSON
with open('webapp/public/data/livro_pt-BR.json', 'r', encoding='utf-8') as f:
    book_data = json.load(f)

# Testar a função NCX com parâmetros corretos
print("🧪 TESTE ISOLADO DA FUNÇÃO NCX")
print("=====================================")

# Teste 1: sem oração e prefácio
print("📋 Teste 1: has_prayer_in_json=False, has_preface_in_json=False")
ncx_content_1 = create_ncx_file(book_data, 'pt', False, False)
with open('teste_ncx_1.xml', 'w', encoding='utf-8') as f:
    f.write(ncx_content_1)
print("   ✅ Arquivo criado: teste_ncx_1.xml")

# Teste 2: com oração e prefácio  
print("📋 Teste 2: has_prayer_in_json=True, has_preface_in_json=True")
ncx_content_2 = create_ncx_file(book_data, 'pt', True, True)
with open('teste_ncx_2.xml', 'w', encoding='utf-8') as f:
    f.write(ncx_content_2)
print("   ✅ Arquivo criado: teste_ncx_2.xml")

print("🔍 Verificando diferenças:")
print("Teste 1 (sem oração/prefácio) - primeiras linhas:")
with open('teste_ncx_1.xml', 'r', encoding='utf-8') as f:
    lines = f.readlines()[:25]
    for i, line in enumerate(lines, 1):
        if 'dedicatory' in line.lower() or 'preface' in line.lower():
            print(f"   LINHA {i}: {line.strip()}")

print("\nTeste 2 (com oração/prefácio) - primeiras linhas:")
with open('teste_ncx_2.xml', 'r', encoding='utf-8') as f:
    lines = f.readlines()[:25]
    for i, line in enumerate(lines, 1):
        if 'dedicatory' in line.lower() or 'preface' in line.lower():
            print(f"   LINHA {i}: {line.strip()}")
