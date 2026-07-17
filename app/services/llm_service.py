from openai import OpenAI

client = OpenAI()

def generate_commentary(text: str) -> str:
    prompt = f"""
        You are a teacher explaining school textbook content.

        Explain the following content in a simple, clear way for students.

        TEXT: {text}

        Return only the explanation.
    """

    #return "Mock commentary for testing: " + text[:100]  # Placeholder for actual LLM call

    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.5
    )

    content = response.choices[0].message.content
    # Ensure we always return a string (API may return None)
    if content is None:
        return ""
    return content

def generate_narration(commentary: str) -> str:
    prompt = f"""
        Convert the following educational explanation into a natural spoken script for audio lessons.

        Rules:
        - Use simple spoken English
        - Add pauses and transitions
        - Make it engaging like a teacher speaking
        - Do NOT include headings or bullet points

        CONTENT:
        {commentary}
    """

    #return "Mock narration: " + commentary[:100] # Placeholder for actual LLM call

    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.6
    )

    return response.choices[0].message.content or ""
