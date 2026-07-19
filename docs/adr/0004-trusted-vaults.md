# ADR 0004: Trusted Vaults

Status: proposed

## Purpose and Boundary

Trusted Vaults provide private backup and deliberate sharing of user-controlled data among
people and devices that mutually approve each other. The feature is content-neutral, but it
is not designed to evade monitoring, create a hidden public index, or distribute material a
participant lacks permission to share. The UI requires the owner to confirm that authority.

There is no global library browser, public search, popularity ranking, stranger matching,
or automatic trust inheritance. Knowing an invite code does not grant folder access.

## Reused Components

- Syncthing supplies mature device IDs, mutual device configuration, encrypted transport,
  folder synchronization, receive-only mode, conflict handling, and versioning. Batocera
  already packages it, so v1 adds a controller-first policy UI rather than another sync engine.
- Restic is the candidate storage-only backend for encrypted, authenticated backup objects
  when the replica operator must not see names or contents.
- I2P may later carry explicitly configured peer connections through its SAM API. It remains
  optional and experimental; the project does not build a routing or anonymity protocol.

Syncthing's encrypted untrusted-device mode is not a stable default while upstream labels it
beta/testing. It can be offered only in an experimental channel with an export/recovery test.

## Trust Model

A person profile and a device key are different objects. Pairing requires confirmation on
both devices and shows short authentication words plus a QR code. A grant then names one
vault, one recipient device set, one access mode, and an optional expiry:

- **Backup replica**: receive-only encrypted storage; cannot browse payloads.
- **Personal device**: read/write synchronization among one owner's devices.
- **Shared reader**: receives a read-only published snapshot and its decryption capability.

No peer becomes an introducer by default. Grants do not transitively authorize a recipient's
friends or new devices. Revocation stops future synchronization and key use where possible,
but cannot erase plaintext or keys a trusted recipient already copied; the UI states this
before a readable grant is issued.

## Network Modes

1. **Local/private address**: global discovery, public relays, NAT traversal, and usage
   reporting disabled; peers use explicit LAN, VPN, or owner-provided addresses.
2. **Direct assisted**: encrypted direct connection with narrowly selected discovery/relay
   services and a clear metadata disclosure.
3. **I2P experimental**: explicit destinations through a separately maintained I2P router,
   Ed25519 SAM destinations, bounded tunnels, and no clearnet fallback.

None of these modes promises invisibility. Network observers may still infer timing, volume,
endpoints, software use, or relationship metadata depending on transport.

## Data and Key Safety

Vault services receive only explicitly granted roots through a mount namespace. Credentials,
SSH material, update signing keys, private migration bundles, emulator keys, and system
configuration are denied by default. Every invite is signed, single-use, short-lived, and
contains no folder key in plaintext. Recovery keys are exported separately with an explicit
backup ceremony.

Public update swarms and Trusted Vaults use separate processes, identities, caches, ports,
logs, and policy. A public seeder can never discover or announce a vault object.

## Product UX

The graphical flow is: create vault, choose scope, choose backup or readable sharing, review
rights/privacy warning, pair peer, verify words on both screens, set limits, and confirm.
The dashboard shows last verified sync, copies available, peer access, storage consumed,
version history, pause, revoke, rotate key, restore, and export recovery information.

## Library Integration

Library vaults use Batocera's generated system definitions as the authority for system names,
ROM directories, and accepted extensions. Users can select complete systems, ES collections,
or individual titles. A published library is send-only; a recipient stages it outside the
live library, verifies its signed manifest and hashes, reserves space, previews conflicts,
then commits files atomically into `/userdata/roms/{system}` and asks ES to refresh.

Metadata and artwork can travel with a library. Saves require a separate explicit grant.
Raw emulator configuration never travels with content: shareable settings use a versioned,
declarative allowlist that cannot contain commands, absolute paths, account data, or keys.
Executable-oriented systems such as Ports and Windows remain disabled until a stronger
package-signing and sandbox review exists. The machine contract is
`profiles/library-vault-v1.json`.
