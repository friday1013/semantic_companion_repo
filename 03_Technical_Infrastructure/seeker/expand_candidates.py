#!/usr/bin/env python3
"""
Expand v1 — explodes each model's size tags into individual,
hardware-fit-tagged candidate rows.

VRAM/RAM estimate is a heuristic for Q4-class quantization:
  estimated_gb ~= params_b * 0.6 * 1.15  (15% headroom for KV cache)
An approximation for triage, not a promise — actual footprint
depends on quant level and context length. Confirm a borderline
fit with a real `ollama pull` + `ollama ps`, don't trust this alone.

Machine budgets (GB), headroom already subtracted:
  athena    : 11   (RTX A2000 12GB, shared with Heimdall/Arion/OI)
  cambridge : 22   (RTX 4500 Ada 24GB)
  shaoshi   : 22   (TITAN RTX 24GB — runs CAP today, treat as busy)
  foundry   : 46   (RTX A6000 48GB — VPN peer not yet live)
  mars      : 100  (no real GPU; RAM-bound CPU offload, 128GB RAM)
"""
import json, re

IN_PATH = "/mnt/seagate/SemanticCrew/Tools/seeker/candidates_20260617.json"
OUT_PATH = "/mnt/seagate/SemanticCrew/Tools/seeker/candidates_expanded_20260617.json"

BUDGETS = {"athena": 11, "cambridge": 22, "shaoshi": 22, "foundry": 46, "mars": 100}
LABELS = {"shaoshi": "shaoshi (busy: CAP)", "foundry": "foundry (VPN pending)",
          "mars": "mars (slow, CPU-only)"}

TAG_RE = re.compile(r"(\d+(?:\.\d+)?)\s*b", re.IGNORECASE)


def estimate_gb(params_b):
    if params_b is None:
        return None
    return round(params_b * 0.6 * 1.15, 1)


def fits(est_gb):
    if est_gb is None:
        return []
    return [LABELS.get(m, m) for m, budget in BUDGETS.items() if est_gb <= budget]


def explode_ollama(rows):
    out = []
    for r in rows:
        tags = r.get("size_tags") or []
        if not tags:
            out.append({"source": r["source"], "id": r["id"], "variant": None,
                         "name": r["name"], "params_b": None, "est_gb": None,
                         "fits": [], "pulls": r.get("pulls"), "url": r.get("url")})
            continue
        for t in tags:
            m = TAG_RE.search(t)
            pb = float(m.group(1)) if m else None
            est = estimate_gb(pb)
            out.append({
                "source": r["source"], "id": r["id"], "variant": f'{r["id"]}:{t}',
                "name": r["name"], "description": r.get("description"),
                "capabilities": r.get("capabilities"), "params_b": pb,
                "est_gb": est, "fits": fits(est), "pulls": r.get("pulls"),
                "url": r.get("url"),
            })
    return out


def pass_through_hf(rows):
    out = []
    for r in rows:
        pb = r.get("params_b_guess")
        est = estimate_gb(pb)
        out.append({
            "source": r["source"], "id": r["id"], "variant": r["id"],
            "name": r["name"], "capabilities": r.get("size_tags", []),
            "params_b": pb, "est_gb": est,
            "fits": fits(est), "downloads": r.get("downloads"),
            "likes": r.get("likes"), "url": r.get("url"),
        })
    return out


def main():
    d = json.load(open(IN_PATH))
    expanded = {
        "ollama_library": explode_ollama(d.get("ollama_library", [])),
        "huggingface_gguf": pass_through_hf(d.get("huggingface_gguf", [])),
    }
    json.dump(expanded, open(OUT_PATH, "w"), indent=2)

    for src, rows in expanded.items():
        athena_ok = [r for r in rows if r["fits"] and "athena" in r["fits"]]
        unknown = [r for r in rows if r["params_b"] is None]
        print(f"--- {src}: {len(rows)} variant rows ---")
        print(f"  fit Athena (<=11GB est): {len(athena_ok)}")
        print(f"  size unparseable:        {len(unknown)}")
    print(f"written: {OUT_PATH}")


if __name__ == "__main__":
    main()
