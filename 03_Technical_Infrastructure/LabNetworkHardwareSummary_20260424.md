# QuietWire / Semantic Companion Lab — Hardware Summary
**Updated:** 2026-04-24 (N+22)
**Change notes:** Mars build complete. 64GB RAM Shaoshi→Mars.
Shaoshi now 128GB (was 192GB). Mars 128GB confirmed live.
Ubuntu 26.04 LTS (Resolute Raccoon) on Mars — first lab machine on 26.04.

## Athena — 172.17.50.232
- Role: Primary ops hub, Claude Desktop + DC MCP, Logitech camera
- GPU: RTX A2000 12GB | RAM: 64GB | OS: Ubuntu 24.04 LTS
- Storage: /mnt/fastdata (sessions, ChromaDB), /mnt/seagate (corpus)
- Status: PRIMARY

## Shaoshi — 172.17.50.246
- Role: CAP host, local model server (Ollama)
- CPU: Xeon E5-2670 v3 dual socket (12c/24t, max 3.1GHz)
- GPU: Titan RTX 24GB | Driver: 590.48.01
- RAM: 128GB (was 192GB — 64GB to Mars 2026-04-24)
- Storage: sda 1.8TB (OS), sdb 12.7TB (data)
- OS: Ubuntu 24.04.4 LTS | Kernel: 6.17.0-22-generic
- Status: ACTIVE — CAP running

## Mars — 172.17.50.222
- Role: Agentic host — Huginn & Muninn
- CPU: Xeon E5-2690 v4 dual socket (14c/28t, max 3.5GHz)
- GPU: Quadro K620 2GB (display only — neopallium, not prefrontal)
- RAM: 128GB (received 64GB from Shaoshi 2026-04-24)
- Storage: sda 465.8GB SSD (OS, correct drive), sdb 698.6GB HDD (data)
           sdc 931.5GB (installer USB — remove after setup)
- OS: Ubuntu 26.04 LTS "Resolute Raccoon" | Kernel: 7.0.0-14-generic
- Status: FRESH INSTALL — SSH confirmed, setup in progress

## Cambridge — 172.17.50.242
- Role: Vision processing, heavy compute
- CPU: Dual Xeon (T7910)
- GPU: RTX 4500 Ada 24GB | RAM: 256GB
- Cameras: EMEET Pixy PTZ (/dev/video0), snap.sh in ~/bin/
- Storage: /media/hillery/crew 4TB, /media/hillery/DeepThought 24TB
- OS: Ubuntu 24.04 LTS
- Status: OFFLINE — planned vision model host (Moondream2/Florence-2)

## Remount
- Role: Coordination, remote sessions
- Hardware: MacBook | OS: macOS | Status: ACTIVE

## Squirrel
- Role: Secondary
- Hardware: Repurposed MacBook | OS: Ubuntu 24.04 | Status: Available

## Architecture Notes
Compute philosophy: architecture over scale, right hardware for right role.
Brain analog mapping:
- Mars K620: neopallium (display routing only)
- Mars CPU/RAM: Huginn/Muninn agent substrate
- Shaoshi Titan: heavy inference / cortex analog
- Cambridge RTX 4500 Ada: visual cortex (planned)
- ChromaDB on Athena: long-term semantic memory
- session_current + passdowns: hippocampal index prosthetic

## Mars Setup Checklist
[ ] Confirm openssh-server installed (SSH working — likely yes)
[ ] ssh-keygen + key exchange with Athena
[ ] Remove installer USB (sdc)
[ ] Mount sdb for data
[ ] Install Ollama
[ ] First agent model (Huginn candidate — small, fast, instruction-following)
[ ] Desktop Commander MCP
[ ] Add Mars to /etc/hosts on all lab machines

---
Generated N+22 | 2026-04-24 via live SSH catalog from Athena
