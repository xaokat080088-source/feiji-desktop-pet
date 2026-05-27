# Feiji Desktop Pet (肥鸡桌面宠物)

A cute cockatiel desktop pet built with Python and PyQt5. Feiji lives on your desktop, walks around, flies, sings, and chats with you powered by DeepSeek LLM.

## Features

- Transparent always-on-top desktop window
- Frame-by-frame PNG animation system (59 animation groups)
- Entrance flight animation
- Drag interaction (grab & release reactions)
- Feeding / Petting / Singing interactions
- Hover action buttons
- Local MP3 playback with fade-in/out
- TTS voice (edge-tts)
- LLM chat via DeepSeek API (returns JSON to control animations)
- System tray with right-click menu
- Three size modes (small / medium / large)
- Pin/unpin movement toggle
- Affection system (persistent)
- Windows installer support (Inno Setup)

## Tech Stack

- Python 3.10+
- PyQt5 (transparent window, animation, UI)
- pygame (audio playback)
- edge-tts (text-to-speech)
- DeepSeek API (LLM chat)
- PyInstaller (packaging)
- Inno Setup (Windows installer)

## Setup

### 1. Install dependencies

```bash
pip install -r requirements.txt
```

### 2. Configure API Key

Copy `.env.example` to `.env` and fill in your DeepSeek API key:

```bash
cp .env.example .env
```

Or set the environment variable directly:

**CMD:**
```cmd
set DEEPSEEK_API_KEY=your_api_key_here
```

**PowerShell:**
```powershell
$env:DEEPSEEK_API_KEY="your_api_key_here"
```

The pet will still run without an API key — chat will show a friendly reminder to configure it.

### 3. Run

```bash
python main_new.py
```

## Project Structure

```
main_new.py          - Main entry, PetWindow, tray, drag
animation_new.py     - Animation manager (59 groups, multi-size cache)
behavior_new.py      - Behavior engine (walk, fly, sleep, mischief)
hover_buttons.py     - Hover action buttons UI
chat_window.py       - Chat window, DeepSeek integration
deepseek_client.py   - DeepSeek API client
llm_prompt.py        - LLM system prompt (customizable)
llm_parser.py        - JSON response parser with fallback
llm_mapper.py        - Animation key → actual animation mapping
tts_engine.py        - TTS engine (edge-tts + pygame)
music_player.py      - Local MP3 player with fade
app_paths.py         - Path management (dev & packaged mode)
```

## Assets

- `frames_nobg/` — Animation frames (PNG, transparent background)
- `musik/` — Sample MP3 files used by the singing animation. You can replace them with your own.
- `assets/` — Icons

`musik/` 目录中包含示例 MP3，用于桌宠唱歌动画。你也可以替换为自己的音乐文件。

> This project uses frame-by-frame PNG animations, so the repository may be relatively large (~50MB).

## Customization

- Edit `llm_prompt.py` to customize the pet's personality and responses
- Replace animation frames in `frames_nobg/` with your own
- Add MP3 files to `musik/` for the singing feature

## Packaging

### PyInstaller

```bash
pyinstaller feiji.spec
```

### Inno Setup

Use `installer/feiji_setup.iss` to create a Windows installer from the PyInstaller output.

## Privacy Notice

- Never commit your API key or `.env` file
- This public version contains no private information
- Users can customize the pet name and prompt freely

## License

MIT License. See [LICENSE](LICENSE) for details.
