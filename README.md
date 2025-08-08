# Introduction to the Devout Life - Digital Edition

## 📚 Sobre o Projeto

Este projeto é uma edição digital completa do clássico "Introduction to the Devout Life" (Introdução à Vida Devota) de São Francisco de Sales, originalmente publicado em 1609. O projeto inclui:

- 📖 **Aplicação web React** para leitura interativa bilíngue
- 🔧 **Pipeline completo** de processamento EPUB → JSON → EPUB
- 🌐 **Sistema de tradução** automático via Google Translate
- 📱 **Interface responsiva** otimizada para dispositivos móveis
- 📊 **Ferramentas de análise** de conteúdo e comparação
- 📚 **EPUBs gerados** com estrutura completa e licença CC0

## 🚀 Recursos

### 📱 Aplicação Web
- Interface limpa e responsiva com React
- Navegação por capítulos e partes (118 capítulos + conteúdo introdutório)
- Suporte bilíngue completo (português e inglês)
- Design otimizado para leitura em todos os dispositivos
- Dados JSON estruturados com metadados completos

### 🔧 Pipeline de Processamento Completo
- Extração inteligente de conteúdo de arquivos EPUB
- Correção conservativa de erros de OCR
- Sistema de tradução via Google Translate com workflow DOCX
- Geração de EPUBs atualizados com estrutura completa
- **Menu interativo central** com 12 funcionalidades integradas
- **Análise de conteúdo** e comparação entre versões

### 📊 Ferramentas de Análise
- Comparação de contagem de caracteres entre EPUBs
- Análise detalhada de conteúdo adicionado nas versões
- Relatórios automáticos de status do projeto
- Verificação de integridade de arquivos

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

### 🎯 Script Principal (Recomendado)
```bash
# Execute o menu interativo central
python main.py
```

**Menu disponível:**
1. 📖 Processar EPUB → JSON (com word_count automático)
2. 🔄 Reorganizar JSON baseado no summary.csv
3. 🔧 Corrigir OCR no JSON inglês
4. 📄 Gerar DOCX para tradução
5. 🌐 Reconstruir JSON português (após tradução)
6. 📚 Gerar EPUBs atualizados
7. 🔄 Pipeline completo (EPUB → Reorganizar → OCR → DOCX → EPUBs)
8. ℹ️ Mostrar status do projeto
9. 🚀 Iniciar aplicação web
10. 📊 Comparar contagem de caracteres dos EPUBs
11. 🔍 Analisar conteúdo adicionado nas versões geradas
12. ❌ Sair

### 🌐 Executar a Aplicação Web
```bash
cd webapp
npm install
npm start
```

### 📚 Processar um Novo EPUB (Pipeline Manual)
```bash
# 1. Processar EPUB original
python scripts/epub_processing/epub_to_json_processor.py data/arquivo.epub

# 2. Reorganizar baseado no summary.csv
python reorganize_final.py

# 3. Corrigir OCR (se necessário)
python scripts/ocr_fixes/fix_ocr_manual.py

# 4. Gerar DOCX para tradução
python scripts/translation/tradutor_docx_clean.py

# 5. Após traduzir no Google Translate
python scripts/translation/reconstruir_json_portugues.py

# 6. Gerar EPUBs atualizados
python scripts/epub_processing/gerar_epub_atualizado.py --auto
```

## 🔧 Scripts Disponíveis

### 🎯 Script Principal
- `main.py` - **Menu interativo central** com todas as funcionalidades integradas

### 📚 Processamento de EPUB
- `epub_to_json_processor.py` - Converte EPUB para JSON estruturado (com word_count automático)
- `process_epub.py` - Processador EPUB alternativo (versão antiga)
- `gerar_epub_atualizado.py` - Gera EPUB a partir de JSON com estrutura completa

### 🔍 Correção de OCR
- `fix_ocr_manual.py` - Correções conservativas de OCR
- `fix_ocr_professional.py` - Correções avançadas com bibliotecas especializadas

### 🌐 Sistema de Tradução
- `tradutor_docx_clean.py` - Gera DOCX limpo para tradução (sem metadados)
- `reconstruir_json_portugues.py` - Reconstrói JSON a partir da tradução
- `reorganize_final.py` - Reorganiza JSON baseado no summary.csv

### 📊 Análise e Comparação
- `compare_epub_text.py` - Compara contagem de caracteres entre EPUBs
- `analyze_added_content.py` - Analisa conteúdo adicionado nas versões geradas

## 🌐 Tradução

O projeto suporta tradução automatizada via Google Translate com workflow otimizado:

1. Execute `python main.py` → opção 4 para gerar arquivo DOCX limpo (sem metadados)
2. Faça upload em [Google Translate](https://translate.google.com) para tradução automática
3. Baixe o arquivo traduzido como `livro_traducao_google.docx`
4. Execute `python main.py` → opção 5 para reintegrar a tradução ao JSON
5. Execute `python main.py` → opção 6 para gerar EPUBs com ambas as versões

**Ou use o pipeline completo:** `python main.py` → opção 7

## 📱 Demo Online

Acesse a aplicação em: [GitHub Pages](https://dannyxyz22.github.io/introduction-devout-life)

## 📊 Status do Projeto

- ✅ **Pipeline 100% funcional** com menu interativo central
- ✅ **Aplicação web bilíngue** com interface otimizada
- ✅ **Sistema de tradução completo** via Google Translate
- ✅ **Geração de EPUB** com estrutura completa (122 capítulos)
- ✅ **Correção de OCR** conservativa e profissional
- ✅ **Ferramentas de análise** e comparação de conteúdo
- ✅ **Documentação completa** e organizada
- ✅ **Estrutura de arquivos** totalmente organizada
- ✅ **Licença Creative Commons CC0** integrada

### � Métricas do Projeto
| Item | Quantidade | Tamanho |
|------|------------|---------|
| **Scripts Python** | 12 principais | ~80KB código |
| **Capítulos processados** | 118 + introdução | Ambos idiomas |
| **JSON dados** | 2 arquivos | ~1.2MB total |
| **EPUBs gerados** | 2 arquivos | ~0.6MB total |
| **Componentes React** | Interface completa | ~150KB |
| **Funcionalidades integradas** | 12 no menu principal | 100% funcionais |

## 🤝 Contribuindo

1. Fork o projeto
2. Crie uma branch para sua feature (`git checkout -b feature/AmazingFeature`)
3. Commit suas mudanças (`git commit -m 'Add some AmazingFeature'`)
4. Push para a branch (`git push origin feature/AmazingFeature`)
5. Abra um Pull Request

## 📄 Licença

Este projeto está sob a licença MIT. Veja o arquivo [LICENSE](LICENSE) para detalhes.
O conteúdo do livro está em domínio público e foi dedicado também ao domínio público via Creative Commons CC0.

## 👨‍💻 Autor

- **Daniel Lélis Baggio** - [GitHub](https://github.com/dannyxyz22)

## 🙏 Reconhecimentos

- **São Francisco de Sales** - Autor original (1567-1622)
- **Texto base**: Edição inglesa de 1885, digitalizada pelo Google Books
- **Nihil Obstat**: P. MacCabe, Arcebispo de Dublin (aprovação histórica)
- **Tecnologias**: React, Python, Google Translate
- **Inspiração**: Aplicações modernas de leitura digital

---

**Nota**: Este é um projeto educacional e de preservação cultural. O texto original de 1609 está em domínio público e esta edição digital foi dedicada ao domínio público via licença CC0.
