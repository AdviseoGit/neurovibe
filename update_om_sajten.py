import os
import glob

# Neutralize any expert copy that might be present in newly generated html files
for file in glob.glob("static/*.html"):
    with open(file, "r") as f:
        content = f.read()
    
    if "vårt team av experter" in content or "branschexperter" in content or "Våra experter" in content:
        content = content.replace("vårt team av experter", "vi")
        content = content.replace("branschexperter", "personer")
        content = content.replace("Våra experter", "Vi")
        
        with open(file, "w") as f:
            f.write(content)

