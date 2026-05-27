"""
LLM 响应解析器 - 解析 DeepSeek 返回的 JSON，提供兜底策略
"""

import json
import re

VALID_EMOTIONS = {
    "normal", "happy", "excited", "comfort", "playful",
    "sleepy", "curious", "angry", "shy", "surprised",
}

VALID_ANIMATIONS = {
    "happy_jump", "happy_mid1", "happy_mid2", "happy_light",
    "angry_big", "angry_small", "snicker", "eat", "nap",
    "look", "pet", "like", "sing_start",
    "startle_small", "startle_big", "idle_anim",
}

_FALLBACK_PAYLOAD = {
    "text": "啾……我刚刚有点没听清，但我还在这里陪你。",
    "emotion": "normal",
    "action": "idle",
    "animation": "idle_anim",
    "tts": True,
}


def parse_llm_response(raw_text: str) -> dict:
    """
    解析 DeepSeek 原始输出，返回合法 payload。
    失败时返回 fallback，不抛异常。
    """
    if not raw_text or not raw_text.strip():
        return dict(_FALLBACK_PAYLOAD)

    text = raw_text.strip()

    # 剥离 Markdown 代码块
    md_match = re.search(r"```(?:json)?\s*([\s\S]*?)```", text)
    if md_match:
        text = md_match.group(1).strip()

    # 尝试直接解析
    payload = _try_parse_json(text)
    if payload is not None:
        return validate_llm_payload(payload)

    # 尝试提取第一个 {...} 块
    brace_match = re.search(r"\{[\s\S]*?\}", text)
    if brace_match:
        payload = _try_parse_json(brace_match.group())
        if payload is not None:
            return validate_llm_payload(payload)

    # 最后兜底：把原始文本当作 text 字段
    fallback = dict(_FALLBACK_PAYLOAD)
    # 如果原始文本看起来像自然语言（不含大括号），直接用作 text
    if "{" not in raw_text and len(raw_text.strip()) < 200:
        fallback["text"] = raw_text.strip()
    return fallback


def _try_parse_json(text: str):
    try:
        obj = json.loads(text)
        if isinstance(obj, dict):
            return obj
    except (json.JSONDecodeError, ValueError):
        pass
    return None


def validate_llm_payload(payload: dict) -> dict:
    """
    校验并补全 payload 字段，确保所有字段合法。
    """
    result = dict(_FALLBACK_PAYLOAD)

    # text：必须非空字符串
    text = payload.get("text", "")
    if isinstance(text, str) and text.strip():
        result["text"] = text.strip()

    # emotion：白名单校验
    emotion = payload.get("emotion", "normal")
    result["emotion"] = emotion if emotion in VALID_EMOTIONS else "normal"

    # action：直接透传，仅供语义参考，不做严格校验
    action = payload.get("action", "idle")
    result["action"] = action if isinstance(action, str) else "idle"

    # animation：白名单校验
    animation = payload.get("animation", "idle_anim")
    result["animation"] = animation if animation in VALID_ANIMATIONS else "idle_anim"

    # tts：布尔，缺失默认 True
    tts = payload.get("tts", True)
    result["tts"] = bool(tts)

    return result
