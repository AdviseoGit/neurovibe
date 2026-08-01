import os
import re

file_path = "/data/workspace/projects/neurovibe/static/arbetsgivarpaketet.html"
if os.path.exists(file_path):
    print("arbetsgivarpaketet.html exists")
else:
    print("Does not exist")
