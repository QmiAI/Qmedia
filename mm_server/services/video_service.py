import base64
from pathlib import Path
from typing import BinaryIO, Iterable, List, NamedTuple, Optional, Tuple, Union

import cv2
import numpy as np
from cachetools import TTLCache, cached, keys
from config import Config
from llama_index.core.schema import *
from PIL import Image
from rich import print

try:
    print(" Long loading whisper time ")
    from faster_whisper import WhisperModel
    from faster_whisper.transcribe import Segment, TranscriptionInfo
except ImportError as e:
    print(f"Error importing required libraries: {str(e)}")

video_cached = TTLCache(maxsize=1, ttl=Config.video_keep_alive)


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


class AudioTranscriptionRemote(WhisperModel):
    def get_audio_transcription(
        self, audio, beam_size=5, vad_filter=True
    ) -> AudioResponse:
        """
        Transcribes the given audio using the Whisper model.

        Args:
            audio: The audio to be transcribed.
            beam_size: The beam size for decoding. Default is 5.
            vad_filter: Whether to apply voice activity detection (VAD) filter. Default is True.

        Returns:
            An instance of AudioResponse containing the transcribed audio information.

        """
        segments: List[Segment]
        info: TranscriptionInfo

        try:
            segments, info = self.transcribe(
                audio, beam_size=beam_size, vad_filter=vad_filter
            )
        except Exception as e:
            print(f"Error occurred during audio transcription: {str(e)}")
            return AudioResponse(
                language="",
                language_probability=0.0,
                duration=0.0,
                duration_after_vad=0.0,
                segments=[],
            )

        print(
            "Detected language '%s' with probability %f"
            % (info.language, info.language_probability)
        )
        print(info)

        _segments = []
        for s in segments:
            # print(s)
            print("[%.2fs -> %.2fs] %s" % (s.start, s.end, s.text))
            _segments.append(
                SentenceSegment(
                    id=s.id, seek=s.seek, start=s.start, end=s.end, text=s.text
                )
            )
        audio_resp = AudioResponse(
            language=info.language,
            language_probability=info.language_probability,
            duration=info.duration,
            duration_after_vad=info.duration_after_vad,
            segments=_segments,
        )

        return audio_resp


# audio_trans_model = AudioTranscriptionRemote(
#     model_size_or_path=Config.audio_model_name,
#     device='cpu',
#     compute_type='int8')

# print("@ Load audio_trans_model")


@cached(video_cached)
def video_init_model():
    print(f"@ Init AudioTranscriptionRemote model server")
    model = AudioTranscriptionRemote(
        model_size_or_path=Config.audio_model_name, device="cpu", compute_type="int8"
    )
    return model


def test_run_whisper():

    audio = ""
    audio_resp = video_init_model().get_audio_transcription(audio)

    print(audio_resp)
