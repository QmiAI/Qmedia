import uvicorn
from api import cached_service, embed_service, image_service, video_service
from config import Config
from fastapi import FastAPI

app = FastAPI()


def include_routers():
    app.include_router(image_service.router, tags=["image process"])
    app.include_router(video_service.router, tags=["video process"])
    app.include_router(embed_service.router, tags=["embeddings"])
    app.include_router(cached_service.router, tags=["set model cached"])


def main():
    print(" @ Run mm server")
    include_routers()
    uvicorn.run(app, host=Config.server_host, port=Config.server_port)


if __name__ == "__main__":
    main()
