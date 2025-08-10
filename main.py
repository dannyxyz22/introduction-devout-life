#!/usr/bin/env python3
"""
Script principal para gerenciar o pipeline completo do projeto.
Oferece menu para executar diferentes operações.
"""

import os
import sys
import subprocess
import shutil

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

def run_script_with_args(script_path, args, description):
    """
    Executa um script Python com argumentos e exibe o resultado
    """
    print(f"\n🔄 Executando: {description}")
    print("=" * 50)
    
    try:
        cmd = [sys.executable, script_path] + args
        result = subprocess.run(cmd, 
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

def ensure_output_directory():
    """
    Garante que a pasta output existe
    """
    if not os.path.exists('output'):
        os.makedirs('output')
        print("📁 Pasta 'output' criada")

def copy_to_webapp(source_file, target_file, description="arquivo"):
    """
    Copia arquivo da pasta output para webapp/public/data
    """
    if os.path.exists(source_file):
        # Garantir que o diretório de destino existe
        target_dir = os.path.dirname(target_file)
        if not os.path.exists(target_dir):
            os.makedirs(target_dir)
        
        shutil.copy2(source_file, target_file)
        print(f"📋 {description} copiado para webapp: {target_file}")
        return True
    else:
        print(f"⚠️ {description} não encontrado para cópia: {source_file}")
        return False

def main():
    """
    Menu principal
    """
    print("📚 INTRODUCTION TO THE DEVOUT LIFE - PIPELINE MANAGER")
    print("=" * 60)
    
    # Verificar estrutura do projeto
    print("\n📂 VERIFICANDO ESTRUTURA DO PROJETO:")
    
    # Garantir que a pasta output existe
    ensure_output_directory()
    
    scripts = {
        'epub_process_new': os.path.join('scripts', 'epub_processing', 'epub_to_json_processor.py'),
        'fix_ad_hoc': os.path.join('scripts', 'json_processing', 'fix_ad_hoc.py'),
        'reorganize_json': os.path.join('scripts', 'json_processing', 'reorganize_final.py'),
        'epub_generate': os.path.join('scripts', 'epub_processing', 'gerar_epub_atualizado.py'),
        'ocr_fix': os.path.join('scripts', 'ocr_fixes', 'fix_ocr_manual.py'),
        'split_part_titles': os.path.join('scripts', 'json_processing', 'split_part_titles.py'),
        'docx_clean': os.path.join('scripts', 'translation', 'tradutor_docx_clean.py'),
        'json_reconstruct': os.path.join('scripts', 'translation', 'reconstruir_json_portugues.py')
    }
    
    data_files = {
        'json_en_output': os.path.join('output', 'livro_en.json'),
        'json_pt_output': os.path.join('output', 'livro_pt-BR.json'),
        'json_en_webapp': os.path.join('webapp', 'public', 'data', 'livro_en.json'),
        'json_pt_webapp': os.path.join('webapp', 'public', 'data', 'livro_pt-BR.json'),
        'epub_source': os.path.join('data', 'Introduction_to_the_Devout_Life.epub')
    }
    
    # Verificar scripts
    missing_scripts = []
    for name, path in scripts.items():
        if not check_file_exists(path, f"Script {name}"):
            missing_scripts.append(name)
    
    # Verificar dados
    for name, path in data_files.items():
        check_file_exists(path, f"Dados {name}")
    
    # Verificar arquivo EPUB fonte
    epub_source_exists = check_file_exists(data_files['epub_source'], "EPUB fonte")
    
    if missing_scripts:
        print(f"\n⚠️  Alguns scripts não foram encontrados: {', '.join(missing_scripts)}")
        print("   Certifique-se de que a estrutura do projeto está correta.")
    
    while True:
        print(f"\n📋 MENU PRINCIPAL:")
        print(f"1. 📖 Processar EPUB → JSON (com word_count automático)")
        print(f"2. 🔧 Aplicar correções ad hoc")
        print(f"3. 📋 Reorganizar JSON baseado no summary.csv")
        print(f"4. 🩹 Corrigir OCR no JSON inglês")
        print(f"5. � Merge part name to first chapter")
        print(f"6. �📄 Gerar DOCX para tradução")
        print(f"7. 🌐 Reconstruir JSON português (após tradução)")
        print(f"8. 📚 Gerar EPUBs atualizados")
        print(f"9. 🔄 Pipeline completo (EPUB → Ad hoc → Reorganizar → OCR → Split → DOCX → Reconstruir → EPUBs)")
        print(f"10. ℹ️  Mostrar status do projeto")
        print(f"11. 🚀 Iniciar aplicação web")
        print(f"12. 📊 Comparar contagem de caracteres dos EPUBs")
        print(f"13. 🔍 Analisar conteúdo adicionado nas versões geradas")
        print(f"14. ❌ Sair")
        
        choice = input(f"\nEscolha uma opção (1-14): ").strip()
        
        if choice == '1':
            if not epub_source_exists:
                print("❌ Arquivo EPUB fonte não encontrado! Verifique se 'Introduction_to_the_Devout_Life.epub' está na pasta 'data'.")
            else:
                # Prioriza o novo processador com word_count automático
                if 'epub_process_new' not in missing_scripts:
                    success = run_script_with_args(scripts['epub_process_new'], [data_files['epub_source']], 
                                        "Processamento de EPUB (com word_count automático)")
                    if success:
                        copy_to_webapp(data_files['json_en_output'], data_files['json_en_webapp'], "JSON inglês")
                else:
                    print("❌ Nenhum script de processamento encontrado!")
                
        elif choice == '2':
            if 'fix_ad_hoc' not in missing_scripts:
                success = run_script(scripts['fix_ad_hoc'], "Correções ad hoc")
                if success:
                    copy_to_webapp(data_files['json_en_output'], data_files['json_en_webapp'], "JSON inglês com correções ad hoc")
            else:
                print("❌ Script de correções ad hoc não encontrado!")
                
        elif choice == '3':
            if 'reorganize_json' not in missing_scripts:
                success = run_script(scripts['reorganize_json'], "Reorganização do JSON baseado no summary.csv")
                if success:
                    copy_to_webapp(data_files['json_en_output'], data_files['json_en_webapp'], "JSON inglês reorganizado")
            else:
                print("❌ Script de reorganização não encontrado!")
                
        elif choice == '4':
            if 'ocr_fix' not in missing_scripts:
                success = run_script(scripts['ocr_fix'], "Correção de OCR")
                if success:
                    copy_to_webapp(data_files['json_en_output'], data_files['json_en_webapp'], "JSON inglês corrigido")
            else:
                print("❌ Script de correção de OCR não encontrado!")
                
        elif choice == '5':
            if 'split_part_titles' not in missing_scripts:
                success = run_script(scripts['split_part_titles'], "Split part titles")
                if success:
                    copy_to_webapp(data_files['json_en_output'], data_files['json_en_webapp'], "JSON inglês com part titles divididos")
            else:
                print("❌ Script de split de títulos não encontrado!")
                
        elif choice == '6':
            if 'docx_clean' not in missing_scripts:
                run_script(scripts['docx_clean'], "Geração de DOCX para tradução")
            else:
                print("❌ Script de geração de DOCX não encontrado!")
                
        elif choice == '6':
            if 'docx_clean' not in missing_scripts:
                run_script(scripts['docx_clean'], "Geração de DOCX para tradução")
            else:
                print("❌ Script de geração de DOCX não encontrado!")
                
        elif choice == '7':
            if 'json_reconstruct' not in missing_scripts:
                success = run_script(scripts['json_reconstruct'], "Reconstrução de JSON português")
                if success:
                    copy_to_webapp(data_files['json_pt_output'], data_files['json_pt_webapp'], "JSON português")
            else:
                print("❌ Script de reconstrução não encontrado!")
                
        elif choice == '8':
            if 'epub_generate' not in missing_scripts:
                run_script_with_args(scripts['epub_generate'], ['--auto'], "Geração de EPUBs")
            else:
                print("❌ Script de geração de EPUB não encontrado!")
                
        elif choice == '9':
            if not epub_source_exists:
                print("❌ Arquivo EPUB fonte não encontrado! Verifique se 'Introduction_to_the_Devout_Life.epub' está na pasta 'data'.")
            else:
                print(f"\n🔄 EXECUTANDO PIPELINE COMPLETO...")
                success = True
                
                # 1. Processar EPUB
                if 'epub_process_new' not in missing_scripts:
                    success = run_script_with_args(scripts['epub_process_new'], [data_files['epub_source']], 
                                                 "Processamento de EPUB") and success
                    if success:
                        copy_to_webapp(data_files['json_en_output'], data_files['json_en_webapp'], "JSON inglês")
                
                # 2. Aplicar correções ad hoc
                if 'fix_ad_hoc' not in missing_scripts and success:
                    success = run_script(scripts['fix_ad_hoc'], "Correções ad hoc") and success
                    if success:
                        copy_to_webapp(data_files['json_en_output'], data_files['json_en_webapp'], "JSON inglês com correções ad hoc")
               
                # 3. Reorganizar JSON
                if 'reorganize_json' not in missing_scripts and success:
                    success = run_script(scripts['reorganize_json'], "Reorganização do JSON") and success
                    if success:
                        copy_to_webapp(data_files['json_en_output'], data_files['json_en_webapp'], "JSON inglês reorganizado")
                
                # 4. Corrigir OCR
                if 'ocr_fix' not in missing_scripts and success:
                    success = run_script(scripts['ocr_fix'], "Correção de OCR") and success
                    if success:
                        copy_to_webapp(data_files['json_en_output'], data_files['json_en_webapp'], "JSON inglês corrigido")
                
                # 5. Split part titles
                if 'split_part_titles' not in missing_scripts and success:
                    success = run_script(scripts['split_part_titles'], "Split part titles") and success
                    if success:
                        copy_to_webapp(data_files['json_en_output'], data_files['json_en_webapp'], "JSON inglês com part titles divididos")
                
                # 6. Gerar DOCX
                if 'docx_clean' not in missing_scripts and success:
                    success = run_script(scripts['docx_clean'], "Geração de DOCX") and success
                
                # 7. Reconstruir JSON português (se existir tradução)
                if 'json_reconstruct' not in missing_scripts and success:
                    # Verificar se existe arquivo de tradução para reconstruir
                    output_dir = 'output'
                    docx_files = []
                    if os.path.exists(output_dir):
                        docx_files = [f for f in os.listdir(output_dir) if f.endswith('.docx') and 'traduzido' in f.lower()]
                    
                    if docx_files:
                        success = run_script(scripts['json_reconstruct'], "Reconstrução de JSON português") and success
                        if success:
                            copy_to_webapp(data_files['json_pt_output'], data_files['json_pt_webapp'], "JSON português")
                    else:
                        print(f"\n⚠️  Arquivo de tradução não encontrado.")
                        print(f"   Para completar o pipeline, traduza o DOCX gerado e salve com 'traduzido' no nome.")
                
                # 8. Gerar EPUBs (se JSON português existir)
                if 'epub_generate' not in missing_scripts and success:
                    if os.path.exists(data_files['json_pt_output']):  # Verificar na pasta output
                        run_script_with_args(scripts['epub_generate'], ['--auto'], "Geração de EPUBs")
                    else:
                        print(f"\n⚠️  JSON português não encontrado.")
                        print(f"   Execute a tradução no Google Translate e depois a reconstrução (opção 6).")
                
                if success:
                    print(f"\n🎉 PIPELINE CONCLUÍDO!")
                else:
                    print(f"\n❌ Pipeline interrompido devido a erros.")
                
        elif choice == '10':
            print(f"\n📊 STATUS DO PROJETO:")
            print("=" * 30)
            
            # Verificar arquivos de dados na pasta output
            en_size_output = os.path.getsize(data_files['json_en_output']) / 1024 if os.path.exists(data_files['json_en_output']) else 0
            pt_size_output = os.path.getsize(data_files['json_pt_output']) / 1024 if os.path.exists(data_files['json_pt_output']) else 0
            
            # Verificar arquivos de dados na webapp
            en_size_webapp = os.path.getsize(data_files['json_en_webapp']) / 1024 if os.path.exists(data_files['json_en_webapp']) else 0
            pt_size_webapp = os.path.getsize(data_files['json_pt_webapp']) / 1024 if os.path.exists(data_files['json_pt_webapp']) else 0
            
            print(f"📂 JSON Inglês (output): {'✅' if en_size_output > 0 else '❌'} ({en_size_output:.1f} KB)")
            print(f"📂 JSON Português (output): {'✅' if pt_size_output > 0 else '❌'} ({pt_size_output:.1f} KB)")
            print(f"📋 JSON Inglês (webapp): {'✅' if en_size_webapp > 0 else '❌'} ({en_size_webapp:.1f} KB)")
            print(f"📋 JSON Português (webapp): {'✅' if pt_size_webapp > 0 else '❌'} ({pt_size_webapp:.1f} KB)")
            
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
            
            # Verificar DOCX na pasta output
            docx_files = []
            if os.path.exists(output_dir):
                docx_files = [f for f in os.listdir(output_dir) if f.endswith('.docx')]
            print(f"📄 Arquivos DOCX: {len(docx_files)}")
            if docx_files:
                for docx in docx_files:
                    docx_path = os.path.join(output_dir, docx)
                    docx_size = os.path.getsize(docx_path) / (1024 * 1024)
                    print(f"   📄 {docx} ({docx_size:.2f} MB)")
            
        elif choice == '11':
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
                
        elif choice == '12':
            print(f"\n📊 EXECUTANDO COMPARAÇÃO DE CARACTERES DOS EPUBs...")
            if os.path.exists('compare_epub_text.py'):
                run_script('compare_epub_text.py', "Comparação de contagem de caracteres")
            else:
                print("❌ Script compare_epub_text.py não encontrado!")
                
        elif choice == '13':
            print(f"\n🔍 EXECUTANDO ANÁLISE DE CONTEÚDO ADICIONADO...")
            if os.path.exists('analyze_added_content.py'):
                run_script('analyze_added_content.py', "Análise de conteúdo adicionado")
            else:
                print("❌ Script analyze_added_content.py não encontrado!")
                
        elif choice == '14':
            print(f"\n👋 Até logo!")
            break
            
        else:
            print(f"❌ Opção inválida! Escolha um número de 1 a 14.")

if __name__ == "__main__":
    main()
