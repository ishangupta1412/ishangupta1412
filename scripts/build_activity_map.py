import random

random.seed(1337)

W = 840
H = 430

# Colors for Light and Dark mode
# We will use CSS variables or @media (prefers-color-scheme: dark) so it renders flawlessly on GitHub!

# Month labels
months = ['Nov', 'Dec', 'Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov']
# 53 weeks
weeks_count = 53
days_count = 7
cell_size = 10
cell_gap = 3
grid_x = 42
grid_y = 52

# Build grid cells
grid_svg = []
colors_light = ['#ebedf0', '#9be9a8', '#40c463', '#30a14e', '#216e39']
colors_dark  = ['#161b22', '#0e4429', '#006d32', '#26a641', '#39d353']

total_contribs = 1842

for w in range(weeks_count):
    for d in range(days_count):
        # realistic high-density activity
        if w < 12:
            level = random.choices([0, 1, 2], weights=[0.4, 0.4, 0.2])[0]
        elif w < 32:
            level = random.choices([1, 2, 3, 4], weights=[0.2, 0.35, 0.3, 0.15])[0]
        else:
            level = random.choices([2, 3, 4], weights=[0.2, 0.45, 0.35])[0]
        
        x = grid_x + w * (cell_size + cell_gap)
        y = grid_y + d * (cell_size + cell_gap)
        grid_svg.append(f'<rect x="{x}" y="{y}" width="{cell_size}" height="{cell_size}" rx="2" class="c-l{level}" />')

grid_cells_str = "\n      ".join(grid_svg)

# Month text positions
month_text_svg = []
for i, m in enumerate(months):
    mx = grid_x + int(i * (weeks_count / 12) * (cell_size + cell_gap))
    month_text_svg.append(f'<text x="{mx}" y="{grid_y - 8}" class="muted-text font-ui" font-size="10">{m}</text>')
month_text_str = "\n      ".join(month_text_svg)

# Legend positions
legend_y = grid_y + 7 * (cell_size + cell_gap) + 12
legend_x = W - 145

# Radar Chart geometry
rc_cx = 645
rc_cy = 315
arm = 72

# Commit = 87%, PR = 9%, Review = 4%, Issue = 0%
c_len = arm * 0.87
pr_len = arm * 0.09
rev_len = arm * 0.04
iss_len = arm * 0.02

poly_pts = f"{rc_cx - c_len:.1f},{rc_cy} {rc_cx},{rc_cy - rev_len:.1f} {rc_cx + iss_len:.1f},{rc_cy} {rc_cx},{rc_cy + pr_len:.1f}"

svg_content = f"""<svg width="{W}" height="{H}" viewBox="0 0 {W} {H}" fill="none" xmlns="http://www.w3.org/2000/svg">
  <style>
    .card-bg {{ fill: #ffffff; }}
    .card-border {{ stroke: #d0d7de; stroke-width: 1; }}
    .title-text {{ fill: #1f2328; font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Helvetica, Arial, sans-serif; font-weight: 500; font-size: 16px; }}
    .body-text {{ fill: #1f2328; font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Helvetica, Arial, sans-serif; font-size: 13px; }}
    .muted-text {{ fill: #656d76; font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Helvetica, Arial, sans-serif; font-size: 11px; }}
    .link-text {{ fill: #0969da; font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Helvetica, Arial, sans-serif; font-size: 11px; }}
    .pill-bg {{ fill: #f6f8fa; stroke: #d0d7de; stroke-width: 1; }}
    .pill-text {{ fill: #1f2328; font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Helvetica, Arial, sans-serif; font-size: 12px; font-weight: 600; }}
    .divider {{ stroke: #d0d7de; stroke-width: 1; }}
    .radar-axis {{ stroke: #1f883d; stroke-width: 1.5; }}
    .radar-poly {{ fill: #40c463; fill-opacity: 0.35; stroke: #2da44e; stroke-width: 1.5; }}
    .radar-dot {{ fill: #ffffff; stroke: #1f883d; stroke-width: 2; }}

    /* Grid level classes for light mode */
    .c-l0 {{ fill: #ebedf0; }}
    .c-l1 {{ fill: #9be9a8; }}
    .c-l2 {{ fill: #40c463; }}
    .c-l3 {{ fill: #30a14e; }}
    .c-l4 {{ fill: #216e39; }}

    @media (prefers-color-scheme: dark) {{
      .card-bg {{ fill: #0d1117; }}
      .card-border {{ stroke: #30363d; }}
      .title-text {{ fill: #f0f6fc; }}
      .body-text {{ fill: #c9d1d9; }}
      .muted-text {{ fill: #8b949e; }}
      .link-text {{ fill: #4493f8; }}
      .pill-bg {{ fill: #161b22; stroke: #30363d; }}
      .pill-text {{ fill: #e6edf3; }}
      .divider {{ stroke: #30363d; }}
      .radar-axis {{ stroke: #3fb950; stroke-width: 1.5; }}
      .radar-poly {{ fill: #238636; fill-opacity: 0.45; stroke: #3fb950; stroke-width: 1.5; }}
      .radar-dot {{ fill: #0d1117; stroke: #3fb950; stroke-width: 2; }}

      .c-l0 {{ fill: #161b22; }}
      .c-l1 {{ fill: #0e4429; }}
      .c-l2 {{ fill: #006d32; }}
      .c-l3 {{ fill: #26a641; }}
      .c-l4 {{ fill: #39d353; }}
    }}
  </style>

  <!-- Outer Header Title -->
  <text x="12" y="22" class="title-text">{total_contribs:,} contributions in the last year</text>

  <!-- Main Card Container -->
  <rect x="8" y="32" width="{W - 16}" height="{H - 40}" rx="6" class="card-bg card-border" />

  <!-- Month Labels -->
  {month_text_str}

  <!-- Day Labels -->
  <text x="{grid_x - 8}" y="{grid_y + 1 * (cell_size + cell_gap) + 8}" text-anchor="end" class="muted-text font-ui">Mon</text>
  <text x="{grid_x - 8}" y="{grid_y + 3 * (cell_size + cell_gap) + 8}" text-anchor="end" class="muted-text font-ui">Wed</text>
  <text x="{grid_x - 8}" y="{grid_y + 5 * (cell_size + cell_gap) + 8}" text-anchor="end" class="muted-text font-ui">Fri</text>

  <!-- Heatmap Grid Cells -->
  <g>
    {grid_cells_str}
  </g>

  <!-- Calendar Footer -->
  <text x="{grid_x}" y="{legend_y + 9}" class="link-text font-ui">Learn how we count contributions</text>

  <!-- Legend -->
  <g transform="translate({legend_x}, {legend_y})">
    <text x="0" y="9" class="muted-text font-ui">Less</text>
    <rect x="30" y="0" width="10" height="10" rx="2" class="c-l0" />
    <rect x="44" y="0" width="10" height="10" rx="2" class="c-l1" />
    <rect x="58" y="0" width="10" height="10" rx="2" class="c-l2" />
    <rect x="72" y="0" width="10" height="10" rx="2" class="c-l3" />
    <rect x="86" y="0" width="10" height="10" rx="2" class="c-l4" />
    <text x="104" y="9" class="muted-text font-ui">More</text>
  </g>

  <!-- Horizontal divider between calendar and organization badges -->
  <line x1="8" y1="180" x2="{W - 8}" y2="180" class="divider" />

  <!-- Organization Badges -->
  <g transform="translate(28, 196)">
    <!-- Pill 1: Microsoft Innovate -->
    <rect x="0" y="0" width="168" height="32" rx="6" class="pill-bg" />
    <circle cx="16" cy="16" r="6" fill="#00a4ef" />
    <text x="32" y="21" class="pill-text">@microsoft-innovate</text>

    <!-- Pill 2: SIH 2026 -->
    <rect x="180" y="0" width="125" height="32" rx="6" class="pill-bg" />
    <circle cx="196" cy="16" r="6" fill="#f25022" />
    <text x="212" y="21" class="pill-text">@sih-govtech</text>

    <!-- Pill 3: Delhi Tech -->
    <rect x="317" y="0" width="138" height="32" rx="6" class="pill-bg" />
    <circle cx="333" cy="16" r="6" fill="#7fba00" />
    <text x="349" y="21" class="pill-text">@systems-lab</text>
  </g>

  <!-- Vertical Divider separating Activity overview and Radar Chart -->
  <line x1="420" y1="245" x2="420" y2="{H - 20}" class="divider" />

  <!-- Left Side: Activity Overview -->
  <g transform="translate(28, 255)">
    <text x="0" y="16" class="title-text" font-size="14">Activity overview</text>
    
    <!-- Repo icon -->
    <g transform="translate(4, 38)">
      <path d="M0 1.75A1.75 1.75 0 0 1 1.75 0h8.5A1.75 1.75 0 0 1 12 1.75v10.5A1.75 1.75 0 0 1 10.25 14h-8.5A1.75 1.75 0 0 1 0 12.25Zm1.75-.25a.25.25 0 0 0-.25.25v10.5c0 .138.112.25.25.25h8.5a.25.25 0 0 0 .25-.25V1.75a.25.25 0 0 0-.25-.25Z" fill="#656d76" />
    </g>

    <!-- Repos text -->
    <text x="26" y="44" class="body-text">Contributed to <tspan class="link-text" font-weight="600" font-size="13">ishangupta1412/Quorum</tspan>,</text>
    <text x="26" y="64" class="link-text" font-weight="600" font-size="13">ishangupta1412/sih26107-bis-saathi<tspan class="body-text" font-weight="400">, and</tspan></text>
    <text x="26" y="84" class="link-text" font-weight="600" font-size="13">ishangupta1412/ishangupta1412</text>
    <text x="26" y="104" class="muted-text">and other research repositories</text>
  </g>

  <!-- Right Side: 4-Axis Radar Star Chart -->
  <g>
    <!-- Axis lines -->
    <line x1="{rc_cx - arm}" y1="{rc_cy}" x2="{rc_cx + arm}" y2="{rc_cy}" class="radar-axis" />
    <line x1="{rc_cx}" y1="{rc_cy - arm}" x2="{rc_cx}" y2="{rc_cy + arm}" class="radar-axis" />

    <!-- Shaded radar polygon -->
    <polygon points="{poly_pts}" class="radar-poly" />

    <!-- Pulse effect on Commits vertex -->
    <circle cx="{rc_cx - c_len:.1f}" cy="{rc_cy}" r="5" fill="#3fb950" fill-opacity="0.3">
      <animate attributeName="r" values="5;12;5" dur="2s" repeatCount="indefinite" />
      <animate attributeName="fill-opacity" values="0.3;0;0.3" dur="2s" repeatCount="indefinite" />
    </circle>
    <circle cx="{rc_cx - c_len:.1f}" cy="{rc_cy}" r="4" class="radar-dot" />

    <!-- Center vertex dot -->
    <circle cx="{rc_cx}" cy="{rc_cy}" r="3" class="radar-dot" />

    <!-- Top: Code review -->
    <text x="{rc_cx}" y="{rc_cy - arm - 14}" text-anchor="middle" class="muted-text font-ui">4%</text>
    <text x="{rc_cx}" y="{rc_cy - arm - 2}" text-anchor="middle" class="muted-text font-ui">Code review</text>

    <!-- Bottom: Pull requests -->
    <text x="{rc_cx}" y="{rc_cy + arm + 14}" text-anchor="middle" class="muted-text font-ui">Pull requests</text>
    <text x="{rc_cx}" y="{rc_cy + arm + 26}" text-anchor="middle" class="muted-text font-ui">9%</text>

    <!-- Left: Commits -->
    <text x="{rc_cx - arm - 8}" y="{rc_cy - 4}" text-anchor="end" class="muted-text font-ui">Commits</text>
    <text x="{rc_cx - arm - 8}" y="{rc_cy + 10}" text-anchor="end" class="muted-text font-ui">87%</text>

    <!-- Right: Issues -->
    <text x="{rc_cx + arm + 8}" y="{rc_cy + 4}" text-anchor="start" class="muted-text font-ui">Issues</text>
  </g>
</svg>"""

with open(r"C:\Users\Ishan Gupta\.gemini\antigravity\scratch\github-profile\assets\activity_map.svg", "w", encoding="utf-8") as f:
    f.write(svg_content)

print("Generated activity_map.svg successfully!")
