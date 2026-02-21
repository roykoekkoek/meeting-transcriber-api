# Meeting Transcriber API

A FastAPI service that accepts `.mp4` meeting recordings, extracts the audio, and transcribes it using the `gpt-4o-mini-transcribe` model via Azure AI Foundry.

## How it works

1. Receives an `.mp4` file
2. Strips the audio track to `.mp3` using `ffmpeg`
3. Splits the audio into 5-minute chunks to stay within API limits
4. Sends each chunk to the Azure AI Foundry transcription API
5. Returns the concatenated transcript

## Requirements

- Python >= 3.10
- [ffmpeg](https://ffmpeg.org/) installed and available on `PATH`
- An Azure AI Foundry deployment of `gpt-4o-mini-transcribe`

## Setup

1. Clone the repository and create a virtual environment:

   ```bash
   python -m venv .venv
   source .venv/bin/activate  # Windows: .venv\Scripts\activate
   pip install -e .
   ```

2. Copy `.env.example` to `.env` and fill in your credentials:

   ```bash
   cp .env.example .env
   ```

   Required environment variables:

   | Variable | Description |
   |---|---|
   | `AZURE_AI_FOUNDRY_URL` | Base URL of your Azure AI Foundry endpoint |
   | `AZURE_AI_FOUNDRY_API_KEY` | API key for authentication |

## Running

```bash
uvicorn app:app --reload
```

## Dependencies

| Package | Purpose |
|---|---|
| `fastapi` | Web framework / API layer |
| `pydub` | Audio chunking |
| `requests` | HTTP calls to Azure AI Foundry |
| `python-dotenv` | Loading environment variables |
