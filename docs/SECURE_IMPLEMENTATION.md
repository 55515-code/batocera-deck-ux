# Secure Implementation Policy
LuigiOS treats memory safety, least privilege, and reproducible trust as design inputs,
not release cleanup. The goal is modern platform-quality code without replacing mature
upstream projects merely to claim local ownership.

This policy governs code authored for LuigiOS. Imported projects retain their upstream
language and architecture, but integrations must pin versions, isolate privileges, track
vulnerabilities, preserve security updates, and avoid expanding their trust boundary.

## Security objectives

Every new LuigiOS component is designed around five practical outcomes:

- Memory-safe implementation by default, with a narrow and reviewed exception path for
  unavoidable unsafe, FFI, kernel, or hardware code.
- Defense in depth across process privileges, filesystem access, kernel controls, input
  bounds, authenticated updates, and recoverable state transitions.
- Small, explicit security cores: privileged services do the minimum work required and
  expose typed operations instead of general command execution.
- Fail-closed handling of untrusted ROM metadata, archives, network objects, controller
  input, and update content, while preserving user data during crashes or interrupted work.
- Evidence before promotion: policy checks, static analysis, hardening, dependency review,
  sanitizers, fuzzing, and recovery tests are release inputs rather than post-release hopes.

“Secure core” refers to the small privileged boundary that protects device settings,
storage, updates, migration, and recovery. It does not mean that an emulator, desktop
application, or imported upstream component is trusted merely because it is included in
the image. Those applications remain unprivileged where practical and are isolated behind
the narrowest supported boundary.

## Language selection

1. New image-owned daemons, privileged brokers, network services, update clients,
   artifact verifiers, parsers, and long-running native components default to stable Rust.
2. Rust crates use `#![forbid(unsafe_code)]` when possible. Necessary FFI or hardware
   access lives in a small module with a documented invariant, a `SAFETY` explanation,
   focused tests, and security review.
3. Python is appropriate for unprivileged workstation tools, deterministic generators,
   and orchestration where native performance is unnecessary. Use typed structured
   parsers, argument-vector subprocess calls, bounded inputs, and no dynamic evaluation.
4. Shell is limited to short lifecycle and build orchestration. It must use strict error
   handling, quote expansions, validate external identifiers, use atomic state updates,
   and delegate complex parsing or security decisions to structured code.
5. New C or C++ requires a written hardware, kernel, ABI, or upstream-integration reason.
   It must avoid owning untrusted parsing where a memory-safe boundary is practical and
   must pass the native hardening and dynamic-analysis requirements below.

Rewriting a maintained dependency is not automatically safer. Prefer a narrow, pinned,
well-isolated integration with a clear update path over a new local implementation.

## Memory and native-code hardening

- Native executables use PIE, ASLR, non-executable stack, stack protection, full RELRO,
  immediate binding, and the strongest supported `FORTIFY_SOURCE` level.
- Release builds retain integer-overflow checks where the language/toolchain supports
  them. Debug and candidate builds enable assertions without exposing secrets.
- Native code runs under AddressSanitizer and UndefinedBehaviorSanitizer in CI-capable
  host builds. Parser and protocol surfaces receive coverage-guided fuzzing.
- Rust unsafe code additionally receives Miri or an equivalent interpreter check where
  supported. Dependency review uses locked versions plus vulnerability and license audits.
- Secrets are kept out of command lines, logs, crash reports, and general configuration.
  Secret-bearing buffers use established zeroization types; copies and lifetimes are
  minimized. Core dumps are disabled for services that can hold credentials or keys.
- Inputs have explicit size, count, nesting, path, and time limits. Integer conversions,
  allocation growth, decompression ratios, and archive extraction paths fail closed.
- Low-memory and allocation-failure behavior is part of fault testing. A service may
  reject work or restart cleanly; it must not corrupt persistent state.
- Emulator content, save data, metadata, and imported configuration are treated as
  untrusted input even when supplied locally. Parsers and importers must use bounded,
  recoverable workflows and must never require root merely to play a game.

## Process and privilege boundaries

- Foreground interfaces run unprivileged. Root work is exposed through typed broker
  methods with narrow arguments and authorization, never arbitrary shell commands.
- Long-running services receive a dedicated user where practical, `no_new_privs`, a
  capability allowlist, read-only executable/configuration paths, bounded writable state,
  private temporary storage, and resource limits.
- Apply seccomp, Landlock, namespaces, or equivalent kernel controls when supported by
  Batocera and the component's job. Document unavailable controls instead of silently
  claiming isolation.
- Network listeners bind only where needed, authenticate before expensive work, rate-limit
  failures, and use maintained cryptographic protocols and libraries. Do not design custom
  cryptography, password storage, or update-signature formats.
- Services have bounded restart policy, health status, and rollback. Watchdogs must not
  create destructive loops or seize policy owned by another system component.

## Supply chain and review

- Dependencies, toolchains, base images, and source commits are immutable inputs. Builds
  do not execute moving remote scripts and produce SBOM, license, provenance, and checksum
  evidence.
- Minimize dependencies across privileged boundaries. Every dependency added to a broker,
  parser, network service, or boot path requires a maintenance and vulnerability rationale.
- Security-sensitive changes include a threat-boundary note, negative tests, malformed
  input tests, interruption tests, and recovery behavior. Two-person review is required
  before stable release once multiple maintainers are available.
- CI gates formatting, warnings, dependency audit, static analysis, native hardening,
  sanitizer tests, and fuzz smoke tests appropriate to the changed component.
- Security findings follow `SECURITY.md`; fixes include regression tests and identify
  affected artifacts without publishing user secrets or exploit-ready private data.

The machine-readable contract is
[`profiles/secure-implementation-v1.json`](../profiles/secure-implementation-v1.json).
