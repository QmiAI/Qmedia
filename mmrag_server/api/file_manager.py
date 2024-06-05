import logging
import random
import uuid
from datetime import datetime
from typing import List, Optional

from core.logger import Log
from fastapi import APIRouter, File, Form, HTTPException, UploadFile
from models.models import ApiResponse, NoteData
from pydantic import BaseModel
from services.dbservice.dbservice import DataBaseManager
from utils.response import resp_error, resp_success

router = APIRouter()
DBManager = DataBaseManager()


class CreateDBResponse(BaseModel):
    db_id: str
    db_name: str
    timestamp: str


class CreateDBRequest(BaseModel):
    user_id: str
    db_name: str


@router.post("/create_db", response_model=ApiResponse[CreateDBResponse])
async def create_db(request: CreateDBRequest):
    # TAG: Request Received
    Log.info("Received request: %s", request)
    user_id = request.user_id
    db_name = request.db_name
    default_db_id = "db" + uuid.uuid4().hex
    db_id = default_db_id

    # TAG: Creating Data Base
    Log.info("Creating Data base with ID: %s for user: %s", db_id, user_id)

    # TAG: Check Database Existence
    not_exist_db_ids = DBManager.check_db_exist(user_id, [db_id])
    if not not_exist_db_ids:
        # TAG: Database Exists
        Log.warning("Database %s already exists for user %s", db_id, user_id)
        raise HTTPException(status_code=400, detail="Database already exists")

    _db_id, _status = DBManager.new_db(db_id=db_id, user_id=user_id, db_name=db_name)
    timestamp = datetime.now().strftime("%Y%m%d%H%M")

    # TAG: Data Base Created
    Log.info("New Data base created with ID: %s, status: %s", _db_id, _status)

    resp_data = CreateDBResponse(db_id=db_id, db_name=db_name, timestamp=timestamp)
    Log.info("Resp %s", resp_data)

    # TAG: Data Frames
    Log.debug("Data base data frame: %s", DBManager.db_df)
    Log.debug("Users data frame: %s", DBManager.users_df)

    # TAG: Response Success
    return resp_success(msg=f"success create Data base {db_id}", data=resp_data, code=0)


class FileData(BaseModel):
    file_id: str
    file_name: str
    status: str
    bytes: int
    timestamp: str


@router.post("/upload_files", response_model=ApiResponse[List[FileData]])
async def upload_files(
    user_id: str = Form(),
    db_id: str = Form(),
    file_names: List[str] = Form(),
    files: List[UploadFile] = File(...),
):

    timestamp = datetime.now().strftime("%Y%m%d%H%M")
    local_files = []
    data = []

    for file, file_name in zip(files, file_names):
        file_id, msg = DBManager.add_file(user_id, db_id, file_name, timestamp)
        # Log.info(file_id, msg)

        # print(DBManager.files_df)
        _state = DBManager.update_file_path(file_id, file.filename)
        local_files.append(file.filename)

        file_content = await file.read()
        with open(f"/tmp/{str(random.randint(0, 1000))}.jpg", "wb+") as f:
            f.write(file_content)

        file_data = FileData(
            file_id=file_id,
            file_name=file_name,
            status="gray",
            bytes=len(file_content),
            timestamp=timestamp,
        )

        data.append(file_data)
    Log.info(data)

    return resp_success(msg="Files uploaded successfully", data=data, code=200)


class DataBase(BaseModel):
    db_id: str
    db_name: str


class ListDBsRequest(BaseModel):
    user_id: str


@router.post("/list_dbs", response_model=ApiResponse[List[DataBase]])
async def list_dbs(request: ListDBsRequest):
    user_id = request.user_id

    dbs: List = DBManager.get_dbs(user_id)
    if not dbs:
        raise HTTPException(status_code=404, detail="No Data bases found")

    db_data = [DataBase(db_id=db[0], db_name=db[1]) for db in dbs]

    logging.info(db_data)

    return resp_success(msg="", data=db_data)


class FileInfo(BaseModel):
    file_id: str
    file_name: str
    status: str
    file_size: int
    content_length: int
    timestamp: str


class ListDocsRequest(BaseModel):
    user_id: str
    db_id: str


@router.post("/list_docs", response_model=ApiResponse[List[FileInfo]])
async def list_docs(request: ListDocsRequest):
    user_id = request.user_id
    db_id = request.db_id
    files = DBManager.get_files(user_id, db_id)
    logging.info(files)

    file_infos = [
        FileInfo(
            file_id=file[0],
            file_name=file[1],
            status=file[2],
            file_size=file[3],
            content_length=file[4],
            timestamp=file[5],
        )
        for file in files
    ]
    logging.info(file_infos)
    return file_infos


class AddDocumentRequest(BaseModel):
    docstore_id: str
    chunk_id: int
    file_id: str
    file_name: str
    db_id: str


@router.post("/add_document", response_model=ApiResponse)
async def add_document(request: AddDocumentRequest):
    docstore_id = request.docstore_id
    chunk_id = request.chunk_id
    file_id = request.file_id
    file_name = request.file_name
    db_id = request.db_id

    DBManager.add_document(
        docstore_id=docstore_id,
        chunk_id=chunk_id,
        file_id=file_id,
        file_name=file_name,
        db_id=db_id,
    )

    return resp_success(msg="Document added successfully", data={})


class DeleteDocsRequest(BaseModel):
    file_ids: List[str]


@router.post("/delete_docs", response_model=ApiResponse[list[str]])
async def delete_docs(request: DeleteDocsRequest):
    file_ids = request.file_ids
    doc_ids = DBManager.get_documents_by_file_ids(file_ids)

    if not doc_ids:
        raise HTTPException(status_code=404, detail="Documents not found")

    DBManager.delete_files(file_ids)
    return resp_success(msg="Documents deleted successfully", data=doc_ids)


class DeleteDataBaseRequest(BaseModel):
    user_id: str
    db_ids: List[str]


@router.post("/delete_db", response_model=ApiResponse[list[str]])
async def delete_db(request: DeleteDataBaseRequest):
    user_id = request.user_id
    db_ids = request.db_ids

    DBManager.delete_db(user_id, db_ids)

    return resp_success(msg="Data bases deleted successfully", data=db_ids)


@router.post("/clean_files_by_status", response_model=ApiResponse[list[FileData]])
async def clean_files_by_status(
    user_id: str = Form(...), status: str = Form(...), db_ids: List[str] = Form(...)
):
    files = DBManager.get_file_by_status(db_ids, status)

    if not files:
        raise HTTPException(
            status_code=404, detail="No files found with the given status"
        )

    data = [FileData.model_validate(file) for file in files]

    return resp_success(msg="Files retrieved successfully", data=data)


class BotResponse(BaseModel):
    bot_id: str
    status: str


class BotRequest(BaseModel):
    user_id: str
    bot_name: str
    description: str
    head_image: str
    prompt_setting: str
    welcome_message: str
    model: str
    db_ids: List[str]


@router.post("/new_bot", response_model=ApiResponse[BotResponse])
async def new_bot(request: BotRequest):
    user_id = request.user_id
    bot_name = request.bot_name
    description = request.description
    head_image = request.head_image
    prompt_setting = request.prompt_setting
    welcome_message = request.welcome_message
    model = request.model
    db_ids = request.db_ids

    bot_id = "BOT" + uuid.uuid4().hex
    db_ids_str = ",".join(db_ids)

    bot_id, status = DBManager.new_bot(
        bot_id,
        user_id,
        bot_name,
        description,
        head_image,
        prompt_setting,
        welcome_message,
        model,
        db_ids_str,
    )

    response_data = BotResponse(bot_id=bot_id, status=status)

    return resp_success(msg="Bot created successfully", data=response_data)


class DeleteBotResponse(BaseModel):
    bot_id: str
    status: str


class DeleteBotRequent(BaseModel):
    user_id: str
    bot_id: str


@router.post("/delete_bot", response_model=ApiResponse[DeleteBotResponse])
async def delete_bot(request: DeleteBotRequent):
    user_id = request.user_id
    bot_id = request.bot_id

    DBManager.delete_bot(user_id, bot_id)

    response_data = DeleteBotResponse(bot_id=bot_id, status="success")

    return resp_success(msg="Bot dele bot successfully", data=response_data)


class UpdateBotResponse(BaseModel):
    bot_id: str
    status: str


class UpdateBotRequest(BaseModel):
    user_id: str
    bot_id: str
    bot_name: str
    description: str
    head_image: str
    prompt_setting: str
    welcome_message: str
    model: str
    db_ids: List[str]


@router.post("/update_bot", response_model=ApiResponse[UpdateBotResponse])
async def update_bot(request: UpdateBotRequest):
    user_id = request.user_id
    bot_id = request.bot_id
    bot_name = request.bot_name
    description = request.description
    head_image = request.head_image
    prompt_setting = request.prompt_setting
    welcome_message = request.welcome_message
    model = request.model
    db_ids = request.db_ids

    update_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    db_ids_str = ",".join(db_ids)

    DBManager.update_bot(
        user_id,
        bot_id,
        bot_name,
        description,
        head_image,
        prompt_setting,
        welcome_message,
        model,
        db_ids_str,
        update_time,
    )

    response_data = {"bot_id": bot_id, "status": "success"}

    return resp_success(data=UpdateBotResponse(**response_data))
