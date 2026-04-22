# Lab Visual Memory — N+22
**Created:** 2026-04-22 ~1430Q | **Corrected:** 2026-04-22 ~1530Q
**Session:** N+22
**Method:** Pixy PTZ sweep (Cambridge) + Athena Logitech snap
**Epistemic standard:**
  [OBSERVED:Claude] = Claude saw image directly (uploaded to context)
  [OBSERVED:Bob] = Bob confirmed from his screen
  [OPEN] = not yet verified
**Architecture note:** Claude cannot see images via DC read_file pipeline.
Visual verification currently requires human confirmation or direct upload.

---

## Camera Infrastructure

- **Athena camera:** Logitech C270 (or similar), fixed mount, /dev/video0,
  top of Athena monitor, approximately eye-level to seated Bob,
  aimed roughly across the room (not at wall behind Bob)
- **Cambridge camera:** EMEET Pixy, /dev/video0, PTZ via v4l2-ctl
  pan_absolute range: ±540000 | tilt_absolute range: ±324000
  Location: to Bob's LEFT (camera-right when facing Bob)
- **Capture:** snap.sh (ffmpeg 1280x720 MJPEG, 30 frames → final frame)
- **Transfer:** SCP Cambridge→Athena /tmp/, then DC read_file display

### PERSPECTIVE NOTE — CRITICAL FOR VISION MODEL DESIGN
Camera-left and subject-left are OPPOSITE. "pixy_left" (pan negative)
points camera-left = Bob's RIGHT. Stage-right convention applies.
Any vision model output referencing "left/right" must specify coordinate
frame: camera coordinates or subject/room coordinates. This is a non-trivial
mapping that must be explicit in the vision pipeline design.

---

## Bob Hillery — Physical Description
**Source:** athena_bob.jpg, 2026-04-22, uploaded directly to Claude context

[OBSERVED:Claude] Male, grey/white short hair (close-cropped).
[OBSERVED:Claude] Tan/rust/olive colored shirt.
[OBSERVED:Claude] 3/4 profile facing camera-right.
[OBSERVED:Claude] Bone-conduction Bluetooth earpiece on right ear.
[OBSERVED:Claude] Expression: attentive, forward gaze.

---

## Lab — Athena Camera View (looking across the room)
**Source:** athena_bob.jpg, Bob facing right (camera perspective)

[OBSERVED:Claude] White painted cinderblock wall visible behind Bob (left background).
[OBSERVED:Claude] Framed circular print on wall — Hunt's Kwa-gulth Moon.
  Colors: black, brown, orange, teal/green. Northwest Coast Native art.
  Circular composition, face/creature motif. Medium-large framed print.
[OBSERVED:Claude] Rattan/bamboo lattice room divider, center-right background.
  Geometric pattern: diamonds and ovals. Large piece, floor-to-ceiling height.
  Bright window light visible through the lattice — window is behind divider.
[OBSERVED:Claude] Ceiling: exposed wooden floor joists. Basement construction confirmed.
  Joists run parallel, white/grey painted. Pipe or wire visible along joists.
[OBSERVED:Claude] Lower left: black stereo stack components. Turntable visible (platter).
  Small antenna — Bluetooth transmitter for music streaming.
[OBSERVED:Claude] Lower center: dark patterned textile draped over furniture.
  Geometric pattern visible — possibly serape or Pendleton-style blanket.
[OBSERVED:Claude] Upper right: white hanging object, likely lamp shade.
[OBSERVED:Bob] Stereo stack cabinet with turntable. Speaker (black box).
[OBSERVED:Bob] Computer with small antenna → Bluetooth → stereo input for streaming.

---

## Lab — Pixy CENTER (pan=0, tilt=0)
**Source:** pixy_center.jpg — Bob confirmed from screenshot (Image 1 in prior message)
**NOTE:** I initially misidentified this as the "Athena snap." Corrected here.

[OBSERVED:Bob] Books and papers on a wooden chest (foreground area).
[OBSERVED:Bob] Plastic trash bag in a tall waste-basket.
[OBSERVED:Bob] Computer parts on a table in background.
[OBSERVED:Bob] Bookcase visible in background.
[OBSERVED:Bob] Bob visible — thoughtful expression, bone-conducting earpiece.
[OBSERVED:Bob] Shoji panel visible (Japanese sliding screen).
[OBSERVED:Bob] Civil War sword scabbard — glint visible.
[OBSERVED:Bob] Didgeridoo visible.

---

## Lab — Pixy LEFT (pan=-300000, tilt=0)
**Source:** pixy_left.jpg — Bob confirmed from screenshot (Image 2 in prior message)
**PERSPECTIVE:** pan negative = camera turns LEFT = points toward Bob's RIGHT side
  and the RIGHT wall of the room as Bob faces the camera.

[OBSERVED:Bob] Japanese samurai sword visible.
[OBSERVED:Bob] Basement window — upper half covered by horizontal Venetian blinds.
  Lower half open / partially visible.
[OBSERVED:Bob] Japanese silk-screen print: snow-covered country scene, framed.
[OBSERVED:Bob] Shoji panel visible.
[OBSERVED:Bob] Cambridge 32" monitor — top edge visible at center-bottom of frame.
[OBSERVED:Claude] (from screenshot) Window frame: wooden, multi-pane.
  Daylight + foliage visible through lower window section.
  Dark object lower-right of frame (now understood: Cambridge monitor top edge).

---

## Lab — Pixy RIGHT (pan=+300000, tilt=0)
**Source:** pixy_right.jpg — [OPEN] Bob has image, description pending.
**PERSPECTIVE:** pan positive = camera turns RIGHT = points toward Bob's LEFT.

---

## Lab — Pixy UP (pan=0, tilt=+60000)
**Source:** pixy_up.jpg — [OPEN] Small file size (32K) suggests ceiling/upper wall.

---

## Lab — Pixy DOWN (pan=0, tilt=-60000)
**Source:** pixy_down.jpg — [OPEN] 47K, likely floor or desk surface below Cambridge.

---

## Known Lab Contents (from passdown + Bob confirmation, not all camera-confirmed)

From session_current / passdown prior knowledge:
- Shoji screen (Japanese sliding panel) [OBSERVED:Bob in pixy_center and pixy_left]
- Didgeridoo with painted figures [OBSERVED:Bob in pixy_center]
- Civil War cavalry saber (US, not naval cutlass as Toddler misidentified) [OBSERVED:Bob pixy_center scabbard glint]
- Stereo stack with turntable [OBSERVED:Claude in athena_bob.jpg]
- Speaker cabinet [OBSERVED:Bob]
- Hunt's Kwa-gulth Moon print [OBSERVED:Claude in athena_bob.jpg]
- Kusanagi glyph on Athena (not yet camera-confirmed this session)
- Persian carpet [not yet camera-confirmed]
- Serape on desk chair [OBSERVED:Claude partial — textile in athena_bob.jpg]
- Brass naval shell converted to lamp [not yet camera-confirmed]
- Philippine bamboo panel [not yet camera-confirmed]
- Japanese silk-screen snow scene (framed) [OBSERVED:Bob in pixy_left]
- Japanese samurai sword [OBSERVED:Bob in pixy_left]
- Two workstations (Athena + Cambridge) — Cambridge monitor top edge [OBSERVED:Bob pixy_left]
- Basement construction: exposed floor joists, cinderblock walls [OBSERVED:Claude athena_bob.jpg]

---

*Written N+22 | 2026-04-22 ~1430Q*
*Corrected ~1530Q: Athena/pixy_center attribution error fixed; perspective note added*
*Pending: pixy_right, pixy_up, pixy_down descriptions from Bob*
