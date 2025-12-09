import streamlit as st
2
3# Configuración de la página
4st.set_page_config(
5    page_title="Observatorio de Seguridad - Santander",
6    page_icon="🏛️",
7    layout="wide",
8    initial_sidebar_state="collapsed"
9)
10
11# CSS SOLO PARA HEADER
12st.markdown("""
13    <style>
14    @import url('https://fonts.googleapis.com/css2?family=Montserrat:wght@400;600;700&family=Open+Sans:wght@300;400;600&display=swap');
15    
16    * {
17        margin: 0;
18        padding: 0;
19        box-sizing: border-box;
20    }
21    
22    /* Ocultar branding Streamlit */
23    #MainMenu, footer, header, .stDeployButton { 
24        visibility: hidden; 
25    }
26    
27    .main {
28        background: #ffffff;
29        padding: 0 !important;
30        margin: 0 !important;
31    }
32    
33    .block-container {
34        padding: 0 !important;
35        margin: 0 !important;
36        max-width: 100% !important;
37    }
38    
39    /* ========== HEADER ========== */
40    .header-container {
41        background: white;
42        padding: 1rem 2rem;
43        position: sticky;
44        top: 0;
45        z-index: 1000;
46        box-shadow: 0 2px 8px rgba(0,0,0,0.08);
47        border-bottom: 1px solid #e5e7eb;
48    }
49    
50    .header-content {
51        max-width: 100%;
52        margin: 0 auto;
53        display: grid;
54        grid-template-columns: 1fr auto 1fr;
55        align-items: center;
56        gap: 2rem;
57    }
58    
59    .logo-section {
60        display: flex;
61        align-items: center;
62        gap: 1rem;
63        justify-self: start;
64    }
65    
66    .logo-section img {
67        height: 50px;
68        width: auto;
69    }
70    
71    .logo-text {
72        font-family: 'Montserrat', sans-serif;
73    }
74    
75    .logo-text h1 {
76        font-size: 1.1rem;
77        font-weight: 700;
78        margin: 0;
79        line-height: 1.2;
80        color: #003d82;
81    }
82    
83    .logo-text p {
84        font-size: 0.8rem;
85        margin: 0;
86        color: #6b7280;
87    }
88    
89    .nav-menu {
90        display: flex;
91        gap: 2rem;
92        align-items: center;
93        justify-self: center;
94    }
95    
96    .nav-cta-container {
97        justify-self: end;
98    }
99    
100    .nav-link {
101        color: #4b5563;
102        text-decoration: none;
103        font-family: 'Montserrat', sans-serif;
104        font-weight: 500;
105        font-size: 0.95rem;
106        padding: 0.5rem 0;
107        transition: all 0.2s ease;
108        cursor: pointer;
109        border-bottom: 2px solid transparent;
110        white-space: nowrap;
111    }
112    
113    .nav-link:hover {
114        color: #003d82;
115        border-bottom: 2px solid #003d82;
116    }
117    
118    .nav-cta {
119        background: #ff6b35;
120        color: white !important;
121        padding: 0.6rem 1.5rem !important;
122        border-radius: 50px;
123        border: none !important;
124        font-weight: 600;
125        text-decoration: none;
126        display: inline-block;
127        transition: all 0.3s ease;
128    }
129    
130    .nav-cta:hover {
131        background: #e55a28;
132        transform: translateY(-2px);
133        box-shadow: 0 4px 12px rgba(255,107,53,0.3);
134        border-bottom: none !important;
135    }
136    </style>
137""", unsafe_allow_html=True)
138
139# ========== HEADER ==========
140st.markdown("""
141    <div class="header-container">
142        <div class="header-content">
143            <div class="logo-section">
144                <img src="assets/logo-santander.png" alt="Gobernación de Santander">
145                <div class="logo-text">
146                    <h1>Observatorio de Seguridad</h1>
147                    <p>Gobernación de Santander</p>
148                </div>
149            </div>
150            <nav class="nav-menu">
151                <a class="nav-link" href="#inicio">Inicio</a>
152                <a class="nav-link" href="#estadisticas">Estadísticas</a>
153                <a class="nav-link" href="#portal-datos">Portal de Datos</a>
154                <a class="nav-link" href="#rutas">Rutas de Atención</a>
155            </nav>
156            <div class="nav-cta-container">
157                <a class="nav-cta" href="#opinion">Cuéntanos tu Opinión</a>
158            </div>
159        </div>
160    </div>
161""", unsafe_allow_html=True)
162
163# ========== CONTENIDO TEMPORAL ==========
164st.markdown("""
165    <div style="padding: 2rem; text-align: center;">
166        <h2>Contenido temporal</h2>
167        <p>Aquí irá el resto de la página paso por paso</p>
168    </div>
169""", unsafe_allow_html=True)
170
