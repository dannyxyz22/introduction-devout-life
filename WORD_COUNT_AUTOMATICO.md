# Processador EPUB com Word Count Automático

Este documento explica como usar o novo sistema de processamento EPUB que sempre inclui contagem de palavras automática.

## 🎯 O que mudou

### Antes
1. Gerava `livro_extracted.json` sem `word_count`
2. Precisava executar script separado para adicionar `word_count`
3. Mais passos no pipeline

### Agora
1. **Gera diretamente `livro_en.json` com `word_count` incluído**
2. **Um só passo** - compatibilidade automática
3. **Pipeline simplificado**

## 📂 Arquivos Principais

### Novo Processador Principal
- **`scripts/epub_processing/epub_to_json_processor.py`** - Classe principal com word_count automático
- **`gerar_livro_en_com_word_count.py`** - Script wrapper fácil de usar

### Scripts Atualizados
- **`scripts/epub_processing/process_epub.py`** - Atualizado com word_count automático
- **`scripts/epub_processing/process_epub_from_file.py`** - Atualizado com word_count automático
- **`main.py`** - Menu principal atualizado

## 🚀 Como Usar

### Opção 1: Script Wrapper (Mais Fácil)
```bash
python gerar_livro_en_com_word_count.py
```

### Opção 2: Menu Principal
```bash
python main.py
# Escolha opção 1: "Processar EPUB → JSON (com word_count automático)"
```

### Opção 3: Classe Direta (Para Desenvolvedores)
```python
from scripts.epub_processing.epub_to_json_processor import EpubToJsonProcessor

processor = EpubToJsonProcessor()
success = processor.process_from_file("meu_arquivo.epub", "saida.json")
```

## 🔧 Funcionalidades

### Contagem de Palavras Automática
- **Função**: `count_words(text)` - Conta palavras removendo espaços extras
- **Aplicação**: Automática em cada item de conteúdo
- **Resultado**: Campo `word_count` em todos os itens

### Estatísticas Detalhadas
```
✅ JSON criado com sucesso!
   📂 Arquivo: webapp/public/data/livro_en.json
   📚 Partes processadas: 8
   📖 Total de capítulos: 287
   📝 Total de itens de conteúdo: 929
   📊 Total de palavras: 89,848
   ✅ Arquivo compatível com todos os scripts (inclui word_count)
```

### Compatibilidade Total
- ✅ Scripts de tradução (`tradutor_docx_clean.py`)
- ✅ Geração de EPUB (`gerar_epub_atualizado.py`) 
- ✅ Reconstrução JSON português (`reconstruir_json_portugues.py`)
- ✅ Todos os scripts OCR

## 📊 Estrutura do JSON Gerado

```json
{
  "type": "p",
  "content": "Texto do parágrafo aqui...",
  "word_count": 42
}
```

## 🔄 Pipeline Atualizado

### Novo Fluxo (Simplificado)
1. **EPUB** → `livro_en.json` (com word_count) ← **UM SÓ PASSO**
2. `livro_en.json` → DOCX para tradução
3. DOCX traduzido → `livro_pt-BR.json`
4. JSONs → EPUBs finais

### Fluxo Antigo (Descontinuado)
1. EPUB → `livro_extracted.json` (sem word_count)
2. `livro_extracted.json` → `livro_en.json` (adicionar word_count)
3. `livro_en.json` → resto do pipeline

## 🎯 Benefícios

### Para Usuários
- **Menos passos** - Pipeline mais simples
- **Automático** - Não precisa lembrar de adicionar word_count
- **Confiável** - Sempre compatível com todos os scripts

### Para Desenvolvedores
- **Classe reutilizável** - `EpubToJsonProcessor`
- **Código limpo** - Lógica centralizada
- **Extensível** - Fácil de adicionar novas funcionalidades

## 🔍 Detalhes Técnicos

### Algoritmo de Contagem
```python
def count_words(self, text):
    if not text or not isinstance(text, str):
        return 0
    
    # Remove espaços extras e quebras de linha
    cleaned_text = ' '.join(text.strip().split())
    
    # Conta palavras (divide por espaços)
    if cleaned_text:
        return len(cleaned_text.split())
    return 0
```

### Processamento de Conteúdo
```python
def process_content_item(self, text_content):
    # Limpa texto
    cleaned_text = re.sub(r'\s+', ' ', text_content).strip()
    if not cleaned_text or len(cleaned_text) <= 10:
        return None
    
    # Conta palavras automaticamente
    word_count = self.count_words(cleaned_text)
    
    return {
        "type": "p",
        "content": cleaned_text,
        "word_count": word_count  # ← SEMPRE INCLUÍDO
    }
```

## 📝 Migração

### Se você estava usando o fluxo antigo:
1. **Delete** `livro_extracted.json` (não é mais necessário)
2. **Use** `gerar_livro_en_com_word_count.py` em vez de múltiplos scripts
3. **Continue** usando todos os outros scripts normalmente

### Para novos projetos:
- **Use sempre** o novo processador
- **Ignore** scripts antigos de word_count
- **Aproveite** o pipeline simplificado

## 🆘 Troubleshooting

### Erro: "ImportError: bs4"
```bash
pip install beautifulsoup4
```

### Erro: "EPUB não encontrado"
- Certifique-se que há arquivo `.epub` na pasta
- Ou especifique o caminho completo

### Erro: "word_count não encontrado"
- Use o novo processador em vez do antigo
- Verifique se está usando `epub_to_json_processor.py`

### JSON sem word_count
- **Problema**: Usando script antigo
- **Solução**: Use `gerar_livro_en_com_word_count.py`
