# Guia de Configuração do Git

Este guia ajuda você a configurar o repositório Git e fazer upload para o GitHub do projeto **Introduction to the Devout Life - Digital Edition**.

## 🚀 Passos para Subir no GitHub

### 1. Inicializar Repositório Git
```bash
# Navegar para a pasta do projeto
cd "Introduction_to_the_Devout_Life - sem colunas"

# Inicializar repositório Git
git init

# Adicionar todos os arquivos
git add .

# Fazer primeiro commit
git commit -m "Initial commit: Introduction to the Devout Life digital edition complete project"
```

### 2. Criar Repositório no GitHub
1. Acesse [GitHub.com](https://github.com)
2. Clique em "New repository"
3. Nome sugerido: `introduction-devout-life`
4. Descrição: "Complete digital edition of Introduction to the Devout Life by St. Francis de Sales (1609) with bilingual support and full processing pipeline"
5. Deixe como **Public** (texto está em domínio público e projeto usa licença CC0)
6. **NÃO** marque "Add a README file" (já temos um completo)
7. Clique em "Create repository"

### 3. Conectar Repositório Local ao GitHub
```bash
# Adicionar origem remota (substitua dannyxyz22 pelo seu username se diferente)
git remote add origin https://github.com/dannyxyz22/introduction-devout-life.git

# Renomear branch principal para main
git branch -M main

# Fazer push inicial
git push -u origin main
```

### 4. Configurar GitHub Pages
Para disponibilizar a aplicação web online automaticamente:

1. No GitHub, vá em "Settings" do repositório
2. Role até "Pages"
3. Em "Source", selecione "Deploy from a branch"
4. Escolha "main" e "/webapp" ou configure GitHub Actions para build automático
5. A aplicação ficará disponível em: `https://dannyxyz22.github.io/introduction-devout-life`

**Alternativa com GitHub Actions:** Configure build automático do React para deployment otimizado.

## 📝 Comandos Git Úteis

### Adicionar Mudanças
```bash
# Ver status
git status

# Adicionar arquivos específicos
git add arquivo.py

# Adicionar todos os arquivos modificados
git add .

# Fazer commit
git commit -m "Descrição das mudanças"

# Enviar para GitHub
git push
```

### Ignorar Arquivos
O arquivo `.gitignore` já está configurado para ignorar:
- Arquivos temporários Python (`__pycache__/`, `*.pyc`)
- Ambiente virtual Python (`.venv/`, `venv/`)
- Arquivos de cache e logs
- Pasta `archive/` com arquivos de desenvolvimento
- Arquivos temporários do sistema (`*.tmp`, `.DS_Store`)
- Dados grandes temporários

### Branches (Opcional)
```bash
# Criar nova branch para desenvolvimento
git checkout -b nova-funcionalidade

# Voltar para main
git checkout main

# Fazer merge
git merge nova-funcionalidade
```

## 🏷️ Tags de Versão
```bash
# Criar tag de versão
git tag -a v1.0 -m "Primeira versão estável"

# Enviar tag para GitHub
git push origin v1.0
```

## 📊 Estrutura Final do Repositório

```
introduction-devout-life/
├── README.md                 # Documentação principal atualizada
├── PROJECT_STATUS.md         # Status completo do projeto  
├── SETUP_GIT.md             # Este guia de configuração
├── LICENSE                   # Licença MIT
├── requirements.txt          # Dependências Python
├── .gitignore               # Arquivos ignorados
├── main.py                  # Script principal com menu interativo (12 opções)
├── compare_epub_text.py     # Análise de caracteres dos EPUBs
├── analyze_added_content.py # Análise de conteúdo adicionado
├── scripts/                 # Scripts organizados por categoria
│   ├── epub_processing/     # Conversão EPUB ↔ JSON
│   │   ├── epub_to_json_processor.py  # Processador principal
│   │   ├── process_epub.py            # Processador alternativo
│   │   └── gerar_epub_atualizado.py   # Gerador de EPUB
│   ├── json_processing/     # Processamento e reorganização JSON
│   │   └── reorganize_final.py        # Reorganização baseada em summary.csv
│   ├── translation/         # Sistema de tradução
│   │   ├── tradutor_docx_clean.py     # Gerador DOCX
│   │   └── reconstruir_json_portugues.py  # Reconstrutor JSON
│   └── ocr_fixes/          # Correção de OCR
│       ├── fix_ocr_manual.py          # Correções conservativas
│       └── fix_ocr_professional.py    # Correções avançadas
├── webapp/                  # Aplicação React completa
│   ├── public/             # Arquivos públicos
│   │   ├── data/           # JSON dos livros (ambos idiomas)
│   │   └── images/         # Imagens do livro
│   ├── src/                # Código fonte React
│   └── package.json        # Dependências Node.js
├── data/                   # Dados originais
│   └── Introduction_to_the_Devout_Life.epub
├── output/                 # Arquivos gerados
│   ├── livro_en.json       # JSON inglês processado
│   ├── livro_pt-BR.json    # JSON português traduzido
│   ├── *.epub              # EPUBs gerados
│   └── *.docx              # Arquivos para tradução
└── summary.csv             # Arquivo de reorganização
```

## 🎯 Próximos Passos

Após subir no GitHub:

1. **✅ README.md atualizado** com documentação completa
2. **🔧 Configurar CI/CD** para deploy automático da aplicação React
3. **📋 Adicionar issues** para funcionalidades futuras (mais idiomas, melhorias de UI)
4. **🏷️ Criar releases** para versões estáveis (v1.0 já pronto)
5. **👥 Documentar contribuições** para colaboradores
6. **🌐 Configurar domínio personalizado** (opcional)
7. **📊 Adicionar badges** de status no README

## 🏆 Conquistas do Projeto

- ✅ **Pipeline 100% funcional** com menu interativo
- ✅ **Documentação profissional** completa
- ✅ **Estrutura organizada** e modular  
- ✅ **Pronto para colaboração** open source
- ✅ **Licença adequada** (MIT + CC0 para conteúdo)

---

**Dica**: Use mensagens de commit descritivas e organizadas:
- ✅ `feat: Add Portuguese translation pipeline with DOCX workflow`
- ✅ `fix: Correct EPUB generation paths to use output directory`
- ✅ `docs: Update README with complete project documentation`
- ✅ `refactor: Integrate analysis tools into main.py menu`
- ✅ `style: Improve React UI responsiveness and typography`
- ❌ `Update`
- ❌ `Fix bug`
- ❌ `Changes`

**Categorias de commit recomendadas:**
- `feat:` - Nova funcionalidade
- `fix:` - Correção de bug
- `docs:` - Documentação
- `style:` - Formatação, UI/UX
- `refactor:` - Refatoração de código
- `test:` - Testes
- `chore:` - Tarefas de manutenção
