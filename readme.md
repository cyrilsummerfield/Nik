# Nik — A Voice‑Activated AI Assistant

This is an AI assistant that I made (with a little help from ChatGPT 😉.) It allows you to talk to various GenAI models verbally, as well as enables the AI to open websites in Chrome. You can be direct with it, such as "Open Gmail," or you can be less precise, such as "Open a website with baseball stats." It is certainly not perfect, for you have to say your command within 2 seconds, and it can be slow to respond to commands and questions. I also have not tested it on any systems besides Raspbian (a Unix build for Raspberry Pis), so it might not work well on other machines. Below I have listed the instructions to set it up on your computer.

---

## 🐧 Linux / macOS Setup

1. **Install packages & Python libraries**

   ```bash
   sudo apt update && sudo apt install -y \
     python3-pip libsndfile1 espeak-ng ffmpeg sox chromium-browser git wget

   pip3 install speechrecognition requests piper-tts
   ```

   > **macOS users** – replace the `apt` line with Homebrew:
   >
   > ```bash
   > brew install python3 espeak-ng ffmpeg sox git wget
   > pip3 install speechrecognition requests piper-tts
   > ```

2. **Download a Piper voice model**

   ```bash
   mkdir -p ~/piper_models/en_US/lessac/medium
   wget -O ~/piper_models/en_US/lessac/medium/en_US-lessac-medium.onnx \
        https://huggingface.co/rhasspy/piper-voices/resolve/main/en/en_US/lessac/medium/en_US-lessac-medium.onnx
   ```

3. **Clone / copy the code**

   ```bash
   git clone https://github.com/<your‑username>/nik-ai-assistant.git
   cd nik-ai-assistant
   ```

4. **Add your OpenRouter API key**

   Edit `nik.py` and replace:

   ```python
   OPENROUTER_API_KEY = "your-api-key-here"
   ```

5. **Run Nik**

   ```bash
   python3 nik.py
   ```

---

## 🪟 Windows Setup

1. **Install Python & tools**

   - Download Python from [https://www.python.org/downloads/](https://www.python.org/downloads/) (check **“Add Python to PATH”**).
   - Install [FFmpeg](https://www.gyan.dev/ffmpeg/builds/) and [eSpeak‑NG](https://github.com/espeak-ng/espeak-ng/releases) and add both to your **PATH**.

2. **Install Python libraries**

   ```powershell
   pip install speechrecognition requests piper-tts
   ```

3. **Download the Piper model**

   ```powershell
   $modelPath = "$env:USERPROFILE\piper_models\en_US\lessac\medium"
   New-Item -Path $modelPath -ItemType Directory -Force | Out-Null
   Invoke-WebRequest -Uri "https://huggingface.co/rhasspy/piper-voices/resolve/main/en/en_US/lessac/medium/en_US-lessac-medium.onnx" -OutFile "$modelPath\en_US-lessac-medium.onnx"
   ```

4. **Add your OpenRouter API key**

   Open `nik.py` in any editor and set `OPENROUTER_API_KEY` to your key.

5. **Run Nik**

   ```powershell
   python nik.py
   ```

---

### Usage Tips

- Wake Nik by saying **“nick …”** then finish your command within two seconds.
- Examples:
  - `Nick, open Gmail`
  - `Nick, open a website with baseball stats`
  - `Nick, what’s the capital of Australia?`
- If Nik can’t find the requested URL it will tell you so.

---

### Troubleshooting

| Issue                   | Fix                                                                   |
| ----------------------- | --------------------------------------------------------------------- |
| No audio out / in       | Check `alsamixer` (Linux) or sound settings (Windows)                 |
| `pyaudio` install error | Linux: `sudo apt install portaudio19-dev` then `pip install pyaudio`  |
| Chromium doesn’t open   | Verify the path in `chromium_open()` matches `which chromium-browser` |

---

Enjoy chatting with **Nik**!

