from graphs.blog_graph import build_graph

app = build_graph()

result = app.invoke({"topic": "Write a blog on self attention"})

print(result["final"])