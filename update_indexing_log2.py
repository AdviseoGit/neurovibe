with open('/data/workspace/projects/neurovibe/INDEXING_LOG.md', 'r') as f:
    content = f.read()

# removing lines for the ones we just added to sitemap on 2026-07-19, assume they'll get crawled. 
# actually let's leave them until they confirm indexed.
