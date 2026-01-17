import streamlit as st
import pandas as pd

st.set_page_config(
    page_title="Sobre",
    page_icon="ℹ️"
)

# Esconder navegação padrão do Streamlit
st.markdown("""
<style>
    [data-testid="stSidebarNav"] {
        display: none;
    }
</style>
""", unsafe_allow_html=True)

# Barra lateral customizada
with st.sidebar:
    st.title("📚 Navegação")
    st.page_link("app.py", label="Resumo", icon="📊")
    st.page_link("pages/sessao_01_contexto.py", label="Contexto", icon="🌲")
    st.page_link("pages/sessao_02_perguntas.py", label="Perguntas", icon="❓")
    st.page_link("pages/sobre.py", label="Sobre", icon="ℹ️")

st.title("ℹ️ Sobre Esta Aplicação")

st.markdown("""
## 📊 Dashboard Streamlit

Uma aplicação interativa desenvolvida com **Streamlit** para análise e visualização de dados em tempo real.

### 🛠️ Tecnologias Utilizadas

- **Streamlit** - Framework para criar apps web
- **Pandas** - Manipulação de dados
- **Plotly** - Visualizações interativas
- **NumPy** - Computações numéricas

### 📚 Como Usar

1. **Ativar o ambiente virtual:**
   ```bash
   .\\venv\\Scripts\\Activate.ps1
   ```

2. **Executar a aplicação:**
   ```bash
   streamlit run app.py
   ```

3. **Acessar no navegador:**
   ```
   http://localhost:8501
   ```

### 📖 Estrutura do Projeto

```
├── app.py                 # Aplicação principal
├── pages/
│   └── sobre.py          # Esta página
├── src/                  # Módulos reutilizáveis
├── data/                 # Dados locais
├── assets/               # Imagens e recursos
├── requirements.txt      # Dependências
└── README.md            # Documentação
```

### 🔗 Links Úteis

- [Documentação Streamlit](https://docs.streamlit.io/)
- [GitHub](https://github.com)
- [Comunidade Streamlit](https://discuss.streamlit.io/)

---

**Desenvolvido com ❤️ usando Streamlit**
""")
