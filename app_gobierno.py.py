import streamlit as st
import streamlit.components.v1 as components
from chatbot.llm_handler import ChatbotHandler

# Configuración de la página
st.set_page_config(
    page_title="Observatorio de Seguridad - Santander",
    page_icon="🛡️",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# CSS para chat lateral expandible estilo EPS Sanitas
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap');
    
    * {
        margin: 0;
        padding: 0;
        box-sizing: border-box;
        font-family: 'Inter', sans-serif;
    }
    
    /* Reset Streamlit */
    .main {
        padding: 0 !important;
        background: white;
    }
    
    .stApp {
        background: white;
    }
    
    #MainMenu, footer, header, .stDeployButton {
        visibility: hidden;
    }
    
    .block-container {
        padding: 0 !important;
        max-width: 100% !important;
    }
    
    /* Contenedor principal con el Power BI */
    .powerbi-container {
        width: 100%;
        height: 100vh;
        transition: width 0.3s ease;
    }
    
    .powerbi-container.chat-open {
        width: calc(100% - 400px);
    }
    
    iframe {
        border: none;
        width: 100%;
        height: 100vh;
        display: block;
    }
    
    /* Botón flotante para abrir chat */
    .chat-toggle-btn {
        position: fixed;
        right: 20px;
        bottom: 20px;
        width: 60px;
        height: 60px;
        background: linear-gradient(135deg, #0066CC 0%, #004C99 100%);
        border-radius: 50%;
        display: flex;
        align-items: center;
        justify-content: center;
        cursor: pointer;
        box-shadow: 0 4px 12px rgba(0, 102, 204, 0.3);
        z-index: 9999;
        transition: all 0.3s ease;
        border: none;
    }
    
    .chat-toggle-btn:hover {
        transform: scale(1.1);
        box-shadow: 0 6px 20px rgba(0, 102, 204, 0.4);
    }
    
    .chat-toggle-btn.chat-open {
        right: 420px;
    }
    
    .chat-toggle-btn svg {
        width: 28px;
        height: 28px;
        fill: white;
    }
    
    /* Panel lateral del chat - estilo EPS Sanitas */
    .chat-sidebar {
        position: fixed;
        right: -400px;
        top: 0;
        width: 400px;
        height: 100vh;
        background: white;
        box-shadow: -4px 0 20px rgba(0, 0, 0, 0.1);
        z-index: 9998;
        transition: right 0.3s ease;
        display: flex;
        flex-direction: column;
    }
    
    .chat-sidebar.open {
        right: 0;
    }
    
    /* Header del chat */
    .chat-header {
        background: linear-gradient(135deg, #0066CC 0%, #004C99 100%);
        padding: 20px;
        display: flex;
        align-items: center;
        justify-content: space-between;
        color: white;
        min-height: 80px;
    }
    
    .chat-header-content {
        display: flex;
        align-items: center;
        gap: 15px;
    }
    
    .chat-avatar {
        width: 50px;
        height: 50px;
        background: white;
        border-radius: 50%;
        display: flex;
        align-items: center;
        justify-content: center;
        font-size: 24px;
        flex-shrink: 0;
    }
    
    .chat-header-text h2 {
        font-size: 18px;
        font-weight: 600;
        margin: 0 0 4px 0;
    }
    
    .chat-header-text p {
        font-size: 13px;
        margin: 0;
        opacity: 0.95;
    }
    
    .chat-close-btn {
        background: rgba(255, 255, 255, 0.2);
        border: none;
        width: 36px;
        height: 36px;
        border-radius: 50%;
        display: flex;
        align-items: center;
        justify-content: center;
        cursor: pointer;
        transition: background 0.2s;
        color: white;
        font-size: 24px;
        flex-shrink: 0;
    }
    
    .chat-close-btn:hover {
        background: rgba(255, 255, 255, 0.3);
    }
    
    /* Área de mensajes */
    .chat-messages-container {
        flex: 1;
        overflow-y: auto;
        padding: 20px;
        background: #F5F7FA;
        display: flex;
        flex-direction: column;
        gap: 16px;
    }
    
    /* Mensajes */
    .message-wrapper {
        display: flex;
        gap: 10px;
        animation: messageSlideIn 0.3s ease;
    }
    
    @keyframes messageSlideIn {
        from {
            opacity: 0;
            transform: translateY(10px);
        }
        to {
            opacity: 1;
            transform: translateY(0);
        }
    }
    
    .message-wrapper.user {
        flex-direction: row-reverse;
    }
    
    .message-avatar {
        width: 32px;
        height: 32px;
        border-radius: 50%;
        background: #E0E7FF;
        display: flex;
        align-items: center;
        justify-content: center;
        font-size: 16px;
        flex-shrink: 0;
    }
    
    .message-wrapper.user .message-avatar {
        background: #DBEAFE;
    }
    
    .message-content {
        max-width: 75%;
        display: flex;
        flex-direction: column;
        gap: 4px;
    }
    
    .message-bubble {
        padding: 12px 16px;
        border-radius: 16px;
        font-size: 14px;
        line-height: 1.5;
        word-wrap: break-word;
    }
    
    .message-wrapper.assistant .message-bubble {
        background: white;
        color: #1F2937;
        border: 1px solid #E5E7EB;
        border-bottom-left-radius: 4px;
    }
    
    .message-wrapper.user .message-bubble {
        background: #0066CC;
        color: white;
        border-bottom-right-radius: 4px;
    }
    
    .message-time {
        font-size: 11px;
        color: #9CA3AF;
        padding: 0 4px;
    }
    
    /* Input del chat */
    .chat-input-area {
        padding: 16px 20px;
        background: white;
        border-top: 1px solid #E5E7EB;
    }
    
    .chat-input-wrapper {
        display: flex;
        align-items: center;
        gap: 10px;
        background: #F3F4F6;
        border-radius: 24px;
        padding: 8px 16px;
        border: 1px solid #E5E7EB;
    }
    
    .chat-input-wrapper:focus-within {
        border-color: #0066CC;
        background: white;
    }
    
    /* Ocultar elementos de Streamlit en el chat */
    .stChatMessage {
        display: none !important;
    }
    
    .stChatInput > div {
        border: none !important;
        background: transparent !important;
        padding: 0 !important;
    }
    
    .stChatInput input {
        border: none !important;
        background: transparent !important;
        font-size: 14px !important;
        padding: 0 !important;
        outline: none !important;
    }
    
    .stChatInput input:focus {
        box-shadow: none !important;
    }
    
    /* Scrollbar personalizado */
    .chat-messages-container::-webkit-scrollbar {
        width: 6px;
    }
    
    .chat-messages-container::-webkit-scrollbar-track {
        background: transparent;
    }
    
    .chat-messages-container::-webkit-scrollbar-thumb {
        background: #CBD5E1;
        border-radius: 3px;
    }
    
    .chat-messages-container::-webkit-scrollbar-thumb:hover {
        background: #94A3B8;
    }
    
    /* Badge de notificación */
    .notification-badge {
        position: absolute;
        top: -4px;
        right: -4px;
        background: #EF4444;
        color: white;
        width: 20px;
        height: 20px;
        border-radius: 50%;
        display: flex;
        align-items: center;
        justify-content: center;
        font-size: 11px;
        font-weight: 600;
        border: 2px solid white;
    }
    
    /* Indicador de escritura */
    .typing-indicator {
        display: flex;
        gap: 4px;
        padding: 12px 16px;
        background: white;
        border: 1px solid #E5E7EB;
        border-radius: 16px;
        width: fit-content;
    }
    
    .typing-dot {
        width: 8px;
        height: 8px;
        background: #9CA3AF;
        border-radius: 50%;
        animation: typingBounce 1.4s infinite;
    }
    
    .typing-dot:nth-child(2) {
        animation-delay: 0.2s;
    }
    
    .typing-dot:nth-child(3) {
        animation-delay: 0.4s;
    }
    
    @keyframes typingBounce {
        0%, 60%, 100% {
            transform: translateY(0);
        }
        30% {
            transform: translateY(-8px);
        }
    }
    
    /* Mensaje de bienvenida */
    .welcome-message {
        background: linear-gradient(135deg, #EFF6FF 0%, #DBEAFE 100%);
        border: 1px solid #BFDBFE;
        border-radius: 12px;
        padding: 16px;
        margin-bottom: 16px;
    }
    
    .welcome-message h3 {
        color: #1E40AF;
        font-size: 15px;
        font-weight: 600;
        margin: 0 0 8px 0;
    }
    
    .welcome-message p {
        color: #1E40AF;
        font-size: 13px;
        margin: 0;
        line-height: 1.5;
    }
    
    /* Responsive */
    @media (max-width: 768px) {
        .chat-sidebar {
            width: 100%;
            right: -100%;
        }
        
        .powerbi-container.chat-open {
            width: 0;
        }
        
        .chat-toggle-btn.chat-open {
            right: 20px;
        }
    }
    
    /* Animaciones suaves */
    .fade-in {
        animation: fadeIn 0.3s ease;
    }
    
    @keyframes fadeIn {
        from {
            opacity: 0;
        }
        to {
            opacity: 1;
        }
    }
    </style>
""", unsafe_allow_html=True)

# JavaScript para controlar el chat
st.markdown("""
    <script>
    function toggleChat() {
        const sidebar = document.querySelector('.chat-sidebar');
        const toggleBtn = document.querySelector('.chat-toggle-btn');
        const powerbiContainer = document.querySelector('.powerbi-container');
        
        sidebar.classList.toggle('open');
        toggleBtn.classList.toggle('chat-open');
        if (powerbiContainer) {
            powerbiContainer.classList.toggle('chat-open');
        }
        
        // Auto-scroll al final
        setTimeout(() => {
            const messagesContainer = document.querySelector('.chat-messages-container');
            if (messagesContainer) {
                messagesContainer.scrollTop = messagesContainer.scrollHeight;
            }
        }, 100);
    }
    
    // Auto-scroll después de cada actualización
    window.addEventListener('load', function() {
        const messagesContainer = document.querySelector('.chat-messages-container');
        if (messagesContainer) {
            messagesContainer.scrollTop = messagesContainer.scrollHeight;
        }
    });
    </script>
""", unsafe_allow_html=True)

# Power BI Container
st.markdown('<div class="powerbi-container" id="powerbiContainer">', unsafe_allow_html=True)

POWER_BI_URL = "https://app.powerbi.com/view?r=eyJrIjoiZGNkYWQ1MzgtMTNhYi00MGNiLWE4MGItYjU3MGNlMjlkNjQ2IiwidCI6ImEyYmE0MzQ1LTc3NjQtNGQyMi1iNmExLTdjZjUyOGYzYjNhNSIsImMiOjR9"

components.iframe(POWER_BI_URL, height=1000, scrolling=True)

st.markdown('</div>', unsafe_allow_html=True)

# Botón flotante
st.markdown("""
    <button class="chat-toggle-btn" onclick="toggleChat()">
        <svg viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg">
            <path d="M20 2H4c-1.1 0-2 .9-2 2v18l4-4h14c1.1 0 2-.9 2-2V4c0-1.1-.9-2-2-2zm0 14H6l-2 2V4h16v12z"/>
            <path d="M7 9h2v2H7zm4 0h2v2h-2zm4 0h2v2h-2z"/>
        </svg>
    </button>
""", unsafe_allow_html=True)

# Panel lateral del chat
st.markdown('<div class="chat-sidebar">', unsafe_allow_html=True)

# Header del chat
st.markdown("""
    <div class="chat-header">
        <div class="chat-header-content">
            <div class="chat-avatar">🤖</div>
            <div class="chat-header-text">
                <h2>Asistente Virtual</h2>
                <p>Disponible 24/7 • Respuesta instantánea</p>
            </div>
        </div>
        <button class="chat-close-btn" onclick="toggleChat()">×</button>
    </div>
""", unsafe_allow_html=True)

# Contenedor de mensajes
st.markdown('<div class="chat-messages-container" id="chatMessagesContainer">', unsafe_allow_html=True)

# Initialize chatbot
if 'chatbot' not in st.session_state:
    st.session_state.chatbot = ChatbotHandler()

if 'chat_history' not in st.session_state:
    st.session_state.chat_history = []
    # Mensaje de bienvenida
    welcome_msg = "¡Hola! 👋 Soy tu asistente virtual del Observatorio de Seguridad de Santander. Puedo ayudarte con estadísticas, predicciones y análisis de seguridad. ¿Qué necesitas saber?"
    st.session_state.chat_history.append({"role": "assistant", "content": welcome_msg})

# Mensaje de bienvenida especial
if len(st.session_state.chat_history) == 1:
    st.markdown("""
        <div class="welcome-message fade-in">
            <h3>👋 ¡Bienvenido al Observatorio de Seguridad!</h3>
            <p>Puedo ayudarte con:</p>
            <p>📊 Estadísticas por municipio<br>
            🎯 Predicciones de seguridad<br>
            📈 Análisis de tendencias<br>
            🗺️ Datos históricos</p>
        </div>
    """, unsafe_allow_html=True)

# Display messages
for message in st.session_state.chat_history:
    role_class = "user" if message["role"] == "user" else "assistant"
    avatar = "👤" if message["role"] == "user" else "🤖"
    
    st.markdown(f"""
        <div class="message-wrapper {role_class} fade-in">
            <div class="message-avatar">{avatar}</div>
            <div class="message-content">
                <div class="message-bubble">{message["content"]}</div>
            </div>
        </div>
    """, unsafe_allow_html=True)

st.markdown('</div>', unsafe_allow_html=True)

# Input area
st.markdown('<div class="chat-input-area">', unsafe_allow_html=True)
st.markdown('<div class="chat-input-wrapper">', unsafe_allow_html=True)

# Chat input
if user_input := st.chat_input("Escribe tu mensaje...", key="chat_input"):
    # Agregar mensaje del usuario
    st.session_state.chat_history.append({"role": "user", "content": user_input})
    
    # Obtener respuesta del bot
    response = st.session_state.chatbot.get_response(user_input)
    st.session_state.chat_history.append({"role": "assistant", "content": response})
    
    # Rerun para actualizar la UI
    st.rerun()

st.markdown('</div>', unsafe_allow_html=True)
st.markdown('</div>', unsafe_allow_html=True)

st.markdown('</div>', unsafe_allow_html=True)
