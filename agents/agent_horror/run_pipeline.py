#!/usr/bin/env python3
"""
Script principal para ejecutar todo el pipeline de generación de videos de terror.
Ejecuta automáticamente: generate.py -> tts.py -> make_video.py -> upload_youtube.py
"""

import argparse
import subprocess
import sys
import os
from datetime import datetime

def run_command(command, description):
    """Ejecuta un comando y maneja errores"""
    print(f"\n🔄 {description}...")
    try:
        result = subprocess.run(command, shell=True, check=True, capture_output=True, text=True)
        print(f"✅ {description} completado exitosamente")
        if result.stdout:
            print(result.stdout)
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ Error en {description}:")
        print(f"Código de salida: {e.returncode}")
        if e.stdout:
            print(f"Salida: {e.stdout}")
        if e.stderr:
            print(f"Error: {e.stderr}")
        return False

def main():
    parser = argparse.ArgumentParser(description="Ejecutar pipeline completo de generación de videos de terror")
    parser.add_argument("--config", required=True, help="Ruta al archivo de configuración")
    parser.add_argument("--skip-upload", action="store_true", help="Saltar la subida a YouTube")
    parser.add_argument("--upload-only", action="store_true", help="Solo subir video existente a YouTube")
    
    args = parser.parse_args()
    
    # Verificar que el archivo de configuración existe
    if not os.path.exists(args.config):
        print(f"❌ Error: Archivo de configuración no encontrado: {args.config}")
        sys.exit(1)
    
    print("🎬 Iniciando pipeline de generación de videos de terror")
    print(f"📅 Fecha: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"⚙️  Configuración: {args.config}")
    
    # Si solo queremos subir
    if args.upload_only:
        print("\n📤 Modo: Solo subida a YouTube")
        success = run_command(f"python upload_youtube.py --config {args.config}", "Subida a YouTube")
        if success:
            print("\n🎉 Pipeline completado exitosamente!")
        else:
            print("\n💥 Pipeline falló en la subida")
            sys.exit(1)
        return
    
    # Pipeline completo
    steps = [
        (f"python generate.py --config {args.config}", "Generación de script"),
        (f"python tts.py --config {args.config}", "Generación de audio"),
        (f"python make_video.py --config {args.config}", "Creación de video")
    ]
    
    # Agregar subida si no se salta
    if not args.skip_upload:
        steps.append((f"python upload_youtube.py --config {args.config}", "Subida a YouTube"))
    
    # Ejecutar cada paso
    for command, description in steps:
        success = run_command(command, description)
        if not success:
            print(f"\n💥 Pipeline falló en: {description}")
            sys.exit(1)
    
    print("\n🎉 Pipeline completado exitosamente!")
    print("📁 Archivos generados en el directorio de salida configurado")

if __name__ == "__main__":
    main()
