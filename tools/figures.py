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
    if h >= 80:
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

# ==================================================================== section figures
SEND_C, ADD_C, REM_C, WAIT_C, CLOSE_C = "#3f99ff", "#40d980", "#ff6b6b", "#b373ff", "#4dd9cc"
PICK_C, COND_C = "#c08cff", "#ff9f43"

def pill(s, x, y, verb, detail, color):
    w = 34 + len(verb) * 8 + len(detail) * 7
    s.rect(x, y, w, 28, "#1d1d24", color, 14)
    s.add(f'<rect x="{x+6}" y="{y+5}" width="{len(verb)*8+12}" height="18" rx="9" fill="{color}"/>')
    s.text(x + 12, y + 18, verb, 10, "#0b0b0e", 800)
    s.text(x + len(verb) * 8 + 26, y + 19, detail, 12, TEXT)
    return (x - 1, y + 14), (x + w + 1, y + 14), w

def caption(s, y, t, color=MUTED):
    s.text(s.w / 2, y, t, 13, color, 500, "middle")

def cond_node(s, x, y, w, text):
    s.rect(x, y, w, 84, "#1d1d24", COND_C, 8)
    s.add(f'<rect x="{x-5}" y="{y+16}" width="6" height="30" rx="3" fill="{COND_C}"/>')
    s.text(x + 14, y + 22, "CONDITION", 9, COND_C, 800)
    s.text(x + 14, y + 42, text, 13, TEXT, 600)
    s.add(f'<rect x="{x+w-1}" y="{y+52}" width="6" height="12" rx="3" fill="{GREEN}"/>'); s.text(x + w - 10, y + 62, "True", 11, GREEN, 600, "end")
    s.add(f'<rect x="{x+w-1}" y="{y+68}" width="6" height="12" rx="3" fill="{END}"/>'); s.text(x + w - 10, y + 78, "Else", 11, END, 600, "end")
    return (x - 2, y + 31), (x + w + 2, y + 58), (x + w + 2, y + 74)

def pick_node(s, x, y, w, mode, n):
    h = 52 + n * 22
    s.rect(x, y, w, h, "#1d1d24", PICK_C, 8)
    s.add(f'<rect x="{x-5}" y="{y+14}" width="6" height="30" rx="3" fill="{PICK_C}"/>')
    s.text(x + 14, y + 22, "PICK", 9, PICK_C, 800); s.text(x + 14, y + 42, mode, 13, TEXT, 600)
    outs = []
    for i in range(n):
        yy = y + 54 + i * 22
        s.add(f'<rect x="{x+w-1}" y="{yy-6}" width="6" height="12" rx="3" fill="{PICK_C}"/>'); s.text(x + w - 10, yy + 4, str(i + 1), 11, PICK_C, 700, "end")
        outs.append((x + w + 2, yy))
    s.text(x + 14, y + h - 10, "+  −", 12, MUTED, 600)
    return (x - 2, y + 29), outs

# ---------------------------------------------------------------- tags: send vs add
s = Svg(900, 360)
s.text(225, 40, "Send Tag  =  an event", 16, "#fff", 700, "middle")
s.text(675, 40, "Add Tag  =  memory", 16, "#fff", 700, "middle")
s.line(450, 24, 450, 300)
s.rect(150, 70, 150, 40, "#1d1d24", SEND_C, 20); s.text(225, 95, "Door.Main.Knock", 13, TEXT, 600, "middle")
for i, (lbl, y) in enumerate([("Door BP", 160), ("Quest log", 210), ("Sound", 260)]):
    s.rect(60 + i * 115, y - 10 + (i % 2) * 0, 100, 34, PANEL2, LINE, 8); s.text(110 + i * 115, y + 12, lbl, 12, "#c9c9d2", 500, "middle")
    s.wire(225, 110, 110 + i * 115, y - 10, SEND_C, 2)
s.text(225, 300, "Heard once by every listener. Not remembered.", 12, MUTED, 400, "middle")
s.rect(540, 70, 270, 190, PANEL2, ADD_C, 10)
s.text(556, 94, "TAG STATE (saved)", 11, ADD_C, 800)
for i, t in enumerate(["Quest.FindKey", "Item.Key.Picked", "Reward.Sword"]):
    s.rect(556, 108 + i * 44, 238, 32, "#1d1d24", LINE, 6); s.text(572, 129 + i * 44, t, 13, TEXT, 500, mono=True)
s.text(675, 300, "Stays until removed. Conditions and quests read it.", 12, MUTED, 400, "middle")
caption(s, 344, "Both are Blueprint nodes and action pills: Send Tag / Add Tag / Remove Tag.")
s.save("tags-send-add.svg")

# ---------------------------------------------------------------- the dialogue editor layout
s = Svg(980, 420)
s.rect(20, 20, 940, 380, PANEL, LINE, 12)
s.rect(20, 20, 940, 50, PANEL2, LINE, 12); s.add(f'<rect x="20" y="50" width="940" height="20" fill="{PANEL2}"/>')
s.rect(40, 32, 90, 28, PANEL, "#4a4a55", 6); s.text(85, 51, "Arrange", 12, TEXT, 600, "middle")
s.rect(146, 32, 240, 28, BG, LINE, 6); s.text(160, 51, "Find in dialogue (Ctrl+F)", 12, MUTED)
s.rect(402, 38, 16, 16, ACCENT, ACCENT, 3); s.text(426, 51, "Follow play", 12, TEXT)
s.rect(30, 80, 640, 310, "#141418", LINE, 8)
for gx in range(30, 670, 40): s.line(gx, 80, gx, 390, "#1b1b21")
for gy in range(80, 390, 40): s.line(30, gy, 670, gy, "#1b1b21")
a, b = small(s, 50, 210, "Start", START)
li, lo = node(s, 170, 190, 210, "Shopkeeper", "Welcome! Need anything?", h=74)
oi, oo = option(s, 440, 150, 190, "Show me your wares.")
oi2, oo2 = option(s, 440, 240, 190, "Goodbye.")
s.wire(*b, *li, GREEN); s.wire(*lo, *oi, OPTION); s.wire(*lo, *oi2, OPTION)
s.rect(680, 80, 270, 310, PANEL2, LINE, 8)
s.text(696, 104, "DETAILS", 11, MUTED, 700)
for i, (k, v) in enumerate([("Speaker", "Shopkeeper"), ("Text", "Welcome! Need..."), ("Portrait", "None"), ("Audio", "None"), ("Once Only", "☐")]):
    y = 120 + i * 48
    s.text(696, y + 14, k, 12, "#c9c9d2"); s.rect(790, y, 146, 26, BG, LINE, 5); s.text(800, y + 17, v, 12, MUTED)
s.badge(40, 30, 1); s.badge(146, 30, 2); s.badge(402, 30, 3); s.badge(30, 82, 4); s.badge(680, 82, 5)
s.text(30, 414, "1 Arrange  ·  2 Find  ·  3 Follow play (live debugger)  ·  4 Graph  ·  5 Details of the selected node", 12, MUTED)
s.save("editor-layout.svg")

# ---------------------------------------------------------------- all node types
s = Svg(980, 470)
a, b = small(s, 30, 70, "Start", START)
s.text(30, 128, "Start", 13, "#fff", 700); s.text(30, 146, "where a fresh talk begins", 11, MUTED)
li, lo = node(s, 190, 40, 220, "Shopkeeper", "Welcome to my shop.", chip="Once only", h=96)
s.text(190, 160, "Line", 13, "#fff", 700); s.text(190, 178, "the NPC speaks", 11, MUTED)
oi, oo = option(s, 470, 60, 200, "I need a sword.")
s.rect(470, 118, 150, 20, "#2d2d38", "#3a3a46", 10); s.text(478, 132, "Requires: Item.Gold", 11, MUTED)
s.text(470, 160, "Option", 13, "#fff", 700); s.text(470, 178, "the player speaks", 11, MUTED)
ei, _ = small(s, 740, 76, "End", END)
s.text(740, 128, "End", 13, "#fff", 700); s.text(740, 146, "ends the talk", 11, MUTED)
s.wire(*b, *li, GREEN); s.wire(*lo, *oi, OPTION); s.wire(*oo, *ei)
ci, ct, ce = cond_node(s, 120, 250, 250, "If Quest.FindKey.Done")
s.text(120, 384, "Condition", 13, "#fff", 700); s.text(120, 402, "checks tags, shows nothing", 11, MUTED)
t1, _ = node(s, 440, 220, 180, "Shopkeeper", "Thank you, hero!", h=60)
t2, _ = node(s, 440, 300, 180, "Shopkeeper", "Found my key yet?", h=60)
s.wire(*ct, *t1, GREEN); s.wire(*ce, *t2, END)
pi, outs = pick_node(s, 690, 240, 150, "Random", 3)
s.text(690, 384, "Pick", 13, "#fff", 700); s.text(690, 402, "one output each time", 11, MUTED)
for i, o in enumerate(outs):
    s.add(f'<rect x="{900}" y="{o[1]-12}" width="56" height="24" rx="6" fill="#1d1d24" stroke="#3a3a46"/>'); s.text(928, o[1] + 4, f"Line {i+1}", 11, "#c9c9d2", 500, "middle")
    s.wire(*o, 900, o[1], PICK_C, 2)
caption(s, 452, "Right-click the graph to add any node. Wires flow left to right.")
s.save("nodes-overview.svg")

# ---------------------------------------------------------------- action pills
s = Svg(980, 330)
li, lo = node(s, 30, 40, 200, "Blacksmith", "Here is your sword.", h=70)
x = 290; prev = lo
for verb, det, col in [("ADD", "Reward.Sword", ADD_C), ("SEND", "Npc.Wave", SEND_C), ("CLOSE", "I need a sword", CLOSE_C)]:
    pin, pout, w = pill(s, x, 61, verb, det, col); s.wire(*prev, *pin); prev = pout; x += w + 40
ei, _ = small(s, x, 58, "End", END); s.wire(*prev, *ei)
s.text(30, 160, "Pills run in order when the conversation passes along the wire.", 13, TEXT)
items = [("SEND", "Send Tag", "broadcast an event", SEND_C), ("ADD", "Add Tag", "remember a tag (saved)", ADD_C), ("REMOVE", "Remove Tag", "forget a tag", REM_C),
         ("WAIT", "Wait For Tag", "pause the talk until it happens", WAIT_C), ("CLOSE", "Close Task", "close an option for good", CLOSE_C)]
for i, (v, n, d, c) in enumerate(items):
    cx = 30 + (i % 2) * 470; cy = 186 + (i // 2) * 34
    s.add(f'<rect x="{cx}" y="{cy}" width="{len(v)*8+12}" height="20" rx="10" fill="{c}"/>'); s.text(cx + 6, cy + 14, v, 10, "#0b0b0e", 800)
    s.text(cx + len(v) * 8 + 22, cy + 15, n, 13, "#fff", 700); s.text(cx + len(v) * 8 + 24 + len(n) * 7.6, cy + 15, "· " + d, 12, MUTED)
s.badge(290, 52, 1)
caption(s, 316, "Add one: double-click any wire, or right-click it → Insert on this wire.")
s.save("actions-pills.svg")

# ---------------------------------------------------------------- tasks flow
s = Svg(980, 440)
oi, oo = option(s, 30, 70, 210, "Can I help?")
s.rect(30, 128, 210, 46, "#2d2d38", "#3a3a46", 8); s.text(42, 146, "Task: Quest.FindKey", 11, TEXT, 600); s.text(42, 164, "Done when: Item.Key.Picked", 11, MUTED)
for i, (pin, col) in enumerate([("Ask  (still working)", PIN), ("Reward  (once)", ADD_C), ("Done  (after reward)", CLOSE_C)]):
    y = 196 + i * 30
    s.add(f'<rect x="{236}" y="{y-6}" width="6" height="12" rx="3" fill="{col}"/>'); s.text(228, y + 4, pin, 11, col, 600, "end")
ti, _ = node(s, 320, 40, 240, "Blacksmith", "Find my key in the barn.", h=62)
a1, _ = node(s, 320, 140, 240, "Blacksmith", "Found my key yet?", h=62)
r1, r1o = node(s, 320, 230, 240, "Blacksmith", "My key! Take this sword.", h=62)
d1, _ = node(s, 320, 320, 240, "Blacksmith", "I already paid you.", h=62)
s.wire(*oo, *ti, OPTION); s.wire(242, 196, *a1, PIN); s.wire(242, 226, *r1, ADD_C); s.wire(242, 256, *d1, CLOSE_C)
pin_, pout, w = pill(s, 600, 247, "ADD", "Reward.Sword", ADD_C); s.wire(*r1o, *pin_)
steps = [("1", "Player picks the option", "first reply; Quest.FindKey added"), ("2", "Talks again, key not found", "plays Ask"),
         ("3", "Game sends Item.Key.Picked", "Quest.FindKey.Done added for you"), ("4", "Talks again", "plays Reward, once"), ("5", "Picks the option later", "plays Done")]
for i, (n, a_, b_) in enumerate(steps):
    y = 70 + i * 60
    s.add(f'<circle cx="{760}" cy="{y}" r="12" fill="{ACCENT}"/>'); s.text(760, y + 5, n, 12, "#041018", 800, "middle")
    s.text(782, y - 2, a_, 12, "#fff", 700); s.text(782, y + 15, b_, 11, MUTED)
s.save("tasks-flow.svg")

# ---------------------------------------------------------------- text variables
s = Svg(900, 230)
s.rect(40, 50, 360, 70, "#1d1d24", "#3a3a46", 8); s.text(56, 76, "LINE TEXT", 10, PIN, 800)
s.text(56, 102, "You have ", 15, TEXT); s.text(124, 102, "{Gold}", 15, ACCENT, 700, mono=True); s.text(186, 102, " gold, ", 15, TEXT); s.text(232, 102, "{PlayerName}", 15, ACCENT, 700, mono=True)
s.arrow(410, 85, 490, 85)
s.rect(500, 50, 360, 70, "rgba(10,10,14,.86)", "#3a3a46", 10); s.text(516, 76, "IN GAME", 10, MUTED, 800); s.text(516, 102, "You have 1,250 gold, Yahya.", 15, "#fff", 600)
s.rect(40, 150, 360, 40, PANEL2, LINE, 8); s.text(56, 175, "Set Number Variable  Gold = 1250", 13, TEXT, 500, mono=True)
s.badge(40, 150, 1)
caption(s, 214, "Set variables from Blueprint; {PlayerName} is built in.")
s.save("text-variables.svg")

# ---------------------------------------------------------------- barks
s = Svg(900, 360)
s.add(f'<rect x="20" y="20" width="860" height="300" rx="12" fill="url(#sky2)"/>')
s.parts.insert(0, '<defs><linearGradient id="sky2" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#25324a"/><stop offset="1" stop-color="#151a24"/></linearGradient></defs>')
for x0 in (200, 600):
    s.add(f'<rect x="{x0}" y="150" width="60" height="110" rx="26" fill="#3b4660"/><circle cx="{x0+30}" cy="132" r="22" fill="#3b4660"/>')
s.rect(130, 64, 200, 44, "rgba(10,10,14,.9)", "#3a3a46", 10); s.add('<path d="M222,108 l8,12 l8,-12 z" fill="rgba(10,10,14,.9)"/>')
s.text(230, 92, "Lovely day for a walk.", 13, "#fff", 500, "middle")
s.rect(220, 272, 460, 36, "rgba(10,10,14,.75)", "#3a3a46", 8); s.text(450, 295, "Guard: Halt! Who goes there?", 14, "#fff", 500, "middle")
s.add(f'<text x="276" y="295" font-family="{FONT}" font-size="14" font-weight="700" fill="{OPTION}" text-anchor="middle"></text>')
s.badge(130, 60, 1); s.badge(220, 268, 2)
s.text(40, 344, "1  TDS Bark Widget: a bubble above the head", 12, TEXT); s.text(470, 344, "2  Bark subtitles (on by default)", 12, TEXT)
s.save("barks.svg")

# ---------------------------------------------------------------- UI styles
s = Svg(980, 330)
def frame(x, title, tag):
    s.rect(x, 40, 290, 200, "#151a24", LINE, 10)
    s.text(x + 145, 270, title, 14, "#fff", 700, "middle"); s.text(x + 145, 292, tag, 12, ACCENT, 500, "middle", mono=True)
frame(20, "List", "UI.Dialogue.List")
s.rect(36, 170, 258, 56, "rgba(10,10,14,.86)", "#3a3a46", 8); s.text(48, 190, "Khalid", 12, OPTION, 700); s.text(48, 210, "What can I do for you?", 12, "#fff")
for i, t in enumerate(["I need a sword.", "Goodbye."]):
    s.rect(160, 92 + i * 34, 130, 28, "rgba(38,187,255,.2)" if i == 0 else "rgba(10,10,14,.8)", ACCENT if i == 0 else "#3a3a46", 5); s.text(170, 111 + i * 34, t, 11, "#fff")
frame(345, "Wheel", "UI.Dialogue.Wheel")
cx, cy = 490, 135
for i in range(4):
    import math
    a0 = math.radians(i * 90 - 45 + 4); a1 = math.radians(i * 90 + 45 - 4); r1, r2 = 38, 80
    p = f"M{cx+r1*math.cos(a0)},{cy+r1*math.sin(a0)} L{cx+r2*math.cos(a0)},{cy+r2*math.sin(a0)} A{r2},{r2} 0 0 1 {cx+r2*math.cos(a1)},{cy+r2*math.sin(a1)} L{cx+r1*math.cos(a1)},{cy+r1*math.sin(a1)} A{r1},{r1} 0 0 0 {cx+r1*math.cos(a0)},{cy+r1*math.sin(a0)} z"
    s.add(f'<path d="{p}" fill="{"rgba(38,187,255,.35)" if i == 3 else "rgba(10,10,14,.85)"}" stroke="{ACCENT if i == 3 else "#3a3a46"}"/>')
s.text(cx, cy + 4, "Give", 11, "#fff", 600, "middle")
frame(670, "Subtitle", "UI.Dialogue.Subtitle")
s.text(815, 200, "Radio: ...the only station in town.", 12, "#fff", 500, "middle")
caption(s, 320, "Project Settings → Tag Dialogue UI maps each style tag to a widget.")
s.save("ui-styles.svg")

# ---------------------------------------------------------------- tag state component
s = Svg(900, 300)
s.window(40, 30, 380, 220, "Details: TDS Tag State")
s.text(60, 92, "When", 13, TEXT); s.rect(160, 74, 240, 30, BG, ACCENT, 6); s.text(172, 94, "Any: Item.Key.Picked", 12, "#fff", 600)
s.text(60, 142, "Action", 13, TEXT); s.rect(160, 124, 240, 30, BG, LINE, 6); s.text(172, 144, "Hide", 12, "#fff", 600)
s.text(60, 192, "On State Changed", 13, TEXT); s.rect(250, 176, 60, 26, ACCENT, ACCENT, 6); s.text(280, 194, "+", 14, "#041018", 800, "middle")
for i, (lbl, hidden) in enumerate([("before pickup", False), ("after pickup", True)]):
    x0 = 500 + i * 200
    s.rect(x0, 60, 170, 150, "#151a24", LINE, 10)
    if not hidden:
        s.add(f'<g transform="translate({x0+60},110)"><circle cx="0" cy="0" r="16" fill="none" stroke="{OPTION}" stroke-width="6"/><rect x="14" y="-4" width="40" height="8" fill="{OPTION}"/><rect x="40" y="4" width="6" height="10" fill="{OPTION}"/></g>')
    else:
        s.text(x0 + 85, 140, "hidden", 13, MUTED, 600, "middle")
    s.text(x0 + 85, 236, lbl, 12, MUTED, 500, "middle")
s.arrow(675, 135, 695, 135)
caption(s, 284, "The world follows the tag state: checked on Begin Play, on every change, and after loading.")
s.save("tag-state.svg")

# ---------------------------------------------------------------- save and load
s = Svg(900, 300)
s.rect(40, 60, 260, 170, PANEL2, ADD_C, 10); s.text(56, 86, "TAG DIALOGUE REMEMBERS", 10, ADD_C, 800)
for i, t in enumerate(["Tag state", "Running tasks", "Every NPC's memory", "Global text variables"]):
    s.text(60, 116 + i * 28, "• " + t, 13, TEXT)
s.rect(380, 60, 220, 60, "#1d1d24", ACCENT, 10); s.text(490, 86, "Save To Slot", 14, "#fff", 700, "middle"); s.text(490, 106, "one node, built in", 11, MUTED, 400, "middle")
s.rect(380, 170, 220, 60, "#1d1d24", "#4a4a55", 10); s.text(490, 196, "Capture Save Data", 14, "#fff", 700, "middle"); s.text(490, 216, "for your own save system", 11, MUTED, 400, "middle")
s.wire(300, 120, 380, 90, ACCENT); s.wire(300, 170, 380, 200, "#9a9aa6")
s.rect(680, 60, 180, 60, PANEL2, LINE, 10); s.text(770, 95, "TagDialogue.sav", 13, TEXT, 500, "middle", mono=True)
s.rect(680, 170, 180, 60, PANEL2, LINE, 10); s.text(770, 205, "Your SaveGame", 13, TEXT, 500, "middle")
s.arrow(604, 90, 674, 90); s.arrow(604, 200, 674, 200)
caption(s, 280, "Load From Slot / Restore Save Data put it back. NPCs update right away.")
s.save("save-load.svg")

# ---------------------------------------------------------------- import json
s = Svg(980, 280)
s.rect(40, 60, 170, 140, PANEL2, LINE, 10); s.text(125, 96, "{ }", 32, ACCENT, 700, "middle", mono=True)
s.text(125, 140, "DA_Blacksmith.json", 12, TEXT, 600, "middle"); s.text(125, 160, "hand-written or AI", 11, MUTED, 400, "middle")
s.arrow(220, 130, 300, 130); s.text(260, 120, "drag", 11, ACCENT, 600, "middle")
s.window(310, 50, 200, 160, "Content Browser")
s.rect(330, 100, 70, 70, "#1c2030", PIN, 8); s.text(365, 190, "DA_Blacksmith", 10, TEXT, 500, "middle")
s.arrow(520, 130, 590, 130)
s.rect(600, 50, 365, 160, "#141418", LINE, 10)
a, b = small(s, 612, 112, "Start", START)
li, lo = node(s, 718, 94, 120, "Khalid", "Welcome!", h=56)
o1, _ = option(s, 866, 103, 90, "Bye.")
s.wire(*b, *li, GREEN); s.wire(*lo, *o1, OPTION)
caption(s, 240, "Each file becomes a Dialogue asset, arranged automatically. Missing tags are added.")
caption(s, 262, "Right-click the asset → Reimport after editing the file.")
s.save("import-json.svg")

# ---------------------------------------------------------------- live debugger
s = Svg(900, 270)
s.rect(20, 20, 860, 230, "#141418", LINE, 12)
a, b = small(s, 50, 106, "Start", START)
n1i, n1o = node(s, 180, 80, 200, "Guard", "Halt. New faces...", h=70)
n2i, n2o = node(s, 450, 80, 200, "Guard", "What do you want?", h=70)
s.wire(*b, *n1i, GREEN); s.wire(*n1o, *n2i)
s.add(f'<rect x="176" y="76" width="208" height="78" rx="10" fill="none" stroke="#7fd6a2" stroke-width="2" opacity=".6"/>')
s.add(f'<rect x="444" y="74" width="212" height="82" rx="11" fill="none" stroke="{GREEN}" stroke-width="3"/>')
s.add(f'<rect x="440" y="70" width="220" height="90" rx="13" fill="none" stroke="{GREEN}" stroke-width="6" opacity=".25"/>')
s.text(550, 186, "playing now", 12, GREEN, 700, "middle"); s.text(280, 186, "already passed", 12, "#7fd6a2", 500, "middle")
caption(s, 228, "Play in the editor with the dialogue open. “Follow play” keeps the node in view.")
s.save("live-debugger.svg")

# ---------------------------------------------------------------- AI workflow
s = Svg(980, 220)
steps = [("AI guide", ".md file"), ("Any AI chat", "asks about your story"), ("Story map", "you approve it"), ("JSON", "ready to import"), ("Unreal", "drag in, done")]
for i, (t, d) in enumerate(steps):
    x0 = 20 + i * 192
    s.rect(x0, 60, 170, 90, "#1d1d24", ACCENT if i in (0, 4) else "#3a3a46", 10)
    s.add(f'<circle cx="{x0+20}" cy="80" r="11" fill="{ACCENT}"/>'); s.text(x0 + 20, 84, str(i + 1), 11, "#041018", 800, "middle")
    s.text(x0 + 85, 110, t, 15, "#fff", 700, "middle"); s.text(x0 + 85, 132, d, 11, MUTED, 400, "middle")
    if i < 4: s.arrow(x0 + 172, 105, x0 + 190, 105)
caption(s, 190, "You decide the story; the AI handles the structure and the JSON.")
s.save("ai-workflow.svg")
print("sections ok")
