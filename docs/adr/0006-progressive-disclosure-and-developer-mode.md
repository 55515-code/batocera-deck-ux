# ADR 0006: Gamer Experience and Developer Mode

Status: accepted product direction

## Context

LuigiOS serves two audiences on the same device. The default owner wants a
polished game system that a child or nontechnical family member can operate and
configure with a controller. Contributors and device designers need access to
files, logs, terminals, development tools, and unsupported controls. Exposing
both audiences to every Linux implementation detail would make the normal
experience noisy and unsafe; permanently removing those tools would make the
system hostile to the people extending it.

## Decision

The factory and reset default is **Gamer Mode**. It presents one LuigiOS app
library, one Device Settings application, task-oriented language, safe presets,
and graphical recovery. Supported setup, play, networking, controller, display,
audio, storage, application, update, backup, restore, and reset workflows must
be complete without a terminal, root login, or knowledge of the base
distribution.
The first foreground task is finding and playing a game; OS implementation and
commercial service placement remain secondary to the owner's library and choices.

An intentionally enabled **Developer Mode** progressively reveals terminals,
raw logs, package and filesystem detail, development applications, unsupported
switches, and extension tooling. Developer Mode extends Gamer Mode rather than
replacing it: controller navigation, unified settings, graphical tools, stable
errors, rollback, and the LuigiOS visual language remain available.

The machine-readable contract is
[`profiles/experience-modes-v1.json`](../../profiles/experience-modes-v1.json).
ADR 0005 remains the source of truth for settings and privileged operations.

## Development connectivity protection

Developer Mode protects active SSH work against incidental Wi-Fi route loss. An
image-owned guard observes active SSH process environments, remembers the last healthy
ConnMan Wi-Fi service, and retains a 15-minute protection window after the connection
drops. If the default route disappears during that window, it asks the existing host
ConnMan daemon to reconnect using exponential backoff capped at two minutes.

The guard does not restart ConnMan, replace network policy, introduce a second network
daemon, or act outside Developer Mode. It records whether Wi-Fi was powered when the
protected session began and may re-enable the radio only when that baseline was on. This
preserves deliberate offline state while recovering from incidental radio loss during
remote development. Status is observable under `/run/luigios-dev-connectivity`; recovery
and disabling Developer Mode always stop further protection.

## Activation and recovery

Developer Mode is enabled from the hidden-by-default Developer Mode settings
surface through an explicit risk summary and confirmation. If owner
authentication is configured, activation requires it. A session restart makes
the visibility change atomic; applications do not appear one by one during a
live session. Recovery can always disable Developer Mode without deleting user
data, even if the desktop no longer launches.

Factory reset and new-user setup return to Gamer Mode. Images, add-ons, OEM
profiles, and migrations may not silently enable Developer Mode.

## Unified presentation

Gamer Mode hides duplicate upstream launchers and distribution plumbing, not
licenses or factual attribution. The foreground uses product concepts such as
Apps, Storage, Updates, Controllers, and Restore Points. Raw package names,
service units, mount paths, and terminal output are available in diagnostics or
Developer Mode but are translated into stable user-facing states elsewhere.

Apps should launch through a LuigiOS library entry or settings deep link.
Separate upstream control panels remain implementation details when their
function is already represented in Device Settings. Unsupported tools are not
deleted from the image solely to hide them; visibility is policy-driven so a
Developer Mode transition is reversible and testable.

## Security boundary

Developer Mode is a capability-discovery and support-state switch, not a
privilege boundary. It does not run the desktop or settings UI as root, grant
unrestricted host sudo, make the immutable image writable, disable signed
update verification, or permit arbitrary commands through the privileged
broker. Developer tools may perform user-authorized work within their actual
permissions, and truly privileged operations still use typed, reviewed broker
methods.

## Acceptance criteria

- A first-time user can complete setup and common maintenance with controller,
  touch, or an external gamepad without encountering a terminal or root prompt.
- Gamer Mode contains no dead launchers, duplicate settings, raw stack traces,
  package-manager dialogs, or unexplained Linux vocabulary.
- Developer Mode activation, session restart, persistence, disable, and
  recovery-reset paths are automated and hardware-tested.
- Every supported workflow remains graphical in Developer Mode; opening a
  terminal is a choice, never the documented primary path.
- Both modes pass handheld, docked, offline, interrupted-operation, and
  accessibility tests.
- Active SSH work survives a simulated default-route loss by reconnecting the last
  healthy Wi-Fi service without restarting ConnMan; retries honor bounded backoff.
