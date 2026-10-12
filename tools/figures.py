"""Draws the Quick Start illustrations as SVG, in the docs site's colors."""
import sys
from pathlib import Path
from xml.sax.saxutils import escape as esc

OUT = Path(sys.argv[1]); OUT.mkdir(parents=True, exist_ok=True)

BG, PANEL, PANEL2, LINE = "#101014", "#18181d", "#202027", "#2c2c35"
TEXT, MUTED, ACCENT = "#e8e8ec", "#9a9aa6", "#26bbff"
PIN, OPTION, START, END, GREEN = "#4da3ff", "#f2c14e", "#4ed38a", "#e2626a", "#4ed38a"
FONT = "Inter, 'Segoe UI', system-ui, sans-serif"

class Svg:
    def __init__(s, w, h):
        s.w, s.h, s.parts = w, h, []
    def add(s, x): s.parts.append(x); return s
    def rect(s, x, y, w, h, fill=PANEL, stroke=LINE, r=8, sw=1, extra=""):
        return s.add(f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="{r}" fill="{fill}" stroke="{stroke}" stroke-width="{sw}" {extra}/>')
    def text(s, x, y, t, size=14, fill=TEXT, weight=400, anchor="start", mono=False):
        fam = "'JetBrains Mono', Consolas, monospace" if mono else FONT
        return s.add(f'<text x="{x}" y="{y}" font-family="{fam}" font-size="{size}" font-weight="{weight}" fill="{fill}" text-anchor="{anchor}">{esc(t)}</text>')
    def line(s, x1, y1, x2, y2, stroke=LINE, sw=1):
        return s.add(f'<line x1="{x1}" y1="{y1}" x2="{x2}" y2="{y2}" stroke="{stroke}" stroke-width="{sw}"/>')
    def wire(s, x1, y1, x2, y2, color="#c9c9d2", sw=2.5):
        dx = max(40, (x2 - x1) * 0.5)
        return s.add(f'<path d="M{x1},{y1} C{x1+dx},{y1} {x2-dx},{y2} {x2},{y2}" fill="none" stroke="{color}" stroke-width="{sw}"/>')
    def badge(s, x, y, n):
        s.add(f'<circle cx="{x}" cy="{y}" r="14" fill="{ACCENT}"/>')
        return s.text(x, y + 5, str(n), 14, "#041018", 800, "middle")
    def arrow(s, x1, y1, x2, y2):
        return s.add(f'<path d="M{x1},{y1} L{x2},{y2}" stroke="{ACCENT}" stroke-width="3" fill="none" marker-end="url(#ah)"/>')
    def highlight(s, x, y, w, h):
        return s.add(f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="7" fill="none" stroke="{ACCENT}" stroke-width="2.5" stroke-dasharray="6 4"/>')
    def window(s, x, y, w, h, title):
        s.rect(x, y, w, h, PANEL, LINE, 10)
        s.add(f'<path d="M{x},{y+10} a10,10 0 0 1 10,-10 h{w-20} a10,10 0 0 1 10,10 v24 h-{w} z" fill="{PANEL2}"/>')
        s.line(x, y + 34, x + w, y + 34)
        return s.text(x + 14, y + 22, title, 13, MUTED, 600)
    def save(s, name):
        head = (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {s.w} {s.h}" width="{s.w}" height="{s.h}">'
                f'<defs><marker id="ah" viewBox="0 0 10 10" refX="8" refY="5" markerWidth="7" markerHeight="7" orient="auto-start-reverse">'
                f'<path d="M0,0 L10,5 L0,10 z" fill="{ACCENT}"/></marker></defs>'
                f'<rect width="{s.w}" height="{s.h}" rx="14" fill="{BG}"/>')
        (OUT / name).write_text(head + "".join(s.parts) + "</svg>", encoding="utf-8")

def node(s, x, y, w, title, body, kind="LINE", color=PIN, chip=None, h=None):
    """A Tag Dialogue graph node like in the editor."""
    h = h or (86 if not chip else 108)
    s.rect(x, y, w, h, "#1d1d24", "#3a3a46", 8)
    s.add(f'<rect x="{x-5}" y="{y+18}" width="6" height="34" rx="3" fill="{color}"/>')       # input bar
    s.add(f'<rect x="{x+w-1}" y="{y+24}" width="6" height="22" rx="3" fill="{color}"/>')     # output bar
    s.add(f'<circle cx="{x+22}" cy="{y+24}" r="11" fill="#2d2d38"/>')
    s.text(x + 40, y + 22, title, 13, TEXT, 700)
    s.text(x + w - 12, y + 20, kind, 9, color, 800, "end")
    s.text(x + 40, y + 42, body, 12, "#c9c9d2")
    if chip:
        s.rect(x + 40, y + 54, len(chip) * 7 + 14, 20, "#2d2d38", "#3a3a46", 10)
        s.text(x + 47, y + 68, chip, 11, MUTED)
    s.text(x + w / 2, y + h - 12, "+  Add option", 11, MUTED, 500, "middle")
    return (x - 2, y + 35), (x + w + 2, y + 35)

def option(s, x, y, w, text):
    s.rect(x, y, w, 52, "#1d1d24", OPTION, 8)
    s.add(f'<rect x="{x-5}" y="{y+10}" width="6" height="32" rx="3" fill="{OPTION}"/>')
    s.add(f'<rect x="{x+w-1}" y="{y+16}" width="6" height="20" rx="3" fill="{OPTION}"/>')
    s.text(x + 14, y + 22, "OPTION", 9, OPTION, 800)
    s.text(x + 14, y + 40, text, 13, TEXT, 600)
    return (x - 2, y + 26), (x + w + 2, y + 26)

def small(s, x, y, label, color):
    s.rect(x, y, 84, 34, "#1d1d24", color, 8)
    s.add(f'<circle cx="{x+16}" cy="{y+17}" r="4" fill="{color}"/>')
    s.text(x + 28, y + 22, label, 13, TEXT, 700)
    return (x - 2, y + 17), (x + 86, y + 17)

# 1 ---------------------------------------------------------------- enable the plugin
s = Svg(900, 330)
s.window(40, 30, 820, 270, "Plugins")
s.rect(60, 80, 300, 34, BG, ACCENT, 6); s.text(76, 102, "Tag Dialogue", 14)
s.rect(60, 135, 780, 140, PANEL2, LINE, 8)
s.add(f'<rect x="80" y="155" width="72" height="72" rx="14" fill="#1c2030"/>')
s.add(f'<rect x="92" y="172" width="48" height="30" rx="8" fill="{PIN}"/><path d="M100,200 l-4,14 l14,-12 z" fill="{PIN}"/>')
s.text(172, 175, "Tag Dialogue", 18, "#fff", 700)
s.text(172, 198, "Dialogue system driven by Gameplay Tags, with a node-graph dialogue editor.", 13, MUTED)
s.text(172, 222, "Version 1.0", 12, MUTED)
s.rect(770, 160, 26, 26, ACCENT, ACCENT, 5); s.add(f'<path d="M776,173 l6,6 l10,-12" stroke="#041018" stroke-width="3" fill="none"/>')
s.text(760, 210, "Enabled", 12, ACCENT, 600, "end")
s.badge(42, 97, 1); s.badge(820, 140, 2)
s.text(450, 316, "Search “Tag Dialogue”, tick Enabled, then restart the editor.", 13, MUTED, 500, "middle")
s.save("qs-1-plugin.svg")

# 2 ---------------------------------------------------------------- welcome popup
s = Svg(900, 300)
s.window(200, 30, 500, 230, "Tag Dialogue")
s.text(224, 92, "Welcome to Tag Dialogue!", 18, "#fff", 700)
s.text(224, 118, "Create ready-made dialogue widgets, or open the demo level.", 13, MUTED)
s.rect(224, 160, 170, 40, ACCENT, ACCENT, 8); s.text(309, 186, "Create Templates", 14, "#041018", 700, "middle")
s.rect(406, 160, 130, 40, PANEL2, "#4a4a55", 8); s.text(471, 186, "Open Demo", 14, TEXT, 600, "middle")
s.rect(548, 160, 128, 40, PANEL2, "#4a4a55", 8); s.text(612, 186, "No thanks", 14, MUTED, 500, "middle")
s.highlight(216, 152, 186, 56); s.badge(216, 150, 1)
s.text(450, 286, "Creates the list, wheel, subtitle and bark widgets and sets them as defaults.", 13, MUTED, 500, "middle")
s.save("qs-2-templates.svg")

# 3 ---------------------------------------------------------------- create the asset
s = Svg(900, 360)
s.window(40, 30, 380, 300, "Content Browser")
for i in range(3):
    s.rect(64 + i * 110, 70, 90, 90, PANEL2, LINE, 8)
s.add(f'<circle cx="250" cy="230" r="5" fill="{ACCENT}"/>'); s.text(262, 234, "right-click", 12, ACCENT, 600)
menu = [("Import to /Game", False), ("Blueprint Class", False), ("Material", False), ("Tag Dialogue", True), ("Widget Blueprint", False)]
s.rect(430, 60, 210, 36 * len(menu) + 16, PANEL2, LINE, 8)
for i, (m, on) in enumerate(menu):
    y = 68 + i * 36
    if on: s.rect(436, y, 198, 32, "rgba(38,187,255,.15)", ACCENT, 6)
    s.text(452, y + 21, m, 13, ACCENT if on else TEXT, 600 if on else 400)
    if on: s.text(622, y + 21, "›", 16, ACCENT, 700, "end")
s.rect(650, 176, 200, 48, PANEL2, LINE, 8)
s.rect(656, 182, 188, 36, "rgba(38,187,255,.15)", ACCENT, 6)
s.add(f'<rect x="668" y="190" width="20" height="20" rx="4" fill="{PIN}"/>')
s.text(698, 205, "Dialogue", 14, "#fff", 700)
s.badge(430, 60, 1); s.badge(650, 176, 2)
s.text(450, 346, "Name it DA_Shopkeeper and double-click it to open the editor.", 13, MUTED, 500, "middle")
s.save("qs-3-create.svg")

# 4 ---------------------------------------------------------------- write the graph
s = Svg(980, 420)
st_in, st_out = small(s, 30, 168, "Start", START)
l_in, l_out = node(s, 170, 150, 230, "Shopkeeper", "Welcome! Need anything?")
o1_in, o1_out = option(s, 470, 80, 200, "Show me your wares.")
o2_in, o2_out = option(s, 470, 160, 200, "Any work for me?")
o3_in, o3_out = option(s, 470, 240, 200, "Goodbye.")
r1_in, r1_out = node(s, 740, 40, 210, "Shopkeeper", "Take a look around.", h=70)
r2_in, r2_out = node(s, 740, 140, 210, "Shopkeeper", "Maybe later, friend.", h=70)
e_in, _ = small(s, 760, 250, "End", END)
s.wire(*st_out, *l_in, GREEN)
for o in (o1_in, o2_in, o3_in): s.wire(*l_out, *o, OPTION)
s.wire(*o1_out, *r1_in); s.wire(*o2_out, *r2_in); s.wire(*o3_out, *e_in)
s.badge(170, 144, 1); s.badge(470, 74, 2); s.badge(740, 34, 3)
s.text(30, 360, "1  Click a line and type its text in Details.", 13, TEXT)
s.text(30, 384, "2  “+ Add option” gives the player choices: options are what the player says.", 13, TEXT)
s.text(30, 408, "3  Wire each option to the NPC's reply. Right-click the graph → Add Line for more.", 13, TEXT)
s.save("qs-4-graph.svg")

# 5 ---------------------------------------------------------------- add the component
s = Svg(900, 340)
s.window(40, 30, 340, 280, "Components")
s.rect(56, 74, 120, 30, ACCENT, ACCENT, 6); s.text(116, 94, "+ Add", 13, "#041018", 700, "middle")
for i, c in enumerate(["BP_Shopkeeper (Self)", "Capsule Component", "Mesh", "TDS Dialogue"]):
    y = 122 + i * 38
    on = c == "TDS Dialogue"
    if on: s.rect(56, y - 4, 308, 32, "rgba(38,187,255,.15)", ACCENT, 6)
    s.text(76 + (0 if i == 0 else 18), y + 17, c, 13, ACCENT if on else TEXT, 700 if on else 400)
s.window(420, 30, 440, 280, "Details")
s.text(440, 74, "TAG DIALOGUE", 11, MUTED, 700)
rows = [("Dialogue", "DA_Shopkeeper"), ("UI Style Override", "None"), ("Barks", "None"), ("Print To Screen", "✓")]
for i, (k, v) in enumerate(rows):
    y = 96 + i * 44
    s.text(440, y + 20, k, 13, TEXT)
    on = k == "Dialogue"
    s.rect(620, y, 220, 30, BG, ACCENT if on else LINE, 6); s.text(632, y + 20, v, 13, "#fff" if on else MUTED, 600 if on else 400)
s.badge(56, 72, 1); s.badge(620, 94, 2)
s.text(450, 330, "Add Component → TDS Dialogue, then pick your dialogue asset.", 13, MUTED, 500, "middle")
s.save("qs-5-component.svg")

# 6 ---------------------------------------------------------------- start dialogue blueprint
s = Svg(900, 330)
def bpnode(x, y, w, h, title, color, pins_in=(), pins_out=()):
    s.rect(x, y, w, h, "#1d1d24", "#3a3a46", 8)
    s.add(f'<path d="M{x},{y+8} a8,8 0 0 1 8,-8 h{w-16} a8,8 0 0 1 8,8 v22 h-{w} z" fill="{color}"/>')
    s.text(x + 12, y + 20, title, 13, "#fff", 700)
    for i, p in enumerate(pins_in):
        s.add(f'<circle cx="{x+14}" cy="{y+50+i*26}" r="5" fill="none" stroke="#c9c9d2" stroke-width="2"/>'); s.text(x + 26, y + 55 + i * 26, p, 12, "#c9c9d2")
    for i, p in enumerate(pins_out):
        s.add(f'<circle cx="{x+w-14}" cy="{y+50+i*26}" r="5" fill="none" stroke="#c9c9d2" stroke-width="2"/>'); s.text(x + w - 26, y + 55 + i * 26, p, 12, "#c9c9d2", 400, "end")
bpnode(40, 60, 200, 80, "Event  Interact (E)", "#8a2b2b", (), ("",))
bpnode(40, 190, 200, 70, "Get Player Pawn", "#2b6b3a", (), ("Return Value",))
bpnode(330, 40, 210, 70, "TDS Dialogue", "#30353f", (), ("",))
bpnode(600, 90, 260, 130, "Start Dialogue", "#1f4f8a", ("", "Target", "Instigator"), ("",))
s.wire(226, 110, 614, 140, "#ffffff", 2.5)
s.wire(526, 90, 614, 166, PIN, 2.5)
s.wire(226, 240, 614, 192, START, 2.5)
s.badge(600, 84, 1); s.badge(40, 184, 2)
s.text(450, 296, "On interact, call Start Dialogue on the TDS Dialogue component.", 13, TEXT, 500, "middle")
s.text(450, 318, "Instigator = the player pawn, so the right player's UI shows it.", 13, MUTED, 400, "middle")
s.save("qs-6-start.svg")

# 7 ---------------------------------------------------------------- in game
s = Svg(900, 380)
s.add(f'<rect x="20" y="20" width="860" height="340" rx="12" fill="url(#sky)"/>')
s.parts.insert(0, '<defs><linearGradient id="sky" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#25324a"/><stop offset="1" stop-color="#151a24"/></linearGradient></defs>')
s.add('<rect x="380" y="120" width="70" height="120" rx="30" fill="#3b4660"/><circle cx="415" cy="100" r="26" fill="#3b4660"/>')
s.rect(140, 240, 620, 100, "rgba(10,10,14,.86)", "#3a3a46", 10)
s.text(164, 268, "Shopkeeper", 15, OPTION, 700)
s.text(164, 294, "Welcome! Need anything?", 15, "#fff")
for i, o in enumerate(["1  Show me your wares.", "2  Any work for me?", "3  Goodbye."]):
    on = i == 0
    s.rect(560, 120 + i * 38, 220, 32, "rgba(38,187,255,.2)" if on else "rgba(10,10,14,.8)", ACCENT if on else "#3a3a46", 6)
    s.text(574, 141 + i * 38, o, 13, "#fff" if on else "#c9c9d2", 600 if on else 400)
s.text(744, 330, "Space ▸", 12, MUTED, 600, "end")
s.badge(560, 114, 1)
s.text(450, 376, "Up/Down or 1–9 pick an option · Space / Enter / click continues", 12, MUTED, 500, "middle")
s.save("qs-7-ingame.svg")
print("ok")
