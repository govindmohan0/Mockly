import os
import whisper

import warnings
warnings.simplefilter("ignore", category=FutureWarning)

model = whisper.load_model("base")
result = model.transcribe("audio.mp3")
print(result["text"])