# Twinkle Treats

Original 5×6 cluster/tumble slot prototype.

## Repository layout
- `game/twinkle_treats_integrated_v020.html`: local browser playtest.
- `math/v0.19/twinkle_math_core.py`: deterministic cluster/rules helper.
- `math/v0.19/test_math_core.py`: automated rules tests.
- `spec/round_rules_contract_v0.18.json`: versioned rules contract.
- `DEVELOPMENT_STATUS.md`: remaining SDK and release work.

## Run
Open the game HTML in a modern browser.

For math tests:
```bash
python -m pip install pytest
cd math/v0.19
python -m pytest -q test_math_core.py
```

## Limitations
The browser demo uses client-side randomness. The Python module is a standalone rules helper, not an official Stake Engine Math SDK game. Outcome books, lookup tables, RGS integration, certified RNG, verified RTP and publication approval are not complete. 96.5% RTP is a target only. Do not use for real-money play.
