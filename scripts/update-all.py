#!/usr/bin/env python3
"""Run every generator/consistency tool in the right order.

Usage:  python3 scripts/update-all.py

Order matters: site constants first (values), then physicians (roster
surfaces), then chrome (shared blocks rendered from both).
"""
import subprocess, sys, pathlib

TOOLS = ["update-site.py", "update-physicians.py", "update-chrome.py"]
here = pathlib.Path(__file__).resolve().parent
for t in TOOLS:
    print(f"== {t} ==")
    r = subprocess.run([sys.executable, str(here / t)])
    if r.returncode:
        sys.exit(r.returncode)
print("== all tools passed ==")
