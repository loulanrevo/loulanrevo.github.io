"""Show each mojibake token with surrounding context, grouped by file.
Also detect PUA (Private Use Area) characters which are another form of font-glyph mojibake.
"""
import os, glob, re

files = sorted(glob.glob(r'c:\Users\loulanRE\OneDrive\Desktop\blog\source-en\_posts\*.md'))

MOJI = set('鈥馃銇鏂鏃鏄鏅鏈鐗鐝鐞鑳钀钁锔锛閫閮闃闄鍋鍒鍕鍘鍚鍛鍝鍥鎰鎴鈮銈銉鍣鎬鎱鏆鏌鏎鏋鏌鎬')

def is_problem(ch):
    cp = ord(ch)
    if ch in MOJI:
        return True
    if 0x9200 <= cp <= 0x95FF:
        return True
    # PUA ranges (font-emoji / icon-font mojibake)
    if 0xE000 <= cp <= 0xF8FF or 0xF0000 <= cp <= 0xFFFFD or 0x100000 <= cp <= 0x10FFFD:
        return True
    return False

out = []
for f in files:
    with open(f, 'r', encoding='utf-8') as fh:
        text = fh.read()
    contexts = []
    # Find runs of CJK + optional ?, or PUA chars
    for m in re.finditer(r'[\u4e00-\u9fff]{1,}\??|[\ue000-\uf8ff]', text):
        tok = m.group(0)
        if any(is_problem(c) for c in tok):
            start = max(0, m.start() - 25)
            end = min(len(text), m.end() + 25)
            ctx = text[start:end].replace('\n', ' ')
            # Show codepoints for PUA
            cps = ' '.join(f'U+{ord(c):04X}' for c in tok if is_problem(c))
            contexts.append((tok, ctx, cps))
    if contexts:
        out.append(f'=== {os.path.basename(f)} ===')
        for tok, ctx, cps in contexts:
            out.append(f'  TOKEN: {repr(tok)}  [{cps}]')
            out.append(f'    CONTEXT: ...{ctx}...')
        out.append('')

with open(r'c:\Users\loulanRE\OneDrive\Desktop\blog\.workbuddy\mojibake_report.txt', 'w', encoding='utf-8') as fh:
    fh.write('\n'.join(out))
print('Report written. Lines:', len(out))
