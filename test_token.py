"""
Script de prueba para verificar token de Hugging Face
Ejecuta esto en Streamlit Cloud para diagnosticar el problema
"""

import streamlit as st
import os
from huggingface_hub import InferenceClient

st.title("🔍 Diagnóstico de Hugging Face Token")

# Verificar si el token existe
token = os.getenv("HUGGINGFACE_TOKEN")

st.subheader("1️⃣ Verificación de Token")
if token:
    st.success(f"✅ Token encontrado: {token[:10]}...")
    st.info(f"Longitud del token: {len(token)} caracteres (debe ser 37)")
else:
    st.error("❌ Token NO encontrado en variables de entorno")
    st.warning("Configura HUGGINGFACE_TOKEN en Settings → Secrets")
    st.stop()

# Probar conexión con Hugging Face
st.subheader("2️⃣ Prueba de Conexión")

try:
    with st.spinner("Probando conexión con Hugging Face..."):
        client = InferenceClient(
            model="mistralai/Mistral-7B-Instruct-v0.2",
            token=token
        )
        
        # Hacer una llamada simple
        response = client.text_generation(
            "Hola, responde con una palabra: éxito",
            max_new_tokens=10,
            temperature=0.7
        )
        
        st.success("✅ Conexión exitosa!")
        st.write("**Respuesta del modelo:**")
        st.code(response)
        
except Exception as e:
    st.error(f"❌ Error en la conexión: {str(e)}")
    
    # Diagnosticar el tipo de error
    error_str = str(e).lower()
    
    if "401" in error_str or "unauthorized" in error_str:
        st.warning("""
        **Error 401: Token inválido**
        
        Soluciones:
        1. Verifica que el token esté completo (37 caracteres)
        2. Regenera el token en Hugging Face:
           https://huggingface.co/settings/tokens
        3. Actualiza el Secret en Streamlit Cloud
        """)
        
    elif "503" in error_str or "loading" in error_str:
        st.info("""
        **Error 503: Modelo cargando**
        
        Esto es normal. El modelo está "dormido" y se está despertando.
        Espera 20-30 segundos e intenta de nuevo.
        """)
        
    elif "rate limit" in error_str or "429" in error_str:
        st.warning("""
        **Error 429: Límite de requests excedido**
        
        Has usado todas las peticiones gratis del día.
        Espera 24 horas o usa otro token.
        """)
    else:
        st.error(f"Error desconocido: {str(e)}")

# Información adicional
st.subheader("3️⃣ Información del Sistema")
st.write(f"**Python version:** {os.sys.version}")
st.write(f"**Variables de entorno disponibles:**")
env_vars = [key for key in os.environ.keys() if 'HUG' in key.upper() or 'TOKEN' in key.upper()]
if env_vars:
    for var in env_vars:
        st.write(f"- {var}")
else:
    st.write("- No se encontraron variables relacionadas")
