"""
新动画系统 - 适配59组动画
基于你提供的动画分组设计
"""

import os
import queue
import threading
from pathlib import Path
from PyQt5.QtGui import QPixmap, QImage, QPainter, QTransform
from PyQt5.QtCore import Qt

from app_paths import FRAMES_DIR

PHOTO_DIR = FRAMES_DIR

# 入场动画必须同步加载，其余后台加载
_ENTRANCE_GROUPS = frozenset([
    "Hop-A（1）", "Hop-A（2）", "Hop-B",
    "Hop-C（1）", "Hop-C（2）", "start-A", "start-B",
])

# 动画组定义
class AnimGroup:
    # 行走
    WALK_A = "Walk-A"           # 正常走路，可循环
    WALK_B = "Walk-B"           # 回头走路，插播用

    # 待机
    IDLE_A1 = "Idle-A（1）"     # 蹲下眨眼1
    IDLE_A2 = "Idle-A（2）"     # 蹲下眨眼2

    # 开心（3种）
    HAPPY_A1 = "Happy-A（1）"   # 跳起来开心-起
    HAPPY_A2 = "Happy-A（2）"   # 跳起来开心-中
    HAPPY_A3 = "Happy-A（3）"   # 跳起来开心-落
    HAPPY_A4 = "Happy-A（4）"   # 中等开心1
    HAPPY_A5 = "Happy-A（5）"   # 中等开心2
    HAPPY_A6 = "Happy-A（6）"   # 中等开心3
    HAPPY_B1 = "Happy-B（1）"   # 第三种开心1
    HAPPY_B2 = "Happy-B（2）"   # 第三种开心2
    HAPPY_B3 = "Happy-B（3）"   # 第三种开心3
    HAPPY_C1 = "Happy-C（1）"   # 第四种开心1
    HAPPY_C2 = "Happy-C（2）"   # 第四种开心2

    # 生气
    ANGRY_A1 = "Angry-A（1）"   # 大生气1
    ANGRY_A2 = "Angry-A（2）"   # 大生气2
    ANGRY_A3 = "Angry-A（3）"   # 大生气3
    ANGRY_B1 = "Angry-B（1）"   # 小生气1
    ANGRY_B2 = "Angry-B（2）"   # 小生气2

    # 偷笑
    SNICKER_A1 = "snicker-A（1）"
    SNICKER_A2 = "snicker-A（2）"
    SNICKER_A3 = "snicker-A（3）"

    # 飞行
    HOP_A1 = "Hop-A（1）"       # 起飞1
    HOP_A2 = "Hop-A（2）"       # 起飞2
    HOP_B  = "Hop-B"            # 巡飞（循环）
    HOP_C1 = "Hop-C（1）"       # 降落1
    HOP_C2 = "Hop-C（2）"       # 降落2

    # 吃东西
    EAT_A1 = "Eat-A（1）"
    EAT_A2 = "Eat-A（2）"
    EAT_A3 = "Eat-A（3）"
    EAT_A4 = "Eat-A（4）"

    # 被抓
    GRAB_A  = "Grab-A"          # 拎起来
    GRAB_B1 = "Grab-B（1）"     # 放下1
    GRAB_B2 = "Grab-B（2）"     # 放下2
    GRAB_B3 = "Grab-B（3）"     # 放下3
    GRAB_C  = "Grab-C"          # 被抓住时扑腾翅膀（循环）

    # 睡觉
    SLEEP_A1 = "Sleep-A（1）"   # 小睡1
    SLEEP_A2 = "Sleep-A（2）"   # 小睡2
    SLEEP_B1 = "Sleep-B（1）"   # 躺下
    SLEEP_B2 = "Sleep-B（2）"   # 睡觉中（循环）
    SLEEP_B3 = "Sleep-B（3）"   # 起床

    # 看向主人
    LOOK_A1 = "look-A（1）"
    LOOK_A2 = "look-A（2）"

    # 被摸头
    PET_A1 = "Pet-A（1）"
    PET_A2 = "Pet-A（2）"
    PET_A3 = "Pet-A（3）"
    PET_A4 = "Pet-A（4）"

    # 喜欢（爱心眼）
    LIKE_A1 = "like-A（1）"
    LIKE_A2 = "like-A（2）"

    # 唱歌
    SING_A1 = "Sing-A（1）"
    SING_A2 = "Sing-A（2）"
    SING_B  = "Sing-B"          # 唱歌中（循环）
    SING_C  = "Sing-C"          # 唱歌结束

    # 受惊
    STARTLE_A1 = "Startle-A（1）"  # 小惊吓1
    STARTLE_A2 = "Startle-A（2）"  # 小惊吓2
    STARTLE_B1 = "Startle-B（1）"  # 大惊吓1
    STARTLE_B2 = "Startle-B（2）"  # 大惊吓2

    # 初始动画
    START_A = "start-A"         # 左右看
    START_B = "start-B"         # 静态站立


# 动画序列定义（哪些动画需要顺序播放）
ANIM_SEQUENCES = {
    # 开心跳跃（必须顺序）
    "happy_jump": [AnimGroup.HAPPY_A1, AnimGroup.HAPPY_A2, AnimGroup.HAPPY_A3],
    # 开心中等1
    "happy_mid1": [AnimGroup.HAPPY_A4, AnimGroup.HAPPY_A5, AnimGroup.HAPPY_A6],
    # 开心中等2
    "happy_mid2": [AnimGroup.HAPPY_B1, AnimGroup.HAPPY_B2, AnimGroup.HAPPY_B3],
    # 开心轻微
    "happy_light": [AnimGroup.HAPPY_C1, AnimGroup.HAPPY_C2],

    # 大生气
    "angry_big": [AnimGroup.ANGRY_A1, AnimGroup.ANGRY_A2, AnimGroup.ANGRY_A3],
    # 小生气
    "angry_small": [AnimGroup.ANGRY_B1, AnimGroup.ANGRY_B2],

    # 偷笑
    "snicker": [AnimGroup.SNICKER_A1, AnimGroup.SNICKER_A2, AnimGroup.SNICKER_A3],

    # 待机小动作链（必须顺序）
    "idle_a_chain": [AnimGroup.IDLE_A1, AnimGroup.IDLE_A2],

    # 起飞
    "takeoff": [AnimGroup.HOP_A1, AnimGroup.HOP_A2],
    # 降落
    "landing": [AnimGroup.HOP_C1, AnimGroup.HOP_C2],

    # 吃东西
    "eat": [AnimGroup.EAT_A1, AnimGroup.EAT_A2, AnimGroup.EAT_A3, AnimGroup.EAT_A4],

    # 被抓放下
    "grabbed": [AnimGroup.GRAB_A],
    "released": [AnimGroup.GRAB_B1, AnimGroup.GRAB_B2, AnimGroup.GRAB_B3],

    # 小睡
    "nap": [AnimGroup.SLEEP_A1, AnimGroup.SLEEP_A2],
    # 大睡
    "sleep_start": [AnimGroup.SLEEP_B1],
    "sleep_end": [AnimGroup.SLEEP_B3],

    # 看主人
    "look": [AnimGroup.LOOK_A1, AnimGroup.LOOK_A2],

    # 被摸头
    "pet": [AnimGroup.PET_A1, AnimGroup.PET_A2, AnimGroup.PET_A3, AnimGroup.PET_A4],

    # 喜欢
    "like": [AnimGroup.LIKE_A1, AnimGroup.LIKE_A2],

    # 唱歌开始
    "sing_start": [AnimGroup.SING_A1, AnimGroup.SING_A2],
    # 唱歌结束
    "sing_end": [AnimGroup.SING_C],

    # 小惊吓
    "startle_small": [AnimGroup.STARTLE_A1, AnimGroup.STARTLE_A2],
    # 大惊吓
    "startle_big": [AnimGroup.STARTLE_B1, AnimGroup.STARTLE_B2],
}

# 可循环动画
LOOP_ANIMS = [
    AnimGroup.WALK_A,
    AnimGroup.HOP_B,
    AnimGroup.SLEEP_B2,
    AnimGroup.SING_B,
    AnimGroup.START_A,
]

# 待机动画（随机插播）
IDLE_ANIMS = [
    AnimGroup.IDLE_A1,
    AnimGroup.IDLE_A2,
]


class AnimationManager:
    def __init__(self, photo_dir: Path, display_size: int, all_sizes: list = None):
        self.photo_dir = photo_dir
        self.display_size = display_size

        # 多档缓存：{size: {group_name: [QPixmap, ...]}}
        self._size_caches = {}
        # 后台预热的其他尺寸列表（不含当前尺寸）
        self._warmup_sizes = [s for s in (all_sizes or []) if s != display_size]

        self._current_seq = []
        self._seq_idx = 0
        self._frame_idx = 0
        self._loop = False
        self._on_finish = None
        self._elapsed = 0
        self._frame_interval = 40
        self._speed_overrides = {
            AnimGroup.GRAB_A:  max(1, int(40 / 6)),
            AnimGroup.GRAB_B1: max(1, int(40 / 6)),
        }

        self._facing = 1

        # 启动时只同步加载入场动画，其余后台加载
        self._pending_q: queue.Queue = queue.Queue()
        self._size_caches[display_size] = self._load_size(display_size, only=_ENTRANCE_GROUPS)
        self._cache = self._size_caches[display_size]
        # 后台加载剩余动画
        self._bg_load(display_size, skip=_ENTRANCE_GROUPS)

    def _load_size(self, size: int, only: frozenset = None, skip: frozenset = None) -> dict:
        """加载指定尺寸的帧。only=只加载这些组；skip=跳过这些组。"""
        cache = {}
        subdirs = [d for d in self.photo_dir.iterdir() if d.is_dir()]
        for d in subdirs:
            if only is not None and d.name not in only:
                continue
            if skip is not None and d.name in skip:
                continue
            frames = sorted(d.glob("*.png"))
            pixmaps = []
            for f in frames:
                img = QImage(str(f))
                if img.isNull():
                    continue
                scaled = img.scaled(
                    size, size,
                    Qt.KeepAspectRatio,
                    Qt.SmoothTransformation
                )
                pixmaps.append(QPixmap.fromImage(scaled))
            if pixmaps:
                cache[d.name] = pixmaps
        return cache

    def _bg_load(self, size: int, skip: frozenset = None):
        """后台线程加载剩余动画组，完成后放入队列，由 tick() 在主线程消费。"""
        photo_dir = self.photo_dir
        q = self._pending_q

        def _worker():
            subdirs = [d for d in photo_dir.iterdir() if d.is_dir()]
            for d in subdirs:
                if skip and d.name in skip:
                    continue
                frames = sorted(d.glob("*.png"))
                images = []
                for f in frames:
                    img = QImage(str(f))
                    if img.isNull():
                        continue
                    images.append(img.scaled(size, size, Qt.KeepAspectRatio, Qt.SmoothTransformation))
                if images:
                    q.put((size, d.name, images))

        threading.Thread(target=_worker, daemon=True).start()

    def _flush_pending(self):
        """主线程调用：把后台加载好的 QImage 转为 QPixmap 写入缓存。"""
        try:
            while True:
                size, name, images = self._pending_q.get_nowait()
                if size in self._size_caches:
                    self._size_caches[size][name] = [QPixmap.fromImage(img) for img in images]
        except queue.Empty:
            pass

    def start_background_warmup(self):
        """在后台线程预生成其他尺寸缓存，不阻塞 UI。"""
        if not self._warmup_sizes:
            return
        def _warmup():
            for size in self._warmup_sizes:
                if size not in self._size_caches:
                    try:
                        # 先加载入场组，再加载其余
                        self._size_caches[size] = self._load_size(size, only=_ENTRANCE_GROUPS)
                        self._bg_load(size, skip=_ENTRANCE_GROUPS)
                    except Exception as e:
                        print(f"[Anim] warmup size={size} failed: {e}")
        threading.Thread(target=_warmup, daemon=True).start()

    def resize(self, new_size: int):
        """切换显示尺寸。若缓存已就绪则立即切换，否则同步生成入场组后后台补全。"""
        if new_size not in self._size_caches:
            self._size_caches[new_size] = self._load_size(new_size, only=_ENTRANCE_GROUPS)
            self._bg_load(new_size, skip=_ENTRANCE_GROUPS)
        self.display_size = new_size
        self._cache = self._size_caches[new_size]

    def set_facing(self, direction: int):
        """设置朝向：1=左，-1=右"""
        self._facing = direction

    def get_facing(self) -> int:
        """获取当前朝向"""
        return self._facing

    def play_sequence(self, seq_name: str, loop=False, on_finish=None):
        """播放动画序列"""
        if seq_name not in ANIM_SEQUENCES:
            return
        self._current_seq = ANIM_SEQUENCES[seq_name]
        self._seq_idx = 0
        self._frame_idx = 0
        self._loop = loop
        self._on_finish = on_finish
        self._elapsed = 0

    def play_single(self, group_name: str, loop=False, on_finish=None):
        """播放单个动画组"""
        if group_name not in self._cache:
            return
        self._current_seq = [group_name]
        self._seq_idx = 0
        self._frame_idx = 0
        self._loop = loop
        self._on_finish = on_finish
        self._elapsed = 0

    def tick(self, dt_ms: int) -> bool:
        """返回是否需要重绘"""
        self._flush_pending()
        if not self._current_seq:
            return False
        group = self._current_seq[self._seq_idx]
        interval = self._speed_overrides.get(group, self._frame_interval)

        self._elapsed += dt_ms
        if self._elapsed < interval:
            return False

        self._elapsed = 0

        frames = self._cache.get(group, [])
        if not frames:
            return False

        self._frame_idx += 1
        if self._frame_idx >= len(frames):
            # 当前组播完
            self._frame_idx = 0
            self._seq_idx += 1

            if self._seq_idx >= len(self._current_seq):
                # 整个序列播完
                if self._loop:
                    self._seq_idx = 0
                else:
                    self._seq_idx = len(self._current_seq) - 1
                    self._frame_idx = len(frames) - 1
                    if self._on_finish:
                        cb = self._on_finish
                        self._on_finish = None
                        cb()

        return True

    def current_frame(self) -> QPixmap:
        if not self._current_seq:
            return QPixmap()
        group = self._current_seq[self._seq_idx]
        frames = self._cache.get(group, [])
        if not frames:
            return QPixmap()

        pixmap = frames[self._frame_idx]

        # 如果朝右，水平翻转
        if self._facing == -1:
            pixmap = pixmap.transformed(
                QTransform().scale(-1, 1),
                Qt.SmoothTransformation
            )

        return pixmap

    def current_anim(self) -> str:
        if not self._current_seq:
            return ""
        return self._current_seq[self._seq_idx]
