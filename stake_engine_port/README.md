# Twinkle Treats — official Math SDK port (in progress)

This directory is an **overlay for the official Engine Math SDK**, not a standalone SDK clone.

## Install into the official SDK checkout
1. Clone https://github.com/engineio/math-sdk
2. Install Python 3.12+ and pip. Install Rust/Cargo if running optimization.
3. From the SDK root, run `make setup`.
4. Copy this directory's contents into the SDK checkout at `games/twinkle_treats/`.
5. Run from the SDK root: `python games/twinkle_treats/run.py`.

## Port status
Implemented in this first integration pass:
- SDK-shaped GameConfig, GameState and executable/calculation adapter.
- 6 reels × 5 visible rows.
- 8-way cluster resolver with wild substitution, no wild-only awards and deterministic non-overlap resolution.
- Initial base/free mode configuration and SDK book/config generation entry point.

Not yet implemented or verified:
- The 500-free-spin cumulative ceiling in SDK state/wallet.
- Scatter checks after every tumble (SDK's stock trigger path must be extended for the agreed rule).
- 5+ scatter hidden multiplier award and its event/wallet accounting.
- Exact per-component rounding and total 25,000× paid-round cap across base + freegame + hidden award.
- Proper calibrated reel strips, RTP optimization, force distributions, large simulation batches, RGS verification.
- Frontend event adapter and RGS integration.

The bundled reel strips are **temporary placeholders**, not balanced production strips. RTP 96.5% is only a target. Do not publish or use for real-money play.
