import re

file_path = "/data/workspace/projects/neurovibe/static/verktyg-burnout-kalkylator.html"
with open(file_path, "r", encoding="utf-8") as f:
    content = f.read()

lead_html = """
    <!-- Lead Magnet Integration -->
    <div class="glass-panel p-8 md:p-12 mt-12 mb-12 max-w-4xl mx-auto text-center relative overflow-hidden" style="background: rgba(255, 255, 255, 0.02); backdrop-filter: blur(30px); border: 1px solid rgba(255, 255, 255, 0.05); border-radius: 24px;">
        <div class="neuro-accent-blur absolute top-1/2 left-1/2 transform -translate-x-1/2 -translate-y-1/2" style="width: 200px; height: 200px; opacity: 0.5;"></div>
        <div class="relative z-10">
            <h3 class="text-2xl font-bold text-white mb-4">Få tillgång till "Burnout Rescue Guide" (PDF)</h3>
            <p class="text-[#A0A0A0] mb-8 max-w-2xl mx-auto">
                Ligger du i riskzonen? Ladda ner vår gratis 12-sidiga guide om hur du omedelbart kan sänka den kognitiva belastningen på jobbet — inklusive färdiga manus för hur du pratar med din chef om anpassningar.
            </p>
            <form id="burnout-lead-form" class="max-w-md mx-auto flex flex-col sm:flex-row gap-4">
                <input type="email" placeholder="Din e-postadress" required class="flex-grow bg-black/50 border border-white/10 px-4 py-3 rounded-xl text-white outline-none focus:border-[#D83131]">
                <button type="submit" class="bg-[#D83131] hover:bg-[#B72A2A] text-white font-bold py-3 px-6 rounded-xl transition-colors whitespace-nowrap">
                    Skicka guiden
                </button>
            </form>
            <div id="burnout-success" class="hidden mt-4 text-[#D83131] font-bold">Guiden skickas till din e-post inom kort!</div>
        </div>
    </div>
"""

script_html = """
    <script>
        const leadForm = document.getElementById('burnout-lead-form');
        if (leadForm) {
            leadForm.addEventListener('submit', async (e) => {
                e.preventDefault();
                const email = e.target.querySelector('input[type="email"]').value;
                const btn = e.target.querySelector('button');
                btn.disabled = true;
                btn.textContent = "Skickar...";
                
                try {
                    await fetch('/api/lead', {
                        method: 'POST',
                        headers: { 'Content-Type': 'application/json' },
                        body: JSON.stringify({ email: email, source: 'burnout_calculator_lead' })
                    });
                    e.target.style.display = 'none';
                    document.getElementById('burnout-success').style.display = 'block';
                } catch(err) {
                    btn.disabled = false;
                    btn.textContent = "Försök igen";
                }
            });
        }
    </script>
"""

if "<!-- Lead Magnet Integration -->" not in content and "<!-- Footer -->" in content:
    content = content.replace("<!-- Footer -->", f"{lead_html}\n<!-- Footer -->")
    
    if "</body>" in content:
        content = content.replace("</body>", f"{script_html}\n</body>")
        
    with open(file_path, "w", encoding="utf-8") as f:
        f.write(content)
    print("Burnout kalkylatorn uppdaterades med Lead Magnet före footern.")
else:
    print("Lead magnet finns redan eller Footer saknas.")

