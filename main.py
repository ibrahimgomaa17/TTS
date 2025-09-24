# import re
# import torch
# from TTS.tts.configs.xtts_config import XttsConfig
# from TTS.tts.models.xtts import XttsAudioConfig, XttsArgs
# from TTS.config.shared_configs import BaseDatasetConfig
# from TTS.api import TTS

# # Allow-list XTTS classes for torch serialization
# torch.serialization.add_safe_globals([XttsConfig, XttsAudioConfig, BaseDatasetConfig, XttsArgs])

# # Initialize TTS
# tts = TTS("tts_models/en/ljspeech/vit")

# # Original text
# text = "At the story's opening, Commander Yu prepares his soldiers to attack the invading Japanese army. However, as his wife makes her way through the sorghum fields with food for the soldiers, she is shot and killed by the Japanese. Her death forges a link in the novel between the past and the present. As the story progresses, the unnamed narrator (the grandson of Commander Yu) reminisces about the history of his family and the conflicts they participated in during the war. He describes how his grandmother was forced to marry the son of a rich distillery owner. Because his grandfather, who was a bandit, had already fallen in love with her, he murders the distillery owner's son. Thus, his grandmother takes over the business, and the narrator recounts in another memory the reasons why their wine is so good."

# # Insert a 1 second pause (<break time="1000ms"/>) after each sentence
# processed_text = re.sub(r'([.!?])', r'\1 <break time="3000ms"/>', text)

# # Save audio with pauses
# tts.tts_to_file(
#     text=processed_text,
#     speaker_wav="audio.wav",  # your clean sample
#     file_path="out.wav",
#     speed=0.85,
# )


# kokoro_run.py
from kokoro import KPipeline
import soundfile as sf

# 'a' means auto-detect; you can also try explicit codes like 'en', 'es', 'fr', 'de', 'it', etc.
pipeline = KPipeline(lang_code='a')

text = '''
At the story's opening, Commander Yu prepares his soldiers to attack the invading Japanese army. However, as his wife makes her way through the sorghum fields with food for the soldiers, she is shot and killed by the Japanese. Her death forges a link in the novel between the past and the present. As the story progresses, the unnamed narrator (the grandson of Commander Yu) reminisces about the history of his family and the conflicts they participated in during the war. He describes how his grandmother was forced to marry the son of a rich distillery owner. Because his grandfather, who was a bandit, had already fallen in love with her, he murders the distillery owner's son. Thus, his grandmother takes over the business, and the narrator recounts in another memory the reasons why their wine is so good.
'''

# Try different voices, e.g., 'af_heart', 'af_bella', 'am_michael', 'bf_emma', etc., depending on the Kokoro build.
generator = pipeline(text, voice='af_heart')

for i, (graphemes, phonemes, audio) in enumerate(generator):
    print(i, graphemes, phonemes)
    sf.write(f'{i}.wav', audio, 24000)

print("Done. Wrote numbered WAV files in the current directory.")
