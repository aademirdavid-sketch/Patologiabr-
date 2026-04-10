import streamlit as st
from PIL import Image
import google.generativeai as genai
import os

# 1. Configuração da Página
st.set_page_config(
    page_title="PatologiaBR", 
    page_icon="🏗️", 
    layout="wide"
)

# 2. Configuração da Chave API
# O código busca a chave nos Secrets do Streamlit para sua segurança
api_key = st.secrets.get("GOOGLE_API_KEY")

if api_key:
    # Remove espaços em branco acidentais
    api_key = api_key.strip()
    try:
        genai.configure(api_key=api_key)
        # Usando a versão estável e rápida para análise de imagens
        model = genai.GenerativeModel('gemini-1.5-flash')
    except Exception as e:
        st.error(f"Erro ao configurar o Google Gemini: {e}")
        st.stop()
else:
    st.error("❌ ERRO: Chave API não configurada nos Secrets do Streamlit.")
    st.info("💡 Vá em Settings > Secrets e adicione: GOOGLE_API_KEY = 'sua_chave_aqui'")
    st.stop()

# 3. Interface do Usuário
st.title("🏗️ PatologiaBR: Analista Técnico I.A.")
st.write("Diagnóstico inteligente de patologias da construção civil baseado em NBRs.")

# Inicialização da variável de imagem para evitar erros de fluxo
img = None

col1, col2 = st.columns(2)

with col1:
    st.subheader("📸 Registro Fotográfico")
    foto = st.file_uploader("Suba a imagem da patologia (JPG, PNG, JPEG)", type=["jpg", "png", "jpeg"])
    if foto:
        try:
            img = Image.open(foto)
            st.image(img, caption="Imagem carregada para análise", use_container_width=True)
        except Exception as e:
            st.error(f"Erro ao processar imagem: {e}")

with col2:
    st.subheader("📝 Contexto da Inspeção")
    detalhes = st.text_area(
        "Descreva o local e detalhes observados:", 
        placeholder="Ex: Fissura em viga de concreto, prédio de 15 anos, ambiente industrial.",
        height=150
    )
    analisar = st.button("🚀 Executar Diagnóstico Técnico", type="primary", use_container_width=True)

# 4. Bloco de Execução da Análise
if analisar:
    if img is not None:
        with st.spinner('Analisando imagem e consultando normas técnicas...'):
            try:
                # Prompt estruturado para perfil técnico/pericial
                prompt_tecnico = f"""
                Aja como um Engenheiro Civil perito em Patologia das Construções.
                Analise a imagem fornecida e considere este contexto adicional: {detalhes}.
                
                Forneça um relatório técnico organizado nos seguintes tópicos:
                1. DIAGNÓSTICO: Identificação técnica da patologia vista na foto.
                2. CAUSAS PROVÁVEIS: Por que esse problema ocorreu?
                3. NORMAS TÉCNICAS: Referencie NBRs brasileiras relevantes (ex: NBR 6118, NBR 15575, NBR 5674).
                4. RECOMENDAÇÕES: Sugestões práticas de reparo ou necessidade de ensaios.
                
                Seja objetivo, profissional e técnico.
                """
                
                # Chamada para a API enviando texto e imagem
                response = model.generate_content([prompt_tecnico, img])
                
                st.markdown("---")
                st.success("✅ Diagnóstico Concluído")
                st.markdown("### 📋 Relatório de Análise Técnica")
                st.write(response.text)
                
            except Exception as e:
                if "API key not valid" in str(e):
                    st.error("❌ Chave API Inválida! Verifique se a chave no Secrets está correta.")
                else:
                    st.error(f"Erro durante a análise: {e}")
    else:
        st.warning("⚠️ Atenção: Você precisa carregar uma foto antes de iniciar a análise.")

# Rodapé
st.markdown("---")
st.caption("PatologiaBR - Assistente Digital para Gerenciamento de Obras e Perícias.")
