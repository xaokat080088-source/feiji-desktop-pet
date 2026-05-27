"""
本地 MP3 播放器，用于肥鸡唱歌功能。
使用 pygame.mixer，不弹系统播放器，支持渐入/渐出。
"""

import random
import threading
from pathlib import Path
from PyQt5.QtCore import QTimer, QObject
from app_paths import MUSIK_DIR
FADE_STEP_MS = 80       # 渐变定时器间隔
FADE_IN_STEPS = 12      # 渐入步数（约 1 秒）
FADE_OUT_STEPS = 12     # 渐出步数（约 1 秒）
MAX_VOLUME = 0.85


class MusicPlayer(QObject):
    def __init__(self, parent=None):
        super().__init__(parent)
        self._mixer_ready = False
        self._playing = False
        self._fade_timer = QTimer(self)
        self._fade_timer.timeout.connect(self._fade_step)
        self._fade_target = 0.0
        self._fade_current = 0.0
        self._fade_delta = 0.0
        self._on_fade_done = None
        self._init_mixer()

    def _init_mixer(self):
        try:
            import pygame
            if not pygame.mixer.get_init():
                pygame.mixer.init()
            self._mixer_ready = True
        except Exception as e:
            print(f"[Music] mixer init failed: {e}")

    def _get_tracks(self):
        if not MUSIK_DIR.exists():
            return []
        return list(MUSIK_DIR.glob("*.mp3"))

    def play_fade_in(self):
        """随机选一首，从音量 0 渐入到 MAX_VOLUME。"""
        if not self._mixer_ready:
            return
        tracks = self._get_tracks()
        if not tracks:
            return
        track = random.choice(tracks)
        try:
            import pygame
            pygame.mixer.music.load(str(track))
            pygame.mixer.music.set_volume(0.0)
            pygame.mixer.music.play(-1)  # 循环播放，唱歌动画结束时停
            self._playing = True
            self._start_fade(0.0, MAX_VOLUME, FADE_IN_STEPS)
        except Exception as e:
            print(f"[Music] play failed: {e}")

    def fade_out(self, on_done=None):
        """渐出到 0，完成后停止。"""
        if not self._mixer_ready or not self._playing:
            if on_done:
                on_done()
            return
        self._on_fade_done = on_done
        self._start_fade(self._fade_current, 0.0, FADE_OUT_STEPS)

    def stop_immediately(self):
        """立即停止，不渐出。"""
        self._fade_timer.stop()
        self._playing = False
        self._on_fade_done = None
        try:
            import pygame
            pygame.mixer.music.stop()
        except Exception:
            pass

    def is_playing(self):
        return self._playing

    def _start_fade(self, from_vol: float, to_vol: float, steps: int):
        self._fade_timer.stop()
        self._fade_current = from_vol
        self._fade_target = to_vol
        self._fade_delta = (to_vol - from_vol) / max(steps, 1)
        self._fade_timer.start(FADE_STEP_MS)

    def _fade_step(self):
        self._fade_current += self._fade_delta
        if self._fade_delta > 0:
            reached = self._fade_current >= self._fade_target
        else:
            reached = self._fade_current <= self._fade_target

        vol = max(0.0, min(MAX_VOLUME, self._fade_current))
        try:
            import pygame
            pygame.mixer.music.set_volume(vol)
        except Exception:
            pass

        if reached:
            self._fade_timer.stop()
            self._fade_current = self._fade_target
            if self._fade_target <= 0.0:
                self._playing = False
                try:
                    import pygame
                    pygame.mixer.music.stop()
                except Exception:
                    pass
            cb = self._on_fade_done
            self._on_fade_done = None
            if cb:
                cb()
