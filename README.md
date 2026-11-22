# Twinkle Treats

Original 6×5 cluster/tumble slot-game prototype.

## Project status
- Visual baseline: v0.13 polished playtest (frozen; do not overwrite).
- Rules contract: v0.18.
- Standalone deterministic math core: v0.19.
- Official Stake Engine Math SDK integration: not yet implemented.
- RTP target: 96.5%; experimental only, not certified or verified.
- Not approved for real-money use.

## Repository layout
- `game/`: browser playtest build.
- `math/v0.19/`: standalone Python math rules core and tests.
- `spec/`: versioned rules contract.

## Run math-core tests
```bash
python -m pip install pytest
python -m pytest -q math/v0.19/tests
```

The v0.19 module is a deterministic rules harness, not official Stake Engine SDK code. See `math/v0.19/README.md` for limitations and next steps.
