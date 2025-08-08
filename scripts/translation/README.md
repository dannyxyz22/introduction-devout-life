# Scripts de Tradução

Esta pasta contém scripts para traduzir o livro via Google Translate.

## Scripts Disponíveis

### `tradutor_docx_clean.py`
Gera arquivo DOCX limpo para tradução no Google Translate.

**Uso:**
```bash
python tradutor_docx_clean.py
```

**Entrada:** JSON em inglês (`output/livro_en.json`)
**Saída:** `output/livro_en_CLEAN_for_translation.docx`

**Características:**
- Remove metadados que contaminam a tradução
- Preserva marcadores de ID para reconstrução
- Formato otimizado para Google Translate

### `reconstruir_json_portugues.py`
Reconstrói JSON em português a partir do arquivo traduzido.

**Uso:**
```bash
python reconstruir_json_portugues.py
```

**Entrada:** Arquivo DOCX traduzido do Google Translate
**Saída:** JSON em português (`webapp/public/data/livro_pt-BR.json`)

**Processo:**
- Detecta automaticamente arquivo traduzido
- Preserva estrutura original
- Cria backup antes de sobrescrever

## Fluxo de Tradução

1. **Gerar DOCX limpo:**
   ```bash
   python tradutor_docx_clean.py
   ```

2. **Traduzir no Google Translate:**
   - Acesse [Google Translate](https://translate.google.com)
   - Faça upload do arquivo `output/livro_en_CLEAN_for_translation.docx`
   - Traduza de Inglês para Português
   - Baixe o arquivo traduzido na pasta `output/`

3. **Reconstruir JSON:**
   ```bash
   python reconstruir_json_portugues.py
   ```

## Marcadores de ID

Os scripts usam marcadores especiais para preservar a estrutura:

```
###ID0001### Primeiro parágrafo...
###ID0002### Segundo parágrafo...
```

**Importante:** Não remova estes marcadores durante a tradução!
