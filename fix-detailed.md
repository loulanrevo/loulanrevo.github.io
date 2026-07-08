# Hexo 博客双语化（中/英）细粒度执行手册

> **适用对象**: 已有 Hexo + Butterfly 纯中文博客，需添加英文支持
> **目标站点**: `https://loulanrevo.github.io`（中文 `/`，英文 `/en/`）
> **核心插件**: `hexo-multiple-language-generate`
> **总检查项**: 约 130 项，逐项打勾推进
> **预计耗时**: 首次执行约 2-3 小时（含验证）

---

## 阅读指南

每步骤包含以下要素：

| 要素 | 含义 |
|------|------|
| ⚠️ **PITFALL** | 已知陷阱，执行前必读 |
| 📋 **Pre-check** | 执行前必须满足的条件 |
| ▶️ **Execute** | 执行命令或操作 |
| 📤 **Expected** | 预期输出/结果 |
| ✅ **Verify** | 验证方法 |
| 🔙 **Rollback** | 如果出错如何回滚 |

标记说明：
- `[ ]` = 待执行
- `[x]` = 已完成

---

## Phase 0: 环境审计与前置检查

> 目的：确认项目环境正确，避免半途因版本/路径问题中断。

---

### 0.1 定位 Hexo 项目根目录

⚠️ **PITFALL**: 你必须在 Hexo **源代码项目**根目录执行本手册（包含 `_config.yml`、`package.json`、`source/`），**不是**编译后的 `public/` 目录。如果不确定，请先找到包含 `_config.yml` 和 `node_modules/` 的目录。

#### 📋 Pre-check
- [ ] 你知道 Hexo 源代码项目在哪台电脑的哪个路径

#### ▶️ Execute
```bash
# 确认当前目录是 Hexo 源码根目录
pwd
ls _config.yml _config.butterfly.yml package.json source/
```
期望看到三个文件和一个目录都存在。

#### ✅ Verify
- [ ] `_config.yml` 存在
- [ ] `_config.butterfly.yml` 存在
- [ ] `package.json` 存在
- [ ] `source/` 目录存在
- [ ] `node_modules/` 目录存在

#### 🔙 Rollback
如果 `node_modules/` 不存在，说明依赖未安装，执行：
```bash
npm install
```

---

### 0.2 Node.js 与 npm 版本检查

⚠️ **PITFALL**: `hexo-multiple-language-generate` 要求 Node.js >= 14.17.0。版本不足会导致安装失败或运行时错误。

#### ▶️ Execute
```bash
node -v   # 期望 >= v14.17.0
npm -v    # 记录版本号
```

#### ✅ Verify
- [ ] Node.js 版本 >= 14.17.0（如 `v18.20.0`、`v20.11.0`）
- [ ] npm 版本已知（记录在旁：`____`）

#### 🔙 Rollback
如果版本不足，使用 nvm 切换：
```bash
nvm ls                    # 查看已安装版本
nvm install 18            # 安装 Node 18 LTS
nvm use 18                # 切换
```

---

### 0.3 Git 状态检查

⚠️ **PITFALL**: 脏工作区（未提交修改）会让后续回滚不可靠。必须先清理。

#### ▶️ Execute
```bash
git status
git remote -v
```

#### ✅ Verify
- [ ] 工作区干净（`nothing to commit, working tree clean`）
- [ ] 远程仓库已知（应为 `https://github.com/loulanrevo/loulanrevo.github.io.git`）
- [ ] 如果工作区不干净 → 先 `git add -A && git commit -m "chore: pre-bilingual snapshot"` 或 `git stash`

---

### 0.4 识别现有自定义内容（关键审计）

⚠️ **PITFALL**: 自定义 injector 脚本和 `skip_render` 规则在拆分后可能路径失效。必须提前记录。

#### ▶️ Execute
```bash
# 列出 source/ 下所有非 _posts 目录
ls -d source/*/ 2>/dev/null | grep -v _posts

# 检查 skip_render 规则
grep -A 5 "skip_render" _config.yml

# 列出已安装的 Hexo 插件
npm list --depth=0 2>/dev/null | grep hexo

# 检查自定义 scripts 目录
ls scripts/ 2>/dev/null

# 检查主题覆盖文件
ls -R themes/butterfly/ 2>/dev/null | head -50
```

#### ✅ Verify
- [ ] 记录了 `source/` 下所有自定义目录（如 `about/`、`links/`）: `_______________`
- [ ] 记录了 `skip_render` 规则（如果有）: `_______________`
- [ ] 记录了已有插件列表
- [ ] 记录了自定义 scripts（如果有）

---

### 0.5 记录现有配置快照

⚠️ **PITFALL**: 拆分配置时这是唯一参考。漏记一项就会丢失一项。

#### ▶️ Execute
```bash
# 记录关键配置字段
grep -E "^(url|root|language|theme|source_dir|public_dir|permalink|timezone|deploy)" _config.yml
grep -A 3 "^deploy:" _config.yml
```

#### ✅ Verify
- [ ] 填写下表（从 `_config.yml` 实际值填入）：

| 字段 | 当前值 |
|------|--------|
| `url` | _______________ |
| `root` | _______________ |
| `language` | _______________ |
| `theme` | _______________ |
| `source_dir` | _______________ |
| `public_dir` | _______________ |
| `permalink` | _______________ |
| `deploy.type` | _______________ |
| `deploy.repo` | _______________ |
| `deploy.branch` | _______________ |

---

## Phase 1: 全量备份与安全网

> 目的：在修改任何文件之前建立完整的安全网，确保任何步骤都可以回滚。

---

### 1.1 Git 备份分支

#### ▶️ Execute
```bash
git checkout -b backup/before-multilang
git push origin backup/before-multilang  # 推送到远程（如有）
```

#### ✅ Verify
- [ ] 分支创建成功（`git branch | grep backup` 可见）
- [ ] 推送成功（如有远程）

#### 🔙 Rollback
任何时候都可以：
```bash
git checkout backup/before-multilang
```
恢复到修改前的完整状态。

---

### 1.2 文件级冷备份

⚠️ **PITFALL**: Git 备份不够，文件级冷备份是最后的救命稻草。备份到项目**外部**。

#### ▶️ Execute
```bash
# 创建备份目录（替换日期为今天）
BACKUP_DIR=~/hexo-backup-$(date +%Y%m%d)
mkdir -p "$BACKUP_DIR"

# 复制关键文件
cp _config.yml "$BACKUP_DIR/"
cp _config.butterfly.yml "$BACKUP_DIR/"
cp -r source/ "$BACKUP_DIR/"
cp package.json "$BACKUP_DIR/"
cp package-lock.json "$BACKUP_DIR/" 2>/dev/null

# 备份 CI/CD 配置
cp -r .github/ "$BACKUP_DIR/" 2>/dev/null

# 备份 scripts 目录
cp -r scripts/ "$BACKUP_DIR/" 2>/dev/null

echo "备份完成: $BACKUP_DIR"
```

#### ✅ Verify
- [ ] 备份目录创建成功: `ls "$BACKUP_DIR"`
- [ ] 文件数一致: `ls source/_posts/*.md | wc -l` vs `ls "$BACKUP_DIR"/source/_posts/*.md | wc -l`
- [ ] 内容一致: `diff _config.yml "$BACKUP_DIR"/_config.yml` 无差异

#### 🔙 Rollback
如需从冷备份完全恢复：
```bash
cp "$BACKUP_DIR"/_config.yml .
cp "$BACKUP_DIR"/_config.butterfly.yml .
cp -r "$BACKUP_DIR"/source/ .
cp "$BACKUP_DIR"/package.json .
```

---

### 1.3 回滚脚本骨架

#### ▶️ Execute
在备份目录创建 `rollback.sh`（仅注释说明，不直接执行）：
```bash
cat > ~/hexo-backup-$(date +%Y%m%d)/rollback.sh << 'EOF'
#!/bin/bash
# 回滚脚本 — 仅作参考，手动逐条执行
echo "=== 回滚到双语化前状态 ==="
echo "1. git checkout backup/before-multilang"
echo "2. 或从本目录手动复制文件回去"
echo "3. 具体步骤见 fix-detailed.md 附录 B"
EOF
```

#### ✅ Verify
- [ ] `rollback.sh` 已创建

---

## Phase 2: 安装 hexo-multiple-language-generate 插件

> 目的：安装双语构建核心依赖。

---

### 2.1 安装前检查

#### 📋 Pre-check
- [ ] 当前在 Hexo 项目根目录
- [ ] `node_modules/` 存在
- [ ] 已完成 Phase 1 备份

#### ▶️ Execute
```bash
# 记录安装前状态
npm list hexo-multiple-language-generate 2>/dev/null
# 应该输出 "(empty)" 或报错
```

#### ✅ Verify
- [ ] 插件尚未安装（否则需要先确认版本兼容性）

---

### 2.2 执行安装

⚠️ **PITFALL**: 如果安装报 peer dependency 错误，添加 `--legacy-peer-deps` 标志。

#### ▶️ Execute
```bash
npm install hexo-multiple-language-generate --save
```

#### 📤 Expected
```
+ hexo-multiple-language-generate@x.x.x
added N packages in Xs
```

#### ✅ Verify
- [ ] `grep "hexo-multiple-language-generate" package.json` 返回结果
- [ ] `ls node_modules/hexo-multiple-language-generate/` 目录存在
- [ ] `package-lock.json` 已更新（`git diff package-lock.json` 有变化）

#### 🔙 Rollback
```bash
npm uninstall hexo-multiple-language-generate
```

---

### 2.3 验证插件版本

#### ▶️ Execute
```bash
# 记录版本号
npm list hexo-multiple-language-generate
```

#### ✅ Verify
- [ ] 版本号已记录: `v________`
- [ ] 访问 [插件 GitHub](https://github.com/NextZeus/hexo-multiple-language-generate) 确认当前版本无 known issue

---

## Phase 3: 内容目录重构

> 目的：将单一 `source/` 拆分为中文 `source-zh/` 和英文 `source-en/`。

---

### 3.1 重命名中文源目录

⚠️ **PITFALL**: 确保 `source-zh/` 尚不存在，否则会被覆盖。

#### 📋 Pre-check
- [ ] `source/` 目录存在且非空
- [ ] `source-zh/` 目录不存在

#### ▶️ Execute
```bash
# 方案 A：普通 mv（非 git 仓库项目直接用）
mv source/ source-zh/

# 方案 B：git mv（在 git 仓库内推荐，保留版本历史）
# git mv source/ source-zh/
```

#### 📤 Expected
`source/` 消失，`source-zh/` 出现，内容完全一致。

#### ✅ Verify
- [ ] `ls source-zh/_posts/` 能列出所有中文文章
- [ ] 文章数与备份一致（应该是 9 篇）: `ls source-zh/_posts/*.md | wc -l`

#### 🔙 Rollback
```bash
mv source-zh/ source/
```

---

### 3.2 创建英文源目录

#### ▶️ Execute
```bash
mkdir -p source-en/_posts
```

#### ✅ Verify
- [ ] `ls -d source-en/_posts/` 目录存在

---

### 3.3 静态资源共享策略

⚠️ **PITFALL**: 重复的静态资源（img/、css/、js/）会增加仓库大小。推荐策略：资源共享。

#### ▶️ Execute
```bash
# 检查 source-zh/ 下的静态资源目录
ls -d source-zh/*/ | grep -v _posts
```

#### ✅ Verify
- [ ] 决定策略（推荐 A）：
  - **策略 A（推荐）**: 仅保留在 `source-zh/`，英文站通过绝对 URL 引用
  - **策略 B**: 复制到 `source-en/`
- [ ] 如果选策略 B: `cp -r source-zh/img source-en/` 等

---

### 3.4 处理自定义页面

⚠️ **PITFALL**: `tags/` 和 `categories/` 是 Hexo 自动生成的页面，**不需要**手动复制。只需要复制手动创建的页面（如 `about/`、`links/`）。

#### ▶️ Execute
```bash
# 查看 source-zh/ 下的自定义页面目录（排除 _posts 和 _data）
ls -d source-zh/*/ 2>/dev/null | grep -v "_posts\|_data"
```

对于每个自定义页面（如 `about/`），在 `source-en/` 创建英文版本：
```bash
mkdir -p source-en/about
cat > source-en/about/index.md << 'EOF'
---
title: About
date: YYYY-MM-DD HH:MM:SS
type: about
lang: en
---
(English about page content)
EOF
```

#### ✅ Verify
- [ ] 自定义页面列表已记录: `_______________`
- [ ] 每个需要的页面在 `source-en/` 下都有对应英文版

---

## Phase 4: 拆分 Hexo 核心配置

> 目的：创建完整的中文和英文 Hexo 配置文件。

---

### 4.1 原则说明（执行前必读）

🚨 **CRITICAL**: `hexo-multiple-language-generate` **不会合并**配置文件。`config.zh.yml` 和 `config.en.yml` 必须是**完整的** Hexo 配置，不能只写差异字段。

🚨 如果只写 `url`、`root`、`source_dir` 三个字段，构建结果将丢失所有插件、主题、部署配置，变成默认 Landscape 主题的空白站点。

🚨 只修改以下标记为"需要修改"的字段，其余字段保持与原 `_config.yml` 完全一致。

---

### 4.2 创建中文核心配置 config.zh.yml

#### 📋 Pre-check
- [ ] 当前 `_config.yml` 内容完整
- [ ] 已备份 `_config.yml`

#### ▶️ Execute
```bash
# 复制原配置
cp _config.yml config.zh.yml
```

然后编辑 `config.zh.yml`，修改以下字段（**只改这些**）：

```yaml
# ===== 必须修改的字段 =====
url: https://loulanrevo.github.io
root: /
source_dir: source-zh
public_dir: public
language: zh-CN

# ===== 必须添加的字段 =====
ignore:
  - source-en/
```

> **注意**: 如果原 `_config.yml` 已有 `ignore` 字段，替换为上述值。如果没有，直接在文件末尾添加。

#### ✅ Verify
- [ ] `config.zh.yml` 文件存在
- [ ] 行数与 `_config.yml` 一致（除了 `ignore` 可能新增几行）
- [ ] `grep "source_dir" config.zh.yml` 输出 `source_dir: source-zh`
- [ ] `grep "ignore" config.zh.yml` 包含 `source-en/`
- [ ] `grep "url" config.zh.yml` 输出 `url: https://loulanrevo.github.io`
- [ ] YAML 语法正确（如果装了 Python: `python -c "import yaml; yaml.safe_load(open('config.zh.yml'))"` 不报错）

#### 🔙 Rollback
```bash
rm config.zh.yml
git checkout -- _config.yml
```

---

### 4.3 创建英文核心配置 config.en.yml

#### 📋 Pre-check
- [ ] `config.zh.yml` 创建成功

#### ▶️ Execute
```bash
# 复制中文配置（它已经是完整配置）
cp config.zh.yml config.en.yml
```

然后编辑 `config.en.yml`，修改以下字段：

```yaml
# ===== 必须修改的字段 =====
url: https://loulanrevo.github.io/en        # 注意末尾有 /en
root: /en/                                   # 注意前后都有 /
source_dir: source-en
public_dir: public-en
language: en

# ===== 可选修改的字段（建议改成英文） =====
title: loulanre                              # 英文标题
subtitle: The world forgets, but the Bone Pigeon won't
description: Thanks for being here
author: LouLanRE                             # 英文笔名

# ===== 必须修改 ignore =====
ignore:
  - source-zh/
```

> ⚠️ **PITFALL**: `url` 末尾不要加 `/`，但 `root` 必须以 `/` 开头和结尾。`url` 是 `https://loulanrevo.github.io/en`，`root` 是 `/en/`。

#### ✅ Verify
- [ ] `config.en.yml` 文件存在
- [ ] `grep "url" config.en.yml` 输出 `url: https://loulanrevo.github.io/en`
- [ ] `grep "root" config.en.yml` 输出 `root: /en/`
- [ ] `grep "source_dir" config.en.yml` 输出 `source_dir: source-en`
- [ ] `grep "language" config.en.yml` 输出 `language: en`
- [ ] 运行 `diff config.zh.yml config.en.yml` 审视差异，确认所有差异都有意为之

#### 🔙 Rollback
```bash
rm config.en.yml
```

---

### 4.4 原 _config.yml 处理

⚠️ **PITFALL**: 插件不使用 `_config.yml`，但保留它作为参考和回退很有价值。**建议保留而非删除**。

#### ▶️ Execute
在原 `_config.yml` **最顶部**添加注释：
```yaml
# ============================================================
# DEPRECATED: 此文件不再用于多语言构建
# 中文构建使用: config.zh.yml
# 英文构建使用: config.en.yml
# 此文件仅保留作为参考
# ============================================================
```

#### ✅ Verify
- [ ] 注释已添加在文件最顶部
- [ ] 原配置内容保持不变

---

## Phase 5: 拆分 Butterfly 主题配置

> 目的：创建中文和英文版本的主题配置，重点是菜单翻译和语言切换按钮。

---

### 5.1 创建中文主题配置 config.butterfly.zh.yml

#### 📋 Pre-check
- [ ] `_config.butterfly.yml` 内容完整
- [ ] 已备份 `_config.butterfly.yml`

#### ▶️ Execute
```bash
cp _config.butterfly.yml config.butterfly.zh.yml
```

编辑 `config.butterfly.zh.yml`，将 `menu:` 块修改为如下格式（保持你现有的菜单项，添加语言切换按钮）：

```yaml
menu:
  首页: / || fas fa-home
  归档: /archives/ || fas fa-archive
  标签: /tags/ || fas fa-tags
  分类: /categories/ || fas fa-folder-open
  # ===== 以下为新增的语言切换按钮 =====
  语言 || fas fa-language:
    English: en || fa-solid fa-language multiple-language-switch
    中文: zh || fa-solid fa-language multiple-language-switch
```

> ⚠️ **PITFALL**: `multiple-language-switch` 是**关键 CSS class**，插件通过它注入点击切换逻辑。拼写错误（如 `multiple-langauge-switch`）将导致切换按钮完全无效。

> ⚠️ **PITFALL**: 保持你原有的菜单项顺序和图标。上述模板仅供参考结构，你实际的菜单项可能和模板不完全一致。

#### ✅ Verify
- [ ] `config.butterfly.zh.yml` 文件存在
- [ ] `grep "multiple-language-switch" config.butterfly.zh.yml` 有 2 条结果
- [ ] 原有的菜单项都保留（通过对比 `_config.butterfly.yml` 的 menu 段）

#### 🔙 Rollback
```bash
rm config.butterfly.zh.yml
```

---

### 5.2 创建英文主题配置 config.butterfly.en.yml

#### 📋 Pre-check
- [ ] `config.butterfly.zh.yml` 创建成功

#### ▶️ Execute
```bash
cp config.butterfly.zh.yml config.butterfly.en.yml
```

编辑 `config.butterfly.en.yml`，**翻译菜单项为英文**，且**所有 URL 添加 `/en/` 前缀**：

```yaml
menu:
  Home: /en/ || fas fa-home
  Archives: /en/archives/ || fas fa-archive
  Tags: /en/tags/ || fas fa-tags
  Categories: /en/categories/ || fas fa-folder-open
  # ===== 语言切换按钮 =====
  Language || fas fa-language:
    中文: zh || fa-solid fa-language multiple-language-switch
    English: en || fa-solid fa-language multiple-language-switch
```

> 🚨 **CRITICAL**: 所有菜单 URL 必须以 `/en/` 为前缀。忘了加前缀会导致点击英文站菜单跳回中文站。

> ⚠️ 其他面向用户的文本也应翻译（如 `footer`、`copyright`、`subtitle` 等）。

对于 `footer` 和 `copyright` 相关字段，建议翻译：
```yaml
footer:
  owner:
    since: 2025
  copyright: "Copyright © 2025 - 2026 By LouLanRE"
```

#### ✅ Verify
- [ ] `config.butterfly.en.yml` 文件存在
- [ ] `grep "/en/" config.butterfly.en.yml` 确认所有菜单 URL 有 `/en/` 前缀
- [ ] `grep "multiple-language-switch" config.butterfly.en.yml` 有 2 条结果

#### 🔙 Rollback
```bash
rm config.butterfly.en.yml
```

---

### 5.3 两版主题配置一致性检查

⚠️ **PITFALL**: 功能性配置（非文本）不一致会导致中英文站视觉效果不同。

#### ▶️ Execute
```bash
# 对比关键功能配置项
echo "=== darkmode ==="; grep -A 3 "darkmode" config.butterfly.zh.yml | head -5; echo "---"; grep -A 3 "darkmode" config.butterfly.en.yml | head -5
echo "=== highlight ==="; grep "highlight" config.butterfly.zh.yml; grep "highlight" config.butterfly.en.yml
echo "=== social ==="; grep -A 20 "^social:" config.butterfly.zh.yml | head -20; echo "---"; grep -A 20 "^social:" config.butterfly.en.yml | head -20
```

#### ✅ Verify
- [ ] Dark mode 配置一致
- [ ] 代码高亮配置一致
- [ ] 社交链接 URL 一致
- [ ] CDN 配置一致
- [ ] 自定义 CSS/JS 注入路径一致
- [ ] 只有语言相关字段（菜单文案、footer、copyright、标题描述）有差异

---

## Phase 6: 创建插件配置文件 hexo-multiple-language.yml

> 目的：告诉插件如何构建多语言站点。

---

### 6.1 创建配置文件

#### ▶️ Execute
在项目根目录创建 `hexo-multiple-language.yml`，内容如下：

```yaml
# Hexo 多语言站点配置
# 用于生成双语版本 (中文 / , 英文 /en/)
hexo-multiple-language:
  # ===== 默认语言（中文）配置 =====
  default-language:
    # 生成目录，必须与 config.zh.yml 中的 public_dir 一致
    "generate-dir": "public"
    # 配置文件列表（不含 .yml 后缀，插件自动追加）
    "config-file-name":
      - "config.zh"
      - "config.butterfly.zh"

  # ===== 其他语言（英文）配置 =====
  other-language:
    - "enable": true
      # 英文独立构建目录，必须与 config.en.yml 中的 public_dir 一致
      "generate-dir": "public-en"
      # 合并到默认语言输出目录下的子目录名
      "language-path": "en"
      "config-file-name":
        - "config.en"
        - "config.butterfly.en"

  # ===== 浏览器语言自动切换配置 =====
  switch-language:
    # 是否启用自动切换
    enable: true
    # 需要注入切换脚本的主题配置文件名前缀
    # "config.butterfly" 会匹配 config.butterfly.zh 和 config.butterfly.en
    support-theme: "config.butterfly"
    # 用户手动切换语言后的有效期（毫秒），1 天 = 86400000
    storage-ttl: 86400000
    # 浏览器语言不匹配任何已配置语言时的默认语言
    not-matched-use: "zh"
    # 默认语言（中文）匹配的浏览器语言代码
    default-language:
      - "zh"
      - "zh-CN"
      - "zh-TW"
      - "zh-HK"
    # 其他语言（英文）匹配的浏览器语言代码
    other-language:
      "en":
        - "en"
        - "en-US"
        - "en-GB"
```

#### ✅ Verify
- [ ] `hexo-multiple-language.yml` 文件存在
- [ ] `generate-dir` 与对应 config 文件中 `public_dir` 一致：
  - `"public"` ↔ `config.zh.yml` 中 `public_dir: public`
  - `"public-en"` ↔ `config.en.yml` 中 `public_dir: public-en`
- [ ] `language-path: "en"` 与 `config.en.yml` 中 `root: /en/` 对应
- [ ] `config-file-name` 不含 `.yml` 后缀（插件自动追加）
- [ ] `not-matched-use` 的值 (`zh`) 是 `other-language` 的一个 key
- [ ] YAML 语法正确

---

### 6.2 配置项交叉验证

⚠️ **PITFALL**: 配置文件中多处提到相同概念的值必须一致。逐一核对：

| 概念 | config.zh.yml | config.en.yml | hexo-multiple-language.yml | 一致? |
|------|:---:|:---:|:---:|:---:|
| 输出目录 | `public_dir: public` | `public_dir: public-en` | `generate-dir: "public"` + `"public-en"` | [ ] |
| 源目录 | `source_dir: source-zh` | `source_dir: source-en` | (无，由 config 决定) | [ ] |
| 语言 | `language: zh-CN` | `language: en` | `default-language: ["zh-CN",...]` + `other-language: "en":["en",...]` | [ ] |
| URL 根路径 | `root: /` | `root: /en/` | — | [ ] |
| 子目录名 | — | `root: /en/` | `language-path: "en"` | [ ] |

- [ ] 全部一致

---

## Phase 7: 内容翻译准备

> 目的：为英文内容制定策略和模板，不要求立即翻译所有文章。

---

### 7.1 制定翻译策略

#### ✅ Verify
- [ ] 决定翻译范围：全 9 篇 / 精选 ____ 篇 / 仅新增文章
- [ ] 决定翻译深度：全文翻译 / 摘要翻译 / 仅标题翻译
- [ ] 规划分类翻译对照表：

| 中文分类 | 英文分类 |
|----------|----------|
| 技术教程 | Technology |
| 生活随笔 | Life |
| 读书笔记 | Reading Notes |
| DevOps | DevOps |
| 工具使用 | Tools |
| 音乐 | Music |
| Daily-Rituals | Daily Rituals |

- [ ] 规划标签翻译对照表：

| 中文标签 | 英文标签 |
|----------|----------|
| 阅读 | reading |
| 翻译 | translation |
| 音乐 | music |
| 教程 | tutorial |
| 数据科学 | data-science |
| 思政 | politics |
| AI | AI |
| IPO | IPO |
| 经济 | economics |
| 资本市场 | capital-markets |
| HIFI | HIFI |
| 工具 | tools |

---

### 7.2 创建英文文章 Front Matter 模板

#### ▶️ Execute
在 `source-en/_posts/` 创建一篇模板文章：

```markdown
---
title: "Your English Title Here"
date: YYYY-MM-DD HH:MM:SS
updated: YYYY-MM-DD HH:MM:SS
tags:
  - tag1
  - tag2
categories:
  - Category
  - SubCategory
lang: en
description: "English description for SEO"
---

Your English content here.
```

> ⚠️ **PITFALL**: `date` 字段如果与中文版不一致（即使是 1 秒），归档排序可能会混乱。建议保持相同日期。

#### ✅ Verify
- [ ] 模板文件已创建
- [ ] 至少保留一份空白模板供后续使用

---

### 7.3 双语内容同步流程

#### ▶️ Execute
建立日后新增文章的工作流程规范：

```
新文章工作流:
1. 在 source-zh/_posts/ 创建中文 .md → hexo g 本地预览
2. 在 source-en/_posts/ 创建同名英文 .md（或不同名，但保持相同日期）
3. 本地构建验证: npx hexo multiple-language-generate && npx hexo s
4. 检查两个语言版本文档是否都能正常渲染
5. git commit && git push
```

#### ✅ Verify
- [ ] 工作流程已记录（可添加到项目 README 或 CONTRIBUTING.md）

---

## Phase 8: CI/CD 与构建脚本更新

> 目的：让 CI/CD 使用新的多语言构建命令。

---

### 8.1 检查现有 CI/CD 配置

#### ▶️ Execute
```bash
# 查找 GitHub Actions
ls -R .github/workflows/ 2>/dev/null

# 检查 package.json 构建脚本
grep -A 5 '"scripts"' package.json
```

#### ✅ Verify
- [ ] 是否存在 `.github/workflows/` 目录及 `.yml` 文件: `______`
- [ ] 当前 `package.json` 的 `scripts` 字段内容已记录

---

### 8.2 修改 GitHub Actions（如果有）

#### ▶️ Execute
编辑 `.github/workflows/*.yml`，找到构建步骤，将：
```yaml
- run: hexo generate
# 或
- run: npx hexo g
# 或
- run: hexo g
```
替换为：
```yaml
- run: npx hexo multiple-language-generate
```

> ⚠️ **PITFALL**: 如果有 `hexo clean` 步骤，**保留**它在新命令之前。

#### ✅ Verify
- [ ] 构建命令已替换为 `npx hexo multiple-language-generate`
- [ ] `hexo clean`（如果有）未被删除

如果**没有** GitHub Actions（部署通过本地 `hexo g -d`），跳过此步。

---

### 8.3 更新 package.json scripts

#### ▶️ Execute
编辑 `package.json` 的 `scripts` 字段：

```json
{
  "scripts": {
    "build": "hexo multiple-language-generate",
    "build:zh": "hexo generate",
    "server": "hexo multiple-language-generate && hexo server",
    "server:zh": "hexo server",
    "clean": "hexo clean",
    "deploy": "hexo multiple-language-generate && hexo deploy"
  }
}
```

> 说明：`build:zh` 和 `server:zh` 保留纯中文构建能力，方便紧急回退。

#### ✅ Verify
- [ ] `grep "multiple-language-generate" package.json` 有结果
- [ ] JSON 格式正确（用 IDE 或 `python -m json.tool package.json` 验证）

---

### 8.4 更新 .gitignore

#### ▶️ Execute
在 `.gitignore` 中添加（如果还没有）：
```
public/
public-en/
```

#### ✅ Verify
- [ ] `.gitignore` 包含 `public/` 和 `public-en/`

---

## Phase 9: 本地构建验证（核心阶段）

> 🔴 **这是整个手册最重要的阶段**。如果这里验证不通过，不要部署。

---

### 9.1 清理旧的构建产物

#### ▶️ Execute
```bash
npx hexo clean
rm -rf public/ public-en/ 2>/dev/null
```

#### ✅ Verify
- [ ] `ls public/` 报错（目录不存在）
- [ ] `ls public-en/` 报错（目录不存在）

---

### 9.2 首次完整构建

#### ▶️ Execute
```bash
npx hexo multiple-language-generate
```

#### 📤 Expected
终端输出应包含：
```
INFO  Start processing (Chinese site)
INFO  Files loaded in source-zh/
INFO  Generated: index.html
INFO  ...
INFO  Start processing (English site)
INFO  Files loaded in source-en/
INFO  Generated: en/index.html
INFO  ...
```

#### ✅ Verify
- [ ] 命令成功退出（无 error）
- [ ] 两个语言版本都显示生成完成
- [ ] 无 WARNING 或 ERROR（除了可能缺少英文文章的空目录警告）

#### 🔙 Rollback
如果构建失败，检查：
- Phase 4 的 config.*.yml 配置是否完整
- Phase 6 的 hexo-multiple-language.yml 配置项是否正确
- YAML 语法是否正确

---

### 9.3 输出目录结构验证

#### ▶️ Execute
```bash
# 中文站
echo "=== Chinese site (public/) ==="
ls public/index.html && echo "index.html OK"
ls public/archives/ && echo "archives/ OK"
ls public/tags/ && echo "tags/ OK"
ls public/categories/ && echo "categories/ OK"
ls public/css/ && echo "css/ OK"
ls public/js/ && echo "js/ OK"

# 英文站
echo "=== English site (public/en/) ==="
ls public/en/index.html && echo "en/index.html OK"
ls public/en/archives/ && echo "en/archives/ OK"
ls public/en/tags/ && echo "en/tags/ OK"
ls public/en/categories/ && echo "en/categories/ OK"
ls public/en/css/ && echo "en/css/ OK"
ls public/en/js/ && echo "en/js/ OK"
```

#### ✅ Verify
- [ ] 中文站所有核心目录存在
- [ ] 英文站所有核心目录存在

---

### 9.4 HTML 内容抽查

#### ▶️ Execute
```bash
# 检查中文首页
echo "=== Chinese index.html ==="
grep '<html lang=' public/index.html
grep 'og:url' public/index.html | head -1
grep 'canonical' public/index.html | head -1

# 检查英文首页
echo "=== English index.html ==="
grep '<html lang=' public/en/index.html
grep 'og:url' public/en/index.html | head -1
grep 'canonical' public/en/index.html | head -1
```

#### 📤 Expected
```
# 中文首页
<html lang="zh-CN">
<meta property="og:url" content="https://loulanrevo.github.io/index.html">
<link rel="canonical" href="https://loulanrevo.github.io/index.html">

# 英文首页
<html lang="en">
<meta property="og:url" content="https://loulanrevo.github.io/en/index.html">
<link rel="canonical" href="https://loulanrevo.github.io/en/index.html">
```

#### ✅ Verify
- [ ] 中文站 `lang="zh-CN"`
- [ ] 英文站 `lang="en"`
- [ ] 中文站 canonical URL 不以 `/en/` 开头
- [ ] 英文站 canonical URL 以 `/en/` 开头
- [ ] 所有 URL 是 `https://loulanrevo.github.io`（不是 `http://example.com`）

#### 🔙 Rollback
如果看到 `http://example.com`，说明 `config.*.yml` 的 `url` 字段未正确修改。回到 Phase 4 检查。

---

### 9.5 语言切换脚本验证

#### ▶️ Execute
```bash
# 搜索插件注入的切换代码
grep -r "multiple-language-switch" public/ --include="*.js" --include="*.html" | head -20
grep -r "storage-ttl\|localStorage" public/ --include="*.js" | head -10
```

#### ✅ Verify
- [ ] 输出包含 JavaScript 切换逻辑
- [ ] 包含 `localStorage` 存储逻辑
- [ ] `86400000`（1 天，storage-ttl）出现在脚本中

---

### 9.6 本地服务器测试

⚠️ **PITFALL**: 直接 `hexo server` 使用的是 `_config.yml`，不会触发多语言构建。正确的方式是：

#### ▶️ Execute
```bash
# 先多语言构建，再启动服务器
npx hexo multiple-language-generate && npx hexo server
```

#### ✅ Verify — 中文站基础测试
- [ ] 访问 `http://localhost:4000/` — 显示中文首页
- [ ] 点击文章链接 — 正常打开中文文章
- [ ] 点击"归档" — 正常显示归档页
- [ ] 点击"标签" — 正常显示标签页
- [ ] 点击"分类" — 正常显示分类页

#### ✅ Verify — 英文站基础测试
- [ ] 访问 `http://localhost:4000/en/` — 显示英文首页（可能是空白或仅有框架，因为还没英文文章）
- [ ] 检查菜单链接都指向 `/en/` 路径

#### ✅ Verify — 语言切换测试
- [ ] 在中文站点击 "English" → 跳转到 `/en/`
- [ ] 在英文站点击 "中文" → 跳转到 `/`

#### ✅ Verify — 浏览器语言自动跳转测试
- [ ] 将浏览器首选语言设为**英文**，访问 `http://localhost:4000/` → 应自动跳转到 `/en/`
- [ ] 将浏览器首选语言设为**中文**，访问 `http://localhost:4000/` → 应停留 `/`（不跳转）

> 💡 浏览器语言设置方法：
> - Chrome: `设置 → 语言`，将英文拖到中文上方
> - Firefox: `设置 → 常规 → 语言`，添加英文并置顶
> - 或用无痕模式 + 系统语言临时改为英文

---

### 9.7 功能特性逐项验证

#### ▶️ Execute
逐一测试以下博客功能特性：

- [ ] **Dark mode** — 中/英文站都正常切换亮/暗模式
- [ ] **Highlight.js** — 代码块语法高亮正常（查看含代码的文章）
- [ ] **Mermaid 图表** — 如果有相关文章，图表正常渲染
- [ ] **本地搜索** — 中/英文站各自搜索正常
- [ ] **Pjax 页面切换** — 页面间跳转无闪烁、URL 正确
- [ ] **FontAwesome 图标** — 所有图标正常显示
- [ ] **社交链接** — GitHub、知乎、哔哩哔哩、网易云音乐链接正常
- [ ] **blog-data 组件** — 如果有的话，正常加载

---

## Phase 10: 清理与最终检查

> 目的：整理项目，准备提交。

---

### 10.1 旧配置文件标注

#### ▶️ Execute
确认 `_config.yml` 和 `_config.butterfly.yml` 顶部已添加 DEPRECATED 注释（Phase 4.4 和 Phase 5 已做）。

#### ✅ Verify
- [ ] `_config.yml` 顶部有 DEPRECATED 注释
- [ ] `_config.butterfly.yml` 顶部有 DEPRECATED 注释

---

### 10.2 文件结构最终审核

#### ▶️ Execute
```bash
echo "=== 期望的目录结构 ==="
ls -la | grep -E "config\.|hexo-multiple|source-|_config|package"
```

#### ✅ Verify
期望看到的文件/目录：

```
✓ config.zh.yml               # 中文 Hexo 配置（完整）
✓ config.en.yml               # 英文 Hexo 配置（完整）
✓ config.butterfly.zh.yml     # 中文主题配置（完整）
✓ config.butterfly.en.yml     # 英文主题配置（完整）
✓ hexo-multiple-language.yml  # 插件配置
✓ source-zh/                  # 中文内容
✓ source-en/                  # 英文内容
✓ _config.yml                 # DEPRECATED 保留参考
✓ _config.butterfly.yml       # DEPRECATED 保留参考
✓ package.json                # 含更新后的 scripts
```

不应出现的文件/目录：

```
✗ source/                     # 应该已被重命名为 source-zh/
✗ public/                     # 应该被 .gitignore 忽略且在 git status 中不出现
✗ public-en/                  # 同上
```

- [ ] 所有 ✓ 项存在
- [ ] 所有 ✗ 项不存在或已被忽略

---

### 10.3 Git 提交

#### ▶️ Execute
```bash
git status              # 仔细审视变更列表
git add -A
git status              # 再次确认
```

#### ✅ Verify
- [ ] 没有意外文件被加入（如 `public/`、`public-en/`、`node_modules/`）
- [ ] 提交信息建议:
```
feat: add bilingual (zh/en) support with hexo-multiple-language-generate

- Install hexo-multiple-language-generate plugin
- Split source/ into source-zh/ and source-en/
- Create config.zh.yml, config.en.yml for Hexo core
- Create config.butterfly.zh.yml, config.butterfly.en.yml for theme
- Add language switch button with auto-browser-redirect
- Update build scripts and CI/CD
```

#### ▶️ Execute
```bash
git commit -m "feat: add bilingual (zh/en) support with hexo-multiple-language-generate"
git push origin main  # 或你的默认分支
```

- [ ] `git push` 成功

---

## Phase 11: 部署与部署后验证

> 目的：部署到生产环境并全面验证。

---

### 11.1 GitHub Pages 设置确认

#### ▶️ Execute
访问 `https://github.com/loulanrevo/loulanrevo.github.io/settings/pages`，确认：

#### ✅ Verify
- [ ] Source 设置正确（如 `Deploy from a branch` → `main` `/ (root)` 或 GitHub Actions）
- [ ] 自定义域名（如果有）正确配置
- [ ] 如果使用自定义域名，确认 `CNAME` 文件在 `source-zh/` 目录中

---

### 11.2 触发部署

取决于你的部署方式：

**方式 A：GitHub Actions（推荐）**
- 11.2 的 push 应已触发 Actions
- 访问 `https://github.com/loulanrevo/loulanrevo.github.io/actions` 监控运行

**方式 B：本地部署**
```bash
npx hexo multiple-language-generate && npx hexo deploy
```

#### ✅ Verify
- [ ] GitHub Actions 运行成功（绿色 ✓）
- [ ] 或本地部署命令成功退出

---

### 11.3 生产环境验证清单

> 🚨 **每一项都必须验证。任何一项不通过，不要宣布完成。**

#### 基础访问
- [ ] `https://loulanrevo.github.io/` — 中文首页正常加载
- [ ] `https://loulanrevo.github.io/en/` — 英文首页正常加载
- [ ] 中文站返回 HTTP 200
- [ ] 英文站返回 HTTP 200

#### 导航
- [ ] 中文站菜单正常工作（首页/归档/标签/分类）
- [ ] 英文站菜单正常工作（Home/Archives/Tags/Categories），所有链接指向 `/en/` 路径
- [ ] 每篇文章链接正常打开

#### 语言切换
- [ ] 中文站点击 "English" → 跳转到 `/en/`
- [ ] 英文站点击 "中文" → 跳转到 `/`
- [ ] 切换后刷新页面 → 保持在当前语言（localStorage 生效）

#### 浏览器语言自动跳转
- [ ] 浏览器首选语言为中文 → 访问 `https://loulanrevo.github.io/` 停留不跳转
- [ ] 浏览器首选语言为英文 → 访问 `https://loulanrevo.github.io/` 自动跳转到 `/en/`
- [ ] 浏览器首选语言为日文（未配置） → 使用 `not-matched-use` 默认中文，停留不跳转

#### SEO
- [ ] 中文站 `<link rel="canonical">` 指向 `https://loulanrevo.github.io/...`
- [ ] 英文站 `<link rel="canonical">` 指向 `https://loulanrevo.github.io/en/...`
- [ ] 中文站 `<html lang="zh-CN">`
- [ ] 英文站 `<html lang="en">`

#### 功能特性
- [ ] Dark mode 正常
- [ ] 代码高亮正常
- [ ] 搜索功能正常
- [ ] 社交链接正常

#### 性能
- [ ] 中文站加载时间可接受（< 3 秒）
- [ ] 英文站加载时间可接受（< 3 秒）

---

## 附录 A: 常见问题排查

### A.1 构建后 public/ 为空或只有默认 Landscape 主题

**现象**: `npx hexo multiple-language-generate` 完成但 `public/` 内容不对。

**根因**: `config.zh.yml` 或 `config.en.yml` 不是完整配置，缺少 `theme: butterfly` 等关键字段。

**解决**:
```bash
# 对比原 _config.yml 和 config.zh.yml 的差异
diff _config.yml config.zh.yml
# 确认除了 source_dir、url、root、language、ignore 外，其他字段完全一致
```

---

### A.2 英文站访问 404

**现象**: `http://localhost:4000/en/` 返回 404。

**根因**: 常见原因：
1. `hexo server` 直接启动，没用 `hexo multiple-language-generate` 先构建
2. `config.en.yml` 中 `root: /en/` 与 `hexo-multiple-language.yml` 中 `language-path: "en"` 不一致

**解决**:
```bash
# 正确启动方式
npx hexo multiple-language-generate && npx hexo server
# 确认配置一致性
grep "root:" config.en.yml
grep "language-path" hexo-multiple-language.yml
```

---

### A.3 语言切换按钮点击无反应

**现象**: 点击 "English" / "中文" 按钮无任何反应。

**根因**: `multiple-language-switch` CSS class 拼写错误，或被主题的其他 JS 覆盖。

**解决**:
```bash
# 检查主题配置中的按钮定义
grep "multiple-language-switch" config.butterfly.zh.yml config.butterfly.en.yml
# 确认拼写完全正确：m-u-l-t-i-p-l-e-语言名称-s-w-i-t-c-h
# 检查构建后的 HTML 中是否有切换脚本
grep "switchLanguage\|multiple-language" public/index.html
```

---

### A.4 浏览器语言自动跳转不生效

**现象**: 浏览器语言设为英文，访问根 URL 却没有跳转到 `/en/`。

**根因**:
1. `switch-language.enable: false`
2. `other-language` 映射中缺少浏览器的语言代码
3. 浏览器语言代码未被正确识别

**解决**:
```bash
# 检查 YAML 配置
grep -A 10 "switch-language" hexo-multiple-language.yml
# 确保 enable: true
# 确保 other-language 的 en 映射中包含 "en"、"en-US"、"en-GB"
# 测试：浏览器开发者工具 Console 中执行
console.log(navigator.language)  # 应该输出 "en-US" 或类似
```

---

### A.5 站点 URL 仍是 http://example.com

**现象**: 构建后的 HTML 里 `<meta og:url>` 还是 `http://example.com`。

**根因**: `config.zh.yml` 和 `config.en.yml` 的 `url` 字段未修改。

**解决**:
```bash
grep "url:" config.zh.yml config.en.yml
# 应分别为：
# config.zh.yml: url: https://loulanrevo.github.io
# config.en.yml: url: https://loulanrevo.github.io/en
```

---

### A.6 菜单链接指向错误路径

**现象**: 英文站的菜单链接指向中文站（缺少 `/en/` 前缀），或反过来。

**根因**: `config.butterfly.en.yml` 中菜单 URL 忘了加 `/en/` 前缀。

**解决**: 编辑 `config.butterfly.en.yml`，确保所有菜单项 URL 形如：
```yaml
Home: /en/ || fas fa-home
Archives: /en/archives/ || fas fa-archive
```

---

### A.7 构建时报 YAML 解析错误

**现象**: `npx hexo multiple-language-generate` 报 YAML 解析错误。

**根因**: 某个 `.yml` 文件语法错误（缩进不一致、特殊字符未转义等）。

**解决**:
```bash
# 逐一检查每个新创建的 YAML 文件
python -c "import yaml; yaml.safe_load(open('config.zh.yml'))"
python -c "import yaml; yaml.safe_load(open('config.en.yml'))"
python -c "import yaml; yaml.safe_load(open('config.butterfly.zh.yml'))"
python -c "import yaml; yaml.safe_load(open('config.butterfly.en.yml'))"
python -c "import yaml; yaml.safe_load(open('hexo-multiple-language.yml'))"
# 哪个报错就是哪个有问题
```

---

### A.8 构建时报 source_dir 找不到

**现象**: `FATAL Can't find source dir: source-en/`

**根因**: `source-en/` 目录未创建或命名不一致。

**解决**:
```bash
mkdir -p source-en/_posts
ls -d source-en/
```

---

### A.9 GitHub Actions 部署失败

**现象**: CI/CD 运行失败。

**根因**: Actions 中仍使用 `hexo generate` 而不是 `hexo multiple-language-generate`。

**解决**: 检查 `.github/workflows/*.yml`，确认构建命令已替换。

---

### A.10 本地搜索英文站搜不到英文文章

**现象**: 英文站搜索无结果。

**根因**: 搜索索引基于 `source_dir` 生成，英文文章在 `source-en/`，可能需确认搜索插件配置。

**解决**: 检查搜索插件配置（`local_search` 或 `algolia`）在两个 config 中一致。本地搜索通常自动适配。

---

### A.11 图片/静态资源在英文站 404

**现象**: 英文站文章中的图片不显示。

**根因**: 图片路径使用了相对路径，英文站路径前缀不同。

**解决**:
- 方案 A（推荐）: 使用绝对 URL 引用图片，如 `https://loulanrevo.github.io/img/xxx.png`
- 方案 B: 复制 `source-en/img/` 并调整文章中的图片路径

---

### A.12 主题样式在两个语言站中不一致

**现象**: 中文站和英文站看起来不一样。

**根因**: `config.butterfly.zh.yml` 和 `config.butterfly.en.yml` 的功能性配置不一致。

**解决**: 回到 Phase 5.3 做一致性检查，确保只有文本字段有差异。

---

### A.13 中英文文章归档排序不一致

**现象**: 中英文站的文章排序不同。

**根因**: 中文和英文文章的 `date` Front Matter 不一致。

**解决**: 确保同名文章使用相同的 `date` 值。

---

### A.14 Pjax 在跨语言切换时异常

**现象**: 语言切换后 Pjax 导致页面混乱。

**根因**: Pjax 不处理跨域/跨路径切换。这是预期行为，插件设计为手动点击切换时做完整页面跳转。

**解决**: 这是正常行为，无需处理。

---

### A.15 node_modules 变化导致原有功能异常

**现象**: 安装插件后原博客功能出现问题。

**根因**: 插件引入的依赖与现有依赖冲突。

**解决**:
```bash
# 回滚到安装前
npm uninstall hexo-multiple-language-generate
rm -rf node_modules package-lock.json
npm install        # 重新安装原有依赖
# 然后重新安装插件并检查
npm install hexo-multiple-language-generate --save
```

---

## 附录 B: 回滚完全指南

### B.1 快速回滚（30 秒内）

**适用**: 构建失败、效果不符合预期，想立即回到原始状态。

```bash
# Git 恢复所有修改
git checkout backup/before-multilang
# 或
git reset --hard HEAD~1
```

### B.2 选择性回滚

**适用**: 只想恢复部分内容。

```bash
# 恢复目录结构
rm -rf source-zh/ source-en/
mv source/ source-zh/ 2>/dev/null || git checkout -- source/

# 恢复配置文件
rm -f config.zh.yml config.en.yml config.butterfly.zh.yml config.butterfly.en.yml hexo-multiple-language.yml
git checkout -- _config.yml _config.butterfly.yml

# 卸载插件
npm uninstall hexo-multiple-language-generate
```

### B.3 从冷备份完全恢复

**适用**: Git 历史被破坏，需要从文件备份恢复。

```bash
# 定义备份目录
BACKUP_DIR=~/hexo-backup-YYYYMMDD  # 替换实际日期

# 恢复所有文件
cp "$BACKUP_DIR"/_config.yml .
cp "$BACKUP_DIR"/_config.butterfly.yml .
cp -r "$BACKUP_DIR"/source/ .
cp "$BACKUP_DIR"/package.json .
cp "$BACKUP_DIR"/package-lock.json . 2>/dev/null

# 清理新增文件
rm -f config.zh.yml config.en.yml config.butterfly.zh.yml config.butterfly.en.yml hexo-multiple-language.yml
rm -rf source-zh/ source-en/

# 重新安装依赖
npm install
```

### B.4 回滚验证

```bash
npx hexo clean
npx hexo generate
npx hexo server
# 确认 http://localhost:4000 显示原始中文博客
```

---

## 附录 C: 配置文件差异速查表

### C.1 Hexo 核心配置差异（config.zh.yml vs config.en.yml）

| 字段 | config.zh.yml | config.en.yml | 说明 |
|------|:---|:---|------|
| `url` | `https://loulanrevo.github.io` | `https://loulanrevo.github.io/en` | 站点 URL |
| `root` | `/` | `/en/` | 根路径 |
| `source_dir` | `source-zh` | `source-en` | 源文件目录 |
| `public_dir` | `public` | `public-en` | 编译输出目录 |
| `language` | `zh-CN` | `en` | 站点语言 |
| `title` | `loulanre`（中文） | `loulanre`（英文） | 站点标题 |
| `subtitle` | 中文 | 英文翻译 | 副标题 |
| `description` | 中文 | 英文翻译 | 站点描述 |
| `author` | `楼兰RE` | `LouLanRE` | 作者名 |
| `ignore` | `[source-en/]` | `[source-zh/]` | 忽略目录 |
| 其他字段 | 完全一致 | 完全一致 | — |

### C.2 Butterfly 主题配置差异（config.butterfly.zh.yml vs config.butterfly.en.yml）

| 区域 | config.butterfly.zh.yml | config.butterfly.en.yml |
|------|------|------|
| 菜单文案 | 首页、归档、标签、分类、语言 | Home、Archives、Tags、Categories、Language |
| 菜单 URL | `/`、`/archives/`、`/tags/`、`/categories/` | `/en/`、`/en/archives/`、`/en/tags/`、`/en/categories/` |
| 语言切换（中文按钮）| 中文: zh | 中文: zh |
| 语言切换（英文按钮）| English: en | English: en |
| footer | 中文 | 英文 |
| copyright | 中文 | 英文 |
| 其他功能性配置 | — | **完全相同** |

---

## 执行总结 Checklist

完成所有 Phase 后，验证以下高层目标：

- [ ] `npx hexo multiple-language-generate` 成功运行
- [ ] 中文站 `http://localhost:4000/` 正常
- [ ] 英文站 `http://localhost:4000/en/` 正常（至少框架和菜单正确）
- [ ] 语言切换按钮双向可用
- [ ] 浏览器语言自动跳转正常
- [ ] GitHub Pages 生产环境正常
- [ ] Git 提交已推送到远程

---

> **手册版本**: v1.0
> **基于**: fix.md（初版 7 步骤）
> **适用**: Hexo v8.x + Butterfly v5.x + hexo-multiple-language-generate
> **最后更新**: 2026-07-08
