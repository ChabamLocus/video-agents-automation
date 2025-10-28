#!/bin/bash
# Script de instalación para GitHub Actions

echo "Instalando dependencias..."

# Actualizar pip
python -m pip install --upgrade pip

# Instalar dependencias una por una para mejor control
pip install moviepy==1.0.3
pip install gTTS==2.4.0
pip install requests==2.31.0
pip install google-api-python-client==2.100.0
pip install google-auth-oauthlib==1.1.0
pip install "imageio[ffmpeg]==2.31.0"
pip install imageio-ffmpeg==0.4.8

echo "Verificando instalación de moviepy..."
python -c "import moviepy.editor; print('✅ MoviePy instalado correctamente')"

echo "Todas las dependencias instaladas!"
