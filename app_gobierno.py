import streamlit as st

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

st.markdown("""
    <div style="padding: 2rem; text-align: center;">
        <h2>Contenido temporal</h2>
        <p>Aquí irá el resto de la página paso por paso</p>
    </div>
""", unsafe_allow_html=True)
