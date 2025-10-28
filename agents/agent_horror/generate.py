import argparse, json, os
from datetime import datetime
import random

def load_config(path):
    with open(path,'r',encoding='utf-8') as f:
        return json.load(f)

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
        f"Generated automatically on {datetime.utcnow().strftime('%B %d, %Y')}."
    )
    return script

if __name__ == "__main__":
    p = argparse.ArgumentParser()
    p.add_argument("--config", required=True)
    args = p.parse_args()
    cfg = load_config(args.config)
    outdir = cfg.get("output_dir","outputs")
    os.makedirs(outdir, exist_ok=True)
    script_text = generate_script(cfg)
    script_path = os.path.join(outdir, "script.txt")
    with open(script_path,"w",encoding="utf-8") as f:
        f.write(script_text)
    print("Horror script saved to", script_path)
