#!/usr/bin/env python3
"""
Seeker v1 — candidate model finder.

Queries two registries for local-model candidates:
  - ollama.com/library : official catalog, scraped directly (server-
    rendered HTML; ollamadb.dev's community mirror API was tried
    first but its hostname does not resolve from Athena's DNS — the
    site itself is reachable from elsewhere, so this is a local
    network quirk, not a dead project. Worth a look later.)
  - huggingface.co : models tagged "gguf", sorted by downloads

Honest about its own limits: size-in-billions is parsed heuristically
from names/tags, not read from real metadata. "Popularity" is a proxy
for "actively maintained," not for honesty or quality — screening for
those properties is the test battery's job, not this script's.
"""
import json, os, re, time
import requests

OUT_DIR = "/mnt/seagate/SemanticCrew/Tools/seeker"
OUT_PATH = os.path.join(OUT_DIR, "candidates_20260617.json")

SIZE_RE = re.compile(r"(\d+(?:\.\d+)?)\s*[bB](?![a-zA-Z])")


def tier(params_b):
    if params_b is None:
        return "unknown"
    if params_b <= 8:
        return "small (<=8B)"
    if params_b <= 24:
        return "mid (9-24B)"
    if params_b <= 70:
        return "large (25-70B)"
    return "very large (>70B)"


def parse_size(text):
    sizes = [float(m) for m in SIZE_RE.findall(text or "")]
    return max(sizes) if sizes else None


def fetch_ollama_catalog():
    url = "https://ollama.com/library"
    r = requests.get(url, timeout=20)
    r.raise_for_status()
    html = r.text

    blocks = re.split(r'<a href="/library/', html)[1:]
    out = []
    for block in blocks:
        id_m = re.match(r'([a-zA-Z0-9_.-]+)"', block)
        if not id_m:
            continue
        model_id = id_m.group(1)
        title_m = re.search(r'x-test-model-title title="([^"]*)"', block)
        desc_m = re.search(r'<p class="max-w-lg[^"]*">([^<]*)</p>', block)
        caps = re.findall(r'x-test-capability[^>]*>([^<]+)</span>', block)
        sizes = re.findall(r'x-test-size[^>]*>([^<]+)</span>', block)
        pulls_m = re.search(r'x-test-pull-count>([^<]+)</span>', block)
        size_guess = parse_size(" ".join(sizes)) or parse_size(model_id)
        out.append({
            "source": "ollama_library",
            "id": model_id,
            "name": (title_m.group(1) if title_m else model_id),
            "description": (desc_m.group(1).strip() if desc_m else None),
            "capabilities": caps,
            "size_tags": sizes,
            "params_b_guess": size_guess,
            "tier": tier(size_guess),
            "pulls": (pulls_m.group(1) if pulls_m else None),
            "url": f"https://ollama.com/library/{model_id}",
        })
    return out


def fetch_hf_gguf(limit=60):
    url = "https://huggingface.co/api/models"
    params = {"filter": "gguf", "sort": "downloads", "direction": -1, "limit": limit}
    r = requests.get(url, params=params, timeout=15)
    r.raise_for_status()
    data = r.json()
    out = []
    for m in data:
        mid = m.get("id", "")
        size_guess = parse_size(mid)
        out.append({
            "source": "huggingface_gguf",
            "id": mid,
            "name": mid.split("/")[-1] if "/" in mid else mid,
            "size_tags": m.get("tags", []),
            "params_b_guess": size_guess,
            "tier": tier(size_guess),
            "downloads": m.get("downloads"),
            "likes": m.get("likes"),
            "last_updated": m.get("lastModified"),
            "url": f"https://huggingface.co/{mid}",
        })
    return out


def main():
    os.makedirs(OUT_DIR, exist_ok=True)
    catalog = {"fetched_at_utc": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())}

    try:
        catalog["ollama_library"] = fetch_ollama_catalog()
    except Exception as e:
        catalog["ollama_library_error"] = str(e)

    try:
        catalog["huggingface_gguf"] = fetch_hf_gguf()
    except Exception as e:
        catalog["huggingface_gguf_error"] = str(e)

    with open(OUT_PATH, "w") as f:
        json.dump(catalog, f, indent=2)

    n1 = len(catalog.get("ollama_library", []))
    n2 = len(catalog.get("huggingface_gguf", []))
    print(f"ollama_library candidates: {n1}")
    print(f"huggingface_gguf candidates: {n2}")
    print(f"written: {OUT_PATH}")


if __name__ == "__main__":
    main()
