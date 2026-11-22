# Twinkle Treats v0.19 — deterministic math core

Standalone deterministic Python implementation of the 5×6 cluster, wild, overlap, scatter-tier, free-spin ceiling, cascade-multiplier and integer-hundredths wallet rules.

**This is not an official Stake Engine Math SDK game.** SDK game-state integration, outcome generation, books, lookup tables, optimization and RGS verification remain outstanding.

## Run tests
```bash
python -m pip install pytest
python -m pytest -q
```

## Deterministic overlap policy
Eligible candidate clusters are ordered by descending cluster size, fixed symbol priority (gem, berry, blue, lolli, orange, heart, lemon), then lowest cell index. Candidates are greedily accepted only if none of their cells has already been claimed.

This overlap policy is an implementation choice and must be accepted before math is frozen.

## Not implemented
- Official SDK GameConfig/GameState/executable/event integration.
- RTP-calibrated symbol generation and complete paid/free-spin orchestration.
- Weighted hidden multiplier RNG in official SDK.
- Books, lookup tables, index.json, optimization and RGS verification.
- Browser frontend ↔ RGS event playback.

No real-money use. No RTP certification.
