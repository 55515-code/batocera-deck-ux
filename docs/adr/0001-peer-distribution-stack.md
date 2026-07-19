# ADR 0001: Peer Distribution Stack

Status: accepted for prototype

## Context

The OS needs low-cost, resilient distribution without allowing peers, trackers, gateways,
or a compromised mirror to decide what code a device installs. It should reuse Batocera's
existing torrent machinery and established security specifications.

## Decision

The first production data plane will use:

- TUF consistent snapshots and delegated roles as the only installation authority.
- BitTorrent v2/BEP 52 swarms for immutable bulk objects and release payloads.
- BEP 19 HTTPS web seeds and OCI/static mirrors as availability fallbacks.
- Signed magnet/torrent descriptors referenced by TUF target metadata.
- A dedicated, unprivileged object cache that cannot read general `/userdata`.
- Opt-in seeding with battery, metered-network, quota, schedule, and privacy controls.

The bootstrap image contains several independently operated metadata mirror addresses and
the initial TUF root. Peers may mirror metadata, torrents, and objects, but clients reject
expired, rolled-back, incorrectly signed, or digest-mismatched material.

## Deferred options

IPFS/libp2p will be benchmarked only when mutable catalog discovery, small-object exchange,
or community communication has a demonstrated requirement that BitTorrent plus signed
metadata cannot satisfy. Adopting it would add a second DHT, cache, NAT traversal stack, and
resource profile, so novelty alone is insufficient.

I2P is a future opt-in privacy profile for users who understand its separate network and
performance tradeoffs. It is not the default release transport and the UI must never call
ordinary P2P anonymous. Transport encryption protects links; signatures and hashes protect
release authenticity.

## Consequences

This decision provides a practical path from Batocera's current updater while keeping the
trust model transport-independent. It does not eliminate every bootstrap or relay service;
instead, those services become replaceable, untrusted, community-run peers rather than
authoritative infrastructure.
