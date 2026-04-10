
import streamlit as st
from PIL import Image
import google.generativeai as genai
import os

# Configuração da página
st.set_page_config(page_title="PatologiaBR", page_icon="🏗️", layout="wide")

# Puxa a chave de forma segura dos Secrets do Streamlit
if "GOOGLE_API_KEY" in st.secrets:
    api_key = st.secrets["GOOGLE_API_KEY"]
else:
    api_key = os.getenv("GOOGLE_API_KEY")

if api_key:
    genai.configure(api_key=api_key)
    model = genai.GenerativeModel('gemini-1.5-flash')
else:
    st.error("Chave API não configurada nos Secrets.")

# Título e Interface
st.title("🏗️ PatologiaBR: Analista Técnico I.A.")
st.write("Análise de patologias da construção baseada em NBRs.")

col1, col2 = st.columns(2)
col1, col2 = st.columns(2)

# Deixamos a variável img pronta aqui fora
img = None 

with col1:
    foto = st.file_uploader("Suba a foto da patologia", type=["jpg", "png", "jpeg"])
    if foto:
        img = Image.open(foto) 
        st.image(img, caption="Imagem para análise", use_container_width=True)

with col2:
    detalhes = st.text_area("Descreva o contexto (local, idade da obra, etc.):")
    analisar = st.button("Executar Diagnóstico Técnico", type="primary")

# Só roda a análise se o botão for clicado e houver imagem
if analisar:
    if img is not None:
        with st.spinner('Analisando conforme normas técnicas...'):
            prompt_completo = f"""
            Aja como um perito em engenharia civil.
            Analise a imagem e o seguinte contexto: {detalhes}
            Identifique a patologia, cite as NBRs brasileiras relevantes 
            e sugira ações de correção.
            """
            
            response = model.generate_content([prompt_completo, img])
            
            st.markdown("---")
            st.markdown("### 📋 Resultado da Análise")
            st.write(response.text)
    else:
        st.error("⚠️ Por favor, faça o upload de uma foto antes de clicar em analisar.")
