"""
音频特征提取 - A 负责实现。

入参：临时音频路径 + Whisper 已转写结果（避免重复转写）
出参：VoiceMetrics dict（参见 docs/expression_module_contract.md §2.1）

约定：
- 必须复用 stt_service.transcribe_detailed() 的结果，不重新调 Whisper
- 音频 < 3 秒 或 转写为空 → 返回 None
- 填充词清单从 evaluation.filler_words import，禁止硬编码
- wpm 中文按字/分钟，英文按 1 词≈2 字折算
"""

from typing import Optional
from evaluation.filler_words import FILLER_WORDS  # noqa: F401


# ============== mock 实现：让 B 可以并行联调 ==============
# A 完成真实实现后请删除此函数，将 _mock_analyze 改为 analyze_audio。

def analyze_audio(audio_path: str, whisper_result: dict) -> Optional[dict]:
    """
    Args:
        audio_path: 临时音频文件路径
        whisper_result: stt_service.transcribe_detailed() 完整返回

    Returns:
        VoiceMetrics dict 或 None（音频太短/转写失败）
    """
    return _mock_analyze(audio_path, whisper_result)


def _mock_analyze(audio_path: str, whisper_result: dict) -> Optional[dict]:
    """临时 mock 实现。返回固定特征便于 B 端联调。"""
    text = (whisper_result or {}).get("text", "").strip()
    if not text:
        return None

    return {
        "duration_sec": 30.0,
        "transcript": text,
        "segments": (whisper_result or {}).get("segments", []),

        "wpm": 220.0,
        "char_count": len(text),

        "pause_ratio": 0.18,
        "long_pause_count": 2,
        "filler_words": [
            {"word": "嗯", "count": 3},
            {"word": "然后", "count": 5},
        ],
        "filler_total": 8,

        "pitch_mean": 180.0,
        "pitch_std": 14.0,
        "volume_mean": 0.05,
        "volume_std": 0.012,
    }


# ============== 真实实现待办（A 实现） ==============
# def _real_analyze(audio_path, whisper_result):
#     import librosa, numpy as np
#     y, sr = librosa.load(audio_path, sr=16000)
#     duration = len(y) / sr
#     if duration < 3.0:
#         return None
#     # 1. wpm = char_count / duration * 60
#     # 2. pause_ratio: 用 librosa.effects.split 或 webrtcvad 算静音
#     # 3. long_pause_count: 遍历 segments 间隙 > 1.5s
#     # 4. filler_words: 在 transcript 里子串计数（FILLER_WORDS）
#     # 5. pitch_mean/std: librosa.yin(y, fmin=50, fmax=500)
#     # 6. volume_mean/std: librosa.feature.rms(y=y)
#     ...
