#!/usr/bin/env python3
"""Bakes the real candidate data into template.html -> model_manifest.html.
No placeholder/sample data — this embeds the actual catalog produced by
find_candidates.py and expand_candidates.py."""
import json

BASE = "/mnt/seagate/SemanticCrew/Tools/seeker"
data = json.load(open(f"{BASE}/candidates_expanded_20260617.json"))
template = open(f"{BASE}/template.html").read()
out = template.replace("{{DATA_JSON}}", json.dumps(data, separators=(",", ":")))
open(f"{BASE}/model_manifest.html", "w").write(out)
print(f"wrote {BASE}/model_manifest.html ({len(out)} bytes)")
