#!/usr/bin/env python3
"""
download_mistral.py – pull the full Mistral-7B repo into a local cache.

• Reads your HF token from the HF_TOKEN env-var (recommended) or
  prompts interactively.
• Resumes if the download is interrupted.
• Uses symlinks when the installed hub version supports it.
"""

from huggingface_hub import login, snapshot_download
import os, getpass, pathlib, inspect

REPO_ID   = "mistralai/Mistral-7B-v0.1"
CACHE_DIR = pathlib.Path("/path/to/exports").expanduser()
TOKEN     = os.getenv("HF_TOKEN") or getpass.getpass("🤗  Enter HF token: ")


# 1️⃣  Persist token for future scripts/CLI calls
login(token=TOKEN, add_to_git_credential=False)

# 2️⃣  Call snapshot_download with the right signature
kwargs = dict(
    repo_id=REPO_ID,
    cache_dir=CACHE_DIR,
    resume_download=True,
    token=TOKEN,
)

# Older hub builds expect 'local_dir_use_symlinks'; newer ones accept it too.
if "local_dir_use_symlinks" in inspect.signature(snapshot_download).parameters:
    kwargs["local_dir_use_symlinks"] = "auto"   # or True / False

snapshot_download(**kwargs)
print(f"✅  Cached under: {CACHE_DIR}")
