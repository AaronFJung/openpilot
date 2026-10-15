# Aaron's openpilot fork

## About

<!-- Copy this paragraph into the repo's About description on GitHub (gear icon next to About). Keep it under 350 characters and update it when features change. -->
Aaron's fork of MVL's sunnypilot Honda branch for a comma four on a 2027 CR-V Hybrid. Adds UI toggles (hide confidence ball, hide wheel, planned stop distance, torque bar height) and a set speed start option. Synced nightly from mvl-boston/openpilot. See aaron_README.md.

A personal fork of [MVL's sunnypilot Honda branch](https://github.com/mvl-boston/openpilot) (`sp-honda-dev-202608`) for a comma four on a 2027 Honda CR-V Sport-L Hybrid. MVL's README.md is left untouched; everything of mine starts with `aaron_`.

* [aaron_FEATURES.md](aaron_FEATURES.md): what this fork adds and how to turn it on
* [aaron_TODO.md](aaron_TODO.md): ideas and known issues for later

## Install on the comma four

Uninstall the current software from the device settings, then enter this as custom software:

```
installer.comma.ai/AaronFJung/aaron-ui-sp-honda-dev-202608
```

The device builds the branch on first boot. To go back to MVL: `installer.comma.ai/mvl-boston/sp-honda-dev-202608`.

## Automation

| Workflow | What it does |
|---|---|
| `aaron-upstream-sync.yaml` | Nightly (and on demand): merges MVL's latest into `sync/<MVL branch>` and opens a PR into this branch. Conflicts open an issue. A newer `sp-honda-dev-YYYYMM` branch from MVL opens an issue, creates `aaron-ui-<new branch>`, and tries to port my commits |
| `aaron-copilot-autoassign.yaml` | Assigns Copilot to issues I open (including the sync issues). Other people's issues need the `copilot` label; `no-copilot` keeps it off |
| `copilot-setup-steps.yml` | Gives Copilot a built openpilot (`tools/op.sh setup` + `scons`) so it can run lint and tests |
| `.github/copilot-instructions.md` | Rules Copilot follows, including never touching safety code, and the list of files this fork changes |

Merging a sync PR is what deploys to the car, so check that the `tests` workflow passed first. Copilot opens draft PRs, and workflow runs on them wait for "Approve and run".

### One time GitHub setup

1. Repo Settings > General: default branch `aaron-ui-sp-honda-dev-202608`. The sync job follows whatever MVL branch that name points at.
2. Actions tab: enable workflows.
3. Fine grained personal access token limited to this repo, read and write on Actions, Contents, Issues, Pull requests and Workflows. Save it as repo secret `AUTOMATION_PAT`. Tokens expire; when the nightly job fails on auth, renew it.
4. Copilot plan with the Copilot cloud agent enabled for this repo.
5. Optional, quiets upstream workflows that only make noise on a fork:
   ```bash
   gh workflow disable lfs-maintenance.yaml -R AaronFJung/openpilot
   gh workflow disable stale.yaml -R AaronFJung/openpilot
   ```

## Develop in WSL (CommaUbuntu)

Commit in `C:\Users\comis\Documents\Car\openpilot`; build and test in WSL (symlinks and line endings break on NTFS).

```bash
git clone --branch aaron-ui-sp-honda-dev-202608 https://github.com/AaronFJung/openpilot.git ~/aaron-openpilot
cd ~/aaron-openpilot
git config pull.ff only
tools/op.sh setup
source .venv/bin/activate
scons -u -k -j"$(nproc)"
```

Update later with `git pull` (or `git fetch origin && git reset --hard origin/aaron-ui-sp-honda-dev-202608` after a force push), then `scons -u -k -j"$(nproc)"`.

### Demo UI

Skip onboarding once:

```bash
python -c "
from openpilot.common.params import Params
from openpilot.common.version import terms_version, terms_version_sp, training_version, sunnylink_consent_declined
p = Params()
p.put('HasAcceptedTerms', terms_version); p.put('HasAcceptedTermsSP', terms_version_sp)
p.put('CompletedTrainingVersion', training_version); p.put('CompletedSunnylinkConsentVersion', sunnylink_consent_declined)"
```

Then in two terminals (both with the venv active):

```bash
openpilot/tools/replay/replay --demo --wide-road --no-hw-decoder   # terminal 1
cd openpilot/selfdrive/ui && SCALE=2 ./ui.py                        # terminal 2, comma four layout
```

Flip settings live, for example `python -c "from openpilot.common.params import Params; Params().put_bool('ShowStopIndicator', True)"`.
