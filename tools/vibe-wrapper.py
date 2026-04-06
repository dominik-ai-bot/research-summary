# VibeVoice TTS Wrapper Tool
# Local offline TTS using Microsoft VibeVoice
# No API key required - uses local ONNX or Python model

# What this tool does:
# 1. Checks if VibeVoice is downloaded in your workspace
# 2. Downloads it if needed (or guides you to download)
# 3. Runs VibeVoice to generate speech from text
# 4. Saves audio file to your workspace
# 5. Generates text transcription for reference

# Requirements:
# - Windows: WSL2 with Python 3.10+
# - MacOS: Python 3.10+ with Homebrew packages
# - Linux: Python 3.10+ with pip

# Installation:
# This script will guide you through installation and setup

# Usage:
# python3 vibe-wrapper.py "Your text here"
# Output: workspace/voice-notes/YYYY-MM-DD_HHMMSS.wav
# Transcript: workspace/voice-notes/YYYY-MM-DD_HHMMSS_transcript.txt

# Voice Notes vs. Research Summaries:
#
# Voice notes (audio files) are local only - they're stored in your workspace and not distributed anywhere.
#
# Research summaries are at https://dominik-ai-bot.github.io/research-summary/ - these are publicly accessible via GitHub Pages.
#
# For automated voice note distribution to GitHub Pages:
# 1. Create a simple static page: workspace/voice-notes/index.html
# 2. Use GitHub Actions to auto-generate list of voice notes
# 3. Voice notes are local files - this means you control distribution
#    and no API keys or cloud dependencies
#    You can listen to them anytime, upload to GitHub Pages when ready

# Installation:

# On Windows (WSL2):
#   ```powershell
#   # Install VibeVoice
#   cd C:\Users\dominik\.openclaw\workspace\tools
#   git clone https://github.com/microsoft/VibeVoice.git
#   cd VibeVoice
#   pip install -r requirements.txt
#   ```

# On MacOS:
#   ```bash
#   brew install python-tk
#   pip install onnxruntime
#   pip install https://github.com/microsoft/VibeVoice/releases/download/python/v1/vibe.whl
#   ```

# On Linux:
#   ```bash
#   pip install onnxruntime
#   pip install https://github.com/microsoft/VibeVoice/releases/download/python/v1/vibe.whl
#   ```

import subprocess
import sys
import os
import datetime
from pathlib import Path

def main():
    if len(sys.argv) < 2:
        print("Usage: python vibe-wrapper.py \"Your text here\"")
        print("Output: workspace/voice-notes/YYYY-MM-DD_HHMMSS.wav")
        sys.exit(1)
    
    text = sys.argv[1]
    
    # Workspace paths
    workspace = Path.home() / ".openclaw" / "workspace"
    voice_dir = workspace / "voice-notes"
    voice_dir.mkdir(parents=True, exist_ok=True)
    
    # Create timestamped filename
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d_%H%M%S")
    wav_filename = voice_dir / f"{timestamp}.wav"
    txt_filename = voice_dir / f"{timestamp}_transcript.txt"
    
    # Check if VibeVoice exists
    vibe_path = workspace / "tools" / "VibeVoice"
    
    if not vibe_path.exists():
        print("⚠️  VibeVoice not found in workspace/tools/VibeVoice/")
        print("📥 Please download VibeVoice from GitHub:")
        print("   GitHub: https://github.com/microsoft/VibeVoice")
        print("")
        print("Installation options:")
        print("   Option 1 (Python pip):")
        print("   ```bash")
        print("   pip install https://github.com/microsoft/VibeVoice/releases/download/python/v1/vibe.whl")
        print("   ```")
        print("")
        print("   Option 2 (Python source):")
        print("   ```bash")
        print("   git clone https://github.com/microsoft/VibeVoice.git")
        print("   pip install -r VibeVoice/requirements.txt")
        print("   python3 -m vibe --text \"Your text\" --output audio.wav")
        print("   ```")
        print("")
        print("After installation, run this tool again to generate audio.")
        sys.exit(1)
    
    # Try to use VibeVoice (will try Python import first, then CLI)
    try:
        print(f"🎤 Generating audio from: {text[:100]}...")
        
        # Method 1: Try Python package import
        import importlib
        spec = importlib.util.find_spec("vibe")
        if spec:
            print("✅ Using VibeVoice Python package")
            try:
                from vibe import generate_audio
                generate_audio(text, output=str(wav_filename))
            except ImportError:
                print("⚠️  VibeVoice package found but failed to import")
                print("   Trying CLI method instead...")
                spec = None
        else:
            print("📦 VibeVoice Python package not installed")
            print("   Trying CLI method...")
        
        # Method 2: Use CLI if package not available
        if spec is None:
            try:
                result = subprocess.run(
                    ["python3", "-m", "vibe", "--text", text, "--output", str(wav_filename)],
                    cwd=vibe_path,
                    capture_output=True,
                    text=True,
                    timeout=120
                )
                
                if result.returncode == 0:
                    print(f"✅ Audio generated: {wav_filename.name}")
                    print(f"📄 Transcript saved: {txt_filename.name}")
                else:
                    print(f"❌ VibeVoice CLI failed with return code: {result.returncode}")
                    print(f"   Error: {result.stderr}")
                    sys.exit(1)
                    
            except subprocess.TimeoutExpired:
                print("❌ VibeVoice timed out (2 minutes max)")
                sys.exit(1)
            except FileNotFoundError:
                print("⚠️  VibeVoice command not found - ensure installation")
                sys.exit(1)
            except Exception as e:
                print(f"❌ Unexpected error: {e}")
                print("   Trying basic generation method...")
                result = subprocess.run(
                    ["python3", "-c", f"from vibe import generate_audio; generate_audio({repr(text)}, '{str(wav_filename)}')"],
                    cwd=vibe_path,
                    capture_output=True,
                    text=True,
                    timeout=120
                )
                
                if result.returncode == 0:
                    print(f"✅ Audio generated (basic method): {wav_filename.name}")
                else:
                    print(f"❌ Basic method also failed")
                    sys.exit(1)
    
    # Generate text transcript (for reference)
    txt_content = f"""Voice Note - {timestamp}
Source: Design (OpenClaw AI Agent)
Text: {text}

Generated using Microsoft VibeVoice TTS - local offline operation

To listen: Open the audio file in any audio player
To reference: Use the transcript file above
"""
    
    with open(txt_filename, "w", encoding="utf-8") as f:
        f.write(txt_content)
    
    print(f"\n🎤 SUCCESS!")
    print(f"📁 Audio: {wav_filename}")
    print(f"📄 Transcript: {txt_filename}")
    print(f"\n💡 To upload to GitHub Pages:")
    print(f"   1. Create: workspace/voice-notes/index.html")
    print(f"   2. Upload: {wav_filename.name} and {txt_filename.name}")
    print(f"   3. Or manually copy files to GitHub Pages repo")
    print(f"\n🔗 Research summaries: https://dominik-ai-bot.github.io/research-summary/")
    print(f"\n📝 Tip: Voice notes are LOCAL files - you control when to share them")

if __name__ == "__main__":
    main()
