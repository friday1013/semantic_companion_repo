#!/usr/bin/env bash
# session_writer_install.sh
# Install session_writer on a new machine.
# Portable version — works on any Linux or macOS with Python 3.10+
#
# Usage:
#   bash session_writer_install.sh           # basic install
#   bash session_writer_install.sh --systemd # also install systemd user service

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
BIN_DIR="$HOME/bin"
CONFIG_PATH="$HOME/.config/session_writer/config.toml"
LOCAL_CONF="$SCRIPT_DIR/session_writer.conf"

INSTALL_SYSTEMD=false
for arg in "$@"; do
    [[ "$arg" == "--systemd" ]] && INSTALL_SYSTEMD=true
done

# ─────────────────────────────────────────────────────────────
# Output helpers
# ─────────────────────────────────────────────────────────────
ok()   { echo "  ✓ $*"; }
warn() { echo "  ! $*"; }
fail() { echo "  ✗ $*"; }
step() { echo ""; echo "--- $* ---"; }

echo ""
echo "=== session_writer install ==="
echo ""

# ─────────────────────────────────────────────────────────────
# 1. Python check (3.10+)
# ─────────────────────────────────────────────────────────────
step "Python"

PYTHON=$(command -v python3 || true)
if [[ -z "$PYTHON" ]]; then
    fail "python3 not found in PATH — install Python 3.10+ first"
    exit 1
fi

PYMAJ=$("$PYTHON" -c "import sys; print(sys.version_info.major)")
PYMIN=$("$PYTHON" -c "import sys; print(sys.version_info.minor)")
PYVER="${PYMAJ}.${PYMIN}"

if [[ "$PYMAJ" -lt 3 ]] || { [[ "$PYMAJ" -eq 3 ]] && [[ "$PYMIN" -lt 10 ]]; }; then
    fail "Python 3.10+ required (found $PYVER)"
    exit 1
fi
ok "Python $PYVER"

# ─────────────────────────────────────────────────────────────
# 2. Check for source files
# ─────────────────────────────────────────────────────────────
step "Source files"

for f in session_writer.py session_writer_setup.py; do
    if [[ -f "$SCRIPT_DIR/$f" ]]; then
        ok "$f found"
    else
        fail "$f not found in $SCRIPT_DIR"
        exit 1
    fi
done

# ─────────────────────────────────────────────────────────────
# 3. Optional: install watchdog
# watchdog enables filesystem event triggers (in addition to timer).
# Without it, timer-only mode works fine.
# ─────────────────────────────────────────────────────────────
step "watchdog (optional — filesystem event triggers)"

if "$PYTHON" -c "import watchdog" 2>/dev/null; then
    ok "watchdog already installed"
else
    warn "watchdog not installed — attempting pip3 install..."
    # --break-system-packages needed on Ubuntu 23.04+/Debian 12+ with externally-managed Python
    if pip3 install watchdog --quiet --break-system-packages 2>/dev/null || \
       pip3 install watchdog --quiet 2>/dev/null; then
        ok "watchdog installed"
    else
        warn "watchdog install failed — timer-only mode will be used"
        warn "You can install it later with: pip3 install watchdog"
    fi
fi

# ─────────────────────────────────────────────────────────────
# 4. Install scripts to ~/bin
# ─────────────────────────────────────────────────────────────
step "Install to ~/bin"

mkdir -p "$BIN_DIR"

cp "$SCRIPT_DIR/session_writer.py"       "$BIN_DIR/session_writer.py"
cp "$SCRIPT_DIR/session_writer_setup.py" "$BIN_DIR/session_writer_setup.py"
chmod +x "$BIN_DIR/session_writer.py" "$BIN_DIR/session_writer_setup.py"
ok "Installed to $BIN_DIR"

if [[ ":$PATH:" != *":$HOME/bin:"* ]]; then
    warn "~/bin is not in your PATH — add this to ~/.bashrc:"
    warn "  export PATH=\"\$HOME/bin:\$PATH\""
fi

# ─────────────────────────────────────────────────────────────
# 5. Config setup
# Check for existing config. If none found, run the setup wizard.
# The wizard creates ~/.config/session_writer/config.toml interactively.
# ─────────────────────────────────────────────────────────────
step "Config"

if [[ -f "$CONFIG_PATH" ]]; then
    ok "Config found at $CONFIG_PATH — skipping setup wizard"
elif [[ -f "$LOCAL_CONF" ]]; then
    ok "Local config found at $LOCAL_CONF — skipping setup wizard"
else
    warn "No config file found — running setup wizard now"
    echo ""
    "$PYTHON" "$BIN_DIR/session_writer_setup.py"
    # Wizard exits with 0 regardless of whether user cancelled,
    # so we just check if the file exists after.
    if [[ -f "$CONFIG_PATH" ]]; then
        ok "Config written by wizard"
    else
        warn "Config not written (wizard cancelled or skipped)"
        warn "Run later with: python3 session_writer_setup.py"
    fi
fi

# ─────────────────────────────────────────────────────────────
# 6. Shell alias instructions
# We print but do NOT write to ~/.bashrc automatically — that's too invasive.
# Let the user add it deliberately.
# ─────────────────────────────────────────────────────────────
step "Shell alias"

# Determine inbox path from config if possible
INBOX_PATH="~/session_notes/session_inbox.md"  # fallback
if [[ -f "$CONFIG_PATH" ]]; then
    RAW_BASE=$(grep '^base_dir' "$CONFIG_PATH" 2>/dev/null | head -1 | \
               sed 's/.*= *"\(.*\)"/\1/' | sed "s/.*= *'\(.*\)'/\1/")
    if [[ -n "$RAW_BASE" ]]; then
        INBOX_PATH="${RAW_BASE}/session_inbox.md"
    fi
fi

echo ""
echo "  Add this alias to ~/.bashrc:"
echo ""
echo "    # session_writer inbox — append tagged lines"
echo "    sw() { echo \"\$*\" >> $INBOX_PATH; }"
echo ""
echo "  Then use it:"
echo "    sw [DECISION] we chose approach A"
echo "    sw [PENDING] follow up with Chris"
echo "    sw [FLAG] compaction event at 85%"
echo "    sw [WORK] VPN setup | blocked | waiting on CA cert"

# ─────────────────────────────────────────────────────────────
# 7. Optional: systemd user service
# ─────────────────────────────────────────────────────────────
if $INSTALL_SYSTEMD; then
    step "systemd user service"

    SYSTEMD_DIR="$HOME/.config/systemd/user"
    SERVICE_FILE="$SYSTEMD_DIR/session_writer.service"
    mkdir -p "$SYSTEMD_DIR"

    cat > "$SERVICE_FILE" << EOF
[Unit]
Description=Session Writer — autonomous session state daemon
Documentation=file://$BIN_DIR/README.md
After=local-fs.target

[Service]
Type=simple
ExecStart=$PYTHON $BIN_DIR/session_writer.py --foreground
Restart=on-failure
RestartSec=30
StandardOutput=journal
StandardError=journal
Environment=SEMANTIC_SESSION=unknown

[Install]
WantedBy=default.target
EOF

    systemctl --user daemon-reload 2>/dev/null || true
    ok "Service file written: $SERVICE_FILE"

    echo ""
    echo "  To enable and start:"
    echo "    SEMANTIC_SESSION=MyProject-N1 systemctl --user start session_writer"
    echo "    systemctl --user enable session_writer  # start on login"
    echo ""
    echo "  To view logs:"
    echo "    journalctl --user -u session_writer -f"
fi

# ─────────────────────────────────────────────────────────────
# 8. Final summary
# ─────────────────────────────────────────────────────────────
step "Done"

echo ""
echo "  Quick start:"
echo "    export SEMANTIC_SESSION=MyProject-N1"
echo "    python3 $BIN_DIR/session_writer.py --start"
echo "    python3 $BIN_DIR/session_writer.py --status"
echo "    python3 $BIN_DIR/session_writer.py --checkpoint"
echo "    python3 $BIN_DIR/session_writer.py --stop"
echo ""
echo "  Config:  $CONFIG_PATH"
echo "  Docs:    $SCRIPT_DIR/README.md"
echo ""
