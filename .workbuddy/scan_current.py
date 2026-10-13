#!/usr/bin/env python3
"""Scan all English _posts files for remaining mojibake."""
import os
import re

BASE = r'c:\Users\loulanRE\OneDrive\Desktop\blog\source-en\_posts'

# Mojibake indicator ranges:
# - U+9200-U+95FF (CJK Unified Ideographs that are rare/uncommon - often mojibake)
# - U+E000-U+F8FF (PUA - Private Use Area, always mojibake)
# - U+0400-U+04FF (Cyrillic - appears in mojibake of Japanese)
# - U+0500-U+058F (Cyrillic Supplement - Armenian appears in mojibake)
# - U+0080-U+00FF (Latin-1 Supplement - € etc. appears in mojibake)

def is_mojibake_char(cp):
    # PUA - always mojibake
    if 0xE000 <= cp <= 0xF8FF:
        return True
    # Cyrillic - shouldn't appear in English blog posts
    if 0x0400 <= cp <= 0x052F:
        return True
    # Armenian - shouldn't appear
    if 0x0530 <= cp <= 0x058F:
        return True
    # CJK Unified Ideographs range U+9200-U+95FF - these are rare chars
    # commonly produced by GBK misinterpretation of UTF-8
    # But we need to be careful - some may be legitimate
    if 0x9200 <= cp <= 0x95FF:
        return True
    return False

# Known mojibake sequences and their fixes
KNOWN_MOJIBAKE = {
    '鈥?': '— (em-dash)',  # U+9225 U+003F
    '鈮?': '≥ (greater-or-equal)',  # U+922E U+003F
    '鈥揝': '– (en-dash + S)',  # U+9225 U+63DD
    '馃挰': '💬 (comments emoji)',  # U+9983 U+6330
    '馃寪': '🖥️ (desktop emoji)',  # U+9983 U+5BEA
    '馃枼锔?': '🖼️ (image emoji)',  # U+9983 U+67BC U+9514 U+003F
    '馃摑': '📝 (memo emoji)',  # U+9983 U+6451
    '馃敡': '⚙️ (gear emoji)',  # U+9983 U+6561
    '馃悕': '🐍 (snake emoji)',  # U+9983 U+6095
    '馃摝': '📦 (package emoji)',  # U+9983 U+645D
    '馃搸': '🎨 (palette emoji)',  # U+9983 U+6438
    '馃摃': '📄 (page emoji)',  # U+9983 U+6443
}

results = {}
files_with_mojibake = 0
total_mojibake = 0

for fname in sorted(os.listdir(BASE)):
    if not fname.endswith('.md'):
        continue
    fpath = os.path.join(BASE, fname)
    with open(fpath, 'r', encoding='utf-8') as fh:
        text = fh.read()

    file_hits = []

    # Check for known mojibake sequences first
    for seq, desc in KNOWN_MOJIBAKE.items():
        if seq in text:
            count = text.count(seq)
            # Get first context
            idx = text.find(seq)
            start = max(0, idx - 30)
            end = min(len(text), idx + len(seq) + 30)
            ctx = text[start:end].replace('\n', '\\n')
            file_hits.append((seq, count, desc, ctx))

    # Check for any character in mojibake ranges
    for i, ch in enumerate(text):
        cp = ord(ch)
        if is_mojibake_char(cp):
            # Check if it's part of a known sequence already found
            # Get surrounding context
            start = max(0, i - 5)
            end = min(len(text), i + 10)
            run = text[start:end]
            # Check if this char is in a known sequence
            in_known = False
            for seq, _ in KNOWN_MOJIBAKE.items():
                if ch in seq:
                    # Check if this specific occurrence is part of that sequence
                    for j in range(max(0, i - len(seq) + 1), i + 1):
                        if text[j:j+len(seq)] == seq:
                            in_known = True
                            break
                    if in_known:
                        break
            if not in_known:
                ctx_start = max(0, i - 30)
                ctx_end = min(len(text), i + 30)
                ctx = text[ctx_start:ctx_end].replace('\n', '\\n')
                file_hits.append((ch, 1, f'U+{cp:04X}', ctx))

    if file_hits:
        files_with_mojibake += 1
        results[fname] = file_hits
        total_mojibake += sum(h[1] for h in file_hits)

print(f'=== Scan Results ===')
print(f'Files with mojibake: {files_with_mojibake}')
print(f'Total mojibake occurrences: {total_mojibake}')
print()

for fname, hits in results.items():
    print(f'--- {fname} ---')
    for seq, count, desc, ctx in hits:
        print(f'  [{desc}] x{count}: ...{ctx}...')
    print()
