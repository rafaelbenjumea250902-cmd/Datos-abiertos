import pandas as pd
import os
from typing import List, Dict, Any
import json

class DataProcessor:
    """
    Procesa los datos históricos y de predicciones para alimentar el chatbot
    VERSIÓN MEJORADA: Extrae estadísticas detalladas por zona, tipo, comuna, etc.
    """
    
    def __init__(self, data_dir: str = "data"):
        self.data_dir = data_dir
        self.predicciones_zona_df = None
        self.predicciones_bucaramanga_df = None
        self.context_data = None
        
        # Mapeo de municipios a zonas de Santander
        self.municipio_zona = {
            # Zona Metropolitana
            "bucaramanga": "Metropolitana",
            "floridablanca": "Metropolitana",
            "girón": "Metropolitana",
            "piedecuesta": "Metropolitana",
            
            # Zona Guanentá
            "san gil": "Guanentá",
            "barichara": "Guanentá",
            "villanueva": "Guanentá",
            "curití": "Guanentá",
            "charalá": "Guanentá",
            "páramo": "Guanentá",
            
            # Zona Vélez
            "vélez": "Vélez",
            "barbosa": "Vélez",
            "puente nacional": "Vélez",
            "guavatá": "Vélez",
            "chipatá": "Vélez",
            
            # Zona Soto Norte
            "california": "Soto Norte",
            "vetas": "Soto Norte",
            "suratá": "Soto Norte",
            "matanza": "Soto Norte",
            
            # Zona Yariguíes
            "barrancabermeja": "Yariguíes",
            "puerto wilches": "Yariguíes",
            "sabana de torres": "Yariguíes",
            "san vicente de chucurí": "Yariguíes",
            
            # Zona Comunera
            "socorro": "Comunera",
            "san gil": "Comunera",
            "mogotes": "Comunera",
            "onzaga": "Comunera"
        }
        
    def load_data(self) -> bool:
        """Carga los archivos CSV de datos"""
        try:
            # Archivo 1: Predicciones por zona y tipo
            zona_path = os.path.join(self.data_dir, "001_predicciones_zona_tipo_SIN_FUGA__1_.csv")
            if os.path.exists(zona_path):
                self.predicciones_zona_df = pd.read_csv(zona_path, encoding='utf-8-sig')
                print(f"✅ Predicciones por zona: {len(self.predicciones_zona_df)} registros")
            
            # Archivo 2: Predicciones Bucaramanga
            bga_path = os.path.join(self.data_dir, "predicciones_riesgo_bucaramanga_20251126_005322__1_.csv")
            if os.path.exists(bga_path):
                self.predicciones_bucaramanga_df = pd.read_csv(bga_path, encoding='utf-8-sig')
                print(f"✅ Predicciones Bucaramanga: {len(self.predicciones_bucaramanga_df)} registros")
            
            # Generar contexto detallado para el LLM
            self._generate_context()
            return True
            
        except Exception as e:
            print(f"❌ Error cargando datos: {e}")
            return False
    
    def _generate_context(self):
        """Genera un contexto DETALLADO de los datos para el LLM"""
        context = {
            "descripcion": "Predicciones de seguridad y criminalidad de Santander, Colombia",
            "fuente": "Modelos de Machine Learning - Observatorio de Seguridad",
            "advertencia": "IMPORTANTE: Solo usa la información de este contexto. NO inventes datos."
        }
        
        # Estadísticas del archivo 1: Zonas
        if self.predicciones_zona_df is not None:
            df = self.predicciones_zona_df
            
            # Totales generales
            context["predicciones_zonas"] = {
                "total_registros": len(df),
                "periodo": f"{df['AÑO'].min()}-{df['AÑO'].max()}" if 'AÑO' in df.columns else "N/A",
                
                # Top zonas por delitos reales
                "zonas_mas_delitos": df.groupby('ZONA')['TOTAL_DELITOS_REAL'].sum().sort_values(ascending=False).head(5).to_dict(),
                
                # Top tipos de delito
                "tipos_delito": df.groupby('TIPO_DELITO')['TOTAL_DELITOS_REAL'].sum().sort_values(ascending=False).to_dict(),
                
                # Totales
                "total_delitos_reales": int(df['TOTAL_DELITOS_REAL'].sum()),
                "total_delitos_predichos": int(df['TOTAL_DELITOS_PREDICHO'].sum()),
                
                # Precisión del modelo
                "error_promedio_porcentual": round(df['ERROR_PORCENTUAL'].mean(), 2),
                "error_minimo": round(df['ERROR_PORCENTUAL'].min(), 2),
                "error_maximo": round(df['ERROR_PORCENTUAL'].max(), 2),
                
                # Zonas disponibles
                "zonas": list(df['ZONA'].unique()),
                
                # Años disponibles
                "años": list(df['AÑO'].unique()) if 'AÑO' in df.columns else []
            }
            
            # Estadísticas por zona
            context["detalles_por_zona"] = {}
            for zona in df['ZONA'].unique()[:10]:  # Top 10 zonas
                df_zona = df[df['ZONA'] == zona]
                
                # Calcular tendencia (comparar primer vs último año)
                if 'AÑO' in df.columns:
                    años = sorted(df_zona['AÑO'].unique())
                    if len(años) >= 2:
                        primer_año = df_zona[df_zona['AÑO'] == años[0]]['TOTAL_DELITOS_REAL'].sum()
                        ultimo_año = df_zona[df_zona['AÑO'] == años[-1]]['TOTAL_DELITOS_REAL'].sum()
                        
                        if primer_año > 0:
                            cambio_porcentual = ((ultimo_año - primer_año) / primer_año) * 100
                            if cambio_porcentual > 10:
                                tendencia = f"aumento significativo ({int(cambio_porcentual)}%)"
                            elif cambio_porcentual > 0:
                                tendencia = f"aumento leve ({int(cambio_porcentual)}%)"
                            elif cambio_porcentual < -10:
                                tendencia = f"disminución significativa ({int(abs(cambio_porcentual))}%)"
                            elif cambio_porcentual < 0:
                                tendencia = f"disminución leve ({int(abs(cambio_porcentual))}%)"
                            else:
                                tendencia = "estable"
                        else:
                            tendencia = "sin datos suficientes"
                    else:
                        tendencia = "sin datos suficientes"
                else:
                    tendencia = "sin datos suficientes"
                
                context["detalles_por_zona"][zona] = {
                    "total_delitos": int(df_zona['TOTAL_DELITOS_REAL'].sum()),
                    "delitos_predichos": int(df_zona['TOTAL_DELITOS_PREDICHO'].sum()),
                    "tipos_delito": df_zona.groupby('TIPO_DELITO')['TOTAL_DELITOS_REAL'].sum().to_dict(),
                    "tendencia": tendencia
                }
        
        # Estadísticas del archivo 2: Bucaramanga
        if self.predicciones_bucaramanga_df is not None:
            df = self.predicciones_bucaramanga_df
            
            context["predicciones_bucaramanga"] = {
                "total_registros": len(df),
                
                # Comunas con más riesgo alto
                "comunas_riesgo_alto": df[df['NIVEL_RIESGO'] == 'ALTO'].groupby('COMUNA').size().sort_values(ascending=False).head(5).to_dict(),
                
                # Distribución por nivel de riesgo
                "distribucion_riesgo": df['NIVEL_RIESGO'].value_counts().to_dict(),
                
                # Días con más riesgo alto
                "dias_mas_riesgo": df[df['NIVEL_RIESGO'] == 'ALTO'].groupby('DIA_SEMANA').size().sort_values(ascending=False).to_dict(),
                
                # Horarios con más riesgo alto
                "horarios_mas_riesgo": df[df['NIVEL_RIESGO'] == 'ALTO'].groupby('BLOQUE_HORARIO').size().sort_values(ascending=False).to_dict(),
                
                # Tipos de delito
                "tipos_delito": df['TIPO_DELITO'].unique().tolist(),
                
                # Comunas disponibles
                "comunas": list(df['COMUNA'].unique()),
                
                # Total delitos históricos
                "total_delitos_historicos": int(df['DELITOS_HISTORICOS'].sum())
            }
            
            # Detalles por comuna (top 5)
            context["detalles_por_comuna"] = {}
            top_comunas = df.groupby('COMUNA').size().sort_values(ascending=False).head(5).index
            for comuna in top_comunas:
                df_comuna = df[df['COMUNA'] == comuna]
                context["detalles_por_comuna"][comuna] = {
                    "total_predicciones": len(df_comuna),
                    "riesgo_alto": len(df_comuna[df_comuna['NIVEL_RIESGO'] == 'ALTO']),
                    "riesgo_medio": len(df_comuna[df_comuna['NIVEL_RIESGO'] == 'MEDIO']),
                    "riesgo_bajo": len(df_comuna[df_comuna['NIVEL_RIESGO'] == 'BAJO']),
                    "delitos_historicos": int(df_comuna['DELITOS_HISTORICOS'].sum())
                }
        
        self.context_data = context
    
    def get_context_string(self) -> str:
        """Retorna el contexto como string formateado para el LLM"""
        if self.context_data is None:
            return "No hay datos disponibles."
        
        context_str = f"""
═══════════════════════════════════════════════════════════════
CONTEXTO DE DATOS DEL OBSERVATORIO DE SEGURIDAD DE SANTANDER
═══════════════════════════════════════════════════════════════

⚠️ REGLA CRÍTICA: Solo usa la información de este contexto. 
Si no tienes el dato específico aquí, di "No tengo esa información en los datos disponibles".
NO inventes números ni uses conocimiento general.

Descripción: {self.context_data['descripcion']}
Fuente: {self.context_data['fuente']}

"""
        
        # Datos de predicciones por zona
        if "predicciones_zonas" in self.context_data:
            pz = self.context_data["predicciones_zonas"]
            context_str += f"""
─────────────────────────────────────────────────────────────
📊 PREDICCIONES POR ZONA Y TIPO DE DELITO
─────────────────────────────────────────────────────────────
Total de registros: {pz['total_registros']:,}
Período: {pz['periodo']}

TOTALES:
• Delitos reales: {pz['total_delitos_reales']:,}
• Delitos predichos: {pz['total_delitos_predichos']:,}

PRECISIÓN DEL MODELO:
• Error promedio: {pz['error_promedio_porcentual']}%
• Error mínimo: {pz['error_minimo']}%
• Error máximo: {pz['error_maximo']}%

TOP 5 ZONAS CON MÁS DELITOS:
"""
            for i, (zona, total) in enumerate(pz['zonas_mas_delitos'].items(), 1):
                context_str += f"{i}. {zona}: {int(total):,} delitos\n"
            
            context_str += "\nTIPOS DE DELITO Y TOTALES:\n"
            for tipo, total in pz['tipos_delito'].items():
                context_str += f"• {tipo}: {int(total):,}\n"
            
            context_str += f"\nZonas disponibles: {', '.join(pz['zonas'])}\n"
            context_str += f"Años con datos: {', '.join(map(str, pz['años']))}\n"
            
            # Agregar mapeo municipio → zona
            context_str += "\n─── MUNICIPIOS POR ZONA ───\n"
            zona_municipios = {}
            for municipio, zona in self.municipio_zona.items():
                if zona not in zona_municipios:
                    zona_municipios[zona] = []
                zona_municipios[zona].append(municipio.title())
            
            for zona in sorted(zona_municipios.keys()):
                context_str += f"\n{zona}: {', '.join(sorted(zona_municipios[zona]))}\n"
        
        # Detalles por zona
        if "detalles_por_zona" in self.context_data:
            context_str += "\n─── ESTADÍSTICAS DETALLADAS POR ZONA ───\n"
            for zona, datos in self.context_data["detalles_por_zona"].items():
                context_str += f"\n{zona}:\n"
                context_str += f"  Tendencia: {datos['tendencia']}\n"
                context_str += f"  Delitos principales:\n"
                for tipo, cant in sorted(datos['tipos_delito'].items(), key=lambda x: x[1], reverse=True)[:2]:
                    context_str += f"    • {tipo}: {int(cant)}\n"
        
        # Datos de Bucaramanga
        if "predicciones_bucaramanga" in self.context_data:
            pb = self.context_data["predicciones_bucaramanga"]
            context_str += f"""
─────────────────────────────────────────────────────────────
📍 PREDICCIONES DE RIESGO - BUCARAMANGA
─────────────────────────────────────────────────────────────
Total de predicciones: {pb['total_registros']:,}
Total delitos históricos: {pb['total_delitos_historicos']:,}

DISTRIBUCIÓN DE RIESGO:
"""
            for nivel, cant in pb['distribucion_riesgo'].items():
                context_str += f"• {nivel}: {cant:,} casos\n"
            
            context_str += "\nTOP 5 COMUNAS CON MÁS RIESGO ALTO:\n"
            for i, (comuna, cant) in enumerate(pb['comunas_riesgo_alto'].items(), 1):
                context_str += f"{i}. {comuna}: {cant} casos de riesgo alto\n"
            
            context_str += "\nDÍAS CON MÁS RIESGO ALTO (Solo Bucaramanga):\n"
            for dia, cant in pb['dias_mas_riesgo'].items():
                context_str += f"• {dia}: {cant} casos\n"
        
        # Detalles por comuna
        if "detalles_por_comuna" in self.context_data:
            context_str += "\n─── ESTADÍSTICAS POR COMUNA (TOP 5) ───\n"
            for comuna, datos in self.context_data["detalles_por_comuna"].items():
                context_str += f"\n{comuna}:\n"
                context_str += f"  Riesgo ALTO: {datos['riesgo_alto']}\n"
                context_str += f"  Riesgo MEDIO: {datos['riesgo_medio']}\n"
                context_str += f"  Riesgo BAJO: {datos['riesgo_bajo']}\n"
                context_str += f"  Delitos históricos: {datos['delitos_historicos']}\n"
        
        context_str += "\n═══════════════════════════════════════════════════════════════\n"
        
        return context_str
    
    def get_summary(self) -> str:
        """Retorna resumen general de los datos"""
        if self.context_data is None:
            return "No hay datos cargados."
        
        summary = "📊 RESUMEN DEL SISTEMA:\n\n"
        
        if "predicciones_zonas" in self.context_data:
            pz = self.context_data["predicciones_zonas"]
            summary += f"• Predicciones por zona: {pz['total_registros']:,} registros\n"
            summary += f"• Total delitos analizados: {pz['total_delitos_reales']:,}\n"
        
        if "predicciones_bucaramanga" in self.context_data:
            pb = self.context_data["predicciones_bucaramanga"]
            summary += f"• Predicciones Bucaramanga: {pb['total_registros']:,} registros\n"
        
        summary += "\n✅ Sistema de predicción activo"
        
        return summary
