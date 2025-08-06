#!/usr/bin/env python3
"""
Script de verificação dos índices EPUB.
Extrai e examina o arquivo NCX para verificar se os links estão corretos.
"""

import zipfile
import os
from xml.etree import ElementTree as ET

def verificar_indices_epub(epub_path):
    """
    Verifica se os índices do EPUB estão corretos
    """
    print(f"🔍 VERIFICANDO ÍNDICES DO EPUB: {epub_path}")
    print("=" * 60)
    
    if not os.path.exists(epub_path):
        print(f"❌ Arquivo EPUB não encontrado: {epub_path}")
        return False
    
    try:
        with zipfile.ZipFile(epub_path, 'r') as epub:
            # Lê o arquivo NCX (navegação)
            try:
                ncx_content = epub.read('OEBPS/toc.ncx').decode('utf-8')
                print("✅ Arquivo NCX encontrado")
            except KeyError:
                print("❌ Arquivo NCX não encontrado no EPUB")
                return False
            
            # Parse do XML
            root = ET.fromstring(ncx_content)
            
            # Namespace do NCX
            ns = {'ncx': 'http://www.daisy.org/z3986/2005/ncx/'}
            
            # Encontra todos os navPoints
            nav_points = root.findall('.//ncx:navPoint', ns)
            
            print(f"\n📚 Total de pontos de navegação encontrados: {len(nav_points)}")
            print("\n📋 ESTRUTURA DE NAVEGAÇÃO:")
            print("   Play Order | ID | Título | Arquivo")
            print("   " + "-" * 60)
            
            for nav_point in nav_points:
                play_order = nav_point.get('playOrder', 'N/A')
                point_id = nav_point.get('id', 'N/A')
                
                # Texto do título
                label = nav_point.find('ncx:navLabel/ncx:text', ns)
                title = label.text if label is not None else 'N/A'
                
                # Arquivo de destino
                content = nav_point.find('ncx:content', ns)
                src = content.get('src', 'N/A') if content is not None else 'N/A'
                
                print(f"   {play_order:>10} | {point_id:<15} | {title:<25} | {src}")
            
            # Verifica se existem os arquivos referenciados
            print(f"\n🔍 VERIFICANDO ARQUIVOS REFERENCIADOS:")
            arquivos_faltando = []
            arquivos_encontrados = 0
            
            for nav_point in nav_points:
                content = nav_point.find('ncx:content', ns)
                if content is not None:
                    src = content.get('src')
                    if src:
                        # Verifica se o arquivo existe no EPUB
                        try:
                            if src.startswith('text/'):
                                file_path = f'OEBPS/{src}'
                            else:
                                file_path = f'OEBPS/{src}'
                            
                            epub.read(file_path)
                            arquivos_encontrados += 1
                            print(f"   ✅ {src}")
                        except KeyError:
                            arquivos_faltando.append(src)
                            print(f"   ❌ {src} - ARQUIVO NÃO ENCONTRADO")
            
            print(f"\n📊 RESUMO:")
            print(f"   ✅ Arquivos encontrados: {arquivos_encontrados}")
            print(f"   ❌ Arquivos faltando: {len(arquivos_faltando)}")
            
            if arquivos_faltando:
                print(f"\n❌ ARQUIVOS FALTANDO:")
                for arquivo in arquivos_faltando:
                    print(f"   - {arquivo}")
                return False
            else:
                print(f"\n🎉 TODOS OS ARQUIVOS REFERENCIADOS FORAM ENCONTRADOS!")
                print(f"   ✅ A navegação do EPUB deve estar funcionando corretamente")
                return True
                
    except Exception as e:
        print(f"❌ Erro ao verificar EPUB: {e}")
        return False

def main():
    """Função principal"""
    print("🔍 VERIFICADOR DE ÍNDICES EPUB")
    print("=" * 40)
    
    # Procura EPUBs
    epub_files = []
    for file in os.listdir('.'):
        if file.endswith('.epub'):
            epub_files.append(file)
    
    if not epub_files:
        print("❌ Nenhum arquivo EPUB encontrado na pasta atual!")
        return
    
    print("📖 Arquivos EPUB encontrados:")
    for i, file in enumerate(epub_files):
        print(f"   {i+1}. {file}")
    
    # Se só há um arquivo, usa esse
    if len(epub_files) == 1:
        epub_file = epub_files[0]
        print(f"\n📚 Verificando automaticamente: {epub_file}")
    else:
        try:
            choice = int(input("\nEscolha o arquivo (número): ")) - 1
            epub_file = epub_files[choice]
        except (ValueError, IndexError):
            print("❌ Escolha inválida!")
            return
    
    # Verifica o arquivo
    sucesso = verificar_indices_epub(epub_file)
    
    if sucesso:
        print("\n✅ VERIFICAÇÃO CONCLUÍDA - ÍNDICES CORRETOS!")
    else:
        print("\n❌ VERIFICAÇÃO CONCLUÍDA - PROBLEMAS ENCONTRADOS!")

if __name__ == "__main__":
    main()
