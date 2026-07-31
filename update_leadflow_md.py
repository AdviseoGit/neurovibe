import os

file_path = "/data/workspace/projects/neurovibe/LEADFLOW.md"

with open(file_path, "r") as f:
    content = f.read()

# Update the status of "Producera arbetsgivarpaketets fem dokument"
content = content.replace(
    "- [ ] Producera arbetsgivarpaketets fem dokument (avsnitt 3)",
    "- [x] Producera arbetsgivarpaketets fem dokument (avsnitt 3)"
)

with open(file_path, "w") as f:
    f.write(content)
print("Updated LEADFLOW.md")
