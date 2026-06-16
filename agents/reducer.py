from utils.file_io import save_markdown


def reducer(state):
    title = state["plan"].blog_title
    body = "\n\n".join(state["sections"]).strip()
    final_md = f"# {title}\n\n{body}\n"
    save_markdown(title, final_md)
    return {"final": final_md}
