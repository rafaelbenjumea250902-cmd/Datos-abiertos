"""
Script de prueba para Groq API
"""

import streamlit as st
import os
from groq import Groq

st.title("🔍 Diagnóstico de Groq API")

# Verificar si la API key existe
api_key = os.getenv("GROQ_API_KEY")

st.subheader("1️⃣ Verificación de API Key")
if api_key:
    st.success(f"✅ API Key encontrada: {api_key[:10]}...")
    st.info(f"Longitud de la key: {len(api_key)} caracteres")
else:
    st.error("❌ GROQ_API_KEY NO encontrada")
    st.warning("""
    **Configura en Settings → Secrets:**
    
    ```
    GROQ_API_KEY = "gsk_xxxxxxxxxxxxxxxxxxxxx"
    ```
    """)
    st.info("""
    **Cómo obtener tu API Key:**
    
    1. Ve a: https://console.groq.com
    2. Sign up (NO requiere tarjeta de crédito)
    3. API Keys → Create API Key
    4. Copia la key (empieza con "gsk_")
    
    **100% GRATIS permanente**
    """)
    st.stop()

# Probar conexión
st.subheader("2️⃣ Prueba de Conexión")

try:
    with st.spinner("Probando conexión con Groq..."):
        # Crear cliente
        client = Groq(api_key=api_key)
        
        # Hacer request de prueba
        response = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[
                {"role": "user", "content": "Responde en español con una sola palabra: éxito"}
            ],
            max_tokens=50
        )
        
        response_text = response.choices[0].message.content
        
        st.success("✅ Conexión exitosa!")
        st.write("**Respuesta del modelo:**")
        st.code(response_text)
        
        # Información del modelo
        st.info("**Modelo:** llama-3.3-70b-versatile (Llama 3.3 70B)")
        st.info("**Proveedor:** Groq (Ultra Rápido)")
        st.info("**Estado:** Operacional ✅")
        
except Exception as e:
    st.error(f"❌ Error en la conexión: {str(e)}")
    
    error_str = str(e).lower()
    
    if "api key" in error_str or "invalid" in error_str or "401" in error_str:
        st.warning("""
        **Error: API Key inválida**
        
        Soluciones:
        1. Verifica que la API Key esté completa
        2. Genera una nueva en: https://console.groq.com
        3. Asegúrate de copiar "gsk_..." completo
        4. Actualiza el Secret en Streamlit Cloud
        """)
        
    elif "quota" in error_str or "limit" in error_str or "429" in error_str:
        st.warning("""
        **Error: Límite excedido**
        
        Límite: 30 requests/minuto
        Espera 1 minuto e intenta de nuevo.
        """)
        
    else:
        st.error(f"**Error completo:** {str(e)}")

# Información adicional
st.subheader("3️⃣ Información del Sistema")
st.write(f"**Python version:** {os.sys.version}")

try:
    import groq
    st.write(f"**groq version:** {groq.__version__}")
except:
    st.write("**groq version:** No disponible")

st.subheader("4️⃣ Por Qué Groq es INCREÍBLE")
st.write("""
**Ventajas de Groq:**

⚡ **VELOCIDAD:** 0.5-1 segundo (vs 2-3 seg otras APIs)
✅ **GRATIS:** Permanentemente, sin tarjeta
✅ **LÍMITES:** 30 req/min, 14,400/día
✅ **ESPAÑOL:** Excelente (9/10)
✅ **MODELOS:** Llama 3.3 70B, Mixtral, Gemma
✅ **ESTABLE:** API muy confiable
✅ **SETUP:** 2 minutos

**Hardware especial:**
Groq usa chips LPU diseñados para IA.
Por eso es TAN rápido.
""")

st.subheader("5️⃣ Comparación de APIs Gratuitas")
st.write("""
| Característica | Groq | Gemini | Claude |
|----------------|------|--------|--------|
| **Tarjeta** | ❌ No | ❌ No | ⚠️ Sí* |
| **Velocidad** | ⚡ 0.5 seg | 2-3 seg | 1-2 seg |
| **Límite/min** | 30 ✅ | 15 | 50 |
| **Límite/día** | 14,400 ✅ | 1,500 | ~1,000 |
| **Problemas** | ❌ Ninguno | ⚠️ Algunos | ❌ Ninguno |
| **Español** | 9/10 | 9/10 | 10/10 |
| **Setup** | 2 min ✅ | 5-10 min | 2 min |
| **Gratis** | Forever ✅ | Forever | $5 inicial |

*Claude pide tarjeta después de $5

**GANADOR: Groq** 🏆
""")

st.subheader("6️⃣ Modelos Disponibles en Groq")
st.write("""
**Recomendados (gratis):**

1. **llama-3.3-70b-versatile** ⭐ (el mejor)
   - Más potente
   - Excelente razonamiento
   - 128K tokens contexto

2. **llama-3.1-70b-versatile**
   - Muy bueno
   - 128K tokens

3. **mixtral-8x7b-32768**
   - Rápido
   - Bueno en español
   - 32K tokens

Todos gratis, sin límite de uso (dentro de 30 req/min)
""")
