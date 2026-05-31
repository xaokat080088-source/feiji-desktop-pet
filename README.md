# Feiji Desktop Pet（肥鸡桌面宠物）

<img width="1280" height="640" alt="preview" src="https://github.com/user-attachments/assets/cff02bb9-6f90-47e9-a793-0f6c88860b5f" />

一个基于 Python / PyQt5 的可爱玄凤鹦鹉桌面宠物项目，支持逐帧动画、拖拽互动、喂食、摸摸、唱歌、TTS 朗读、系统托盘、亲密度系统，以及基于 LLM 的对话与动画联动。

> 中文说明在前，English version below.

[中文介绍](#中文介绍) | [English](#english)

---

## 中文介绍

### 项目简介

Feiji Desktop Pet 是一个可爱的玄凤鹦鹉桌面宠物。它可以停留在桌面上，走动、飞行、唱歌、被拖拽、被喂食、被摸摸，还可以通过 DeepSeek API 进行对话，并根据回复内容播放对应动画。

### 功能特点

- 透明置顶桌面宠物窗口
- 逐帧 PNG 动画系统（59 组动画）
- 入场飞行动画
- 拖拽互动（抓起 / 放下反应）
- 喂食、摸摸、唱歌
- 悬停按钮
- 本地 MP3 唱歌音乐（渐入 / 渐出）
- TTS 语音朗读（edge-tts）
- DeepSeek LLM 对话
- JSON 隐藏指令驱动动画
- 系统托盘 + 右键菜单
- 大 / 中 / 小尺寸切换
- 曲别针固定移动开关
- 亲密度系统（持久化）
- Windows 安装包支持（Inno Setup）

### 技术栈

- Python 3.10+
- PyQt5
- pygame
- edge-tts
- DeepSeek API
- PyInstaller
- Inno Setup

### 安装依赖

```bash
pip install -r requirements.txt
```

### 配置 DeepSeek API Key

本项目不会内置 API Key。如果你想使用 LLM 对话功能，需要自行配置环境变量。

**PowerShell:**

```powershell
$env:DEEPSEEK_API_KEY="your_api_key_here"
```

**CMD:**

```cmd
set DEEPSEEK_API_KEY=your_api_key_here
```

也可以复制 `.env.example` 为 `.env` 后填入。

如果没有配置 API Key，桌宠仍然可以正常运行，但对话功能会返回友好提示信息。

### 运行项目

```bash
python main_new.py
```

### 项目结构

```
main_new.py          主入口、桌宠窗口、托盘、拖拽
animation_new.py     动画系统（多尺寸缓存）
behavior_new.py      行为状态机（走路、飞行、睡觉、捣乱）
hover_buttons.py     悬停按钮
chat_window.py       对话窗口
deepseek_client.py   DeepSeek API 客户端
llm_prompt.py        LLM 人设提示词（可自定义）
llm_parser.py        JSON 解析（带兜底）
llm_mapper.py        动画映射
tts_engine.py        TTS 语音
music_player.py      本地音乐播放
app_paths.py         路径管理（开发 / 打包双模式）
frames_nobg/         逐帧动画素材
musik/               MP3 音乐目录
assets/              图标资源
installer/           Inno Setup 安装脚本
```

### 素材说明

- `frames_nobg/` 包含逐帧 PNG 动画素材
- `musik/` 包含示例 MP3，用于唱歌动画，你可以替换为自己的音乐
- `assets/` 包含图标

> 注意：由于项目使用大量逐帧 PNG 动画，仓库体积可能较大（约 50MB）。

### 自定义

- 编辑 `llm_prompt.py` 自定义宠物人设和回复风格
- 替换 `frames_nobg/` 中的动画帧为你自己的素材
- 在 `musik/` 中添加自己的 MP3 文件

### 打包

**PyInstaller:**

```bash
pyinstaller feiji.spec
```

**Inno Setup:**

使用 `installer/feiji_setup.iss` 从 PyInstaller 输出生成 Windows 安装包。

### 隐私说明

- 请不要提交自己的 API Key 或 `.env` 文件
- 公开版本不包含任何私人信息
- 你可以自行修改宠物名称、性格和提示词

### License

MIT License. 详见 [LICENSE](LICENSE)。

---

## English

### Overview

Feiji Desktop Pet is a cute cockatiel desktop companion built with Python and PyQt5. Feiji lives on your desktop, walks around, flies, sings, and chats with you powered by DeepSeek LLM. Replies drive matching animations through a hidden JSON protocol.

### Features

- Transparent always-on-top desktop window
- Frame-by-frame PNG animation system (59 animation groups)
- Entrance flight animation
- Drag interaction (grab & release reactions)
- Feeding / Petting / Singing
- Hover action buttons
- Local MP3 playback with fade-in/out
- TTS voice (edge-tts)
- LLM chat via DeepSeek API (returns JSON to control animations)
- System tray with right-click menu
- Three size modes (small / medium / large)
- Pin/unpin movement toggle
- Affection system (persistent)
- Windows installer support (Inno Setup)

### Tech Stack

- Python 3.10+
- PyQt5
- pygame
- edge-tts
- DeepSeek API
- PyInstaller
- Inno Setup

### Install dependencies

```bash
pip install -r requirements.txt
```

### Configure API Key

This project does not bundle any API key. To enable LLM chat, set an environment variable:

**PowerShell:**

```powershell
$env:DEEPSEEK_API_KEY="your_api_key_here"
```

**CMD:**

```cmd
set DEEPSEEK_API_KEY=your_api_key_here
```

Or copy `.env.example` to `.env` and fill in your key.

The pet still runs without an API key — chat will show a friendly reminder to configure it.

### Run

```bash
python main_new.py
```

### Project Structure

```
main_new.py          Main entry, PetWindow, tray, drag
animation_new.py     Animation manager (multi-size cache)
behavior_new.py      Behavior engine (walk, fly, sleep, mischief)
hover_buttons.py     Hover action buttons UI
chat_window.py       Chat window, DeepSeek integration
deepseek_client.py   DeepSeek API client
llm_prompt.py        LLM system prompt (customizable)
llm_parser.py        JSON response parser with fallback
llm_mapper.py        Animation key → actual animation mapping
tts_engine.py        TTS engine (edge-tts + pygame)
music_player.py      Local MP3 player with fade
app_paths.py         Path management (dev & packaged mode)
frames_nobg/         Animation frame assets
musik/               MP3 directory
assets/              Icons
installer/           Inno Setup installer script
```

### Assets

- `frames_nobg/` — Animation frames (PNG, transparent background)
- `musik/` — Sample MP3 files used by the singing animation. You can replace them with your own.
- `assets/` — Icons

> This project uses frame-by-frame PNG animations, so the repository may be relatively large (~50MB).

### Customization

- Edit `llm_prompt.py` to customize the pet's personality and responses
- Replace animation frames in `frames_nobg/` with your own
- Add MP3 files to `musik/` for the singing feature

### Packaging

**PyInstaller:**

```bash
pyinstaller feiji.spec
```

**Inno Setup:**

Use `installer/feiji_setup.iss` to create a Windows installer from the PyInstaller output.

### Privacy Notice

- Never commit your API key or `.env` file
- This public version contains no private information
- Users can customize the pet name and prompt freely

### License

MIT License. See [LICENSE](LICENSE) for details.
