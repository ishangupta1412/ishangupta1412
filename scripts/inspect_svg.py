import re

with open(r"C:\Users\Ishan Gupta\.gemini\antigravity\scratch\github-profile\scripts\jason_chat.svg", "r", encoding="utf-8") as f:
    svg = f.read()

# Let's find all <text> elements
texts = re.findall(r'<text[^>]*>(.*?)</text>', svg, re.DOTALL)
for t in texts:
    print("TEXT:", t.strip())
