import streamlit as st
from PIL import Image
import google.generativeai as genai
import os

# 1. Configuração da Página
st.set_page_config(page_title="PatologiaBR", page_icon="🏗️", layout="wide")

# 2. Configuração da API
api_key = st.secrets.get("GOOGLE_API_KEY")

if api_key:
    api_key = api_key.strip()
    genai.configure(api_key=api_key)
    
    # AJUSTE PARA EVITAR 404: 
    # Forçamos o modelo sem o prefixo 'models/' que às vezes causa conflito
    try:
        model = genai.GenerativeModel('gemini-1.5-flash')
    except Exception as e:
        st.error(f"Erro ao carregar o motor da IA: {e}")
        st.stop()
else:
    st.error("❌ Chave API não configurada nos Secrets.")
    st.stop()

# 3. Interface
st.title("🏗️ PatologiaBR: Analista Técnico I.A.")
st.write("Análise técnica de patologias da construção baseada em NBRs.")

img = None
col1, col2 = st.columns(2)

with col1:
    st.subheader("📸 Registro Fotográfico")
    foto = st.file_uploader("Suba a imagem da patologia", type=["jpg", "png", "jpeg"])
    if foto:
        img = Image.open(foto)
        st.image(img, caption="Imagem carregada", use_container_width=True)

with col2:
    st.subheader("📝 Contexto")
    detalhes = st.text_area("Descreva o local e detalhes observados:", 
                            placeholder="Ex: Fissura em viga de concreto, prédio com 15 anos.")
    analisar = st.button("🚀 Executar Diagnóstico Técnico", type="primary", use_container_width=True)

# 4. Execução da Análise
if analisar:
    if img is not None:
        with st.spinner('Analisando imagem conforme normas técnicas...'):
            try:
                # O prompt agora é passado diretamente
                prompt = f"""
                Aja como um perito em engenharia civil especializado em patologias.
                Analise a imagem e este contexto: {detalhes}.
                Identifique a patologia, cite NBRs brasileiras relevantes e sugira correções.
                """
                
                # Gerar conteúdo
                response = model.generate_content([prompt, img])
                
                st.markdown("---")
                st.success("✅ Análise Concluída")
                st.markdown("### 📋 Relatório Técnico")
                st.write(response.text)
                
            except Exception as e:
                st.error(f"Erro durante a análise: {e}")
                st.info("Se o erro persistir, clique em 'Manage App' e depois em 'Reboot App' no painel do Streamlit.")
    else:
        st.warning("⚠️ Por favor, suba uma foto antes de analisar.")

# Rodapé
st.markdown("---")
st.caption("AD Construções e Gerenciamento de Obras")
