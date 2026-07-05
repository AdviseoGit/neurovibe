#!/bin/bash
for file in /data/workspace/projects/neurovibe/static/*.html; do
    if grep -q "Denna sajt skapas och drivs helt av AI" "$file"; then
        echo "OK: $file"
    else
        echo "MISSING: $file"
        # Om filen har en </footer>, infoga AI-texten
    fi
done
