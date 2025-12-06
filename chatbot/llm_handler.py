from groq import Groq
import os
from typing import List, Dict
from .data_processor import DataProcessor

class ChatbotHandler:
    """
    Maneja las interacciones con Groq usando SOLO datos de CSVs
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
        """Construye el prompt del sistema con instrucciones ESTRICTAS"""
        
        base_prompt = """Eres Lupita, un asistente virtual especializado en análisis de seguridad ciudadana para el Observatorio de Seguridad de Santander, Colombia.

═══════════════════════════════════════════════════════════════
⚠️ REGLAS CRÍTICAS (DEBES SEGUIRLAS SIEMPRE):
═══════════════════════════════════════════════════════════════

1. SOLO usa la información del CONTEXTO DE DATOS que recibes
2. NO inventes números, estadísticas ni información
3. NO uses tu conocimiento general sobre Colombia o Santander
4. Si NO tienes el dato específico en el contexto, di claramente:
   "No tengo esa información específica en los datos disponibles"
5. SIEMPRE cita números exactos del contexto cuando los uses
6. NO hagas suposiciones ni estimaciones

CARACTERÍSTICAS DE TUS RESPUESTAS:
- Respondes en español de manera clara y profesional
- Usas SOLO datos específicos del contexto proporcionado
- Explicas conceptos técnicos de forma accesible
- Eres preciso y citas los números exactos
- Cuando no tienes información específica, lo indicas claramente
- ⚠️ CRÍTICO: Respuestas de MÁXIMO 2 LÍNEAS (muy concisas)
- Ve directo al punto, sin introducciones ni despedidas
- No uses saltos de línea innecesarios

FORMATO DE RESPUESTA:
- Cuando pregunten por un MUNICIPIO específico:
  1. Indica a qué ZONA pertenece
  2. Di si los delitos han AUMENTADO o DISMINUIDO (usa la tendencia)
  3. Menciona el GÉNERO más afectado en esa zona
  4. Menciona los DÍAS MÁS PELIGROSOS de esa zona
  5. Menciona el tipo de delito principal
- NO des cifras exactas de delitos, habla en porcentajes o tendencias
- NO menciones horarios
- Habla en términos de: "aumentó", "disminuyó", "estable", "masculino/femenino más afectado"
- Para Bucaramanga específicamente, puedes mencionar si fin de semana es más peligroso
- Si no tienes datos de género o días, di "No tengo esa información para esa zona"

"""
        
        # Agregar contexto de datos si están cargados
        if self.data_loaded:
            data_context = self.data_processor.get_context_string()
            base_prompt += f"\n{data_context}\n"
        else:
            base_prompt += "\n⚠️ ADVERTENCIA: Los datos aún no están cargados. Informa al usuario que debe cargar los archivos CSV.\n"
        
        base_prompt += """
═══════════════════════════════════════════════════════════════
RECORDATORIO FINAL:
═══════════════════════════════════════════════════════════════
1. Solo responde con información del CONTEXTO DE DATOS de arriba
2. NO uses conocimiento externo. NO inventes datos
3. ⚠️ MÁXIMO 2 LÍNEAS de respuesta - sé ultra conciso
4. Responde DIRECTO sin saludos ni despedidas (excepto en "hola")
"""
        
        return base_prompt
    
    def get_response(self, user_message: str, max_tokens: int = 100) -> str:
        """
        Genera respuesta usando Groq con contexto estricto de datos
        Respuestas MUY CONCISAS (máximo 2 líneas)
        """
        
        if not self.api_available:
            return self._fallback_response(user_message)
        
        try:
            # Construir mensajes con énfasis en usar SOLO el contexto
            messages = [
                {"role": "system", "content": self.system_prompt},
                {"role": "user", "content": user_message}
            ]
            
            # Generar respuesta con Groq
            response = self.client.chat.completions.create(
                model=self.model,
                messages=messages,
                max_tokens=max_tokens,
                temperature=0.3,  # Más bajo = más preciso, menos creativo
                top_p=0.9  # Más conservador
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
        
        # Asegurar que termina en punto
        if response and not response[-1] in ['.', '!', '?']:
            last_period = response.rfind('.')
            if last_period > len(response) * 0.7:
                response = response[:last_period + 1]
        
        return response
    
    def _fallback_response(self, user_message: str) -> str:
        """Respuesta de emergencia cuando el LLM falla"""
        
        user_message_lower = user_message.lower()
        
        if any(word in user_message_lower for word in ['hola', 'buenos días', 'buenas tardes', 'hey']):
            if self.data_loaded:
                return """Hola, soy Lupita, tu asistente virtual para el Observatorio de Seguridad de Santander. Tengo datos de predicciones por zona, tipos de delitos y análisis de riesgo para Bucaramanga. ¿Qué necesitas saber?"""
            else:
                return "Hola, soy Lupita. Los datos aún no están cargados. Verifica que los archivos CSV estén en la carpeta 'data/'."
        
        elif 'datos' in user_message_lower or 'información' in user_message_lower or 'tienes' in user_message_lower:
            return self.get_data_summary()
        
        else:
            if self.data_loaded:
                return """Puedo ayudarte con información específica sobre seguridad en Santander basada en datos reales.

Pregúntame sobre:
- Zonas con más delitos
- Tipos de delitos específicos
- Precisión de las predicciones
- Análisis de riesgo en Bucaramanga
- Patrones temporales (días, horarios)

¿Qué información necesitas?"""
            else:
                return "Para consultas específicas, asegúrate de que GROQ_API_KEY esté configurada y que los archivos CSV estén cargados."
    
    def get_data_summary(self) -> str:
        """Retorna resumen de datos disponibles"""
        if self.data_loaded:
            return self.data_processor.get_summary()
        else:
            return "⚠️ No hay datos cargados. Verifica que los archivos CSV estén en la carpeta 'data/'."
