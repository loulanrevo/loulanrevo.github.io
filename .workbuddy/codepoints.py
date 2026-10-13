"""Show exact codepoint sequences for mojibake+PUA in each file."""
import os, glob, re

files = sorted(glob.glob(r'c:\Users\loulanRE\OneDrive\Desktop\blog\source-en\_posts\*.md'))

# Detect any non-ASCII problematic char: mojibake CJK (0x9200-0x95FF range) or PUA
def is_problem(ch):
    cp = ord(ch)
    if 0x9200 <= cp <= 0x95FF:
        return True
    if 0xE000 <= cp <= 0xF8FF:
        return True
    # Also detect common mojibake lead chars
    if ch in '鈥馃銇鏂鏃鏄鏅鏈鐗鐝鐞鑳钀钁锔锛閫閮闃闄鍋鍒鍕鍘鍚鍛鍝鍥鎰鎴鈮銈銉':
        return True
    return False

out = []
for f in files:
    with open(f, 'r', encoding='utf-8') as fh:
        text = fh.read()
    # Find all runs of problematic chars (including PUA) with optional trailing ?
    # A run = consecutive problem chars or CJK chars adjacent to problem chars
    problems = []
    i = 0
    while i < len(text):
        if is_problem(text[i]):
            # Find the extent of the problematic run
            j = i
            # Extend forward through CJK + PUA + ?
            while j < len(text):
                cp = ord(text[j])
                if 0x4E00 <= cp <= 0x9FFF or 0xE000 <= cp <= 0xF8FF or text[j] == '?':
                    j += 1
                else:
                    break
            run = text[i:j]
            cps = ' '.join(f'U+{ord(c):04X}' for c in run)
            start = max(0, i - 20)
            end = min(len(text), j + 20)
            ctx = text[start:end].replace('\n', ' ')
            problems.append((run, cps, ctx))
            i = j
        else:
            i += 1
    if problems:
        out.append(f'=== {os.path.basename(f)} ===')
        for run, cps, ctx in problems:
            out.append(f'  RUN: {repr(run)}')
            out.append(f'  CPS: {cps}')
            out.append(f'  CTX: ...{ctx}...')
        out.append('')

with open(r'c:\Users\loulanRE\OneDrive\Desktop\blog\.workbuddy\codepoint_report.txt', 'w', encoding='utf-8') as fh:
    fh.write('\n'.join(out))
print(f'Report written, {len(out)} lines')
