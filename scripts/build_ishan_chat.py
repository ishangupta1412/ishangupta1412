import re, os

SRC = r"C:\Users\Ishan Gupta\.gemini\antigravity\scratch\github-profile\scripts\jason_chat.svg"
OUT = r"C:\Users\Ishan Gupta\.gemini\antigravity\scratch\github-profile\assets\chat_animation.svg"

with open(SRC, "r", encoding="utf-8") as f:
    svg = f.read()

# 1. Replace "Hi, I'm Jason" with "Hi, I'm Ishan"
svg = svg.replace("Hi, I'm Jason", "Hi, I'm Ishan")

# 2. Replace Columbus, Ohio with Delhi, India
svg = svg.replace(
    "I live in Columbus, Ohio where it’s supposed to be",
    "I live in Delhi, India where it’s supposed to be"
)
svg = svg.replace(
    "43° F (6° C) and <tspan class=\"emoji\">☁️</tspan> today.",
    "77° F (25° C) and <tspan class=\"emoji\">☀️</tspan> today."
)

# 3. Replace job description
svg = svg.replace(
    "I’m a product designer. I used to work at GitHub,",
    "I’m a systems engineer. I build enterprise SOC defense,"
)
svg = svg.replace(
    "but I’ve been at PlanetScale for almost 6 years now.",
    "multimodal AI, and high-performance web systems."
)

# 4. Message 4: keep the isometric contributions text exactly like Jason's!
# "My favorite project is isometric-contributions. It’s a"
# "browser extension that shows your GitHub"
# "contributions like this"
# It already has the isometric image right below it!

# 5. Social link: Bluesky -> X / Twitter
svg = svg.replace("You can find me on Bluesky at", "You can find me on X at")
svg = re.sub(
    r'<a xlink:href="https://bsky\.app/profile/jasonlong\.me">https://bsky\.app/profile/jasonlong\.me</a>',
    r'<a xlink:href="https://x.com/ishangupta1412">https://x.com/ishangupta1412</a>',
    svg
)
# Update rect width for message 5 if needed (X url is shorter)
# Old url: https://bsky.app/profile/jasonlong.me (35 chars)
# New url: https://x.com/ishangupta1412 (28 chars)

# 6. Final greeting
svg = re.sub(r'Have a great [A-Za-z]+! <tspan class="emoji">.*?</tspan>', 'Have a great day! <tspan class="emoji">✌️</tspan>', svg)
# Adjust width for "Have a great day! ✌️"
# Jason had {dayBubbleWidth} around 220-260, 220 is perfect.

with open(OUT, "w", encoding="utf-8") as f:
    f.write(svg)

print(f"Generated {OUT} ({len(svg):,} bytes)")
