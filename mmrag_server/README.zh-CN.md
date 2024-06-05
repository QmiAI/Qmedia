## mmrag_server 安装说明

**简体中文** | [English](./README.md)

#### 环境安装

可以使用[miniconda](https://docs.anaconda.com/free/miniconda/miniconda-install/) 轻量安装 python conda 环境

```bash
# 安装虚拟环境
conda create -n qmedia python==3.11
source activate qmedia

cd mmrag_server

# 安装 python 依赖环境
pip install -r requirements.txt
```

<br/>

#### 修改 配置文件

编辑模型配置项:

```
cp config.py.local config.py
```

根据使用情况修改 config.py 配置文件

- use_video_service: 是否使用 视频服务, 默认关闭
- use_google_search: 是否使用 google 搜索服务

```python
@dataclass
class Configer:
    server_host = "localhost"
    server_port = 8001

    # ollama llm model name
    model_name = "llama3:8b-instruct-q4_0"
    # note: Large models can be used remotely
    # model_name = "llama3:70b-instruct"

    # multi model llm model
    mm_model_name = "llava-llama3"

    # ollama llm model host:port
    ollama_url = "http://localhost:11434"

    # mm_server host:port
    mm_server_url = "http://localhost:50110"

    # text embedding model
    embedding_model_name = "BAAI/bge-small-en-v1.5"

    store_host = "http://localhost:8001/medias"
    # pseudo data path
    json_file_path = str(TEMPLATE_PATH / "mm_pseudo_data.json")
    local_store_path = str(TEMPLATE_PATH / "medias")

    similarities_thre = 0.6

    # embedding storage path
    db_path = str(DB_PATH)
    db_index_id = "v1"
    docs_persist_path = str(DB_PATH / "docstore.json")

    # image embedding model
    clip_model_name = "ViT-B/32"

    # ocr model server
    ocr_model_name = "ocr"
    ocr_reader_base_url = mm_server_url

    # use video service
    use_video_service = False
    video_model_name = "faster_whisper"
    video_reader_base_url = mm_server_url

    # use google search
    use_google_search = False
```

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

#### 运行服务

需要依赖 [mm_server](../mm_server/README.zh-CN.md) 服务运行

```bash
source activate qmedia
python main.py

# reload 模式, 修改代码后热更新
# uvicorn main:app --reload --host localhost --port 8001
```

#### api 文档:

http://localhost:8001/docs
![alt text](../docs/images/api1.png)

<br/>

<div align="right">

[![][back-to-top]](../README.zh-CN.md)

</div>

[back-to-top]: https://img.shields.io/badge/-BACK_TO_TOP-151515?style=flat-square
