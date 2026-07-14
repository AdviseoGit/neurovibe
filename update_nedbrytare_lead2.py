import re

file_path = "/data/workspace/projects/neurovibe/static/verktyg-nedbrytare.html"
with open(file_path, "r", encoding="utf-8") as f:
    content = f.read()

lead_html = """
    <!-- Lead Magnet Integration -->
    <div class="glass-panel p-8 md:p-12 mt-12 mb-12 max-w-4xl mx-auto text-center relative overflow-hidden" style="background: rgba(255, 255, 255, 0.02); backdrop-filter: blur(30px); border: 1px solid rgba(255, 255, 255, 0.05); border-radius: 24px;">
        <div class="neuro-accent-blur absolute top-1/2 left-1/2 transform -translate-x-1/2 -translate-y-1/2" style="width: 200px; height: 200px; opacity: 0.5;"></div>
        <div class="relative z-10">
            <h3 class="text-2xl font-bold text-white mb-4">Gör det osynliga synligt – Ladda ner vår mall</h3>
            <p class="text-[#A0A0A0] mb-8 max-w-2xl mx-auto">
                Svårt att förklara för chefen varför vissa uppgifter dränerar dig? Ladda ner vår PDF-mall för <strong>Kognitiv Belastningskartläggning</strong> för att tydligt visa var dina flaskhalsar finns och vilka anpassningar du behöver.
            </p>
            <form id="nedbrytare-lead-form" class="max-w-md mx-auto flex flex-col sm:flex-row gap-4">
                <input type="email" placeholder="Din e-postadress" required class="flex-grow bg-black/50 border border-white/10 px-4 py-3 rounded-xl text-white outline-none focus:border-[#D83131]">
                <button type="submit" class="bg-[#D83131] hover:bg-[#B72A2A] text-white font-bold py-3 px-6 rounded-xl transition-colors whitespace-nowrap">
                    Skicka mallen
                </button>
            </form>
            <div id="nedbrytare-success" class="hidden mt-4 text-[#D83131] font-bold">Mallen skickas till din e-post inom kort!</div>
        </div>
    </div>
"""

script_html = """
    <script>
        const nLeadForm = document.getElementById('nedbrytare-lead-form');
        if (nLeadForm) {
            nLeadForm.addEventListener('submit', async (e) => {
                e.preventDefault();
                const email = e.target.querySelector('input[type="email"]').value;
                const btn = e.target.querySelector('button');
                btn.disabled = true;
                btn.textContent = "Skickar...";
                
                try {
                    await fetch('/api/lead', {
                        method: 'POST',
                        headers: { 'Content-Type': 'application/json' },
                        body: JSON.stringify({ email: email, source: 'nedbrytare_lead' })
                    });
                    e.target.style.display = 'none';
                    document.getElementById('nedbrytare-success').style.display = 'block';
                } catch(err) {
                    btn.disabled = false;
                    btn.textContent = "Försök igen";
                }
            });
        }
    </script>
"""

if "<!-- Lead Magnet Integration -->" not in content and "<footer" in content:
    content = content.replace("<footer", f"{lead_html}\n<footer")
    
    if "</body>" in content:
        content = content.replace("</body>", f"{script_html}\n</body>")
        
    with open(file_path, "w", encoding="utf-8") as f:
        f.write(content)
    print("Nedbrytare uppdaterades med Lead Magnet före footern.")
else:
    print("Lead magnet finns redan.")

