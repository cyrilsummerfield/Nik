import os
import re
import time
import webbrowser
import speech_recognition as sr
import subprocess
import requests

# ---------- CONFIG ----------
OPENROUTER_API_KEY = "your-api-key-here"
MODEL = "openai/gpt-3.5-turbo"
WAKE_WORD = "nick"
PIPER_MODEL_PATH = "/home/evilowl/piper_models/en_US/lessac/medium/en_US-lessac-medium.onnx"
# ----------------------------

def speak(text):
    print(f"Nik: {text}")
    try:
        subprocess.run(
            f'echo "{text}" | piper --model {PIPER_MODEL_PATH} --output-raw | aplay -r 22050 -f S16_LE -t raw -',
            shell=True
        )
    except Exception as e:
        print(f"Speech error: {e}")

def listen_once():
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        try:
            audio = recognizer.listen(source, timeout=8)
            text = recognizer.recognize_google(audio)
            print(f"You said: {text}")
            return text.lower()
        except sr.UnknownValueError:
            return ""
        except sr.WaitTimeoutError:
            return ""

def send_to_llm(prompt):
    headers = {
        "Authorization": f"Bearer {OPENROUTER_API_KEY}",
        "Content-Type": "application/json"
    }

    messages = [{"role": "user", "content": prompt}]
    try:
        response = requests.post("https://openrouter.ai/api/v1/chat/completions", headers=headers, json={
            "model": MODEL,
            "messages": messages
        })
        return response.json()["choices"][0]["message"]["content"].strip()
    except Exception as e:
        print(f"Error: {e}")
        return "Sorry, I couldn't reach the AI."

def extract_exact_url(text):
    match = re.match(r"^https?://[a-zA-Z0-9\-_.]+\.[a-z]{2,}.*$", text.strip())
    return match.group(0) if match else None

def chromium_open(url):
    try:
        chromium_path = "/usr/bin/chromium-browser"
        webbrowser.get(f"{chromium_path} %s").open(url)
    except webbrowser.Error:
        speak("Couldn't open Chromium. Please check if it's installed.")

def main():
    speak("Tesla is online.")
    while True:
        heard = listen_once()
        if WAKE_WORD in heard:
            time.sleep(2)
            command = heard.split(WAKE_WORD, 1)[1].strip()
            if not command:
                speak("Say a full command after my name.")
                continue

            if command.startswith("open "):
                site = command[5:].strip()
                prompt = f"What is the URL to {site}? Respond with the URL and nothing more."
                url_response = send_to_llm(prompt)
                url = extract_exact_url(url_response)
                if url:
                    speak("Opening website.")
                    chromium_open(url)
                    continue
                else:
                    speak("I couldn't find the URL.")
                    continue

            # fallback for non-"open" commands
            response = send_to_llm(command)
            speak(response)

        time.sleep(1)

if __name__ == "__main__":
    main()
