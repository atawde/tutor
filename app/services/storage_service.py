def save_script(chapter_id, script):

    path = f"media/scripts/{chapter_id}.txt"

    with open(path, "w", encoding="utf-8") as f:
        f.write(script)

    return path
