import re

def read_file(path):
    with open(path, "r", encoding="utf-8") as f:
        return f.read()

def write_file(path, content):
    with open(path, "w", encoding="utf-8") as f:
        f.write(content)

md_content = read_file("/data/workspace/projects/neurovibe/content/arbetsprovning-2026-forsakringskassan.md")

# Convert md to simple html
html_content = ""
for line in md_content.split("\n"):
    line = line.strip()
    if not line:
        continue
    if line.startswith("### "):
        html_content += f"<h3 class=\"text-xl font-bold mt-6 mb-3 text-gray-800\">{line[4:]}</h3>\n"
    elif line.startswith("## "):
        html_content += f"<h2 class=\"text-2xl font-bold mt-8 mb-4 text-gray-900\">{line[3:]}</h2>\n"
    elif line.startswith("# "):
        pass # Handle H1 separately
    elif line.startswith("- ") or line.startswith("* "):
        # Bold handling in list
        import re
        item = re.sub(r"\*\*(.*?)\*\*", r"<strong>\1</strong>", line[2:])
        # Link handling
        item = re.sub(r"\[(.*?)\]\((.*?)\)", r"<a href=\"\2\" class=\"text-indigo-600 hover:underline\">\1</a>", item)
        html_content += f"<li class=\"ml-4 text-gray-700 mb-1\">{item}</li>\n"
    elif line[0].isdigit() and line[1:3] == ". ":
        import re
        item = re.sub(r"\*\*(.*?)\*\*", r"<strong>\1</strong>", line[3:])
        item = re.sub(r"\[(.*?)\]\((.*?)\)", r"<a href=\"\2\" class=\"text-indigo-600 hover:underline\">\1</a>", item)
        html_content += f"<li class=\"ml-4 text-gray-700 mb-1\">{item}</li>\n"
    else:
        # Bold handling
        import re
        line = re.sub(r"\*\*(.*?)\*\*", r"<strong>\1</strong>", line)
        line = re.sub(r"\[(.*?)\]\((.*?)\)", r"<a href=\"\2\" class=\"text-indigo-600 hover:underline\">\1</a>", line)
        html_content += f"<p class=\"mb-4 text-gray-700\">{line}</p>\n"


template = f"""<!DOCTYPE html>
<html lang="sv">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Arbetsprövning 2026: Nya möjligheter med Försäkringskassan - Neurovibe</title>
    <meta name="description" content="Allt om Försäkringskassans nya regler för arbetsprövning 2026. Lär dig hur du kan testa din arbetsförmåga med bibehållen sjukpenning om du har NPF/ADHD.">
    <script src="https://cdn.tailwindcss.com"></script>
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap" rel="stylesheet">
    <style>
        body {{ font-family: 'Inter', sans-serif; }}
    </style>
    <!-- Structured data -->
    <script type="application/ld+json">
    {{
      "@context": "https://schema.org",
      "@type": "Article",
      "headline": "Arbetsprövning 2026: Nya möjligheter för dig med ADHD och NPF",
      "description": "Allt om Försäkringskassans nya regler för arbetsprövning 2026. Lär dig hur du kan testa din arbetsförmåga med bibehållen sjukpenning om du har NPF/ADHD.",
      "author": {{
        "@type": "Organization",
        "name": "Neurovibe"
      }}
    }}
    </script>
</head>
<body class="bg-gray-50 text-gray-800">

    <header class="bg-white shadow-sm">
        <div class="container mx-auto px-4 py-4 flex justify-between items-center">
            <a href="/index.html" class="text-2xl font-bold text-indigo-600">Neurovibe</a>
            <nav>
                <a href="/resurser.html" class="text-gray-600 hover:text-indigo-600 px-3 py-2">Resurser</a>
                <a href="/om-sajten.html" class="text-gray-600 hover:text-indigo-600 px-3 py-2">Om oss</a>
            </nav>
        </div>
    </header>

    <main class="container mx-auto px-4 py-12">
        <article class="max-w-3xl mx-auto bg-white p-8 rounded-lg shadow">
            <h1 class="text-4xl font-bold mb-4 text-gray-900">Arbetsprövning 2026: Nya möjligheter för dig med ADHD och NPF</h1>
            
            <div class="ad-slot my-8 p-4 bg-gray-100 rounded-md text-center">
                <p class="text-sm text-gray-500">Annonsplats</p>
            </div>
            
            {html_content}

        </article>
    </main>

    <footer class="bg-white mt-12 border-t border-gray-200">
        <div class="container mx-auto px-4 py-6 text-center text-gray-500">
            <p>&copy; 2026 Neurovibe. Alla rättigheter förbehållna.</p>
        </div>
    </footer>
</body>
</html>
"""

write_file("/data/workspace/projects/neurovibe/static/arbetsprovning-2026-forsakringskassan.html", template)
print("Article created.")
