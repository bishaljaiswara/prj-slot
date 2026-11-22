# Twinkle Treats

Original 6×5 cluster/tumble slot-game prototype.

## Project status
- Frozen visual baseline: v0.13 (preserved; do not overwrite).
- Rules contract: v0.18.
- Deterministic standalone math core: v0.19.
- Integrated local browser playtest: v0.20 (rules aligned; still client-side demo randomness).
- Official Stake Engine Math SDK / RGS integration: not yet implemented.
- RTP target: 96.5%; experimental only, not certified or verified.
- Not approved for real-money use.

## Repository layout
- `game/v0.20/`: v0.20 local playtest integration notes.
- `math/v0.19/`: standalone Python math rules core and tests.
- `spec/`: versioned rules contract.

## Run math-core tests
```bash
python -m pip install pytest
python -m pytest -q math/v0.19/tests
```

The v0.19 module is a deterministic rules harness, not official Stake Engine SDK code. The v0.20 browser playtest has a downloadable bundle shared in the project conversation; it is not an RGS-connected game.
