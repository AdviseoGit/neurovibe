import re
with open('/data/workspace/projects/neurovibe/static/data-rapport-2026.html', 'r') as f:
    content = f.read()

new_form = """<form data-nv-lead data-segment="arbetsgivare" data-offer="b2b-datarapport" data-redirect="auto" data-error="#report-error" class="max-w-md mx-auto flex flex-col gap-4 text-left">
                        <input type="email" name="email" placeholder="Din e-postadress" required class="bg-black/50 border border-white/10 px-4 py-3 rounded-xl text-white outline-none focus:border-[#D83131] w-full">
                        <div class="flex gap-3 items-start pt-2">
                            <input type="checkbox" id="report-consent" name="consent" required class="mt-1 w-4 h-4 accent-[#D83131] cursor-pointer">
                            <label for="report-consent" class="text-sm text-[#909090] leading-snug cursor-pointer">
                                Jag godkänner att Neurovibe sparar min e-postadress för att skicka rapporten och enstaka uppdateringar. <a href="/integritetspolicy.html" class="text-[#D83131] hover:underline">Integritetspolicy</a>.
                            </label>
                        </div>
                        <button type="submit" class="bg-[#D83131] hover:bg-[#B72A2A] text-white font-bold py-3 px-6 rounded-xl transition-colors w-full">
                            Skicka rapporten
                        </button>
                        <div id="report-error" class="hidden text-[#FF6B6B] text-sm"></div>
                    </form>
                    <div id="report-success" class="hidden mt-4 text-[#D83131] font-bold">Rapporten skickas till din e-post!</div>"""

old_form_regex = r'<form id="report-lead-form".*?</form>\s*<p class="nv-privacy-note"[^>]*>.*?</p>\s*<div id="report-success"[^>]*>.*?</div>'
content = re.sub(old_form_regex, new_form, content, flags=re.DOTALL)
content = re.sub(r'<script>\s*document\.getElementById\(\'report-lead-form\'\).*?</script>', '', content, flags=re.DOTALL)
if '<script src="/static/leadflow.js" defer></script>' not in content:
    content = content.replace('</body>', '<script src="/static/leadflow.js" defer></script>\n</body>')
with open('/data/workspace/projects/neurovibe/static/data-rapport-2026.html', 'w') as f:
    f.write(content)
