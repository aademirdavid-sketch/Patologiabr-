import streamlit as st
from PIL import Image
import google.generativeai as genai
import os

# 1. Configuração da Página
st.set_page_config(page_title="PatologiaBR", page_icon="🏗️", layout="wide")

# 2. Configuração da Chave API (Segurança)
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

# --- INICIALIZAÇÃO DE VARIÁVEIS ---
# Isso evita o erro 'NameError' pois as variáveis já existem antes do clique
img = None
detalhes = ""

col1, col2 = st.columns(2)

with col1:
    foto = st.file_uploader("Suba a foto da patologia", type=["jpg", "png", "jpeg"])
    if foto:
        try:
            img = Image.open(foto)
            st.image(img, caption="Imagem para análise", use_container_width=True)
        except Exception as e:
            st.error(f"Erro ao abrir imagem: {e}")

with col2:
    detalhes = st.text_area("Descreva o contexto (local, idade da obra, material, etc.):", 
                            placeholder="Ex: Viga de concreto armado com sinais de corrosão, obra de 20 anos.")
    analisar = st.button("Executar Diagnóstico Técnico", type="primary")

# --- BLOCO DE EXECUÇÃO ---
if analisar:
    if img is not None:
        with st.spinner('Consultando normas e analisando imagem...'):
            try:
                # Criamos o prompt dentro do bloco de execução
                prompt_completo = f"""
                Aja como um perito em engenharia civil especialista em patologias das construções.
                Analise a imagem fornecida considerando este contexto: {detalhes}.
                
                Forneça um relatório técnico estruturado:
                1. IDENTIFICAÇÃO: O que é observado na imagem?
                2. CAUSAS PROVÁVEIS: Por que isso aconteceu?
                3. NORMAS TÉCNICAS: Cite as NBRs relevantes (ex: NBR 6118, 15575, 6122, etc).
                4. RECOMENDAÇÕES: Quais os próximos passos técnicos sugeridos?
                """
                
                # Chamada da I.A.
                response = model.generate_content([prompt_completo, img])
                
                st.markdown("---")
                st.subheader("📋 Resultado do Diagnóstico Técnico")
                st.write(response.text)
                
            except Exception as e:
                st.error(f"Erro na comunicação com a I.A.: {e}")
    else:
        st.warning("⚠️ Atenção: Você precisa carregar uma foto antes de executar o diagnóstico.")

# Rodapé técnico
st.markdown("---")
st.caption("PatologiaBR - Ferramenta de auxílio técnico para profissionais da construção.")
