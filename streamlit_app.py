# Título e Interface
st.title("🏗️ PatologiaBR: Analista Técnico I.A.")
st.write("Análise de patologias da construção baseada em NBRs.")

# Criamos as colunas
col1, col2 = st.columns(2)

# IMPORTANTE: Definimos as variáveis como vazias antes de tudo
img = None
prompt_completo = ""

with col1:
    foto = st.file_uploader("Suba a foto da patologia", type=["jpg", "png", "jpeg"])
    if foto:
        img = Image.open(foto)
        st.image(img, caption="Imagem para análise", use_container_width=True)

with col2:
    detalhes = st.text_area("Descreva o contexto (local, idade da obra, etc.):")
    analisar = st.button("Executar Diagnóstico Técnico", type="primary")

# O bloco de execução deve estar colado na margem esquerda (sem espaços no 'if')
if analisar:
    if img is not None:
        with st.spinner('Analisando conforme normas técnicas...'):
            # Criamos o texto do prompt
            prompt_completo = f"""
            Aja como um perito em engenharia civil.
            Analise a imagem e o seguinte contexto: {detalhes}
            Identifique a patologia, cite as NBRs brasileiras relevantes 
            e sugira ações de correção.
            """
            
            # Agora enviamos para a IA
            response = model.generate_content([prompt_completo, img])
            
            st.markdown("---")
            st.markdown("### 📋 Resultado da Análise")
            st.write(response.text)
    else:
        st.error("⚠️ Por favor, suba uma foto da patologia antes de clicar em analisar.")
