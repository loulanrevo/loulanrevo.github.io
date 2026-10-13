# Fix remaining mojibake in 6 English files.
# Uses exact codepoint sequences verified from codepoint dump.
import os

BASE = r'c:\Users\loulanRE\OneDrive\Desktop\blog\source-en\_posts'

# (filename, old_string, new_string, description)
FIXES = [
    # Dark-and-Darker: 葬送のフリーレン (Frieren)
    # Exact codepoints: U+9481 U+E104 U+20AC U+4F75 U+4F04 U+9289 U+66D8 U+5136 U+9289 U+7B3A U+5138 U+9289 U+003F
    ('Dark-and-Darker-Three-Day-Binge.md',
     '\u9481\ue104\u20ac\u4f75\u4f04\u9289\u66d8\u5136\u9289\u7b3a\u5138\u9289\u003f',
     '\u846c\u9001\u306e\u30d5\u30ea\u30fc\u30ec\u30f3',
     '葬送のフリーレン'),

    # Dark-and-Darker: ダンジョン飯 (Delicious in Dungeon)
    # Exact codepoints: U+9289 U+20AC U+9289 U+70BD U+5062 U+9289 U+0441 U+5142 U+690B U+003F
    ('Dark-and-Darker-Three-Day-Binge.md',
     '\u9289\u20ac\u9289\u70bd\u5062\u9289\u0441\u5142\u690b\u003f',
     '\u30c0\u30f3\u30b8\u30e7\u30f3\u98ef',
     'ダンジョン飯'),

    # Fandom-Victory: 届到了 (todoketa)
    # 灞(U+705E) 婂(U+5A42) 埌(U+57CC) 浜(U+6D5C) ?(U+003F)
    ('Fandom-Victory.md',
     '\u705e\u5a42\u57cc\u6d5c\u003f',
     '\u5c4a\u5230\u4e86',
     '届到了'),

    # Fandom-Victory: 届いた (todokita, Japanese)
    # Exact codepoints: U+705E U+5A3F U+4E9C U+9287 U+003F
    ('Fandom-Victory.md',
     '\u705e\u5a3f\u4e9c\u9287\u003f',
     '\u5c4a\u3044\u305f',
     '届いた'),

    # Fandom-Victory: 认知厨 (rènzhī chú)
    # Exact codepoints: U+7481 U+3087 U+7161 U+9358 U+003F
    ('Fandom-Victory.md',
     '\u7481\u3087\u7161\u9358\u003f',
     '\u8ba4\u77e5\u53a8',
     '认知厨'),

    # Fandom-Victory: standalone 厨 (鍘?)
    # Must come AFTER 认知厨 replacement to avoid partial match
    # Context: "鍘? (from Japanese 鍘? meaning
    ('Fandom-Victory.md',
     '\u9358\u003f (from Japanese \u9358\u003f meaning',
     '\u53a8 (from Japanese \u53a8 meaning',
     '厨 (standalone, both instances in one string)'),

    # Group-Project: 赎罪券 (indulgences)
    # Exact codepoints: U+74A7 U+5EA3 U+59DC U+9352 U+003F
    ('Group-Project-Agony.md',
     '\u74a7\u5ea3\u59dc\u9352\u003f',
     '\u8d4e\u7f6a\u5238',
     '赎罪券'),

    # Group-Project: 学习通 (xuexitong)
    # Exact codepoints: U+701B U+FE3F U+7BC4 U+95AB U+003F
    ('Group-Project-Agony.md',
     '\u701b\ufe3f\u7bc4\u95ab\u003f',
     '\u5b66\u4e60\u901a',
     '学习通'),

    # Magic-Attack: 辅导员 (counselor)
    # Exact codepoints: U+6748 U+546D U+E1F1 U+935B U+003F
    ('Magic-Attack-vs-Counselor.md',
     '\u6748\u546d\ue1f1\u935b\u003f',
     '\u8f85\u5bfc\u5458',
     '辅导员'),

    # Northeast-Southwest: サイゼリヤ (Saizeriya)
    # Exact codepoints: U+9480 U+3128 U+5E00 U+6D5C U+003F
    ('Northeast-Southwest-Victorious-Reunion.md',
     '\u9480\u3128\u5e00\u6d5c\u003f',
     '\u30b5\u30a4\u30bc\u30ea\u30e4',
     'サイゼリヤ'),

    # Northeast-Southwest: 轻小说 (light novel)
    # 杞(U+675E) 诲(U+8BEA) 皬(U+76AC) 璇(U+7487) ?(U+003F)
    ('Northeast-Southwest-Victorious-Reunion.md',
     '\u675e\u8bf2\u76ac\u7487\u003f',
     '\u8f7b\u5c0f\u8bf4',
     '轻小说'),

    # Ocean-Painting: Su Shi poem
    # Full mojibake from codepoint dump [4018:4053]
    ('Ocean-Painting-and-Seaside-Trip.md',
     '\u6d63\u66de\ue641\u93c3\u72b3\u6e40\u951b\u71b6\u7d8d\u6fb6\u52ec\u68e4\u7ed4\u89c4\u7146\u951b\u71b6\u7d7e\u704f\u6226\u68fd\u6d5c\u54c4\ue6e7\u935a\u53e5\u88b1\u6d5c\u9e3f\u20ac\u5470\u20ac\u70bd\u20ac\u003f',
     '\u4f55\u591c\u65e0\u6708\uff1f\u4f55\u5904\u65e0\u7af9\u67cf\uff1f\u4f46\u5c11\u95f2\u4eba\u5982\u543e\u4e24\u4eba\u8005\u8033\u3002',
     '何夜无月？何处无竹柏？但少闲人如吾两人者耳。'),
]

total_fixed = 0
for fname, old, new, desc in FIXES:
    fpath = os.path.join(BASE, fname)
    with open(fpath, 'r', encoding='utf-8') as fh:
        text = fh.read()
    if old in text:
        count = text.count(old)
        text = text.replace(old, new)
        with open(fpath, 'w', encoding='utf-8') as fh:
            fh.write(text)
        print(f'  FIXED [{fname}]: {desc} ({count} occurrence(s))')
        total_fixed += 1
    else:
        print(f'  SKIP  [{fname}]: {desc} - pattern not found!')

print(f'\nTotal: {total_fixed}/{len(FIXES)} fixes applied.')
