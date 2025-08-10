# Scripts de Correção de OCR

Esta pasta contém script para corrigir erros comuns de OCR (Optical Character Recognition).

## Script Principal

### `fix_ocr_manual.py` ⭐ **ÚNICO SCRIPT ATIVO**
Aplica correções conservativas e manuais de OCR.

**Uso:**
```bash
python fix_ocr_manual.py
```

**Características:**
- ✅ Correções específicas e testadas
- ✅ Não quebra palavras válidas
- ✅ Abordagem conservativa
- ✅ Preserva integridade do texto
- ✅ **Usado no pipeline principal**

## Tipos de Erros Corrigidos

### Caracteres Comuns
- `tbe` → `the`
- `tbis` → `this`
- `wbicb` → `which`
- `witb` → `with`

### Pontuação
- Espaços antes de pontuação
- Aspas malformadas
- Hífens incorretos

### Capitalização
- Palavras em maiúsculas desnecessárias
- Início de frases

## Aplicação

O script trabalha com o arquivo JSON principal:
- **Entrada:** `output/livro_en.json`
- **Saída:** Arquivo atualizado com correções
- **Backup:** Criado automaticamente antes das alterações

## Integração

Este script é executado automaticamente no **Pipeline Completo** (main.py opção 9) após a reorganização do JSON.
