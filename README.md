# 📊 Projeto Streamlit

Aplicação interativa desenvolvida com Streamlit, pandas e plotly para análise de dados e visualização em tempo real.

## 🚀 Início Rápido

### Pré-requisitos
- Python 3.8 ou superior
- pip (gerenciador de pacotes Python)

### Instalação

1. **Clone ou navegue até o diretório do projeto:**
   ```bash
   git clone git@github.com:diego-augusto/ds-mpes.git
   ```

2. **Crie um ambiente virtual:**
   ```bash
   python -m venv venv
   ```

3. **Ative o ambiente virtual:**
   - **Windows (PowerShell):**
     ```powershell
     .\venv\Scripts\Activate.ps1
     ```
   - **Windows (CMD):**
     ```cmd
     venv\Scripts\activate.bat
     ```
   - **macOS/Linux:**
     ```bash
     source venv/bin/activate
     ```

4. **Instale as dependências:**
   ```bash
   pip install -r requirements.txt
   ```

### Executar a Aplicação

```bash
streamlit run app.py
```

A aplicação será aberta automaticamente em `http://localhost:8501`

## 📁 Estrutura do Projeto

```
ds-mpes/
├── venv/                    # Virtual environment (não versionado)
├── src/                     # Módulos e funções reutilizáveis
├── pages/                   # Páginas adicionais (Streamlit multi-página)
├── data/                    # Dados locais
├── assets/                  # Imagens, ícones, etc
├── .streamlit/
│   └── config.toml         # Configuração do Streamlit
├── .gitignore              # Arquivos a ignorar no git
├── requirements.txt        # Dependências do projeto
├── README.md              # Este arquivo
└── app.py                 # Aplicação principal
```

## 📦 Dependências

- **streamlit** - Framework para criar aplicações web interativas
- **pandas** - Manipulação e análise de dados
- **numpy** - Computações numéricas
- **plotly** - Visualizações interativas
- **requests** - Requisições HTTP
- **python-dotenv** - Gerenciar variáveis de ambiente

## 💡 Funcionalidades

- ✅ Dashboard interativo com KPIs
- ✅ Gráficos dinâmicos com Plotly
- ✅ Filtros por data
- ✅ Visualização de dados em tabelas
- ✅ Export de dados em CSV
- ✅ Estatísticas descritivas

## 🔧 Customização

### Adicionar nova página (multi-página)

1. Crie um arquivo em `pages/` (ex: `pages/analise.py`)
2. Streamlit detectará automaticamente como nova página

### Usar variáveis de ambiente

1. Crie um arquivo `.env` na raiz do projeto:
   ```
   API_KEY=sua_chave_aqui
   ```

2. No seu código Python:
   ```python
   from dotenv import load_dotenv
   import os
   
   load_dotenv()
   api_key = os.getenv('API_KEY')
   ```

## 📚 Recursos Úteis

- [Documentação Streamlit](https://docs.streamlit.io/)
- [Galeria de exemplos](https://streamlit.io/gallery)
- [Comunidade](https://discuss.streamlit.io/)

## 📝 Licença

Este projeto é de código aberto e disponível sob a licença MIT.

---

**Desenvolvido com ❤️ usando Streamlit**
