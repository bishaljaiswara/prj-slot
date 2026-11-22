# Twinkle Treats — official Engine Math SDK port (first pass)

This is a game overlay for the official Engine Math SDK, not a fork or a copy of the SDK.

## Official base
- Repository: https://github.com/engineio/math-sdk
- Sample used as architectural reference: `games/0_0_cluster`
- SDK requires Python 3.12+ and pip. Rust/Cargo is needed for its optimization algorithm.

## Install
1. Clone the official SDK: `git clone https://github.com/engineio/math-sdk.git`
2. From the SDK root run `make setup`.
3. Copy `games/twinkle_treats` from this overlay into the SDK checkout's `games/` folder.
   - Windows PowerShell: run `./install_into_sdk.ps1` from this directory.
   - macOS/Linux: run `./install_into_sdk.sh /path/to/math-sdk`.
4. From the SDK root run `python games/twinkle_treats/run.py`.

The run file currently creates only a tiny uncompressed 100-round debug batch. It deliberately does not run optimization, analysis or RGS format checks.

## First-pass implementation
- SDK-shaped GameConfig, GameState and calculation/executable adapter.
- 6 reels × 5 visible rows.
- 8-way connected cluster evaluation.
- Wild substitutes for one regular symbol type in a cluster; wild-only clusters do not pay.
- Candidate clusters are ordered largest-first, then fixed symbol priority, then first cell; accepted clusters cannot share cells.
- Temporary BR0/FR0 reel strips for wiring/debug only.

## Known blockers before a real SDK math build
- No Python 3.12 SDK environment has been run against this overlay in this workspace. Import/runtime compatibility is unverified.
- 500 free-spin cumulative ceiling is not yet implemented in SDK state.
- Scatter must be checked on the initial board and after every tumble, with one award per spin/cascade; SDK path still needs explicit override and tests.
- 5+ scatter hidden multiplier award and wallet/event accounting are not implemented.
- Exact nearest-0.01× per-component rounding and total 25,000× paid-round cap across base/free/hidden awards are not yet enforced in the SDK wallet path.
- Reel strips are placeholders, not calibrated math.
- RTP optimization, large simulations, analysis and `rgs_verification.py` remain pending.
- Frontend event mapping and RGS integration remain pending.

The 96.5% RTP is only a target. Do not publish this output or use for real-money play.
