# Scan for remaining mojibake in English files.
# Reports characters in mojibake ranges: U+9200-U+95FF, U+4E00-U+4FFF (when from mojibake),
# PUA U+E000-U+F8FF, U+9900-U+99FF (馃 emoji mojibake), etc.
import os, glob, re

files = sorted(glob.glob(r'c:\Users\loulanRE\OneDrive\Desktop\blog\source-en\_posts\*.md'))

# Ranges that indicate mojibake
def is_mojibake(cp):
    if 0x9200 <= cp <= 0x95FF:  # 鈥? etc.
        return True
    if 0xE000 <= cp <= 0xF8FF:  # PUA
        return True
    if 0x9900 <= cp <= 0x99FF:  # 馃 emoji mojibake
        return True
    if 0x9280 <= cp <= 0x9290:  # 銉 Japanese kana mojibake
        return True
    if 0x9340 <= cp <= 0x9480:  # various
        return True
    if cp == 0x2562:  # Box drawing
        return True
    if cp == 0x2C88:  # rare
        return True
    return False

out = []
for f in files:
    with open(f, 'r', encoding='utf-8') as fh:
        text = fh.read()
    basename = os.path.basename(f)
    hits = []
    for i, ch in enumerate(text):
        cp = ord(ch)
        if is_mojibake(cp):
            ctx_start = max(0, i-30)
            ctx_end = min(len(text), i+30)
            ctx = text[ctx_start:ctx_end].replace('\n', '\\n')
            hits.append((i, ch, cp, ctx))
    if hits:
        out.append(f'=== {basename} === ({len(hits)} hits)')
        for i, ch, cp, ctx in hits:
            out.append(f'  pos={i} char={ch!r} cp=U+{cp:04X} ctx=...{ctx}...')
        out.append('')

with open(r'c:\Users\loulanRE\OneDrive\Desktop\blog\.workbuddy\remaining_mojibake.txt', 'w', encoding='utf-8') as fh:
    fh.write('\n'.join(out))
print(f'Done. {sum(1 for l in out if l.startswith("==="))} files with mojibake.')
