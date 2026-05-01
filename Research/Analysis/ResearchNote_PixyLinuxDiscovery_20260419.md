# Research Note: EMEET Pixy — Full Linux Control Discovered
**Date:** 2026-04-19 | **Session:** N+22 | **Author:** Bob Hillery / Claude N+22
**Status:** [OBSERVED] — confirmed by direct hardware test

---

## Summary

The EMEET Pixy dual-camera tracking device is fully controllable on Linux via
standard kernel interfaces. No proprietary driver required. Tracking, gesture
toggle, pan/tilt/zoom, and real-time state monitoring all work through UVC and
HID interfaces available in any modern Linux kernel.

---

## Hardware

- Device: EMEET PIXY (USB ID 328f:00c0)
- Host: Cambridge (Ubuntu 24.04.4, kernel 6.17)
- /dev/video0 — camera (UVC)
- /dev/video1 — not a capture device
- /dev/hidraw2 — tracking state HID interface

---

## Discoveries

### 1. Tracking requires an active UVC stream
Onboard processor is dormant until any UVC consumer opens /dev/video0.
ffmpeg, Google Meet, Zoom, VLC — all activate tracking identically.
[OBSERVED]: LED blinked blue on first ffmpeg stream open before any gesture.

### 2. HID interface — real-time tracking state
32-byte reports from /dev/hidraw2. Header: `09 01 01 01 00 01 00 01`

| Byte 8 | LED   | State                     |
|--------|-------|---------------------------|
| 0x00   | Green | Searching                 |
| 0x01   | Blue  | Tracking — centered       |
| 0x03   | Amber | Tracking — off-center     |

### 3. Gesture toggle is a flip-flop
Palm (5s) toggles tracking on/off regardless of current state.
Full state machine confirmed in pixy_monitor.py session log.

### 4. Full PTZ control via standard v4l2

```
pan_absolute:   min=-540000  max=540000  step=3600  (~±150° pan)
tilt_absolute:  min=-324000  max=324000  step=3600  (~±90° tilt)
zoom_absolute:  min=100      max=150
focus_absolute: min=0        max=1023
```

Room sweep test: camera physically moved to commanded positions.
Subject located in center frame. HID confirmed BLUE at correct position.

### 5. Google Meet — works without configuration
Tracking activated within 1 second of stream open. Servo acquisition <1s.

---

## Software Written (Cambridge ~/bin/)

- pixy_monitor.py — HID state reader
- pixy_watch.sh — stream + HID monitor + rotating log (~/.local/share/pixy/pixy.log)
- snap.sh — single frame capture
- /etc/udev/rules.d/99-emeet-pixy.rules — plugdev access to hidraw2
- ~/.local/share/applications/pixy-watch.desktop — app launcher icon

---

## Architectural Implications

**Two operating modes:**
1. Tracking: camera autonomously finds/follows subjects
2. Directed: software commands specific pan/tilt positions

**Event-driven pipeline:**
HID SEARCHING→CENTERED = subject entered frame → trigger snap → analyze scene

**Salience detection [OBSERVED]:**
Onboard processor performs editorial compression — reports whether something
worth tracking is centered, not raw pixels. Compaction-first architecture in
physical hardware. Anticipated N+21 on camera arrival; confirmed operationally N+22.

**Connection to world-coupled evidence loop:**
First physically-directed sensory input in lab. Camera provides event-driven
environmental signals, not just on-demand snapshots.

---

## Pending

- [ ] Tilt calibration: needs ~-36000 offset when mounted above desk
- [ ] pixy_watch.sh: tilt correction on CENTERED event
- [ ] Motion detection (motion/motioneye) for idle-until-triggered
- [ ] EMEET email: draft ready in bob@quietwire.ai
- [ ] GitHub: emeet-pixy-linux repo (pending git install on Cambridge)
- [ ] Sync to Athena seagate corpus + index

---
*N+22 | 2026-04-19 | Cambridge | Claude Sonnet 4.6*
