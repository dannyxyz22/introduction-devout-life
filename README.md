# Introduction to the Devout Life - Digital Edition

## 📚 Sobre o Projeto

Este projeto é uma edição digital do clássico "Introduction to the Devout Life" (Introdução à Vida Devota) de São Francisco de Sales. O projeto inclui:

- 📖 **Aplicação web** para leitura interativa
- 🔧 **Scripts de processamento** para conversão de EPUB para JSON
- 🌐 **Sistema de tradução** automatizado
- 📱 **Interface responsiva** com React

## 🚀 Recursos

### Aplicação Web
- Interface limpa e responsiva
- Navegação por capítulos e partes
- Suporte a português e inglês
- Design otimizado para leitura

### Pipeline de Processamento
- Extração de conteúdo de arquivos EPUB
- Correção de erros de OCR
- Sistema de tradução via Google Translate
- Geração de EPUBs atualizados

## 📁 Estrutura do Projeto

```
├── webapp/                    # Aplicação React
│   ├── public/
│   │   └── data/             # Dados do livro (JSON)
│   └── src/                  # Código fonte React
├── scripts/                  # Scripts de processamento
│   ├── epub_processing/      # Processamento de EPUB
│   ├── translation/          # Sistema de tradução
│   └── ocr_fixes/           # Correção de OCR
├── data/                    # Dados originais
└── output/                  # Arquivos gerados
```

## 🛠️ Instalação

### Pré-requisitos
- Python 3.8+
- Node.js 14+
- npm ou yarn

### Backend (Scripts Python)
```bash
# Clone o repositório
git clone https://github.com/seu-usuario/introduction-devout-life.git
cd introduction-devout-life

# Crie ambiente virtual
python -m venv .venv
source .venv/bin/activate  # Linux/Mac
.venv\Scripts\activate     # Windows

# Instale dependências
pip install -r requirements.txt
```

### Frontend (Aplicação React)
```bash
cd webapp
npm install
npm start
```

## 📖 Como Usar

### Executar a Aplicação Web
```bash
cd webapp
npm start
```

### Processar um Novo EPUB
```bash
# 1. Processar EPUB original
python scripts/epub_processing/process_epub.py

# 2. Corrigir OCR (se necessário)
python scripts/ocr_fixes/fix_ocr_manual.py

# 3. Gerar DOCX para tradução
python scripts/translation/tradutor_docx_clean.py

# 4. Após traduzir no Google Translate
python scripts/translation/reconstruir_json_portugues.py

# 5. Gerar EPUB atualizado
python scripts/epub_processing/gerar_epub_atualizado.py
```

## 🔧 Scripts Disponíveis

### Processamento de EPUB
- `process_epub.py` - Converte EPUB para JSON estruturado
- `gerar_epub_atualizado.py` - Gera EPUB a partir de JSON

### Correção de OCR
- `fix_ocr_manual.py` - Correções conservativas de OCR
- `fix_ocr_issues.py` - Correções automáticas de OCR

### Sistema de Tradução
- `tradutor_docx_clean.py` - Gera DOCX limpo para tradução
- `reconstruir_json_portugues.py` - Reconstrói JSON a partir da tradução

## 🌐 Tradução

O projeto suporta tradução automatizada via Google Translate:

1. Execute `tradutor_docx_clean.py` para gerar arquivo DOCX limpo
2. Faça upload em [Google Translate](https://translate.google.com)
3. Baixe o arquivo traduzido
4. Execute `reconstruir_json_portugues.py` para reintegrar a tradução

## 📱 Demo Online

Acesse a aplicação em: [Link para GitHub Pages]

## 🤝 Contribuindo

1. Fork o projeto
2. Crie uma branch para sua feature (`git checkout -b feature/AmazingFeature`)
3. Commit suas mudanças (`git commit -m 'Add some AmazingFeature'`)
4. Push para a branch (`git push origin feature/AmazingFeature`)
5. Abra um Pull Request

## 📄 Licença

Este projeto está sob a licença MIT. Veja o arquivo [LICENSE](LICENSE) para detalhes.

## 👨‍💻 Autor

- **Nome** - [GitHub](https://github.com/seu-usuario)

## 🙏 Reconhecimentos

- São Francisco de Sales - Autor original
- Projeto baseado em domínio público
- Interface inspirada em aplicações modernas de leitura

## 📊 Status do Projeto

- ✅ Aplicação web funcional
- ✅ Sistema de tradução automática
- ✅ Geração de EPUB
- ✅ Correção de OCR
- 🔄 Em desenvolvimento: Melhorias na interface
- 📋 Planejado: Mais idiomas de tradução

---

**Nota**: Este é um projeto educacional e de preservação cultural. O texto original está em domínio público.
