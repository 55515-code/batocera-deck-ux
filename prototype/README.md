# Prototype Code

These files mirror the currently validated live Deck prototype. They are retained
for review, tests, and conversion into Batocera Buildroot packages; they are not a
production installer and must not be copied blindly to another device.

Known non-shipping properties:

- Plasma uses a chroot with broad host mounts.
- The desktop image is not pinned or reproducible.
- Steam remains a local third-party RunImage integration.
- Some controller and ES identifiers are Steam Deck LCD-specific.
- Local provisioning, package installation, and migration scripts are intentionally
  excluded until they no longer contain machine-specific assumptions.

The production move is to split this into a host lifecycle supervisor, a reviewable
controller bridge package, a versioned immutable desktop artifact, a narrow privilege
broker, and controller-first graphical clients.

`addons/bua.sh` replaces the live Deck's moving-branch `curl | python3` launcher
with a hash-checked local copy of the reviewed BUA upstream application.
