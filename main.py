#!/usr/bin/env python3
"""
Script principal para gerenciar o pipeline completo do projeto.
Oferece menu interativo para executar diferentes operações.
"""

import os
import sys
import subprocess

def run_script(script_path, description):
    """
    Executa um script Python e exibe o resultado
    """
    print(f"\n🔄 Executando: {description}")
    print("=" * 50)
    
    try:
        result = subprocess.run([sys.executable, script_path], 
                              capture_output=False, 
                              cwd=os.getcwd())
        
        if result.returncode == 0:
            print(f"\n✅ {description} - Concluído com sucesso!")
        else:
            print(f"\n❌ {description} - Erro na execução!")
            
        return result.returncode == 0
        
    except Exception as e:
        print(f"\n❌ Erro ao executar {description}: {str(e)}")
        return False

def check_file_exists(file_path, description="arquivo"):
    """
    Verifica se um arquivo existe
    """
    if os.path.exists(file_path):
        print(f"✅ {description}: {file_path}")
        return True
    else:
        print(f"❌ {description} não encontrado: {file_path}")
        return False

def main():
    """
    Menu principal
    """
    print("📚 INTRODUCTION TO THE DEVOUT LIFE - PIPELINE MANAGER")
    print("=" * 60)
    
    # Verificar estrutura do projeto
    print("\n📂 VERIFICANDO ESTRUTURA DO PROJETO:")
    
    scripts = {
        'epub_process': os.path.join('scripts', 'epub_processing', 'process_epub.py'),
        'epub_process_new': os.path.join('scripts', 'epub_processing', 'epub_to_json_processor.py'),
        'reorganize_json': 'reorganize_final.py',
        'epub_generate': os.path.join('scripts', 'epub_processing', 'gerar_epub_atualizado.py'),
        'ocr_fix': os.path.join('scripts', 'ocr_fixes', 'fix_ocr_manual.py'),
        'docx_clean': os.path.join('scripts', 'translation', 'tradutor_docx_clean.py'),
        'json_reconstruct': os.path.join('scripts', 'translation', 'reconstruir_json_portugues.py')
    }
    
    data_files = {
        'json_en': os.path.join('webapp', 'public', 'data', 'livro_en.json'),
        'json_pt': os.path.join('webapp', 'public', 'data', 'livro_pt-BR.json')
    }
    
    # Verificar scripts
    missing_scripts = []
    for name, path in scripts.items():
        if not check_file_exists(path, f"Script {name}"):
            missing_scripts.append(name)
    
    # Verificar dados
    for name, path in data_files.items():
        check_file_exists(path, f"Dados {name}")
    
    if missing_scripts:
        print(f"\n⚠️  Alguns scripts não foram encontrados: {', '.join(missing_scripts)}")
        print("   Certifique-se de que a estrutura do projeto está correta.")
    
    while True:
        print(f"\n📋 MENU PRINCIPAL:")
        print(f"1. 📖 Processar EPUB → JSON (com word_count automático)")
        print(f"2. � Reorganizar JSON baseado no summary.csv")
        print(f"3. �🔧 Corrigir OCR no JSON inglês")
        print(f"4. 📄 Gerar DOCX para tradução")
        print(f"5. 🌐 Reconstruir JSON português (após tradução)")
        print(f"6. 📚 Gerar EPUBs atualizados")
        print(f"7. 🔄 Pipeline completo (EPUB → Reorganizar → OCR → DOCX → EPUBs)")
        print(f"8. ℹ️  Mostrar status do projeto")
        print(f"9. 🚀 Iniciar aplicação web")
        print(f"10. 📊 Comparar contagem de caracteres dos EPUBs")
        print(f"11. 🔍 Analisar conteúdo adicionado nas versões geradas")
        print(f"12. ❌ Sair")
        
        choice = input(f"\nEscolha uma opção (1-12): ").strip()
        
        if choice == '1':
            # Prioriza o novo processador com word_count automático
            if 'epub_process_new' not in missing_scripts:
                run_script(scripts['epub_process_new'], "Processamento de EPUB (com word_count automático)")
            elif 'epub_process' not in missing_scripts:
                print("⚠️  Usando processador antigo - recomenda-se usar o novo com word_count automático")
                run_script(scripts['epub_process'], "Processamento de EPUB (versão antiga)")
            else:
                print("❌ Nenhum script de processamento encontrado!")
                
        elif choice == '2':
            if 'reorganize_json' not in missing_scripts:
                run_script(scripts['reorganize_json'], "Reorganização do JSON baseado no summary.csv")
            else:
                print("❌ Script de reorganização não encontrado!")
                
        elif choice == '3':
            if 'ocr_fix' not in missing_scripts:
                run_script(scripts['ocr_fix'], "Correção de OCR")
            else:
                print("❌ Script de correção de OCR não encontrado!")
                
        elif choice == '4':
            if 'docx_clean' not in missing_scripts:
                run_script(scripts['docx_clean'], "Geração de DOCX para tradução")
            else:
                print("❌ Script de geração de DOCX não encontrado!")
                
        elif choice == '5':
            if 'json_reconstruct' not in missing_scripts:
                run_script(scripts['json_reconstruct'], "Reconstrução de JSON português")
            else:
                print("❌ Script de reconstrução não encontrado!")
                
        elif choice == '6':
            if 'epub_generate' not in missing_scripts:
                run_script(scripts['epub_generate'], "Geração de EPUBs")
            else:
                print("❌ Script de geração de EPUB não encontrado!")
                
        elif choice == '7':
            print(f"\n🔄 EXECUTANDO PIPELINE COMPLETO...")
            success = True
            
            # 1. Processar EPUB
            if 'epub_process_new' not in missing_scripts:
                success = run_script(scripts['epub_process_new'], "Processamento de EPUB") and success
            elif 'epub_process' not in missing_scripts and success:
                success = run_script(scripts['epub_process'], "Processamento de EPUB (versão antiga)") and success
            
            # 2. Reorganizar JSON
            if 'reorganize_json' not in missing_scripts and success:
                success = run_script(scripts['reorganize_json'], "Reorganização do JSON") and success
            
            # 3. Corrigir OCR
            if 'ocr_fix' not in missing_scripts and success:
                success = run_script(scripts['ocr_fix'], "Correção de OCR") and success
            
            # 4. Gerar DOCX
            if 'docx_clean' not in missing_scripts and success:
                success = run_script(scripts['docx_clean'], "Geração de DOCX") and success
            
            # 5. Gerar EPUBs (se JSON português existir)
            if 'epub_generate' not in missing_scripts and success:
                if os.path.exists(data_files['json_pt']):
                    run_script(scripts['epub_generate'], "Geração de EPUBs")
                else:
                    print(f"\n⚠️  JSON português não encontrado.")
                    print(f"   Execute a tradução no Google Translate e depois a reconstrução (opção 5).")
            
            if success:
                print(f"\n🎉 PIPELINE CONCLUÍDO!")
            else:
                print(f"\n❌ Pipeline interrompido devido a erros.")
                
        elif choice == '8':
            print(f"\n📊 STATUS DO PROJETO:")
            print("=" * 30)
            
            # Verificar arquivos de dados
            en_size = os.path.getsize(data_files['json_en']) / 1024 if os.path.exists(data_files['json_en']) else 0
            pt_size = os.path.getsize(data_files['json_pt']) / 1024 if os.path.exists(data_files['json_pt']) else 0
            
            print(f"📂 JSON Inglês: {'✅' if en_size > 0 else '❌'} ({en_size:.1f} KB)")
            print(f"📂 JSON Português: {'✅' if pt_size > 0 else '❌'} ({pt_size:.1f} KB)")
            
            # Verificar outputs
            output_dir = 'output'
            if os.path.exists(output_dir):
                epubs = [f for f in os.listdir(output_dir) if f.endswith('.epub')]
                print(f"📚 EPUBs gerados: {len(epubs)}")
                for epub in epubs:
                    epub_path = os.path.join(output_dir, epub)
                    epub_size = os.path.getsize(epub_path) / (1024 * 1024)
                    print(f"   📖 {epub} ({epub_size:.2f} MB)")
            else:
                print(f"📚 EPUBs gerados: 0")
            
            # Verificar DOCX
            docx_files = [f for f in os.listdir('.') if f.endswith('.docx')]
            print(f"📄 Arquivos DOCX: {len(docx_files)}")
            
        elif choice == '9':
            webapp_dir = os.path.join('webapp')
            if os.path.exists(webapp_dir):
                print(f"\n🚀 Iniciando aplicação web...")
                try:
                    subprocess.run(['npm', 'start'], cwd=webapp_dir)
                except KeyboardInterrupt:
                    print(f"\n👋 Aplicação web encerrada.")
                except Exception as e:
                    print(f"\n❌ Erro ao iniciar aplicação: {str(e)}")
                    print(f"   Certifique-se de que Node.js está instalado e execute 'npm install' na pasta webapp.")
            else:
                print(f"❌ Pasta webapp não encontrada!")
                
        elif choice == '10':
            print(f"\n� EXECUTANDO COMPARAÇÃO DE CARACTERES DOS EPUBs...")
            if os.path.exists('compare_epub_text.py'):
                run_script('compare_epub_text.py', "Comparação de contagem de caracteres")
            else:
                print("❌ Script compare_epub_text.py não encontrado!")
                
        elif choice == '11':
            print(f"\n🔍 EXECUTANDO ANÁLISE DE CONTEÚDO ADICIONADO...")
            if os.path.exists('analyze_added_content.py'):
                run_script('analyze_added_content.py', "Análise de conteúdo adicionado")
            else:
                print("❌ Script analyze_added_content.py não encontrado!")
                
        elif choice == '12':
            print(f"\n�👋 Até logo!")
            break
            
        else:
            print(f"❌ Opção inválida! Escolha um número de 1 a 12.")

if __name__ == "__main__":
    main()
