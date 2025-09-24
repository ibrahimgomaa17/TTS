import os
import re
from pathlib import Path

WAV_DIR = Path("data/wavs")         # where 001.wav, 002.wav, ... live
TXT_DIR = Path("transcripts")       # where 001.txt, 002.txt, ... live
OUT = Path("../metadata.csv")

def clean_text(s: str) -> str:
    # collapse whitespace, strip, remove pipes (|) which break CSV format for TTS
    s = s.replace("|", " ")
    s = re.sub(r"\s+", " ", s, flags=re.M).strip()
    return s

def main():
    wavs = sorted(p for p in WAV_DIR.glob("*.wav"))
    txts = sorted(p for p in TXT_DIR.glob("*.txt"))

    if not wavs or not txts:
        raise SystemExit("No WAVs or TXTs found. Check your folders.")

    # map by basename without extension (e.g., "001")
    wav_map = {p.stem: p for p in wavs}
    txt_map = {p.stem: p for p in txts}

    common = sorted(set(wav_map) & set(txt_map), key=lambda x: int(x))
    if not common:
        raise SystemExit("No matching basenames between WAVs and TXTs.")

    # warn if mismatch
    missing_txt = sorted(set(wav_map) - set(txt_map), key=lambda x: int(x))[:10]
    missing_wav = sorted(set(txt_map) - set(wav_map), key=lambda x: int(x))[:10]
    if missing_txt:
        print(f"Warning: {len(missing_txt)} WAVs have no TXT. First few: {missing_txt}")
    if missing_wav:
        print(f"Warning: {len(missing_wav)} TXTs have no WAV. First few: {missing_wav}")

    OUT.parent.mkdir(parents=True, exist_ok=True)
    with OUT.open("w", encoding="utf-8", newline="\n") as f:
        for key in common:
            text = txt_map[key].read_text(encoding="utf-8", errors="ignore")
            text = clean_text(text)
            f.write(f"{key}.wav|{text}\n")

    print(f"Done. Wrote {OUT} with {len(common)} lines.")

if __name__ == "__main__":
    main()
