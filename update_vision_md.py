import os

file_path = "/data/workspace/projects/neurovibe/SITE_VISION.md"

with open(file_path, "r") as f:
    content = f.read()

# Update the status of "Producera arbetsgivarpaketets fem dokument"
content = content.replace(
    "    - [ ] Producera arbetsgivarpaketets fem dokument.\n",
    "    - [x] Producera arbetsgivarpaketets fem dokument.\n"
)

with open(file_path, "w") as f:
    f.write(content)
print("Updated SITE_VISION.md")
