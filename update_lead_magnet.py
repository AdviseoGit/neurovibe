with open('/data/workspace/projects/neurovibe/static/lead-magnet-snippet.html', 'r') as f:
    content = f.read()

# Since it is just a snippet included in other pages, it shouldn't have its own footer.
# But wait, the update_footer script checked *all* html files.
