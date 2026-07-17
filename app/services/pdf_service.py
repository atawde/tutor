import fitz

def extract_pages(pdf_path):

    doc = fitz.open(pdf_path)

    pages = []

    for page_no, page in enumerate(doc):

        text = page.get_text()

        pages.append({
            "page_number": page_no,
            "text": text
        })

    return pages

