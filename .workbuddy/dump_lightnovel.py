# Dump codepoints around "Light novel" in Northeast-Southwest file
import os

fpath = os.path.join(r'c:\Users\loulanRE\OneDrive\Desktop\blog\source-en\_posts',
                     'Northeast-Southwest-Victorious-Reunion.md')
with open(fpath, 'r', encoding='utf-8') as fh:
    text = fh.read()

# Find "Light novel"
idx = text.find('Light novel')
if idx >= 0:
    # Find the ( after it
    paren_idx = text.find('(', idx)
    if paren_idx >= 0:
        start = paren_idx + 1
        # Find the ? or ) after the mojibake
        end = text.find('?', start)
        if end >= 0:
            end += 1  # include the ?
            print(f'Mojibake range [{start}:{end}]:')
            for i in range(start, end):
                ch = text[i]
                cp = ord(ch)
                print(f'  [{i}] U+{cp:04X} {ch!r}')
            print(f'\nFull string: {text[start:end]!r}')
            print(f'As Python escapes: ', end='')
            for ch in text[start:end]:
                print(f'\\u{ord(ch):04x}', end='')
            print()
