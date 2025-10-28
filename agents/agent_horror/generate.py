import argparse, json, os
from datetime import datetime, timezone
import random

def load_config(path):
    try:
        with open(path, 'r', encoding='utf-8') as f:
            return json.load(f)
    except FileNotFoundError:
        raise SystemExit(f"Error: Archivo de configuración no encontrado: {path}")
    except json.JSONDecodeError as e:
        raise SystemExit(f"Error: Archivo de configuración inválido: {e}")

def generate_script(cfg):
    topics = [
        "unsolved murders",
        "cursed objects",
        "serial killers from the 80s",
        "haunted hospitals",
        "urban legends that turned real",
        "mysterious disappearances",
        "bizarre cults",
        "crime scenes with strange clues"
    ]
    topic = random.choice(topics)
    script = (
        f"Tonight’s story is about {topic}. "
        f"Beware... some of these tales are not for the faint of heart. "
        f"This short video explores one of the darkest corners of human history. "
        f"Generated automatically on {datetime.now(timezone.utc).strftime('%B %d, %Y')}."
    )
    return script

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
        
        script_text = generate_script(cfg)
        script_path = os.path.join(outdir, "script.txt")
        
        # Guardar script
        try:
            with open(script_path, "w", encoding="utf-8") as f:
                f.write(script_text)
            print("Horror script saved to", script_path)
        except OSError as e:
            raise SystemExit(f"Error: No se puede escribir el archivo {script_path}: {e}")
            
    except SystemExit:
        raise
    except Exception as e:
        raise SystemExit(f"Error inesperado: {e}")
