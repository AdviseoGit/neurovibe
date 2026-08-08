#!/bin/bash
DATE=$(date +%Y-%m-%d)
COMMIT_MSG="GEO: Optimerade arbetsplats-schema-npf.html med siffror och jämförelsetabell"
echo "$DATE | GEO | Optimerade arbetsplats-schema-npf.html med siffror och jämförelsetabell | AI-citerbarhet och AI-svar synlighet | nästa: Optimera leadflow från formulär" > /tmp/progress_entry
cat /tmp/progress_entry /data/workspace/projects/neurovibe/PROGRESS_LOG.md > /tmp/progress_log.md
mv /tmp/progress_log.md /data/workspace/projects/neurovibe/PROGRESS_LOG.md
bash /data/workspace/skills/site-updater/scripts/git_sync.sh /data/workspace/projects/neurovibe "$COMMIT_MSG"
