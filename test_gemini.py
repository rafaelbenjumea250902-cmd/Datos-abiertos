"""
Script de prueba para verificar Google Gemini API
"""

import streamlit as st
import os
import google.generativeai as genai

st.title("🔍 Diagnóstico de Google Gemini API")

# Verificar si la API key existe
api_key = os.getenv("GOOGLE_API_KEY")

st.subheader("1️⃣ Verificación de API Key")
if api_key:
    st.success(f"✅ API Key encontrada: {api_key[:10]}...")
    st.info(f"Longitud de la key: {len(api_key)} caracteres")
else:
    st.error("❌ GOOGLE_API_KEY NO encontrada en variables de entorno")
    st.warning("Configura GOOGLE_API_KEY en Settings → Secrets")
    st.code('GOOGLE_API_KEY = "tu_api_key_aqui"')
    st.stop()

# Probar conexión con Google Gemini
st.subheader("2️⃣ Prueba de Conexión")

try:
    with st.spinner("Probando conexión con Google Gemini..."):
        # Configurar API
        genai.configure(api_key=api_key)
        
        # Crear modelo
        model = genai.GenerativeModel('gemini-1.5-flash-latest')        
        # Hacer una llamada simple
        response = model.generate_content(
            "Responde en español con una sola palabra: éxito",
            generation_config=genai.types.GenerationConfig(
                max_output_tokens=20,
                temperature=0.7
            )
        )
        
        st.success("✅ Conexión exitosa!")
        st.write("**Respuesta del modelo:**")
        st.code(response.text)
        
        # Información del modelo
        st.info(f"**Modelo:** gemini-1.5-flash")
        st.info(f"**Estado:** Operacional ✅")
        
except Exception as e:
    st.error(f"❌ Error en la conexión: {str(e)}")
    
    # Diagnosticar el tipo de error
    error_str = str(e).lower()
    
    if "api key" in error_str or "invalid" in error_str:
        st.warning("""
        **Error: API Key inválida**
        
        Soluciones:
        1. Verifica que la API Key esté completa
        2. Genera una nueva en: https://aistudio.google.com/app/apikey
        3. Actualiza el Secret en Streamlit Cloud:
           GOOGLE_API_KEY = "tu_nueva_key"
        """)
        
    elif "quota" in error_str or "limit" in error_str:
        st.warning("""
        **Error: Límite de requests excedido**
        
        El límite gratuito es 15 requests/minuto.
        Espera un minuto e intenta de nuevo.
        """)
        
    elif "blocked" in error_str or "safety" in error_str:
        st.info("""
        **Filtro de Seguridad Activado**
        
        Gemini bloqueó la respuesta por seguridad.
        Esto es normal en algunas consultas.
        """)
    else:
        st.error(f"**Error completo:** {str(e)}")

# Información adicional
st.subheader("3️⃣ Información del Sistema")
st.write(f"**Python version:** {os.sys.version}")

st.subheader("4️⃣ Límites de Gemini API (Gratis)")
st.write("""
- ✅ **15 requests por minuto**
- ✅ **1,500 requests por día**
- ✅ **1 millón de tokens por día**
- ✅ Sin tarjeta de crédito requerida
- ✅ Gratis permanente
""")

st.subheader("5️⃣ Ventajas vs Hugging Face")
st.write("""
| Característica | Gemini | Hugging Face |
|---------------|--------|--------------|
| Velocidad | 1-2 seg ⚡ | 20 seg inicial 🐢 |
| Español | Excelente ✅ | Bueno ✅ |
| Límite/día | 1,500 🎉 | ~1,000 ⚠️ |
| Primera carga | Rápida ⚡ | Lenta (modelo dormido) 😴 |
| API estable | Sí ✅ | Cambios recientes ⚠️ |
""")
