import streamlit as st
from chatbot.llm_handler import ChatbotHandler

st.set_page_config(page_title="Observatorio de Seguridad", page_icon="🏛️", layout="wide")

if 'page' not in st.session_state:
    st.session_state.page = 'Inicio'
if 'chatbot' not in st.session_state:
    st.session_state.chatbot = ChatbotHandler()
if 'chat_history' not in st.session_state:
    st.session_state.chat_history = []

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
}

.block-container {
    padding: 0 !important;
    max-width: 100% !important;
}

.header-section {
    background: white;
    padding: 1rem 2rem 0.5rem;
    box-shadow: 0 2px 4px rgba(0,0,0,0.05);
    border-bottom: 1px solid #e5e7eb;
}

.logo-container-center {
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    text-align: center;
}

[data-testid="column"] {
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
}

[data-testid="stImage"] {
    display: flex;
    justify-content: center;
}

.content-section {
    padding: 0;
    margin: 0;
}

.estadisticas-container {
    display: flex;
    height: calc(100vh - 80px);
    width: 100%;
}

.dashboard-panel {
    width: 70%;
    height: 100%;
}

.chat-panel {
    width: 30%;
    height: 100%;
    border-left: 1px solid #e0e0e0;
    display: flex;
    flex-direction: column;
    background: white;
}

.chat-header {
    background: linear-gradient(135deg, #003d82, #0056b3);
    color: white;
    padding: 1rem;
    font-family: 'Montserrat', sans-serif;
    font-weight: 600;
    display: flex;
    justify-content: space-between;
    align-items: center;
}

.chat-header h3 {
    font-size: 1rem;
    margin: 0;
}

.chat-header p {
    font-size: 0.8rem;
    opacity: 0.9;
    margin: 0;
}

.placeholder-content {
    padding: 3rem 2rem;
    text-align: center;
    font-family: 'Montserrat', sans-serif;
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

.stButton button {
    font-family: 'Montserrat', sans-serif !important;
    font-weight: 400 !important;
    font-size: 0.95rem !important;
    color: #666 !important;
    background: transparent !important;
    border: none !important;
    border-bottom: 2px solid transparent !important;
    border-radius: 0 !important;
    padding: 0.5rem 1rem !important;
    letter-spacing: 0.5px !important;
}

.stButton button:hover {
    color: #1a1a1a !important;
    border-bottom: 2px solid #1a1a1a !important;
    background: transparent !important;
}

iframe {
    border: none !important;
}
</style>
""", unsafe_allow_html=True)

st.markdown('<div class="header-section"><div class="logo-container-center">', unsafe_allow_html=True)

st.image("assets/logo-santander.png", use_column_width=True)

st.markdown('</div></div>', unsafe_allow_html=True)

cols = st.columns(5)
pages = ['Inicio', 'Estadísticas', 'Portal de Datos', 'Rutas de Atención', 'Cuéntanos tu Opinión']
for i, page in enumerate(pages):
    if cols[i].button(page, key=f"nav_{page}", use_container_width=True):
        st.session_state.page = page
        st.rerun()

if st.session_state.page == 'Inicio':
    st.markdown('<div class="placeholder-content"><h2>Bienvenido al Observatorio de Seguridad</h2><p>Selecciona una sección del menú</p></div>', unsafe_allow_html=True)

elif st.session_state.page == 'Estadísticas':
    col_dash, col_chat = st.columns([70, 30], gap="small")
    
    with col_dash:
        st.components.v1.iframe("https://app.powerbi.com/view?r=eyJrIjoiZGNkYWQ1MzgtMTNhYi00MGNiLWE4MGItYjU3MGNlMjlkNjQ2IiwidCI6ImEyYmE0MzQ1LTc3NjQtNGQyMi1iNmExLTdjZjUyOGYzYjNhNSIsImMiOjR9", height=800, scrolling=False)
    
    with col_chat:
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
        
        chat_container = st.container(height=600)
        
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
        
        if user_input := st.chat_input("Escribe tu consulta aquí...", key="chat_input"):
            st.session_state.chat_history.append({"role": "user", "content": user_input})
            
            with st.spinner(""):
                response = st.session_state.chatbot.get_response(user_input)
                st.session_state.chat_history.append({"role": "assistant", "content": response})
            
            st.rerun()

elif st.session_state.page == 'Portal de Datos':
    st.markdown('<div class="placeholder-content"><h2>Portal de Datos</h2><p>Contenido próximamente</p></div>', unsafe_allow_html=True)

elif st.session_state.page == 'Rutas de Atención':
    st.markdown('<div class="placeholder-content"><h2>Rutas de Atención</h2><p>Contenido próximamente</p></div>', unsafe_allow_html=True)

elif st.session_state.page == 'Cuéntanos tu Opinión':
    st.markdown('<div class="placeholder-content"><h2>Cuéntanos tu Opinión</h2><p>Contenido próximamente</p></div>', unsafe_allow_html=True)
