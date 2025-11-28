import streamlit as st
import streamlit.components.v1 as components
from chatbot.llm_handler import ChatbotHandler

# Configuración de la página
st.set_page_config(
    page_title="Sistema de Información de Seguridad Ciudadana - Gobernación de Santander",
    page_icon="🏛️",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# CSS Profesional Gubernamental
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');
    
    :root {
        --gold: #D4AF37;
        --gold-light: #E8D7A0;
        --gold-dark: #B8960A;
        --red: #C41E3A;
        --green: #2C6E49;
        --green-light: #4A9D6F;
        --primary: #2C3E50;
        --secondary: #34495E;
        --white: #FFFFFF;
        --light-gray: #F8F9FA;
        --gray: #E9ECEF;
        --text: #2C3E50;
        --text-light: #6C757D;
    }
    
    * {
        font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif;
    }
    
    /* Background */
    .main {
        background: var(--light-gray);
        color: var(--text);
    }
    
    .stApp {
        background: var(--light-gray);
    }
    
    /* Hide Streamlit elements */
    #MainMenu, footer, header, .stDeployButton { visibility: hidden; }
    
    /* Government Header */
    .gov-header {
        background: linear-gradient(135deg, var(--primary) 0%, var(--secondary) 100%);
        color: var(--white);
        padding: 1rem 0;
        margin: -6rem -6rem 2rem -6rem;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
    }
    
    .gov-header-content {
        max-width: 1400px;
        margin: 0 auto;
        padding: 0 1.5rem;
        display: flex;
        align-items: center;
        gap: 1rem;
    }
    
    .gov-logo {
        font-size: 1rem;
        font-weight: 600;
        text-transform: uppercase;
        letter-spacing: 0.5px;
    }
    
    .gov-divider {
        height: 30px;
        width: 1px;
        background: rgba(255, 255, 255, 0.3);
    }
    
    .gov-title {
        font-size: 0.9rem;
        font-weight: 400;
        opacity: 0.95;
    }
    
    /* Page Header */
    .page-header {
        background: var(--white);
        padding: 2rem 1.5rem;
        margin: -1rem -6rem 2rem -6rem;
        box-shadow: 0 1px 3px rgba(0, 0, 0, 0.08);
        border-bottom: 3px solid var(--gold);
    }
    
    .page-title {
        font-size: clamp(1.75rem, 4vw, 2.5rem);
        font-weight: 700;
        color: var(--primary);
        margin-bottom: 0.5rem;
        line-height: 1.2;
    }
    
    .page-subtitle {
        font-size: 1.1rem;
        color: var(--text-light);
        font-weight: 400;
        max-width: 800px;
    }
    
    /* Metrics */
    [data-testid="stMetricValue"] {
        font-size: 2rem;
        font-weight: 700;
        color: var(--gold-dark);
    }
    
    [data-testid="stMetricLabel"] {
        font-size: 0.85rem;
        color: var(--text-light);
        text-transform: uppercase;
        letter-spacing: 0.5px;
        font-weight: 500;
    }
    
    [data-testid="stMetricDelta"] {
        font-size: 0.8rem;
    }
    
    .stMetric {
        background: var(--white);
        padding: 1.5rem;
        border-radius: 8px;
        box-shadow: 0 1px 3px rgba(0, 0, 0, 0.08);
        text-align: center;
        border-right: 1px solid var(--gray);
    }
    
    /* Sections */
    .section-container {
        background: var(--white);
        border-radius: 8px;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
        overflow: hidden;
        margin-bottom: 2rem;
    }
    
    .section-header {
        background: linear-gradient(to right, var(--gold-light), var(--gold));
        padding: 1.5rem;
        border-bottom: 3px solid var(--gold-dark);
    }
    
    .section-title {
        font-size: 1.25rem;
        font-weight: 600;
        color: var(--primary);
        margin: 0;
    }
    
    .section-description {
        font-size: 0.9rem;
        color: var(--text-light);
        margin-top: 0.5rem;
    }
    
    .section-content {
        padding: 1.5rem;
    }
    
    /* Chat Section */
    .chat-header {
        background: linear-gradient(to right, var(--green-light), var(--green));
        padding: 1.5rem;
        border-bottom: 3px solid var(--green);
    }
    
    .chat-title {
        font-size: 1.25rem;
        font-weight: 600;
        color: var(--white);
        margin: 0;
    }
    
    .chat-subtitle {
        font-size: 0.85rem;
        color: rgba(255, 255, 255, 0.9);
        margin-top: 0.5rem;
    }
    
    /* Input Fields */
    .stTextInput input {
        background: var(--white);
        border: 2px solid var(--gray);
        border-radius: 6px;
        padding: 0.75rem;
        color: var(--text);
        font-size: 0.95rem;
        transition: all 0.3s;
    }
    
    .stTextInput input:focus {
        border-color: var(--gold-dark);
        box-shadow: 0 0 0 3px rgba(212, 175, 55, 0.1);
        outline: none;
    }
    
    /* Chat Messages */
    .stChatMessage {
        background: var(--light-gray);
        border-radius: 8px;
        padding: 1rem;
        margin-bottom: 1rem;
        border: 1px solid var(--gray);
    }
    
    .stChatMessage[data-testid="user-message"] {
        background: var(--gold-light);
        border-left: 4px solid var(--gold);
    }
    
    .stChatMessage[data-testid="assistant-message"] {
        background: var(--white);
        border-left: 4px solid var(--green);
    }
    
    /* Buttons */
    .stButton button {
        background: var(--green);
        color: var(--white);
        border: none;
        border-radius: 6px;
        padding: 0.75rem 1.5rem;
        font-weight: 600;
        transition: all 0.3s;
        font-size: 0.95rem;
    }
    
    .stButton button:hover {
        background: var(--green-light);
        transform: translateY(-1px);
        box-shadow: 0 2px 8px rgba(0, 0, 0, 0.15);
    }
    
    /* Info Banner */
    .info-banner {
        background: linear-gradient(135deg, #E85D75 0%, var(--red) 100%);
        color: var(--white);
        padding: 1.5rem;
        border-radius: 6px;
        margin-bottom: 2rem;
    }
    
    .info-banner-title {
        font-size: 1rem;
        font-weight: 600;
        margin-bottom: 0.5rem;
    }
    
    .info-banner-text {
        font-size: 0.9rem;
        opacity: 0.95;
        line-height: 1.6;
    }
    
    /* Footer */
    .footer {
        background: var(--primary);
        color: var(--white);
        padding: 2rem 1.5rem;
        margin: 3rem -6rem -6rem -6rem;
        text-align: center;
    }
    
    .footer-logo {
        font-size: 1.1rem;
        font-weight: 600;
        margin-bottom: 0.5rem;
    }
    
    .footer-text {
        font-size: 0.9rem;
        opacity: 0.9;
        margin-bottom: 0.5rem;
    }
    
    .footer-divider {
        width: 60px;
        height: 2px;
        background: var(--gold);
        margin: 1rem auto;
    }
    
    .footer-credits {
        font-size: 0.85rem;
        opacity: 0.7;
    }
    
    /* Scrollbar */
    ::-webkit-scrollbar {
        width: 8px;
        height: 8px;
    }
    
    ::-webkit-scrollbar-track {
        background: var(--gray);
    }
    
    ::-webkit-scrollbar-thumb {
        background: var(--gold);
        border-radius: 4px;
    }
    </style>
""", unsafe_allow_html=True)

# Inicializar session state
if 'chat_history' not in st.session_state:
    st.session_state.chat_history = []
if 'chatbot_handler' not in st.session_state:
    st.session_state.chatbot_handler = ChatbotHandler()

# Government Header
st.markdown("""
    <div class="gov-header">
        <div class="gov-header-content">
            <div class="gov-logo">Gobernación de Santander</div>
            <div class="gov-divider"></div>
            <div class="gov-title">Secretaría del Interior</div>
        </div>
    </div>
""", unsafe_allow_html=True)

# Page Header
st.markdown("""
    <div class="page-header">
        <h1 class="page-title">Sistema de Información de Seguridad Ciudadana</h1>
        <p class="page-subtitle">
            Herramienta de consulta y análisis de información histórica de seguridad 
            para los 87 municipios del departamento de Santander.
        </p>
    </div>
""", unsafe_allow_html=True)

# Stats
col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric(
        label="Municipios",
        value="87",
        delta="Cobertura departamental"
    )

with col2:
    st.metric(
        label="Registros Históricos",
        value="1M+",
        delta="Datos analizados"
    )

with col3:
    st.metric(
        label="Modelos Predictivos",
        value="3",
        delta="Algoritmos activos"
    )

with col4:
    st.metric(
        label="Actualización",
        value="94%",
        delta="Índice de precisión"
    )

# Info Banner
st.markdown("""
    <div class="info-banner">
        <div class="info-banner-title">Información Importante</div>
        <div class="info-banner-text">
            Este sistema presenta información histórica de seguridad ciudadana. 
            Para reportes de emergencia, comuníquese con la línea 123. 
            Para denuncias, contacte a la Policía Nacional al 112.
        </div>
    </div>
""", unsafe_allow_html=True)

# Main Content Grid
col_dashboard, col_chat = st.columns([2, 1])

with col_dashboard:
    # Dashboard Section
    st.markdown("""
        <div class="section-container">
            <div class="section-header">
                <h2 class="section-title">Panel de Análisis Histórico</h2>
                <p class="section-description">
                    Visualización interactiva de datos históricos de seguridad y criminalidad
                </p>
            </div>
        </div>
    """, unsafe_allow_html=True)
    
    POWER_BI_URL = st.text_input(
        "URL del reporte de Power BI",
        placeholder="Ingrese la URL del reporte de Power BI",
        label_visibility="collapsed"
    )
    
    if POWER_BI_URL and POWER_BI_URL.strip():
        components.iframe(POWER_BI_URL, height=650, scrolling=True)
    else:
        st.markdown("""
            <div style="background: var(--light-gray); border-radius: 6px; padding: 3rem; text-align: center; color: var(--text-light); min-height: 600px; display: flex; align-items: center; justify-content: center;">
                <div>
                    <div style="font-size: 1.2rem; font-weight: 600; color: var(--text); margin-bottom: 1rem;">Panel de Análisis Histórico</div>
                    <div style="font-size: 0.95rem; line-height: 1.8;">
                        Para visualizar el panel de análisis, ingrese la URL del reporte<br>
                        de Power BI en el campo superior.<br><br>
                        El panel mostrará información histórica de criminalidad,<br>
                        estadísticas por municipio y análisis de tendencias.
                    </div>
                </div>
            </div>
        """, unsafe_allow_html=True)

with col_chat:
    # Chatbot Section
    st.markdown("""
        <div class="section-container">
            <div class="chat-header">
                <h2 class="chat-title">Asistente Virtual</h2>
                <p class="chat-subtitle">Consulte información sobre seguridad en su municipio</p>
            </div>
        </div>
    """, unsafe_allow_html=True)
    
    # Initialize with welcome message
    if not st.session_state.chat_history:
        st.session_state.chat_history.append({
            "role": "assistant",
            "content": "Bienvenido al Sistema de Información de Seguridad Ciudadana de Santander. Puede consultarme sobre estadísticas de criminalidad, información por municipio o tendencias de seguridad. ¿En qué puedo ayudarle?"
        })
    
    # Display chat messages
    for message in st.session_state.chat_history:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])
    
    # Chat input
    if prompt := st.chat_input("Escriba su consulta aquí..."):
        st.session_state.chat_history.append({"role": "user", "content": prompt})
        
        with st.chat_message("user"):
            st.markdown(prompt)
        
        with st.chat_message("assistant"):
            with st.spinner("Procesando..."):
                response = st.session_state.chatbot_handler.get_response(prompt)
                st.markdown(response)
        
        st.session_state.chat_history.append({"role": "assistant", "content": response})
        st.rerun()

# Footer
st.markdown("""
    <div class="footer">
        <div class="footer-logo">Gobernación de Santander</div>
        <div class="footer-text">Sistema de Información de Seguridad Ciudadana</div>
        <div class="footer-divider"></div>
        <div class="footer-credits">
            Secretaría del Interior | 2024
        </div>
    </div>
""", unsafe_allow_html=True)
