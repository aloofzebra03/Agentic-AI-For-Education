# Educational API v9.9.6 — local build

Built and checked on 13 October 2026 (IST). Not pushed to Docker Hub and not
deployed to a running container.

Local tags:

- `aloofzebra03/educational-api:v9.9.6`
- `aloofzebra03/educational-api:latest`
- `aloofzebra03/educational-api:v9.9.6-candidate`

Image ID: `sha256:9ebd819c9462f24f739c75ca707f43bc244ba8b7b1be209091036da4a261274e`.

## Comparison with the pulled published image

The pulled Docker Hub `latest` resolved to v9.9.5, digest
`sha256:84968d854ebd09dd7ad690e4458d6d28939d5dbb7f8d71daebab1713ff744b8a`.

| Image | Science SVGs | Maths SVGs | Total |
| --- | ---: | ---: | ---: |
| Published v9.9.5 | 16 | 9 | 25 |
| Local v9.9.6 | 34 | 27 | 61 |
| Added since published release | 18 | 18 | 36 |

Ten of these 36 additions were created in the latest batch: five science scenes
for cells/batteries, conductors/insulators, malleability, ductility and sonority;
five exact maths-agent problems for bracket methods, quiz-score like terms,
isosceles angles, petrol-distance fractions and additive inverses.

All 25 original SVG file checksums match the new image. All 30 base layers are
retained. `Dockerfile.whiteboard-update` replaces only `/app/whiteboard_tutor`.
Main API files, utilities, other teaching agents and dependencies are inherited
unchanged from v9.9.5. The POC working-tree package, including uncommitted new
assets, is the source used for this build; a future rebuild can differ.

## Checks

- Chrome-extension visual review of all ten new scenes, with label and diagram
  corrections during review.
- POC Streamlit science/math selectors contain 34 and 27 lessons respectively;
  all ten new lessons start successfully.
- All 61 scenes pass trusted SVG validation; individual parts of new scenes
  render successfully.
- All 18 bundled maths snapshots match the original maths-agent JSON records.
- Container main API imports; health, concept catalog, scene manifest and all
  61 SVG downloads succeed. Science and maths whiteboard sessions support
  start/status/delete and include reveal timelines.
- Original `/session/start`, `/session/continue`, `/math/session/start` and
  `/doubts` endpoints remain registered.

Container API checks used authentication overrides and `InMemorySaver`; live
Gemini requests, production Postgres persistence and device audio were not tested.
Pre-existing legacy concept-map/audio import warnings did not prevent checks.

## Rebuild

From `Agentic-AI-For-Education`, with the POC alongside it:

```powershell
docker build -f Dockerfile.whiteboard-update `
  --build-context whiteboard_poc=../Whiteboard_Tutor_Education_POC `
  --build-arg BASE_IMAGE=aloofzebra03/educational-api@sha256:84968d854ebd09dd7ad690e4458d6d28939d5dbb7f8d71daebab1713ff744b8a `
  --label org.opencontainers.image.version=v9.9.6 `
  --label education.whiteboard.scene-count=61 `
  -t aloofzebra03/educational-api:v9.9.6 .

docker tag aloofzebra03/educational-api:v9.9.6 aloofzebra03/educational-api:latest
```

Docker Hub `latest` remains v9.9.5 until explicitly pushed. No push was performed.
