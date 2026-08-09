#!/bin/bash
today=$(date +%Y-%m-%d)
progress_log="/data/workspace/projects/neurovibe/PROGRESS_LOG.md"

entry="$today | LEADS | Fix endpoint /api/stats/leads and database migration | Kampanj: Fix leads tracking -> >0 leads | nästa: Optimera leadsformulär conversion\n"

sed -i "1s/^/$entry/" $progress_log
