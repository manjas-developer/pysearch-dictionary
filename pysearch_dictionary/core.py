import json
from pathlib import Path
import sys
import threading
import urllib.request

# ⚙️ Configuration (Set your repo details)
GITHUB_REPO = "manjas-developer/pysearch-dictionary"
GITHUB_TOKEN = "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"  # Optional: token for creating automated issue reports

# Load embedded offline dictionary
DATA_FILE = Path(__file__).parent / "data.json"
try:
  with open(DATA_FILE, "r", encoding="utf-8") as f:
    DICTIONARY = json.load(f)
except Exception:
  DICTIONARY = {}


def _log_missing_word(word: str) -> None:
  """Silently logs an issue to GitHub without blocking execution 🚀"""
  if not GITHUB_TOKEN or not GITHUB_REPO or "YOUR_USERNAME" in GITHUB_REPO:
    return

  try:
    url = f"https://api.github.com/repos/{GITHUB_REPO}/issues"
    payload = json.dumps({
        "title": f"Missing word: {word}",
        "body": (
            f"The word **`{word}`** was requested but not found in the"
            " dictionary."
        ),
        "labels": ["missing-word"],
    }).encode("utf-8")

    req = urllib.request.Request(
        url,
        data=payload,
        headers={
            "Authorization": f"Bearer {GITHUB_TOKEN}",
            "Accept": "application/vnd.github+json",
            "Content-Type": "application/json",
            "User-Agent": "pysearch-dictionary-client",
        },
        method="POST",
    )
    urllib.request.urlopen(req, timeout=2)
  except Exception:
    pass  # Never disrupt user workflow 🛡️


def translate(word: str) -> str:
  """Translates an English word to Hindi 🔍"""
  if not isinstance(word, str):
    return "अमान्य इनपुट (Invalid input)"

  cleaned = word.strip().lower()

  if cleaned in DICTIONARY:
    return DICTIONARY[cleaned]

  # Trigger background logging thread 🕵️‍♂️
  threading.Thread(
      target=_log_missing_word, args=(cleaned,), daemon=True
  ).start()
  return "शब्द नहीं मिला (Word not found)"


def main():
  """CLI entry point for running directly from terminal 💻✨"""
  if len(sys.argv) > 1:
    word = " ".join(sys.argv[1:])
    print(translate(word))
  else:
    print("Usage: pysearch-dictionary <word> 📖")


if __name__ == "__main__":
  main()
