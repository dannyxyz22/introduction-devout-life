# Guia de Configuração do Git

Este guia ajuda você a configurar o repositório Git e fazer upload para o GitHub.

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
git commit -m "Initial commit: Introduction to the Devout Life digital edition"
```

### 2. Criar Repositório no GitHub
1. Acesse [GitHub.com](https://github.com)
2. Clique em "New repository"
3. Nome sugerido: `introduction-devout-life`
4. Descrição: "Digital edition of Introduction to the Devout Life by St. Francis de Sales"
5. Deixe como **Public** (texto está em domínio público)
6. **NÃO** marque "Add a README file" (já temos um)
7. Clique em "Create repository"

### 3. Conectar Repositório Local ao GitHub
```bash
# Adicionar origem remota (substitua SEU-USUARIO pelo seu username)
git remote add origin https://github.com/SEU-USUARIO/introduction-devout-life.git

# Renomear branch principal para main
git branch -M main

# Fazer push inicial
git push -u origin main
```

### 4. Configurar GitHub Pages (Opcional)
Para disponibilizar a aplicação web online:

1. No GitHub, vá em "Settings" do repositório
2. Role até "Pages"
3. Em "Source", selecione "Deploy from a branch"
4. Escolha "main" e "/webapp" (se disponível) ou configure GitHub Actions
5. A aplicação ficará disponível em: `https://SEU-USUARIO.github.io/introduction-devout-life`

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
- Arquivos temporários
- Ambiente virtual Python
- Arquivos de cache
- Pasta `archive/` com arquivos de desenvolvimento

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
├── README.md                 # Documentação principal
├── LICENSE                   # Licença MIT
├── requirements.txt          # Dependências Python
├── .gitignore               # Arquivos ignorados
├── main.py                  # Script principal
├── scripts/                 # Scripts de processamento
│   ├── epub_processing/     # Conversão EPUB ↔ JSON
│   ├── translation/         # Sistema de tradução
│   └── ocr_fixes/          # Correção de OCR
├── webapp/                  # Aplicação React
│   ├── public/             # Arquivos públicos
│   │   └── data/           # Dados JSON do livro
│   └── src/                # Código fonte React
├── data/                   # Dados originais
├── output/                 # Arquivos gerados
└── archive/               # Scripts de desenvolvimento (ignorado)
```

## 🎯 Próximos Passos

Após subir no GitHub:

1. **Atualizar README.md** com link do repositório
2. **Configurar CI/CD** para deploy automático
3. **Adicionar issues** para funcionalidades futuras
4. **Criar releases** para versões estáveis
5. **Documentar contribuições** para colaboradores

---

**Dica**: Use mensagens de commit descritivas:
- ✅ "Fix OCR correction for 'Description' word breaking"
- ✅ "Add Portuguese translation workflow"
- ❌ "Update"
- ❌ "Fix bug"
