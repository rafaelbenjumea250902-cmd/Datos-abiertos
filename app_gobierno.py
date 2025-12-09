import streamlit as st
import streamlit.components.v1 as components
from chatbot.llm_handler import ChatbotHandler

st.set_page_config(
    page_title="Observatorio de Seguridad - Santander",
    page_icon="🏛️",
    layout="wide",
    initial_sidebar_state="collapsed"
)

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
        margin: 0 !important;
    }
    
    .block-container {
        padding: 0 !important;
        margin: 0 !important;
        max-width: 100% !important;
    }
    
    .header-container {
        background: white;
        padding: 1rem 2rem;
        position: sticky;
        top: 0;
        z-index: 1000;
        box-shadow: 0 2px 8px rgba(0,0,0,0.08);
        border-bottom: 1px solid #e5e7eb;
    }
    
    .header-content {
        max-width: 100%;
        margin: 0 auto;
        display: grid;
        grid-template-columns: 1fr 1fr;
        align-items: center;
        gap: 2rem;
    }
    
    .logo-section {
        display: flex;
        align-items: center;
        gap: 1rem;
        justify-self: start;
    }
    
    .logo-section img {
        height: 50px;
        width: auto;
    }
    
    .logo-text {
        font-family: 'Montserrat', sans-serif;
    }
    
    .logo-text h1 {
        font-size: 1.1rem;
        font-weight: 700;
        margin: 0;
        line-height: 1.2;
        color: #003d82;
    }
    
    .logo-text p {
        font-size: 0.8rem;
        margin: 0;
        color: #6b7280;
    }
    
    .nav-menu {
        display: flex;
        gap: 2rem;
        align-items: center;
        justify-self: end;
    }
    
    .nav-cta-container {
        display: inline-block;
    }
    
    .nav-link {
        color: #4b5563;
        text-decoration: none;
        font-family: 'Montserrat', sans-serif;
        font-weight: 500;
        font-size: 1.56rem;
        padding: 0.5rem 0;
        transition: all 0.2s ease;
        cursor: pointer;
        border-bottom: 2px solid transparent;
        white-space: nowrap;
    }
    
    .nav-link:hover {
        color: #003d82;
        border-bottom: 2px solid #003d82;
    }
    
    .nav-cta {
        background: #ff6b35;
        color: white !important;
        padding: 1rem 2.5rem !important;
        border-radius: 50px;
        border: none !important;
        font-weight: 600;
        font-size: 1.56rem;
        text-decoration: none;
        display: inline-block;
        transition: all 0.3s ease;
    }
    
    .nav-cta:hover {
        background: #e55a28;
        transform: translateY(-2px);
        box-shadow: 0 4px 12px rgba(255,107,53,0.3);
        border-bottom: none !important;
    }
    
    /* ========== DASHBOARD Y CHATBOT ========== */
    [data-testid="column"] {
        padding: 0 !important;
    }
    
    .dashboard-container {
        width: 100%;
        height: 1300px;
        margin: 0;
        padding: 0;
    }
    
    .dashboard-container iframe {
        width: 100%;
        height: 1300px;
        border: none;
        display: block;
    }
    
    .chat-sidebar {
        background: white;
        border-left: 1px solid #e0e0e0;
        height: 1300px;
        display: flex;
        flex-direction: column;
        margin: 0;
        padding: 0;
    }
    
    .chat-header {
        background: linear-gradient(135deg, #003d82, #0056b3);
        color: white;
        padding: 1rem;
        display: flex;
        justify-content: space-between;
        align-items: center;
    }
    
    .chat-header h3 {
        font-family: 'Montserrat', sans-serif;
        font-size: 1rem;
        margin: 0;
    }
    
    .chat-header p {
        font-size: 0.8rem;
        opacity: 0.9;
        margin: 0;
    }
    
    .stChatMessage {
        background: #f8f9fa;
        border-radius: 12px;
        padding: 0.875rem;
        margin-bottom: 0.5rem;
    }
    
    .stChatMessage[data-testid="user-message"] {
        background: #e3f2fd;
        border: 1px solid #90caf9;
    }
    
    .stChatMessage p {
        color: #1f2937 !important;
        font-family: 'Open Sans', sans-serif;
        line-height: 1.5;
    }
    </style>
""", unsafe_allow_html=True)

st.markdown("""
    <div class="header-container">
        <div class="header-content">
            <div class="logo-section">
                <img src="assets/logo-santander.png" alt="Gobernación de Santander">
                <div class="logo-text">
                    <h1>Observatorio de Seguridad</h1>
                    <p>Gobernación de Santander</p>
                </div>
            </div>
            <nav class="nav-menu">
                <a class="nav-link" href="#inicio">Inicio</a>
                <a class="nav-link" href="#estadisticas">Estadísticas</a>
                <a class="nav-link" href="#portal-datos">Portal de Datos</a>
                <a class="nav-link" href="#rutas">Rutas de Atención</a>
                <a class="nav-cta" href="#opinion">Cuéntanos tu Opinión</a>
            </nav>
        </div>
    </div>
""", unsafe_allow_html=True)

# ========== DASHBOARD + CHATBOT ==========
st.markdown('<div id="estadisticas"></div>', unsafe_allow_html=True)

# ========== DASHBOARD + CHATBOT ==========
st.markdown('<div id="estadisticas"></div>', unsafe_allow_html=True)

col_dashboard, col_chat = st.columns([70, 30], gap="small")

# Dashboard Power BI
with col_dashboard:
    POWER_BI_URL = "https://app.powerbi.com/view?r=eyJrIjoiZGNkYWQ1MzgtMTNhYi00MGNiLWE4MGItYjU3MGNlMjlkNjQ2IiwidCI6ImEyYmE0MzQ1LTc3NjQtNGQyMi1iNmExLTdjZjUyOGYzYjNhNSIsImMiOjR9"
    st.markdown('<div class="dashboard-container">', unsafe_allow_html=True)
    components.iframe(POWER_BI_URL, height=1300, scrolling=False)
    st.markdown('</div>', unsafe_allow_html=True)

# Chatbot Lupita
with col_chat:
    st.markdown('<div class="chat-sidebar">', unsafe_allow_html=True)
    
    if 'chatbot' not in st.session_state:
        st.session_state.chatbot = ChatbotHandler()
    
    if 'chat_history' not in st.session_state:
        st.session_state.chat_history = []
    
    LUPITA_AVATAR = "assets/lupita.png"
    USER_AVATAR = "assets/user-avatar.png"
    
    col_title, col_reset = st.columns([5, 1])
    with col_title:
        st.markdown("""
            <div class="chat-header">
                <div>
                    <h3>💬 Lupita - Asistente Virtual</h3>
                    <p>Observatorio de Seguridad</p>
                </div>
            </div>
        """, unsafe_allow_html=True)
    
    with col_reset:
        if st.button("🔄", help="Reiniciar conversación", key="reset_chat"):
            st.session_state.chat_history = []
            st.rerun()
    
    chat_container = st.container(height=1200)
    
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
    
    if user_input := st.chat_input("Escribe tu consulta aquí..."):
        st.session_state.chat_history.append({"role": "user", "content": user_input})
        
        with st.spinner(""):
            response = st.session_state.chatbot.get_response(user_input)
            st.session_state.chat_history.append({"role": "assistant", "content": response})
        
        st.rerun()
    
    st.markdown('</div>', unsafe_allow_html=True)

st.markdown("""
    <div style="padding: 2rem; text-align: center;">
        <h2>Contenido temporal</h2>
        <p>Aquí irán las demás secciones paso por paso</p>
    </div>
""", unsafe_allow_html=True)
