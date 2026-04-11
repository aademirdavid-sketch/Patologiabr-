import streamlit as st
from PIL import Image
import google.generativeai as genai

# 1. Configuração da Página
st.set_page_config(page_title="PatologiaBR", page_icon="🏗️", layout="wide")

# 2. Configuração da API
api_key = st.secrets.get("GOOGLE_API_KEY")

if api_key:
    genai.configure(api_key=api_key.strip())
    # Usamos o modelo flash que é excelente para visão e rápido
    model = genai.GenerativeModel('gemini-1.5-flash')
else:
    st.error("❌ Chave API não configurada nos Secrets do Streamlit.")
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
        with st.spinner('IA Processando... Analisando imagem e normas técnicas.'):
            try:
                # O SEGREDO ESTÁ AQUI: O prompt precisa ser uma lista organizada
                # Passamos o texto de instrução, o contexto do usuário e a imagem.
                comando = (
                    "Você é um perito em engenharia civil especializado em patologias das construções. "
                    "Analise tecnicamente a imagem fornecida e os detalhes abaixo.\n\n"
                    f"CONTEXTO DO USUÁRIO: {detalhes}\n\n"
                    "REQUISITOS DO RELATÓRIO:\n"
                    "1. Identificação da Patologia.\n"
                    "2. Prováveis causas (Ex: recalque, carbonatação, corrosão de armadura).\n"
                    "3. Normas Técnicas (NBRs) aplicáveis (ex: NBR 6118, 5674, 15575).\n"
                    "4. Recomendações de intervenção ou ensaios extras."
                )
                
                # Chamada multimodal corrigida
                # O Gemini 1.5 Flash aceita uma lista com strings e o objeto PIL Image
                response = model.generate_content([comando, img])
                
                if response.text:
                    st.markdown("---")
                    st.success("✅ Diagnóstico Gerado com Sucesso")
                    st.subheader("📋 Relatório Técnico Profissional")
                    st.markdown(response.text)
                else:
                    st.warning("A IA processou, mas retornou um resultado vazio. Tente descrever melhor o contexto.")

            except Exception as e:
                st.error(f"Erro Crítico na Análise: {e}")
                st.info("Verifique se sua biblioteca está atualizada: pip install -U google-generativeai")
    else:
        st.warning("⚠️ Por favor, suba uma foto para que a IA possa analisar.")

# Rodapé
st.markdown("---")
st.caption("AD Construção e Gerenciamento de Obras")
