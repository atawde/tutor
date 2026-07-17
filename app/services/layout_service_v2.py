from pdfminer.high_level import extract_text

def extract_layout(pdf_path: str):
    text = extract_text(pdf_path)

    pages = text.split("\f")  # basic page split fallback

    layouts = []
    for i, page in enumerate(pages):
        layouts.append({
            "page": i + 1,
            "text": page.strip()
        })

    return layouts
