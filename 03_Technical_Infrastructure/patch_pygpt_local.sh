#!/bin/bash
# =============================================================================
# patch_pygpt_local.sh
# Applies local patches to PyGPT's LlamaIndex vector store provider.
# Must be re-run after any `pipx upgrade pygpt-net`.
#
# Patches applied:
#   1. base.py  — Sets LlamaSettings.chunk_size=384 globally at import time.
#                 Fixes "input length exceeds context length" (HTTP 400) errors
#                 when indexing with mxbai-embed-large (512-token limit).
#                 LlamaIndex default of 1024 silently breaks local embed models.
#
#   2. simple.py — Adds ValueError fallback in get() so empty/uninitialized
#                 idx stores degrade gracefully instead of throwing
#                 "No index in storage context" on first use.
#
# Upstream status: Both issues worth reporting to PyGPT maintainer (szczyglis-dev).
#   chunk_size: genuine bug, affects any local embed model with <1024 token limit
#   ValueError: defensive fix, improves UX for new store initialization
#
# Usage:
#   ./patch_pygpt_local.sh           # patches local machine (Athena)
#   ./patch_pygpt_local.sh shaoshi   # patches remote via ssh
#   ./patch_pygpt_local.sh cambridge # patches remote via ssh
#
# Idempotent — safe to run multiple times.
# =============================================================================

set -e

TARGET=${1:-local}

PATCH_CMD=$(cat <<'ENDPATCH'
set -e
VENV_PATH="/home/hillery/.local/share/pipx/venvs/pygpt-net/lib/python3.12/site-packages/pygpt_net/provider/vector_stores"
BASE="$VENV_PATH/base.py"
SIMPLE="$VENV_PATH/simple.py"

if [ ! -f "$BASE" ]; then
    echo "ERROR: $BASE not found - is pygpt-net installed via pipx?"
    exit 1
fi

echo "=== PyGPT patch: $HOSTNAME ==="

# --- base.py: add LlamaSettings chunk_size after existing imports ---
if grep -q "LlamaSettings.chunk_size" "$BASE"; then
    echo "  base.py: already patched, skipping"
else
    python3 - "$BASE" <<'PYEOF'
import sys
path = sys.argv[1]
with open(path) as f:
    content = f.read()
old = "from llama_index.core.indices.vector_store.base import VectorStoreIndex"
new = ("from llama_index.core.indices.vector_store.base import VectorStoreIndex\n"
       "from llama_index.core.settings import Settings as LlamaSettings\n\n"
       "# mxbai-embed-large has a 512-token context limit.\n"
       "# LlamaIndex defaults to 1024-token chunks which causes HTTP 400 errors.\n"
       "# Set chunk_size=384 globally (safe margin below 512, with overlap headroom).\n"
       "LlamaSettings.chunk_size = 384\n"
       "LlamaSettings.chunk_overlap = 32")
if old not in content:
    print("ERROR: expected import line not found - PyGPT may have been updated, check manually")
    sys.exit(1)
with open(path, 'w') as f:
    f.write(content.replace(old, new, 1))
print("  base.py: chunk_size=384 patch applied")
PYEOF
fi

# --- simple.py: add ValueError fallback in get() ---
if grep -q "except ValueError" "$SIMPLE"; then
    echo "  simple.py: already patched, skipping"
else
    python3 - "$SIMPLE" <<'PYEOF'
import sys
path = sys.argv[1]
with open(path) as f:
    content = f.read()
old = ("        self.indexes[id] = load_index_from_storage(\n"
       "            storage_context,\n"
       "            llm=llm,\n"
       "            embed_model=embed_model,\n"
       "        )\n"
       "        return self.indexes[id]")
new = ("        try:\n"
       "            self.indexes[id] = load_index_from_storage(\n"
       "                storage_context,\n"
       "                llm=llm,\n"
       "                embed_model=embed_model,\n"
       "            )\n"
       "        except ValueError:\n"
       "            # Empty store (no index persisted yet) - create fresh and persist\n"
       "            self.indexes[id] = self.index_from_empty(embed_model)\n"
       "            self.indexes[id].storage_context.persist(persist_dir=path)\n"
       "        return self.indexes[id]")
if old not in content:
    print("ERROR: expected code block not found - PyGPT may have been updated, check manually")
    sys.exit(1)
with open(path, 'w') as f:
    f.write(content.replace(old, new, 1))
print("  simple.py: ValueError fallback applied")
PYEOF
fi

# Clear .pyc cache so Python picks up the changes immediately
PYCACHE="$VENV_PATH/__pycache__"
if [ -d "$PYCACHE" ]; then
    rm -f "$PYCACHE"/base*.pyc "$PYCACHE"/simple*.pyc
    echo "  __pycache__: base/simple .pyc cleared"
fi

echo "=== Done. Restart PyGPT to apply. ==="
ENDPATCH
)

if [ "$TARGET" = "local" ]; then
    eval "$PATCH_CMD"
else
    echo "=== Applying patches on $TARGET via SSH ==="
    ssh -o StrictHostKeyChecking=no "$TARGET" "bash -s" <<< "$PATCH_CMD"
fi
