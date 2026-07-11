with open('PROGRESS_LOG.md', 'r', encoding='utf-8') as f:
    lines = f.readlines()

new_line = "2026-07-11 | LEADFLOW/DATA | Förbättrad UX och data capture; AI-disclaimer rekrytering | Leadflow & AI | nästa: Implementera backend för ny UX tracker\n"
if "2026-07-11" not in lines[0]:
    with open('PROGRESS_LOG.md', 'w', encoding='utf-8') as f:
        f.write(new_line)
        f.writelines(lines)
