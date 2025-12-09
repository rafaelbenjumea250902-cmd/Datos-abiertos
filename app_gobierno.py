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

# CSS del Portal Gubernamental
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Montserrat:wght@400;600;700&family=Open+Sans:wght@300;400;600&display=swap');
    
    * {
        margin: 0;
        padding: 0;
        box-sizing: border-box;
    }
    
    /* Ocultar branding Streamlit */
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
    
    /* Eliminar padding de columns en estadísticas */
    [data-testid="column"] {
        padding: 0 !important;
    }
    
    /* Eliminar espacio vertical entre bloques */
    [data-testid="stVerticalBlock"] > div {
        gap: 0 !important;
    }
    
    [data-testid="stVerticalBlock"] {
        gap: 0 !important;
    }
    
    /* Forzar sin margin en elementos principales */
    .element-container {
        margin: 0 !important;
    }
    
    /* ========== HEADER/NAVEGACIÓN ========== */
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
        max-width: 1400px;
        margin: 0 auto;
        display: flex;
        align-items: center;
        justify-content: space-between;
    }
    
    .logo-section {
        display: flex;
        align-items: center;
        gap: 1rem;
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
    }
    
    .nav-link {
        color: #4b5563;
        text-decoration: none;
        font-family: 'Montserrat', sans-serif;
        font-weight: 500;
        font-size: 0.95rem;
        padding: 0.5rem 0;
        transition: all 0.2s ease;
        cursor: pointer;
        border-bottom: 2px solid transparent;
    }
    
    .nav-link:hover {
        color: #003d82;
        border-bottom: 2px solid #003d82;
    }
    
    .nav-cta {
        background: #ff6b35;
        color: white !important;
        padding: 0.6rem 1.5rem !important;
        border-radius: 50px;
        border: none !important;
        font-weight: 600;
    }
    
    .nav-cta:hover {
        background: #e55a28;
        transform: translateY(-2px);
        box-shadow: 0 4px 12px rgba(255,107,53,0.3);
    }
    
    /* ========== HERO/CARRUSEL ========== */
    .hero-section {
        background: #ffffff;
        padding: 4rem 2rem;
        text-align: center;
        border-bottom: 1px solid #e0e0e0;
    }
    
    .hero-content {
        max-width: 900px;
        margin: 0 auto;
    }
    
    .hero-content h1 {
        font-family: 'Montserrat', sans-serif;
        font-size: 3rem;
        font-weight: 700;
        margin-bottom: 1rem;
        line-height: 1.2;
        color: #003d82;
    }
    
    .hero-content p {
        font-family: 'Open Sans', sans-serif;
        font-size: 1.3rem;
        margin-bottom: 2rem;
        color: #1a1a1a;
    }
    
    .hero-button {
        display: inline-block;
        background: #ffd700;
        color: #003d82;
        padding: 1rem 2.5rem;
        border-radius: 50px;
        text-decoration: none;
        font-family: 'Montserrat', sans-serif;
        font-weight: 600;
        font-size: 1.1rem;
        transition: all 0.3s ease;
        box-shadow: 0 4px 15px rgba(255,215,0,0.3);
        cursor: pointer;
        border: none;
    }
    
    .hero-button:hover {
        transform: translateY(-3px);
        box-shadow: 0 6px 20px rgba(255,215,0,0.4);
    }
    
    /* ========== SECCIONES ========== */
    .section {
        padding: 3rem 2rem 2rem;
        max-width: 1400px;
        margin: 0 auto;
    }
    
    .section.estadisticas-section {
        padding: 3rem 0 0 0;
        max-width: 100%;
    }
    
    .section-title {
        font-family: 'Montserrat', sans-serif;
        font-size: 2.5rem;
        font-weight: 700;
        color: #003d82;
        margin-bottom: 1rem;
        text-align: center;
    }
    
    .section-subtitle {
        font-family: 'Open Sans', sans-serif;
        font-size: 1.1rem;
        color: #666;
        text-align: center;
        margin-bottom: 2rem;
        max-width: 700px;
        margin-left: auto;
        margin-right: auto;
    }
    
    /* ========== ESTADÍSTICAS (Dashboard + Chat) ========== */
    .estadisticas-container {
        width: 100%;
        max-width: 100%;
        padding: 0;
        margin: 0;
    }
    
    .estadisticas-grid {
        display: grid;
        grid-template-columns: 70% 30%;
        gap: 0;
        width: 100%;
        margin: 0;
        padding: 0;
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
        border-radius: 0;
        box-shadow: none;
        display: block;
    }
    
    .chat-sidebar {
        background: white;
        border-left: 1px solid #e0e0e0;
        border-radius: 0;
        height: 1300px;
        display: flex;
        flex-direction: column;
        box-shadow: none;
        margin: 0;
        padding: 0;
    }
    
    .chat-header {
        background: linear-gradient(135deg, #003d82, #0056b3);
        color: white;
        padding: 1rem;
        border-radius: 8px 8px 0 0;
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
    
    /* ========== PORTAL DE DATOS ========== */
    .datos-grid {
        display: grid;
        grid-template-columns: repeat(auto-fit, minmax(280px, 1fr));
        gap: 2rem;
        margin-top: 3rem;
    }
    
    .dato-card {
        background: white;
        border: 2px solid #e0e0e0;
        border-radius: 12px;
        padding: 2rem;
        text-align: center;
        transition: all 0.3s ease;
        cursor: pointer;
        text-decoration: none;
        color: inherit;
        display: block;
    }
    
    .dato-card:hover {
        transform: translateY(-5px);
        box-shadow: 0 8px 25px rgba(0,61,130,0.15);
        border-color: #0056b3;
    }
    
    .dato-card-icon {
        font-size: 3rem;
        margin-bottom: 1rem;
    }
    
    .dato-card h3 {
        font-family: 'Montserrat', sans-serif;
        font-size: 1.2rem;
        color: #003d82;
        margin-bottom: 0.5rem;
    }
    
    .dato-card p {
        font-family: 'Open Sans', sans-serif;
        font-size: 0.9rem;
        color: #666;
    }
    
    /* ========== RUTAS DE ATENCIÓN ========== */
    .rutas-container {
        text-align: center;
        padding: 2rem;
        background: #f8f9fa;
        border-radius: 12px;
    }
    
    .rutas-container img {
        max-width: 100%;
        height: auto;
        border-radius: 8px;
        box-shadow: 0 4px 15px rgba(0,0,0,0.1);
    }
    
    /* ========== FORMULARIO ========== */
    .form-container {
        max-width: 600px;
        margin: 0 auto;
        background: #f8f9fa;
        padding: 2.5rem;
        border-radius: 12px;
        box-shadow: 0 2px 15px rgba(0,0,0,0.05);
    }
    
    .stTextInput input, .stTextArea textarea {
        border-radius: 8px !important;
        border: 1px solid #ddd !important;
        padding: 0.75rem !important;
        font-family: 'Open Sans', sans-serif !important;
    }
    
    .stTextInput input:focus, .stTextArea textarea:focus {
        border-color: #0056b3 !important;
        box-shadow: 0 0 0 2px rgba(0,86,179,0.1) !important;
    }
    
    .stButton button {
        background: linear-gradient(135deg, #003d82, #0056b3) !important;
        color: white !important;
        border-radius: 50px !important;
        padding: 0.75rem 2.5rem !important;
        font-family: 'Montserrat', sans-serif !important;
        font-weight: 600 !important;
        border: none !important;
        width: 100% !important;
    }
    
    .stButton button:hover {
        transform: translateY(-2px);
        box-shadow: 0 4px 15px rgba(0,61,130,0.3) !important;
    }
    
    /* ========== FOOTER ========== */
    .footer {
        background: #1a1a1a;
        color: white;
        padding: 3rem 2rem 1rem;
        margin-top: 4rem;
    }
    
    .footer-content {
        max-width: 1400px;
        margin: 0 auto;
        display: grid;
        grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
        gap: 2rem;
        margin-bottom: 2rem;
    }
    
    .footer h4 {
        font-family: 'Montserrat', sans-serif;
        color: #ffd700;
        margin-bottom: 1rem;
    }
    
    .footer p, .footer a {
        font-family: 'Open Sans', sans-serif;
        color: #ccc;
        text-decoration: none;
        line-height: 1.8;
    }
    
    .footer a:hover {
        color: #ffd700;
    }
    
    .footer-bottom {
        text-align: center;
        padding-top: 2rem;
        border-top: 1px solid #333;
        font-size: 0.9rem;
        color: #999;
    }
    
    /* Mensajes del chat */
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
    
    /* Responsive */
    @media (max-width: 768px) {
        .estadisticas-grid {
            grid-template-columns: 1fr;
        }
        
        .hero-content h1 {
            font-size: 2rem;
        }
        
        .nav-menu {
            flex-direction: column;
            gap: 0.5rem;
        }
    }
    </style>
""", unsafe_allow_html=True)

# JavaScript para navegación suave
st.markdown("""
    <script>
    function scrollToSection(sectionId) {
        const element = document.getElementById(sectionId);
        if (element) {
            element.scrollIntoView({ behavior: 'smooth', block: 'start' });
        }
    }
    </script>
""", unsafe_allow_html=True)

# ========== HEADER/NAVEGACIÓN ==========
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
                <a class="nav-link nav-cta" href="#opinion">Cuéntanos tu Opinión</a>
            </nav>
        </div>
    </div>
""", unsafe_allow_html=True)

# ========== SECCIÓN: INICIO (HERO/CARRUSEL) ==========
st.markdown('<div id="inicio"></div>', unsafe_allow_html=True)

st.markdown("""
    <div class="hero-section">
        <div class="hero-content">
            <h1>Observatorio de Seguridad de Santander</h1>
            <p>Análisis de datos para un departamento más seguro</p>
            <a href="#estadisticas" class="hero-button">Ver Estadísticas</a>
        </div>
    </div>
""", unsafe_allow_html=True)

# ========== SECCIÓN: ESTADÍSTICAS (DASHBOARD + CHATBOT) ==========
st.markdown('<div id="estadisticas"></div>', unsafe_allow_html=True)

# Dashboard y chat SIN título - directo
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
    
    # Inicializar chatbot
    if 'chatbot' not in st.session_state:
        st.session_state.chatbot = ChatbotHandler()
    
    if 'chat_history' not in st.session_state:
        st.session_state.chat_history = []
    
    # Avatares
    LUPITA_AVATAR = "assets/lupita.png"
    USER_AVATAR = "assets/user-avatar.png"
    
    # Header del chat
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
    
    # Container con mensajes
    chat_container = st.container(height=1200)
    
    with chat_container:
        # Mensaje de bienvenida
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
        
        # Mostrar historial
        for message in st.session_state.chat_history:
            if message["role"] == "assistant":
                with st.chat_message(message["role"], avatar=LUPITA_AVATAR):
                    st.markdown(message["content"])
            else:
                with st.chat_message(message["role"], avatar=USER_AVATAR):
                    st.markdown(message["content"])
    
    # Input del chat
    if user_input := st.chat_input("Escribe tu consulta aquí..."):
        st.session_state.chat_history.append({"role": "user", "content": user_input})
        
        with st.spinner(""):
            response = st.session_state.chatbot.get_response(user_input)
            st.session_state.chat_history.append({"role": "assistant", "content": response})
        
        st.rerun()
    
    st.markdown('</div>', unsafe_allow_html=True)

# ========== SECCIÓN: PORTAL DE DATOS ==========
st.markdown('<div id="portal-datos"></div>', unsafe_allow_html=True)
st.markdown("""
    <div class="section">
        <h2 class="section-title">Portal de Datos Abiertos</h2>
        <p class="section-subtitle">
            Los datos utilizados en este observatorio provienen de Datos Abiertos Colombia, 
            garantizando transparencia y acceso público a la información.
        </p>
        <div class="datos-grid">
            <a href="https://www.datos.gov.co/Seguridad-y-Defensa/Reporte-Delitos-sexuales-Polic-a-Nacional/fpe5-yrmw/about_data" 
               target="_blank" class="dato-card">
                <div class="dato-card-icon">📊</div>
                <h3>Delitos Sexuales</h3>
                <p>Reportes de la Policía Nacional</p>
            </a>
            <a href="https://www.datos.gov.co/Seguridad-y-Defensa/Reporte-Hurto-por-Modalidades-Polic-a-Nacional/6sqw-8cg5/about_data" 
               target="_blank" class="dato-card">
                <div class="dato-card-icon">🚨</div>
                <h3>Hurto por Modalidades</h3>
                <p>Datos por tipo de hurto</p>
            </a>
            <a href="https://www.datos.gov.co/Seguridad-y-Defensa/Reporte-Delito-Violencia-Intrafamiliar-Polic-a-Nac/vuyt-mqpw/about_data" 
               target="_blank" class="dato-card">
                <div class="dato-card-icon">🏠</div>
                <h3>Violencia Intrafamiliar</h3>
                <p>Reportes de violencia doméstica</p>
            </a>
            <a href="https://www.datos.gov.co/Seguridad-y-Defensa/40Delitos-ocurridos-en-el-Municipio-de-Bucaramanga/75fz-q98y/about_data" 
               target="_blank" class="dato-card">
                <div class="dato-card-icon">🏙️</div>
                <h3>Delitos en Bucaramanga</h3>
                <p>Datos específicos del municipio</p>
            </a>
        </div>
    </div>
""", unsafe_allow_html=True)

# ========== SECCIÓN: RUTAS DE ATENCIÓN ==========
st.markdown('<div id="rutas"></div>', unsafe_allow_html=True)
st.markdown("""
    <div class="section">
        <h2 class="section-title">Rutas de Atención</h2>
        <p class="section-subtitle">Información sobre cómo reportar delitos y acceder a servicios de ayuda</p>
        <div class="rutas-container">
            <p style="padding: 4rem; background: #f0f0f0; border-radius: 8px; color: #666;">
                📋 Imagen de Rutas de Atención<br>
                <small>(Placeholder - Reemplazar con imagen real)</small>
            </p>
        </div>
    </div>
""", unsafe_allow_html=True)

# ========== SECCIÓN: CUÉNTANOS TU OPINIÓN ==========
st.markdown('<div id="opinion"></div>', unsafe_allow_html=True)
st.markdown("""
    <div class="section">
        <h2 class="section-title">Cuéntanos tu Opinión</h2>
        <p class="section-subtitle">Tu retroalimentación nos ayuda a mejorar los servicios de seguridad</p>
    </div>
""", unsafe_allow_html=True)

# Formulario
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

# ========== FOOTER ==========
st.markdown("""
    <div class="footer">
        <div class="footer-content">
            <div>
                <h4>Gobernación de Santander</h4>
                <p>Calle 37 No. 10-30<br>
                Bucaramanga, Santander<br>
                Teléfono: (607) 6XX XXXX<br>
                Email: contacto@santander.gov.co</p>
            </div>
            <div>
                <h4>Enlaces Útiles</h4>
                <p><a href="#inicio">Inicio</a><br>
                <a href="#estadisticas">Estadísticas</a><br>
                <a href="#portal-datos">Portal de Datos</a><br>
                <a href="#rutas">Rutas de Atención</a></p>
            </div>
            <div>
                <h4>Redes Sociales</h4>
                <p>
                Facebook: @GobSantander<br>
                Twitter: @GobSantander<br>
                Instagram: @gobsantander
                </p>
            </div>
            <div>
                <h4>Horario de Atención</h4>
                <p>Lunes a Viernes<br>
                8:00 AM - 12:00 PM<br>
                2:00 PM - 6:00 PM</p>
            </div>
        </div>
        <div class="footer-bottom">
            <p>© 2025 Gobernación de Santander - Observatorio de Seguridad | Todos los derechos reservados</p>
        </div>
    </div>
""", unsafe_allow_html=True)
