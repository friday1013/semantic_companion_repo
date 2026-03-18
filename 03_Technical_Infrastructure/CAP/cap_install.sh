#!/usr/bin/env bash
# =============================================================================
# CAP Application Installer — user-space only, no sudo required
# Run AFTER cap_prereqs.sh has completed.
#
# Usage: bash cap_install.sh [options]
#
# Options:
#   --dir DIR       Install to DIR instead of ~/CAP
#   --db-pass PASS  PostgreSQL password (reads ~/.cap_db_pass if omitted)
#   --model MODEL   Ollama model name (default: qwen2.5:7b)
#   --no-seed       Skip database seeding
#   --unattended    Non-interactive (requires --db-pass or ~/.cap_db_pass)
#
# Tested: Ubuntu 24.04 LTS
# =============================================================================
set -euo pipefail

RED='\033[0;31m'; GREEN='\033[0;32m'; YELLOW='\033[1;33m'; NC='\033[0m'
info() { echo -e "${GREEN}[CAP]${NC} $*"; }
warn() { echo -e "${YELLOW}[WARN]${NC} $*"; }
die()  { echo -e "${RED}[FAIL]${NC} $*" >&2; exit 1; }

[[ $EUID -eq 0 ]] && die "Do NOT run with sudo. Run as your normal user: bash $0"

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
CAP_ROOT="${HOME}/CAP"
DB_PASS=""
OLLAMA_MODEL="qwen2.5:7b"
SEED=true
UNATTENDED=false

while [[ $# -gt 0 ]]; do
  case $1 in
    --dir)        CAP_ROOT="$2";     shift 2 ;;
    --db-pass)    DB_PASS="$2";      shift 2 ;;
    --model)      OLLAMA_MODEL="$2"; shift 2 ;;
    --no-seed)    SEED=false;        shift ;;
    --unattended) UNATTENDED=true;   shift ;;
    *) die "Unknown option: $1" ;;
  esac
done

if [[ -z "$DB_PASS" ]]; then
  if [[ -f "${HOME}/.cap_db_pass" ]]; then
    DB_PASS=$(cat "${HOME}/.cap_db_pass")
    info "Using database password from ~/.cap_db_pass"
  elif $UNATTENDED; then
    die "--unattended requires --db-pass or ~/.cap_db_pass"
  else
    read -rsp "Enter PostgreSQL cap_user password: " DB_PASS; echo
    [[ -n "$DB_PASS" ]] || die "Password cannot be empty"
  fi
fi

SRC_ZIP=$(ls "$SCRIPT_DIR"/cap-src-*.zip 2>/dev/null | head -1 || true)
FW_ZIP=$(ls  "$SCRIPT_DIR"/cap-frameworks-*.zip 2>/dev/null | head -1 || true)
MITRE_TS="${SCRIPT_DIR}/data/mitre.ts"
DISARM_TS="${SCRIPT_DIR}/data/disarm.ts"

[[ -f "$SRC_ZIP"   ]] || die "cap-src-*.zip not found in $SCRIPT_DIR"
[[ -f "$FW_ZIP"    ]] || die "cap-frameworks-*.zip not found in $SCRIPT_DIR"
[[ -f "$MITRE_TS"  ]] || die "data/mitre.ts not found"
[[ -f "$DISARM_TS" ]] || die "data/disarm.ts not found"

command -v node &>/dev/null || die "Node.js not found — run cap_prereqs.sh first"

LOG="/tmp/cap_install_$(date +%Y%m%d_%H%M%S).log"
exec > >(tee -a "$LOG") 2>&1

echo "============================================================"
echo " CAP Installer  —  $(date)"
echo " Install dir : $CAP_ROOT"
echo " User        : $(whoami)"
echo " Ollama model: $OLLAMA_MODEL"
echo "============================================================"

# Step 1: Extract source
info "Step 1/8: Extracting source..."
mkdir -p "$CAP_ROOT"
if [[ -d "$CAP_ROOT/core" ]]; then
  info "  Source already extracted — skipping unzip."
else
  info "  Extracting $(basename "$SRC_ZIP")..."
  unzip -q "$SRC_ZIP" -d "$CAP_ROOT"
fi

# Step 2: Apply errata patches
info "Step 2/8: Applying errata patches..."

# C2: run_all.sh hardcoded developer path
if grep -q "LuminaCore" "$CAP_ROOT/scripts/run_all.sh" 2>/dev/null; then
  sed -i 's|ROOT=".*LuminaCore.*"|ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." \&\& pwd)"|' \
    "$CAP_ROOT/scripts/run_all.sh"
  info "  C2: Patched run_all.sh."
fi

# H3: frontend .env hardcoded developer IP
if [[ -f "$CAP_ROOT/frontend/.env" ]]; then
  if grep -qE "VITE_GATEWAY_URL=http" "$CAP_ROOT/frontend/.env"; then
    sed -i 's|VITE_GATEWAY_URL=.*|VITE_GATEWAY_URL=/gateway|' "$CAP_ROOT/frontend/.env"
    sed -i 's|VITE_CORE_URL=.*|VITE_CORE_URL=/core|'          "$CAP_ROOT/frontend/.env"
    info "  H3: Patched frontend/.env to relative URLs."
  fi
fi

# C5/M1: missing Python packages
REQ="$CAP_ROOT/core/requirements.txt"
ADDED=()
grep -q "bcrypt"  "$REQ" || { echo "bcrypt>=4.0.0"   >> "$REQ"; ADDED+=(bcrypt); }
grep -q "ollama"  "$REQ" || { echo "ollama>=0.6.1"   >> "$REQ"; ADDED+=(ollama); }
grep -q "asyncpg" "$REQ" || { echo "asyncpg>=0.30.0" >> "$REQ"; ADDED+=(asyncpg); }
[[ ${#ADDED[@]} -gt 0 ]] && info "  C5/M1: Added to requirements: ${ADDED[*]}"

# C4: mitre.ts and disarm.ts missing from distribution
mkdir -p "$CAP_ROOT/frontend/data"
cp "$MITRE_TS"  "$CAP_ROOT/frontend/data/mitre.ts"
cp "$DISARM_TS" "$CAP_ROOT/frontend/data/disarm.ts"
info "  C4: Copied framework data files."

# C4b: NIDP framework seed JSON — ships with installer as exemplar framework
NIDP_JSON="${SCRIPT_DIR}/data/nidp_v1.0.json"
if [[ -f "$NIDP_JSON" ]]; then
  mkdir -p "$CAP_ROOT/scripts/data/frameworks"
  cp "$NIDP_JSON" "$CAP_ROOT/scripts/data/frameworks/nidp_v1.0.json"
  info "  C4b: Copied NIDP framework seed."
fi

# Step 3: Write .env
info "Step 3/8: Writing .env..."
ENV_FILE="$CAP_ROOT/.env"
if [[ -f "$ENV_FILE" ]]; then
  sed -i "s|DATABASE_URL=.*|DATABASE_URL=postgresql+psycopg://cap_user:${DB_PASS}@127.0.0.1:5432/cap|" "$ENV_FILE"
  sed -i "s|OLLAMA_MODEL=.*|OLLAMA_MODEL=${OLLAMA_MODEL}|" "$ENV_FILE"
  info "  .env updated."
else
  cat > "$ENV_FILE" <<ENV
DATABASE_URL=postgresql+psycopg://cap_user:${DB_PASS}@127.0.0.1:5432/cap
GITHUB_TOKEN=
AI_LLM_PROVIDER=ollama
OLLAMA_HOST=http://127.0.0.1:11434
OLLAMA_MODEL=${OLLAMA_MODEL}
JWT_SECRET=$(openssl rand -hex 32)
JWT_REFRESH_SECRET=$(openssl rand -hex 32)
ENV
  chmod 600 "$ENV_FILE"
  info "  .env written."
fi

# Step 4: Python venv
info "Step 4/8: Python venv and packages..."
if [[ ! -d "$CAP_ROOT/.venv" ]]; then
  python3.12 -m venv "$CAP_ROOT/.venv"
  info "  venv created."
else
  info "  venv already exists."
fi
"$CAP_ROOT/.venv/bin/pip" install --quiet --upgrade pip
"$CAP_ROOT/.venv/bin/pip" install --quiet \
  -r "$CAP_ROOT/core/requirements.txt" \
  -r "$CAP_ROOT/db/requirements.txt"
info "  Packages installed."

# Step 5: Migrations
info "Step 5/8: Database migrations..."
(
  cd "$CAP_ROOT"
  export DATABASE_URL="postgresql+psycopg://cap_user:${DB_PASS}@127.0.0.1:5432/cap"
  .venv/bin/alembic -c db/alembic.ini upgrade head
)
info "  Migrations complete."

# Step 6: Seeds
info "Step 6/8: Seeding database..."
# C6: three different DATABASE_URL prefixes required by three scripts
ADMIN_COUNT=$(PGPASSWORD="$DB_PASS" psql -U cap_user -h 127.0.0.1 -d cap \
  -tAc "SELECT COUNT(*) FROM users" 2>/dev/null || echo "0")

if [[ "$ADMIN_COUNT" -eq 0 ]]; then
  (cd "$CAP_ROOT"
   DATABASE_URL="postgresql://cap_user:${DB_PASS}@127.0.0.1:5432/cap" \
     .venv/bin/python scripts/seed_super_admin.py)
  info "  Admin user seeded."
else
  info "  Admin user already exists — skipping. (C7 upsert workaround)"
fi

if $SEED; then
  # C8: patch seed_frameworks.py to skip files missing the 'framework' key
  #     rather than crashing — upstream JSON files from zip lack this key
  SEED_PY="$CAP_ROOT/scripts/seed_frameworks.py"
  if grep -q "payload\['framework'\]" "$SEED_PY" 2>/dev/null && \
     ! grep -q "framework.*not in payload" "$SEED_PY" 2>/dev/null; then
    sed -i "s|payload = json.loads(file.read_text())\n.*await seed_file|payload = json.loads(file.read_text())\n            if 'framework' not in payload:\n                print(f'Skipping {file.name}: missing framework key (C8)')\n                continue\n            await seed_file|" "$SEED_PY" 2>/dev/null || true
    # sed multiline patch unreliable — use Python rewrite instead
    python3 - "$SEED_PY" <<'PYEOF'
import sys, re
path = sys.argv[1]
text = open(path).read()
old = "            payload = json.loads(file.read_text())\n            await seed_file(conn, payload)"
new = ("            payload = json.loads(file.read_text())\n"
       "            if 'framework' not in payload:\n"
       "                print(f'Skipping {file.name}: missing framework key (C8)')\n"
       "                continue\n"
       "            await seed_file(conn, payload)")
if old in text:
    open(path, 'w').write(text.replace(old, new))
    print("  C8: Patched seed_frameworks.py to skip malformed files.")
else:
    print("  C8: seed_frameworks.py patch not needed or already applied.")
PYEOF
  fi

  # C8 (cont): flatten upstream framework JSONs from subdirs to top level
  FW_DATA="$CAP_ROOT/scripts/data/frameworks"
  mkdir -p "$FW_DATA"
  unzip -qo "$FW_ZIP" -d "$CAP_ROOT/scripts/data/"
  FOUND=0
  while IFS= read -r -d '' jf; do
    bn=$(basename "$jf")
    [[ -f "$FW_DATA/$bn" ]] || cp "$jf" "$FW_DATA/$bn"
    (( FOUND++ )) || true
  done < <(find "$FW_DATA" -mindepth 2 -name "*.json" -print0)

  if [[ $FOUND -gt 0 ]]; then
    info "  Flattened $FOUND framework JSON file(s)."
    (cd "$CAP_ROOT"
     DATABASE_URL="postgres://cap_user:${DB_PASS}@127.0.0.1:5432/cap" \
       .venv/bin/python scripts/seed_frameworks.py) \
    && info "  Frameworks seeded." \
    || warn "  Framework seed failed — see Errata C8 in CAP_Install_Errata_FULL_20260227.md"
  else
    warn "  No framework JSON files found — see Errata C8."
  fi
fi

# Step 7: Build
info "Step 7/8: Building gateway and frontend..."
# H1: --include=dev required; ts-node-dev and vite are devDependencies
(cd "$CAP_ROOT/gateway"  && npm install --include=dev --silent)
(cd "$CAP_ROOT/frontend" && npm install --include=dev --silent && npm run build)
info "  Build complete."

# Step 8: Verify
info "Step 8/8: Verifying installation..."
PASS=0; FAIL=0
chk() {
  local d="$1"; local c="$2"
  if eval "$c" &>/dev/null; then info "  ✓ $d"; (( PASS++ )) || true
  else warn "  ✗ $d"; (( FAIL++ )) || true; fi
}
chk "PostgreSQL reachable"   "PGPASSWORD='$DB_PASS' psql -U cap_user -h 127.0.0.1 -d cap -c 'SELECT 1'"
chk "Migrations applied"     "PGPASSWORD='$DB_PASS' psql -U cap_user -h 127.0.0.1 -d cap -c 'SELECT COUNT(*) FROM users'"
chk "Frontend dist"          "[[ -f '$CAP_ROOT/frontend/dist/index.html' ]]"
chk "Gateway node_modules"   "[[ -d '$CAP_ROOT/gateway/node_modules/ts-node-dev' ]]"
chk "Python venv"            "[[ -x '$CAP_ROOT/.venv/bin/uvicorn' ]]"
chk "nginx config linked"    "[[ -L '/etc/nginx/sites-enabled/cap' ]]"

echo ""
echo "============================================================"
[[ $FAIL -eq 0 ]] \
  && echo -e " ${GREEN}CAP installation complete. All checks passed.${NC}" \
  || echo -e " ${YELLOW}Installation complete with ${FAIL} warning(s). Review: $LOG${NC}"
echo "============================================================"
echo ""
echo "  Start:    cd $CAP_ROOT && bash scripts/run_all.sh"
echo "  Browser:  http://$(hostname)/"
echo "  Login:    admin@cap.local / pass"
echo "  Log:      $LOG"
echo ""
echo "  Pre-load Ollama model: ollama pull $OLLAMA_MODEL"
echo ""

[[ -f "${HOME}/.cap_db_pass" ]] && rm -f "${HOME}/.cap_db_pass" && info "Cleaned up ~/.cap_db_pass"
