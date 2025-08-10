# Scripts de Processamento de EPUB

Esta pasta contém scripts para converter arquivos EPUB para JSON e vice-versa.

## Scripts Disponíveis

### `epub_to_json_processor.py` ⭐ **PRINCIPAL**
Converte arquivo EPUB para formato JSON estruturado com word_count automático.

**Uso:**
```bash
python epub_to_json_processor.py <arquivo_epub>
```

**Entrada:** Arquivo EPUB
**Saída:** JSON estruturado em `output/livro_en.json`

**Características:**
- ✅ Contagem automática de palavras
- ✅ Processamento robusto de XHTML
- ✅ Usado no pipeline principal

### `gerar_epub_atualizado.py` ⭐ **PRINCIPAL**
Gera arquivos EPUB atualizados a partir dos dados JSON.

**Uso:**
```bash
python gerar_epub_atualizado.py
```

**Entrada:** Arquivos JSON em `output/`
**Saída:** Arquivos EPUB em `output/`

**Recursos:**
- Suporte para inglês e português
- Estrutura EPUB padrão
- Navegação NCX inteligente
- Metadados adequados
- **Página de licença CC0 incluída automaticamente**
- **Quebra de linha automática em títulos**
- **Tratamento especial para seções dedicatórias**

## Scripts Auxiliares

### `title_page_en.xhtml` / `title_page_pt-BR.xhtml`
Páginas de título para cada idioma.

### `license.xhtml`
Página de licença Creative Commons.

## Estrutura de Dados

Os scripts trabalham com JSON estruturado em partes e capítulos:

```json
[
  {
    "part_title": "Part I",
    "chapters": [
      {
        "chapter_title": "Chapter 1",
        "content": [
          {
            "type": "p",
            "content": "Texto do parágrafo..."
          }
        ]
      }
    ]
  }
]
```
