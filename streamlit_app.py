import streamlit as st
from PIL import Image
import google.generativeai as genai
import os

# 1. Configuração da Página
st.set_page_config(page_title="PatologiaBR", page_icon="🏗️", layout="wide")

# 2. Puxa a chave de forma segura
api_key = st.secrets.get("GOOGLE_API_KEY") or os.getenv("GOOGLE_API_KEY")

if api_key:
    genai.configure(api_key=api_key)
    model = genai.GenerativeModel('gemini-1.5-flash')
else:
    st.error("ERRO: Chave API não configurada nos Secrets do Streamlit.")
    st.stop()

# 3. Título e Interface
st.title("🏗️ PatologiaBR: Analista Técnico I.A.")
st.write("Análise de patologias da construção baseada em NBRs.")

col1, col2 = st.columns(2)

# Inicializamos as variáveis para evitar erro de "NameError"
img = None

with col1:
    foto = st.file_uploader("Suba a foto da patologia", type=["jpg", "png", "jpeg"])
    if foto:
        img = Image.open(foto)
        st.image(img, caption="Imagem para análise", use_container_width=True)

with col2:
    detalhes = st.text_area("Descreva o contexto (local, idade da obra, etc.):")
    analisar = st.button("Executar Diagnóstico Técnico", type="primary")

# 4. Bloco de Execução (Sempre colado na margem esquerda)
if analisar:
    if img is not None:
        with st.spinner('Analisando conforme normas técnicas brasileiras...'):
            try:
                # Criamos o prompt técnico
                prompt_completo = f"""
                Aja como um perito em engenharia civil especializado em patologias.
                Analise a imagem fornecida e considere este contexto: {detalhes}.
                
                Sua resposta deve ser técnica e organizada:
                1. Identificação da patologia observada.
                2. Prováveis causas técnicas.
                3. Normas NBR aplicáveis (ex: NBR 6118, 15575, 5674).
                4. Sugestões de conduta ou reparo.
                """
                
                # Envia para a I.A.
                response = model.generate_content([prompt_completo, img])
                
                st.markdown("---")
                st.markdown("### 📋 Resultado do Diagnóstico")
                st.write(response.text)
                
            except Exception as e:
                st.error(f"Erro ao processar análise: {e}")
    else:
        st.warning("⚠️ Por favor, suba uma foto antes de clicar em analisar.")
