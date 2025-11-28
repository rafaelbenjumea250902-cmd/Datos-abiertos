# 🚀 Sistema de Seguridad Ciudadana - Santander
## Archivos Listos para Deploy en Streamlit Cloud

---

## 📁 Archivos Incluidos

```
observatorio-santander/
├── app_gobierno.py          # Aplicación principal Streamlit
├── requirements.txt         # Dependencias Python
├── .gitignore              # Control de archivos Git
├── chatbot/                # Módulo del chatbot
│   ├── __init__.py
│   ├── llm_handler.py      # Lógica de IA
│   └── data_processor.py   # Procesador de datos
├── .streamlit/             # Configuración
│   └── config.toml         # Tema visual
├── data/                   # Carpeta para datos (opcional)
│   └── README.md
└── README.md               # Este archivo
```

---

## ✅ TODO ESTÁ LISTO

Estos son TODOS los archivos que necesitas para deployar en Streamlit Cloud.

---

## 🚀 PASO 1: Subir a GitHub

### Opción A: GitHub Desktop (MÁS FÁCIL)

```
1. Descarga GitHub Desktop: https://desktop.github.com
2. File → Add Local Repository
3. Selecciona esta carpeta
4. Commit to main
5. Publish repository
   - Name: observatorio-santander
   - Public ✅
6. ¡Listo!
```

### Opción B: Línea de Comandos

```bash
# En esta carpeta, ejecuta:

git init
git add .
git commit -m "Sistema de Seguridad Ciudadana - Santander"

# Con GitHub CLI:
gh auth login
gh repo create observatorio-santander --public --source=. --remote=origin --push

# O manual:
# 1. Crea repo en github.com/new
# 2. Luego:
git remote add origin https://github.com/TU_USUARIO/observatorio-santander.git
git branch -M main
git push -u origin main
```

---

## ☁️ PASO 2: Deploy en Streamlit Cloud

```
1. Ve a: https://share.streamlit.io
2. Sign in with GitHub
3. New app
4. Repository: TU_USUARIO/observatorio-santander
5. Branch: main
6. Main file path: app_gobierno.py
7. Advanced settings → Secrets:

   HUGGINGFACE_TOKEN = "hf_DOD7uWXVsBpNlsgKO4xnYP7jNVBXsFCB"

8. Deploy!
```

---

## ⏱️ Tiempo Total: 15 minutos

```
Subir a GitHub:      5 min
Deploy Streamlit:    3 min
Verificar:          2 min
```

---

## 🎯 Resultado Final

**URL:**
```
https://TU_USUARIO-observatorio-santander.streamlit.app
```

---

## 📞 ¿Necesitas Ayuda?

Si tienes problemas:

1. Verifica que todos los archivos estén en la carpeta
2. Asegúrate de configurar el Secret en Streamlit
3. Revisa los logs en Streamlit Cloud

---

## 🔑 IMPORTANTE: API Key

Tu API key: `hf_DOD7uWXVsBpNlsgKO4xnYP7jNVBXsFCB`

**NO la pongas en el código**. Configúrala en Streamlit Cloud como Secret.

---

## ✅ Checklist Rápido

```
[⬜] Archivos descargados
[⬜] GitHub Desktop instalado (o Git)
[⬜] Cuenta GitHub creada
[⬜] Repositorio creado y código subido
[⬜] Cuenta Streamlit Cloud creada
[⬜] App deployada
[⬜] Secret HUGGINGFACE_TOKEN configurado
[⬜] App funcionando
```

---

## 🎉 ¡Listo para Deployar!

Estos archivos contienen TODO lo necesario para tu presentación del 28 de noviembre.

**¡Éxito!** 🚀
