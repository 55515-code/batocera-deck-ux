# Batocera Deck UX SDK

The SDK is a thin orchestration layer around the upstream Batocera Buildroot tree and
official Batocera build container through Docker or Podman. It does not maintain a compiler, sysroot, package
manager, emulator toolchain, or parallel image format.

## Quick start

```bash
./tools/sdk doctor
./tools/sdk bootstrap
./tools/sdk config
./tools/sdk package batocera-deck-bua
```

`bootstrap` checks out the Batocera revision in `sdk/versions.env` under `.sdk/batocera`
unless `BATOCERA_DIR` names an existing checkout. Existing dirty trees are never reset.

Commands:

- `doctor`: inspect host tools, source revision, disk space, and container availability.
- `bootstrap`: clone the pinned Batocera source and initialize its Buildroot submodule.
- `config`: generate the x86_64 configuration using both external trees in the container.
- `config-local`: perform the same Kconfig parse with host tools for a fast smoke test.
- `package NAME`: build one Buildroot package in the official container.
- `image`: build the complete x86_64 image; this is intentionally expensive.
- `shell`: open the official build container with the same mounts and environment.
- `test`: run the repository's fast local gate.

SDK state stays under `.sdk/`: output, downloads, compiler cache, and the default source
checkout. CI should cache downloads and ccache by pinned source/toolchain identity, never
publish the writable workspace, and upload only reviewed public build artifacts.
