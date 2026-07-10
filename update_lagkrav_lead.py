import re

with open("static/lagkrav-anpassningar-arbetsmiljo.html", "r") as f:
    content = f.read()

# Already has lead-magnet-container, so no need to add it again
