import argparse, json, os, sys
import requests
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload
from google.oauth2.credentials import Credentials

def load_config(path):
    try:
        with open(path, 'r', encoding='utf-8') as f:
            return json.load(f)
    except FileNotFoundError:
        raise SystemExit(f"Error: Archivo de configuración no encontrado: {path}")
    except json.JSONDecodeError as e:
        raise SystemExit(f"Error: Archivo de configuración inválido: {e}")

def get_credentials_from_refresh(client_id, client_secret, refresh_token):
    """Obtiene credenciales usando refresh token"""
    token_url = "https://oauth2.googleapis.com/token"
    data = {
        "client_id": client_id,
        "client_secret": client_secret,
        "refresh_token": refresh_token,
        "grant_type": "refresh_token"
    }
    try:
        r = requests.post(token_url, data=data, timeout=30)
        r.raise_for_status()
        return r.json()
    except requests.exceptions.RequestException as e:
        raise SystemExit(f"Error al obtener credenciales: {e}")
    except Exception as e:
        raise SystemExit(f"Error inesperado al obtener credenciales: {e}")

def process_templates(cfg, topic="mystery"):
    """Procesa los templates reemplazando placeholders"""
    title_template = cfg.get("title_template", "Creepy Tale: {topic}")
    description_template = cfg.get("description_template", "An AI-generated true crime and horror short about {topic}. Viewer discretion is advised.")
    
    try:
        title = title_template.format(topic=topic)
        description = description_template.format(topic=topic)
    except KeyError as e:
        print(f"Advertencia: Placeholder {e} no encontrado en template. Usando template original.")
        title = title_template
        description = description_template
    
    return title, description

if __name__ == "__main__":
    try:
        p = argparse.ArgumentParser()
        p.add_argument("--config", required=True)
        args = p.parse_args()
        cfg = load_config(args.config)
        outdir = cfg.get("output_dir", "outputs")
        
        video_path = os.path.join(outdir, "final.mp4")
        if not os.path.exists(video_path):
            raise SystemExit(f"Error: No se encontró el video en {video_path}. Ejecuta make_video.py primero.")

        # Verificar credenciales de YouTube
        client_id = os.getenv("YOUTUBE_CLIENT_ID")
        client_secret = os.getenv("YOUTUBE_CLIENT_SECRET")
        refresh_token = os.getenv("YOUTUBE_REFRESH_TOKEN")
        
        if not (client_id and client_secret and refresh_token):
            raise SystemExit("Error: Faltan credenciales de YouTube. Configura las variables de entorno: YOUTUBE_CLIENT_ID, YOUTUBE_CLIENT_SECRET, YOUTUBE_REFRESH_TOKEN")

        # Obtener token de acceso
        try:
            token_info = get_credentials_from_refresh(client_id, client_secret, refresh_token)
            access_token = token_info.get("access_token")
            if not access_token:
                raise SystemExit("Error: No se pudo obtener el token de acceso")
        except SystemExit:
            raise
        except Exception as e:
            raise SystemExit(f"Error al obtener credenciales: {e}")

        # Crear cliente de YouTube
        try:
            creds = Credentials(token=access_token, refresh_token=refresh_token,
                              token_uri="https://oauth2.googleapis.com/token",
                              client_id=client_id, client_secret=client_secret)
            youtube = build("youtube", "v3", credentials=creds)
        except Exception as e:
            raise SystemExit(f"Error al crear cliente de YouTube: {e}")

        # Procesar templates
        title, description = process_templates(cfg)

        # Preparar datos del video
        body = {
            "snippet": {
                "title": title,
                "description": description,
                "tags": ["horror", "crime", "AI", "story"],
                "categoryId": "24"
            },
            "status": {"privacyStatus": "private"}
        }

        # Subir video
        try:
            media = MediaFileUpload(video_path, chunksize=-1, resumable=True, mimetype='video/mp4')
            req = youtube.videos().insert(part="snippet,status", body=body, media_body=media)
            res = None
            
            print("Iniciando subida del video...")
            while res is None:
                status, res = req.next_chunk()
                if status:
                    print(f"Progreso de subida: {int(status.progress() * 100)}%")
            
            print("Subida completada. ID del video:", res.get("id"))
            
        except Exception as e:
            raise SystemExit(f"Error al subir el video: {e}")
            
    except SystemExit:
        raise
    except Exception as e:
        raise SystemExit(f"Error inesperado: {e}")
