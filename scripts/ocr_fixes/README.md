# Scripts de Correção de OCR

Esta pasta contém scripts para corrigir erros comuns de OCR (Optical Character Recognition).

## Scripts Disponíveis

### `fix_ocr_manual.py` (Recomendado)
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

### `fix_ocr_issues.py`
Correções automáticas mais agressivas.

**Uso:**
```bash
python fix_ocr_issues.py
```

**Características:**
- ⚠️ Pode quebrar palavras válidas
- ⚠️ Use com cuidado
- 🔧 Para casos específicos

### `fix_ocr_conservative.py`
Versão conservativa com menos correções.

### `fix_ocr_professional.py`
Versão com correções mais avançadas.

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

## Recomendação

Use sempre `fix_ocr_manual.py` primeiro, pois é o mais seguro. Os outros scripts devem ser usados apenas se necessário e com revisão manual posterior.

## Aplicação

Os scripts trabalham com o arquivo JSON principal:
- **Entrada:** `webapp/public/data/livro_en.json`
- **Saída:** Arquivo atualizado com correções
- **Backup:** Criado automaticamente
