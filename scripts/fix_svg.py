import re

path = r'C:\Users\Ishan Gupta\.gemini\antigravity\scratch\github-profile\assets\chat_animation.svg'
with open(path, 'r', encoding='utf-8') as f:
    content = f.read()

print("Before fix:")
print("  unquoted font-family:", content.count("font-family='SFMono"))
print("  mojibake dots:", content.count('Â·'))

# Fix 1: unquoted/broken font-family on text elements
# Pattern: font-family='SFMono-Regular',Consolas,'Liberation Mono',monospace
bad_ff = "font-family='SFMono-Regular',Consolas,'Liberation Mono',monospace"
good_ff = 'font-family="SFMono-Regular,Consolas,Liberation Mono,monospace"'
content = content.replace(bad_ff, good_ff)

# Fix 2: mojibake middle dot character
content = content.replace('\xc2\xb7', '\u00b7')  # UTF-8 double-encoded
content = content.replace('Â·', '·')
content = content.replace('Â', '')

print("\nAfter fix:")
print("  unquoted font-family:", content.count("font-family='SFMono"))
print("  mojibake dots:", content.count('Â·'))

# Validate: try parsing as XML
import xml.etree.ElementTree as ET
try:
    ET.fromstring(content)
    print("  XML: VALID ✓")
except ET.ParseError as e:
    print(f"  XML ERROR: {e}")
    # Find the problematic line
    lines = content.split('\n')
    err_line = e.position[0] - 1
    print(f"  Line {e.position[0]}: {lines[err_line][:120]}")

with open(path, 'w', encoding='utf-8') as f:
    f.write(content)
print("\nSaved.")
