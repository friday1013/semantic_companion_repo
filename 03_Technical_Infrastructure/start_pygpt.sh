#!/bin/bash
# =============================================================================
# start_pygpt.sh — PyGPT launcher with auto-patch validation
#
# Runs patch_pygpt_local.sh (idempotent, ~1s) before launching PyGPT.
# Ensures mxbai chunk_size and idx ValueError fixes survive pip upgrades.
# Replace your normal PyGPT launch with this script.
#
# Usage: ./start_pygpt.sh [pygpt args...]
# =============================================================================

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PATCH_SCRIPT="$SCRIPT_DIR/patch_pygpt_local.sh"

if [ -f "$PATCH_SCRIPT" ]; then
    bash "$PATCH_SCRIPT" local 2>&1 | grep -v "^$"
else
    echo "WARNING: patch script not found at $PATCH_SCRIPT — skipping validation"
fi

exec pygpt "$@"
