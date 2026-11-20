#!/usr/bin/env python3
"""Entry program: copy the pre-built front page to the grader's output directory.

The image was rendered offline by render.py (Pillow, deterministic). The judge
sees exactly these bytes; this program only moves them, per the bounty's
simplest-entry rule. Outside the grader, MAKEFUN_OUTPUT_DIR stands in for /output.
"""
import os
import shutil

src = os.path.join(os.path.dirname(os.path.abspath(__file__)), "entry.png")
out = os.environ.get("MAKEFUN_OUTPUT_DIR", "/output")
os.makedirs(out, exist_ok=True)
shutil.copyfile(src, os.path.join(out, "entry.png"))
