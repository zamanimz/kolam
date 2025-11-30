#!/usr/bin/env python3
"""Run backend and frontend from repo root.

Usage examples:
  python run.py             # runs both backend and frontend
  python run.py --backend   # run only backend
  python run.py --frontend  # run only frontend
  python run.py --open      # open UI in browser after starting

This script is designed for Windows PowerShell and Unix shells.
"""
from __future__ import annotations

import argparse
import os
import signal
import subprocess
import sys
import time
import webbrowser
from pathlib import Path

ROOT = Path(__file__).resolve().parent
BACKEND_DIR = ROOT / "backend"
FRONTEND_DIR = ROOT / "frontend" / "pond-ui"


def start_backend(port: int) -> subprocess.Popen:
    env = os.environ.copy()
    # Tell flask where the app is
    env["FLASK_APP"] = str(BACKEND_DIR / "app.py")
    env["PYTHONUNBUFFERED"] = "1"

    cmd = [sys.executable, "-m", "flask", "run", "--host", "127.0.0.1", "--port", str(port)]
    print(f"Starting backend: {' '.join(cmd)} (FLASK_APP={env['FLASK_APP']})")
    return subprocess.Popen(cmd, cwd=str(ROOT), env=env)


def start_frontend(port: int) -> subprocess.Popen:
    # We pass through environment; vite will default to its own port (usually 5173)
    # If users want a different port they can pass it through npm scripts or env vars.
    cmd = ["npm", "run", "dev"]
    print(f"Starting frontend: {' '.join(cmd)} in {FRONTEND_DIR}")
    return subprocess.Popen(cmd, cwd=str(FRONTEND_DIR), env=os.environ.copy())


def kill_process(p: subprocess.Popen) -> None:
    if p is None:
        return
    try:
        print(f"Stopping pid {p.pid}")
        p.terminate()
        # give it a moment
        for _ in range(10):
            if p.poll() is not None:
                break
            time.sleep(0.2)
        else:
            p.kill()
    except Exception:
        pass


def main() -> int:
    parser = argparse.ArgumentParser(description="Run backend and frontend for this repo.")
    group = parser.add_mutually_exclusive_group()
    group.add_argument("--backend", action="store_true", help="Run only the backend")
    group.add_argument("--frontend", action="store_true", help="Run only the frontend")
    parser.add_argument("--backend-port", type=int, default=5000, help="Backend port (default: 5000)")
    parser.add_argument("--ui-port", type=int, default=5173, help="Frontend dev server port (default: 5173)")
    parser.add_argument("--open", action="store_true", help="Open the UI in the default browser after start")

    args = parser.parse_args()

    run_backend = args.backend or not args.frontend
    run_frontend = args.frontend or not args.backend

    procs = []

    try:
        if run_backend:
            p = start_backend(args.backend_port)
            procs.append(("backend", p, args.backend_port))

        if run_frontend:
            p = start_frontend(args.ui_port)
            procs.append(("frontend", p, args.ui_port))

        # Optionally open the UI after a short delay so the dev server can start
        if args.open and run_frontend:
            url = f"http://127.0.0.1:{args.ui_port}"
            print(f"Opening {url} in default browser...")
            # give the server a second to bind
            time.sleep(1.5)
            webbrowser.open(url)

        # Wait for child processes. If any exits, shutdown the others.
        while True:
            for name, p, _port in procs:
                ret = p.poll()
                if ret is not None:
                    print(f"{name} exited with code {ret}, shutting down remaining processes.")
                    raise KeyboardInterrupt
            time.sleep(0.2)

    except KeyboardInterrupt:
        print("Shutting down services...")
        for _name, p, _ in procs:
            kill_process(p)
        return 0


if __name__ == "__main__":
    raise SystemExit(main())
