import argparse, json, os
from gtts import gTTS

def load_config(path):
    return json.load(open(path,'r',encoding='utf-8'))

if __name__ == "__main__":
    p = argparse.ArgumentParser()
    p.add_argument("--config", required=True)
    args = p.parse_args()
    cfg = load_config(args.config)
    outdir = cfg.get("output_dir","outputs")
    os.makedirs(outdir, exist_ok=True)
    script_path = os.path.join(outdir,"script.txt")
    if not os.path.exists(script_path):
        raise SystemExit("No script found. Run generate.py first.")
    with open(script_path,"r",encoding="utf-8") as f:
        text = f.read()
    lang = cfg.get("language","en")
    tts = gTTS(text=text, lang=lang)
    out_audio = os.path.join(outdir,"narration.mp3")
    tts.save(out_audio)
    print("Audio saved to", out_audio)
