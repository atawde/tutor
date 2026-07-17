import re

def extract_chapters(layouts):
    chapters = []
    current_chapter = None

    chapter_pattern = re.compile(
        r"(chapter\s*\d+|ch\s*\d+|unit\s*\d+|^\d+\.\s+.+)",
        re.IGNORECASE | re.MULTILINE
    )

    print(f"Extracting chapters from {len(layouts)} pages")

    for page in layouts:
        text = page["text"]

        lines = text.split("\n")

        for line in lines:
            match = chapter_pattern.search(line)

            if match:
                if current_chapter:
                    chapters.append(current_chapter)

                current_chapter = {
                    "title": match.group().strip(),
                    "pages": [],
                    "text": ""
                }

        if current_chapter:
            current_chapter["pages"].append(page["page"])
            current_chapter["text"] += text + "\n"

    if current_chapter:
        chapters.append(current_chapter)

    print(f"Finished extracting chapters: {len(chapters)}")
    return chapters
