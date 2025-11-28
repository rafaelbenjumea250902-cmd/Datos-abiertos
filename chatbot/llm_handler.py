import google.generativeai as genai
import os
from typing import List, Dict
from .data_processor import DataProcessor

class ChatbotHandler:
    """
    Maneja las interacciones con Google Gemini API
    """
    
    def __init__(self):
        self.data_processor = DataProcessor()
        self.data_loaded = self.data_processor.load_data()
        
        # Configurar Google Gemini
        api_key = os.getenv("GOOGLE_API_KEY")
        
        if api_key:
            genai.configure(api_key=api_key)
            self.model = genai.GenerativeModel('gemini-pro')
            self.api_available = True
        else:
            self.api_available = False
            print("⚠️ GOOGLE_API_KEY no configurada")
        
        # Sistema de prompts
        self.system_prompt = self._build_system_prompt()
        
    def _build_system_prompt(self) -> str:
        """Construye el prompt del sistema con contexto de datos"""
        
        base_prompt = """Eres un asistente virtual especializado en análisis de seguridad ciudadana para el Observatorio de Seguridad de Santander, Colombia.

Tu función es ayudar a funcionarios públicos, investigadores y ciudadanos a comprender los datos de criminalidad y las predicciones generadas por modelos de machine learning.

CARACTERÍSTICAS:
- Respondes en español de manera clara y profesional
- Usas datos específicos cuando están disponibles
- Explicas conceptos técnicos de forma accesible
- Eres preciso y evitas especulaciones
- Cuando no tienes información específica, lo indicas claramente

"""
        
        if self.data_loaded:
            data_context = self.data_processor.get_context_string()
            base_prompt += f"\n{data_context}\n"
        else:
            base_prompt += "\nNOTA: Los datos aún no están cargados. Informa al usuario que debe cargar los archivos CSV.\n"
        
        base_prompt += """
INSTRUCCIONES:
1. Si te preguntan sobre estadísticas específicas, usa los datos del contexto
2. Si te preguntan sobre predicciones, explica que fueron generadas con modelos ML
3. Si te preguntan sobre metodología, explica Random Forest y análisis temporal
4. Mantén respuestas concisas (máximo 4-5 párrafos)
5. Usa emojis ocasionalmente para hacer la conversación más amigable

Responde siempre de manera útil y basada en datos.
"""
        
        return base_prompt
    
    def get_response(self, user_message: str, max_tokens: int = 500) -> str:
        """
        Genera una respuesta usando Google Gemini
        """
        
        if not self.api_available:
            return self._fallback_response(user_message)
        
        try:
            # Construir el prompt completo
            full_prompt = f"{self.system_prompt}\n\nUsuario: {user_message}\n\nAsistente:"
            
            # Configurar generación
            generation_config = genai.types.GenerationConfig(
                max_output_tokens=max_tokens,
                temperature=0.7,
                top_p=0.95,
            )
            
            # Generar respuesta usando Gemini
            response = self.model.generate_content(
                full_prompt,
                generation_config=generation_config
            )
            
            # Obtener texto de respuesta
            if response.text:
                cleaned_response = self._clean_response(response.text)
                return cleaned_response
            else:
                return self._fallback_response(user_message)
            
        except Exception as e:
            print(f"Error generando respuesta con Gemini: {e}")
            
            # Respuesta de fallback sin LLM
            return self._fallback_response(user_message)
    
    def _clean_response(self, response: str) -> str:
        """Limpia y formatea la respuesta del LLM"""
        # Remover texto repetido o cortado
        response = response.strip()
        
        # Asegurar que termina en punto
        if response and not response[-1] in ['.', '!', '?']:
            # Buscar el último punto
            last_period = response.rfind('.')
            if last_period > len(response) * 0.7:  # Si está en el último 30%
                response = response[:last_period + 1]
        
        return response
    
    def _fallback_response(self, user_message: str) -> str:
        """
        Respuesta de emergencia cuando el LLM falla
        Usa lógica simple basada en palabras clave
        """
        
        user_message_lower = user_message.lower()
        
        # Respuestas por palabras clave
        if any(word in user_message_lower for word in ['hola', 'buenos días', 'buenas tardes', 'hey']):
            return """¡Hola! 👋 Soy el asistente virtual del Observatorio de Seguridad de Santander. 

Puedo ayudarte con:
📊 Estadísticas de criminalidad
🎯 Predicciones de seguridad
🗺️ Información por municipio
📈 Análisis de tendencias

¿Qué te gustaría saber?"""
        
        elif any(word in user_message_lower for word in ['municipio', 'municipios', 'ciudad', 'pueblos']):
            return f"""El Observatorio cubre los **87 municipios** de Santander, incluyendo:

🏛️ **Área Metropolitana:** Bucaramanga, Floridablanca, Girón, Piedecuesta
🌄 **Provincias:** Comunera, García Rovira, Guanentá, Mares, Soto, Vélez

Los datos incluyen análisis históricos y predicciones basadas en machine learning para cada municipio.

¿Sobre qué municipio específico te gustaría información?"""
        
        elif any(word in user_message_lower for word in ['predicción', 'predicciones', 'futuro', 'proyección']):
            return """🎯 **Predicciones de Seguridad**

Utilizamos modelos de Machine Learning (Random Forest) para predecir:
- Nivel de riesgo por municipio
- Tendencias de criminalidad
- Zonas de mayor incidencia
- Patrones temporales

Las predicciones se basan en:
✅ Más de 1 millón de registros históricos
✅ Variables temporales y geoespaciales
✅ Patrones de criminalidad identificados

¿Quieres saber sobre algún municipio específico?"""
        
        elif any(word in user_message_lower for word in ['dato', 'datos', 'estadística', 'estadísticas']):
            if self.data_loaded:
                return self.data_processor.get_summary()
            else:
                return """📊 **Información de Datos**

El sistema está preparado para analizar:
- Datos históricos de criminalidad
- Predicciones generadas por ML
- Información de 87 municipios

⚠️ Los archivos CSV aún no están cargados. Por favor, asegúrate de que los archivos estén en la carpeta `data/`.

¿Necesitas ayuda con la carga de datos?"""
        
        elif any(word in user_message_lower for word in ['funciona', 'cómo', 'qué es', 'explicar']):
            return """🤖 **Sobre este Observatorio**

Este sistema combina:
- **Análisis de Big Data:** Procesamiento de millones de registros
- **Machine Learning:** Modelos predictivos de seguridad
- **Visualización:** Dashboards interactivos en Power BI
- **IA Conversacional:** Este chatbot para consultas

**Tecnologías:**
🐍 Python (Pandas, Scikit-learn)
📊 Power BI
🤖 Hugging Face (Mistral AI)
☁️ Streamlit Cloud

Desarrollado para la Gobernación de Santander 🏛️

¿Qué más te gustaría saber?"""
        
        elif any(word in user_message_lower for word in ['ayuda', 'help', 'qué puedes hacer']):
            return """💬 **¿Cómo puedo ayudarte?**

Puedes preguntarme sobre:

1️⃣ **Estadísticas generales**
   - "¿Cuántos delitos se registraron?"
   - "Dame estadísticas de criminalidad"

2️⃣ **Información por municipio**
   - "¿Qué tal la seguridad en Bucaramanga?"
   - "Municipios más seguros"

3️⃣ **Predicciones**
   - "¿Qué predicen los modelos?"
   - "Tendencias de seguridad"

4️⃣ **Metodología**
   - "¿Cómo funcionan las predicciones?"
   - "¿Qué datos usan?"

¡Escribe tu pregunta! 😊"""
        
        else:
            return """Gracias por tu pregunta. En este momento estoy procesando información limitada sin conexión al modelo principal.

📊 **Puedo ayudarte con:**
- Información general del observatorio
- Explicación de la metodología
- Estadísticas básicas (si los datos están cargados)

Para consultas más específicas, intenta:
- Cargar los archivos CSV en la carpeta `data/`
- Configurar GOOGLE_API_KEY en los Secrets de Streamlit

¿Hay algo específico sobre el observatorio que quieras saber?"""
        
        return response
    
    def get_data_summary(self) -> str:
        """Retorna resumen de datos disponibles"""
        if self.data_loaded:
            return self.data_processor.get_summary()
        else:
            return "⚠️ No hay datos cargados. Agrega archivos CSV en la carpeta 'data/'."
