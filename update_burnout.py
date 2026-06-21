import re

with open('/data/workspace/projects/neurovibe/static/verktyg-burnout-kalkylator.html', 'r', encoding='utf-8') as f:
    content = f.read()

# Add endpoint call and data capture inside calculateRisk, before updateUI
capture_code = """
            // Data capture
            const burnoutData = {
                sensoryLoad,
                cognitiveLoad,
                workHours,
                sleepQuality,
                hyperfocusTime,
                maskingLevel,
                riskPercentage
            };
            
            fetch('/api/burnout-data', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify(burnoutData)
            }).catch(e => console.log('Data capture failed'));
            
            updateUI(riskPercentage, sensoryLoad, maskingLevel, totalRecovery);
"""

new_content = re.sub(r'updateUI\(riskPercentage,\s*sensoryLoad,\s*maskingLevel,\s*totalRecovery\);', capture_code, content)

with open('/data/workspace/projects/neurovibe/static/verktyg-burnout-kalkylator.html', 'w', encoding='utf-8') as f:
    f.write(new_content)
