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
        
        # Archivos de predicciones
        self.predicciones_zona_df = None
        self.predicciones_bucaramanga_df = None
        
        # Archivos históricos (NUEVOS)
        self.historicos_general_df = None
        self.historicos_bucaramanga_df = None
        
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
            # ========== PREDICCIONES ==========
            
            # Archivo 1: Predicciones por zona y tipo
            zona_path = os.path.join(self.data_dir, "001 predicciones_zona_tipo_SIN_FUGA.csv")
            if os.path.exists(zona_path):
                self.predicciones_zona_df = pd.read_csv(zona_path, encoding='utf-8-sig')
                print(f"✅ Predicciones por zona: {len(self.predicciones_zona_df)} registros")
            
            # Archivo 2: Predicciones Bucaramanga
            bga_pred_path = os.path.join(self.data_dir, "predicciones_riesgo_bucaramanga_20251126_005322.csv")
            if os.path.exists(bga_pred_path):
                self.predicciones_bucaramanga_df = pd.read_csv(bga_pred_path, encoding='utf-8-sig')
                print(f"✅ Predicciones Bucaramanga: {len(self.predicciones_bucaramanga_df)} registros")
            
            # ========== HISTÓRICOS (NUEVOS) ==========
            
            # Archivo 3: Históricos generales (con género y días)
            general_path = os.path.join(self.data_dir, "001 General.csv")
            if os.path.exists(general_path):
                self.historicos_general_df = pd.read_csv(general_path, encoding='utf-8-sig')
                print(f"✅ Históricos generales: {len(self.historicos_general_df)} registros")
            
            # Archivo 4: Históricos Bucaramanga (con género y días)
            bga_hist_path = os.path.join(self.data_dir, "datos_historicos_bucaramanga_20251126_005322.csv")
            if os.path.exists(bga_hist_path):
                self.historicos_bucaramanga_df = pd.read_csv(bga_hist_path, encoding='utf-8-sig')
                print(f"✅ Históricos Bucaramanga: {len(self.historicos_bucaramanga_df)} registros")
            
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
            zonas_aumento = []
            zonas_disminucion = []
            
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
                                zonas_aumento.append(zona)
                            elif cambio_porcentual > 0:
                                tendencia = f"aumento leve ({int(cambio_porcentual)}%)"
                                zonas_aumento.append(zona)
                            elif cambio_porcentual < -10:
                                tendencia = f"disminución significativa ({int(abs(cambio_porcentual))}%)"
                                zonas_disminucion.append(zona)
                            elif cambio_porcentual < 0:
                                tendencia = f"disminución leve ({int(abs(cambio_porcentual))}%)"
                                zonas_disminucion.append(zona)
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
            
            # Agregar resumen de tendencias
            context["predicciones_zonas"]["zonas_con_aumento"] = zonas_aumento
            context["predicciones_zonas"]["zonas_con_disminucion"] = zonas_disminucion
            
            # Calcular tendencia general (promedio)
            total_cambios = len(zonas_aumento) - len(zonas_disminucion)
            if total_cambios > 0:
                context["predicciones_zonas"]["tendencia_general"] = "aumento leve"
            elif total_cambios < 0:
                context["predicciones_zonas"]["tendencia_general"] = "disminución leve"
            else:
                context["predicciones_zonas"]["tendencia_general"] = "estable"
        
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
        
        # ========== DATOS HISTÓRICOS (NUEVO) ==========
        
        # Análisis de históricos generales (con género y días)
        if self.historicos_general_df is not None:
            df = self.historicos_general_df
            
            context["historicos_general"] = {
                "total_registros": len(df),
                "periodo": f"{df['AÑO'].min()}-{df['AÑO'].max()}" if 'AÑO' in df.columns else "N/A",
                
                # Análisis por GÉNERO
                "victimas_por_genero": df['GENERO'].value_counts().to_dict() if 'GENERO' in df.columns else {},
                
                # Días más peligrosos (general)
                "dias_mas_delitos": df['NOMBRE_DIA'].value_counts().head(7).to_dict() if 'NOMBRE_DIA' in df.columns else {},
                
                # Género por tipo de delito (top 3 delitos)
                "genero_por_delito": {}
            }
            
            # Análisis género por tipo de delito
            if 'TIPO_DELITO' in df.columns and 'GENERO' in df.columns:
                top_delitos = df['TIPO_DELITO'].value_counts().head(3).index
                for delito in top_delitos:
                    df_delito = df[df['TIPO_DELITO'] == delito]
                    context["historicos_general"]["genero_por_delito"][delito] = df_delito['GENERO'].value_counts().to_dict()
            
            # Análisis por ZONA (días y género)
            context["analisis_por_zona"] = {}
            for zona in df['ZONA'].unique() if 'ZONA' in df.columns else []:
                df_zona = df[df['ZONA'] == zona]
                context["analisis_por_zona"][zona] = {
                    "total_delitos": len(df_zona),
                    "dias_mas_delitos": df_zona['NOMBRE_DIA'].value_counts().head(3).to_dict() if 'NOMBRE_DIA' in df_zona.columns else {},
                    "genero_mas_afectado": df_zona['GENERO'].value_counts().idxmax() if 'GENERO' in df_zona.columns and len(df_zona) > 0 else "N/A",
                    "porcentaje_genero": round((df_zona['GENERO'].value_counts().iloc[0] / len(df_zona) * 100), 1) if 'GENERO' in df_zona.columns and len(df_zona) > 0 else 0
                }
        
        # Análisis de históricos Bucaramanga
        if self.historicos_bucaramanga_df is not None:
            df = self.historicos_bucaramanga_df
            
            context["historicos_bucaramanga"] = {
                "total_registros": len(df),
                
                # Días más peligrosos
                "dias_mas_delitos": df['DIA_SEMANA'].value_counts().head(7).to_dict() if 'DIA_SEMANA' in df.columns else {},
                
                # Género más afectado
                "victimas_por_genero": df['GENERO'].value_counts().to_dict() if 'GENERO' in df.columns else {},
                
                # Fin de semana vs días laborales
                "fin_semana_vs_laboral": {
                    "fin_semana": len(df[df['ES_FIN_SEMANA'] == 1]) if 'ES_FIN_SEMANA' in df.columns else 0,
                    "dias_laborales": len(df[df['ES_FIN_SEMANA'] == 0]) if 'ES_FIN_SEMANA' in df.columns else 0
                }
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
            
            # TENDENCIA GENERAL DEL DEPARTAMENTO
            if 'tendencia_general' in pz:
                context_str += f"\n⚠️ TENDENCIA GENERAL SANTANDER: {pz['tendencia_general']}\n"
                if pz.get('zonas_con_aumento'):
                    context_str += f"Zonas con aumento: {', '.join(pz['zonas_con_aumento'])}\n"
                if pz.get('zonas_con_disminucion'):
                    context_str += f"Zonas con disminución: {', '.join(pz['zonas_con_disminucion'])}\n"
            
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
        
        # ========== DATOS HISTÓRICOS (NUEVO) ==========
        
        # Históricos generales con género y días
        if "historicos_general" in self.context_data:
            hg = self.context_data["historicos_general"]
            context_str += f"""
─────────────────────────────────────────────────────────────
📊 DATOS HISTÓRICOS GENERALES (TODO SANTANDER)
─────────────────────────────────────────────────────────────
Total de registros: {hg['total_registros']:,}
Período: {hg['periodo']}

VÍCTIMAS POR GÉNERO:
"""
            for genero, cant in hg['victimas_por_genero'].items():
                porcentaje = (cant / hg['total_registros'] * 100)
                context_str += f"• {genero}: {porcentaje:.1f}%\n"
            
            context_str += "\nDÍAS CON MÁS DELITOS:\n"
            for dia, cant in hg['dias_mas_delitos'].items():
                context_str += f"• {dia}: {cant:,} delitos\n"
            
            if hg['genero_por_delito']:
                context_str += "\nGÉNERO MÁS AFECTADO POR TIPO DE DELITO:\n"
                for delito, generos in hg['genero_por_delito'].items():
                    genero_principal = max(generos, key=generos.get)
                    context_str += f"• {delito}: {genero_principal}\n"
        
        # Análisis por zona (con días y género)
        if "analisis_por_zona" in self.context_data:
            context_str += "\n─── ANÁLISIS POR ZONA (Género y Días) ───\n"
            for zona, datos in self.context_data["analisis_por_zona"].items():
                context_str += f"\n{zona}:\n"
                context_str += f"  Género más afectado: {datos['genero_mas_afectado']} ({datos['porcentaje_genero']}%)\n"
                if datos['dias_mas_delitos']:
                    dias_top = list(datos['dias_mas_delitos'].keys())[:3]
                    context_str += f"  Días con más delitos: {', '.join(dias_top)}\n"
        
        # Históricos Bucaramanga
        if "historicos_bucaramanga" in self.context_data:
            hb = self.context_data["historicos_bucaramanga"]
            context_str += f"""
─────────────────────────────────────────────────────────────
📍 DATOS HISTÓRICOS - BUCARAMANGA
─────────────────────────────────────────────────────────────
Total de registros: {hb['total_registros']:,}

VÍCTIMAS POR GÉNERO:
"""
            for genero, cant in hb['victimas_por_genero'].items():
                porcentaje = (cant / hb['total_registros'] * 100)
                context_str += f"• {genero}: {porcentaje:.1f}%\n"
            
            context_str += "\nDÍAS CON MÁS DELITOS:\n"
            for dia, cant in list(hb['dias_mas_delitos'].items())[:7]:
                context_str += f"• {dia}: {cant:,} delitos\n"
            
            if hb['fin_semana_vs_laboral']['fin_semana'] > 0:
                total = hb['fin_semana_vs_laboral']['fin_semana'] + hb['fin_semana_vs_laboral']['dias_laborales']
                pct_finde = (hb['fin_semana_vs_laboral']['fin_semana'] / total * 100)
                context_str += f"\nFin de semana: {pct_finde:.1f}% de los delitos\n"
        
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
