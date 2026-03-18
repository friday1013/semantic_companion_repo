#!/usr/bin/env bash
# =============================================================================
# CAP Prerequisites Installer — sudo portion only
# Run this ONCE as: sudo bash cap_prereqs.sh [options]
#
# What this does (everything requiring root):
#   - Installs Node.js 20, PostgreSQL 16 + pgvector, nginx, python3.12-venv
#   - Creates PostgreSQL database, user, enables vector extension
#   - Writes nginx config stub and sets home-directory execute permissions
#
# After this completes, run cap_install.sh as your normal user (no sudo).
#
# Options:
#   --db-pass PASS    PostgreSQL cap_user password (prompted if omitted)
#   --install-dir DIR Install directory (default: /home/<user>/CAP)
#   --unattended      Non-interactive mode (requires --db-pass)
#
# Tested: Ubuntu 24.04 LTS
# =============================================================================
set -euo pipefail

RED='\033[0;31m'; GREEN='\033[0;32m'; YELLOW='\033[1;33m'; NC='\033[0m'
info() { echo -e "${GREEN}[CAP-PRE]${NC} $*"; }
warn() { echo -e "${YELLOW}[WARN]${NC} $*"; }
die()  { echo -e "${RED}[FAIL]${NC} $*" >&2; exit 1; }

[[ $EUID -eq 0 ]] || die "Run with sudo: sudo bash $0"

REAL_USER="${SUDO_USER:-$USER}"
[[ "$REAL_USER" == "root" ]] && die \
  "Do not run as root directly. Use: sudo bash $0 (from your normal user account)"

REAL_HOME=$(getent passwd "$REAL_USER" | cut -d: -f6)
CAP_ROOT="${REAL_HOME}/CAP"
DB_PASS=""
UNATTENDED=false

while [[ $# -gt 0 ]]; do
  case $1 in
    --db-pass)    DB_PASS="$2";    shift 2 ;;
    --install-dir) CAP_ROOT="$2"; shift 2 ;;
    --unattended) UNATTENDED=true; shift ;;
    *) die "Unknown option: $1" ;;
  esac
done

if [[ -z "$DB_PASS" ]]; then
  $UNATTENDED && die "--unattended requires --db-pass"
  read -rsp "Enter password for PostgreSQL cap_user: " DB_PASS; echo
  [[ -n "$DB_PASS" ]] || die "Password cannot be empty"
fi

LOG="/tmp/cap_prereqs_$(date +%Y%m%d_%H%M%S).log"
exec > >(tee -a "$LOG") 2>&1

echo "============================================================"
echo " CAP Prerequisites  —  $(date)"
echo " Installing for user : $REAL_USER"
echo " CAP directory       : $CAP_ROOT"
echo "============================================================"

# ---------------------------------------------------------------------------
# 0. Bootstrap — curl required before NodeSource fetch (GAP-21)
# ---------------------------------------------------------------------------
info "Checking bootstrap dependencies..."
if ! command -v curl &>/dev/null; then
  info "  Installing curl..."
  apt install -y curl
  info "  curl installed."
else
  info "  curl already present."
fi

# ---------------------------------------------------------------------------
# 1. Node.js 20
# ---------------------------------------------------------------------------
info "Checking Node.js..."
if ! command -v node &>/dev/null || \
   [[ $(node --version | cut -d. -f1 | tr -d v) -lt 20 ]]; then
  info "  Installing Node.js 20 via NodeSource..."
  curl -fsSL https://deb.nodesource.com/setup_20.x | bash -
  apt install -y nodejs
  info "  Node.js $(node --version) installed."
else
  info "  Node.js $(node --version) already present."
fi

# ---------------------------------------------------------------------------
# 2. System packages
# ---------------------------------------------------------------------------
info "Checking system packages..."
PKGS=()
dpkg -s postgresql-16          &>/dev/null || PKGS+=(postgresql-16)
dpkg -s postgresql-16-pgvector &>/dev/null || PKGS+=(postgresql-16-pgvector)
dpkg -s nginx                  &>/dev/null || PKGS+=(nginx)
dpkg -s python3.12-venv        &>/dev/null || PKGS+=(python3.12-venv)
# GAP-19: python3.12-venv is a separate package on Ubuntu 24.04

if [[ ${#PKGS[@]} -gt 0 ]]; then
  info "  Installing: ${PKGS[*]}"
  apt install -y "${PKGS[@]}"
else
  info "  All system packages present."
fi

# ---------------------------------------------------------------------------
# 3. PostgreSQL database + user
# ---------------------------------------------------------------------------
info "Configuring PostgreSQL..."
systemctl is-active --quiet postgresql || systemctl start postgresql

DB_EXISTS=$(sudo -u postgres psql -tAc \
  "SELECT 1 FROM pg_database WHERE datname='cap'" 2>/dev/null || true)

if [[ "$DB_EXISTS" != "1" ]]; then
  info "  Creating database, user, and vector extension..."
  sudo -u postgres psql <<SQL
CREATE DATABASE cap;
CREATE USER cap_user WITH PASSWORD '${DB_PASS}';
GRANT ALL PRIVILEGES ON DATABASE cap TO cap_user;
\c cap
CREATE EXTENSION IF NOT EXISTS vector;
GRANT ALL ON SCHEMA public TO cap_user;
SQL
else
  info "  Database 'cap' already exists — updating password."
  sudo -u postgres psql -c \
    "ALTER USER cap_user WITH PASSWORD '${DB_PASS}';" &>/dev/null || true
  sudo -u postgres psql -d cap -c \
    "GRANT ALL ON SCHEMA public TO cap_user;" &>/dev/null || true
fi

# ---------------------------------------------------------------------------
# 4. nginx stub and directory permissions
# ---------------------------------------------------------------------------
info "Configuring nginx permissions..."

# GAP (H4): nginx worker runs as www-data and cannot read /home/<user>
chmod o+x "$REAL_HOME"

mkdir -p "${CAP_ROOT}/frontend/dist"
chown -R "$REAL_USER:$REAL_USER" "$CAP_ROOT"
chmod o+x "$CAP_ROOT" "${CAP_ROOT}/frontend" "${CAP_ROOT}/frontend/dist"

mkdir -p "${CAP_ROOT}/scripts"
cat > "${CAP_ROOT}/scripts/cap-nginx.conf" <<NGINX
server {
    listen 80;
    server_name $(hostname) localhost;

    location = /index.html {
        root ${CAP_ROOT}/frontend/dist;
        add_header Cache-Control "no-cache, no-store, must-revalidate";
    }
    location / {
        root ${CAP_ROOT}/frontend/dist;
        try_files \$uri \$uri/ /index.html;
    }
    location /core/ {
        proxy_pass http://127.0.0.1:8100/;
        proxy_set_header Host \$host;
        proxy_set_header X-Real-IP \$remote_addr;
    }
    location /gateway/ {
        proxy_pass http://127.0.0.1:4000/;
        proxy_set_header Host \$host;
        proxy_set_header X-Real-IP \$remote_addr;
    }
}
NGINX

ln -sf "${CAP_ROOT}/scripts/cap-nginx.conf" /etc/nginx/sites-enabled/cap
rm -f /etc/nginx/sites-enabled/default
nginx -t && systemctl reload nginx
chown "$REAL_USER:$REAL_USER" "${CAP_ROOT}/scripts/cap-nginx.conf"

# ---------------------------------------------------------------------------
# 5. Write DB password for cap_install.sh
# ---------------------------------------------------------------------------
PASS_FILE="${REAL_HOME}/.cap_db_pass"
echo "$DB_PASS" > "$PASS_FILE"
chmod 600 "$PASS_FILE"
chown "$REAL_USER:$REAL_USER" "$PASS_FILE"

# ---------------------------------------------------------------------------
# 6. Final ownership fix — all CAP_ROOT files must be owned by install user
#    Scripts directory is created after the earlier chown so needs this pass (GAP-22)
# ---------------------------------------------------------------------------
chown -R "$REAL_USER:$REAL_USER" "$CAP_ROOT"
chmod -R 775 "$CAP_ROOT"

echo ""
echo "============================================================"
echo -e " ${GREEN}Prerequisites complete.${NC}"
echo "============================================================"
echo ""
echo "  Now run (as $REAL_USER, no sudo):"
echo "    bash cap_install.sh"
echo ""
echo "  Or with model selection:"
echo "    bash cap_install.sh --model mistral-nemo:12b-instruct-2407-q5_K_M"
echo ""
echo "  Log: $LOG"
echo ""
