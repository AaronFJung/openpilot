# Aaron's TODO (future work, not implemented)

## 1. LKAS button steering without MAIN

Goal: the LKAS button engages comma steering even when MAIN (cruise main) is off.

Facts:
* MVL's carstate reads the LKAS button from `SCM_BUTTONS` on bus 0 as `CRUISE_SETTING == LKAS` and emits `ButtonType.lkas`.
* sunnypilot MADS (`openpilot/sunnypilot/mads/mads.py`) only reacts if `CS.cruiseState.available` or `self.allow_always`, and `allow_always` is only True for Tesla and some Hyundais.
* MADS also forces steering off when MAIN turns off, unless `self.no_main_cruise` is True, which only happens for brands in `MADS_NO_ACC_MAIN_BUTTON`.
* Verified against `mads.py` on Oct 14 2026 (lines ~45 to 52, 175, 189).

Changing this likely needs panda safety changes too, so it needs careful review. Safety related: do not hand to Copilot.

## 2. Button remapping in general

Desired: MAIN only arms cruise, LKAS only toggles comma steering.
Current workaround in sunnylink MADS settings: Toggle with Main Cruise off, Unified Engagement Mode off.

## 3. Hybrid battery SOC on screen

Possible later: show hybrid battery state of charge, after finding the CAN signal in cabana.

## 4. Camera plus one widget on the right

When `HideConfidenceBall` is on, the camera now widens into the 60px side panel (`SIDE_PANEL_WIDTH` in `openpilot/selfdrive/ui/mici/onroad/__init__.py`). Future idea: let that column instead host one widget to the right of the camera, for example the SOC gauge from item 3. Only one widget at a time, chosen by a param (Off / Confidence ball / Widget A / ...), so the layout stays simple.

## 5. Planned stop indicator (done, ShowStopIndicator)

Implemented in the set speed badge ("<distance> STOP"), driven by the model's planned speed (`modelV2.velocity`), not `shouldStop`, which only turns true below 0.3 m/s. Possible later: tune the trigger (STOP_SPEED in stop_indicator.py) after real drives.

## 6. Notes from Oct 14 2026 test drives

* Dynamic Experimental Control gives up on stop signs around 9 mph and hands off to ACC, which accelerates hard. Cause: it compares the model's planned path length to a speed based target (`SLOW_DOWN_DIST` in `openpilot/sunnypilot/selfdrive/controls/lib/dec/constants.py`). Running with Dynamic off. Report to sunnypilot.
* Best setup so far: CD210 model, experimental on, Dynamic off.
* Report to MVL: lurching between 0 and 2 mph at red lights, hard braking, ping pong following behind trucks on the highway.

## 7. Experimental mode alert should say On or Off

Long pressing the distance button shows "Experimental Mode Switched", which doesn't say which way it switched.

Facts (MVL's branch, Oct 15 2026):
* The alert is `EventNameSP.experimentalModeSwitched` in `openpilot/sunnypilot/selfdrive/selfdrived/events.py`: `NormalPermanentAlert("Experimental Mode Switched", duration=1.5)`.
* It fires from `update_experimental_mode()` in `openpilot/sunnypilot/selfdrive/car/cruise_helpers.py`, right after it writes the new `ExperimentalMode` value, so the new state is known at that point.
* openpilot's personality alert already does this kind of thing: `personality_changed_alert` builds "Driving Personality: <name>" with a callback instead of fixed text.

Options: split it into two events (experimentalModeOn and experimentalModeOff, which needs a cereal enum change), or make the alert a callback that reads the new mode. Check sunnypilot master first in case it was already fixed upstream. UI and alert text only, nothing safety related.
