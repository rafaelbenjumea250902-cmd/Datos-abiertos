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

# CSS Mejorado con chat fijo
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600&display=swap');
    
    * {
        font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif;
    }
    
    /* Ocultar branding de Streamlit */
    #MainMenu, footer, header, .stDeployButton { 
        visibility: hidden; 
    }
    
    /* Fondo blanco */
    .main {
        background: #ffffff;
        padding: 0.5rem 1rem !important;
    }
    
    .stApp {
        background: #ffffff;
    }
    
    .block-container {
        padding-top: 0rem !important;
        padding-bottom: 1rem !important;
        max-width: 100% !important;
    }
    
    /* Alinear columnas arriba */
    .row-widget.stHorizontal {
        align-items: flex-start !important;
    }
    
    div[data-testid="column"] > div {
        height: 100%;
    }
    
    /* Columnas alineadas arriba */
    [data-testid="column"] {
        padding: 0.5rem;
        vertical-align: top;
    }
    
    /* Forzar alineación superior */
    [data-testid="stVerticalBlock"] > [data-testid="column"] {
        align-self: flex-start;
    }
    
    /* CHAT CONTAINER - Altura fija, alineado arriba */
    .chat-container {
        height: calc(100vh - 4rem);
        display: flex;
        flex-direction: column;
        background: #ffffff;
        border: 1px solid #e5e7eb;
        border-radius: 8px;
        overflow: hidden;
        margin-top: 0;
    }
    
    /* Header del chat */
    .chat-header {
        background: linear-gradient(135deg, #1e3a8a, #3b82f6);
        color: white;
        padding: 1rem;
        border-bottom: 1px solid #e5e7eb;
        flex-shrink: 0;
    }
    
    .chat-header h3 {
        margin: 0;
        font-size: 1rem;
        font-weight: 600;
    }
    
    .chat-header p {
        margin: 0.25rem 0 0 0;
        font-size: 0.75rem;
        opacity: 0.9;
    }
    
    /* Área de mensajes con scroll */
    .chat-messages {
        flex: 1;
        overflow-y: auto;
        padding: 1rem;
        display: flex;
        flex-direction: column;
        gap: 0.75rem;
    }
    
    /* Mensajes del chat */
    .stChatMessage {
        background: #f9fafb;
        border-radius: 12px;
        padding: 0.875rem;
        border: 1px solid #e5e7eb;
        max-width: 85%;
        word-wrap: break-word;
    }
    
    .stChatMessage[data-testid="user-message"] {
        background: #eff6ff;
        border-color: #bfdbfe;
        margin-left: auto;
    }
    
    .stChatMessage[data-testid="assistant-message"] {
        background: #f9fafb;
        border-color: #e5e7eb;
        margin-right: auto;
    }
    
    .stChatMessage p,
    .stChatMessage div {
        color: #1f2937 !important;
        line-height: 1.5;
        font-size: 0.875rem;
        margin: 0;
    }
    
    /* Input del chat */
    [data-testid="stChatInput"] {
        border-top: 1px solid #e5e7eb;
        padding: 1rem;
        background: #ffffff;
        flex-shrink: 0;
    }
    
    .stChatInput textarea {
        border: 1px solid #e5e7eb !important;
        border-radius: 8px !important;
        font-size: 0.875rem;
        padding: 0.75rem !important;
    }
    
    .stChatInput textarea:focus {
        border-color: #3b82f6 !important;
        box-shadow: 0 0 0 3px rgba(59, 130, 246, 0.1) !important;
        outline: none !important;
    }
    
    /* Scrollbar del chat */
    .chat-messages::-webkit-scrollbar {
        width: 6px;
    }
    
    .chat-messages::-webkit-scrollbar-track {
        background: #f9fafb;
    }
    
    .chat-messages::-webkit-scrollbar-thumb {
        background: #d1d5db;
        border-radius: 3px;
    }
    
    .chat-messages::-webkit-scrollbar-thumb:hover {
        background: #9ca3af;
    }
    
    /* Mensaje de bienvenida */
    .welcome-message {
        background: linear-gradient(135deg, #f0f9ff, #e0f2fe);
        border: 1px solid #bae6fd;
        border-radius: 12px;
        padding: 1.25rem;
        margin-bottom: 1rem;
        text-align: center;
    }
    
    .welcome-message h4 {
        color: #0c4a6e;
        font-size: 0.95rem;
        font-weight: 600;
        margin: 0 0 0.5rem 0;
    }
    
    .welcome-message p {
        color: #075985;
        font-size: 0.8rem;
        margin: 0;
        line-height: 1.5;
    }
    
    /* Scrollbar general */
    ::-webkit-scrollbar {
        width: 8px;
        height: 8px;
    }
    
    ::-webkit-scrollbar-track {
        background: #f9fafb;
    }
    
    ::-webkit-scrollbar-thumb {
        background: #d1d5db;
        border-radius: 4px;
    }
    
    ::-webkit-scrollbar-thumb:hover {
        background: #9ca3af;
    }
    
    /* Responsive */
    @media (max-width: 768px) {
        .chat-container {
            height: 500px;
        }
    }
    </style>
""", unsafe_allow_html=True)

# JavaScript para auto-scroll del chat
st.markdown("""
    <script>
    function scrollToBottom() {
        const chatMessages = document.querySelector('.chat-messages');
        if (chatMessages) {
            chatMessages.scrollTop = chatMessages.scrollHeight;
        }
    }
    
    // Ejecutar después de que cargue la página
    setTimeout(scrollToBottom, 100);
    
    // Observar cambios en el chat
    const observer = new MutationObserver(scrollToBottom);
    const chatContainer = document.querySelector('.chat-messages');
    if (chatContainer) {
        observer.observe(chatContainer, { childList: true, subtree: true });
    }
    </script>
""", unsafe_allow_html=True)

# Crear 2 columnas: Dashboard (70%) y Chatbot (30%)
col_dashboard, col_chat = st.columns([7, 3])

# ========== COLUMNA IZQUIERDA: DASHBOARD ==========
with col_dashboard:
    # URL de Power BI ya incluida
    POWER_BI_URL = "https://app.powerbi.com/view?r=eyJrIjoiZGNkYWQ1MzgtMTNhYi00MGNiLWE4MGItYjU3MGNlMjlkNjQ2IiwidCI6ImEyYmE0MzQ1LTc3NjQtNGQyMi1iNmExLTdjZjUyOGYzYjNhNSIsImMiOjR9"
    
    # Mostrar iframe
    components.iframe(POWER_BI_URL, height=850, scrolling=True)

# ========== COLUMNA DERECHA: CHATBOT ==========
with col_chat:
    # Contenedor del chat
    st.markdown('<div class="chat-container">', unsafe_allow_html=True)
    
    # Header del chat
    st.markdown("""
        <div class="chat-header">
            <h3>💬 Asistente Virtual</h3>
            <p>Consulta sobre seguridad en Santander</p>
        </div>
    """, unsafe_allow_html=True)
    
    # Área de mensajes
    st.markdown('<div class="chat-messages">', unsafe_allow_html=True)
    
    # Inicializar chatbot
    if 'chatbot' not in st.session_state:
        st.session_state.chatbot = ChatbotHandler()
    
    if 'chat_history' not in st.session_state:
        st.session_state.chat_history = []
    
    # Mostrar mensaje de bienvenida si no hay mensajes
    if len(st.session_state.chat_history) == 0:
        st.markdown("""
            <div class="welcome-message">
                <h4>👋 ¡Bienvenido!</h4>
                <p>Puedo ayudarte con información sobre seguridad ciudadana en Santander. 
                Pregunta sobre estadísticas, predicciones o datos de municipios.</p>
            </div>
        """, unsafe_allow_html=True)
    
    # Mostrar mensajes del chat
    for message in st.session_state.chat_history:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])
    
    st.markdown('</div>', unsafe_allow_html=True)
    
    # Input del chat (siempre visible abajo)
    if user_input := st.chat_input("Escribe tu consulta aquí..."):
        # Agregar mensaje del usuario
        st.session_state.chat_history.append({"role": "user", "content": user_input})
        
        # Generar respuesta
        with st.spinner(""):
            response = st.session_state.chatbot.get_response(user_input)
            st.session_state.chat_history.append({"role": "assistant", "content": response})
        
        # Recargar para mostrar nuevos mensajes
        st.rerun()
    
    st.markdown('</div>', unsafe_allow_html=True)
