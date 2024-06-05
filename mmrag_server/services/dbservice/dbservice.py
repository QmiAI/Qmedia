import uuid
from datetime import datetime
from pathlib import Path
from typing import List, Optional

import pandas as pd
from config import Config
from pydantic import BaseModel, Field


class DataBaseManager:
    def __init__(self):
        self.db_df = self.load_or_create_df(
            Config.db_path / "db.csv", ["db_id", "user_id", "db_name", "deleted"]
        )
        self.users_df = self.load_or_create_df(
            Config.db_path / "users.csv", ["user_id", "user_name"]
        )
        self.files_df = self.load_or_create_df(
            Config.db_path / "files.csv",
            [
                "file_id",
                "db_id",
                "file_name",
                "status",
                "timestamp",
                "file_path",
                "file_size",
                "deleted",
            ],
        )
        self.documents_df = self.load_or_create_df(
            Config.db_path / "documents.csv",
            ["docstore_id", "chunk_id", "file_id", "file_name", "db_id"],
        )
        self.bot_df = self.load_or_create_df(
            Config.db_path / "bot.csv",
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
            ],
        )
        self.faq_df = self.load_or_create_df(
            Config.db_path / "faq.csv",
            ["faq_id", "user_id", "db_id", "question", "answer", "nos_keys"],
        )

    def load_or_create_df(self, file_path: Path, columns: List):
        if file_path.exists():
            return pd.read_csv(file_path)
        else:
            return pd.DataFrame(columns=columns)

    def new_db(self, db_id, user_id, db_name, user_name=None):
        if not self.check_user_exist(user_id):
            self.add_user(user_id, user_name)
        # 添加新的知识库记录到DataFrame
        new_db_entry = pd.DataFrame(
            {
                "db_id": [db_id],
                "user_id": [user_id],
                "db_name": [db_name],
                "deleted": [0],
            }
        )
        self.db_df = pd.concat([self.db_df, new_db_entry], ignore_index=True)
        return db_id, "success"

    def check_user_exist(self, user_id):
        # 检查用户是否存在
        return not self.users_df[self.users_df["user_id"] == user_id].empty

    def check_db_exist(self, user_id: str, db_ids: List[str]) -> List[str]:
        # 筛选出未删除且属于指定用户的知识库条目
        valid_entries = self.db_df[
            (self.db_df["user_id"] == user_id)
            & (self.db_df["deleted"] == 0)
            & (self.db_df["db_id"].isin(db_ids))
        ]

        # 获取有效的db_id列表
        valid_db_ids = valid_entries["db_id"].tolist()

        # 计算无效的db_id列表
        unvalid_db_ids = list(set(db_ids) - set(valid_db_ids))
        return unvalid_db_ids

    def add_user(self, user_id, user_name=None):
        # 添加新用户到DataFrame
        new_user_entry = pd.DataFrame({"user_id": [user_id], "user_name": [user_name]})
        self.users_df = pd.concat([self.users_df, new_user_entry], ignore_index=True)
        return user_id

    def add_file(
        self, user_id: str, db_id: str, file_name: str, timestamp: str, status="gray"
    ):
        if not self.check_user_exist(user_id):
            return None, "invalid user_id, please check..."
        # not_exist_db_ids = self.check_db_exist(user_id, [db_id])
        # if not_exist_db_ids:
        # return None, f"invalid db_id, please check {not_exist_db_ids}"

        file_id = uuid.uuid4().hex
        # 使用pandas添加文件信息
        # self.files_df.loc[len(self.files_df)] = [file_id, db_id, file_name, status, timestamp, None]
        new_user_entry = pd.DataFrame(
            {
                "file_id": [file_id],
                "db_id": [db_id],
                "file_name": [file_name],
                "status": [status],
                "timestamp": [timestamp],
                "deleted": [0],
            }
        )
        self.files_df = pd.concat([self.files_df, new_user_entry], ignore_index=True)

        return file_id, "success"

    def update_file_path(self, file_id, file_path):
        # 找到对应file_id的行索引
        file_index = self.files_df[self.files_df["file_id"] == file_id].index

        # 如果找到了对应的文件记录
        if not file_index.empty:
            # 确保file_index只包含一个元素，然后使用.at[]更新
            if len(file_index) == 1:
                self.files_df.at[file_index.item(), "file_path"] = file_path
            else:
                # 如果file_index包含多个元素，使用.loc[]更新
                self.files_df.loc[file_index, "file_path"] = file_path
            return "success"
        else:
            return "file_id not found"

    def get_dbs(self, user_id) -> List:
        # 筛选出指定用户且未删除的知识库
        user_dbs = self.db_df[
            (self.db_df["user_id"] == user_id) & (self.db_df["deleted"] == 0)
        ][["db_id", "db_name"]]

        # 将结果转换为列表格式
        result = user_dbs.values.tolist()
        return result

    def get_files(self, user_id, db_id):
        # 检查给定的db_id是否属于给定的user_id且未被删除
        valid_db = self.db_df[
            (self.db_df["db_id"] == db_id)
            & (self.db_df["user_id"] == user_id)
            & (self.db_df["deleted"] == 0)
        ]

        if valid_db.empty:
            return None, "invalid db_id or user_id, please check..."

        # 获取指定知识库下未被删除的文件
        files = self.files_df[
            (self.files_df["db_id"] == db_id) & (self.files_df["deleted"] == 0)
        ]  # [['file_id', 'file_name', 'status', 'file_size', 'content_length', 'timestamp']]

        # 将结果转换为列表格式
        result = files.values.tolist()
        return result

    def add_document(self, docstore_id, chunk_id, file_id, file_name, db_id):
        new_document = pd.DataFrame(
            [
                {
                    "docstore_id": docstore_id,
                    "chunk_id": chunk_id,
                    "file_id": file_id,
                    "file_name": file_name,
                    "db_id": db_id,
                }
            ]
        )
        self.documents_df = pd.concat(
            [self.documents_df, new_document], ignore_index=True
        )

    # faiss 删除
    # 数据库删除
    def get_documents_by_file_ids(self, file_id):
        # 使用 Pandas DataFrame 查询指定文件ID的文档
        result = self.documents_df[self.documents_df["file_id"].isin(file_id)][
            "docstore_id"
        ].tolist()
        return result

    def delete_files(self, kb_id, file_ids):
        # 使用 Pandas DataFrame 更新 File 表中的删除状态
        self.files_df.loc[
            (self.files_df["kb_id"] == kb_id)
            & (self.files_df["file_id"].isin(file_ids)),
            "deleted",
        ] = 1

    def delete_db(self, user_id, db_ids):
        # 更新 KnowledgeBase 表中的删除状态
        self.db_df.loc[
            (self.db_df["user_id"] == user_id) & (self.db_df["db_id"].isin(db_ids)),
            "deleted",
        ] = 1

        # 更新 File 表中的删除状态
        self.files_df.loc[
            (self.files_df["db_id"].isin(db_ids))
            & (
                self.files_df["db_id"].isin(
                    self.db_df[self.db_df["user_id"] == user_id]["db_id"]
                )
            ),
            "deleted",
        ] = 1

    def get_file_by_status(self, db_ids, status):
        # 使用 Pandas DataFrame 查询指定知识库ID和状态的文件
        result = self.files_df[
            (self.files_df["db_id"].isin(db_ids))
            & (self.files_df["deleted"] == 0)
            & (self.files_df["status"] == status)
        ][["file_id", "file_name"]].to_dict(orient="records")
        return result

    def new_bot(
        self,
        bot_id,
        user_id,
        bot_name,
        description,
        head_image,
        prompt_setting,
        welcome_message,
        model,
        db_ids_str,
    ):
        new_bot = pd.DataFrame(
            [
                {
                    "bot_id": bot_id,
                    "user_id": user_id,
                    "bot_name": bot_name,
                    "description": description,
                    "head_image": head_image,
                    "prompt_setting": prompt_setting,
                    "welcome_message": welcome_message,
                    "model": model,
                    "db_ids_str": db_ids_str,
                    "deleted": 0,
                    "create_time": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                    "update_time": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                }
            ]
        )

        self.bot_df = pd.concat([self.bot_df, new_bot], ignore_index=True)
        return bot_id, "success"

    def delete_bot(self, user_id, bot_id):
        # 使用 Pandas DataFrame 更新表中的删除状态
        self.bot_df.loc[
            (self.bot_df["user_id"] == user_id) & (self.bot_df["bot_id"] == bot_id),
            "deleted",
        ] = 1

    def update_bot(
        self,
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
    ):
        # 使用 Pandas DataFrame 更新表中的信息
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
