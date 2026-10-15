# Instructions for Copilot in this fork

This is Aaron's personal fork of MVL's sunnypilot Honda branch (openpilot based), running on a comma four in a 2027 Honda CR-V Hybrid (Bosch CAN FD, HONDA_CRV_6G). Code you write here ends up driving a real car.

## Hard rules

1. Never modify safety related code. That includes `panda/` (especially safety modes), anything under `opendbc_repo/opendbc/safety/`, driver monitoring (`openpilot/selfdrive/monitoring/`, `openpilot/selfdrive/modeld/dmonitoringmodeld*`), steering and braking limits, `openpilot/selfdrive/controls/`, `openpilot/sunnypilot/mads/`, and car controllers or car interfaces in `opendbc_repo`. If a task seems to require touching these, stop and explain why in the PR instead.
2. Never bump or repoint submodules unless the issue explicitly asks for it.
3. Keep diffs minimal. No refactors, no reformatting of unrelated code. The fork must keep merging cleanly with MVL's branch.
4. MVL's code wins in conflicts, except for this fork's own features (see Fork files below and `aaron_FEATURES.md`), which must keep working.

## Repo layout

* The real code lives under `openpilot/` (for example `openpilot/selfdrive/ui/...`).
* The comma four UI is the "mici" UI: `openpilot/selfdrive/ui/mici/`. The comma 3X UI is the older one under `openpilot/selfdrive/ui/` and `openpilot/selfdrive/ui/sunnypilot/layouts/`.
* Params are declared in `openpilot/common/params_keys.h`.
* sunnylink settings pages are YAML in `openpilot/sunnypilot/sunnylink/settings_ui_src/pages/`. Never hand edit `openpilot/sunnypilot/sunnylink/settings_ui.json`; regenerate it with `python openpilot/sunnypilot/sunnylink/tools/compile_settings_ui.py` and check with `--check`. Read `openpilot/sunnypilot/sunnylink/docs/README.md` first.

## Checks to run before finishing

```bash
source .venv/bin/activate
python openpilot/sunnypilot/sunnylink/tools/compile_settings_ui.py --check
scripts/lint/lint.sh
python tools/test_runner.py openpilot/sunnypilot/sunnylink/tests openpilot/common/tests/test_params.py
```

## Pull requests

Explain what changed and why, list the checks you ran, and add an on device test checklist for Aaron.

## Fork files

Files this fork changes or adds on top of MVL's branch. Keep this list current.

* `openpilot/common/params_keys.h` (HideConfidenceBall, HideSteeringWheelIcon, ShowStopIndicator, SetSpeedStart, TorqueBarHeight)
* `openpilot/selfdrive/ui/sunnypilot/ui_state.py`
* `openpilot/selfdrive/ui/mici/layouts/settings/toggles.py`
* `openpilot/selfdrive/ui/mici/onroad/augmented_road_view.py`
* `openpilot/selfdrive/ui/mici/onroad/hud_renderer.py`
* `openpilot/selfdrive/ui/mici/onroad/torque_bar.py`
* `openpilot/selfdrive/ui/sunnypilot/mici/onroad/stop_indicator.py` (new)
* `openpilot/selfdrive/car/cruise.py` (one branch in `initialize_v_cruise`)
* `openpilot/sunnypilot/selfdrive/car/cruise_ext.py`
* `openpilot/sunnypilot/selfdrive/car/tests/test_set_speed_start.py` (new)
* `openpilot/sunnypilot/sunnylink/settings_ui_src/pages/visuals.yaml`, `cruise.yaml` and the generated `settings_ui.json`
* `.github/workflows/aaron-*.yaml`, `.github/workflows/copilot-setup-steps.yml`, this file, and the `aaron_*.md` docs
