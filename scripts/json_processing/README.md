# Scripts de Processamento de JSON

Esta pasta contém scripts para processar e corrigir arquivos JSON gerados a partir do EPUB.

## Scripts Principais

### `reorganize_final.py` ⭐ **PRINCIPAL**
Reorganiza o JSON baseado no arquivo summary.csv para estrutura correta.

**Uso:**
```bash
python reorganize_final.py
```

**Entrada:** 
- `output/livro_en.json` (JSON inicial)
- `summary.csv` (estrutura de referência)

**Saída:** JSON reorganizado com estrutura correta

**Características:**
- ✅ Extrai seções especiais (DEDICATORY PRAYER, PREFACE)
- ✅ Organiza capítulos por partes
- ✅ Preserva integridade do conteúdo
- ✅ **Usado no pipeline principal**

### `fix_ad_hoc.py` ⭐ **PRINCIPAL**
Aplica correções específicas pontuais no JSON inglês.

**Uso:**
```bash
python fix_ad_hoc.py
```

**Entrada:** `output/livro_en.json`
**Saída:** JSON com correções aplicadas

**Correções Aplicadas:**
- Títulos incompletos
- Problemas de formatação
- Palavras concatenadas
- Duplicações indesejadas

**Características:**
- ✅ Correções conservativas e testadas
- ✅ Recalculo automático de word_count
- ✅ Backup automático antes das alterações
- ✅ **Usado no pipeline principal**

### `split_part_titles.py` ⭐ **PRINCIPAL**
Divide títulos de partes em título e subtítulo.

**Uso:**
```bash
python split_part_titles.py
```

**Entrada:** `output/livro_en.json`
**Saída:** JSON com títulos de partes divididos

**Funcionalidade:**
- Separa títulos longos em `part_title` e `part_subtitle`
- Melhora a apresentação visual
- Preserva conteúdo original

**Características:**
- ✅ **Usado no pipeline principal**

## Integração com Pipeline

Todos estes scripts são executados automaticamente no **Pipeline Completo** (main.py opção 9) na seguinte ordem:

1. Processamento inicial do EPUB
2. **fix_ad_hoc.py** - Correções pontuais
3. **reorganize_final.py** - Reorganização estrutural
4. Correção de OCR
5. **split_part_titles.py** - Divisão de títulos

## Estrutura de Dados

Os scripts trabalham com JSON estruturado em partes e capítulos:

```json
[
  {
    "part_title": "PART I",
    "part_subtitle": "Containing counsels and exercises...",
    "chapters": [
      {
        "chapter_title": "CHAPTER I. Of the nature and excellence of devotion",
        "content": [
          {
            "type": "p",
            "content": "Texto do parágrafo...",
            "word_count": 42
          }
        ]
      }
    ]
  }
]
```
