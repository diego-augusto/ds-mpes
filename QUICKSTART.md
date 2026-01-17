# 🚀 GUIA DE USO RÁPIDO - Streamlit Project

## ✅ Status: Projeto Criado com Sucesso!

Seu projeto Streamlit está 100% configurado e pronto para usar.

---

## 📋 O que foi criado:

✅ **Virtual Environment (venv)** - Isolamento de dependências Python  
✅ **Streamlit** - Framework para apps web interativos  
✅ **Dependências instaladas** - pandas, plotly, numpy, requests, python-dotenv  
✅ **Estrutura do projeto** - Organizada em pastas (src, pages, data, assets)  
✅ **App.py funcional** - Dashboard com KPIs, gráficos e filtros  
✅ **Página adicional** - Exemplo de aplicação multi-página  
✅ **Utilitários reutilizáveis** - Funções prontas em src/utils.py  
✅ **Configurações Streamlit** - Theme customizado em .streamlit/config.toml  
✅ **Git inicializado** - Repositório pronto com primeiro commit  

---

## 🎯 Como Executar:

### Opção 1: Script Rápido (Recomendado - Windows PowerShell)
```powershell
.\start.ps1
```

### Opção 2: Manual
```powershell
# Ativar virtual environment
.\venv\Scripts\Activate.ps1

# Executar aplicação
streamlit run app.py
```

### Resultado:
A aplicação abrirá automaticamente em `http://localhost:8501`

---

## 📁 Estrutura do Projeto:

```
ds-mpes/
├── venv/                      # Virtual environment (não versionado)
├── .streamlit/
│   └── config.toml           # Configuração do Streamlit
├── .gitignore               # Arquivos ignorados no git
├── .env.example             # Exemplo de variáveis de ambiente
├── app.py                   # ⭐ APLICAÇÃO PRINCIPAL (execute isso)
├── requirements.txt         # Dependências do projeto
├── README.md               # Documentação completa
├── start.ps1               # Script para iniciar
├── src/
│   ├── __init__.py
│   └── utils.py            # Funções reutilizáveis
├── pages/
│   └── sobre.py            # Página adicional (multi-página)
├── data/                   # Para seus dados locais
└── assets/                 # Imagens, ícones, etc
```

---

## 💡 Próximos Passos:

1. **Explore o dashboard** - Veja os gráficos e KPIs funcionando
2. **Customize a cor** - Edite `.streamlit/config.toml`
3. **Adicione dados** - Coloque arquivos em `data/`
4. **Crie novas páginas** - Adicione mais arquivos em `pages/`
5. **Use os utilitários** - Importe funções de `src.utils`

---

## 🔧 Comandos Úteis:

```powershell
# Instalar novo pacote
pip install nome-do-pacote

# Gerar novo requirements.txt
pip freeze > requirements.txt

# Ver versão do Streamlit
streamlit --version

# Limpar cache do Streamlit
streamlit cache clear

# Executar em modo dev (com debug)
streamlit run app.py --logger.level=debug
```

---

## 📚 Documentação:

- [Streamlit Docs](https://docs.streamlit.io/)
- [Plotly Charts](https://plotly.com/python/)
- [Pandas Guide](https://pandas.pydata.org/docs/)
- [Python venv](https://docs.python.org/3/library/venv.html)

---

## 🎨 Customizar Tema:

Edite `.streamlit/config.toml` para mudar cores:

```toml
[theme]
primaryColor = "#FF6B6B"           # Cor principal
backgroundColor = "#FFFFFF"        # Fundo
secondaryBackgroundColor = "#F0F2F6" # Fundo secundário
textColor = "#262730"             # Texto
font = "sans serif"               # Fonte
```

---

## ❓ Dúvidas Frequentes:

**P: Como ativar o venv?**  
R: Execute `.\venv\Scripts\Activate.ps1` (Windows PowerShell)

**P: Posso usar em macOS/Linux?**  
R: Sim! Use `source venv/bin/activate` em vez disso

**P: Como adicionar mais dependências?**  
R: `pip install nome-do-pacote` e depois `pip freeze > requirements.txt`

**P: A porta 8501 está em uso?**  
R: Use `streamlit run app.py --server.port=8502`

---

**🎉 Tudo pronto! Execute `.\start.ps1` e aproveite! 🚀**
