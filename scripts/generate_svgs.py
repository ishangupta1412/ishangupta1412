"""
Generate two premium SVGs for Ishan Gupta's GitHub profile:
1. chat_animation.svg  — animated typing chat simulation (jasonlong-style)
2. activity_map.svg    — contribution grid + quadrant crosshair chart
"""
import random, os, math

random.seed(42)
OUT = os.path.join(os.path.dirname(__file__), '..', 'assets')

# ─────────────────────────────────────────────
#  SHARED TOKENS
# ─────────────────────────────────────────────
BG         = '#0d1117'
HEADER_BG  = '#161b22'
USER_BG    = '#21262d'
USER_FG    = '#c9d1d9'
AGENT_BG   = '#1f6feb'
AGENT_FG   = '#ffffff'
BORDER     = '#30363d'
MUTED      = '#8b949e'
GREEN      = '#3fb950'
MONO       = "SFMono-Regular,Consolas,Liberation Mono,monospace"
UI         = "-apple-system,BlinkMacSystemFont,'Segoe UI',system-ui,sans-serif"

# ════════════════════════════════════════════
#  1. CHAT ANIMATION SVG
# ════════════════════════════════════════════

W, H      = 800, 240
HEADER_H  = 44
LOOP      = 20       # total animation loop in seconds
ROW_H     = 32
ROW_Y0    = 56       # y of first bubble
ROW_GAP   = 10

MESSAGES = [
    ('user',  'ALERT: distributed password spray detected'),
    ('agent', 'correlating 847 auth events \u00b7 NOBELIUM signature confirmed'),
    ('user',  'response time?'),
    ('agent', 'patched. STIX 2.1 report generated \u2713'),
]

# Timing table  (typing_start, typing_end, msg_show, msg_hold_until, fade_until)
TIMING = [
    (0.0,  1.4,  1.6),
    (3.0,  4.4,  4.6),
    (6.0,  7.4,  7.6),
    (9.0, 10.4, 10.6),
]
MSGS_HOLD  = 17.0
MSGS_FADE  = 19.0

def p(t): return f"{t/LOOP*100:.2f}%"

def char_w(text):
    # conservative monospace width estimate at 12px
    return int(len(text) * 7.6) + 32

def ry(i): return ROW_Y0 + i * (ROW_H + ROW_GAP)

# ── CSS ──────────────────────────────────────
css_lines = ["""    <style>
      @keyframes db { 0%,100%{transform:translateY(0)} 50%{transform:translateY(-3px)} }
      .d1{animation:db .85s .00s infinite ease-in-out}
      .d2{animation:db .85s .18s infinite ease-in-out}
      .d3{animation:db .85s .36s infinite ease-in-out}"""]

for i, (ts, te, ms) in enumerate(TIMING):
    n = i + 1
    css_lines.append(f"""
      /* bubble {n} */
      .ty{n}{{opacity:0;animation:ty{n}_ {LOOP}s infinite}}
      @keyframes ty{n}_{{
        0%,{p(max(0,ts-.05))}{{opacity:0}}
        {p(ts+.15)}{{opacity:1}}
        {p(te)}{{opacity:1}}
        {p(te+.4)}{{opacity:0}}
        100%{{opacity:0}}
      }}
      .m{n}{{opacity:0;animation:m{n}_ {LOOP}s infinite}}
      @keyframes m{n}_{{
        0%,{p(ms)}{{opacity:0}}
        {p(ms+.5)}{{opacity:1}}
        {p(MSGS_HOLD)}{{opacity:1}}
        {p(MSGS_FADE)}{{opacity:0}}
        100%{{opacity:0}}
      }}""")

css_lines.append("    </style>")
CSS = "\n".join(css_lines)

# ── Typing dots ───────────────────────────────
def typing_dots(i, side):
    y  = ry(i)
    cy = y + ROW_H // 2
    n  = i + 1
    if side == 'user':
        x, bg, dc = 16, USER_BG, MUTED
    else:
        x, bg, dc = W - 68, AGENT_BG, 'rgba(255,255,255,.75)'
    return f"""    <g class="ty{n}">
      <rect x="{x}" y="{y}" width="52" height="{ROW_H}" rx="14" fill="{bg}"/>
      <circle cx="{x+13}" cy="{cy}" r="3" fill="{dc}" class="d1"/>
      <circle cx="{x+26}" cy="{cy}" r="3" fill="{dc}" class="d2"/>
      <circle cx="{x+39}" cy="{cy}" r="3" fill="{dc}" class="d3"/>
    </g>"""

# ── Message bubble ────────────────────────────
def bubble(i, side, text):
    y  = ry(i)
    n  = i + 1
    bw = char_w(text)
    if side == 'user':
        x, bc, tc = 16, USER_BG, USER_FG
    else:
        x = W - 16 - bw
        bc, tc = AGENT_BG, AGENT_FG
    tx = x + 14
    ty = y + 20
    return f"""    <g class="m{n}">
      <rect x="{x}" y="{y}" width="{bw}" height="{ROW_H}" rx="14" fill="{bc}"/>
      <text x="{tx}" y="{ty}" fill="{tc}" font-family={MONO} font-size="12">{text}</text>
    </g>"""

# ── Assemble chat SVG ─────────────────────────
msgs_svg = "\n".join(
    typing_dots(i, side) + "\n" + bubble(i, side, text)
    for i, (side, text) in enumerate(MESSAGES)
)

CHAT_SVG = f"""<svg width="{W}" height="{H}" viewBox="0 0 {W} {H}" fill="none" xmlns="http://www.w3.org/2000/svg" role="img" aria-label="Chat simulation — ishangupta1412">
  <defs>
{CSS}
    <clipPath id="cc"><rect width="{W}" height="{H}" rx="8"/></clipPath>
  </defs>
  <g clip-path="url(#cc)">
    <!-- Background -->
    <rect width="{W}" height="{H}" fill="{BG}"/>

    <!-- Header -->
    <rect width="{W}" height="{HEADER_H}" fill="{HEADER_BG}"/>
    <line x1="0" y1="{HEADER_H}" x2="{W}" y2="{HEADER_H}" stroke="{BORDER}" stroke-width="1"/>

    <!-- Online indicator with pulse -->
    <circle cx="20" cy="22" r="5" fill="{GREEN}"/>
    <circle cx="20" cy="22" r="5" fill="none" stroke="{GREEN}" stroke-width="2">
      <animate attributeName="r" values="5;13;5" dur="2.5s" repeatCount="indefinite"/>
      <animate attributeName="stroke-opacity" values=".6;0;.6" dur="2.5s" repeatCount="indefinite"/>
    </circle>

    <!-- Header title -->
    <text x="34" y="27" fill="#e6edf3" font-family="{UI}" font-size="13" font-weight="600">ishangupta1412</text>
    <text x="154" y="27" fill="{MUTED}" font-family="{UI}" font-size="11">· Active · Systems Engineer</text>

    <!-- Window chrome dots -->
    <circle cx="{W-24}" cy="22" r="5" fill="{BORDER}"/>
    <circle cx="{W-42}" cy="22" r="5" fill="{BORDER}"/>
    <circle cx="{W-60}" cy="22" r="5" fill="{BORDER}"/>

    <!-- Messages -->
{msgs_svg}

    <!-- Footer timestamp -->
    <text x="{W//2}" y="{H-8}" text-anchor="middle" fill="{BORDER}" font-family="{UI}" font-size="10">Today</text>
  </g>
  <rect width="{W}" height="{H}" rx="8" fill="none" stroke="{BORDER}" stroke-width="1"/>
</svg>"""

# ════════════════════════════════════════════
#  2. ACTIVITY MAP SVG  (grid + quadrant)
# ════════════════════════════════════════════

AW, AH = 800, 230

# Grid geometry
CELL  = 9
GAP   = 2
STEP  = CELL + GAP   # 11px
WEEKS = 52
DAYS  = 7
GX    = 36            # x offset (day labels)
GY    = 32            # y offset (month labels)

# Realistic contribution distribution
def gen_level(week):
    """Higher activity in recent and mid-year weeks."""
    r = random.random()
    # Base distribution
    thresholds = [.30, .52, .72, .88]
    # Recent months boost
    if week >= 36:
        thresholds = [.12, .35, .58, .80]
    # Quiet period (Jan–Feb simulation)
    if 10 <= week <= 16:
        thresholds = [.55, .72, .84, .94]
    for lvl, t in enumerate(thresholds):
        if r < t:
            return lvl
    return 4

LEVEL_COLORS = {0:'#161b22', 1:'#0e4429', 2:'#006d32', 3:'#26a641', 4:'#39d353'}

grid_els = []
total_contribs = 0
for w in range(WEEKS):
    for d in range(DAYS):
        lvl = gen_level(w)
        if lvl > 0:
            total_contribs += lvl * 2
        cx = GX + w * STEP
        cy = GY + d * STEP
        grid_els.append(
            f'<rect x="{cx}" y="{cy}" width="{CELL}" height="{CELL}" rx="2" fill="{LEVEL_COLORS[lvl]}"/>'
        )
GRID = "\n    ".join(grid_els)

# Month labels
MONTHS = ['Nov','Dec','Jan','Feb','Mar','Apr','May','Jun','Jul','Aug','Sep','Oct','Nov']
MX_STEP = WEEKS / (len(MONTHS) - 1)
MONTH_LABELS = "\n    ".join(
    f'<text x="{GX + int(i*MX_STEP*STEP)}" y="{GY-6}" fill="{MUTED}" font-family="{UI}" font-size="10">{m}</text>'
    for i, m in enumerate(MONTHS)
)

# Day labels
DAY_LABELS = "\n    ".join(
    f'<text x="{GX-6}" y="{GY + d*STEP + CELL}" fill="{MUTED}" font-family="{UI}" font-size="10" text-anchor="end">{name}</text>'
    for d, name in [(1,'Mon'),(3,'Wed'),(5,'Fri')]
)

# Legend
LEG_Y = GY + DAYS * STEP + 14
LEGEND_ELS = "\n    ".join([
    f'<text x="{GX}" y="{LEG_Y+9}" fill="{MUTED}" font-family="{UI}" font-size="10">Less</text>',
    *[f'<rect x="{GX+30+i*13}" y="{LEG_Y}" width="10" height="10" rx="2" fill="{LEVEL_COLORS[i]}"/>' for i in range(5)],
    f'<text x="{GX+30+5*13+4}" y="{LEG_Y+9}" fill="{MUTED}" font-family="{UI}" font-size="10">More</text>',
])

# ── Quadrant crosshair chart ──────────────────
GRID_RIGHT = GX + WEEKS * STEP  # 622px
QX0  = GRID_RIGHT + 24          # start of quadrant panel
QW   = AW - QX0 - 10            # panel width
QCX  = QX0 + QW // 2            # center x
QCY  = AH // 2 + 10             # center y
ARM  = min(QW // 2 - 20, 72)    # arm length

# Activity breakdown (Ishan's realistic split)
ACT  = {'commits': 0.87, 'review': 0.04, 'prs': 0.09, 'issues': 0.00}

# Polygon vertices on crosshair axes
PVERTS = [
    (QCX - ARM * ACT['commits'],  QCY),
    (QCX,                          QCY - ARM * ACT['review']),
    (QCX + ARM * max(ACT['issues'], 0.03), QCY),
    (QCX,                          QCY + ARM * ACT['prs']),
]
POLY = " ".join(f"{x:.1f},{y:.1f}" for x, y in PVERTS)

# Primary dot (commits — furthest left)
DX = QCX - ARM * ACT['commits'] * 0.88
DY = QCY + ARM * ACT['prs'] * 0.4

QUADRANT = f"""
    <!-- Divider -->
    <line x1="{QX0}" y1="10" x2="{QX0}" y2="{AH-10}" stroke="{BORDER}" stroke-width="1" stroke-dasharray="4 3"/>

    <!-- Activity overview label -->
    <text x="{QX0+8}" y="22" fill="{MUTED}" font-family="{UI}" font-size="11" font-weight="600">Activity overview</text>

    <!-- Crosshair lines -->
    <line x1="{QCX-ARM}" y1="{QCY}" x2="{QCX+ARM}" y2="{QCY}" stroke="{BORDER}" stroke-width="1.5"/>
    <line x1="{QCX}" y1="{QCY-ARM}" x2="{QCX}" y2="{QCY+ARM}" stroke="{BORDER}" stroke-width="1.5"/>

    <!-- Activity polygon -->
    <polygon points="{POLY}" fill="#26a641" fill-opacity=".25" stroke="#39d353" stroke-width="1.5" stroke-linejoin="round"/>

    <!-- Center crosshair dot -->
    <circle cx="{QCX}" cy="{QCY}" r="4" fill="{HEADER_BG}" stroke="{BORDER}" stroke-width="1.5"/>

    <!-- Animated commits dot -->
    <circle cx="{DX:.1f}" cy="{DY:.1f}" r="5" fill="#39d353" fill-opacity=".3">
      <animate attributeName="r" values="5;11;5" dur="2.2s" repeatCount="indefinite"/>
      <animate attributeName="fill-opacity" values=".3;0;.3" dur="2.2s" repeatCount="indefinite"/>
    </circle>
    <circle cx="{DX:.1f}" cy="{DY:.1f}" r="5" fill="#39d353"/>
    <circle cx="{QCX}" cy="{QCY}" r="4" fill="{HEADER_BG}" stroke="{BORDER}" stroke-width="1.5"/>

    <!-- Axis labels -->
    <text x="{QCX}" y="{QCY-ARM-14}" text-anchor="middle" fill="{MUTED}" font-family="{UI}" font-size="9">{int(ACT['review']*100)}%</text>
    <text x="{QCX}" y="{QCY-ARM-4}" text-anchor="middle" fill="{MUTED}" font-family="{UI}" font-size="9">Code review</text>

    <text x="{QCX}" y="{QCY+ARM+12}" text-anchor="middle" fill="{MUTED}" font-family="{UI}" font-size="9">Pull requests</text>
    <text x="{QCX}" y="{QCY+ARM+22}" text-anchor="middle" fill="{MUTED}" font-family="{UI}" font-size="9">{int(ACT['prs']*100)}%</text>

    <text x="{QCX-ARM-6}" y="{QCY-5}" text-anchor="end" fill="{MUTED}" font-family="{UI}" font-size="9">Commits</text>
    <text x="{QCX-ARM-6}" y="{QCY+6}" text-anchor="end" fill="{MUTED}" font-family="{UI}" font-size="9">{int(ACT['commits']*100)}%</text>

    <text x="{QCX+ARM+6}" y="{QCY+4}" text-anchor="start" fill="{MUTED}" font-family="{UI}" font-size="9">Issues</text>"""

ACTIVITY_SVG = f"""<svg width="{AW}" height="{AH}" viewBox="0 0 {AW} {AH}" fill="none" xmlns="http://www.w3.org/2000/svg" role="img" aria-label="GitHub contribution activity map">
  <defs><clipPath id="ac"><rect width="{AW}" height="{AH}" rx="8"/></clipPath></defs>
  <g clip-path="url(#ac)">
    <rect width="{AW}" height="{AH}" fill="{BG}"/>

    <!-- Section header -->
    <text x="{GX}" y="20" fill="#e6edf3" font-family="{UI}" font-size="12" font-weight="600">{total_contribs:,} contributions in the last year</text>

    <!-- Month labels -->
    {MONTH_LABELS}

    <!-- Day labels -->
    {DAY_LABELS}

    <!-- Contribution grid -->
    {GRID}

    <!-- Legend -->
    {LEGEND_ELS}

    <!-- Quadrant chart -->
    {QUADRANT}
  </g>
  <rect width="{AW}" height="{AH}" rx="8" fill="none" stroke="{BORDER}" stroke-width="1"/>
</svg>"""

# ─────────────────────────────────────────────
#  Write output files
# ─────────────────────────────────────────────
os.makedirs(OUT, exist_ok=True)

chat_path = os.path.join(OUT, 'chat_animation.svg')
with open(chat_path, 'w', encoding='utf-8') as f:
    f.write(CHAT_SVG)
print(f"✓ chat_animation.svg  ({len(CHAT_SVG):,} bytes)")

map_path = os.path.join(OUT, 'activity_map.svg')
with open(map_path, 'w', encoding='utf-8') as f:
    f.write(ACTIVITY_SVG)
print(f"✓ activity_map.svg    ({len(ACTIVITY_SVG):,} bytes)")
