"""
LLM 动画映射器 - 把 DeepSeek 返回的 animation key 映射到实际动画调用
"""

import random
from animation_new import ANIM_SEQUENCES, AnimGroup

# DeepSeek 允许返回的 animation key → 实际调用方式
# "sequence" 表示调用 play_sequence，"single" 表示调用 play_single
_ANIM_MAP = {
    "happy_jump":    ("sequence", "happy_jump"),
    "happy_mid1":    ("sequence", "happy_mid1"),
    "happy_mid2":    ("sequence", "happy_mid2"),
    "happy_light":   ("sequence", "happy_light"),
    "angry_big":     ("sequence", "angry_big"),
    "angry_small":   ("sequence", "angry_small"),
    "snicker":       ("sequence", "snicker"),
    "eat":           ("sequence", "eat"),
    "nap":           ("sequence", "nap"),
    "look":          ("sequence", "look"),
    "pet":           ("sequence", "pet"),
    "like":          ("sequence", "like"),
    "sing_start":    ("sequence", "sing_start"),
    "startle_small": ("sequence", "startle_small"),
    "startle_big":   ("sequence", "startle_big"),
    "idle_anim":     ("idle", None),   # 特殊处理
}

# 对话结束后回到的默认待机动画
_IDLE_GROUPS = [AnimGroup.IDLE_A1, AnimGroup.IDLE_A2]

# 对话期间不允许打断的行为状态
_PROTECTED_STATES = {"interact", "mischief"}


def resolve_animation(animation_key: str) -> str:
    """返回合法的 animation key，不合法则降级为 idle_anim。"""
    if animation_key in _ANIM_MAP:
        return animation_key
    return "idle_anim"


def apply_llm_command(pet, payload: dict):
    """
    根据 payload 执行动画。
    如果宠物当前处于强交互状态（喂食/拖拽/唱歌），跳过动画，只做 TTS。
    动画结束后回到 start-B 待机。
    """
    animation_key = resolve_animation(payload.get("animation", "idle_anim"))

    # 检查当前行为状态，强交互中不打断
    current_state = getattr(pet.behavior, "_state", "idle")
    if current_state in _PROTECTED_STATES:
        # 只做 TTS，不播动画
        return

    # 将行为状态设为 interact，防止行为引擎在动画期间乱插行为
    pet.behavior._state = "interact"

    def _on_finish():
        pet.behavior._state = "idle"
        pet.anim_mgr.play_single(AnimGroup.START_B, loop=True)

    entry = _ANIM_MAP.get(animation_key, ("idle", None))
    mode, key = entry

    if mode == "sequence":
        # 确认序列 key 真实存在，防御性检查
        if key in ANIM_SEQUENCES:
            pet.anim_mgr.play_sequence(key, loop=False, on_finish=_on_finish)
        else:
            _play_idle(pet, _on_finish)
    else:
        _play_idle(pet, _on_finish)


def _play_idle(pet, on_finish):
    """播放随机 Idle-A 动画，失败则直接回到 start-B。"""
    group = random.choice(_IDLE_GROUPS)
    if group in pet.anim_mgr._cache:
        pet.anim_mgr.play_single(group, loop=False, on_finish=on_finish)
    else:
        on_finish()
