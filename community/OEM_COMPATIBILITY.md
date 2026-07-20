# Downstream Compatibility Program

This program gives device makers and downstream distributions a practical reason
to test with LuigiOS without requiring LuigiOS branding, promotional attribution,
exclusive hardware, fees, or assignment of their changes.

## What the project offers

- A public compatibility entry linked to the downstream's product or support page.
- Candidate-image notice and a shared release-test window when maintainers have capacity.
- Reproduction help for failures that affect supported, upstreamable interfaces.
- Review of reusable controller, display, audio, suspend, storage, and recovery patches.
- Credit for submitted evidence when the submitter requests it.

Listings report evidence; they are not warranties, certifications, or paid endorsements.
The project may remove or age a listing when its image digest, support URL, or results
can no longer be verified.

## Qualification

1. Submit the GitHub **Hardware test report** against an identified image digest.
2. Include the hardware revision, firmware version, controllers, display path, and
   storage configuration needed to reproduce the result.
3. Exercise the current candidate-image gate in `docs/TESTING.md` and identify every
   skipped or failed case.
4. Provide a public support contact if the device is sold to end users.
5. State whether the submitter wants a public listing, link, and attribution.

Evidence is assigned the `community-tested`, `downstream-maintained`, `experimental`,
or `unverified` tier defined in `profiles/hardware-support-v1.json`. Steam Deck remains
the core `reference` platform. A tier always identifies the tested image and hardware
tuple, limitations, evidence date, and responsible support party. Results from
maintainers, volunteers, owners, and manufacturers use the same evidence schema.

## Boundaries

- A listing never grants permission to use LuigiOS marks or imply official manufacture.
- Security reports follow `SECURITY.md`, not public compatibility issues.
- Device vendors remain responsible for warranties, regulatory obligations, customer
  support, bundled content, and compliance with every redistributed component license.
- Commercial status neither raises nor lowers the technical acceptance bar.
- Community-tested and experimental entries carry no core-project support promise.
- A result for one revision never implies compatibility with a device family.

The broader fork and branding position is defined in `DOWNSTREAM.md`.
