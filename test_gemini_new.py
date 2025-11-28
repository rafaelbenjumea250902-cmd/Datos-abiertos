"""
Script de prueba para Google Gemini (nueva API oficial)
"""

import streamlit as st
import os
from google import genai

st.title("🔍 Diagnóstico de Google Gemini API (Nueva)")

# Verificar si la API key existe
api_key = os.getenv("GEMINI_API_KEY")

st.subheader("1️⃣ Verificación de API Key")
if api_key:
    st.success(f"✅ API Key encontrada: {api_key[:10]}...")
    st.info(f"Longitud de la key: {len(api_key)} caracteres")
else:
    st.error("❌ GEMINI_API_KEY NO encontrada en variables de entorno")
    st.warning("""
    **Configura en Settings → Secrets:**
    
    ```
    GEMINI_API_KEY = "tu_api_key_aqui"
    ```
    
    Nota: El nombre cambió de GOOGLE_API_KEY a GEMINI_API_KEY
    """)
    st.stop()

# Probar conexión
st.subheader("2️⃣ Prueba de Conexión")

try:
    with st.spinner("Probando conexión con Google Gemini..."):
        # Configurar variable de entorno (necesaria para la nueva librería)
        os.environ["GEMINI_API_KEY"] = api_key
        
        # Crear cliente (automáticamente usa GEMINI_API_KEY del entorno)
        client = genai.Client()
        
        # Probar con gemini-2.0-flash-exp (el más nuevo)
        response = client.models.generate_content(
            model="gemini-2.0-flash-exp",
            contents="Responde en español con una sola palabra: éxito"
        )
        
        st.success("✅ Conexión exitosa!")
        st.write("**Respuesta del modelo:**")
        st.code(response.text)
        
        # Información del modelo
        st.info("**Modelo:** gemini-2.0-flash-exp")
        st.info("**Librería:** google-genai (nueva API oficial)")
        st.info("**Estado:** Operacional ✅")
        
except Exception as e:
    st.error(f"❌ Error en la conexión: {str(e)}")
    
    error_str = str(e).lower()
    
    if "api key" in error_str or "invalid" in error_str or "401" in error_str:
        st.warning("""
        **Error: API Key inválida**
        
        Soluciones:
        1. Verifica que la API Key esté completa
        2. Genera una nueva en: https://aistudio.google.com/app/apikey
        3. Actualiza el Secret en Streamlit Cloud:
           ```
           GEMINI_API_KEY = "AIzaSyDxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"
           ```
        """)
        
    elif "quota" in error_str or "limit" in error_str or "429" in error_str:
        st.warning("""
        **Error: Límite de requests excedido**
        
        El límite gratuito es 15 requests/minuto.
        Espera un minuto e intenta de nuevo.
        """)
        
    else:
        st.error(f"**Error completo:** {str(e)}")

# Información adicional
st.subheader("3️⃣ Información del Sistema")
st.write(f"**Python version:** {os.sys.version}")

try:
    import google.genai
    st.write(f"**google-genai version:** {google.genai.__version__}")
except:
    st.write("**google-genai version:** No disponible")

st.subheader("4️⃣ Cambios en la Nueva API")
st.write("""
**Diferencias con la API anterior:**

| Aspecto | API Anterior | API Nueva |
|---------|--------------|-----------|
| **Librería** | `google-generativeai` | `google-genai` ✅ |
| **Import** | `import google.generativeai` | `from google import genai` ✅ |
| **Variable** | `GOOGLE_API_KEY` | `GEMINI_API_KEY` ✅ |
| **Cliente** | `genai.configure()` | `genai.Client()` ✅ |
| **Modelo** | `gemini-pro` | `gemini-2.0-flash-exp` ✅ |
| **Método** | `generate_content()` | `models.generate_content()` ✅ |

**Ventajas:**
- ✅ Más estable
- ✅ Mejor documentación
- ✅ API oficial de Google
- ✅ Modelos más nuevos
""")

st.subheader("5️⃣ Límites de Gemini API (Gratis)")
st.write("""
- ✅ **15 requests por minuto**
- ✅ **1,500 requests por día**
- ✅ **1 millón de tokens por día**
- ✅ Sin tarjeta de crédito requerida
- ✅ Gratis permanente
""")
