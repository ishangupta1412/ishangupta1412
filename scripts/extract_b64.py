with open('jason_template.svg', 'r', encoding='utf-8') as f:
    text = f.read()

idx = text.find('data:image/png;base64,')
print('Found base64 at index:', idx)
if idx != -1:
    end_idx = text.find('"', idx)
    b64_data = text[idx:end_idx]
    print('Base64 data length:', len(b64_data))
    with open('isometric_b64.txt', 'w', encoding='utf-8') as out:
        out.write(b64_data)
    print('Saved isometric_b64.txt successfully')
