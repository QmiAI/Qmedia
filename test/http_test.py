import requests
from llama_index.core.multi_modal_llms.generic_utils import (
    encode_image,
    image_documents_to_base64,
)
from pydantic import BaseModel
from rich import print

baseUrl = "http://127.0.0.1:8001"


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


def image_embeddings():
    model_name = "clip"
    base_url = "http://localhost:50110"

    request_body = {
        "model": model_name,
        "image": encode_image("../docs/images/query.png"),
    }

    response = requests.post(
        url=f"{base_url}/api/clip-image-embeddings",
        headers={"Content-Type": "application/json"},
        json=request_body,
    )

    print(response)
    print(response.json())


def image_ocr():
    model_name = "ocr"
    base_url = "http://localhost:50110"

    request_body = {
        "model": model_name,
        "image": encode_image("../docs/images/query.png"),
    }

    response = requests.post(
        url=f"{base_url}/api/image-ocr",
        headers={"Content-Type": "application/json"},
        json=request_body,
    )

    print(response)
    print(response.json())


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


if __name__ == "__main__":
    # test_build_databse()
    # test_notes_search()
    # test_notes_query()
    image_ocr()
    # image_embeddings()
    # test_embeddings()
