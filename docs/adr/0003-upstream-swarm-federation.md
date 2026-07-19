# ADR 0003: Upstream Swarm Federation

Status: accepted for prototype

## Context

Batocera already ships a Transmission-based `batocera_torrent` service and produces
stable update torrents with public trackers. A derivative can harm both communities if it
repackages identical bytes under new identities, discards a vanilla user's torrent state,
or diverts peers into a branded but unnecessarily separate swarm.

## Decision

Upstream and derivative artifacts are federated by content identity, not project name.

- An unchanged Batocera artifact retains its upstream filename, digest, torrent info
  dictionary, source attribution, and upstream swarm identity. We do not make a cosmetic
  rebuild or replacement torrent merely to claim it as a Deck UX artifact.
- Our peer may seed upstream-authorized public artifacts from the dedicated object cache
  when the user enables seeding. This traffic follows the same battery, metered-network,
  bandwidth, schedule, privacy, and cache limits as project traffic.
- Derivative artifacts with any byte difference receive a separate target digest and swarm.
  They reference the exact upstream source/image provenance from which they were produced.
- Shared immutable objects are stored once by digest. Signed Batocera and Deck UX catalogs
  may both reference an identical object without copying it into competing namespaces.
- Installing over vanilla Batocera preserves recognized torrent state and completed public
  update payloads after validating paths and hashes. It never erases, retags, or silently
  stops upstream seeds simply because the device changed release channels.
- Upstream removal, revocation, trademark, tracker, and opt-out requests are respected. The
  project does not announce to an upstream tracker with altered content or impersonate an
  upstream release signer.

The UI reports aggregate contribution plus per-community ratios without turning bandwidth
into a loyalty contest. Users can stop one catalog, all seeding, or delete cached objects;
the cache manager explains when one object is still referenced by another trusted catalog.

## Implementation Notes

The existing Batocera torrent directory is imported read-only first, then recognized jobs
are adopted transactionally into the managed cache. Unknown personal torrents remain
untouched and outside the OS updater. TUF roots stay separate: trusting Deck UX does not
grant its keys authority over Batocera targets, and vice versa.

Cross-seeding is allowed only when the torrent's complete content identity matches. Similar
files or common chunks may save local disk through the content store, but they do not justify
joining a swarm whose advertised artifact differs.
