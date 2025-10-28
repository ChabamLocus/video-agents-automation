# Video Agents Automation - Horror Stories

Sistema automatizado para generar videos de terror/crimen verdadero usando IA. El sistema genera scripts, los convierte a audio, crea videos y los sube a YouTube.

## 🎬 Características

- **Generación automática de scripts** sobre temas de terror y crimen verdadero
- **Text-to-Speech** usando Google TTS
- **Creación de videos** con fondo negro y audio
- **Subida automática a YouTube** con configuración personalizable
- **Pipeline completo automatizado** con un solo comando

## 📋 Requisitos

- Python 3.8+
- FFmpeg instalado en el sistema
- Credenciales de YouTube API configuradas

## 🚀 Instalación

1. **Clonar el repositorio:**
```bash
git clone <repository-url>
cd video-agents-automation-main
```

2. **Instalar dependencias:**
```bash
pip install -r requirements.txt
```

3. **Instalar FFmpeg:**
   - **Windows:** Descargar desde https://ffmpeg.org/download.html
   - **macOS:** `brew install ffmpeg`
   - **Linux:** `sudo apt install ffmpeg`

4. **Configurar credenciales de YouTube:**
```bash
export YOUTUBE_CLIENT_ID="tu_client_id"
export YOUTUBE_CLIENT_SECRET="tu_client_secret"
export YOUTUBE_REFRESH_TOKEN="tu_refresh_token"
```

## ⚙️ Configuración

Edita `agents/agent_horror/config.json` para personalizar:

```json
{
  "agent_name": "agent_horror",
  "niche": "true crime and horror stories",
  "title_template": "Creepy Tale: {topic}",
  "description_template": "An AI-generated true crime and horror short about {topic}. Viewer discretion is advised.",
  "language": "en",
  "output_dir": "outputs",
  "video_settings": {
    "width": 1080,
    "height": 1920,
    "fps": 24,
    "background_color": [0, 0, 0]
  },
  "youtube_settings": {
    "category_id": "24",
    "privacy_status": "private",
    "tags": ["horror", "crime", "AI", "story"]
  }
}
```

## 🎯 Uso

### Pipeline Completo (Recomendado)
```bash
python agents/agent_horror/run_pipeline.py --config agents/agent_horror/config.json
```

### Pasos Individuales
```bash
# 1. Generar script
python agents/agent_horror/generate.py --config agents/agent_horror/config.json

# 2. Crear audio
python agents/agent_horror/tts.py --config agents/agent_horror/config.json

# 3. Crear video
python agents/agent_horror/make_video.py --config agents/agent_horror/config.json

# 4. Subir a YouTube
python agents/agent_horror/upload_youtube.py --config agents/agent_horror/config.json
```

### Opciones Adicionales
```bash
# Saltar subida a YouTube
python agents/agent_horror/run_pipeline.py --config agents/agent_horror/config.json --skip-upload

# Solo subir video existente
python agents/agent_horror/run_pipeline.py --config agents/agent_horror/config.json --upload-only
```

## 📁 Estructura de Archivos

```
agents/agent_horror/
├── config.json          # Configuración del agente
├── generate.py          # Generación de scripts
├── tts.py              # Text-to-Speech
├── make_video.py       # Creación de videos
├── upload_youtube.py   # Subida a YouTube
└── run_pipeline.py     # Script principal automatizado

outputs/                 # Directorio de salida (creado automáticamente)
├── script.txt          # Script generado
├── narration.mp3       # Audio generado
└── final.mp4          # Video final
```

## 🔧 Mejoras Implementadas

- ✅ **Manejo robusto de errores** en todos los scripts
- ✅ **Liberación de recursos** para evitar memory leaks
- ✅ **Validación de archivos** y configuraciones
- ✅ **Procesamiento de templates** con placeholders
- ✅ **Dependencias con versiones específicas**
- ✅ **Pipeline automatizado** con un solo comando
- ✅ **Mensajes informativos** en español
- ✅ **Compatibilidad con Python 3.12+**

## 🐛 Solución de Problemas

### Error: "No se puede crear el directorio"
- Verifica permisos de escritura en el directorio actual
- Asegúrate de que el path en `output_dir` sea válido

### Error: "Faltan credenciales de YouTube"
- Configura las variables de entorno correctamente
- Verifica que las credenciales sean válidas

### Error: "FFmpeg no encontrado"
- Instala FFmpeg y asegúrate de que esté en el PATH
- Reinicia la terminal después de instalar

### Error: "No se puede cargar el archivo de audio"
- Ejecuta los scripts en orden: generate.py → tts.py → make_video.py
- Verifica que el archivo `narration.mp3` se haya creado correctamente

## 📝 Notas

- Los videos se suben como **privados** por defecto
- El sistema genera contenido sobre temas de terror/crimen verdadero
- Se recomienda revisar el contenido antes de hacer público
- Los archivos temporales se guardan en el directorio `outputs/`

## 🤝 Contribuciones

Las contribuciones son bienvenidas. Por favor:
1. Fork el proyecto
2. Crea una rama para tu feature
3. Commit tus cambios
4. Push a la rama
5. Abre un Pull Request
