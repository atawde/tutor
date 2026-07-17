from pathlib import Path
from openai import OpenAI
from uuid import uuid4

client = OpenAI()

OUTPUT_DIR = Path("output/audio")
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

def text_to_audio(text: str):

    filename = f"{uuid4()}.mp3"
    output_path = OUTPUT_DIR / filename

    with client.audio.speech.with_streaming_response.create(
        model="gpt-4o-mini-tts",
        voice="alloy",
        input=text,
    ) as response:
        response.stream_to_file(output_path)

    return str(output_path)
