## mm_server 模型服务安装说明

**简体中文** | [English](./README.md)

#### 环境安装

可以使用[miniconda](https://docs.anaconda.com/free/miniconda/miniconda-install/) 轻量安装 python conda 环境

```bash
# 安装虚拟环境
conda create -n qllm python==3.11
source activate qllm

cd mm_server

#安装 python 依赖环境
pip install -r requirements.txt
```

<br/>

#### 修改配置文件

编辑模型配置项:

```
cp config.py.local config.py
```

根据使用情况修改 config.py 配置文件

- clip_model_name: 视觉编码模型, 文本编码模型
- ocr_model_path: ocr 文字识别模型
- hf_embedding_model_name: 文本编码模型
- audio_model_name: 视频转文案模型

```python
@dataclass
class Configer:
    # mm server host
    server_host = "localhost"
    server_port = 50110

    # image encoder model name
    clip_model_name = "ViT-B/32"
    # model keep alive time (s)
    clip_keep_alive = 60

    # ocr model path
    ocr_model_path = str(TEMPLATE_PATH / "services/ocr_server/ocr_models")
    # model keep alive time (s)
    ocr_keep_alive = 60

    # text embedding model name
    hf_embedding_model_name = "BAAI/bge-small-en-v1.5"
    # model keep alive time (s)
    hf_keep_alive = 60

    # video transcription  model name
    audio_model_name = "small"
    # model keep alive time (s)
    video_keep_alive = 1

```

#### 运行服务

```bash
source activate qllm
python main.py

# reload 模式, 修改代码后热更新
# uvicorn main:app --reload --host localhost --port 50110
```

<br/>

#### 本地 ollama 模型部署

Install ollama 参考:

- https://ollama.com/download/mac

**本地模型启动**
本地模型选择 8b, 效果会有损失

```bash
# 本地版本:
ollama run llama3:8b-instruct-q4_0
```

**(可选) 本地 70B 大模型**
服务器可选择 70b 大模型版本, 需要同时修改`mmrag_server/config.py` 中的 `model_name`

```bash
# 远端服务器版本:
ollama run llama3:70b-instruct
```

**(可选)模型生命周期管理**
当前 ollama 会自动释放模型, 5min 不使用则释放模型, 再次访问时重启模型, 如果需要长期持有可按照以下教程配置

- 持续时间字符串（例如“10m”或“24h”）
- 以秒为单位的数字（例如 3600）
- 模型永久保持: 任何将模型加载到内存中的负数（例如-1 或“-1m”）
- 释放模型: “0”将在生成响应后立即卸载模型

```bash
# 永久持有
curl http://localhost:11434/api/generate -d '{"model": "模型名称", "keep_alive": -1}'

# 卸载
curl http://localhost:11434/api/generate -d '{"model": "模型名称", "keep_alive": 0}'

# 设定自动释放时间
curl http://localhost:11434/api/generate -d '{"model": "模型名称", "keep_alive": 3600}'

```

<!-- 模型将模型保存在内存或立即卸载
The keep_alive parameter can be set to:keep_alive 参数可以设置为：

- a duration string (such as "10m" or "24h")
- a number in seconds (such as 3600)
- any negative number which will keep the model loaded in memory (e.g. -1 or "-1m")
- '0' which will unload the model immediately after generating a response“0”将在生成响应后立即卸载模型 -->

#### 模型选配置

- 长文本:[ 524k llama3 版本 ](https://ollama.com/pxlksr/llama-3-70b-instruct-gradient-524k)

- 高质量 LLM 开源模型: [Llama-3-70b-Instruct](https://ollama.com/library/llama3:70b-instruct)
- 高质量小模型: [llama3:8b-instruct](https://ollama.com/library/llama3:8b-instruct-q4_0)

- 文本 embedding 模型: [bge-small](https://huggingface.co/BAAI/bge-small-en-v1.5)
- 图片 embedding 模型: [CLIP](https://github.com/openai/CLIP)

- [llm 榜单](https://chat.lmsys.org/?leaderboard)

<br/>

#### api 文档:

http://localhost:50110/docs

![alt text](../docs/images/api2.png)

<!--  -->
<div align="right">

[![][back-to-top]](../README.zh-CN.md)

</div>

[back-to-top]: https://img.shields.io/badge/-BACK_TO_TOP-151515?style=flat-square
