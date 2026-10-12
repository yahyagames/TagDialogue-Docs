"""Builds the Tag Dialogue docs site (static HTML) from the plugin's Markdown docs."""
import html, json, re, shutil, sys
from pathlib import Path
import markdown

SRC = Path(sys.argv[1])          # folder with TagDialogue_Manual.md, TagDialogue_AI_Writing_Guide.md, Icon128.png
OUT = Path(sys.argv[2])
FAB_URL = "#"                    # replace with the Fab listing link once it exists
SUPPORT = "mailto:yahya@harcs.studio"
VERSION = "1.0 · Unreal Engine 5.6"

MD_EXT = ["tables", "fenced_code", "attr_list", "sane_lists", "toc"]

def slugify(title):
    title = re.sub(r"^\d+\.\s*", "", title)
    return re.sub(r"[^a-z0-9]+", "-", title.lower()).strip("-")

# ---------------------------------------------------------------- split the manual into pages
manual = (SRC / "TagDialogue_Manual.md").read_text(encoding="utf-8")
parts = re.split(r"^## ", manual, flags=re.M)
intro = parts[0]
pages = []  # (slug, title, number, markdown)
anchor_to_slug = {}
for part in parts[1:]:
    title, _, body = part.partition("\n")
    title = title.strip()
    if title.lower() == "contents":
        continue
    m = re.match(r"(\d+)\.\s*(.*)", title)
    number, clean = (m.group(1), m.group(2)) if m else ("", title)
    slug = slugify(title)
    # the manual's own anchors look like #16-live-debugger-and-search
    anchor = re.sub(r"[^a-z0-9 -]", "", title.lower()).replace(" ", "-")
    anchor_to_slug[anchor] = slug
    pages.append((slug, clean, number, body.strip().rstrip("-").strip()))

def fix_links(md_text):
    def repl(m):
        target = m.group(2)
        if target.startswith("#") and target[1:] in anchor_to_slug:
            return f"[{m.group(1)}]({anchor_to_slug[target[1:]]}.html)"
        return m.group(0)
    md_text = re.sub(r"\[([^\]]+)\]\((#[^)]+)\)", repl, md_text)
    md_text = md_text.replace("`Docs/TagDialogue_AI_Writing_Guide.md`", "the [AI Writing Guide](ai-writing.html)")
    return md_text

def render(md_text):
    return markdown.markdown(fix_links(md_text), extensions=MD_EXT, output_format="html5")

# ---------------------------------------------------------------- layout
NAV_GROUPS = [
    ("Getting started", ["quick-start", "how-it-works-tags", "demo-level"]),
    ("Writing dialogue", ["the-dialogue-editor", "nodes", "actions-pills-on-wires", "tasks-quests", "text-variables"]),
    ("In your game", ["the-tds-dialogue-component", "barks", "tds-tag-state-component", "blueprint-nodes-for-tags", "save-and-load"]),
    ("UI and input", ["ui", "input-and-controls"]),
    ("Tools", ["import-and-export-json-csv", "live-debugger-and-search", "ai-writing"]),
    ("Help", ["troubleshooting"]),
]
titles = {slug: title for slug, title, _, _ in pages}
titles["ai-writing"] = "Writing with AI (JSON)"
order = [s for _, group in NAV_GROUPS for s in group]
missing = [s for s, *_ in pages if s not in order]
assert not missing, f"pages not in nav: {missing}"

def sidebar(active):
    out = ['<nav class="sidebar" id="sidebar"><a class="brand" href="index.html"><img src="assets/icon.png" alt=""><span>Tag Dialogue</span></a>',
           '<div class="search"><input id="search" type="search" placeholder="Search docs..." autocomplete="off"><div id="results"></div></div>']
    for group, slugs in NAV_GROUPS:
        out.append(f'<div class="group">{html.escape(group)}</div>')
        for s in slugs:
            cls = ' class="active"' if s == active else ""
            out.append(f'<a{cls} href="{s}.html">{html.escape(titles[s])}</a>')
    out.append(f'<div class="group">Links</div><a href="{FAB_URL}">Get it on Fab</a><a href="{SUPPORT}">Support</a></nav>')
    return "\n".join(out)

def page_html(title, body, active=None, wide=False, extra_head=""):
    nav = sidebar(active)
    prevnext = ""
    if active in order:
        i = order.index(active)
        prev_link = f'<a class="prev" href="{order[i-1]}.html"><small>Previous</small>{html.escape(titles[order[i-1]])}</a>' if i > 0 else "<span></span>"
        next_link = f'<a class="next" href="{order[i+1]}.html"><small>Next</small>{html.escape(titles[order[i+1]])}</a>' if i + 1 < len(order) else "<span></span>"
        prevnext = f'<div class="prevnext">{prev_link}{next_link}</div>'
    return f"""<!doctype html>
<html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1">
<title>{html.escape(title)} · Tag Dialogue</title>
<link rel="icon" href="assets/icon.png">
<link rel="preconnect" href="https://fonts.googleapis.com"><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&family=JetBrains+Mono:wght@400;500&display=swap" rel="stylesheet">
<link rel="stylesheet" href="assets/style.css">{extra_head}
</head><body>
<header class="topbar"><button class="menu" onclick="document.body.classList.toggle('nav-open')" aria-label="Menu">☰</button>
<a class="brand" href="index.html"><img src="assets/icon.png" alt=""><span>Tag Dialogue</span></a>
<span class="spacer"></span><a class="btn small" href="{FAB_URL}">Get it on Fab</a></header>
<div class="layout">{nav}
<main class="content{' wide' if wide else ''}"><article>{body}</article>{prevnext}
<footer>Tag Dialogue {VERSION} · © Yahya · Unreal Engine is a trademark of Epic Games, Inc. This site is not affiliated with Epic Games.</footer></main></div>
<script src="assets/search.js"></script></body></html>"""

OUT.mkdir(parents=True, exist_ok=True)
(OUT / "assets").mkdir(exist_ok=True)
shutil.copy(SRC / "Icon128.png", OUT / "assets" / "icon.png")
search_index = []

def text_of(h):
    return re.sub(r"\s+", " ", html.unescape(re.sub(r"<[^>]+>", " ", h))).strip()

for slug, title, number, body in pages:
    h = render(body)
    (OUT / f"{slug}.html").write_text(page_html(title, f"<h1>{html.escape(title)}</h1>\n{h}", slug), encoding="utf-8")
    search_index.append({"url": f"{slug}.html", "title": title, "text": text_of(h)[:6000]})

# AI guide page (+ the raw file to download and give to an AI)
ai = (SRC / "TagDialogue_AI_Writing_Guide.md").read_text(encoding="utf-8")
ai_body = re.sub(r"^# .*\n", "", ai, count=1)
shutil.copy(SRC / "TagDialogue_AI_Writing_Guide.md", OUT / "TagDialogue_AI_Writing_Guide.md")
ai_intro = """<h1>Writing with AI (JSON)</h1>
<div class="callout"><strong>How to use it:</strong> download the file below, upload it (or paste it) into ChatGPT, Claude, Gemini or any AI chat, and say <em>"Let's start"</em>.
The AI asks about your story, shows you a readable story map, then writes JSON you drag straight into Unreal.<br><br>
<a class="btn" href="TagDialogue_AI_Writing_Guide.md" download>Download the AI guide (.md)</a></div>
<p class="muted">The full file is shown below. It is also the complete reference for the JSON format.</p>"""
ai_h = render(ai_body)
(OUT / "ai-writing.html").write_text(page_html("Writing with AI (JSON)", ai_intro + ai_h, "ai-writing"), encoding="utf-8")
search_index.append({"url": "ai-writing.html", "title": "Writing with AI (JSON)", "text": text_of(ai_h)[:8000]})

# ---------------------------------------------------------------- landing page
features = [
    ("Node graph editor", "Lines, options, conditions, random and in-order picks, and action pills right on the wires."),
    ("Driven by Gameplay Tags", "Dialogue talks to your game through tags: quests, doors and pickups react without hard references."),
    ("Quests built in", "Ask, Reward (once) and Done lines. Tasks complete themselves when the right tags happen."),
    ("Barks", "Ambient lines with no UI takeover: subtitles, speech bubbles above heads, or your own UI."),
    ("Ready-made UI", "One click creates list, wheel and subtitle widgets. Or build your own from drop-in blocks."),
    ("Save anywhere", "One-node save to slot, or capture the data into your own save system."),
    ("Live debugger", "Watch the playing node glow in the graph while you play in the editor."),
    ("Write with AI", "Import dialogues as JSON. A ready guide turns any AI chat into a dialogue writer."),
]
cards = "\n".join(f'<div class="card"><h3>{html.escape(t)}</h3><p>{html.escape(d)}</p></div>' for t, d in features)
lead = re.sub(r"^#.*\n|^Version.*\n|^---\s*$", "", intro, flags=re.M).strip()
lead_html = markdown.markdown(lead)
landing = f"""<section class="hero">
<img src="assets/icon.png" alt="" class="hero-icon">
<h1>Tag Dialogue</h1>
<p class="tagline">A dialogue system for Unreal Engine 5, driven by Gameplay Tags. Built for Blueprint.</p>
<div class="hero-buttons"><a class="btn" href="quick-start.html">Quick start</a><a class="btn ghost" href="{FAB_URL}">Get it on Fab</a></div>
<p class="muted small">{VERSION}</p>
</section>
<section class="lead">{lead_html}</section>
<section class="cards">{cards}</section>
<section class="start"><h2>Start here</h2>
<div class="links"><a href="quick-start.html">Quick start →</a><a href="nodes.html">Nodes →</a><a href="tasks-quests.html">Quests →</a><a href="ui.html">UI →</a><a href="ai-writing.html">Writing with AI →</a><a href="troubleshooting.html">Troubleshooting →</a></div></section>"""
(OUT / "index.html").write_text(page_html("Documentation", landing, None, wide=True), encoding="utf-8")

(OUT / "assets" / "search-index.json").write_text(json.dumps(search_index), encoding="utf-8")
(OUT / ".nojekyll").write_text("")
print("pages:", len(pages) + 2)
