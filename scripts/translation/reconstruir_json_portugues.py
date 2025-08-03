#!/usr/bin/env python3
"""
Script para reconstruir o JSON em português a partir do .docx traduzido.
Execute este script depois de traduzir o arquivo .docx no Google Translate.
"""

import os
import sys

# Importar a função do script limpo
from tradutor_docx_clean import reconstruct_from_clean_docx

def main():
    """
    Executa a reconstrução do JSON em português
    """
    print("🔄 RECONSTRUÇÃO DE JSON A PARTIR DO DOCX TRADUZIDO")
    print("=" * 55)
    
    # Detectar diretório base do projeto
    script_dir = os.path.dirname(os.path.abspath(__file__))
    project_root = os.path.dirname(os.path.dirname(script_dir))
    
    # Arquivos esperados
    original_json = os.path.join(project_root, 'webapp', 'public', 'data', 'livro_en.json')
    output_json = os.path.join(project_root, 'webapp', 'public', 'data', 'livro_pt-BR.json')
    
    # Verificar se arquivo original existe
    if not os.path.exists(original_json):
        print(f"❌ Arquivo original não encontrado: {original_json}")
        return
    
    # Procurar arquivo traduzido
    docx_files = [f for f in os.listdir('.') if f.endswith('.docx') and 'traduzido' in f.lower()]
    
    if not docx_files:
        # Procurar arquivo específico
        expected_file = 'livro_en_CLEAN_for_translation.docx'
        if os.path.exists(expected_file):
            print(f"⚠️  Encontrado arquivo original: {expected_file}")
            print(f"   Este parece ser o arquivo original, não o traduzido.")
            print(f"   Você deve primeiro:")
            print(f"   1. 📤 Fazer upload em https://translate.google.com")
            print(f"   2. 🇧🇷 Traduzir de Inglês para Português")
            print(f"   3. 📥 Baixar o arquivo traduzido")
            print(f"   4. 🔄 Executar este script novamente")
            return
        
        print(f"❌ Nenhum arquivo .docx traduzido encontrado!")
        print(f"   Procurando por arquivos que contenham 'traduzido' no nome.")
        print(f"   Certifique-se de que o arquivo baixado do Google Translate está na pasta atual.")
        
        # Mostrar arquivos .docx disponíveis
        all_docx = [f for f in os.listdir('.') if f.endswith('.docx')]
        if all_docx:
            print(f"\n📂 Arquivos .docx encontrados:")
            for i, file in enumerate(all_docx, 1):
                print(f"   {i}. {file}")
            
            choice = input(f"\nEscolha um arquivo (1-{len(all_docx)}) ou ENTER para cancelar: ").strip()
            
            if choice.isdigit() and 1 <= int(choice) <= len(all_docx):
                translated_docx = all_docx[int(choice) - 1]
            else:
                print("❌ Operação cancelada.")
                return
        else:
            print(f"❌ Nenhum arquivo .docx encontrado na pasta atual.")
            return
    else:
        # Usar o primeiro arquivo encontrado
        translated_docx = docx_files[0]
        print(f"📂 Arquivo traduzido encontrado: {translated_docx}")
    
    # Verificar se arquivo traduzido existe
    if not os.path.exists(translated_docx):
        print(f"❌ Arquivo traduzido não encontrado: {translated_docx}")
        return
    
    # Criar backup se necessário
    if os.path.exists(output_json):
        backup_file = output_json.replace('.json', '_backup_before_translation.json')
        print(f"💾 Criando backup: {backup_file}")
        
        import shutil
        shutil.copy2(output_json, backup_file)
    
    # Executar reconstrução
    try:
        reconstruct_from_clean_docx(translated_docx, output_json, original_json)
        
        print(f"\n🎉 TRADUÇÃO CONCLUÍDA COM SUCESSO!")
        print(f"   📂 Arquivo gerado: {output_json}")
        print(f"   🇧🇷 O livro agora está disponível em português!")
        
    except Exception as e:
        print(f"\n❌ ERRO durante a reconstrução:")
        print(f"   {str(e)}")
        print(f"\n🔧 Possíveis soluções:")
        print(f"   1. Verifique se o arquivo .docx foi traduzido pelo Google Translate")
        print(f"   2. Certifique-se de que os marcadores ###IDXXXX### foram preservados")
        print(f"   3. Verifique se o arquivo não foi corrompido durante o download")

if __name__ == "__main__":
    main()
