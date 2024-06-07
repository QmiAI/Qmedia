<div align="center"><a name="readme-top"></a>

<a href="https://x.com/Lafe8088" target="_blank">
  <img src="/docs/images/top.png" alt="alt text">
</a>

<h1>QMedia</h1>
<h3>
AI content search engine designed specifically for content creators. <br /> 
</h3>

<div style="text-align: center;">

**English** | [简体中文](./README.zh-CN.md)

[Changelog](./CHANGELOG.md) - [Report Issues][g-issues-link] - [Request Feature][g-issues-link]

[![Twitter](https://img.shields.io/twitter/url/https/twitter.com/cloudposse.svg?style=social&label=Follow%20%40Lafe)][lafe-twitter] <a href="https://x.com/LinkLin1987"><img src="https://img.shields.io/badge/Follow-%40LinkLin-1DA1F2?logo=twitter&style={style}"></a> [![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](./LICENSE) <a href="https://discord.gg/MtMeTeGy"><img src="https://img.shields.io/discord/1245752894389489704?style=social&logo=discord"></a>

</div>

<div align="left">

### **Key Features**

- Search for image/text and short video materials.
- Efficiently analyze image/text and short video content, integrating scattered information.
- Provide content sources and decompose image/text and short video information, presenting information through content cards.
- Generate customized search results based on user interests and needs from image/text and short video content.
- Local deployment, enabling offline content search and Q&A for private data.

<details open="open">
<summary>Directory</summary>

- [👋🏻 Introduction](#-introduction)
- [💫 feature overview](#-feature-overview)
  - [`1` content cards](#content-cards)
  - [`2` multimodal content rag](#multimodal-content-rag)
  - [`3` pure local multimodalmodels](#pure-local-multimodal-models)
- [🤖 installation instructions](#-installation)
  - [mm_server Installation](#mm_server-installation)
  - [mmrag_server Installation](#mmrag_server-installation)
  - [qmedia_web Installation](#qmedia_web-installation)
- [⭐️ Usage](#️-usage)
  - [Combined Usage](#combined-usage)
  - [Independent model service](#independent-model-service)
  - [pure local multimodal](#pure-local-multimodal-models)
  </details>

<!-- ============================================ -->

### 👋🏻 Introduction

**QMedia** is an open-source multimedia AI content search engine , provides rich information extraction methods for text/image and short video content. It integrates unstructured text/image and short video information to build a multimodal RAG content Q&A system. The aim is to share and exchange ideas on AI content creation in an open-source manner. [issues][g-issues-link]

**Share QMedia with your friends.**

[![][share-x-shield]][share-x-link]

**Spark new ideas for content creation**
| <div align="center"> <a href="https://discord.gg/rQq4QX3v"><img src="https://img.shields.io/discord/1245752894389489704?style=social&logo=discord"></a> </div>| Join our Discord community！ |
| :---------------------------------------- | :------------------------ |
| ![alt text](docs/images/image-1.png) | **Join our WeChat group !** |

<br/>

<div align="right">

[![][back-to-top]](#readme-top)

</div>

<!-- ============================================ -->

### 💫 Feature Overview

- #### Content Cards

  - Display image/text and video content in the form of cards
  - `Web Service` inspired by XHS web version, implemented using the technology stack of Typescript, Next.js, TailwindCSS, and Shadcn/UI
  - `RAG Search/Q&A Service` and `Image/Text/Video Model Service` implemented using the Python framework and LlamaIndex applications
  - Web Service, `RAG Search/Q&A Service`, and `Image/Text/Video Model Service` can be deployed separately for flexible deployment based on user resources, and can be embedded into other systems for image/text and video content extraction.

  <a href="https://x.com/Lafe8088" target="_blank">
    <img src="/docs/images/media_card.png" alt="alt text">
  </a>

  <br/>

- #### Multimodal Content RAG

  - Search for image/text and short video materials.
  - Extract useful information from image/text and short video content based on user queries to generate high-quality answers.
  - Present content sources and the breakdown of image/text and short video information through content cards.
  - Retrieval and Q&A rely on the breakdown of image/text and short video content, including image style, text layout, short video transcription, video summaries, etc.
  - Support Google content search.

  <a href="https://x.com/Lafe8088" target="_blank">
    <img src="/docs/images/query.png" alt="alt text">
  </a>

- #### **Pure Local Multimodal Models**

  Deployment of various types of models locally
  Separation from the RAG application layer, making it easy to replace different models
  Local model lifecycle management, configurable for manual or automatic release to reduce server load

  **Language Models**:

  - Support local Ollama model switching.
    - [llama3:8b-instruct](https://ollama.com/library/llama3:8b-instruct-q4_0) Lightweight local deployment of LLM models.
    - [llama3:70b-instruct](https://ollama.com/library/llama3:70b-instruct) Eighth place in open-source LLM models.

  **Feature Embedding Models**:

  - Image Embedding: [CLIP Encoder](https://github.com/openai/CLIP) Convert images to text feature encoding.
  - Text Embedding: [BGE Encoder](https://github.com/FlagOpen/FlagEmbedding) Multilingual embedded model, converting text to feature encoding, with local models aligned to GPT Encoder.

  **Image Models**:

  - Image Text OCR Recognition: [Qanything](https://github.com/netease-youdao/QAnything/tree/v1.4.0-python) Local Knowledge Base Q&A System OCR
  <!-- - Image Layout and Character Recognition: [HQ-SAM](https://github.com/FlagOpen/HQ-SAM) High-Quality Segmentation of Everything -->
  - Visual Understanding Models:

    - [ ] [llava-llama3](https://ollama.com/library/llava-llama3): Ollama's locally deployed GPT-4V level visual understanding model.

  **Video Models**

  - Video Transcription:
    - [Faster Whisper](https://github.com/SYSTRAN/faster-whisper): Quickly extract video transcription content, can run on local CPU.
  - LLM-based Short Video Content Summarization
  - [ ] Identification of highlights in short videos
  - [ ] Recognition of short video style types
  - [ ] Analysis and breakdown of short video content

  <!-- ![alt text](/docs/images/image-14.png) -->

<div align="right">

[![][back-to-top]](#readme-top)

</div>

<!-- ============================================ -->

#### Future Plans

- [ ] **Image/Text Short Video Content Analysis and Viral Content Breakdown**
- [ ] **Search for Similar Image/Text/Video**
- [ ] **Card Image/Text Content Generation**
- [ ] **Short Video Content Editing**

<div align="right">

[![][back-to-top]](#readme-top)

</div>

---

<!-- ============================================ -->

### 🤖 Installation

#### File Structure Introduction

**QMedia services:**
Depending on resource availability, they can be deployed locally or the model services can be deployed in the cloud

#### **[mm_server Installation](./mm_server/README.md)**

- Multimodal Model Service `mm_server`:

  - Multimodal model deployment and API calls
  - Ollama LLM models
  - Image models
  - Video models
  - Feature embedding models

    <br/>

#### **[mmrag_server Installation](./mmrag_server/README.md)**

- Content Search and Q&A Service `mmrag_server`:

  - Content Card Display and Query
  - Image/Text/Short Video Content Extraction, Embedding, and Storage Service
  - Multimodal Data RAG Retrieval Service
  - Content Q&A Service

    <br/>

#### **[qmedia_web Installation](./qmedia_web/README.md)**

- Web Service `qmedia_web`:
  Language: TypeScript
  Framework: Next.js
  Styling: Tailwind CSS
  Components: shadcn/ui

<div align="right">

[![][back-to-top]](#readme-top)

</div>

---

### ⭐️ Usage

#### **Combined Usage**

`mm_server` + `qmedia_web` + `mmrag_server`
Web Page Content Display, Content RAG Search and Q&A, Model Service

1. Service Startup Process:

```bash
# Start mm_server service
cd mm_server
source activate qllm
python main.py

# Start mmrag_server service
cd mmrag_server
source activate qmedia
python main.py

# Start qmedia_web service
cd qmedia_web
pnpm dev
```

2. Using Functions via the Web Page
   During the startup phase, `mmrag_server` will read pseudo data from `assets/medias` and `assets/mm_pseudo_data.json`, and call `mm_server` to extract and structure the information from text/image and short videos into `node` information, which is then stored in the `db`. The retrieval and Q&A will be based on the data in the `db`.

#### Custom Data

```bash
# assets file structure
assets
├── mm_pseudo_data.json # Content card data
└── medias # Image/Video files
```

Replace the contents in `assets` and delete the historically stored `db` file.
`assets/medias` contains image/video files, which can be replaced with your own image/video files.
`assets/mm_pseudo_data.json` contains content card data, which can be replaced with your own content card data. After running the service, the model will automatically extract the information and store it in the `db`.

<div align="right">

[![][back-to-top]](#readme-top)

</div>

---

#### **Independent Model Service**

Can use the `mm_server` local image/text/video information extraction service independently.
It can be used as a standalone image encoding, text encoding, video transcription extraction, and image OCR service, accessible via API in any scenario.

```bash
# Start mm_server service independently
cd mm_server
python main.py

# uvicorn main:app --reload --host localhost --port 50110
```

API Content:

- http://localhost:50110/docs

![alt text](/docs/images/api2.png)

<br/>

#### **Pure Python RAG Service/Model Service**

Can use `mm_server` + `qmedia_web` together to perform content extraction and RAG retrieval in a pure Python environment via APIs.

```bash
# Start mmrag_server service independently
cd mmrag_server
python main.py

# uvicorn main:app --reload --host localhost --port 50110
```

API Content:

- http://localhost:50110/docs
- http://localhost:8001/docs

![alt text](/docs/images/api1.png)

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
[share-x-link]: https://twitter.com/intent/tweet?url=https://github.com/QmiAI/Qmedia&text=Qmedia%0AAn%20open-source%20AI%20content%20search%20engine%20designed%20specifically%20for%20content%20creators.%0ASupports%20extraction%20of%20text,%20images,%20and%20short%20videos.%0AAllows%20full%20local%20deployment%20(web%20app,%20RAG%20server,%20LLM%20server).%0ASupports%20multi-modal%20RAG%20content%20QA.
