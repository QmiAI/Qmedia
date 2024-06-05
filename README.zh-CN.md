<div align="center"><a name="readme-top"></a>

<a href="https://x.com/Lafe8088" target="_blank">
  <img src="/docs/images/top.png" alt="alt text">
</a>

<h1>QMedia</h1>
<h3>
专为内容创作者设计的AI内容搜索引擎 <br /> 
</h3>

<div style="text-align: center;">

[English](./README.md) | **简体中文**

[更新日志](./CHANGELOG.md) - [报告问题][g-issues-link] - [请求功能][g-issues-link]

[![Twitter](https://img.shields.io/twitter/url/https/twitter.com/cloudposse.svg?style=social&label=Follow%20%40Lafe)][lafe-twitter] <a href="https://x.com/LinkLin1987"><img src="https://img.shields.io/badge/Follow-%40LinkLin-1DA1F2?logo=twitter&style={style}"></a> [![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](./LICENSE) <a href="https://discord.gg/rQq4QX3v"><img src="https://img.shields.io/discord/1245752894389489704?style=social&logo=discord"></a>

</div>

<div align="left">

### **主要特点**:

- 图文/短视频素材搜索.
- 高效分析图文/短视频内容, 整合零散信息.
- 提供内容来源及图文短视频信息拆解, 通过内容卡片的方式呈现信息.
- 基于图文/短视频内容, 根据用户兴趣需求生成定制化搜索结果.
- 本地化部署, 可针对私有数据离线内容搜索问答.

<details open="open">
<summary>目录树</summary>

- [👋🏻 介绍](#-介绍)
- [💫 特性一览](#-特性一览)
  - [`1` 内容卡片](#内容卡片)
  - [`2` 多模态内容 rag](#多模态内容-rag)
  - [`3` 本地图文/视频模型](#100-pure-local-multimodal-models)
- [🤖 Qmedia 本地安装](#-qmedia-安装说明)
  - [mm_server 模型安装](#mm_server-安装说明)
  - [mmrag_server 应用安装](#mmrag_server-安装说明)
  - [qmedia_web 网页安装](#qmedia_web-安装说明)
- [⭐️ Qmedia 使用](#qmedia-使用说明)
  - [组合使用](#组合使用)
  - [multimodel 单独使用](#独立模型服务)
  - [纯 python rag 服务/模型服务](#纯-python-rag-服务模型服务)
  </details>

<!-- ============================================ -->

### 👋🏻 介绍

**QMedia** 是一款开源的多媒体 AI 内容搜索引擎, 针对图文/短视频内容提供丰富的信息提取方式, 整合非结构化的图文/短视频信息, 构建多模态 RAG 内容问答. 希望以开源的方式分享交流 AI 内容创作
QMedia 目前正在积极开发中，有任何需求或者问题，欢迎提交 [issues][g-issues-link]

**分享 QMedia 给你的好友**
[![][share-x-shield]][share-x-link]

**碰撞内容创作新思路**
| <div align="center"> <a href="https://discord.gg/rQq4QX3v"><img src="https://img.shields.io/discord/1245752894389489704?style=social&logo=discord"></a> </div>| 加入我们的 Discord 社区！ |
| :---------------------------------------- | :------------------------ |
| ![alt text](docs/images/image-1.png) | **加入我们的 wechat 群聊 !** |

<br/>

<div align="right">

[![][back-to-top]](#readme-top)

</div>

<!-- ============================================ -->

### 💫 特性一览

- #### 内容卡片

  - 通过卡片的形式展示图文/视频内容
  - `web 服务` 借鉴小红书 web 版，基于 Typescript nextjs, tailwindcss, shadcn/ui 技术栈实现
  - `rag搜索/问答服务`, `图文/视频模型服务`基于 python, LlamaIndex 应用程序的框架实现
  - `web 服务`, `rag搜索/问答服务`, `图文/视频模型服务`可分离部署单独使用, 方便根据用户资源情况灵活部署, 嵌入其他系统用于图文/视频内容提取.

  <a href="https://x.com/Lafe8088" target="_blank">
    <img src="/docs/images/media_card.png" alt="alt text">
  </a>

  <br/>

- #### 多模态内容 RAG

  - 图文/短视频素材搜索.
  - 根据用户问题从图文/短视频内容提取有用信息, 生成高质量回答.
  - 通过内容卡片的方式呈现内容来源, 及图文短视频信息拆解.
    - 检索问答依赖对图文/短视频内容拆解, 包括图片风格,文案排版, 短视频文案转录, 视频总结等
  - 支持 google 内容搜索

  <a href="https://x.com/Lafe8088" target="_blank">
    <img src="/docs/images/query.png" alt="alt text">
  </a>

- #### **100% Pure Local multimodal models**

  - 多种类型模型本地部署
  - 与 rag 应用层分离, 便于替换不同模型
  - 本地模型生命周期管理, 可配置手动或自动释放, 减少服务器压力

  **语言模型**:

  - 支持本地 ollama 不同模型切换
    - [llama3:8b-instruct](https://ollama.com/library/llama3:8b-instruct-q4_0) 轻量级本地部署 LLM 模型
    - [llama3:70b-instruct](https://ollama.com/library/llama3:70b-instruct) 开源 llm 模型第八名

  **特征编码模型**:

  - 图片特征编码: [CLIP Encoder](https://github.com/openai/CLIP) 图片转为文本特征编码.
  - 文本编码: [BGE Encoder](https://github.com/FlagOpen/FlagEmbedding) 多语言嵌入式模型, 文本转为特征编码, 本地模型对齐 gpt Encoder.

  **图片类模型**:

  - 图片文案 OCR 识别: [Qanything](https://github.com/netease-youdao/QAnything/tree/v1.4.0-python) 本地知识库问答系统 OCR
  <!-- - 图片排版, 人物识别: [HQ-SAM](https://github.com/FlagOpen/HQ-SAM) 高质量分割一切 -->
  - 视觉理解大模型:

    - [ ] [llava-llama3](https://ollama.com/library/llava-llama3): ollama 本地部署 GPT-4V Level 视觉理解模型

  **视频类模型**:

  - 视频文案转录:
    - [Faster Whisper](https://github.com/SYSTRAN/faster-whisper): 快捷提取视频文案内容, 可本地 cpu 运行
  - 基于 LLM 短视频内容总结
  - [ ] 视频精彩片段识别
  - [ ] 视频风格类型识别
  - [ ] 视频分镜内容拆解

  <!-- ![alt text](/docs/images/image-14.png) -->

<div align="right">

[![][back-to-top]](#readme-top)

</div>

<!-- ============================================ -->

#### 后续计划

- [ ] **图文短视频内容分析, 爆款内容拆解**
- [ ] **同款图文/视频搜索**
- [ ] **卡片图文内容生成**
- [ ] **短视频内容剪辑**

<div align="right">

[![][back-to-top]](#readme-top)

</div>

---

<!-- ============================================ -->

### 🤖 QMedia 安装说明

#### 文件结构介绍

**QMedia 包含三组服务:**
可根据资源情况选择同步部署本地, 或模型服务部署云端.

#### **[mm_server 安装说明](./mm_server/README.zh-CN.md)**

- 多模态模型服务 `mm_server`:

  - 多模态模型部署及调用 API
  - Ollama LLM 模型
  - 图片类模型
  - 视频类模型
  - 特征嵌入模型

    <br/>

#### **[mmrag_server 安装说明](./mmrag_server/README.zh-CN.md)**

- AI 内容搜索问答服务 `mmrag_server`:

  - 内容卡片展示查询
  - 图文/短视频内容提取, 编码, 存储服务
  - 多模态数据 rag 检索服务
  - 内容问答服务

    <br/>

#### **[qmedia_web 安装说明](./qmedia_web/README.zh-CN.md)**

- web 服务 `qmedia_web`:
  语言: Typescript
  框架: Next.js
  样式: tailwindcss
  组件: shadcn/ui

<div align="right">

[![][back-to-top]](#readme-top)

</div>

---

### QMedia 使用说明

#### **组合使用**

`mm_server` + `qmedia_web` + `mmrag_server`
web 网页内容展示, 内容 rag 搜索问答, 调用模型服务

1. 服务启动流程:

```bash
# mm_server 服务启动
cd mm_server
source activate qllm
python main.py

# mmrag_server 服务启动
cd mmrag_server
source activate qmedia
python main.py

# qmedia_web 服务启动
cd qmedia_web
pnpm dev
```

2. 可通过网页使用检索功能
   `mmrag_server` 启动阶段会读取 `assets/medias`和 `assets/mm_pseudo_data.json` 中的伪数据, 并且调用`mm_server` 提取图文/短视频的信息结构化为`node`信息, 存储在 `db`中, 检索问答会根据`db`中的数据进行.

#### 自定义数据

```bash
# assets 文件结构
assets
├── mm_pseudo_data.json # 内容卡片数据
└── medias # 图片/视频文件
```

替换`assets`中的内容, 并且删除历史存储的`db`文件
`assets/medias` 为图片/视频文件, 可替换成自己图片/视频文件
`assets/mm_pseudo_data.json` 为内容卡片数据, 可替换成自己内容卡片数据, 运行服务后模型会自动提取信息, 存储在`db`中

<div align="right">

[![][back-to-top]](#readme-top)

</div>

---

#### **独立模型服务**

可单独使用 `mm_server` 本地图文/视频信息提取服务
当做独立的图片编码, 文字编码, 视频文案提取, 图片 OCR 服务, 通过 API 形式在任意场景使用

```bash
# 单独 mm_server 服务启动
cd mm_server
python main.py

# uvicorn main:app --reload --host localhost --port 50110
```

API 内容:

- http://localhost:50110/docs

![alt text](/docs/images/api2.png)

<br/>

#### **纯 python rag 服务/模型服务**

可配合 mm_server + qmedia_web, 在纯 python 环境下进行内容提取,rag 检索等 api 使用.

```bash
# 单独 mm_server 服务启动
cd mmrag_server
python main.py

# uvicorn main:app --reload --host localhost --port 50110
```

![alt text](/docs/images/api1.png)

API 内容:

- http://localhost:50110/docs
- http://localhost:8001/docs

<div align="right">

[![][back-to-top]](#readme-top)

</div>

---

### Star History

[![Star History Chart](https://api.star-history.com/svg?repos=QmiAI/Qmedia&type=Date)](https://star-history.com/#QmiAI/Qmedia&Date)

### License

`QMedia` is licensed under [MIT License](./LICENSE)

### Acknowledgments

Thanks to [QAnything](https://github.com/netease-youdao/QAnything/) for strong OCR models.

Thanks to [llava-llama3](https://github.com/netease-youdao/QAnything/) for strong llm vision models.

[lafe-twitter]: https://x.com/Lafe8088
[g-issues-link]: https://github.com/QmiAI/Qmedia/issues
[back-to-top]: https://img.shields.io/badge/-BACK_TO_TOP-151515?style=flat-square
[share-x-shield]: https://img.shields.io/badge/-share%20on%20x-black?labelColor=black&logo=x&logoColor=white&style=flat-square
[share-x-link]: https://twitter.com/intent/tweet?url=https://github.com/QmiAI/Qmedia&text=Qmedia%20%0A%E4%B8%80%E6%AC%BE%E5%BC%80%E6%BA%90AI%E5%86%85%E5%AE%B9%E6%90%9C%E7%B4%A2%E5%BC%95%E6%93%8E,%20%E4%B8%93%E4%B8%BA%E5%86%85%E5%AE%B9%E5%88%9B%E4%BD%9C%E8%80%85%E8%AE%BE%E8%AE%A1%E3%80%82%0A%E6%94%AF%E6%8C%81%E5%9B%BE%E6%96%87/%E7%9F%AD%E8%A7%86%E9%A2%91%E5%86%85%E5%AE%B9%E6%8F%90%E5%8F%96,%20%E5%8F%AF%E4%BB%A5%E6%9C%AC%E5%9C%B0%E6%90%AD%E5%BB%BA%E5%85%A8%E5%A5%97%E7%8E%AF%E5%A2%83%20(web%20app%20,%20rag%20server%20,%20llm%20server)%20,%20%E6%94%AF%E6%8C%81%E5%A4%9A%E6%A8%A1%E6%80%81RAG%E5%86%85%E5%AE%B9%E9%97%AE%E7%AD%94%0A%E6%AC%A2%E8%BF%8E%E4%BD%93%E9%AA%8C%E4%BA%A4%E6%B5%81
