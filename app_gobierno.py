import streamlit as st

st.set_page_config(page_title="Observatorio de Seguridad", page_icon="🏛️", layout="wide")

if 'page' not in st.session_state:
    st.session_state.page = 'Inicio'
if 'messages' not in st.session_state:
    st.session_state.messages = []

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

.header-nav {
    background: white;
    padding: 1rem 2rem;
    box-shadow: 0 2px 8px rgba(0,0,0,0.08);
    border-bottom: 1px solid #e5e7eb;
    display: flex;
    justify-content: space-between;
    align-items: center;
}

.nav-links {
    display: flex;
    gap: 2rem;
    align-items: center;
}

.nav-link {
    color: #4b5563;
    text-decoration: none;
    font-family: 'Montserrat', sans-serif;
    font-weight: 500;
    font-size: 1.1rem;
    padding: 0.5rem 1rem;
    cursor: pointer;
    border-bottom: 2px solid transparent;
    transition: all 0.2s;
}

.nav-link:hover {
    color: #003d82;
    border-bottom: 2px solid #003d82;
}

.nav-link.active {
    color: #003d82;
    border-bottom: 2px solid #003d82;
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
    background: #f5f5f5;
}

.chat-header {
    background: linear-gradient(135deg, #003d82, #0056b3);
    color: white;
    padding: 1rem;
    font-family: 'Montserrat', sans-serif;
    font-weight: 600;
}

.chat-messages {
    flex: 1;
    overflow-y: auto;
    padding: 1rem;
    display: flex;
    flex-direction: column;
    gap: 0.75rem;
}

.message {
    display: flex;
    margin-bottom: 0.5rem;
}

.message.user {
    justify-content: flex-end;
}

.message.bot {
    justify-content: flex-start;
}

.message-bubble {
    max-width: 70%;
    padding: 0.75rem 1rem;
    border-radius: 18px;
    font-family: 'Open Sans', sans-serif;
    font-size: 0.95rem;
    line-height: 1.4;
}

.message.user .message-bubble {
    background: #0084ff;
    color: white;
    border-bottom-right-radius: 4px;
}

.message.bot .message-bubble {
    background: #e4e6eb;
    color: #050505;
    border-bottom-left-radius: 4px;
}

.chat-input-area {
    padding: 1rem;
    background: white;
    border-top: 1px solid #e0e0e0;
}

.placeholder-content {
    padding: 3rem 2rem;
    text-align: center;
    font-family: 'Montserrat', sans-serif;
}

.stTextInput input {
    border-radius: 20px !important;
    padding: 0.75rem 1rem !important;
    border: 1px solid #ddd !important;
}

.stButton button {
    background: #0084ff !important;
    color: white !important;
    border-radius: 20px !important;
    padding: 0.5rem 2rem !important;
    font-weight: 600 !important;
    border: none !important;
}

iframe {
    border: none !important;
}
</style>
""", unsafe_allow_html=True)

col1, col2 = st.columns([1, 3])

with col1:
    st.markdown('<div style="font-family: Montserrat; font-weight: 700; color: #003d82; font-size: 1.2rem; padding: 1rem 2rem;">Observatorio</div>', unsafe_allow_html=True)

with col2:
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
        st.markdown('<div class="chat-header">💬 Asistente Virtual</div>', unsafe_allow_html=True)
        
        chat_container = st.container(height=600)
        with chat_container:
            for msg in st.session_state.messages:
                role_class = "user" if msg["role"] == "user" else "bot"
                st.markdown(f'<div class="message {role_class}"><div class="message-bubble">{msg["content"]}</div></div>', unsafe_allow_html=True)
        
        with st.form(key="chat_form", clear_on_submit=True):
            user_input = st.text_input("Escribe tu mensaje...", key="user_input", label_visibility="collapsed")
            submit = st.form_submit_button("Enviar")
            
            if submit and user_input:
                st.session_state.messages.append({"role": "user", "content": user_input})
                st.session_state.messages.append({"role": "bot", "content": "Estoy procesando tu consulta..."})
                st.rerun()

elif st.session_state.page == 'Portal de Datos':
    st.markdown('<div class="placeholder-content"><h2>Portal de Datos</h2><p>Contenido próximamente</p></div>', unsafe_allow_html=True)

elif st.session_state.page == 'Rutas de Atención':
    st.markdown('<div class="placeholder-content"><h2>Rutas de Atención</h2><p>Contenido próximamente</p></div>', unsafe_allow_html=True)

elif st.session_state.page == 'Cuéntanos tu Opinión':
    st.markdown('<div class="placeholder-content"><h2>Cuéntanos tu Opinión</h2><p>Contenido próximamente</p></div>', unsafe_allow_html=True)
