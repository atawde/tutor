def generate_commentary(chapter):

    prompt = f"""
    Explain the following chapter
    in student-friendly language.

    Title:
    {chapter['title']}

    Content:
    {chapter['content']}
    """

    commentary = llm_call(prompt)
    #commentary = f"Commentary for {chapter['title']}"

    return commentary