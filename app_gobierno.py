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

# CSS Minimalista
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600&display=swap');
    
    * {
        font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif;
    }
    
    /* Ocultar todo el branding de Streamlit */
    #MainMenu, footer, header, .stDeployButton { 
        visibility: hidden; 
    }
    
    /* Fondo blanco limpio */
    .main {
        background: #ffffff;
        padding: 2rem 1rem !important;
    }
    
    .stApp {
        background: #ffffff;
    }
    
    /* Contenedor principal */
    .block-container {
        padding-top: 1rem !important;
        padding-bottom: 1rem !important;
        max-width: 100% !important;
    }
    
    /* Grid de 2 columnas */
    [data-testid="column"] {
        padding: 0.5rem;
    }
    
    /* Estilo del iframe de Power BI */
    iframe {
        border: 1px solid #e5e7eb;
        border-radius: 8px;
        box-shadow: 0 1px 3px rgba(0, 0, 0, 0.1);
    }
    
    /* Input de Power BI */
    .stTextInput input {
        border: 1px solid #e5e7eb;
        border-radius: 6px;
        padding: 0.5rem;
        font-size: 0.875rem;
    }
    
    .stTextInput input:focus {
        border-color: #3b82f6;
        outline: none;
        box-shadow: 0 0 0 3px rgba(59, 130, 246, 0.1);
    }
    
    /* Mensajes del chat */
    .stChatMessage {
        background: #f9fafb;
        border-radius: 8px;
        padding: 0.75rem;
        margin-bottom: 0.5rem;
        border: 1px solid #e5e7eb;
    }
    
    .stChatMessage[data-testid="user-message"] {
        background: #eff6ff;
        border-color: #3b82f6;
    }
    
    .stChatMessage p,
    .stChatMessage div {
        color: #1f2937 !important;
        line-height: 1.5;
        font-size: 0.875rem;
    }
    
    /* Input del chat */
    .stChatInput textarea {
        border: 1px solid #e5e7eb;
        border-radius: 6px;
        font-size: 0.875rem;
    }
    
    .stChatInput textarea:focus {
        border-color: #3b82f6;
        box-shadow: 0 0 0 3px rgba(59, 130, 246, 0.1);
    }
    
    /* Scrollbar minimalista */
    ::-webkit-scrollbar {
        width: 6px;
        height: 6px;
    }
    
    ::-webkit-scrollbar-track {
        background: #f9fafb;
    }
    
    ::-webkit-scrollbar-thumb {
        background: #d1d5db;
        border-radius: 3px;
    }
    
    ::-webkit-scrollbar-thumb:hover {
        background: #9ca3af;
    }
    </style>
""", unsafe_allow_html=True)

# Crear 2 columnas: Dashboard (70%) y Chatbot (30%)
col_dashboard, col_chat = st.columns([7, 3])

# ========== COLUMNA IZQUIERDA: DASHBOARD ==========
with col_dashboard:
    # Input para URL de Power BI
    POWER_BI_URL = st.text_input(
        "URL del Dashboard de Power BI",
        placeholder="Ingrese la URL del reporte de Power BI",
        label_visibility="collapsed"
    )
    
    # Mostrar iframe si hay URL
    if POWER_BI_URL and POWER_BI_URL.strip():
        components.iframe(POWER_BI_URL, height=800, scrolling=True)

# ========== COLUMNA DERECHA: CHATBOT ==========
with col_chat:
    # Inicializar chatbot
    if 'chatbot' not in st.session_state:
        st.session_state.chatbot = ChatbotHandler()
    
    if 'chat_history' not in st.session_state:
        st.session_state.chat_history = []
    
    # Mostrar mensajes del chat
    for message in st.session_state.chat_history:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])
    
    # Input del chat
    if user_input := st.chat_input("Escribe tu pregunta..."):
        # Agregar mensaje del usuario
        st.session_state.chat_history.append({"role": "user", "content": user_input})
        with st.chat_message("user"):
            st.markdown(user_input)
        
        # Generar respuesta
        with st.chat_message("assistant"):
            with st.spinner(""):
                response = st.session_state.chatbot.get_response(user_input)
                st.markdown(response)
                st.session_state.chat_history.append({"role": "assistant", "content": response})
