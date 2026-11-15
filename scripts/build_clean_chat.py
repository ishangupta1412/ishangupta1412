"""
Generate clean, minimal iMessage-style floating text pop-up bubbles for Ishan Gupta.
- Clean floating rounded bubbles (NO WhatsApp frame, NO terminal box, NO fake images)
- NO Delhi mention
- NO links in text (refers directly to the coins below)
- Sequential fade-in pop-up animation
- Full Light & Dark mode support
"""

W = 650
H = 380

BUBBLES = [
    {
        "y": 15,
        "w": 220,
        "h": 44,
        "text": "Hey there! I'm Ishan 👋",
        "font_size": 15.5,
        "delay": "0.2s"
    },
    {
        "y": 72,
        "w": 485,
        "h": 44,
        "text": "First-year engineering student passionate about math &amp; computing 📐⚡",
        "font_size": 14.5,
        "delay": "0.6s"
    },
    {
        "y": 129,
        "w": 505,
        "h": 44,
        "text": "I love building clean software, diving into algorithms &amp; experimenting with AI 💻🚀",
        "font_size": 14,
        "delay": "1.0s"
    },
    {
        "y": 186,
        "w": 460,
        "h": 44,
        "text": "Always curious, learning continuously and solving hard problems 💡✨",
        "font_size": 14.5,
        "delay": "1.4s"
    },
    {
        "y": 243,
        "w": 405,
        "h": 44,
        "text": "You can connect with me on LinkedIn, Gmail, and X 👇",
        "font_size": 14.5,
        "delay": "1.8s"
    },
    {
        "y": 300,
        "w": 225,
        "h": 44,
        "text": "Have a great day ahead! ✌️",
        "font_size": 15.5,
        "delay": "2.2s"
    }
]

def generate_clean_chat_svg():
    bubbles_svg = []
    style_classes = []

    for i, b in enumerate(BUBBLES):
        n = i + 1
        y, w, h = b["y"], b["w"], b["h"]
        fs = b["font_size"]
        text = b["text"]
        delay = b["delay"]

        style_classes.append(f"""
    .bubble-{n} {{
      opacity: 0;
      animation: popIn 0.4s cubic-bezier(0.16, 1, 0.3, 1) {delay} forwards;
    }}""")

        bubbles_svg.append(f"""
    <!-- Message {n} -->
    <g class="bubble-{n}">
      <rect x="20" y="{y}" width="{w}" height="{h}" rx="18" class="bubble-bg" />
      <text x="36" y="{y + 27}" class="bubble-text font-ui" font-size="{fs}">{text}</text>
    </g>""")

    css_classes = "\n".join(style_classes)
    bubbles_code = "\n".join(bubbles_svg)

    svg = f"""<svg width="{W}" height="{H}" viewBox="0 0 {W} {H}" fill="none" xmlns="http://www.w3.org/2000/svg" role="img" aria-label="Ishan Gupta - Introduction">
  <style>
    .font-ui {{
      font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial, sans-serif;
      letter-spacing: -0.01em;
    }}
    .bubble-bg {{
      fill: #e9e9eb;
      transition: fill 0.3s;
    }}
    .bubble-text {{
      fill: #1c1c1e;
      font-weight: 450;
    }}

    @media (prefers-color-scheme: dark) {{
      .bubble-bg {{
        fill: #2c2c2e;
      }}
      .bubble-text {{
        fill: #f2f2f7;
      }}
    }}

    @keyframes popIn {{
      0% {{
        opacity: 0;
      }}
      100% {{
        opacity: 1;
      }}
    }}
{css_classes}
  </style>

  <!-- Message Bubbles Stack -->
  <g>
{bubbles_code}
  </g>
</svg>"""
    return svg

if __name__ == "__main__":
    out_path = r"C:\Users\Ishan Gupta\.gemini\antigravity\scratch\github-profile\assets\chat_animation.svg"
    svg = generate_clean_chat_svg()
    with open(out_path, "w", encoding="utf-8") as f:
        f.write(svg)
    print(f"Generated clean chat SVG at {out_path} ({len(svg):,} bytes)")

    import xml.etree.ElementTree as ET
    ET.fromstring(svg)
    print("XML is 100% VALID!")
