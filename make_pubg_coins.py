import xml.etree.ElementTree as ET
import os

def make_pubg_coin(name, brand_color_outer, brand_color_inner, logo_svg, sheen_delay='0s'):
    svg = f"""<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 64 64" width="56" height="56">
  <defs>
    <!-- Tactical Gunmetal Bevel Rim -->
    <linearGradient id="tacticalRim_{name}" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" stop-color="#94A3B8" />
      <stop offset="25%" stop-color="#475569" />
      <stop offset="50%" stop-color="#CBD5E1" />
      <stop offset="75%" stop-color="#1E293B" />
      <stop offset="100%" stop-color="#334155" />
    </linearGradient>

    <!-- Combat Face Radial -->
    <radialGradient id="combatFace_{name}" cx="35%" cy="35%" r="65%">
      <stop offset="0%" stop-color="{brand_color_inner}" />
      <stop offset="65%" stop-color="{brand_color_outer}" />
      <stop offset="100%" stop-color="#080C14" />
    </radialGradient>

    <!-- Tactical Radar Sheen -->
    <linearGradient id="sheen_{name}" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" stop-color="#ffffff" stop-opacity="0" />
      <stop offset="45%" stop-color="#ffffff" stop-opacity="0.05" />
      <stop offset="50%" stop-color="#00f0ff" stop-opacity="0.7" />
      <stop offset="55%" stop-color="#ffffff" stop-opacity="0.05" />
      <stop offset="100%" stop-color="#ffffff" stop-opacity="0" />
    </linearGradient>

    <filter id="depth_{name}" x="-15%" y="-15%" width="130%" height="130%">
      <feDropShadow dx="0" dy="3.5" stdDeviation="2.5" flood-color="#000000" flood-opacity="0.75" />
    </filter>

    <clipPath id="faceClip_{name}">
      <circle cx="32" cy="32" r="23" />
    </clipPath>
  </defs>

  <style>
    @keyframes sheenSweep_{name} {{
      0% {{ transform: translateX(-64px) translateY(-64px); }}
      35%, 100% {{ transform: translateX(64px) translateY(64px); }}
    }}
    .coin-sheen_{name} {{
      animation: sheenSweep_{name} 3.5s cubic-bezier(0.4, 0, 0.2, 1) infinite;
      animation-delay: {sheen_delay};
    }}
  </style>

  <!-- 3D Ground Shadow -->
  <circle cx="32" cy="34.5" r="27" fill="#000000" opacity="0.6" />

  <!-- Heavy Outer Tactical Rim -->
  <circle cx="32" cy="32" r="27" fill="url(#tacticalRim_{name})" filter="url(#depth_{name})" />

  <!-- Military Beveled Ring -->
  <circle cx="32" cy="32" r="24.5" fill="none" stroke="#0F172A" stroke-width="1.2" />
  <circle cx="32" cy="32" r="23.5" fill="none" stroke="#94A3B8" stroke-width="0.8" stroke-opacity="0.7" />

  <!-- 4 Tactical Rivet Bolts -->
  <circle cx="32" cy="6.5" r="1.3" fill="#E2E8F0" stroke="#0F172A" stroke-width="0.6" />
  <circle cx="57.5" cy="32" r="1.3" fill="#E2E8F0" stroke="#0F172A" stroke-width="0.6" />
  <circle cx="32" cy="57.5" r="1.3" fill="#E2E8F0" stroke="#0F172A" stroke-width="0.6" />
  <circle cx="6.5" cy="32" r="1.3" fill="#E2E8F0" stroke="#0F172A" stroke-width="0.6" />

  <!-- Recessed Combat Face -->
  <circle cx="32" cy="32" r="23" fill="url(#combatFace_{name})" />

  <!-- Tactical Reticle Crosshairs (PUBG sight notches) -->
  <path d="M 32 10 L 32 13 M 32 51 L 32 54 M 10 32 L 13 32 M 51 32 L 54 32" stroke="#00F0FF" stroke-width="1.3" stroke-opacity="0.8" />

  <!-- Embossed Official Brand Logo -->
  <g fill="#FFFFFF" opacity="0.95">
    {logo_svg}
  </g>

  <!-- Animated Cyan Laser Sheen -->
  <g clip-path="url(#faceClip_{name})">
    <rect class="coin-sheen_{name}" x="-32" y="-32" width="128" height="128" fill="url(#sheen_{name})" />
  </g>

  <!-- Top Rim Specular Glint -->
  <path d="M 14 18 A 24 24 0 0 1 50 18" fill="none" stroke="#FFFFFF" stroke-width="1.1" stroke-opacity="0.5" />
</svg>"""
    # Verify XML is 100% valid
    ET.fromstring(svg)
    return svg

# 1. LinkedIn
linkedin_logo = """<g transform="translate(21, 21)">
  <rect x="0.5" y="7" width="4.5" height="15" rx="1" />
  <circle cx="2.7" cy="2.3" r="2.5" />
  <path d="M 8 7 L 12.3 7 L 12.3 9.2 C 13.2 7.8 15.1 6.8 17.3 6.8 C 21 6.8 23 9.2 23 13.8 L 23 22 L 18.5 22 L 18.5 14.5 C 18.5 12.6 17.7 11.5 16 11.5 C 14.3 11.5 13.4 12.7 13.4 14.7 L 13.4 22 L 8.9 22 L 8.9 7 Z" />
</g>"""

# 2. Gmail
gmail_logo = """<g transform="translate(19.5, 22)">
  <path d="M 2 3 C 0.9 3 0 3.9 0 5 L 0 20 C 0 21.1 0.9 22 2 22 L 23 22 C 24.1 22 25 21.1 25 20 L 25 5 C 25 3.9 24.1 3 23 3 L 2 3 Z M 12.5 13.8 L 3.5 6 L 21.5 6 L 12.5 13.8 Z M 2 7.5 L 8 13 L 2 18.5 L 2 7.5 Z M 23 7.5 L 23 18.5 L 17 13 L 23 7.5 Z M 9.5 14.2 L 12.5 16.5 L 15.5 14.2 L 21.2 20 L 3.8 20 L 9.5 14.2 Z" />
</g>"""

# 3. GitHub
github_logo = """<g transform="translate(20, 20)">
  <path d="M 12 0 C 5.4 0 0 5.4 0 12 C 0 17.3 3.4 21.8 8.2 23.4 C 8.8 23.5 9 23.1 9 22.8 C 9 22.5 9 21.5 9 20.3 C 5.6 21 4.9 18.7 4.9 18.7 C 4.4 17.4 3.6 17 3.6 17 C 2.6 16.2 3.7 16.3 3.7 16.3 C 4.9 16.3 5.5 17.5 5.5 17.5 C 6.6 19.3 8.4 18.7 9.1 18.4 C 9.2 17.6 9.5 17.1 9.9 16.8 C 7.2 16.5 4.4 15.4 4.4 10.7 C 4.4 9.4 4.9 8.3 5.7 7.5 C 5.6 7.2 5.1 5.9 5.9 4.3 C 5.9 4.3 6.9 4 9.1 5.6 C 10.1 5.3 11.1 5.2 12.1 5.2 C 13.1 5.2 14.1 5.3 15.1 5.6 C 17.3 4 18.3 4.3 18.3 4.3 C 19.1 5.9 18.6 7.2 18.5 7.5 C 19.3 8.3 19.8 9.4 19.8 10.7 C 19.8 15.4 17 16.5 14.3 16.8 C 14.7 17.2 15.1 18 15.1 19.1 C 15.1 20.7 15.1 22.1 15.1 22.5 C 15.1 22.9 15.4 23.3 16 23.1 C 20.8 21.6 24.2 17.2 24.2 12 C 24 5.4 18.6 0 12 0 Z" />
</g>"""

# 4. X (Twitter)
x_logo = """<g transform="translate(22, 22)">
  <path d="M 15.7 0 L 19.3 0 L 11.4 9.0 L 20.7 21 L 13.4 21 L 7.7 13.6 L 1.2 21 L -2.4 21 L 5.9 11.4 L -2.9 0 L 4.5 0 L 9.7 6.8 L 15.7 0 Z M 14.4 18.9 L 16.4 18.9 L 4.0 2.0 L 1.9 2.0 L 14.4 18.9 Z" />
</g>"""

out_dir = r'C:\Users\Ishan Gupta\.gemini\antigravity\scratch\github-profile\assets'
os.makedirs(out_dir, exist_ok=True)

coins = [
    ('coin_linkedin.svg', 'linkedin', '#004B87', '#0077B5', linkedin_logo, '0s'),
    ('coin_gmail.svg', 'gmail', '#8B0000', '#EA4335', gmail_logo, '0.9s'),
    ('coin_github.svg', 'github', '#161B22', '#334155', github_logo, '1.8s'),
    ('coin_x.svg', 'x', '#0B0F19', '#1E293B', x_logo, '2.7s')
]

for filename, name, outer, inner, logo, delay in coins:
    svg_content = make_pubg_coin(name, outer, inner, logo, delay)
    path = os.path.join(out_dir, filename)
    with open(path, 'w', encoding='utf-8') as f:
        f.write(svg_content)
    print(f'Successfully generated {filename} ({os.path.getsize(path)} bytes)')
