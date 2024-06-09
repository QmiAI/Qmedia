FROM pytorch/pytorch:2.2.2-cuda12.1-cudnn8-devel

WORKDIR /app

RUN apt-get update && \
    apt-get install -y curl git git-lfs && \
    git-lfs install

COPY ./mmrag_server/. ./

RUN pip install -r /app/requirements.txt


EXPOSE 50111

CMD ["python","main.py"]
