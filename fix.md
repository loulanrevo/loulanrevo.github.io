

```markdown
Role: Senior Front-End and DevOps Engineer
Task: Configure my existing Hexo (Butterfly theme) blog to support bilingual (Chinese/English) output with automatic browser-language redirection.

We will use the "hexo-multiple-language-generate" plugin to split the configuration and content, enabling Chinese under "/" and English under "/en/".

Please execute the following steps precisely:

---

### Step 1: Install the Plugin
Run this command in the Hexo project root directory:
`npm install hexo-multiple-language-generate --save`

---

### Step 2: Set up Content Directories (Source Files)
1. Rename the existing `source/` folder to `source-zh/` (this will contain your Chinese posts and pages).
2. Create a new directory named `source-en/`.
3. Inside `source-en/`, create a subdirectory `source-en/_posts/` (this is where English markdown posts will reside).
4. If there are other custom pages (e.g., `about/index.md`, `tags/index.md`) in `source-zh/`, duplicate their folder structure into `source-en/` and modify their front-matter if needed.

---

### Step 3: Create the Plugin Configuration File
Create a new file named `hexo-multiple-language.yml` in the project root directory, and populate it with the following configuration:

```yaml
# Hexo多语言站点配置
# 用于生成多语言版本的静态博客站点
hexo-multiple-language:
  # ===== 默认语言配置 =====
  default-language:
    # Hexo默认语言的生成目录，与config.zh.yml中的public_dir保持一致
    "generate-dir": "public"
    # 默认语言的完整配置文件列表
    # 插件会将这些文件复制为构建目录中的_config*.yml，不会与原始配置合并
    "config-file-name": [
      "config.zh",           # Hexo主配置文件
      "config.butterfly.zh"  # Butterfly主题配置文件
    ]
  # ===== 其他语言配置 =====
  other-language: [
    {
      "enable": true,                     # 是否启用该语言
      "generate-dir": "public-en",        # 当前语言的生成目录，需与config.en.yml中的public_dir保持一致
      "language-path": "en",              # 合并到默认语言输出目录下的子目录名
      "config-file-name": [
        "config.en",                      # 英文版Hexo主配置
        "config.butterfly.en"             # 英文版主题配置
      ]
    }
  ]
  # ===== 语言切换配置 =====
  # 基于浏览器语言自动切换或手动切换的相关配置
  switch-language:
    # 是否启用语言切换功能
    enable: true
    # 需要自动注入语言切换脚本的主题配置文件名前缀
    support-theme: "config.butterfly"
    # 手动切换语言后的有效期 (单位: 毫秒，如：86400000 毫秒代表1天)
    storage-ttl: 86400000
    # 当浏览器语言不匹配时使用的默认语言
    not-matched-use: 'zh'
    # 默认语言支持的语言代码列表
    default-language: [ "zh", "zh-CN", "zh-TW", "zh-HK" ]
    # 其他语言支持的语言代码映射
    other-language: {
      "en": ["en", "en-US", "en-GB"]
    }
```

---

### Step 4: Split Hexo Core Configuration Files
Note: The plugin does NOT merge configs. The files below must be COMPLETE Hexo configuration files (duplicate your original `_config.yml` first).

1. Create `config.zh.yml` (Complete copy of your current `_config.yml` with these modifications):
```yaml
url: https://yourusername.github.io  # Change to your actual site URL
root: /
source_dir: source-zh
public_dir: public
language: zh-CN
ignore:
  - source-en/
```

2. Create `config.en.yml` (Complete copy of your current `_config.yml` with these modifications):
```yaml
url: https://yourusername.github.io/en  # Change to your actual site URL /en
root: /en/
source_dir: source-en
public_dir: public-en
language: en
ignore:
  - source-zh/
```

---

### Step 5: Split Theme Configuration Files (Butterfly)
Note: Duplicate your original `_config.butterfly.yml` first.

1. Create `config.butterfly.zh.yml` (Complete copy of your theme config):
- Locate the `menu:` configuration section.
- Add a Language Switch button like this:
```yaml
menu:
  # ... your existing menu items ...
  语言||fas fa-language:
    English: en || fa-solid fa-language multiple-language-switch
    中文: zh || fa-solid fa-language multiple-language-switch
```

2. Create `config.butterfly.en.yml` (Complete copy of your theme config):
- Translate the menu keys into English (e.g., 首页 -> Home, 归档 -> Archives).
- Add the Language Switch button in English:
```yaml
menu:
  # ... your translated menu items ...
  Language||fas fa-language:
    English: en || fa-solid fa-language multiple-language-switch
    中文: zh || fa-solid fa-language multiple-language-switch
```

---

### Step 6: Update GitHub Actions / CI-CD Deployment Script (If applicable)
If there is a GitHub Actions workflow file in `.github/workflows/` (usually deploying on push):
- Find the step where Hexo generates pages (typically `npx hexo g` or `hexo generate`).
- Replace it with:
  `npx hexo multiple-language-generate`

If there is a custom package.json build script:
- Update `package.json` scripts if necessary.

---

### Step 7: Cleanup
Since `_config.yml` and `_config.butterfly.yml` are no longer needed by the builder (though keeping them as a local backup is fine), make sure to remove them from being parsed directly, as HMLG uses `config.*.yml` files instead.

Please verify the file structures and run local tests using:
`npx hexo multiple-language-generate && npx hexo s`
to confirm that both Chinese and English sites are rendered and redirecting correctly.
```

---

### 💡 提示与说明（供您参考）：

1. **备份原始配置**：在执行前，建议将您现有的 `_config.yml`、`_config.butterfly.yml` 以及整个 `source/` 目录复制一个备份到项目外部。
2. **翻译文章**：配置完成后，中文文章会继续留在 `source-zh/_posts`；当您想为某篇文章撰写英文版时，只需在 `source-en/_posts` 下新建一个同名的 Markdown 文件（或者不同的名字，保持 Front-Matter 合理即可），用英文书写即可。
3. **测试跳转**：本地启动预览后（`hexo s`），如果您使用中文版浏览器访问 `localhost:4000`，会停留在中文版；如果您将浏览器首选语言临时调整为英文（或者使用无痕模式且系统/浏览器首选语言为英文），它就会自动跳转至 `localhost:4000/en/`。