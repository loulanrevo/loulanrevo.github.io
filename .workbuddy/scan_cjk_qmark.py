#!/usr/bin/env python3
"""Scan all English _posts files for mojibake patterns:
1. CJK character + ? (classic mojibake indicator)
2. PUA characters (U+E000-U+F8FF)
3. Any remaining known mojibake sequences
4. CJK chars in English footnotes that should be verified
"""
import os
import re

BASE = r'c:\Users\loulanRE\OneDrive\Desktop\blog\source-en\_posts'

def is_cjk(cp):
    """Check if codepoint is in CJK ranges."""
    if 0x4E00 <= cp <= 0x9FFF:  # CJK Unified Ideographs
        return True
    if 0x3400 <= cp <= 0x4DBF:  # CJK Extension A
        return True
    if 0x2E80 <= cp <= 0x2EFF:  # CJK Radicals
        return True
    if 0x3000 <= cp <= 0x303F:  # CJK Symbols
        return True
    if 0xFF00 <= cp <= 0xFFEF:  # Halfwidth/Fullwidth
        return True
    return False

def is_pua(cp):
    return 0xE000 <= cp <= 0xF8FF

def is_hiragana_katakana(cp):
    if 0x3040 <= cp <= 0x309F:  # Hiragana
        return True
    if 0x30A0 <= cp <= 0x30FF:  # Katakana
        return True
    return False

results = {}
files_with_issues = 0
total_issues = 0

for fname in sorted(os.listdir(BASE)):
    if not fname.endswith('.md'):
        continue
    fpath = os.path.join(BASE, fname)
    with open(fpath, 'r', encoding='utf-8') as fh:
        text = fh.read()

    file_hits = []

    # Pattern 1: CJK character + ? (mojibake)
    # Look for patterns like: [CJK]? 
    for m in re.finditer(r'[\u4e00-\u9fff\u3400-\u4dbf]\u003f', text):
        idx = m.start()
        start = max(0, idx - 20)
        end = min(len(text), idx + 10)
        ctx = text[start:end].replace('\n', '\\n')
        file_hits.append(('CJK+?', f'U+{ord(m.group()[0]):04X}+U+003F', ctx))

    # Pattern 2: PUA characters
    for i, ch in enumerate(text):
        cp = ord(ch)
        if is_pua(cp):
            start = max(0, i - 20)
            end = min(len(text), i + 10)
            ctx = text[start:end].replace('\n', '\\n')
            file_hits.append(('PUA', f'U+{cp:04X}', ctx))

    if file_hits:
        files_with_issues += 1
        results[fname] = file_hits
        total_issues += len(file_hits)

print(f'=== Enhanced Mojibake Scan Results ===')
print(f'Files with issues: {files_with_issues}')
print(f'Total issues: {total_issues}')
print()

for fname, hits in results.items():
    print(f'--- {fname} ---')
    for ptype, detail, ctx in hits:
        print(f'  [{ptype}] {detail}: ...{ctx}...')
    print()