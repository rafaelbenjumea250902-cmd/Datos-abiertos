import streamlit as st
from chatbot.llm_handler import ChatbotHandler

st.set_page_config(page_title="Observatorio de Seguridad", page_icon="🏛️", layout="wide")

if 'page' not in st.session_state:
    st.session_state.page = 'Inicio'
if 'chatbot' not in st.session_state:
    st.session_state.chatbot = ChatbotHandler()
if 'chat_history' not in st.session_state:
    st.session_state.chat_history = []

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Montserrat:wght@400;600;700&family=Open+Sans:wght@300;400;600&display=swap');

* {
    margin: 0;
    padding: 0;
    box-sizing: border-box;
}

#MainMenu, footer, header, .stDeployButton {
    visibility: hidden;
}

.main {
    background: #ffffff;
    padding: 0 !important;
}

.block-container {
    padding: 0 !important;
    max-width: 100% !important;
}

.header-section {
    background: white;
    padding: 1rem 2rem 0.5rem;
    box-shadow: 0 2px 4px rgba(0,0,0,0.05);
    border-bottom: 1px solid #e5e7eb;
}

.logo-container-center {
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    text-align: center;
}

[data-testid="column"] {
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
}

[data-testid="stImage"] {
    display: flex;
    justify-content: center;
}

.content-section {
    padding: 0;
    margin: 0;
    min-height: calc(100vh - 200px);
    display: flex;
    align-items: center;
    justify-content: center;
}

.estadisticas-container {
    width: 100%;
    max-width: 100%;
}

.dashboard-panel {
    width: 70%;
    height: 100%;
}

.chat-panel {
    width: 30%;
    height: 100%;
    border: 3px solid #003d82 !important;
    display: flex;
    flex-direction: column;
    background: white;
    border-radius: 11px;
    box-shadow: 0 0 0 3px #003d82;
}

.chat-header {
    background: linear-gradient(135deg, #003d82, #0056b3);
    color: white;
    padding: 1rem;
    font-family: 'Montserrat', sans-serif;
    font-weight: 600;
    display: flex;
    justify-content: center;
    align-items: center;
    border-radius: 8px 8px 0 0;
    margin: -3px -3px 0 -3px;
    position: relative;
}

.chat-header h3 {
    font-size: 28px;
    margin: 0;
    color: white;
    text-align: center;
}

.chat-header p {
    font-size: 0.8rem;
    margin: 0;
    color: white;
    opacity: 0.9;
}

.placeholder-content {
    padding: 3rem 2rem;
    text-align: center;
    font-family: 'Montserrat', sans-serif;
}

.stChatMessage {
    background: #f8f9fa;
    border-radius: 11px;
    padding: 0.875rem;
    margin-bottom: 0.5rem;
}

.stChatMessage[data-testid="user-message"] {
    background: #e3f2fd;
    border: 1px solid #90caf9;
    border-radius: 11px;
}

.stChatMessage p {
    color: #1f2937 !important;
    font-family: 'Open Sans', sans-serif;
    line-height: 1.5;
}

.stButton button {
    font-family: 'Montserrat', sans-serif !important;
    font-weight: 400 !important;
    font-size: 0.95rem !important;
    color: #666 !important;
    background: transparent !important;
    border: none !important;
    border-bottom: 2px solid transparent !important;
    border-radius: 0 !important;
    padding: 0.5rem 1rem !important;
    letter-spacing: 0.5px !important;
}

.stButton button:hover {
    color: #1a1a1a !important;
    border-bottom: 2px solid #1a1a1a !important;
    background: transparent !important;
}

iframe {
    border: none !important;
}
</style>
""", unsafe_allow_html=True)

st.markdown('<div class="header-section"><div class="logo-container-center">', unsafe_allow_html=True)

try:
    st.image("assets/logo-santander.png", width=600)
except:
    st.markdown('<h2 style="text-align: center; color: #003d82;">OBSERVATORIO DE SEGURIDAD DE SANTANDER</h2>', unsafe_allow_html=True)

st.markdown('</div></div>', unsafe_allow_html=True)

cols = st.columns(5)
pages = ['Inicio', 'Estadísticas', 'Portal de Datos', 'Rutas de Atención', 'Cuéntanos tu Opinión']
for i, page in enumerate(pages):
    if cols[i].button(page, key=f"nav_{page}", use_container_width=True):
        st.session_state.page = page
        st.rerun()

if st.session_state.page == 'Inicio':
    st.markdown('<div class="placeholder-content"><h2>Bienvenido al Observatorio de Seguridad</h2><p>Selecciona una sección del menú</p></div>', unsafe_allow_html=True)

elif st.session_state.page == 'Estadísticas':
    st.markdown('<div style="padding-top: 5vh;"></div>', unsafe_allow_html=True)
    
    col_dash, col_chat = st.columns([70, 30], gap="small")
    
    with col_dash:
        st.components.v1.iframe("https://app.powerbi.com/view?r=eyJrIjoiZGNkYWQ1MzgtMTNhYi00MGNiLWE4MGItYjU3MGNlMjlkNjQ2IiwidCI6ImEyYmE0MzQ1LTc3NjQtNGQyMi1iNmExLTdjZjUyOGYzYjNhNSIsImMiOjR9", height=1105, scrolling=False)
    
    with col_chat:
        st.markdown('''
            <div style="
                border: 3px solid #003d82; 
                border-radius: 11px; 
                overflow: hidden;
                height: 100%;
                box-sizing: border-box;
                padding: 0;
                margin: 0;
            ">
        ''', unsafe_allow_html=True)
        
        LUPITA_AVATAR = "assets/lupita.png"
        USER_AVATAR = "assets/user-avatar.png"
        
        st.markdown("""
            <div class="chat-header">
                <div>
                    <h3>Lupita - Asistente Virtual</h3>
                </div>
            </div>
        """, unsafe_allow_html=True)
        
        chat_container = st.container(height=949)
        
        with chat_container:
            if len(st.session_state.chat_history) == 0:
                st.markdown("""
                    <div style="background: linear-gradient(135deg, #f0f9ff, #e0f2fe); 
                         border: 1px solid #bae6fd; border-radius: 12px; padding: 1.25rem; 
                         text-align: center; margin: 1rem;">
                        <h4 style="color: #0c4a6e; font-size: 0.95rem; font-weight: 600; margin: 0 0 0.5rem 0;">
                            👋 Hola, soy Lupita
                        </h4>
                        <p style="color: #075985; font-size: 0.8rem; margin: 0; line-height: 1.5;">
                            Tu asistente virtual para el Observatorio de Seguridad de Santander. 
                            Pregúntame sobre estadísticas, zonas, tipos de delitos y predicciones de riesgo.
                        </p>
                    </div>
                """, unsafe_allow_html=True)
            
            for message in st.session_state.chat_history:
                if message["role"] == "assistant":
                    with st.chat_message(message["role"], avatar=LUPITA_AVATAR):
                        st.markdown(message["content"])
                else:
                    with st.chat_message(message["role"], avatar=USER_AVATAR):
                        st.markdown(message["content"])
        
        if user_input := st.chat_input("Escribe tu consulta aquí...", key="chat_input"):
            st.session_state.chat_history.append({"role": "user", "content": user_input})
            
            with st.spinner(""):
                response = st.session_state.chatbot.get_response(user_input)
                st.session_state.chat_history.append({"role": "assistant", "content": response})
            
            st.rerun()
        
        st.markdown('</div>', unsafe_allow_html=True)

elif st.session_state.page == 'Portal de Datos':
    st.markdown('<div class="placeholder-content"><h2>Portal de Datos</h2><p>Contenido próximamente</p></div>', unsafe_allow_html=True)

elif st.session_state.page == 'Rutas de Atención':
    st.markdown('<div style="padding-top: 5vh;"></div>', unsafe_allow_html=True)
    col1, col2, col3 = st.columns([0.05, 0.9, 0.05])
    with col2:
        st.image("assets/rutas-atencion.png", use_column_width=True)

elif st.session_state.page == 'Cuéntanos tu Opinión':
    st.markdown('<div style="padding-top: 10vh;"></div>', unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns([0.15, 0.7, 0.15])
    with col2:
        st.markdown("""
            <div style="text-align: center; margin-bottom: 2rem;">
                <h2 style="font-family: 'Montserrat', sans-serif; font-size: 2rem; color: #003d82; margin-bottom: 0.5rem;">
                    Cuéntanos tu Opinión
                </h2>
                <p style="font-family: 'Open Sans', sans-serif; font-size: 1rem; color: #666;">
                    Tu retroalimentación es importante para mejorar el Observatorio de Seguridad
                </p>
            </div>
        """, unsafe_allow_html=True)
        
        with st.form("formulario_opinion", clear_on_submit=True):
            st.markdown("### Información Personal")
            
            col_nombre, col_email = st.columns(2)
            with col_nombre:
                nombre = st.text_input("Nombre completo *", placeholder="Ej: Juan Pérez")
            with col_email:
                email = st.text_input("Correo electrónico *", placeholder="ejemplo@correo.com")
            
            col_municipio, col_edad = st.columns(2)
            with col_municipio:
                municipio = st.selectbox("Municipio *", [
                    "Selecciona tu municipio",
                    "Bucaramanga",
                    "Floridablanca", 
                    "Girón",
                    "Piedecuesta",
                    "Barrancabermeja",
                    "San Gil",
                    "Socorro",
                    "Vélez",
                    "Barichara",
                    "Otro"
                ])
            with col_edad:
                rango_edad = st.selectbox("Rango de edad", [
                    "Prefiero no decir",
                    "18-25 años",
                    "26-35 años",
                    "36-45 años",
                    "46-55 años",
                    "56-65 años",
                    "Más de 65 años"
                ])
            
            st.markdown("### Evaluación del Observatorio")
            
            col_usabilidad, col_informacion = st.columns(2)
            with col_usabilidad:
                usabilidad = st.select_slider(
                    "¿Qué tan fácil fue navegar en la plataforma?",
                    options=["Muy difícil", "Difícil", "Regular", "Fácil", "Muy fácil"],
                    value="Regular"
                )
            with col_informacion:
                informacion = st.select_slider(
                    "¿La información fue útil?",
                    options=["Nada útil", "Poco útil", "Moderadamente útil", "Útil", "Muy útil"],
                    value="Útil"
                )
            
            chatbot_util = st.radio(
                "¿Utilizaste el asistente virtual Lupita?",
                ["No lo utilicé", "Sí, y fue útil", "Sí, pero no fue útil"],
                horizontal=True
            )
            
            if chatbot_util != "No lo utilicé":
                calificacion_lupita = st.slider(
                    "Califica tu experiencia con Lupita (1-5)",
                    min_value=1,
                    max_value=5,
                    value=3
                )
            
            st.markdown("### Sugerencias y Comentarios")
            
            mejoras = st.multiselect(
                "¿Qué te gustaría ver mejorado? (Puedes seleccionar varias opciones)",
                [
                    "Más datos y estadísticas",
                    "Mejor diseño visual",
                    "Información más actualizada",
                    "Más opciones de filtrado",
                    "Descarga de reportes",
                    "Tutoriales o guías de uso",
                    "Aplicación móvil",
                    "Otro"
                ]
            )
            
            comentarios = st.text_area(
                "Comentarios adicionales",
                placeholder="Cuéntanos qué piensas sobre el Observatorio de Seguridad...",
                height=150
            )
            
            col_privacidad, col_submit = st.columns([3, 1])
            with col_privacidad:
                acepta_terminos = st.checkbox(
                    "Acepto que mis datos sean procesados según la política de privacidad",
                    value=False
                )
            
            with col_submit:
                submitted = st.form_submit_button("Enviar", use_container_width=True)
            
            if submitted:
                if not nombre or not email or municipio == "Selecciona tu municipio":
                    st.error("⚠️ Por favor completa todos los campos obligatorios (*)")
                elif not acepta_terminos:
                    st.error("⚠️ Debes aceptar la política de privacidad para continuar")
                else:
                    st.success("✅ ¡Gracias por tu opinión! Tu retroalimentación ha sido enviada correctamente.")
                    st.balloons()
