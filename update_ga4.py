filepath = '/data/workspace/projects/neurovibe/static/arbetsgivarpaketet.html'
with open(filepath, 'r') as f:
    content = f.read()

ga4_snippet = """
    <!-- Google tag (gtag.js) -->
    <script async src="https://www.googletagmanager.com/gtag/js?id=G-YJG1D5GJPR"></script>
    <script>
      window.dataLayer = window.dataLayer || [];
      function gtag(){dataLayer.push(arguments);}
      gtag('js', new Date());
      gtag('config', 'G-YJG1D5GJPR');
    </script>
</head>
"""

if "G-YJG1D5GJPR" not in content:
    content = content.replace("</head>", ga4_snippet)
    with open(filepath, 'w') as f:
        f.write(content)
    print("Added GA4.")
else:
    print("GA4 already present.")
