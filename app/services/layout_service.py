
from email.mime import text
from pydoc import text
from pdfminer.high_level import extract_text

def extract_layout(pdf_path: str):
    text = extract_text(pdf_path)

#    return text.strip() # instead of breaking at page boundaries, we will return the entire text and split it into pages based on form feed characters (\f) which is a common page delimiter in PDFs.
#    print("=" * 80)
    print("Total extracted text length:", len(text))
#    print(text[:1000])
#    print(repr(text[:500]))
#    print("=" * 80)

    pages = text.split("\f")  # basic page split fallback

#    for i, page in enumerate(pages):
#        print(f"Page {i+1} length = {len(page)}")
#        print(page[:300])
    
    layouts = []
    for i, page in enumerate(pages):
        layouts.append({
            "page": i + 1,
            "text": page.strip()
        })

    return layouts
