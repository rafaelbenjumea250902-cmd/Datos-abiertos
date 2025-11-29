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

# CSS Minimalista con Chatbot Messenger
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Segoe+UI:wght@400;600&display=swap');
    
    /* Reset y página blanca */
    * {
        margin: 0;
        padding: 0;
        box-sizing: border-box;
        font-family: 'Segoe UI', -apple-system, BlinkMacSystemFont, sans-serif;
    }
    
    .main {
        padding: 0 !important;
        background: white;
    }
    
    .stApp {
        background: white;
    }
    
    /* Ocultar elementos de Streamlit */
    #MainMenu, footer, header, .stDeployButton {
        visibility: hidden;
    }
    
    .block-container {
        padding: 0 !important;
        max-width: 100% !important;
    }
    
    /* Power BI iframe a pantalla completa */
    iframe {
        border: none;
        width: 100vw;
        height: 100vh;
        display: block;
    }
    
    /* Botón flotante estilo Messenger */
    .chat-fab {
        position: fixed;
        bottom: 24px;
        right: 24px;
        width: 60px;
        height: 60px;
        background: linear-gradient(135deg, #00B2FF 0%, #006AFF 100%);
        border-radius: 50%;
        display: flex;
        align-items: center;
        justify-content: center;
        cursor: pointer;
        box-shadow: 0 4px 12px rgba(0, 106, 255, 0.4);
        z-index: 9999;
        transition: all 0.3s ease;
    }
    
    .chat-fab:hover {
        transform: scale(1.1);
        box-shadow: 0 6px 16px rgba(0, 106, 255, 0.5);
    }
    
    .chat-fab svg {
        width: 28px;
        height: 28px;
        fill: white;
    }
    
    /* Contador de mensajes */
    .chat-badge {
        position: absolute;
        top: -4px;
        right: -4px;
        background: #FF3B30;
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
    
    /* Contenedor del chat estilo Messenger */
    .chat-window {
        position: fixed;
        bottom: 100px;
        right: 24px;
        width: 380px;
        height: 580px;
        background: white;
        border-radius: 16px;
        box-shadow: 0 12px 48px rgba(0, 0, 0, 0.15);
        display: none;
        flex-direction: column;
        z-index: 9998;
        overflow: hidden;
    }
    
    .chat-window.active {
        display: flex;
        animation: slideUp 0.3s ease;
    }
    
    @keyframes slideUp {
        from {
            opacity: 0;
            transform: translateY(20px);
        }
        to {
            opacity: 1;
            transform: translateY(0);
        }
    }
    
    /* Header del chat Messenger */
    .chat-header {
        background: linear-gradient(135deg, #00B2FF 0%, #006AFF 100%);
        color: white;
        padding: 16px 20px;
        display: flex;
        align-items: center;
        justify-content: space-between;
    }
    
    .chat-header-info {
        display: flex;
        align-items: center;
        gap: 12px;
    }
    
    .chat-avatar {
        width: 36px;
        height: 36px;
        background: white;
        border-radius: 50%;
        display: flex;
        align-items: center;
        justify-content: center;
        font-size: 18px;
    }
    
    .chat-header-text h3 {
        font-size: 15px;
        font-weight: 600;
        margin: 0;
    }
    
    .chat-header-text p {
        font-size: 12px;
        margin: 0;
        opacity: 0.9;
    }
    
    .chat-close {
        background: none;
        border: none;
        color: white;
        cursor: pointer;
        font-size: 24px;
        width: 32px;
        height: 32px;
        border-radius: 50%;
        display: flex;
        align-items: center;
        justify-content: center;
        transition: background 0.2s;
    }
    
    .chat-close:hover {
        background: rgba(255, 255, 255, 0.2);
    }
    
    /* Área de mensajes */
    .chat-messages {
        flex: 1;
        overflow-y: auto;
        padding: 20px;
        background: white;
        display: flex;
        flex-direction: column;
        gap: 12px;
    }
    
    /* Mensajes estilo Messenger */
    .message {
        display: flex;
        gap: 8px;
        max-width: 75%;
        animation: messageIn 0.3s ease;
    }
    
    @keyframes messageIn {
        from {
            opacity: 0;
            transform: scale(0.9);
        }
        to {
            opacity: 1;
            transform: scale(1);
        }
    }
    
    .message.user {
        align-self: flex-end;
        flex-direction: row-reverse;
    }
    
    .message-bubble {
        padding: 12px 16px;
        border-radius: 18px;
        font-size: 14px;
        line-height: 1.4;
        word-wrap: break-word;
    }
    
    .message.assistant .message-bubble {
        background: #F0F0F0;
        color: #000;
        border-bottom-left-radius: 4px;
    }
    
    .message.user .message-bubble {
        background: linear-gradient(135deg, #00B2FF 0%, #006AFF 100%);
        color: white;
        border-bottom-right-radius: 4px;
    }
    
    .message-time {
        font-size: 11px;
        color: #65676B;
        margin-top: 4px;
        padding: 0 8px;
    }
    
    /* Input del chat estilo Messenger */
    .chat-input-container {
        padding: 12px 16px;
        background: white;
        border-top: 1px solid #E4E6EB;
    }
    
    .chat-input-wrapper {
        display: flex;
        align-items: center;
        gap: 8px;
        background: #F0F2F5;
        border-radius: 24px;
        padding: 8px 16px;
    }
    
    .stChatInput {
        flex: 1;
    }
    
    .stChatInput > div {
        border: none !important;
        background: transparent !important;
    }
    
    .stChatInput input {
        border: none !important;
        background: transparent !important;
        font-size: 14px !important;
        padding: 0 !important;
    }
    
    .stChatInput input:focus {
        outline: none !important;
        box-shadow: none !important;
    }
    
    /* Scrollbar personalizado */
    .chat-messages::-webkit-scrollbar {
        width: 6px;
    }
    
    .chat-messages::-webkit-scrollbar-track {
        background: transparent;
    }
    
    .chat-messages::-webkit-scrollbar-thumb {
        background: #CCC;
        border-radius: 3px;
    }
    
    .chat-messages::-webkit-scrollbar-thumb:hover {
        background: #999;
    }
    
    /* Indicador de escritura */
    .typing-indicator {
        display: flex;
        gap: 4px;
        padding: 12px 16px;
        background: #F0F0F0;
        border-radius: 18px;
        width: fit-content;
    }
    
    .typing-dot {
        width: 8px;
        height: 8px;
        background: #90949C;
        border-radius: 50%;
        animation: typing 1.4s infinite;
    }
    
    .typing-dot:nth-child(2) {
        animation-delay: 0.2s;
    }
    
    .typing-dot:nth-child(3) {
        animation-delay: 0.4s;
    }
    
    @keyframes typing {
        0%, 60%, 100% {
            transform: translateY(0);
        }
        30% {
            transform: translateY(-8px);
        }
    }
    
    /* Mensajes de Streamlit ocultos */
    .stChatMessage {
        display: none !important;
    }
    
    /* Responsive */
    @media (max-width: 768px) {
        .chat-window {
            width: 100%;
            height: 100%;
            bottom: 0;
            right: 0;
            border-radius: 0;
        }
        
        .chat-fab {
            bottom: 20px;
            right: 20px;
        }
    }
    </style>
""", unsafe_allow_html=True)

# JavaScript para manejar el chat
st.markdown("""
    <script>
    function toggleChat() {
        const chatWindow = document.querySelector('.chat-window');
        chatWindow.classList.toggle('active');
    }
    
    // Auto-scroll al final de los mensajes
    function scrollToBottom() {
        const messagesContainer = document.querySelector('.chat-messages');
        if (messagesContainer) {
            messagesContainer.scrollTop = messagesContainer.scrollHeight;
        }
    }
    
    // Llamar al scroll después de cada actualización
    setTimeout(scrollToBottom, 100);
    </script>
""", unsafe_allow_html=True)

# Power BI Embed
POWER_BI_URL = "https://app.powerbi.com/view?r=eyJrIjoiZGNkYWQ1MzgtMTNhYi00MGNiLWE4MGItYjU3MGNlMjlkNjQ2IiwidCI6ImEyYmE0MzQ1LTc3NjQtNGQyMi1iNmExLTdjZjUyOGYzYjNhNSIsImMiOjR9"

components.iframe(POWER_BI_URL, height=800, scrolling=False)

# Botón flotante del chat
st.markdown("""
    <div class="chat-fab" onclick="toggleChat()">
        <svg viewBox="0 0 28 28" xmlns="http://www.w3.org/2000/svg">
            <path d="M14 2C7.38 2 2 6.93 2 13c0 3.19 1.63 6.05 4.18 7.93V26l5.02-2.76c1.23.34 2.53.52 3.8.52 6.62 0 12-4.93 12-11S20.62 2 14 2zm1.5 14.5h-3v-3h3v3zm0-4.5h-3V7h3v5z"/>
        </svg>
    </div>
""", unsafe_allow_html=True)

# Ventana del chat
st.markdown("""
    <div class="chat-window" id="chatWindow">
        <div class="chat-header">
            <div class="chat-header-info">
                <div class="chat-avatar">🤖</div>
                <div class="chat-header-text">
                    <h3>Asistente Virtual</h3>
                    <p>Normalmente responde al instante</p>
                </div>
            </div>
            <button class="chat-close" onclick="toggleChat()">×</button>
        </div>
        <div class="chat-messages" id="chatMessages">
""", unsafe_allow_html=True)

# Initialize chatbot
if 'chatbot' not in st.session_state:
    st.session_state.chatbot = ChatbotHandler()

if 'chat_history' not in st.session_state:
    st.session_state.chat_history = []
    welcome_msg = "¡Hola! 👋 Soy tu asistente virtual. ¿En qué puedo ayudarte hoy?"
    st.session_state.chat_history.append({"role": "assistant", "content": welcome_msg})

# Display messages estilo Messenger
for message in st.session_state.chat_history:
    role_class = "user" if message["role"] == "user" else "assistant"
    st.markdown(f"""
        <div class="message {role_class}">
            <div class="message-bubble">{message["content"]}</div>
        </div>
    """, unsafe_allow_html=True)

st.markdown("""
        </div>
        <div class="chat-input-container">
            <div class="chat-input-wrapper">
""", unsafe_allow_html=True)

# Chat input
if user_input := st.chat_input("Escribe un mensaje...", key="messenger_input"):
    st.session_state.chat_history.append({"role": "user", "content": user_input})
    
    # Get bot response
    response = st.session_state.chatbot.get_response(user_input)
    st.session_state.chat_history.append({"role": "assistant", "content": response})
    
    st.rerun()

st.markdown("""
            </div>
        </div>
    </div>
""", unsafe_allow_html=True)
