"""Create a dated real-source sample using the running API. Does not fetch publishers."""
import argparse
import json
from pathlib import Path
import httpx


def seed(api_url):
    root = Path(__file__).resolve().parents[1]
    sources = json.loads((root / "docs/sample_sources.json").read_text(encoding="utf-8"))
    newsletter = (root / "docs/SAMPLE_NEWSLETTER.md").read_text(encoding="utf-8")
    with httpx.Client(base_url=api_url.rstrip("/") + "/api", timeout=20) as client:
        result = client.post("/projects", json={"title": "gpt-oss: an August 2025 retrospective"})
        result.raise_for_status()
        pid = result.json()["id"]
        for source in sources:
            result = client.post(f"/projects/{pid}/sources", json=source)
            result.raise_for_status()
        result = client.post(f"/projects/{pid}/brief")
        result.raise_for_status()
        result = client.put(f"/projects/{pid}/draft", json={"text": newsletter})
        result.raise_for_status()
    print(f"Created sample project {pid}. Source input consists of attributed editorial paraphrases.")


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--api-url", default="http://127.0.0.1:8000")
    args = parser.parse_args()
    seed(args.api_url)


if __name__ == "__main__":
    main()
