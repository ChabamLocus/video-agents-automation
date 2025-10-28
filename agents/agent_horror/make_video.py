import argparse, json, os
from moviepy.editor import AudioFileClip, ColorClip

def load_config(path):
    return json.load(open(path,'r',encoding='utf-8'))

if __name__ == "__main__":
    p = argparse.ArgumentParser()
    p.add_argument("--config", required=True)
    args = p.parse_args()
    cfg = load_config(args.config)
    outdir = cfg.get("output_dir","outputs")
    os.makedirs(outdir, exist_ok=True)

    audio_path = os.path.join(outdir,"narration.mp3")
    if not os.path.exists(audio_path):
        print("No audio found at", audio_path); raise SystemExit(1)

    audio = AudioFileClip(audio_path)
    clip = ColorClip(size=(1080,1920), color=(0,0,0), duration=audio.duration).set_fps(24).set_audio(audio)

    out_video = os.path.join(outdir,"final.mp4")
    clip.write_videofile(out_video, codec="libx264", audio_codec="aac", fps=24)
    print("Video created:", out_video)
