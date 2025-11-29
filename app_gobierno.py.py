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

# CSS para layout 75/25 HORIZONTAL
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap');
    
    * {
        margin: 0;
        padding: 0;
        box-sizing: border-box;
        font-family: 'Inter', sans-serif;
    }
    
    html, body, #root {
        height: 100%;
        overflow: hidden;
    }
    
    /* Reset Streamlit - MUY IMPORTANTE */
    .main {
        padding: 0 !important;
        background: white;
        height: 100vh !important;
        overflow: hidden !important;
    }
    
    .stApp {
        background: white;
        height: 100vh !important;
        overflow: hidden !important;
    }
    
    #MainMenu, footer, header, .stDeployButton {
        visibility: hidden !important;
        display: none !important;
    }
    
    .block-container {
        padding: 0 !important;
        max-width: 100% !important;
        height: 100vh !important;
        overflow: hidden !important;
    }
    
    /* Ocultar TODOS los elementos de Streamlit que no necesitamos */
    section[data-testid="stSidebar"] {
        display: none !important;
    }
    
    div[data-testid="stToolbar"] {
        display: none !important;
    }
    
    div[data-testid="stDecoration"] {
        display: none !important;
    }
    
    div[data-testid="stStatusWidget"] {
        display: none !important;
    }
    
    /* Forzar que el contenedor principal ocupe todo */
    .main .block-container > div:first-child {
        height: 100vh !important;
    }
    
    /* Ocultar el chat input de Streamlit por defecto */
    .stChatInput {
        position: absolute !important;
        bottom: 14px !important;
        left: 0 !important;
        right: 0 !important;
        width: calc(100% - 32px) !important;
        margin: 0 16px !important;
        z-index: 100 !important;
    }
    
    .stChatMessage {
        display: none !important;
    }
    
    .stChatInput > div {
        border: none !important;
        background: transparent !important;
        padding: 0 !important;
        margin: 0 !important;
    }
    
    .stChatInput input {
        border: none !important;
        background: transparent !important;
        font-size: 13px !important;
        padding: 8px 0 !important;
        outline: none !important;
        width: 100% !important;
    }
    
    .stChatInput input:focus {
        box-shadow: none !important;
    }
    
    .stChatInput input::placeholder {
        color: #9CA3AF !important;
    }
    </style>
""", unsafe_allow_html=True)

# Estructura HTML completa con iframe embebido
st.markdown(f"""
    <style>
    /* Contenedor principal - Layout HORIZONTAL */
    .main-layout {{
        display: flex;
        flex-direction: row;
        height: 100vh;
        width: 100%;
        overflow: hidden;
        position: fixed;
        top: 0;
        left: 0;
        right: 0;
        bottom: 0;
    }}
    
    /* Power BI - 75% del ancho A LA IZQUIERDA */
    .powerbi-section {{
        width: 75%;
        height: 100vh;
        background: #f8f9fa;
        overflow: hidden;
        position: relative;
    }}
    
    .powerbi-section iframe {{
        border: none;
        width: 100%;
        height: 100%;
        display: block;
        position: absolute;
        top: 0;
        left: 0;
    }}
    
    /* Chat - 25% del ancho A LA DERECHA */
    .chat-section {{
        width: 25%;
        height: 100vh;
        background: white;
        border-left: 1px solid #E5E7EB;
        display: flex;
        flex-direction: column;
        overflow: hidden;
        position: relative;
    }}
    
    /* Header del chat */
    .chat-header {{
        background: linear-gradient(135deg, #0066CC 0%, #004C99 100%);
        padding: 20px;
        color: white;
        flex-shrink: 0;
        z-index: 10;
    }}
    
    .chat-header-content {{
        display: flex;
        align-items: center;
        gap: 12px;
    }}
    
    .chat-avatar {{
        width: 45px;
        height: 45px;
        background: white;
        border-radius: 50%;
        display: flex;
        align-items: center;
        justify-content: center;
        font-size: 22px;
        flex-shrink: 0;
    }}
    
    .chat-header-text h2 {{
        font-size: 16px;
        font-weight: 600;
        margin: 0 0 3px 0;
    }}
    
    .chat-header-text p {{
        font-size: 12px;
        margin: 0;
        opacity: 0.95;
    }}
    
    /* Área de mensajes */
    .chat-messages-area {{
        flex: 1;
        overflow-y: auto;
        padding: 16px;
        padding-bottom: 80px;
        background: #F5F7FA;
        display: flex;
        flex-direction: column;
        gap: 12px;
    }}
    
    /* Mensajes */
    .message-item {{
        display: flex;
        gap: 8px;
        animation: messageAppear 0.3s ease;
    }}
    
    @keyframes messageAppear {{
        from {{
            opacity: 0;
            transform: translateY(8px);
        }}
        to {{
            opacity: 1;
            transform: translateY(0);
        }}
    }}
    
    .message-item.user {{
        flex-direction: row-reverse;
    }}
    
    .msg-avatar {{
        width: 28px;
        height: 28px;
        border-radius: 50%;
        background: #E0E7FF;
        display: flex;
        align-items: center;
        justify-content: center;
        font-size: 14px;
        flex-shrink: 0;
    }}
    
    .message-item.user .msg-avatar {{
        background: #DBEAFE;
    }}
    
    .msg-bubble {{
        max-width: 80%;
        padding: 10px 14px;
        border-radius: 14px;
        font-size: 13px;
        line-height: 1.5;
        word-wrap: break-word;
    }}
    
    .message-item.assistant .msg-bubble {{
        background: white;
        color: #1F2937;
        border: 1px solid #E5E7EB;
        border-bottom-left-radius: 4px;
    }}
    
    .message-item.user .msg-bubble {{
        background: #0066CC;
        color: white;
        border-bottom-right-radius: 4px;
    }}
    
    /* Input del chat */
    .chat-input-section {{
        padding: 14px 16px;
        background: white;
        border-top: 1px solid #E5E7EB;
        flex-shrink: 0;
        position: absolute;
        bottom: 0;
        left: 0;
        right: 0;
        z-index: 20;
    }}
    
    .input-box {{
        display: flex;
        align-items: center;
        gap: 8px;
        background: #F3F4F6;
        border-radius: 20px;
        padding: 6px 14px;
        border: 1px solid #E5E7EB;
    }}
    
    .input-box:focus-within {{
        border-color: #0066CC;
        background: white;
    }}
    
    /* Scrollbar */
    .chat-messages-area::-webkit-scrollbar {{
        width: 5px;
    }}
    
    .chat-messages-area::-webkit-scrollbar-track {{
        background: transparent;
    }}
    
    .chat-messages-area::-webkit-scrollbar-thumb {{
        background: #CBD5E1;
        border-radius: 3px;
    }}
    
    .chat-messages-area::-webkit-scrollbar-thumb:hover {{
        background: #94A3B8;
    }}
    
    /* Badge de bienvenida */
    .welcome-badge {{
        background: linear-gradient(135deg, #EFF6FF 0%, #DBEAFE 100%);
        border: 1px solid #BFDBFE;
        border-radius: 10px;
        padding: 12px;
        margin-bottom: 12px;
        text-align: center;
    }}
    
    .welcome-badge h3 {{
        color: #1E40AF;
        font-size: 14px;
        font-weight: 600;
        margin: 0 0 6px 0;
    }}
    
    .welcome-badge p {{
        color: #1E40AF;
        font-size: 12px;
        margin: 4px 0;
        line-height: 1.4;
    }}
    
    /* Responsive */
    @media (max-width: 1024px) {{
        .powerbi-section {{
            width: 70%;
        }}
        
        .chat-section {{
            width: 30%;
        }}
    }}
    
    @media (max-width: 768px) {{
        .main-layout {{
            flex-direction: column;
        }}
        
        .powerbi-section {{
            width: 100%;
            height: 60vh;
        }}
        
        .chat-section {{
            width: 100%;
            height: 40vh;
            border-left: none;
            border-top: 1px solid #E5E7EB;
        }}
    }}
    </style>
    
    <div class="main-layout">
        <!-- POWER BI SECTION (75% IZQUIERDA) -->
        <div class="powerbi-section">
            <iframe 
                src="https://app.powerbi.com/view?r=eyJrIjoiZGNkYWQ1MzgtMTNhYi00MGNiLWE4MGItYjU3MGNlMjlkNjQ2IiwidCI6ImEyYmE0MzQ1LTc3NjQtNGQyMi1iNmExLTdjZjUyOGYzYjNhNSIsImMiOjR9"
                frameborder="0"
                allowFullScreen="true">
            </iframe>
        </div>
        
        <!-- CHAT SECTION (25% DERECHA) -->
        <div class="chat-section">
            <!-- Header -->
            <div class="chat-header">
                <div class="chat-header-content">
                    <div class="chat-avatar">🤖</div>
                    <div class="chat-header-text">
                        <h2>Asistente Virtual IA</h2>
                        <p>Respuesta instantánea</p>
                    </div>
                </div>
            </div>
            
            <!-- Mensajes -->
            <div class="chat-messages-area" id="chatMessages">
""", unsafe_allow_html=True)

# Initialize chatbot
if 'chatbot' not in st.session_state:
    st.session_state.chatbot = ChatbotHandler()

if 'chat_history' not in st.session_state:
    st.session_state.chat_history = []
    welcome = "¡Hola! 👋 Soy tu asistente del Observatorio de Seguridad de Santander. Pregúntame sobre estadísticas, predicciones y análisis de seguridad."
    st.session_state.chat_history.append({"role": "assistant", "content": welcome})

# Mensaje de bienvenida
if len(st.session_state.chat_history) == 1:
    st.markdown("""
        <div class="welcome-badge">
            <h3>👋 ¡Bienvenido!</h3>
            <p>📊 Estadísticas por municipio</p>
            <p>🎯 Predicciones de seguridad</p>
            <p>📈 Análisis de tendencias</p>
        </div>
    """, unsafe_allow_html=True)

# Display messages
for msg in st.session_state.chat_history:
    role = "user" if msg["role"] == "user" else "assistant"
    avatar = "👤" if msg["role"] == "user" else "🤖"
    
    st.markdown(f"""
        <div class="message-item {role}">
            <div class="msg-avatar">{avatar}</div>
            <div class="msg-bubble">{msg["content"]}</div>
        </div>
    """, unsafe_allow_html=True)

# Cerrar área de mensajes y agregar input
st.markdown("""
            </div>
            
            <!-- Input Section -->
            <div class="chat-input-section">
                <div class="input-box">
                    <span style="color: #9CA3AF; font-size: 13px;">✍️</span>
                </div>
            </div>
        </div>
    </div>
""", unsafe_allow_html=True)

# Chat input de Streamlit (ahora posicionado correctamente)
if user_input := st.chat_input("Escribe tu mensaje...", key="chat"):
    st.session_state.chat_history.append({"role": "user", "content": user_input})
    response = st.session_state.chatbot.get_response(user_input)
    st.session_state.chat_history.append({"role": "assistant", "content": response})
    st.rerun()

# Auto-scroll
st.markdown("""
    <script>
    window.addEventListener('load', function() {
        const chat = document.getElementById('chatMessages');
        if (chat) {
            chat.scrollTop = chat.scrollHeight;
        }
    });
    
    // Mover el input de Streamlit dentro del chat
    document.addEventListener('DOMContentLoaded', function() {
        const chatInput = document.querySelector('.stChatInput');
        const inputBox = document.querySelector('.input-box');
        if (chatInput && inputBox) {
            inputBox.appendChild(chatInput);
        }
    });
    </script>
""", unsafe_allow_html=True)