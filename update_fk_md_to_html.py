import markdown
import json
import re
from datetime import datetime

with open('/data/workspace/projects/neurovibe/content/arbetsprovning-2026-forsakringskassan-expanded.md', 'r', encoding='utf-8') as f:
    md_content = f.read()

# Convert markdown to HTML
html_content = markdown.markdown(md_content, extensions=['extra', 'toc'])

# Replace the internal link to point to HTML instead of MD
html_content = html_content.replace('/content/neurodiversitet-och-ai-2026.md', '/ai-verktyg-neurodiversitet.html')

article_schema = {
    "@context": "https://schema.org",
    "@type": "Article",
    "headline": "Arbetsprövning 2026: Nya möjligheter för dig med ADHD och NPF",
    "datePublished": datetime.today().strftime('%Y-%m-%d'),
    "dateModified": datetime.today().strftime('%Y-%m-%d'),
    "author": {
        "@type": "Organization",
        "name": "Neurovibe"
    },
    "publisher": {
        "@type": "Organization",
        "name": "Neurovibe",
        "logo": {
            "@type": "ImageObject",
            "url": "https://neurovibe.se/favicon.svg"
        }
    },
    "description": "Förstå Försäkringskassans nya regler 2026 för arbetsprövning med NPF, ADHD och Autism. Arbetshjälpmedel, lönebidrag och myndighetskontakter."
}

# Template
template = f"""<!DOCTYPE html>
<html lang="sv" class="bg-[#050505]">
<head>
<!-- Google tag (gtag.js) -->
<script async src="https://www.googletagmanager.com/gtag/js?id=G-YJG1D5GJPR"></script>
<script>
  window.dataLayer = window.dataLayer || [];
  function gtag(){{dataLayer.push(arguments);}}
  gtag('js', new Date());
  gtag('config', 'G-YJG1D5GJPR');
</script>

    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Arbetsprövning & Försäkringskassan 2026 (ADHD/Autism) - Neurovibe</title>
    
    <!-- Schema.org Markup -->
    <script type="application/ld+json">
{json.dumps(article_schema, indent=2, ensure_ascii=False)}
    </script>

    <meta name="description" content="Förstå Försäkringskassans nya regler 2026 för arbetsprövning med NPF, ADHD och Autism. Arbetshjälpmedel, lönebidrag och myndighetskontakter.">
    <meta name="keywords" content="arbetsprövning adhd, försäkringskassan adhd, lönebidrag npf, arbetshjälpmedel autism, sjukpenning arbetsprövning">
    <link rel="icon" href="/favicon.svg" type="image/svg+xml">
    
    <!-- Tailwind CSS -->
    <script src="https://cdn.tailwindcss.com"></script>
    <!-- Phosphor Icons -->
    <script src="https://unpkg.com/@phosphor-icons/web"></script>
    
    <style>
        body {{
            font-family: 'Inter', system-ui, -apple-system, sans-serif;
            color: #E0E0E0;
        }}
        .prose h1, .prose h2, .prose h3 {{
            color: #FFFFFF;
            font-weight: 600;
        }}
        .prose a {{
            color: #A3E635;
            text-decoration: underline;
        }}
        .prose p {{
            margin-bottom: 1.5rem;
            line-height: 1.7;
        }}
        .prose ul {{
            list-style-type: disc;
            padding-left: 1.5rem;
            margin-bottom: 1.5rem;
        }}
        .prose li {{
            margin-bottom: 0.5rem;
        }}
    </style>
</head>
<body class="min-h-screen flex flex-col antialiased">
    
    <!-- Navigation -->
    <nav class="sticky top-0 z-50 bg-[#0A0A0A]/80 backdrop-blur-md border-b border-white/10">
        <div class="max-w-6xl mx-auto px-4 sm:px-6 lg:px-8">
            <div class="flex justify-between h-16">
                <div class="flex">
                    <a href="/" class="flex-shrink-0 flex items-center gap-2">
                        <i class="ph ph-brain text-2xl text-[#A3E635]"></i>
                        <span class="text-xl font-bold text-white tracking-tight">Neurovibe</span>
                    </a>
                </div>
                <div class="hidden sm:ml-6 sm:flex sm:items-center sm:space-x-8">
                    <a href="/npf-arbetslivet.html" class="text-sm font-medium text-gray-300 hover:text-white transition-colors">NPF i Arbetslivet</a>
                    <a href="/resurser.html" class="text-sm font-medium text-gray-300 hover:text-white transition-colors">Verktyg & Resurser</a>
                    <a href="/om-sajten.html" class="text-sm font-medium text-gray-300 hover:text-white transition-colors">Om Sajten</a>
                </div>
            </div>
        </div>
    </nav>

    <!-- Main Content -->
    <main class="flex-grow pt-12 pb-24">
        <article class="max-w-3xl mx-auto px-4 sm:px-6">
            
            <header class="mb-12">
                <div class="inline-flex items-center gap-1.5 px-3 py-1 rounded-full bg-[#A3E635]/10 text-[#A3E635] text-xs font-medium mb-4 border border-[#A3E635]/20">
                    <i class="ph ph-info"></i> Guide
                </div>
                <h1 class="text-4xl sm:text-5xl font-bold text-white mb-6 leading-tight tracking-tight">Arbetsprövning 2026: Nya möjligheter för dig med ADHD och NPF</h1>
                <div class="flex items-center gap-4 text-sm text-gray-400">
                    <span class="flex items-center gap-1.5"><i class="ph ph-calendar-blank"></i> Uppdaterad: {datetime.today().strftime('%Y-%m-%d')}</span>
                    <span class="flex items-center gap-1.5"><i class="ph ph-clock"></i> Lästid: ca 8 min</span>
                </div>
            </header>

            <div class="prose prose-invert prose-lg max-w-none text-gray-300">
                {html_content}
            </div>

            <!-- Lead Magnet Snippet -->
            <div id="lead-magnet-container" class="mt-16"></div>

        </article>
    </main>

    <!-- Footer -->
    <footer class="bg-[#0A0A0A] border-t border-white/5 py-12 mt-auto">
        <div class="max-w-6xl mx-auto px-4 sm:px-6 lg:px-8">
            <div class="grid grid-cols-1 md:grid-cols-4 gap-8">
                <div class="col-span-1 md:col-span-2">
                    <a href="/" class="flex items-center gap-2 mb-4">
                        <i class="ph ph-brain text-2xl text-[#A3E635]"></i>
                        <span class="text-xl font-bold text-white">Neurovibe</span>
                    </a>
                    <p class="text-sm text-gray-400 max-w-md">
                        Målet med Neurovibe är att tillhandahålla uppdaterad, evidensbaserad information om neurodiversitet i arbetslivet,
                        och att erbjuda verktyg för både individer och arbetsgivare.
                    </p>
                </div>
                
                <div>
                    <h3 class="text-sm font-semibold text-white uppercase tracking-wider mb-4">Snabblänkar</h3>
                    <ul class="space-y-3">
                        <li><a href="/npf-arbetslivet.html" class="text-sm text-gray-400 hover:text-[#A3E635] transition-colors">Fakta om NPF</a></li>
                        <li><a href="/resurser.html" class="text-sm text-gray-400 hover:text-[#A3E635] transition-colors">Resursbibliotek</a></li>
                    </ul>
                </div>
                
                <div>
                    <h3 class="text-sm font-semibold text-white uppercase tracking-wider mb-4">Information</h3>
                    <ul class="space-y-3">
                        <li><a href="/om-sajten.html" class="text-sm text-gray-400 hover:text-[#A3E635] transition-colors">Om Neurovibe</a></li>
                        <li><a href="/integritetspolicy.html" class="text-sm text-gray-400 hover:text-[#A3E635] transition-colors">Integritet & Cookies</a></li>
                        <li><a href="mailto:hej@neurovibe.se" class="text-sm text-gray-400 hover:text-[#A3E635] transition-colors">Kontakt</a></li>
                    </ul>
                </div>
            </div>
            <div class="mt-12 pt-8 border-t border-white/5 flex flex-col md:flex-row justify-between items-center gap-4">
                <p class="text-xs text-gray-500">
                    &copy; 2026 Neurovibe.se. Utvecklat som ett fristående initiativ.
                </p>
                <!-- AI Transparency -->
                <div class="flex items-center gap-2 text-xs text-gray-500 bg-white/5 px-3 py-1.5 rounded-full border border-white/5">
                    <i class="ph ph-robot text-[#A3E635]"></i>
                    <span>Innehållet på denna sajt är framtaget med stöd av AI, men granskat av människor.</span>
                </div>
            </div>
        </div>
    </footer>

    <script>
        // Load lead magnet snippet
        fetch('/lead-magnet-snippet.html')
            .then(response => response.text())
            .then(data => {{
                document.getElementById('lead-magnet-container').innerHTML = data;
                
                const form = document.getElementById('newsletter-form');
                if (form) {{
                    form.addEventListener('submit', async (e) => {{
                        e.preventDefault();
                        const emailInput = form.querySelector('input[type="email"]');
                        const email = emailInput.value;
                        const button = form.querySelector('button');
                        const originalText = button.innerHTML;
                        
                        button.innerHTML = '<i class="ph ph-spinner animate-spin"></i> Skickar...';
                        button.disabled = true;
                        
                        try {{
                            const response = await fetch('/api/leads', {{
                                method: 'POST',
                                headers: {{ 'Content-Type': 'application/json' }},
                                body: JSON.stringify({{ email: email, source: 'guide_forsakringskassan' }})
                            }});
                            
                            if (response.ok) {{
                                button.innerHTML = '<i class="ph ph-check"></i> Skickat!';
                                button.classList.remove('bg-[#A3E635]', 'text-black', 'hover:bg-[#86CB15]');
                                button.classList.add('bg-green-600', 'text-white');
                                emailInput.value = '';
                                
                                setTimeout(() => {{
                                    button.innerHTML = originalText;
                                    button.disabled = false;
                                    button.classList.add('bg-[#A3E635]', 'text-black', 'hover:bg-[#86CB15]');
                                    button.classList.remove('bg-green-600', 'text-white');
                                }}, 3000);
                            }} else {{
                                throw new Error('Network response was not ok');
                            }}
                        }} catch (error) {{
                            console.error('Error:', error);
                            button.innerHTML = 'Något gick fel';
                            button.classList.remove('bg-[#A3E635]', 'text-black', 'hover:bg-[#86CB15]');
                            button.classList.add('bg-red-500', 'text-white');
                            
                            setTimeout(() => {{
                                button.innerHTML = originalText;
                                button.disabled = false;
                                button.classList.add('bg-[#A3E635]', 'text-black', 'hover:bg-[#86CB15]');
                                button.classList.remove('bg-red-500', 'text-white');
                            }}, 3000);
                        }}
                    }});
                }}
            }});
    </script>
</body>
</html>"""

with open('/data/workspace/projects/neurovibe/static/arbetsprovning-2026-forsakringskassan.html', 'w', encoding='utf-8') as f:
    f.write(template)

print("HTML saved to static/arbetsprovning-2026-forsakringskassan.html")
