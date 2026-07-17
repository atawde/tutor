from ..services.llm_service import (
    generate_commentary,
    generate_narration
)

from ..db.session import SessionLocal
from ..services.audio_service import text_to_audio
from ..services.layout_service_v2 import extract_layout
from ..services.chapter_service import extract_chapters

from ..models.audio_lesson import AudioLesson
from ..models.job import ProcessingJob

def process_chapter(job_id): #subject_id, chapter_title, chapter_text):

    chapters = []
    lessons = []
    db = SessionLocal()   # 🔥 create fresh session
    job = db.query(ProcessingJob).get(job_id)
    subject_id = job.subject_id
    pdf_path = job.pdf_path
    job.status = "processing"
    db.commit()

    
    try:
        print(f"pipeline start for job {job_id}") 


        # extract chapters here
        layouts = extract_layout(pdf_path)

#        for i, layout in enumerate(layouts):
#           print("Page", layout["page"])
#           print("Length:", len(layout["text"]))
#           print(repr(layout["text"][:300]))

        print(f"Extracted layouts: {len(layouts)} pages")

        chapters = [
            {
                "title": f"Page {layout['page']}",
                "pages": [layout["page"]],
                "text": layout["text"]
            }
            for layout in layouts
            if layout["text"].strip()
        ]
#        chapters = extract_chapters(layouts)  commented out for now, as we are using each page as a chapter

#        for j, chapter in enumerate(chapters):
#            print("=" * 80)
#            print("TITLE:", chapter["title"])
#            print("TEXT LENGTH:", len(chapter["text"]))
#            print(repr(chapter["text"][:500]))

        print(f"Extracted chapters: {len(chapters)}")
    
    except Exception as e:
        job.status = "failed"
        db.commit()
        print("PIPELINE ERROR:", e)
    
    for chapter in chapters:
        try:
            # 1. LLM Commentary
            commentary = generate_commentary(chapter["text"])
            # 2. LLM Narration
            narration = generate_narration(commentary)
            # 3. TTS
            audio_path = text_to_audio(narration)
            # 4. Save DB
            lesson = AudioLesson(
                subject_id=subject_id,
                chapter_title=chapter["title"],
                narration_text=narration,
                audio_url=audio_path
            )

            db.add(lesson)
            db.commit()
            lessons.append(lesson)

        except Exception as e:
            job.status = "failed"
            db.commit()
            print(f"Error occurred: {e}")
            raise

    job.status = "completed"
    db.commit()
    db.close()
    return lessons
    
