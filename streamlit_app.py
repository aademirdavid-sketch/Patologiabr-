if analisar:
    if foto is not None:
        with st.spinner('Analisando conforme normas técnicas...'):
            # Criamos o prompt usando o que você escreveu em 'detalhes'
            prompt_completo = f"""
            Aja como um perito em engenharia civil. 
            Analise a imagem e o seguinte contexto: {detalhes}
            Identifique a patologia, cite as NBRs brasileiras relevantes 
            e sugira ações de correção.
            """
            
            # Usamos a 'img' que foi aberta lá em cima
            response = model.generate_content([prompt_completo, img])
            
            st.markdown("---")
            st.markdown("### 📋 Resultado da Análise")
            st.write(response.text)
    else:
        st.warning("⚠️ Por favor, suba uma foto da patologia antes de clicar em analisar.")
