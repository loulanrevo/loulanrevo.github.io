"""Analyze mojibake patterns in English blog posts.

The garbled text is UTF-8 bytes that were misread as GBK/CP936, then re-saved as UTF-8.
To recover: take the mojibake string, encode as GBK to get the original UTF-8 bytes,
then decode as UTF-8.

Problem: some bytes were unrecoverable and became '?' (ASCII 0x3F). Those need
context-based manual fixing.
"""
import os, glob, re

files = glob.glob(r'c:\Users\loulanRE\OneDrive\Desktop\blog\source-en\_posts\*.md')

# Collect all distinct mojibake tokens (runs of CJK chars, optionally with trailing ?)
token_pat = re.compile(r'[\u9200-\u95ff\u9300-\u93ff\u9400-\u947f\u9480-\u95ff]{2,}\??|鈥\?|馃[\u9fa5-\u9fff]?|銇\?[\u9280-\u92ff]*\??')

all_tokens = {}
for f in files:
    with open(f, 'r', encoding='utf-8') as fh:
        text = fh.read()
    for m in re.finditer(r'[\u4e00-\u9fff]{1,}\??', text):
        tok = m.group(0)
        # Filter: only keep tokens that contain at least one known mojibake char
        if any(c in '鈥馃銇鏂鏃鏄鏅鏈鐗鐝鐞鑳钀钁锔锛閫閮闃闄鍋鍒鍕鍘鍚鍛鍝鍥鎰鎴鈮銈銉' for c in tok):
            all_tokens.setdefault(tok, []).append(os.path.basename(f))

print("Distinct mojibake tokens found:")
for tok in sorted(all_tokens.keys()):
    files_using = set(all_tokens[tok])
    # Try to decode
    cleaned = tok.rstrip('?')
    try:
        decoded = cleaned.encode('gbk').decode('utf-8')
        status = f"  -> DECODED: '{decoded}'"
    except Exception as e:
        try:
            decoded = cleaned.encode('gb18030').decode('utf-8')
            status = f"  -> DECODED(gb18030): '{decoded}'"
        except Exception as e2:
            status = f"  -> FAIL: {e2}"
    print(f"  {repr(tok)}{status}  (in {len(files_using)} files)")
