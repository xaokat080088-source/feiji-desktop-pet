import asyncio
import threading
import io
import re
import hashlib
from pathlib import Path
from PyQt5.QtCore import QObject, pyqtSignal
from app_paths import CACHE_DIR


class TTSEngine(QObject):
    finished = pyqtSignal()

    def __init__(self):
        super().__init__()
        self.enabled = True
        self.voice = "zh-CN-XiaoxiaoNeural"
        self.rate  = "+25%"
        self.pitch = "+15Hz"
        self._lock = threading.Lock()
        CACHE_DIR.mkdir(parents=True, exist_ok=True)

        # 预初始化 pygame mixer，避免第一次播放时初始化耗时
        try:
            import pygame
            if not pygame.mixer.get_init():
                pygame.mixer.init(frequency=24000, size=-16, channels=1, buffer=512)
        except Exception:
            pass

    # ── 公共接口 ──────────────────────────────────────────────

    def speak(self, text: str, on_done=None):
        """后台线程朗读，流式生成直接播放，减少等待。"""
        if not self.enabled or not text.strip():
            if on_done:
                on_done()
            return
        threading.Thread(target=self._run_stream, args=(text, on_done), daemon=True).start()

    def speak_cached(self, text: str, on_done=None):
        """固定文本：有缓存直接播，无缓存流式生成并缓存。"""
        if not self.enabled or not text.strip():
            if on_done:
                on_done()
            return
        threading.Thread(target=self._run_cached, args=(text, on_done), daemon=True).start()

    def stop(self):
        try:
            import pygame
            pygame.mixer.music.stop()
        except Exception:
            pass

    # ── 内部实现 ──────────────────────────────────────────────

    def _cache_path(self, text: str) -> Path:
        key = f"{self.voice}|{self.rate}|{self.pitch}|{text}"
        h = hashlib.md5(key.encode("utf-8")).hexdigest()[:12]
        return CACHE_DIR / f"tts_{h}.mp3"

    def _run_cached(self, text: str, on_done):
        """缓存版：命中缓存直接播，否则流式生成并保存缓存。"""
        path = self._cache_path(text)
        try:
            if path.exists():
                self._play_file(str(path))
            else:
                # 流式生成，同时写入缓存文件
                buf = self._stream_to_bytes(text)
                if buf:
                    try:
                        path.write_bytes(buf)
                    except Exception:
                        pass
                    self._play_bytes(buf)
        except Exception as e:
            print(f"[TTS] cached speak error: {e}")
        finally:
            if on_done:
                on_done()

    def _run_stream(self, text: str, on_done):
        """普通朗读：流式生成到内存，完成后立即播放（省去文件 I/O）。"""
        try:
            buf = self._stream_to_bytes(text)
            if buf:
                self._play_bytes(buf)
        except Exception as e:
            print(f"[TTS] stream speak error: {e}")
        finally:
            if on_done:
                on_done()

    def _stream_to_bytes(self, text: str) -> bytes:
        """用 edge-tts 流式接口把音频数据收集到内存，返回 bytes。"""
        import edge_tts

        buf = io.BytesIO()

        async def _collect():
            communicate = edge_tts.Communicate(
                text, self.voice,
                rate=self.rate,
                pitch=self.pitch,
            )
            async for chunk in communicate.stream():
                if chunk["type"] == "audio":
                    buf.write(chunk["data"])

        asyncio.run(_collect())
        return buf.getvalue()

    def _play_bytes(self, data: bytes):
        """用 pygame 播放内存中的 MP3 数据。"""
        try:
            import pygame
            if not pygame.mixer.get_init():
                pygame.mixer.init(frequency=24000, size=-16, channels=1, buffer=512)
            buf = io.BytesIO(data)
            pygame.mixer.music.load(buf)
            pygame.mixer.music.play()
            import time
            while pygame.mixer.music.get_busy():
                time.sleep(0.05)
        except Exception as e:
            print(f"[TTS] play_bytes error: {e}")

    def _play_file(self, path: str):
        """播放本地文件（缓存命中时用）。"""
        try:
            import pygame
            if not pygame.mixer.get_init():
                pygame.mixer.init(frequency=24000, size=-16, channels=1, buffer=512)
            pygame.mixer.music.load(path)
            pygame.mixer.music.play()
            import time
            while pygame.mixer.music.get_busy():
                time.sleep(0.05)
        except Exception as e:
            print(f"[TTS] play_file error: {e}")
