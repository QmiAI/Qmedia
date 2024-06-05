import logging

import uvicorn
from api import mm_rag_search, note_view, rag_search, search
from config import Config
from fastapi import FastAPI, Request, status
from fastapi.exceptions import RequestValidationError
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from fastapi.staticfiles import StaticFiles

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(note_view.router, tags=["note"])
app.include_router(search.router, tags=["public_search"])
app.include_router(rag_search.router, tags=["search"])
app.include_router(mm_rag_search.router, tags=["mm_search"])
app.mount("/medias", StaticFiles(directory=Config.local_store_path), name="medias")


@app.get("/")
async def read_root():
    return JSONResponse(content={"msg": "Access success."})


async def on_startup():
    await mm_rag_search.embedding_mm(embed_mode="auto")


app.add_event_handler("startup", on_startup)


@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    exc_str = f"{exc}".replace("\n", " ").replace("   ", " ")
    logging.error(f"{request}: {exc_str}")
    content = {"status_code": 10422, "message": exc_str, "data": None}
    return JSONResponse(
        content=content, status_code=status.HTTP_422_UNPROCESSABLE_ENTITY
    )


if __name__ == "__main__":
    uvicorn.run(app, host=Config.server_host, port=Config.server_port)
