import json

import requests
from llama_index.core.multi_modal_llms.generic_utils import (
    encode_image,
    image_documents_to_base64,
)
from pydantic import BaseModel
from rich import print


def test_embeddings():
    prompt = "test prompt"
    model_name = "bge"
    base_url = "http://localhost:50110"

    request_body = {
        "prompt": prompt,
        "model": model_name,
    }

    response = requests.post(
        url=f"{base_url}/api/embeddings",
        headers={"Content-Type": "application/json"},
        json=request_body,
    )

    print(response)
    print(response.json().keys())


def clip_image_embeddings(image_path: str):
    if image_path is None:
        image_path = "../docs/images/image-1.png"
    model_name = "clip"
    base_url = "http://localhost:50110"

    request_body = {"model": model_name, "image": encode_image(image_path)}

    response = requests.post(
        url=f"{base_url}/api/clip-image-embeddings",
        headers={"Content-Type": "application/json"},
        json=request_body,
    )

    print(response)
    print(response.json())


def clip_text_embeddings():
    model_name = "clip"
    base_url = "http://localhost:50110"
    prompt = "hello "

    request_body = {"model": model_name, "prompt": prompt}

    response = requests.post(
        url=f"{base_url}/api/clip-text-embeddings",
        headers={"Content-Type": "application/json"},
        json=request_body,
    )

    print(response)
    print(response.json())


def image_ocr(image_path):
    if image_path is None:
        image_path = "../docs/images/image-1.png"
    model_name = "ocr"
    base_url = "http://localhost:50110"

    request_body = {"model": model_name, "image": encode_image(image_path)}

    response = requests.post(
        url=f"{base_url}/api/image-ocr",
        headers={"Content-Type": "application/json"},
        json=request_body,
    )

    print(response)
    print(response.json())


baseUrl = "http://127.0.0.1:8001"


def test_build_databse():
    # 构建检索数据库
    url = f"{baseUrl}/embedding-mm"
    response = requests.get(url)
    print(response.status_code)
    print(response.json())


def test_notes_search():
    # note search
    query = "how to vlog"
    url = f"{baseUrl}/mm-rag-search?query={query}"

    response = requests.get(url)

    print(response.status_code)
    print(response.json())


def test_notes_query():
    query = "how to vlog"
    url = f"{baseUrl}/mm-rag-query?query={query}"

    response = requests.get(url)
    print(response.status_code)
    print(response.json())


def lifecycle_clip_image_embeddings(image_path: str):
    if image_path is None:
        image_path = "../docs/images/image-1.png"
    model_name = "clip"
    base_url = "http://localhost:8000"

    request_body = {"model": model_name, "image": encode_image(image_path)}

    response = requests.post(
        url=f"{base_url}/api/clip-image-embeddings",
        headers={"Content-Type": "application/json"},
        json=request_body,
    )

    print(response)
    print(response.json())


def set_model():
    # 设置请求的URL
    url = "http://localhost:50110/api/set-keep-alive"

    # 设置请求的数据
    data = {
        "model_name": "all",
        "keep_alive": 100,  # 设置持有时间为600秒
        "hold_forever": False,  # 设置为非永久持有
    }

    # 发送POST请求
    response = requests.post(url, json=data)

    # 打印响应
    print(response.json())


def lifecycle_set_model():
    # 设置请求的URL
    url = "http://localhost:8000/api/set-model-config"

    # 设置请求的数据
    data = {
        "hold_time": 5,  # 设置持有时间为600秒
        "hold_forever": False,  # 设置为非永久持有
    }

    # 发送POST请求
    response = requests.post(url, json=data)

    # 打印响应
    print(response.json())


if __name__ == "__main__":
    image_path = "../assets/medias/6370c90a000000001501704b_0.jpg"
    # lifecycle_clip_image_embeddings(image_path)

    # test_build_databse()
    # test_notes_search()
    # test_notes_query()
    # image_ocr(image_path)
    clip_image_embeddings(image_path)
    # clip_text_embeddings()
    # test_embeddings()

    # set_model()
    # lifecycle_set_model()
