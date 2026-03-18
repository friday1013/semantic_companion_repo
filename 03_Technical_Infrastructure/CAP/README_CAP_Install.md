# CAP — Civic Attestation Platform
## Installation and Getting Started Guide

**Version:** cap-src-20260219
**Tested:** Ubuntu 24.04 LTS (Desktop and Server)
**Last updated:** 2026-03-18

---

## Phase 1 — Before You Install

### Why CAP Exists — The Problem Space

The diagram included in this package (`WardleOIP-66109306.jpg`)
shows the three-part taxonomy of information disorder developed by Claire Wardle
and Hossein Derakhshan (First Draft / Council of Europe, 2017):

- **Misinformation** — false information, regardless of intent
- **Disinformation** — deliberately created to harm or manipulate
- **Malinformation** — true information, weaponized out of context

CAP and the NIDP framework are designed to defend against all three — not through
fact-checking content, but through provenance attestation: *who vouched for this,
when, and in what context.* See `InformationDisorder_Attribution.md` for the full
citation and the connection to NIDP's design.

### What You Will Need

- A computer running **Ubuntu 24.04 LTS** with internet access
- The **CAP installer package** (a `.zip` or `.tar.gz` file from QuietWire)
- A **password** you will choose for the database (write it down — you will need it twice)
- About **15–20 minutes** (more if downloading a large AI model)

### Choose Your Install Account

**This is the most important decision before you start.**

CAP installs entirely under the user account that runs the installer. All files,
services, and data will be owned by that account. You have two options:

**Option A — Your personal account** (simplest for single-person use)

Just use your normal login. CAP will install to `~/CAP` in your home directory.
Good for: personal use, development, testing.

**Option B — A dedicated service account** (recommended for shared or permanent nodes)

Create a separate account (e.g., `quietwire`) before installing. CAP will be
owned by that account and survives if your personal login changes.

```bash
# Create the service account (do this ONCE before running the installer)
sudo useradd -m -s /bin/bash quietwire
sudo passwd quietwire
sudo usermod -aG sudo quietwire

# Then switch to that account for all installation steps:
su - quietwire
```

> For a QuietWire shared node, Option B is strongly recommended.
> Use `quietwire` as the account name — it is the QW standard.

### Hardware Minimum

| Component | Minimum |
|-----------|---------|
| RAM | 8 GB |
| Disk | 20 GB free |
| OS | Ubuntu 24.04 LTS |
| Network | Internet access during install |

AI model performance improves significantly with a GPU, but CAP installs and
runs on CPU-only hardware. The default model (`qwen2.5:7b`) works on CPU.

---

## Phase 2 — Installing CAP

### Step 1: Get the installer files into place

Copy the installer files to the home directory of your install account.
The installer expects these files in the **same directory** you run it from:

```
cap_prereqs.sh
cap_install.sh
cap-src-*.zip
cap-frameworks-*.zip
data/
  mitre.ts
  disarm.ts
```

If you received a `.tar.gz` package:
```bash
tar -xzf cap-usb-installer-*.tar.gz
cd cap-usb-installer
```

### Step 2: Run prerequisites (requires sudo — run once)

```bash
sudo bash cap_prereqs.sh --db-pass 'YourChosenPassword'
```

Replace `YourChosenPassword` with the database password you chose in Phase 1.
Use single quotes around it if it contains any special characters.

**What this does:** Installs Node.js, PostgreSQL, nginx, and Python tools;
creates the database; sets up file permissions. Takes 3–5 minutes.

**What success looks like:**
```
[CAP-PRE] Prerequisites complete.
  Now run (as <user>, no sudo):
    bash cap_install.sh
```

### Step 3: Run the application installer (no sudo)

```bash
bash cap_install.sh
```

**What this does:** Extracts CAP, sets up the Python environment, runs
database migrations, seeds initial data, and builds the web interface.
Takes 5–10 minutes.

**What success looks like:**
```
CAP installation complete. All checks passed.

  Start:    cd ~/CAP && bash scripts/run_all.sh
  Browser:  http://<hostname>/
  Login:    admin@cap.local / pass
```

> **NIDP pre-loaded:** The Narrative Integrity Distribution Protocol (v1.0)
> framework seeds automatically during install. When you first log in, you will
> find NIDP already populated under Frameworks — 5 integrity phases, 5 governance
> layers, and 3 precision modes. This gives new nodes a working example of
> QuietWire's core narrative integrity approach and a starting point for
> customizing your node's operating framework.

If you see warnings instead of "All checks passed," see the Troubleshooting
section at the bottom of this file.

### Step 4: Start CAP

```bash
cd ~/CAP && bash scripts/run_all.sh
```

Wait about 15 seconds, then open a browser to:

```
http://localhost/
```

Or from another machine on the same network:
```
http://<hostname>/
```

Log in with: `admin@cap.local` / `pass`

**Change your password immediately** — go to the account menu in the top right.

### Step 5: Pre-load the AI model (optional but recommended)

The AI Advisor pulls its model on first use, which can take several minutes.
Pre-load it now so it is ready when you need it:

```bash
ollama pull qwen2.5:7b
```

For Shaoshi (24GB VRAM), use the larger model:
```bash
ollama pull mistral-nemo:12b-instruct-2407-q5_K_M
```

---

## Phase 3 — Using Your Node

### Stopping and Starting CAP

```bash
# Start
cd ~/CAP && bash scripts/run_all.sh

# Stop
pkill -f "uvicorn app.main"
pkill -f "ts-node-dev"

# Check if running
ps aux | grep -E "uvicorn|ts-node-dev" | grep -v grep

# Health check
curl http://localhost/core/health
# Expected: {"status":"ok"}
```

### Default Credentials

| What | URL | Username | Password |
|------|-----|----------|----------|
| CAP Web UI | http://localhost/ | admin@cap.local | pass |
| PostgreSQL | localhost:5432 | cap_user | (set at install) |

Change the admin password on first login.

### Customizing Your Node

A CAP node is not just a chatbot — it is a named AI instance with context,
memory, and rules defined by its operator. The customization workflow has
three surfaces working together:

1. **Browser** — shows the live node as it actually is
2. **Civic AI** — the AI conversation attached to your account (planning layer)
3. **Terminal** — implements the changes

The basic loop:
- Open the node in a browser and observe what needs to change
- Describe the change to the Civic AI; ask for implementation instructions
- Apply those instructions via the terminal
- Refresh the browser and verify the result
- Repeat

See `NodeCustomizationInstructions.md` in this directory for the full
step-by-step workflow.

### Framework Data

CAP includes MITRE ATT&CK and DISARM framework data. Check seeding status:

```bash
PGPASSWORD=<your_pass> psql -U cap_user -h 127.0.0.1 -d cap \
  -c "SELECT code, title FROM frameworks;"
```

---

## Re-installation / Clean Slate

The installer is safe to re-run on an existing installation (updates configs,
rebuilds frontend, skips already-seeded data). For a completely clean reinstall:

```bash
# Drop and recreate database
sudo -u postgres psql -c "DROP DATABASE IF EXISTS cap;"
sudo bash cap_prereqs.sh --db-pass 'YourPassword'
bash cap_install.sh
```

---

## Troubleshooting

**"Permission denied" errors during install**
You may have run `sudo su` and then the installer. Don't. Run:
`sudo bash cap_prereqs.sh` from your normal (or service) account.

**nginx returns 403 Forbidden**
```bash
sudo chmod o+x $HOME ~/CAP ~/CAP/frontend ~/CAP/frontend/dist
```

**Frontend loads but API calls fail**
```bash
cat ~/CAP/frontend/.env | grep VITE
# Should show /gateway and /core, not hardcoded IPs
# Fix: re-run bash cap_install.sh
```

**Health check fails immediately after startup**
Normal on slower systems — services need ~15 seconds to start:
```bash
sleep 15 && curl http://localhost/core/health
```

**Migrations fail with permission error**
```bash
sudo -u postgres psql -d cap -c "GRANT ALL ON SCHEMA public TO cap_user;"
```

**Re-install shows "UniqueViolation" on admin seed**
```bash
bash cap_install.sh --no-seed
```

---

## Options Reference

### cap_prereqs.sh
```
--db-pass PASS     PostgreSQL password (prompted if omitted)
--install-dir DIR  Install to DIR instead of ~/CAP
--unattended       Non-interactive (requires --db-pass)
```

### cap_install.sh
```
--dir DIR          Install to DIR instead of ~/CAP
--db-pass PASS     Override password (reads ~/.cap_db_pass by default)
--model MODEL      Ollama model (default: qwen2.5:7b)
--no-seed          Skip database seeding (use on re-install if admin exists)
--unattended       Non-interactive
```

---

## File Layout

```
cap-usb-installer/
├── cap_prereqs.sh                      ← Phase 2, Step 2 — run with sudo
├── cap_install.sh                      ← Phase 2, Step 3 — no sudo
├── README_CAP_Install.md               ← This file
├── NodeCustomizationInstructions.md    ← Phase 3 detail
├── CAP_Install_Errata_FULL_20260227.md ← Full issue reference (technical)
├── cap-src-*.zip                       ← CAP application source
├── cap-frameworks-*.zip                ← Framework reference data
└── data/
    ├── mitre.ts
    └── disarm.ts
```

---

*QuietWire Civic AI — CAP Installation and Getting Started Guide*
*Maintained by Bob Hillery + Claude N+17 | 2026-03-18*
