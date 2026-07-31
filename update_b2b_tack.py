import os

file_path = "/data/workspace/projects/neurovibe/static/tack.html"
with open(file_path, "r") as f:
    content = f.read()

# Make sure it links properly to the actual document and is correctly labelled
content = content.replace("'/arbetsgivarpaketet.html'", "'/arbetsgivarpaketet.html'")

with open(file_path, "w") as f:
    f.write(content)
print("Updated tack.html")
