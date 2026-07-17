from app.services.pdf_service import convert_pdf_to_images
from app.services.layout_service import analyze_pages
from app.services.narration_service import build_narration
from app.services.tts_service import generate_audio

def process_pdf_task(pdf_path):

    pages = convert_pdf_to_images(pdf_path)

    structured_pages = analyze_pages(pages)

    narration_script = build_narration(structured_pages)

    audio_path = generate_audio(narration_script)

    return audio_path