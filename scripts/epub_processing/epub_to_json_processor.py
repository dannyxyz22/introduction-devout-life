#!/usr/bin/env python3
"""
Processador EPUB para JSON com word_count automático.
Classe unificada que sempre inclui contagem de palavras no JSON gerado.
"""

import json
import re
import os
import zipfile
import tempfile
from bs4 import BeautifulSoup


class EpubToJsonProcessor:
    """
    Processador para converter arquivos EPUB em JSON estruturado.
    Sempre inclui word_count automaticamente para manter compatibilidade.
    """
    
    def __init__(self):
        """Inicializa o processador"""
        self.total_words = 0
        self.total_content_items = 0
        self.total_chapters = 0
        self.total_parts = 0
    
    def count_words(self, text):
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
    
    def extract_epub(self, epub_path, extract_dir):
        """Extrai conteúdo do EPUB para diretório temporário"""
        with zipfile.ZipFile(epub_path, 'r') as epub:
            epub.extractall(extract_dir)
        return extract_dir
    
    def find_content_files(self, extract_dir):
        """Encontra arquivos de conteúdo no EPUB extraído"""
        content_files = []
        
        # Procura por arquivos XML/XHTML de conteúdo
        for root, dirs, files in os.walk(extract_dir):
            for file in files:
                if file.endswith(('.xml', '.xhtml', '.html')):
                    file_path = os.path.join(root, file)
                    # Verifica se é um arquivo de conteúdo (não navegação)
                    if 'content' in file.lower() or 'chapter' in file.lower():
                        content_files.append(file_path)
        
        # Ordena os arquivos por nome para manter ordem
        content_files.sort()
        return content_files
    
    def process_content_item(self, text_content):
        """
        Processa um item de conteúdo, limpando o texto e adicionando word_count.
        
        Args:
            text_content (str): Texto bruto do elemento
            
        Returns:
            dict or None: Item de conteúdo processado ou None se inválido
        """
        # Limpa e valida texto
        cleaned_text = re.sub(r'\s+', ' ', text_content).strip()
        if not cleaned_text or len(cleaned_text) <= 10:  # Ignora textos muito curtos
            return None
        
        # Conta palavras
        word_count = self.count_words(cleaned_text)
        self.total_words += word_count
        self.total_content_items += 1
        
        return {
            "type": "p",
            "content": cleaned_text,
            "word_count": word_count
        }
    
    def process_epub_to_json(self, epub_path, output_json_path=None):
        """
        Converte arquivo EPUB para JSON estruturado com word_count automático.
        
        Args:
            epub_path (str): Caminho para o arquivo EPUB
            output_json_path (str, optional): Caminho do arquivo JSON de saída
            
        Returns:
            bool: True se sucesso, False se erro
        """
        if not output_json_path:
            output_json_path = 'webapp/public/data/livro_en.json'
        
        print(f"📚 Processando EPUB: {epub_path}")
        print(f"   🎯 Arquivo de saída: {output_json_path}")
        
        # Reset de estatísticas
        self.total_words = 0
        self.total_content_items = 0
        self.total_chapters = 0
        self.total_parts = 0
        
        # Cria diretório temporário
        with tempfile.TemporaryDirectory() as temp_dir:
            try:
                # Extrai EPUB
                extract_dir = self.extract_epub(epub_path, temp_dir)
                print(f"   📂 EPUB extraído para: {extract_dir}")
                
                # Encontra arquivos de conteúdo
                content_files = self.find_content_files(extract_dir)
                print(f"   📄 Arquivos de conteúdo encontrados: {len(content_files)}")
                
                if not content_files:
                    print("   ❌ Nenhum arquivo de conteúdo encontrado!")
                    return False
                
                book_structure = []
                
                # Processa cada arquivo
                for i, file_path in enumerate(content_files):
                    print(f"   📖 Processando: {os.path.basename(file_path)}")
                    
                    try:
                        with open(file_path, 'r', encoding='utf-8') as f:
                            content = f.read()
                        
                        soup = BeautifulSoup(content, 'html.parser')
                        
                        # Determina título da parte
                        part_title = f"Part {i + 1}"
                        
                        # Tenta encontrar título no conteúdo
                        title_elem = soup.find(['h1', 'h2', 'title'])
                        if title_elem:
                            potential_title = title_elem.get_text().strip()
                            if potential_title and len(potential_title) < 200:
                                part_title = potential_title
                        
                        current_part = {
                            "part_title": part_title,
                            "chapters": []
                        }
                        
                        # Processa elementos do arquivo
                        all_elements = soup.find_all(['p', 'div', 'h1', 'h2', 'h3'])
                        current_chapter = None
                        
                        for element in all_elements:
                            text_content = element.get_text().strip()
                            if not text_content:
                                continue
                            
                            # Detecta títulos de capítulo
                            is_chapter_title = (
                                re.match(r'^CHAPTER\s+[IVXLCDM]+', text_content, re.IGNORECASE) or
                                re.match(r'^Chapter\s+\d+', text_content, re.IGNORECASE) or
                                element.name in ['h1', 'h2'] and len(text_content) < 100
                            )
                            
                            if is_chapter_title:
                                current_chapter = {
                                    "chapter_title": text_content,
                                    "content": []
                                }
                                current_part["chapters"].append(current_chapter)
                                self.total_chapters += 1
                                continue
                            
                            # Adiciona conteúdo
                            if element.name == 'p' and text_content:
                                # Se não há capítulo atual, cria um
                                if not current_chapter:
                                    current_chapter = {
                                        "chapter_title": "Content",
                                        "content": []
                                    }
                                    current_part["chapters"].append(current_chapter)
                                    self.total_chapters += 1
                                
                                # Processa item de conteúdo
                                content_item = self.process_content_item(text_content)
                                if content_item:
                                    current_chapter["content"].append(content_item)
                        
                        # Só adiciona a parte se tiver conteúdo
                        if current_part["chapters"]:
                            book_structure.append(current_part)
                            self.total_parts += 1
                            
                    except Exception as e:
                        print(f"   ⚠️ Erro ao processar {file_path}: {e}")
                        continue
                
                # Salva JSON com word_count incluído
                os.makedirs(os.path.dirname(output_json_path), exist_ok=True)
                with open(output_json_path, 'w', encoding='utf-8') as f:
                    json.dump(book_structure, f, indent=2, ensure_ascii=False)
                
                self._print_statistics(output_json_path)
                return True
                
            except Exception as e:
                print(f"   ❌ Erro durante processamento: {e}")
                return False
    
    def _print_statistics(self, output_json_path):
        """Imprime estatísticas do processamento"""
        print(f"\n✅ JSON criado com sucesso!")
        print(f"   📂 Arquivo: {output_json_path}")
        print(f"   📚 Partes processadas: {self.total_parts}")
        print(f"   📖 Total de capítulos: {self.total_chapters}")
        print(f"   📝 Total de itens de conteúdo: {self.total_content_items}")
        print(f"   📊 Total de palavras: {self.total_words:,}")
        print(f"   ✅ Arquivo compatível com todos os scripts (inclui word_count)")
    
    def process_from_file(self, epub_filename=None, output_path=None):
        """
        Processa EPUB encontrando arquivo automaticamente.
        
        Args:
            epub_filename (str, optional): Nome específico do arquivo EPUB
            output_path (str, optional): Caminho do arquivo de saída
            
        Returns:
            bool: True se sucesso, False se erro
        """
        print("📚 CONVERSOR EPUB → JSON (com word_count automático)")
        print("=" * 55)
        
        if epub_filename:
            if not os.path.exists(epub_filename):
                print(f"❌ Arquivo EPUB não encontrado: {epub_filename}")
                return False
            epub_file = epub_filename
        else:
            # Procura arquivo EPUB
            epub_files = []
            for file in os.listdir('.'):
                if file.endswith('.epub'):
                    epub_files.append(file)
            
            if not epub_files:
                print("❌ Nenhum arquivo EPUB encontrado na pasta atual!")
                return False
            
            if len(epub_files) == 1:
                epub_file = epub_files[0]
                print(f"📖 Arquivo EPUB encontrado: {epub_file}")
            else:
                print("📖 Arquivos EPUB encontrados:")
                for i, file in enumerate(epub_files):
                    print(f"   {i+1}. {file}")
                
                try:
                    choice = int(input("\nEscolha o arquivo (número): ")) - 1
                    epub_file = epub_files[choice]
                except (ValueError, IndexError):
                    print("❌ Escolha inválida!")
                    return False
        
        # Processa o arquivo
        success = self.process_epub_to_json(epub_file, output_path)
        
        if success:
            print("\n🎉 Conversão concluída com sucesso!")
            print("   ✅ Arquivo livro_en.json gerado com word_count automático")
            print("   ✅ Compatível com todos os scripts existentes")
        else:
            print("\n❌ Erro na conversão!")
        
        return success


def main():
    """Função principal para uso direto do script"""
    import sys
    
    processor = EpubToJsonProcessor()
    
    # Verifica se foi passado um arquivo EPUB como argumento
    if len(sys.argv) > 1:
        epub_file = sys.argv[1]
        output_path = sys.argv[2] if len(sys.argv) > 2 else None
        
        if not os.path.exists(epub_file):
            print(f"❌ Arquivo EPUB não encontrado: {epub_file}")
            sys.exit(1)
            
        print(f"📚 Processando arquivo especificado: {epub_file}")
        success = processor.process_epub_to_json(epub_file, output_path)
        
        if success:
            print("\n🎉 Conversão concluída com sucesso!")
            print("   ✅ Arquivo livro_en.json gerado com word_count automático")
            print("   ✅ Compatível com todos os scripts existentes")
        else:
            print("\n❌ Erro na conversão!")
            sys.exit(1)
    else:
        # Usa o método original de busca automática
        processor.process_from_file()


if __name__ == "__main__":
    main()
