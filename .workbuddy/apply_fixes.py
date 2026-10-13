# Comprehensive mojibake fixer v2.
# The mojibake was caused by UTF-8 text being misread as GBK/CP936, then re-saved as UTF-8.
# To reverse: encode the mojibake chars as GBK to recover original UTF-8 bytes, then decode as UTF-8.
# Complication: some bytes were unrecoverable and became '?' (0x3F) or PUA chars.
# Those are handled by explicit manual mappings.
import os, glob, re

files = sorted(glob.glob(r'c:\Users\loulanRE\OneDrive\Desktop\blog\source-en\_posts\*.md'))

# Chars that are legitimate (not mojibake) and should pass through unchanged
EXPECTED_CPS = set()
for cp in [0x2014, 0x2013, 0x2018, 0x2019, 0x201C, 0x201D, 0x2026, 0x00B7, 0x2022,
           0x00B0, 0x00A9, 0x00AE, 0x2122, 0x00D7, 0x00F7, 0x2192, 0x2190, 0x2194,
           0x20AC, 0x00A3, 0x00A5, 0x00A7, 0x00B6, 0x2020, 0x2021, 0x2030, 0x2116, 0x203B,
           0x00E1, 0x00E0, 0x00E9, 0x00E8, 0x00ED, 0x00EC, 0x00F3, 0x00F2, 0x00FA, 0x00F9,
           0x00FC, 0x00F1, 0x00E7, 0x00DF, 0x00C1, 0x00C9, 0x00CD, 0x00D3, 0x00DA, 0x00DC,
           0x01CE, 0x01D4, 0x014D, 0x012B, 0x0101, 0x016B, 0x011B, 0x01D0, 0x01D2, 0x016B]:
    EXPECTED_CPS.add(cp)
# Also allow emoji we're adding (0x1F000+)
# And Japanese kana/kanji that are legitimate (we add them via MANUAL replacements)

# Manual replacements for sequences with ? or PUA chars (can't be auto-decoded)
# Format: (old_string, new_string)
MANUAL = [
    # em-dash (most common): U+9225 U+003F -> em-dash
    ('\u9225?', '\u2014'),
    # greater-equal: U+922E U+003F -> >=
    ('\u922E?', '\u2265'),
    # en-dash in Northeast-Southwest title: U+9225 U+63DD -> en-dash + S
    ('\u9225\u63dd', '\u2013S'),
    # 7-10 time range (the "1" was consumed by mojibake)
    ('7\u9225?0', '7\u201310'),
    
    # Old-Friend: Japanese username ぎ さん
    ('\u9287?\u9287\u66d8\u5031', '\u304e \u3055\u3093'),
    # Old-Friend: 文科 with PUA U+E756
    ('\u93c2\u56e9\ue756', '\u6587\u79d1'),
    # Old-Friend: 理科 with PUA U+E756
    ('\u941e\u55d9\ue756', '\u7406\u79d1'),
    # Old-Friend: 班主任 with PUA U+E15D
    ('\u941d\ue15d\u5bcc\u6d60?', '\u73ed\u4e3b\u4efb'),
    # Old-Friend: 早恋 (has Box Drawing char U+2562 breaking detection)
    ('\u93c3\u2562\u4eb1', '\u65e9\u604b'),
    
    # Group-Project: 晚自习 (U+93C5 U+6C33 U+569C U+6D94 U+003F)
    ('\u93c5\u6c33\u569c\u6d94?', '\u665a\u81ea\u4e60'),
    # Group-Project: 牛马 (U+9417 U+6DA2 U+2C88?) - need to check. From report: 鐗涢┈
    # Actually 鐗涢┈ = U+9417 U+6DA2 U+2C88. But U+2C88 might not be right. Let me use the string.
    ('\u9417\u6da2\u2c88', '\u725b\u9a6c'),
    # Group-Project: 赎罪券 (璧庣姜鍒? = has ?)
    ('\u74a7\u5e37\u59ff\u5212?', '\u8d4e\u7f6a\u5238'),
    # Group-Project: 学习通 (瀛︿範閫? = has ?)
    ('\u5b66\u4e0d\u8303\u9020?', '\u5b66\u4e60\u901a'),
    # Group-Project: 躺尸 (韬哄案)
    ('\u9785\u54c4\u6848', '\u8eba\u5c38'),
    # Group-Project: 红温 (绾㈡俯)
    ('\u7ea0\u3012\u4fef', '\u7ea2\u6e29'),
    
    # Magic-Attack: 辅导员 - full mojibake is 杈呭 + PUA + 鍛 + ?
    # 杈呭 = U+6776 U+5450, PUA = U+E1F1, 鍛 = U+935B, ? = U+003F
    ('\u6776\u5450\ue1f1\u935b?', '\u8f85\u5bfc\u5458'),
    # Magic-Attack: pinyin fǔdǎo (mojibake'd to f菙d菐o)
    # 菙 = U+83D9, 菐 = U+83D0
    ('f\u83d9d\u83d0o', 'f\u01d4d\u01ceo'),
    # Magic-Attack: pinyin yuán (mojibake'd to yu谩n) - 谩 = U+8C29
    ('yu\u8c29n', 'yu\u00e1n'),
    
    # Moon-at-Astronomy: 翘课 with PUA U+E1F3
    # 缈樿 = U+7F08 U+6A3F, PUA = U+E1F3
    ('\u7f08\u6a3f\ue1f3', '\u7fc7\u8bfe'),
    
    # Fandom-Victory: 届到了 (灞婂埌浜?)
    ('\u6d9e\u5a42\u57cc\u6d5c?', '\u5c4a\u5230\u4e86'),
    # Fandom-Victory: 届いた (灞娿亜銇?)
    ('\u6d9e\u5a61\u4e9c\u9287?', '\u5c4a\u3044\u305f'),
    # Fandom-Victory: 认知厨 (璁ょ煡鍘?)
    ('\u7479\u946f\u9508?', '\u8ba4\u77e5\u53a8'),
    # Fandom-Victory: 厨 alone - 鍘? (from Japanese 鍘? meaning obsessive fan)
    ('\u9508? (from Japanese \u9508? meaning', '\u53a8 (from Japanese \u53a8 meaning'),
    
    # Fever-Dream: 夺舍 (澶鸿垗)
    ('\u5927\u9e3f\u57b4', '\u593a\u820d'),
    
    # Gin-and-1984: 国庆 (decoded)
    ('\u9365\u85c9\u7c21', '\u56fd\u5e86'),
    
    # Green-Train: 哐当哐当 (decoded)
    ('\u935d\u612c\u7d8b\u935d\u612c\u7d8b', '\u54d0\u5f53\u54d0\u5f53'),
    
    # Hunger-for-Victory: 三冠 (涓夊啝)
    ('\u6d93\u590a\u555d', '\u4e09\u51a0'),
    
    # MyGO-Sequel: 假药 (decoded)
    ('\u934b\u56ea\u5d42', '\u5047\u836f'),
    
    # Never-Follow: 我们三个 (decoded)
    ('\u93b4\u621c\u6ed1\u6d93\u5909\u91dc', '\u6211\u4eec\u4e09\u4e2a'),
    # Never-Follow: 未遂 with PUA U+E048 (鏈\ue048亗)
    ('\u93c8\ue048\u4e97', '\u672a\u9042'),
    
    # Northeast-Southwest: 胜利会师 (decoded)
    ('\u9473\u6ec3\u57c4\u6d7c\u6c2c\u7b00', '\u80dc\u5229\u4f1a\u5e08'),
    # Northeast-Southwest: Saizeriya サイゼリヤ (钀ㄨ帀浜?)
    ('\u9480\u8c8a\u6d52?', '\u30b5\u30a4\u30bc\u30ea\u30e4'),
    # Northeast-Southwest: 轻小说 (杞诲皬璇?)
    ('\u675e\u8f7b\u5c0f\u748f?', '\u8f7b\u5c0f\u8bf4'),
    
    # Ocean-Painting: 大爷 (澶х埛)
    ('\u5927\u7383\u579b', '\u5927\u7237'),
    # Ocean-Painting: 五一调休 (浜斾竴璋冧紤)
    ('\u6d93\u65b9\u4e00\u7490\u5192\u7d9d', '\u4e94\u4e00\u8c03\u4f11'),
    # Ocean-Painting: Song dynasty poem (complex with PUA chars)
    # Correct: 何夜无月？何处无竹柏？但少闲人如吾两人者耳。
    ('\u4f55\u591c\ue641\u65e0\u6708\uff1f\u4f55\u5904\u65e0\u7af9\u67cf\uff1f\u4f46\u5c11\u95f2\u4eba\u5982\u543e\ue6e7\u4e24\u4eba\u8005\u8033\u3002?',
     '\u4f55\u591c\u65e0\u6708\uff1f\u4f55\u5904\u65e0\u7af9\u67cf\uff1f\u4f46\u5c11\u95f2\u4eba\u5982\u543e\u4e24\u4eba\u8005\u8033\u3002'),
    # Ocean-Painting: 记承天寺夜游 with PUA U+E1EF
    ('\u8bb0\u627f\u5929\ue1ef\u591c\u6e38', '\u8bb0\u627f\u5929\u5bfa\u591c\u6e38'),
    # Ocean-Painting: 体测 (浣撴祴)
    ('\u4f53\u6292\u79b4', '\u4f53\u6d4b'),
    
    # Sunlight-Deprivation: 勒就是雾都重庆 with PUA U+E21E
    ('\u9355\u6391\u6c28\u93c4\ue21e\u6d58\u95ae\u4ecb\u5678\u6434?', '\u52d2\u5c31\u662f\u96fe\u90fd\u91cd\u5e86'),
    # Sunlight-Deprivation: 勒 (鍕?) - context: "鍕? (l膿)"
    ('\u9355? (l\u8128)', '\u52d2 (l\u0113)'),
    # Sunlight-Deprivation: 阳菜/晴女 (闃宠彍/鏅村コ)
    ('\u9603\u5ba0\u83dc/\u93c5\u6751\u30b3', '\u9633\u83dc/\u6674\u5973'),
    # Sunlight-Deprivation: 天野阳菜 (澶╅噹闄借彍) - different mojibake than 阳菜
    ('\u5929\u91ce\u9633\u83dc', '\u5929\u91ce\u9633\u83dc'),  # already correct if decoded
    # Sunlight-Deprivation: 天気之子 with PUA U+E1BC
    ('\u5929\u6c14\ue1bc\u5b50', '\u5929\u6c17\u4e4b\u5b50'),
    # Sunlight-Deprivation: 晴女 alone (鏅村コ)
    ('\u93c5\u6751\u30b3', '\u6674\u5973'),
    # Sunlight-Deprivation: 阳莱 (闃宠幈)
    ('\u9603\u5ba0\u5e48', '\u9633\u83b1'),
    # Sunlight-Deprivation: 寄吧 (涓堣偛)
    ('\u6d93\u5802\u5076', '\u5bc4\u5427'),
    # Sunlight-Deprivation: 文盲 (decoded)
    ('\u93c2\u56e9\u6d38', '\u6587\u76f2'),
    # Sunlight-Deprivation: emoji 😡🤜 (馃槨馃\ue641)
    ('\u9983\u69e8\u9983\ue641', '\U0001F621\U0001F91C'),
    
    # What-Can-Love-Still-Do: 愛にできることはまだあるかい (full Japanese)
    ('\u93b0\u6d96\u4f00\u9287\u3059\u4ebf\u9288\u5b28\u4ebf\u9287\u306b\u4f00\u9287\u4ff1\u4ee9\u9287\u5098\u5020\u9287\u5b28\u4e9c',
     '\u611b\u306b\u3067\u304d\u308b\u3053\u3068\u306f\u307e\u3060\u3042\u308b\u304b\u3044'),
    # What-Can-Love-Still-Do: 天気之子 with PUA (same as Sunlight)
    # already handled above
    
    # Dark-and-Darker: 葬送のフリーレン (钁\ue104併伄銉曘儶銉笺儸銉?)
    ('\u9481\ue104\u4f75\u4f84\u9289\u66d8\u5136\u9289\u7b3a\u5138\u9289?',
     '\u846c\u9001\u306e\u30d5\u30ea\u30fc\u30ec\u30f3'),
    # Dark-and-Darker: ダンジョン飯 (銉€銉炽偢銉с兂椋?)
    ('\u9289\u20ac\u9289\u70bd\u5062\u9289\u3059\u5152\u690b?',
     '\u30c0\u30f3\u30b8\u30e7\u30f3\u98ef'),
    
    # AI-Parallel-Dev: emojis
    ('\u9983\u5bea', '\U0001F310'),  # 🌐
    ('\u9983\u67bc\u9514?', '\U0001F5A5\uFE0F'),  # 🖥️
    ('\u9983\ue63b', '\U0001F916'),  # 🤖
    
    # Code-Display: emojis
    ('\u9983\u6451', '\U0001F4DD'),  # 📝
    ('\u9983\u6561', '\U0001F527'),  # 🔧
    ('\u9983\u6095', '\U0001F40D'),  # 🐍
    ('\u9983\u645d', '\U0001F4E6'),  # 📦
    ('\u9983\u6438', '\U0001F4CE'),  # 📎
    ('\u9983\u6443', '\U0001F4D5'),  # 📕
    
    # Comments header emoji (all files)
    ('\u9983\u6330', '\U0001F4AC'),  # 💬
]

def try_decode_run(run):
    """Try to decode a mojibake run by reversing UTF-8->GBK misread."""
    clean = run.rstrip('?')
    if not clean:
        return None
    try:
        gbk_bytes = clean.encode('gb18030')
        decoded = gbk_bytes.decode('utf-8')
        # Verify the decoded text doesn't contain mojibake-range chars
        for c in decoded:
            cp = ord(c)
            if 0x9200 <= cp <= 0x95FF:
                return None  # still mojibake
        return decoded
    except:
        return None

def is_expected(ch):
    cp = ord(ch)
    if cp in EXPECTED_CPS:
        return True
    if cp < 0x80:  # ASCII
        return True
    if 0x1F000 <= cp <= 0x1FFFF:  # emoji
        return True
    if 0x3000 <= cp <= 0x303F:  # CJK punctuation
        return True
    if 0xFF00 <= cp <= 0xFFEF:  # fullwidth forms
        return True
    return False

changes_log = []
total_fixed = 0
for f in files:
    with open(f, 'r', encoding='utf-8') as fh:
        text = fh.read()
    original = text
    
    # Apply manual replacements first (longest first)
    for old, new in sorted(MANUAL, key=lambda x: -len(x[0])):
        text = text.replace(old, new)
    
    # Now try auto-decode for remaining non-ASCII runs
    result = []
    i = 0
    while i < len(text):
        ch = text[i]
        cp = ord(ch)
        if cp > 0x7F and not is_expected(ch):
            # Collect run of non-expected non-ASCII chars (+ trailing ?)
            j = i
            while j < len(text):
                cj = text[j]
                cpj = ord(cj)
                if cpj > 0x7F and not is_expected(cj):
                    j += 1
                elif cj == '?' and j > i and ord(text[j-1]) > 0x7F:
                    j += 1
                else:
                    break
            run = text[i:j]
            decoded = try_decode_run(run)
            if decoded is not None:
                result.append(decoded)
            else:
                result.append(run)  # keep as-is for manual fix
            i = j
        else:
            result.append(ch)
            i += 1
    text = ''.join(result)
    
    if text != original:
        total_fixed += 1
        import difflib
        changes = []
        for line in difflib.unified_diff(original.splitlines(), text.splitlines(), lineterm='', n=0):
            if line.startswith('+++') or line.startswith('---') or line.startswith('@@'):
                continue
            changes.append(line)
        changes_log.append(f'=== {os.path.basename(f)} === ({len(changes)} diff lines)')
        for c in changes:
            changes_log.append(f'  {c}')
        changes_log.append('')
        with open(f, 'w', encoding='utf-8') as fh:
            fh.write(text)

with open(r'c:\Users\loulanRE\OneDrive\Desktop\blog\.workbuddy\fix_log.txt', 'w', encoding='utf-8') as fh:
    fh.write('\n'.join(changes_log))
print(f'Fixed {total_fixed} files. Log: {len(changes_log)} lines.')
