import streamlit as st
from PIL import Image
import google.generativeai as genai

# 1. Configuração da Página
st.set_page_config(page_title="PatologiaBR", page_icon="🏗️", layout="wide")

# 2. Configuração da API (Versão Robusta contra Erro 404)
api_key = st.secrets.get("GOOGLE_API_KEY")

if api_key:
    # Remove espaços em branco e configura a API
    genai.configure(api_key=api_key.strip())
    
    try:
        # Lista os modelos disponíveis para encontrar o nome exato aceito pelo sistema
        modelos_disponiveis = [m.name for m in genai.list_models() if 'generateContent' in m.supported_generation_methods]
        
        # Prioriza o Gemini 1.5 Flash (ideal para fotos e velocidade)
        if 'models/gemini-1.5-flash' in modelos_disponiveis:
            nome_modelo = 'models/gemini-1.5-flash'
        elif 'models/gemini-1.5-pro' in modelos_disponiveis:
            nome_modelo = 'models/gemini-1.5-pro'
        else:
            # Fallback se a lista falhar, usando o nome padrão da nova versão
            nome_modelo = 'gemini-1.5-flash'
            
        model = genai.GenerativeModel(nome_modelo)
    except Exception as e:
        st.error(f"Erro ao conectar com o catálogo de modelos do Google: {e}")
        st.stop()
else:
    st.error("❌ Chave API não configurada nos Secrets do Streamlit.")
    st.stop()

# 3. Interface do Usuário
st.title("🏗️ PatologiaBR: Analista Técnico I.A.")
st.write("Análise técnica de patologias da construção baseada em NBRs.")

img = None
col1, col2 = st.columns(2)

with col1:
    st.subheader("📸 Registro Fotográfico")
    foto = st.file_uploader("Suba a imagem da patologia", type=["jpg", "png", "jpeg"])
    if foto:
        img = Image.open(foto)
        st.image(img, caption="Imagem carregada para análise", use_container_width=True)

with col2:
    st.subheader("📝 Contexto da Observação")
    detalhes = st.text_area("Descreva o local e detalhes observados:", 
                            placeholder="Ex: Fissura em viga de concreto, prédio com 15 anos, próximo à região costeira.")
    analisar = st.button("🚀 Executar Diagnóstico Técnico", type="primary", use_container_width=True)

# 4. Processamento e Geração do Relatório
if analisar:
    if img is not None:
        with st.spinner('Analisando imagem e consultando normas técnicas...'):
            try:
                # Instrução detalhada para a IA agir como perito
                comando_pericial = (
                    "Você é um engenheiro civil perito em patologia das construções. "
                    "Analise a imagem fornecida detalhadamente e considere o seguinte contexto: "
                    f"'{detalhes}'.\n\n"
                    "Gere um relatório técnico estruturado contendo:\n"
                    "1. DIAGNÓSTICO: Identificação da patologia.\n"
                    "2. CAUSAS PROVÁVEIS: Explique o fenômeno físico/químico.\n"
                    "3. REFERÊNCIA NORMATIVA: Cite NBRs relevantes (ex: NBR 6118, 15575, 5674).\n"
                    "4. RECOMENDAÇÕES: Sugira intervenções ou ensaios complementares."
                )
                
                # Chamada enviando Texto e Imagem em uma lista
                response = model.generate_content([comando_pericial, img])
                
                if response.text:
                    st.markdown("---")
                    st.success("✅ Diagnóstico Concluído")
                    st.subheader("📋 Relatório Técnico Profissional")
                    st.markdown(response.text)
                else:
                    st.warning("A IA não conseguiu gerar uma resposta. Tente uma imagem mais clara.")
                    
            except Exception as e:
                st.error(f"Erro durante a análise: {e}")
                st.info("Se o erro persistir, faça o 'Reboot App' no painel do Streamlit Cloud.")
    else:
        st.warning("⚠️ Por favor, suba uma foto antes de clicar em analisar.")

# Rodapé profissional
st.markdown("---")
st.caption("AD Construção e Gerenciamento de Obras")
