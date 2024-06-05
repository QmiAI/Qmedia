# AudioTranscriptionReader(),
# AudioSummaryReader(),


import os
from dataclasses import Field
from pathlib import Path, PurePosixPath
from typing import Any, Callable, Dict, Generator, List, Optional, Type

import requests
from llama_index.core import Document, Settings
from llama_index.core.base.llms.types import ChatResponse
from llama_index.core.llms import ChatMessage
from llama_index.core.readers.base import BaseReader
from llama_index.core.schema import DEFAULT_METADATA_TMPL, DEFAULT_TEXT_NODE_TMPL
from pydantic import BaseModel

try:
    from moviepy.editor import VideoFileClip
except ImportError:
    raise ImportError(
        "Could not import moviepy library."
        "Please install requests with `pip install moviepy`"
    )


class SentenceSegment(BaseModel):
    id: int
    seek: int
    start: float
    end: float
    text: str


class AudioResponse(BaseModel):
    language: str
    language_probability: float
    duration: float
    duration_after_vad: float
    segments: List[SentenceSegment]


class AudioTranscriptionReader(BaseReader):
    """Image parser."""

    def __init__(
        self,
        model_name,
        base_url,
        parse_summary=True,
        audio_trans=True,
        meta_reader_type=None,
    ):
        """Init parser."""
        self.model_name = model_name
        self.base_url = base_url
        self.use_parse_summary = parse_summary
        self.use_audio_trans = audio_trans
        self.meta_reader_type = meta_reader_type or self.get_reader_type()

    def get_reader_type(self):
        """Return the class name of the instance."""
        return {"reader_type": self.__class__.__name__}

    def _get_text_from_model(self, video_audio_path: str) -> AudioResponse:

        if video_audio_path.endswith(".mp4"):
            video_clip = VideoFileClip(video_audio_path)
            # 获取video_audio_path 的文件名使用Path

            audio_location = Path(video_audio_path).with_suffix(".mp3").as_posix()
            video_clip.audio.write_audiofile(audio_location, codec="mp3")
            video_clip.close()
            video_audio_path = audio_location

        elif not video_audio_path.endswith(".mp3"):
            raise ValueError

        with open(video_audio_path, "rb") as audio_file:
            response = requests.post(
                url=f"{self.base_url}/api/audio_transcription",
                files={"file": audio_file},
                data={"model": self.model_name},
            )

        response.encoding = "utf-8"
        if response.status_code != 200:
            optional_detail = response.json().get("error")
            raise ValueError(
                f"AudioTranscriptionReader call failed with status code {response.status_code}."
                f" Details: {optional_detail}"
            )

        try:
            resp = AudioResponse.model_validate(response.json())
            return resp
        except requests.exceptions.JSONDecodeError as e:
            raise ValueError(
                f"Error raised for AudioTranscriptionReader Call: {e}.\nResponse: {response.text}"
            )

    def _parse_to_summary(self, resp: AudioResponse):

        # 使用GPT模型对resp的内容进行组合和总结的prompt
        prompt = f"""
        我有一个视频对象包含以下信息：
        - 语言: {resp.language}
        - 文案片段的详细信息如下：
        """

        for segment in resp.segments:
            prompt += segment.text

        prompt += """
        请根据上述信息生成一个总结，包含视频的主要内容和关键片段。总结应简洁明了，突出视频的核心信息。
        """
        messages = [
            ChatMessage(role="system", content=prompt),
        ]
        response: ChatResponse = Settings.llm.chat(messages)
        content = str(response)
        return content

    def _parse_to_transcription(self, resp: AudioResponse):
        texts = []
        for segment in resp.segments:
            texts.append(segment.text)
        content = ".".join(texts)
        return content

    def load_data(self, file: str, **load_kwargs: Any) -> List[Document]:
        try:
            if not os.path.exists(file):
                raise FileNotFoundError(f"File '{file}' does not exist.")

            resp: AudioResponse = self._get_text_from_model(file)

            load_kwargs.setdefault("metadata", {}).update(self.meta_reader_type)
            docs = []
            if self.use_parse_summary:
                text_str: str = self._parse_to_summary(resp)
                docs.append(Document(text=text_str, **load_kwargs))
            if self.use_audio_trans:
                text_str = self._parse_to_transcription(resp)
                docs.append(Document(text=text_str, **load_kwargs))
            return docs

        except Exception as e:
            print(f"Error raised for {str(e)}")
            return []

        # Document(
        #     text=text_str,
        #     metadata=extra_info,
        #     excluded_llm_metadata_keys=excluded_llm_keys,
        #     excluded_embed_metadata_keys=excluded_embed_keys,
        #     metadata_template=meta_template,
        #     metadata_seperator=seperator,
        #     text_template=text_template)
        #         # excluded_llm_keys=[],
        # # excluded_embed_keys=[],
        # # meta_template=DEFAULT_METADATA_TMPL, # meta k: v
        # # text_template=DEFAULT_TEXT_NODE_TMPL,
        # # seperator="\n", # meta_template
