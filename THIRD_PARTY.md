# Third-Party Software

## Batocera Unofficial Add-Ons

The default image includes the graphical launcher from
[Batocera Unofficial Add-Ons](https://github.com/batocera-unofficial-addons/batocera-unofficial-addons),
an independent GPL-3.0 community project that is not affiliated with the Batocera
team. The reviewed upstream commit and file hashes are recorded in
`third_party/bua/UPSTREAM.json`; corresponding source and license text are shipped
in the repository and image.

BUA is reused as-is instead of maintaining a competing store implementation. Its
catalog can install software from changing third-party network locations and some
catalog actions execute upstream shell installers with elevated Batocera privileges.
Those add-ons are not part of the immutable base image, are not authorized by the
OS release-signing keys, and need their own provenance and compatibility review.

Opening BUA is always an explicit user action. The base image does not launch it at
boot, preinstall catalog items, or include proprietary catalog payloads. Factory
reset and support tooling must be able to distinguish BUA-managed files under
`/userdata` from signed base-image files.

## ConnMan System Tray

The live prototype uses [CMST](https://github.com/andrew-bibb/cmst) `2023.03.14-2`
as an unprivileged graphical client for Batocera's existing ConnMan daemon. The package
was built from the Arch User Repository recipe at commit
`f4a6712266825dca944373aba1d241ade154b873`; its upstream source archive has SHA-256
`eba0ec46b99968f83b889079373d18f9e5c2c624b622a3fc95f09c9362f1f423`.

CMST is a prototype dependency only. It must never start a second ConnMan instance, and
it is not the shipping settings architecture because upstream describes the project as
feature-complete and largely unmaintained. The product direction is an unprivileged KDE
settings page backed by a narrow, typed host broker.
