import requests
from pydub import AudioSegment
from io import BytesIO
from dotenv import load_dotenv
import os
import json
from subprocess import run

load_dotenv()

#Path to mp4. Needs to be replaced with HTTP POST input
path = "local/Bellen met Raygene Petroudis-20251209_111207-Opname van vergadering"

run([
    "ffmpeg", "-i", f"{path}.mp4",
    "-vn",           # drop video
    "-acodec", "mp3",
    "-q:a", "0",     # quality (0=best, 9=worst)
    f"{path}.mp3"
], check=True)

# Load audio
audio = AudioSegment.from_mp3("local/Bellen met Raygene Petroudis-20251209_111207-Opname van vergadering.mp3")

# Split into 5-minute chunks because of API limits
chunk_length_ms = 5 * 60 * 1000
chunks = [audio[i:i + chunk_length_ms] for i in range(0, len(audio), chunk_length_ms)]

url = f"{os.getenv("AZURE_AI_FOUNDRY_URL")}/openai/deployments/gpt-4o-mini-transcribe/audio/transcriptions?api-version=2025-03-01-preview"
headers = {"Authorization": f"Bearer {os.getenv("AZURE_AI_FOUNDRY_API_KEY")}"}

results = []
for i, chunk in enumerate(chunks):
    print(f"Busy with chunk {i}")
    buffer = BytesIO()
    chunk.export(buffer, format="mp3")
    buffer.seek(0)

    response = requests.post(
        url,
        headers=headers,
        files={"file": (f"chunk_{i}.mp3", buffer, "audio/mpeg")},
        data={
            "model": "gpt-4o-mini-transcribe",
        },
    )
    results.append(response.json())
    print(f"Chunk {i+1}/{len(chunks)} done")

with open("local/result.txt", "w") as f:
    for fragment in results:
        f.write(fragment["text"])

