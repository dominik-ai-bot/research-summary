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
# python vibe-wrapper.py "Your text here"
# Output: workspace/voice-notes/YYYY-MM-DD_HHMMSS.wav
# Transcript: workspace/voice-notes/YYYY-MM-DD_HHMMSS_transcript.txt

# For research summaries (automatic voice notes):
# The TTS output will be saved alongside your research summary pages
# You can then reference them or upload to GitHub Pages manually
