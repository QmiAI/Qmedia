import uuid
from datetime import datetime
from pathlib import Path
from typing import List, Optional

import pandas as pd
from pydantic import BaseModel, Field


# 定义数据模型
class User(BaseModel):
    user_id: str
    user_name: Optional[str]


class DB(BaseModel):
    db_id: str
    user_id: str
    db_name: str
    deleted: int = 0


class File(BaseModel):
    file_id: str
    db_id: str
    file_name: str
    status: str
    timestamp: str
    file_path: Optional[str]
    file_size: Optional[int]
    deleted: int = 0


class LocalDocument(BaseModel):
    docstore_id: str
    chunk_id: str
    file_id: str
    file_name: str
    db_id: str


class Bot(BaseModel):
    bot_id: str
    user_id: str
    bot_name: str
    description: str
    head_image: str
    prompt_setting: str
    welcome_message: str
    model: str
    db_ids_str: str
    deleted: int = 0
    create_time: str
    update_time: str


# 修改后的DataFrameManager和相关管理类
class DataFrameManager:
    def __init__(self, db_path: Path, file_name: Path):
        self.db_path = db_path
        self.file_name = file_name

    def load_or_create_df(self, columns: List[str]) -> pd.DataFrame:
        file_path = self.db_path / self.file_name
        if file_path.exists():
            return pd.read_csv(file_path)
        else:
            return pd.DataFrame(columns=columns)

    def save_df(self, df: pd.DataFrame, file_name: str):
        file_path = self.db_path / file_name
        df.to_csv(file_path, index=False)


class UserManager(DataFrameManager):
    def __init__(self, db_path: Path, file_name: Path):
        super().__init__(db_path, file_name)
        self.users_df = self.load_or_create_df(["user_id", "user_name"])

    def add_user(self, user: User):
        new_user_entry = pd.DataFrame([user.model_dump()])
        self.users_df = pd.concat([self.users_df, new_user_entry], ignore_index=True)
        self.save_df(self.users_df, self.file_name)
        return user.user_id

    def check_user_exist(self, user_id: str) -> bool:
        return not self.users_df[self.users_df["user_id"] == user_id].empty


class DBManager(DataFrameManager):
    def __init__(self, db_path: Path, user_manager: UserManager, file_name: Path):
        super().__init__(db_path, file_name)
        self.db_df = self.load_or_create_df(["db_id", "user_id", "db_name", "deleted"])
        self.user_manager = user_manager

    def new_db(self, db: DB):
        if not self.user_manager.check_user_exist(db.user_id):
            self.user_manager.add_user(User(user_id=db.user_id, user_name=None))
        new_db_entry = pd.DataFrame([db.model_dump()])
        self.db_df = pd.concat([self.db_df, new_db_entry], ignore_index=True)
        self.save_df(self.db_df, self.file_name)
        return db.db_id, "success"

    def check_db_exist(self, user_id: str, db_ids: List[str]) -> List[str]:
        valid_entries = self.db_df[
            (self.db_df["user_id"] == user_id)
            & (self.db_df["deleted"] == 0)
            & (self.db_df["db_id"].isin(db_ids))
        ]
        valid_db_ids = valid_entries["db_id"].tolist()
        unvalid_db_ids = list(set(db_ids) - set(valid_db_ids))
        return unvalid_db_ids

    def get_dbs(self, user_id: str) -> List:
        user_dbs = self.db_df[
            (self.db_df["user_id"] == user_id) & (self.db_df["deleted"] == 0)
        ][["db_id", "db_name"]]
        result = user_dbs.values.tolist()
        return result

    def delete_db(self, user_id: str, db_ids: List[str]):
        self.db_df.loc[
            (self.db_df["user_id"] == user_id) & (self.db_df["db_id"].isin(db_ids)),
            "deleted",
        ] = 1
        self.save_df(self.db_df, self.file_name)


class FileManager:
    def __init__(
        self,
        df_manager: DataFrameManager,
        db_manager: DBManager,
        user_manager: UserManager,
        file_name: Path,
    ):
        self.files_df = df_manager.load_or_create_df(
            [
                "file_id",
                "db_id",
                "file_name",
                "status",
                "timestamp",
                "file_path",
                "file_size",
                "deleted",
            ]
        )
        self.db_manager = db_manager
        self.user_manager = user_manager
        self.file_name = file_name

    def add_file(self, user_id: str, file: File):
        if not self.user_manager.check_user_exist(user_id):
            return None, "invalid user_id, please check..."
        new_file_entry = pd.DataFrame([file.model_dump()])
        self.files_df = pd.concat([self.files_df, new_file_entry], ignore_index=True)
        self.save_df(self.files_df, self.file_name)
        return file.file_id, "success"

    def update_file_path(self, file_id: str, file_path: str):
        file_index = self.files_df[self.files_df["file_id"] == file_id].index
        if not file_index.empty:
            if len(file_index) == 1:
                self.files_df.at[file_index.item(), "file_path"] = file_path
            else:
                self.files_df.loc[file_index, "file_path"] = file_path
            self.save_df(self.files_df, self.file_name)
            return "success"
        else:
            return "file_id not found"

    def get_files(self, user_id: str, db_id: str):
        valid_db = self.db_manager.db_df[
            (self.db_manager.db_df["db_id"] == db_id)
            & (self.db_manager.db_df["user_id"] == user_id)
            & (self.db_manager.db_df["deleted"] == 0)
        ]
        if valid_db.empty:
            return None, "invalid db_id or user_id, please check..."
        files = self.files_df[
            (self.files_df["db_id"] == db_id) & (self.files_df["deleted"] == 0)
        ]
        result = files.values.tolist()
        return result

    def delete_files(self, db_id: str, file_ids: List[str]):
        self.files_df.loc[
            (self.files_df["db_id"] == db_id)
            & (self.files_df["file_id"].isin(file_ids)),
            "deleted",
        ] = 1
        self.save_df(self.files_df, self.file_name)

    def get_file_by_status(self, db_ids: List[str], status: str):
        result = self.files_df[
            (self.files_df["db_id"].isin(db_ids))
            & (self.files_df["deleted"] == 0)
            & (self.files_df["status"] == status)
        ][["file_id", "file_name"]].to_dict(orient="records")
        return result


class DocumentManager:
    def __init__(self, df_manager: DataFrameManager, file_name: Path):
        self.documents_df = df_manager.load_or_create_df(
            ["docstore_id", "chunk_id", "file_id", "file_name", "db_id"]
        )
        self.file_name = file_name

    def add_document(self, document: LocalDocument):
        new_document = pd.DataFrame([document.model_dump()])
        self.documents_df = pd.concat(
            [self.documents_df, new_document], ignore_index=True
        )
        self.save_df(self.documents_df, self.file_name)

    def get_documents_by_file_ids(self, file_ids: List[str]) -> List[str]:
        result = self.documents_df[self.documents_df["file_id"].isin(file_ids)][
            "docstore_id"
        ].tolist()
        return result


class BotManager:
    def __init__(
        self, df_manager: DataFrameManager, user_manager: UserManager, file_name: Path
    ):
        self.bot_df = df_manager.load_or_create_df(
            [
                "bot_id",
                "user_id",
                "bot_name",
                "description",
                "head_image",
                "prompt_setting",
                "welcome_message",
                "model",
                "db_ids_str",
                "deleted",
                "create_time",
                "update_time",
            ]
        )
        self.user_manager = user_manager
        self.file_name = file_name

    def new_bot(self, bot: Bot):
        if not self.user_manager.check_user_exist(bot.user_id):
            return None, "invalid user_id, please check..."
        new_bot_entry = pd.DataFrame([bot.model_dump()])
        self.bot_df = pd.concat([self.bot_df, new_bot_entry], ignore_index=True)
        self.save_df(self.bot_df, self.file_name)
        return bot.bot_id, "success"

    def delete_bot(self, user_id: str, bot_id: str):
        self.bot_df.loc[
            (self.bot_df["user_id"] == user_id) & (self.bot_df["bot_id"] == bot_id),
            "deleted",
        ] = 1
        self.save_df(self.bot_df, self.file_name)

    def update_bot(
        self,
        user_id: str,
        bot_id: str,
        bot_name: str,
        description: str,
        head_image: str,
        prompt_setting: str,
        welcome_message: str,
        model: str,
        db_ids_str: str,
        update_time: str,
    ):
        mask = (
            (self.bot_df["user_id"] == user_id)
            & (self.bot_df["bot_id"] == bot_id)
            & (self.bot_df["deleted"] == 0)
        )
        self.bot_df.loc[
            mask,
            [
                "bot_name",
                "description",
                "head_image",
                "prompt_setting",
                "welcome_message",
                "model",
                "db_ids_str",
                "update_time",
            ],
        ] = [
            bot_name,
            description,
            head_image,
            prompt_setting,
            welcome_message,
            model,
            db_ids_str,
            update_time,
        ]
        self.save_df(self.bot_df, self.file_name)

    def get_bots(self, user_id: str) -> List:
        user_bots = self.bot_df[
            (self.bot_df["user_id"] == user_id) & (self.bot_df["deleted"] == 0)
        ][
            [
                "bot_id",
                "bot_name",
                "description",
                "head_image",
                "prompt_setting",
                "welcome_message",
                "model",
                "db_ids_str",
                "create_time",
                "update_time",
            ]
        ]
        result = user_bots.values.tolist()
        return result

    def get_bot_details(self, user_id: str, bot_id: str) -> Optional[Bot]:
        bot_details = self.bot_df[
            (self.bot_df["user_id"] == user_id)
            & (self.bot_df["bot_id"] == bot_id)
            & (self.bot_df["deleted"] == 0)
        ]
        if bot_details.empty:
            return None
        bot_data = bot_details.iloc[0].to_dict()
        return Bot(**bot_data)
