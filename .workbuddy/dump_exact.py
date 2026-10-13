# Dump exact codepoint sequences for remaining mojibake
import os, glob

files_with_issues = {
    'Dark-and-Darker-Three-Day-Binge.md': [(915, 955), (1125, 1155)],
    'Fandom-Victory.md': [(600, 625), (895, 1000)],
    'Group-Project-Agony.md': [(3785, 3810), (3990, 4015)],
    'Magic-Attack-vs-Counselor.md': [(1280, 1305)],
    'Northeast-Southwest-Victorious-Reunion.md': [(1175, 1200)],
    'Ocean-Painting-and-Seaside-Trip.md': [(4010, 4060)],
}

base = r'c:\Users\loulanRE\OneDrive\Desktop\blog\source-en\_posts'
out = []
for fname, ranges in files_with_issues.items():
    fpath = os.path.join(base, fname)
    with open(fpath, 'r', encoding='utf-8') as fh:
        text = fh.read()
    out.append(f'=== {fname} ===')
    for start, end in ranges:
        out.append(f'  Range [{start}:{end}]:')
        for i in range(start, min(end, len(text))):
            ch = text[i]
            cp = ord(ch)
            out.append(f'    [{i}] U+{cp:04X} {ch!r}')
    out.append('')

with open(r'c:\Users\loulanRE\OneDrive\Desktop\blog\.workbuddy\exact_codepoints.txt', 'w', encoding='utf-8') as fh:
    fh.write('\n'.join(out))
print('Done')
