---
title: Mermaid数据可视化演示
date: 2026-05-04 16:00:00
tags: ["工具", "教程"]
categories: ["技术教程", "工具使用"]
---

# 📊 博客数据可视化：Mermaid 图表完全指南

本文展示如何在博客中使用**Mermaid**创建精美的数据可视化图表。所有图表都是通过 Markdown 代码块直接编写，无需外部服务。

## 🔧 技术栈与插件

| 层级 | 技术/插件 | 说明 |
| --- | --- | --- |
| 博客框架 | [Hexo](https://hexo.io/)`v8.1.1` | 静态博客生成器 |
| 主题 | [Butterfly](https://butterfly.js.org/)`v5.5.4` | 内置 Mermaid 支持，配置`mermaid.code_write: true` |
| 图表引擎 | [Mermaid](https://mermaid.js.org/) | 基于 JavaScript 的图表绘制工具，支持流程图、时序图、甘特图等 |
| 语法转换 | `mermaid-convert.js` | 自研 Hexo Filter 插件，自动将````mermaid`代码块转换为 Butterfly 的`&#123;% mermaid %}`标签 |
| 样式主题 | `darkmode.css` | 自定义暗色主题变量，确保图表在 dark mode 下清晰可读 |

---

## 1. 流程图 (Flowchart)

流程图是最常用的图表类型，适合展示工作流程、决策过程等。

```mermaid
graph TD
    A[开始写博客] --> B{选择主题?}
    B -->|Butterfly| C[安装主题]
    B -->|其他| D[自定义配置]
    C --> E[配置插件]
    D --> E
    E --> F[撰写内容]
    F --> G{需要图表?}
    G -->|是| H[使用 Mermaid]
    G -->|否| I[纯文本/图片]
    H --> J[发布文章]
    I --> J
```

### 使用场景

- 工作流程说明
- 决策树
- 算法逻辑
- 系统架构

---

## 2. 时序图 (Sequence Diagram)

时序图用于展示对象之间的交互顺序，特别适合描述 API 调用、用户操作等场景。

```mermaid
sequenceDiagram
    participant 用户
    participant 浏览器
    participant Hexo服务器
    participant GitHub Pages

    用户->>浏览器: 访问博客 URL
    浏览器->>GitHub Pages: 发送 HTTP 请求
    GitHub Pages-->>浏览器: 返回 HTML 页面
    
    Note over 用户,浏览器: 页面开始渲染
    
    浏览器->>浏览器: 解析 Mermaid 代码块
    浏览器->>浏览器: 渲染 SVG 图表
    浏览器-->>用户: 显示可视化内容
    
    User->>User: 欣赏精美图表 ✨
```

### 使用场景

- API 文档
- 用户交互流程
- 系统消息传递
- 协议说明

---

## 3. 饼图 (Pie Chart)

饼图适合展示数据占比和分布情况。

```mermaid
pie title 我的博客内容类型分布
    "技术教程" : 35
    "读书笔记" : 25
    "生活随笔" : 20
    "音乐分享" : 12
    "项目总结" : 8
```

```mermaid
pie showData
    title 2026 年度写作计划
    "前端开发" : 30
    "后端技术" : 25
    "工具推荐" : 20
    "哲学思考" : 15
    "翻译作品" : 10
```

### 使用场景

- 数据统计
- 占比分析
- 时间分配
- 分类展示

---

## 4. 甘特图 (Gantt Chart)

甘特图是项目管理的好帮手，可以清晰展示任务时间线。

```mermaid
gantt
    title 博客建设计划 2026
    dateFormat  YYYY-MM-DD
    section 基础搭建
    安装 Hexo          :a1, 2026-01-01, 3d
    配置 Butterfly 主题 :a2, after a1, 5d
    部署到 GitHub Pages :a3, after a2, 2d
    
    section 内容创作
    写第一篇文章        :b1, after a3, 7d
    配置 Mermaid 插件   :b2, after b1, 2d
    编写数据可视化教程  :b3, after b2, 5d
    
    section 优化提升
    SEO 优化            :c1, after b3, 4d
    性能优化            :c2, after c1, 3d
    添加评论系统        :c3, after c2, 3d
```

### 使用场景

- 项目进度管理
- 学习计划
- 发布路线图
- 任务依赖关系

---

## 5. 类图 (Class Diagram)

类图用于展示代码结构和面向对象设计。

```mermaid
classDiagram
    class Article {
        +String title
        +Date date
        +String[] tags
        +String content
        +publish()
        +edit()
        +delete()
    }
    
    class Category {
        +String name
        +String slug
        +Article[] articles
        +addArticle()
        +getCount()
    }
    
    class Tag {
        +String name
        +Article[] articles
        +getRelatedArticles()
    }
    
    class Author {
        +String name
        +String email
        +Article[] posts
        +writePost()
    }
    
    Article "*" --> "1" Category : belongsTo
    Article "*" --> "*" Tag : hasTag
    Article "*" --> "1" Author : writtenBy
```

### 使用场景

- 代码文档
- 数据库设计
- API 结构说明
- 系统架构

---

## 6. 状态图 (State Diagram)

状态图用于展示对象的状态变化和转换条件。

```mermaid
stateDiagram-v2
    [*] --> 草稿: 新建文章
    草稿 --> 编辑中: 开始编辑
    编辑中 --> 草稿: 放弃修改
    编辑中 --> 审核中: 提交审核
    审核中 --> 编辑中: 需要修改
    审核中 --> 已发布: 审核通过
    已发布 --> 已下架: 下架文章
    已下架 --> 编辑中: 重新编辑
    已发布 --> [*]: 删除
```

### 使用场景

- 流程状态管理
- 生命周期说明
- 业务规则
- 状态机设计

---

## 7. ER 图 (Entity Relationship)

ER 图用于展示数据库实体之间的关系。

```mermaid
erDiagram
    POST ||--o{ COMMENT : has
    POST ||--o{ TAG : contains
    POST }o--|| CATEGORY : belongs_to
    USER ||--o{ POST : writes
    USER ||--o{ COMMENT : creates
    
    POST {
        int id PK
        string title
        text content
        datetime created_at
        datetime updated_at
        int category_id FK
        int author_id FK
    }
    
    USER {
        int id PK
        string username
        string email
        string avatar
        datetime created_at
    }
    
    COMMENT {
        int id PK
        text content
        datetime created_at
        int post_id FK
        int user_id FK
    }
    
    TAG {
        int id PK
        string name
        string slug
    }
    
    CATEGORY {
        int id PK
        string name
        string description
    }
```

### 使用场景

- 数据库设计
- 数据模型说明
- API 关系文档
- 系统架构

---

## 8. 思维导图 (Mindmap)

思维导图适合展示层次化的知识结构。

```mermaid
mindmap
  root((博客运营))
    内容创作
      技术教程
        前端开发
        后端技术
        DevOps
      生活随笔
        读书笔记
        音乐分享
        旅行记录
      项目总结
        开源贡献
        学习心得
    技术优化
      性能优化
        图片压缩
        CDN 加速
        代码分割
      SEO 优化
        元数据配置
        sitemap 生成
      用户体验
        响应式设计
        暗色模式
    运营推广
      社交媒体
        微博
        Twitter
        即刻
      社区互动
        GitHub
        知乎
        V2EX
```

### 使用场景

- 知识整理
- 思路梳理
- 项目规划
- 学习路径

---

## 🎨 高级技巧

### 自定义样式

Mermaid 支持自定义颜色和样式：

```mermaid
graph LR
    A[🔵 核心功能] --> B[🟢 扩展模块]
    B --> C[🔴 外部集成]
    
    style A fill:#e1f5ff,stroke:#01579b,stroke-width:3px
    style B fill:#e8f5e9,stroke:#2e7d32,stroke-width:2px
    style C fill:#ffebee,stroke:#c62828,stroke-width:2px
```

### 子图 (Subgraphs)

使用子图组织复杂图表：

```mermaid
graph TB
    subgraph 前端["前端层"]
        A[React 组件]
        B[状态管理]
        C[路由配置]
    end
    
    subgraph 后端["后端层"]
        D[API 服务]
        E[数据库]
        F[缓存层]
    end
    
    subgraph 基础设施["基础设施"]
        G[CDN]
        H[监控系统]
    end
    
    A --> D
    B --> D
    C --> D
    D --> E
    D --> F
    A --> G
    D --> H
```

---

## 📝 使用建议

1. **保持简洁**：每个图表只表达一个核心观点
2. **合理选择**：根据数据类型选择合适的图表
3. **注意可读性**：避免过于复杂的嵌套结构
4. **添加说明**：配合文字解释图表含义
5. **测试渲染**：发布前预览确保显示正常

---

## 🔧 相关资源

- [Mermaid 官方文档](https://mermaid.js.org/intro/)
- [Mermaid 在线编辑器](https://mermaid.live/)
- [Butterfly 主题文档](https://butterfly.js.org/posts/4aa8abbe/)

---

> 💡**提示**：本文所有图表都是实时渲染的 SVG，支持缩放和打印，且无需加载任何外部图片资源。