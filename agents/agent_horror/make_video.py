import argparse, json, os
from moviepy.editor import AudioFileClip, ColorClip

def load_config(path):
    try:
        with open(path, 'r', encoding='utf-8') as f:
            return json.load(f)
    except FileNotFoundError:
        raise SystemExit(f"Error: Archivo de configuración no encontrado: {path}")
    except json.JSONDecodeError as e:
        raise SystemExit(f"Error: Archivo de configuración inválido: {e}")

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

        audio_path = os.path.join(outdir, "narration.mp3")
        if not os.path.exists(audio_path):
            raise SystemExit(f"Error: No se encontró el audio en {audio_path}. Ejecuta tts.py primero.")

        # Cargar audio con manejo de recursos
        try:
            audio = AudioFileClip(audio_path)
        except Exception as e:
            raise SystemExit(f"Error al cargar el archivo de audio: {e}")

        try:
            # Crear video con fondo negro
            clip = ColorClip(size=(1080, 1920), color=(0, 0, 0), duration=audio.duration).set_fps(24).set_audio(audio)
            
            out_video = os.path.join(outdir, "final.mp4")
            
            # Escribir video con manejo de errores
            try:
                clip.write_videofile(out_video, codec="libx264", audio_codec="aac", fps=24, verbose=False, logger=None)
                print("Video creado:", out_video)
            except Exception as e:
                raise SystemExit(f"Error al crear el video: {e}")
            finally:
                # Liberar recursos
                clip.close()
                audio.close()
                
        except Exception as e:
            # Asegurar que se liberen los recursos en caso de error
            try:
                audio.close()
            except:
                pass
            raise SystemExit(f"Error al procesar el video: {e}")
            
    except SystemExit:
        raise
    except Exception as e:
        raise SystemExit(f"Error inesperado: {e}")
