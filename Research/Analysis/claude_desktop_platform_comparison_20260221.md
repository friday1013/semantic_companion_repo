# Claude Desktop Platform & Version Comparison
## Cowork VM Architecture Analysis
**Compiled:** 20260221T1100Q — Bob Hillery + Claude N+10
**Systems:** Remount (macOS, native Anthropic app) vs Athena (Ubuntu 24.04, aaddrick community build)

---

## Version State at Time of Analysis

| | Remount (Mac) | Athena (Linux) |
|---|---|---|
| **App version** | 1.1.3918 (Anthropic direct) | 1.1.3647-1.3.12 (aaddrick build) |
| **Update channel** | Squirrel auto-update, in-app | apt via aaddrick PPA |
| **Update lag** | Immediate from Anthropic | Community build lag (3647 vs 3918) |
| **Two updates needed** | Yes — 3541 to 3647 to 3918 in one session | apt update reached 3647 only |

---

## Cowork VM Architecture Comparison

| | Mac 1.1.3918 | Linux 1.1.3647 |
|---|---|---|
| **VM status** | Real, operational, running | Phase 1 stub only |
| **VM implementation** | Apple Virtualization Framework | QEMU/KVM (Phase 3, placeholder) |
| **rootfs.img** | 10GB, touched this session | Does not exist |
| **rootfs.img.zst** | Gone post-update (applied and cleaned) | Does not exist |
| **sessiondata.img** | 31MB, live session state | Does not exist |
| **VM IP address** | 192.168.64.11 (persistent, RFC 1918) | No VM |
| **VM MAC address** | da:e4:f3:88:a9:f7 (fixed since Jan 19) | No VM |
| **Machine UUID** | Persistent binary plist, fixed since Jan 19 | No VM |
| **vm_bundles dir** | Present (claudevm.bundle + warm/) | Not present |
| **Sandbox** | macOS Seatbelt + --enable-sandbox | Explicitly none — full home dir access |
| **Socket** | Internal Apple VZ framework | Unix domain socket at XDG_RUNTIME_DIR |
| **coworkScheduledTasksEnabled** | false (in config) | Not in config |

---

## VM Identity Persistence (Mac)

The VM on Remount has had the same hardware identity since January 19, 2026:
- Fixed MAC address: da:e4:f3:88:a9:f7
- Fixed machine UUID (binary plist, unchanged through all app updates)
- Fixed IP: 192.168.64.11 (Apple private virtualization subnet 192.168.64.0/24)

After update chain 1.1.3541 to 3647 to 3918:
- VM identity: UNCHANGED (same MAC, same UUID, same IP)
- rootfs.img: UPDATED (new OS image applied, .zst source bundle cleaned post-apply)
- sessiondata.img: LIVE (31MB, session state carried forward across updates)

The .origin tracking files present in 3541 (.rootfs.img.origin, .rootfs.img.zst.origin)
are absent in 3918. The update mechanism changed — origin tracking removed or internalized.

---

## The RFC 1918 Network Question

192.168.64.0/24 is Apple Virtualization Framework's default private subnet,
assigned to VMs created via the macOS native virtualization API.
This is distinct from user-managed VMs (Parallels uses 10.211.x.x, VMware uses 192.168.x.x).

The VM is provisioned with:
- Its own persistent MAC address (hardware identity)
- Its own IP on a host-only network segment
- Anthropic's rootfs image as its operating system
- A sessiondata.img that persists state across launches and app updates

This network interface exists on the host machine from the moment Claude Desktop
is installed and Cowork first activated. It is not created on-demand per session.

**Open questions requiring further investigation:**
1. What processes run inside the VM? (requires VM console or rootfs inspection)
2. Can the VM initiate outbound connections beyond the host-only segment?
3. What does sessiondata.img contain — user data, credentials, conversation state?
4. Does the VM have access to host filesystem via virtio or similar shared mount?
5. What does warm/ directory contain? (currently: one SHA1 hash file)
6. Is an equivalent VM provisioned on Windows, and on what subnet?
7. Is VM provisioning disclosed in Anthropic's privacy policy or Terms of Service?
8. What happens to VM identity and sessiondata.img on app uninstall?

---

## Security Posture Summary

**Mac:** Strong sandbox. VM isolates Cowork agent from host. macOS Seatbelt
(BSD mandatory access control) enforced at kernel level for renderer processes.
Cowork agent runs inside a contained VM environment. The VM is the security boundary.

**Linux:** No sandbox currently. The cowork-vm-service.js README warning states
explicitly: "no sandbox — Claude has access to your entire home directory."
Phase 3 (QEMU/KVM VM) will close this gap when shipped. Timeline unknown.

**The asymmetry:** Same application, same Cowork feature, fundamentally different
security posture by platform. Linux Cowork users run with full home directory
exposure. Mac Cowork users run inside a VM. This difference is not prominently
disclosed to users.

**Version lag adds risk:** Linux community build lags Anthropic releases (3647 vs 3918
at time of writing). Security-relevant updates ship to Mac first.

---

## Relevance to AI Agent Threat Vectors

See: ai_agent_threat_vectors_20260220.md — Vector 2: Skill/Plugin Injection

The VM architecture is the correct technical defense against a malicious skill
attempting system command execution. On Mac, the skill runs inside the VM —
SSH keys, API keys, .env files, browser credentials on the host are unreachable.

On Linux (until Phase 3), a malicious skill with embedded curl-pipe-bash instructions
executes with the agent's full home directory access. This is the same exposure
profile that made the ClawHub/OpenClaw attack so damaging.

---

*Analysis: Claude N+10 via Desktop Commander MCP, Remount + Athena SSH*
*Status: Preliminary. Open questions require VM console access for full audit.*
*Next document: cowork_vm_network_architecture.md*
