"""Test against a disposable database and separate ports; never mutate the user's workspace."""
import argparse
import os
from pathlib import Path
import shutil
import site
import subprocess
import sys
import tempfile
import time
import urllib.request

ROOT = Path(__file__).resolve().parents[1]


def wait_for(url, child):
    for _ in range(120):
        if child.poll() is not None:
            raise RuntimeError("A test server exited before readiness.")
        try:
            with urllib.request.urlopen(url, timeout=1) as response:
                if response.status == 200:
                    return
        except Exception:
            time.sleep(0.25)
    raise RuntimeError("A test server did not become ready within 30 seconds.")


def stop(child):
    if child and child.poll() is None:
        if os.name == "nt":
            subprocess.run(["taskkill", "/PID", str(child.pid), "/T", "/F"], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        else:
            child.terminate()
        try:
            child.wait(timeout=5)
        except subprocess.TimeoutExpired:
            child.kill()
            child.wait()


def verify(api_port, web_port):
    node = shutil.which("node")
    if not node:
        raise RuntimeError("Node.js is required for browser verification.")
    api = web = None
    with tempfile.TemporaryDirectory(prefix="fieldnotes-verify-") as temp:
        env = {**os.environ, "DATABASE_URL": "sqlite:///" + (Path(temp) / "verify.db").as_posix(),
               "GEMINI_API_KEY": "", "WORKSPACE_PASSWORD": "", "SESSION_SECRET": "", "VERCEL": "",
               "VITE_API_URL": f"http://127.0.0.1:{api_port}", "CORS_ORIGINS": f"http://127.0.0.1:{web_port}",
               "PYTHONPATH": os.pathsep.join(site.getsitepackages()),
               "PLAYWRIGHT_BASE_URL": f"http://127.0.0.1:{web_port}", "PLAYWRIGHT_EXTERNAL_SERVER": "1"}
        subprocess.run([sys.executable, "-m", "alembic", "upgrade", "head"], cwd=ROOT / "backend", env=env, check=True)
        with open(ROOT / "verification-api.log", "w", encoding="utf-8") as api_log, open(ROOT / "verification-web.log", "w", encoding="utf-8") as web_log:
            try:
                api = subprocess.Popen([getattr(sys, "_base_executable", sys.executable), "-m", "uvicorn", "app.main:app", "--host", "127.0.0.1", "--port", str(api_port)], cwd=ROOT / "backend", env=env, stdout=api_log, stderr=subprocess.STDOUT)
                web = subprocess.Popen([node, str(ROOT / "frontend/node_modules/vite/bin/vite.js"), "--host", "127.0.0.1", "--port", str(web_port), "--strictPort"], cwd=ROOT / "frontend", env=env, stdout=web_log, stderr=subprocess.STDOUT)
                wait_for(f"http://127.0.0.1:{api_port}/api/health", api)
                wait_for(f"http://127.0.0.1:{web_port}", web)
                result = subprocess.run([node, str(ROOT / "frontend/node_modules/@playwright/test/cli.js"), "test", "--workers=1"], cwd=ROOT / "frontend", env=env)
                return result.returncode
            finally:
                stop(web)
                stop(api)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--api-port", type=int, default=8001)
    parser.add_argument("--web-port", type=int, default=5174)
    args = parser.parse_args()
    return verify(args.api_port, args.web_port)


if __name__ == "__main__":
    sys.exit(main())

