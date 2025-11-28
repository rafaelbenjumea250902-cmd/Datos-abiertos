import streamlit as st
import streamlit.components.v1 as components
from chatbot.llm_handler import ChatbotHandler

# Configuración de la página
st.set_page_config(
    page_title="Observatorio de Seguridad - Santander",
    page_icon="🏛️",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# CSS Moderno Tipo Portal
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&family=Poppins:wght@600;700&display=swap');
    
    :root {
        --primary: #1e3a8a;
        --primary-light: #3b82f6;
        --secondary: #dc2626;
        --accent: #f59e0b;
        --success: #10b981;
        --bg-main: #f8fafc;
        --bg-card: #ffffff;
        --text-primary: #1e293b;
        --text-secondary: #64748b;
        --border: #e2e8f0;
        --shadow-sm: 0 1px 2px 0 rgb(0 0 0 / 0.05);
        --shadow-md: 0 4px 6px -1px rgb(0 0 0 / 0.1);
        --shadow-lg: 0 10px 15px -3px rgb(0 0 0 / 0.1);
        --shadow-xl: 0 20px 25px -5px rgb(0 0 0 / 0.1);
    }
    
    * {
        font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif;
    }
    
    /* Background */
    .main {
        background: var(--bg-main);
        padding: 0 !important;
    }
    
    .stApp {
        background: var(--bg-main);
    }
    
    /* Hide Streamlit branding */
    #MainMenu, footer, header, .stDeployButton { 
        visibility: hidden; 
    }
    
    /* ========== HEADER MODERNO ========== */
    .modern-header {
        background: linear-gradient(135deg, var(--primary) 0%, #1e40af 100%);
        padding: 0;
        margin: -6rem -6rem 0 -6rem;
        box-shadow: var(--shadow-lg);
        position: sticky;
        top: 0;
        z-index: 1000;
    }
    
    .header-top {
        background: rgba(0, 0, 0, 0.1);
        padding: 0.5rem 0;
        border-bottom: 1px solid rgba(255, 255, 255, 0.1);
    }
    
    .header-top-content {
        max-width: 1400px;
        margin: 0 auto;
        padding: 0 2rem;
        display: flex;
        justify-content: space-between;
        align-items: center;
        font-size: 0.75rem;
        color: rgba(255, 255, 255, 0.9);
    }
    
    .header-main {
        max-width: 1400px;
        margin: 0 auto;
        padding: 1.25rem 2rem;
        display: grid;
        grid-template-columns: auto 1fr auto;
        gap: 2rem;
        align-items: center;
    }
    
    .logo-section {
        display: flex;
        align-items: center;
        gap: 1rem;
    }
    
    .logo-icon {
        width: 50px;
        height: 50px;
        background: var(--accent);
        border-radius: 10px;
        display: flex;
        align-items: center;
        justify-content: center;
        font-size: 1.5rem;
        box-shadow: var(--shadow-md);
    }
    
    .logo-text {
        color: white;
    }
    
    .logo-title {
        font-family: 'Poppins', sans-serif;
        font-size: 1.25rem;
        font-weight: 700;
        margin: 0;
        line-height: 1.2;
    }
    
    .logo-subtitle {
        font-size: 0.75rem;
        opacity: 0.9;
        font-weight: 400;
    }
    
    .nav-menu {
        display: flex;
        gap: 2rem;
        align-items: center;
    }
    
    .nav-item {
        color: white;
        text-decoration: none;
        font-weight: 500;
        font-size: 0.875rem;
        transition: all 0.2s;
        padding: 0.5rem 0;
        border-bottom: 2px solid transparent;
    }
    
    .nav-item:hover {
        border-bottom-color: var(--accent);
        opacity: 1;
    }
    
    .header-cta {
        background: var(--accent);
        color: var(--primary);
        padding: 0.625rem 1.5rem;
        border-radius: 6px;
        font-weight: 600;
        font-size: 0.875rem;
        border: none;
        cursor: pointer;
        transition: all 0.2s;
        box-shadow: var(--shadow-md);
    }
    
    .header-cta:hover {
        transform: translateY(-2px);
        box-shadow: var(--shadow-lg);
    }
    
    /* ========== HERO SECTION ========== */
    .hero-section {
        background: linear-gradient(135deg, #1e3a8a 0%, #1e40af 50%, #3b82f6 100%);
        color: white;
        padding: 4rem 2rem;
        margin: 0 -6rem 3rem -6rem;
        position: relative;
        overflow: hidden;
    }
    
    .hero-section::before {
        content: '';
        position: absolute;
        top: 0;
        left: 0;
        right: 0;
        bottom: 0;
        background: url('data:image/svg+xml,<svg width="100" height="100" xmlns="http://www.w3.org/2000/svg"><rect width="100" height="100" fill="none"/><circle cx="50" cy="50" r="1" fill="white" opacity="0.1"/></svg>');
        opacity: 0.3;
    }
    
    .hero-content {
        max-width: 1400px;
        margin: 0 auto;
        position: relative;
        z-index: 1;
    }
    
    .hero-title {
        font-family: 'Poppins', sans-serif;
        font-size: clamp(2rem, 5vw, 3.5rem);
        font-weight: 700;
        margin-bottom: 1rem;
        line-height: 1.1;
    }
    
    .hero-subtitle {
        font-size: clamp(1rem, 2vw, 1.25rem);
        opacity: 0.95;
        max-width: 700px;
        line-height: 1.6;
        font-weight: 300;
    }
    
    /* ========== STATS CARDS ========== */
    .stats-grid {
        display: grid;
        grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
        gap: 1.5rem;
        margin: -3rem 0 3rem 0;
        position: relative;
        z-index: 10;
    }
    
    .stat-card {
        background: var(--bg-card);
        border-radius: 12px;
        padding: 1.75rem;
        box-shadow: var(--shadow-xl);
        border: 1px solid var(--border);
        transition: all 0.3s ease;
        position: relative;
        overflow: hidden;
    }
    
    .stat-card::before {
        content: '';
        position: absolute;
        top: 0;
        left: 0;
        width: 4px;
        height: 100%;
        background: var(--primary-light);
        transition: width 0.3s ease;
    }
    
    .stat-card:hover {
        transform: translateY(-4px);
        box-shadow: var(--shadow-xl), 0 0 0 1px var(--primary-light);
    }
    
    .stat-card:hover::before {
        width: 100%;
        opacity: 0.05;
    }
    
    .stat-icon {
        width: 48px;
        height: 48px;
        background: linear-gradient(135deg, var(--primary-light), var(--primary));
        border-radius: 10px;
        display: flex;
        align-items: center;
        justify-content: center;
        font-size: 1.5rem;
        margin-bottom: 1rem;
        box-shadow: var(--shadow-md);
    }
    
    .stat-value {
        font-family: 'Poppins', sans-serif;
        font-size: 2.25rem;
        font-weight: 700;
        color: var(--text-primary);
        line-height: 1;
        margin-bottom: 0.5rem;
    }
    
    .stat-label {
        font-size: 0.875rem;
        color: var(--text-secondary);
        font-weight: 500;
        text-transform: uppercase;
        letter-spacing: 0.5px;
    }
    
    .stat-change {
        font-size: 0.75rem;
        color: var(--success);
        font-weight: 600;
        margin-top: 0.5rem;
        display: inline-flex;
        align-items: center;
        gap: 0.25rem;
    }
    
    /* ========== CONTENT GRID (Magazine Layout) ========== */
    .content-grid {
        display: grid;
        grid-template-columns: 2fr 1fr;
        gap: 2rem;
        margin-bottom: 3rem;
    }
    
    @media (max-width: 1024px) {
        .content-grid {
            grid-template-columns: 1fr;
        }
    }
    
    /* ========== CARDS MODERNAS ========== */
    .card {
        background: var(--bg-card);
        border-radius: 12px;
        box-shadow: var(--shadow-md);
        border: 1px solid var(--border);
        overflow: hidden;
        transition: all 0.3s ease;
    }
    
    .card:hover {
        box-shadow: var(--shadow-lg);
        transform: translateY(-2px);
    }
    
    .card-header {
        padding: 1.5rem;
        border-bottom: 1px solid var(--border);
        background: linear-gradient(to bottom, var(--bg-card), var(--bg-main));
    }
    
    .card-title {
        font-family: 'Poppins', sans-serif;
        font-size: 1.25rem;
        font-weight: 600;
        color: var(--text-primary);
        margin: 0;
        display: flex;
        align-items: center;
        gap: 0.75rem;
    }
    
    .card-icon {
        width: 32px;
        height: 32px;
        background: linear-gradient(135deg, var(--primary-light), var(--primary));
        border-radius: 8px;
        display: flex;
        align-items: center;
        justify-content: center;
        color: white;
        font-size: 1rem;
    }
    
    .card-body {
        padding: 1.5rem;
    }
    
    .card-feature {
        background: var(--bg-main);
        padding: 1rem;
        border-radius: 8px;
        margin-bottom: 0.75rem;
        border-left: 3px solid var(--primary-light);
        transition: all 0.2s;
    }
    
    .card-feature:hover {
        background: white;
        border-left-color: var(--accent);
        transform: translateX(4px);
    }
    
    .feature-title {
        font-weight: 600;
        color: var(--text-primary);
        margin-bottom: 0.25rem;
        font-size: 0.875rem;
    }
    
    .feature-text {
        font-size: 0.8125rem;
        color: var(--text-secondary);
        line-height: 1.5;
    }
    
    /* ========== CHAT SECTION ========== */
    .chat-container {
        background: var(--bg-card);
        border-radius: 12px;
        box-shadow: var(--shadow-lg);
        border: 1px solid var(--border);
        overflow: hidden;
        height: 600px;
        display: flex;
        flex-direction: column;
    }
    
    .chat-header {
        background: linear-gradient(135deg, var(--primary), var(--primary-light));
        color: white;
        padding: 1.25rem;
        display: flex;
        align-items: center;
        gap: 1rem;
    }
    
    .chat-avatar {
        width: 40px;
        height: 40px;
        background: var(--accent);
        border-radius: 50%;
        display: flex;
        align-items: center;
        justify-content: center;
        font-size: 1.25rem;
    }
    
    .chat-info h3 {
        margin: 0;
        font-size: 1rem;
        font-weight: 600;
    }
    
    .chat-info p {
        margin: 0;
        font-size: 0.75rem;
        opacity: 0.9;
    }
    
    .chat-messages {
        flex: 1;
        overflow-y: auto;
        padding: 1.5rem;
        background: var(--bg-main);
    }
    
    /* Mensajes del chat */
    .stChatMessage {
        background: var(--bg-card);
        border-radius: 12px;
        padding: 1rem;
        margin-bottom: 1rem;
        border: 1px solid var(--border);
        box-shadow: var(--shadow-sm);
    }
    
    .stChatMessage[data-testid="user-message"] {
        background: linear-gradient(135deg, var(--primary-light), var(--primary));
        color: white;
        border: none;
        margin-left: 2rem;
    }
    
    .stChatMessage[data-testid="user-message"] p,
    .stChatMessage[data-testid="user-message"] div {
        color: white !important;
    }
    
    .stChatMessage[data-testid="assistant-message"] {
        background: var(--bg-card);
        margin-right: 2rem;
    }
    
    .stChatMessage p,
    .stChatMessage div {
        color: var(--text-primary) !important;
        line-height: 1.6;
    }
    
    /* ========== ALERT BANNER ========== */
    .alert-banner {
        background: linear-gradient(135deg, var(--secondary), #ef4444);
        color: white;
        padding: 1rem 1.5rem;
        border-radius: 10px;
        margin-bottom: 2rem;
        display: flex;
        align-items: center;
        gap: 1rem;
        box-shadow: var(--shadow-md);
    }
    
    .alert-icon {
        font-size: 1.5rem;
        animation: pulse 2s infinite;
    }
    
    @keyframes pulse {
        0%, 100% { opacity: 1; }
        50% { opacity: 0.7; }
    }
    
    .alert-content h4 {
        margin: 0 0 0.25rem 0;
        font-weight: 600;
        font-size: 1rem;
    }
    
    .alert-content p {
        margin: 0;
        font-size: 0.875rem;
        opacity: 0.95;
    }
    
    /* ========== POWER BI IFRAME ========== */
    iframe {
        border-radius: 10px;
        border: 1px solid var(--border);
        box-shadow: var(--shadow-md);
    }
    
    /* ========== INPUT FIELDS ========== */
    .stTextInput input {
        border: 2px solid var(--border);
        border-radius: 8px;
        padding: 0.75rem 1rem;
        font-size: 0.875rem;
        transition: all 0.2s;
    }
    
    .stTextInput input:focus {
        border-color: var(--primary-light);
        box-shadow: 0 0 0 3px rgba(59, 130, 246, 0.1);
        outline: none;
    }
    
    /* ========== RESPONSIVE ========== */
    @media (max-width: 768px) {
        .header-main {
            grid-template-columns: 1fr;
            gap: 1rem;
        }
        
        .nav-menu {
            display: none;
        }
        
        .stats-grid {
            grid-template-columns: 1fr;
        }
        
        .stChatMessage[data-testid="user-message"],
        .stChatMessage[data-testid="assistant-message"] {
            margin-left: 0;
            margin-right: 0;
        }
    }
    
    /* ========== ANIMATIONS ========== */
    @keyframes fadeIn {
        from {
            opacity: 0;
            transform: translateY(20px);
        }
        to {
            opacity: 1;
            transform: translateY(0);
        }
    }
    
    .card, .stat-card {
        animation: fadeIn 0.5s ease-out;
    }
    
    /* ========== SCROLLBAR ========== */
    ::-webkit-scrollbar {
        width: 8px;
        height: 8px;
    }
    
    ::-webkit-scrollbar-track {
        background: var(--bg-main);
    }
    
    ::-webkit-scrollbar-thumb {
        background: var(--border);
        border-radius: 4px;
    }
    
    ::-webkit-scrollbar-thumb:hover {
        background: var(--text-secondary);
    }
    </style>
""", unsafe_allow_html=True)

# Header Moderno
st.markdown("""
    <div class="modern-header">
        <div class="header-top">
            <div class="header-top-content">
                <div>📅 Actualizado: Noviembre 2024</div>
                <div>📞 Línea de Emergencias: 123</div>
            </div>
        </div>
        <div class="header-main">
            <div class="logo-section">
                <div class="logo-icon">🏛️</div>
                <div class="logo-text">
                    <h1 class="logo-title">Observatorio de Seguridad</h1>
                    <p class="logo-subtitle">Gobernación de Santander</p>
                </div>
            </div>
            <nav class="nav-menu">
                <a href="#" class="nav-item">Inicio</a>
                <a href="#" class="nav-item">Estadísticas</a>
                <a href="#" class="nav-item">Predicciones</a>
                <a href="#" class="nav-item">Municipios</a>
            </nav>
            <button class="header-cta">📊 Ver Reportes</button>
        </div>
    </div>
""", unsafe_allow_html=True)

# Hero Section
st.markdown("""
    <div class="hero-section">
        <div class="hero-content">
            <h2 class="hero-title">Sistema Inteligente de Análisis de Seguridad Ciudadana</h2>
            <p class="hero-subtitle">Información en tiempo real, análisis predictivo y herramientas de inteligencia artificial para la toma de decisiones en seguridad pública del departamento de Santander.</p>
        </div>
    </div>
""", unsafe_allow_html=True)

# Stats Cards
col1, col2, col3, col4 = st.columns(4)

with col1:
    st.markdown("""
        <div class="stat-card">
            <div class="stat-icon">🏘️</div>
            <div class="stat-value">87</div>
            <div class="stat-label">Municipios</div>
            <div class="stat-change">↗ Cobertura total</div>
        </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown("""
        <div class="stat-card">
            <div class="stat-icon">📊</div>
            <div class="stat-value">1.2M+</div>
            <div class="stat-label">Registros</div>
            <div class="stat-change">↗ Datos históricos</div>
        </div>
    """, unsafe_allow_html=True)

with col3:
    st.markdown("""
        <div class="stat-card">
            <div class="stat-icon">🎯</div>
            <div class="stat-value">3</div>
            <div class="stat-label">Modelos ML</div>
            <div class="stat-change">↗ Predicción activa</div>
        </div>
    """, unsafe_allow_html=True)

with col4:
    st.markdown("""
        <div class="stat-card">
            <div class="stat-icon">📈</div>
            <div class="stat-value">94%</div>
            <div class="stat-label">Precisión</div>
            <div class="stat-change">↗ Modelos validados</div>
        </div>
    """, unsafe_allow_html=True)

# Alert Banner
st.markdown("""
    <div class="alert-banner">
        <div class="alert-icon">🚨</div>
        <div class="alert-content">
            <h4>Líneas de Emergencia</h4>
            <p>Policía Nacional: 123 | Bomberos: 119 | Cruz Roja: 132 | Defensa Civil: 144</p>
        </div>
    </div>
""", unsafe_allow_html=True)

# Content Grid
col_main, col_side = st.columns([2, 1])

with col_main:
    # Power BI Card
    st.markdown("""
        <div class="card">
            <div class="card-header">
                <h3 class="card-title">
                    <span class="card-icon">📊</span>
                    Dashboard Interactivo
                </h3>
            </div>
            <div class="card-body">
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
            <div style="background: var(--bg-main); padding: 3rem; border-radius: 8px; text-align: center;">
                <div style="font-size: 3rem; margin-bottom: 1rem;">📊</div>
                <h4 style="color: var(--text-primary); margin-bottom: 0.5rem;">Panel de Análisis Histórico</h4>
                <p style="color: var(--text-secondary); max-width: 500px; margin: 0 auto;">
                    Para visualizar el panel de análisis, ingrese la URL del reporte de Power BI en el campo superior.
                </p>
            </div>
        """, unsafe_allow_html=True)
    
    st.markdown("</div></div>", unsafe_allow_html=True)

with col_side:
    # Chatbot Card
    st.markdown("""
        <div class="chat-container">
            <div class="chat-header">
                <div class="chat-avatar">🤖</div>
                <div class="chat-info">
                    <h3>Asistente Virtual IA</h3>
                    <p>Disponible 24/7 • Respuesta instantánea</p>
                </div>
            </div>
    """, unsafe_allow_html=True)
    
    # Initialize chatbot
    if 'chatbot' not in st.session_state:
        st.session_state.chatbot = ChatbotHandler()
    
    if 'chat_history' not in st.session_state:
        st.session_state.chat_history = []
        # Welcome message
        welcome_msg = "¡Hola! Soy el asistente virtual del Observatorio de Seguridad de Santander. Puedo ayudarte con estadísticas, predicciones y análisis de seguridad. ¿Qué necesitas saber?"
        st.session_state.chat_history.append({"role": "assistant", "content": welcome_msg})
    
    # Display chat messages
    for message in st.session_state.chat_history:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])
    
    # Chat input
    if user_input := st.chat_input("Escribe tu pregunta aquí..."):
        st.session_state.chat_history.append({"role": "user", "content": user_input})
        with st.chat_message("user"):
            st.markdown(user_input)
        
        with st.chat_message("assistant"):
            with st.spinner("Procesando..."):
                response = st.session_state.chatbot.get_response(user_input)
                st.markdown(response)
                st.session_state.chat_history.append({"role": "assistant", "content": response})
    
    st.markdown("</div>", unsafe_allow_html=True)

# Features Grid
st.markdown("<br>", unsafe_allow_html=True)

col1, col2, col3 = st.columns(3)

with col1:
    st.markdown("""
        <div class="card">
            <div class="card-header">
                <h3 class="card-title">
                    <span class="card-icon">🎯</span>
                    Predicciones ML
                </h3>
            </div>
            <div class="card-body">
                <div class="card-feature">
                    <div class="feature-title">Zonas de Riesgo</div>
                    <div class="feature-text">Identificación de áreas críticas mediante algoritmos de aprendizaje automático</div>
                </div>
                <div class="card-feature">
                    <div class="feature-title">Tendencias Temporales</div>
                    <div class="feature-text">Análisis de patrones de criminalidad por horarios y fechas</div>
                </div>
                <div class="card-feature">
                    <div class="feature-title">Alertas Tempranas</div>
                    <div class="feature-text">Sistema de notificación proactiva de situaciones de riesgo</div>
                </div>
            </div>
        </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown("""
        <div class="card">
            <div class="card-header">
                <h3 class="card-title">
                    <span class="card-icon">📈</span>
                    Análisis de Datos
                </h3>
            </div>
            <div class="card-body">
                <div class="card-feature">
                    <div class="feature-title">Big Data Processing</div>
                    <div class="feature-text">Procesamiento de más de 1.2 millones de registros históricos</div>
                </div>
                <div class="card-feature">
                    <div class="feature-title">Visualización Interactiva</div>
                    <div class="feature-text">Dashboards dinámicos con Power BI para análisis detallado</div>
                </div>
                <div class="card-feature">
                    <div class="feature-title">Reportes Automatizados</div>
                    <div class="feature-text">Generación automática de informes periódicos y personalizados</div>
                </div>
            </div>
        </div>
    """, unsafe_allow_html=True)

with col3:
    st.markdown("""
        <div class="card">
            <div class="card-header">
                <h3 class="card-title">
                    <span class="card-icon">🤖</span>
                    Inteligencia Artificial
                </h3>
            </div>
            <div class="card-body">
                <div class="card-feature">
                    <div class="feature-title">Chatbot Especializado</div>
                    <div class="feature-text">Asistente virtual 24/7 con conocimiento del sistema</div>
                </div>
                <div class="card-feature">
                    <div class="feature-title">NLP Avanzado</div>
                    <div class="feature-text">Procesamiento de lenguaje natural para consultas complejas</div>
                </div>
                <div class="card-feature">
                    <div class="feature-title">Aprendizaje Continuo</div>
                    <div class="feature-text">Mejora constante basada en nuevos datos y patrones</div>
                </div>
            </div>
        </div>
    """, unsafe_allow_html=True)
