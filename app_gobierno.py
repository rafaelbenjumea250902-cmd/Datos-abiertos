import streamlit as st
import streamlit.components.v1 as components
from chatbot.llm_handler import ChatbotHandler

st.set_page_config(page_title="Observatorio de Seguridad - Santander", page_icon="🏛️", layout="wide", initial_sidebar_state="collapsed")

if 'chatbot' not in st.session_state:
    st.session_state.chatbot = ChatbotHandler()
if 'chat_history' not in st.session_state:
    st.session_state.chat_history = []

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');

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

/* HEADER MINIMALISTA */
.header-fixed {
    position: fixed;
    top: 0;
    left: 0;
    right: 0;
    background: rgba(255, 255, 255, 0.95);
    backdrop-filter: blur(10px);
    border-bottom: 1px solid #f0f0f0;
    padding: 1rem 3rem;
    display: flex;
    justify-content: space-between;
    align-items: center;
    z-index: 1000;
    box-shadow: 0 1px 3px rgba(0,0,0,0.05);
}

.logo {
    font-family: 'Inter', sans-serif;
    font-weight: 700;
    font-size: 1.1rem;
    color: #1a1a1a;
    letter-spacing: -0.5px;
}

.nav-menu {
    display: flex;
    gap: 2.5rem;
    align-items: center;
}

.nav-link {
    font-family: 'Inter', sans-serif;
    font-weight: 500;
    font-size: 0.95rem;
    color: #666;
    text-decoration: none;
    transition: color 0.2s;
    cursor: pointer;
}

.nav-link:hover {
    color: #1a1a1a;
}

/* SECCIONES */
.section {
    min-height: 100vh;
    padding: 8rem 3rem 4rem;
    scroll-margin-top: 80px;
}

.section-title {
    font-family: 'Inter', sans-serif;
    font-weight: 700;
    font-size: 2.5rem;
    color: #1a1a1a;
    margin-bottom: 1rem;
    letter-spacing: -1px;
}

.section-subtitle {
    font-family: 'Inter', sans-serif;
    font-weight: 400;
    font-size: 1.1rem;
    color: #666;
    margin-bottom: 3rem;
}

/* ESTADÍSTICAS */
.stats-grid {
    display: grid;
    grid-template-columns: 70% 30%;
    gap: 0;
    height: 800px;
}

.dashboard-side {
    background: #fafafa;
    border-right: 1px solid #f0f0f0;
}

.chat-side {
    background: white;
    display: flex;
    flex-direction: column;
}

.chat-header-minimal {
    padding: 1.5rem;
    border-bottom: 1px solid #f0f0f0;
}

.chat-header-minimal h4 {
    font-family: 'Inter', sans-serif;
    font-weight: 600;
    font-size: 1rem;
    color: #1a1a1a;
    margin: 0;
}

.chat-messages-minimal {
    flex: 1;
    overflow-y: auto;
    padding: 1.5rem;
    display: flex;
    flex-direction: column;
    gap: 1rem;
}

.chat-input-minimal {
    padding: 1.5rem;
    border-top: 1px solid #f0f0f0;
}

.stChatMessage {
    background: transparent !important;
    padding: 0 !important;
}

.stChatMessage[data-testid="user-message"] {
    background: #1a1a1a !important;
    color: white !important;
    padding: 0.75rem 1rem !important;
    border-radius: 18px !important;
    border-bottom-right-radius: 4px !important;
    max-width: 80%;
    margin-left: auto;
}

.stChatMessage[data-testid="assistant-message"] {
    background: #f5f5f5 !important;
    padding: 0.75rem 1rem !important;
    border-radius: 18px !important;
    border-bottom-left-radius: 4px !important;
    max-width: 80%;
}

.stChatMessage p {
    font-family: 'Inter', sans-serif !important;
    font-size: 0.95rem !important;
    line-height: 1.5 !important;
    margin: 0 !important;
}

/* PORTAL DE DATOS */
.data-grid {
    display: grid;
    grid-template-columns: repeat(2, 1fr);
    gap: 1.5rem;
    max-width: 900px;
}

.data-card {
    background: #fafafa;
    border: 1px solid #f0f0f0;
    padding: 2rem;
    border-radius: 8px;
    transition: all 0.2s;
    text-decoration: none;
    display: block;
}

.data-card:hover {
    transform: translateY(-2px);
    box-shadow: 0 4px 12px rgba(0,0,0,0.08);
    border-color: #e0e0e0;
}

.data-card-title {
    font-family: 'Inter', sans-serif;
    font-weight: 600;
    font-size: 1.1rem;
    color: #1a1a1a;
    margin-bottom: 0.5rem;
}

.data-card-desc {
    font-family: 'Inter', sans-serif;
    font-size: 0.9rem;
    color: #666;
}

/* RUTAS */
.rutas-image {
    max-width: 100%;
    border-radius: 8px;
    box-shadow: 0 2px 8px rgba(0,0,0,0.1);
}

/* FORMULARIO */
.form-container {
    max-width: 600px;
    background: #fafafa;
    padding: 2.5rem;
    border-radius: 8px;
}

.stTextInput input, .stTextArea textarea, .stSelectbox select {
    border: 1px solid #e0e0e0 !important;
    border-radius: 6px !important;
    padding: 0.75rem !important;
    font-family: 'Inter', sans-serif !important;
    background: white !important;
}

.stTextInput input:focus, .stTextArea textarea:focus, .stSelectbox select:focus {
    border-color: #1a1a1a !important;
    box-shadow: 0 0 0 2px rgba(26,26,26,0.1) !important;
}

.stButton button {
    background: #1a1a1a !important;
    color: white !important;
    border-radius: 6px !important;
    padding: 0.75rem 2rem !important;
    font-family: 'Inter', sans-serif !important;
    font-weight: 600 !important;
    border: none !important;
    width: 100% !important;
    transition: all 0.2s !important;
}

.stButton button:hover {
    background: #000 !important;
    transform: translateY(-1px);
}

/* SMOOTH SCROLL */
html {
    scroll-behavior: smooth;
}

[data-testid="column"] {
    padding: 0 !important;
}
</style>
""", unsafe_allow_html=True)

st.markdown("""
<div class="header-fixed">
    <div class="logo">Observatorio de Seguridad</div>
    <nav class="nav-menu">
        <a class="nav-link" href="#inicio">Inicio</a>
        <a class="nav-link" href="#estadisticas">Estadísticas</a>
        <a class="nav-link" href="#datos">Portal de Datos</a>
        <a class="nav-link" href="#rutas">Rutas de Atención</a>
        <a class="nav-link" href="#opinion">Cuéntanos</a>
    </nav>
</div>
""", unsafe_allow_html=True)

st.markdown('<div class="section" id="inicio">', unsafe_allow_html=True)
st.markdown('<h1 class="section-title">Observatorio de Seguridad de Santander</h1>', unsafe_allow_html=True)
st.markdown('<p class="section-subtitle">Análisis de datos para un departamento más seguro</p>', unsafe_allow_html=True)
st.markdown('</div>', unsafe_allow_html=True)

st.markdown('<div class="section" id="estadisticas">', unsafe_allow_html=True)
st.markdown('<h2 class="section-title">Estadísticas</h2>', unsafe_allow_html=True)
st.markdown('<p class="section-subtitle">Dashboard interactivo y asistente virtual Lupita</p>', unsafe_allow_html=True)

col_dash, col_chat = st.columns([70, 30], gap="small")

with col_dash:
    st.markdown('<div class="dashboard-side">', unsafe_allow_html=True)
    POWER_BI_URL = "https://app.powerbi.com/view?r=eyJrIjoiZGNkYWQ1MzgtMTNhYi00MGNiLWE4MGItYjU3MGNlMjlkNjQ2IiwidCI6ImEyYmE0MzQ1LTc3NjQtNGQyMi1iNmExLTdjZjUyOGYzYjNhNSIsImMiOjR9"
    components.iframe(POWER_BI_URL, height=800, scrolling=False)
    st.markdown('</div>', unsafe_allow_html=True)

with col_chat:
    st.markdown('<div class="chat-side">', unsafe_allow_html=True)
    st.markdown('<div class="chat-header-minimal"><h4>💬 Lupita - Asistente Virtual</h4></div>', unsafe_allow_html=True)
    
    LUPITA_AVATAR = "assets/lupita.png"
    USER_AVATAR = "assets/user-avatar.png"
    
    chat_container = st.container(height=600)
    
    with chat_container:
        if len(st.session_state.chat_history) == 0:
            st.info("👋 Hola, soy Lupita. Pregúntame sobre estadísticas, zonas, tipos de delitos y predicciones de riesgo en Santander.")
        
        for message in st.session_state.chat_history:
            with st.chat_message(message["role"], avatar=LUPITA_AVATAR if message["role"] == "assistant" else USER_AVATAR):
                st.markdown(message["content"])
    
    if user_input := st.chat_input("Escribe tu consulta aquí...", key="chat_input"):
        st.session_state.chat_history.append({"role": "user", "content": user_input})
        with st.spinner(""):
            response = st.session_state.chatbot.get_response(user_input)
            st.session_state.chat_history.append({"role": "assistant", "content": response})
        st.rerun()
    
    st.markdown('</div>', unsafe_allow_html=True)

st.markdown('</div>', unsafe_allow_html=True)

st.markdown('<div class="section" id="datos">', unsafe_allow_html=True)
st.markdown('<h2 class="section-title">Portal de Datos Abiertos</h2>', unsafe_allow_html=True)
st.markdown('<p class="section-subtitle">Datos utilizados del portal de Datos Abiertos Colombia</p>', unsafe_allow_html=True)
st.markdown("""
<div class="data-grid">
    <a href="https://www.datos.gov.co/Seguridad-y-Defensa/Reporte-Delitos-sexuales-Polic-a-Nacional/fpe5-yrmw/about_data" target="_blank" class="data-card">
        <div class="data-card-title">📊 Delitos Sexuales</div>
        <div class="data-card-desc">Reportes de la Policía Nacional</div>
    </a>
    <a href="https://www.datos.gov.co/Seguridad-y-Defensa/Reporte-Hurto-por-Modalidades-Polic-a-Nacional/6sqw-8cg5/about_data" target="_blank" class="data-card">
        <div class="data-card-title">🚨 Hurto por Modalidades</div>
        <div class="data-card-desc">Datos por tipo de hurto</div>
    </a>
    <a href="https://www.datos.gov.co/Seguridad-y-Defensa/Reporte-Delito-Violencia-Intrafamiliar-Polic-a-Nac/vuyt-mqpw/about_data" target="_blank" class="data-card">
        <div class="data-card-title">🏠 Violencia Intrafamiliar</div>
        <div class="data-card-desc">Reportes de violencia doméstica</div>
    </a>
    <a href="https://www.datos.gov.co/Seguridad-y-Defensa/40Delitos-ocurridos-en-el-Municipio-de-Bucaramanga/75fz-q98y/about_data" target="_blank" class="data-card">
        <div class="data-card-title">🏙️ Delitos en Bucaramanga</div>
        <div class="data-card-desc">Datos específicos del municipio</div>
    </a>
</div>
""", unsafe_allow_html=True)
st.markdown('</div>', unsafe_allow_html=True)

st.markdown('<div class="section" id="rutas">', unsafe_allow_html=True)
st.markdown('<h2 class="section-title">Rutas de Atención</h2>', unsafe_allow_html=True)
st.markdown('<p class="section-subtitle">Información sobre cómo reportar delitos y acceder a servicios de ayuda</p>', unsafe_allow_html=True)
st.image("assets/rutas-atencion.png", use_container_width=True)
st.markdown('</div>', unsafe_allow_html=True)

st.markdown('<div class="section" id="opinion">', unsafe_allow_html=True)
st.markdown('<h2 class="section-title">Cuéntanos tu Opinión</h2>', unsafe_allow_html=True)
st.markdown('<p class="section-subtitle">Tu retroalimentación nos ayuda a mejorar</p>', unsafe_allow_html=True)
st.markdown('<div class="form-container">', unsafe_allow_html=True)

with st.form("opinion_form"):
    nombre = st.text_input("Nombre completo *")
    email = st.text_input("Correo electrónico *")
    municipio = st.selectbox("Municipio *", [
        "Selecciona tu municipio",
        "Bucaramanga", "Floridablanca", "Girón", "Piedecuesta",
        "Barichara", "San Gil", "Socorro", "Vélez",
        "Barrancabermeja", "Otro"
    ])
    mensaje = st.text_area("Mensaje *", height=150, placeholder="Escribe aquí tus comentarios o sugerencias...")
    
    submitted = st.form_submit_button("Enviar Opinión")
    
    if submitted:
        if nombre and email and municipio != "Selecciona tu municipio" and mensaje:
            st.success("✅ ¡Gracias por tu opinión! Tu mensaje ha sido enviado correctamente.")
        else:
            st.error("⚠️ Por favor completa todos los campos marcados con *")

st.markdown('</div>', unsafe_allow_html=True)
st.markdown('</div>', unsafe_allow_html=True)
