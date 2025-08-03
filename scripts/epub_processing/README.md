# Scripts de Processamento de EPUB

Esta pasta contém scripts para converter arquivos EPUB para JSON e vice-versa.

## Scripts Disponíveis

### `process_epub.py`
Converte arquivo EPUB para formato JSON estruturado.

**Uso:**
```bash
python process_epub.py
```

**Entrada:** Arquivo EPUB na pasta principal
**Saída:** JSON estruturado em `webapp/public/data/`

### `gerar_epub_atualizado.py`
Gera arquivos EPUB atualizados a partir dos dados JSON.

**Uso:**
```bash
python gerar_epub_atualizado.py
```

**Entrada:** Arquivos JSON em `webapp/public/data/`
**Saída:** Arquivos EPUB em `../../output/`

**Recursos:**
- Suporte para inglês e português
- Estrutura EPUB padrão
- Navegação NCX
- Metadados adequados

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
