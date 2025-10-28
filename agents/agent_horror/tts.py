import argparse, json, os
from gtts import gTTS

def load_config(path):
    try:
        with open(path, 'r', encoding='utf-8') as f:
            return json.load(f)
    except FileNotFoundError:
        raise SystemExit(f"Error: Archivo de configuración no encontrado: {path}")
    except json.JSONDecodeError as e:
        raise SystemExit(f"Error: Archivo de configuración inválido: {e}")

def validate_language(lang):
    """Valida que el idioma sea soportado por gTTS"""
    supported_languages = ['en', 'es', 'fr', 'de', 'it', 'pt', 'ru', 'ja', 'ko', 'zh']
    if lang not in supported_languages:
        print(f"Advertencia: Idioma '{lang}' puede no ser soportado. Usando 'en' por defecto.")
        return 'en'
    return lang

if __name__ == "__main__":
    try:
        p = argparse.ArgumentParser()
        p.add_argument("--config", required=True)
        args = p.parse_args()
        cfg = load_config(args.config)
        outdir = cfg.get("output_dir", "outputs")
        
        # Crear directorio de salida
        try:
            os.makedirs(outdir, exist_ok=True)
        except OSError as e:
            raise SystemExit(f"Error: No se puede crear el directorio {outdir}: {e}")
        
        script_path = os.path.join(outdir, "script.txt")
        if not os.path.exists(script_path):
            raise SystemExit("Error: No se encontró el script. Ejecuta generate.py primero.")
        
        # Leer script
        try:
            with open(script_path, "r", encoding="utf-8") as f:
                text = f.read()
        except OSError as e:
            raise SystemExit(f"Error: No se puede leer el archivo {script_path}: {e}")
        
        if not text.strip():
            raise SystemExit("Error: El script está vacío.")
        
        # Validar y usar idioma
        lang = validate_language(cfg.get("language", "en"))
        
        # Generar audio
        try:
            tts = gTTS(text=text, lang=lang)
            out_audio = os.path.join(outdir, "narration.mp3")
            tts.save(out_audio)
            print("Audio guardado en:", out_audio)
        except Exception as e:
            raise SystemExit(f"Error al generar audio: {e}")
            
    except SystemExit:
        raise
    except Exception as e:
        raise SystemExit(f"Error inesperado: {e}")
