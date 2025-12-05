from groq import Groq
import os
from typing import List, Dict
from .data_processor import DataProcessor

class ChatbotHandler:
    """
    Maneja las interacciones con Groq usando datos de CSVs (sin RAG pesado)
    """
    
    def __init__(self):
        # Cargar datos de CSVs
        self.data_processor = DataProcessor()
        self.data_loaded = self.data_processor.load_data()
        
        # Configurar Groq
        api_key = os.getenv("GROQ_API_KEY")
        
        if api_key:
            self.client = Groq(api_key=api_key)
            self.model = "llama-3.3-70b-versatile"
            self.api_available = True
        else:
            self.api_available = False
            print("⚠️ GROQ_API_KEY no configurada")
        
        # Sistema de prompts con datos
        self.system_prompt = self._build_system_prompt()
        
    def _build_system_prompt(self) -> str:
        """Construye el prompt del sistema con datos de CSVs"""
        
        base_prompt = """Eres un asistente virtual especializado en análisis de seguridad ciudadana para el Observatorio de Seguridad de Santander, Colombia.

CARACTERÍSTICAS:
- Respondes en español de manera clara y profesional
- Usas datos específicos de los contextos proporcionados
- Explicas conceptos técnicos de forma accesible
- Eres preciso y citas datos cuando están disponibles

INSTRUCCIONES:
1. SIEMPRE usa los datos del contexto cuando estén disponibles
2. Si el contexto tiene información relevante, úsala en tu respuesta
3. Si no hay datos en el contexto, indícalo claramente
4. Mantén respuestas CONCISAS (máximo 2-3 párrafos)
5. Ve directo al punto

"""
        
        # Agregar contexto de datos si están cargados
        if self.data_loaded:
            data_context = self.data_processor.get_context_string()
            base_prompt += f"\n{data_context}\n"
        else:
            base_prompt += "\nNOTA: Los datos aún no están cargados.\n"
        
        base_prompt += "\nResponde de manera útil, directa y basada en datos."
        
        return base_prompt
    
    def get_response(self, user_message: str, max_tokens: int = 300) -> str:
        """
        Genera respuesta usando Groq con contexto de datos
        """
        
        if not self.api_available:
            return self._fallback_response(user_message)
        
        try:
            # Construir mensajes
            messages = [
                {"role": "system", "content": self.system_prompt},
                {"role": "user", "content": user_message}
            ]
            
            # Generar respuesta con Groq
            response = self.client.chat.completions.create(
                model=self.model,
                messages=messages,
                max_tokens=max_tokens,
                temperature=0.7,
                top_p=0.95
            )
            
            # Obtener texto de respuesta
            if response.choices and response.choices[0].message.content:
                cleaned_response = self._clean_response(response.choices[0].message.content)
                return cleaned_response
            else:
                return self._fallback_response(user_message)
            
        except Exception as e:
            print(f"❌ Error con Groq: {e}")
            return self._fallback_response(user_message)
    
    def _clean_response(self, response: str) -> str:
        """Limpia y formatea la respuesta"""
        response = response.strip()
        
        if response and not response[-1] in ['.', '!', '?']:
            last_period = response.rfind('.')
            if last_period > len(response) * 0.7:
                response = response[:last_period + 1]
        
        return response
    
    def _fallback_response(self, user_message: str) -> str:
        """Respuesta de emergencia cuando el LLM falla"""
        
        user_message_lower = user_message.lower()
        
        if any(word in user_message_lower for word in ['hola', 'buenos días', 'buenas tardes', 'hey']):
            return """¡Hola! Soy el asistente del Observatorio de Seguridad de Santander.

Puedo ayudarte con:
- Estadísticas de criminalidad
- Información por municipio
- Análisis de datos históricos
- Predicciones de seguridad

¿Qué necesitas saber?"""
        
        else:
            return """Gracias por tu pregunta. Para consultas específicas, asegúrate de que GROQ_API_KEY esté configurada en los Secrets de Streamlit.

¿Hay algo específico sobre el observatorio que quieras saber?"""
    
    def get_data_summary(self) -> str:
        """Retorna resumen de datos disponibles"""
        if self.data_loaded:
            return self.data_processor.get_summary()
        else:
            return "⚠️ No hay datos cargados."
