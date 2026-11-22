# v0.20 Integrated Local Playtest

The v0.20 browser build aligns the local UI demo with the standalone v0.19 rules core:

- 5×6 board and 8-way connected clusters of 5+.
- Wild substitutes for a single regular symbol type; wild-only clusters do not pay.
- Deterministic overlap resolution: largest candidate first, then fixed symbol priority, then lowest cell index; candidates are accepted only if all cells are unclaimed.
- Maximum 12 cascades; cascade multiplier increases by 0.25× to a maximum of 4.0×.
- Scatter tiers: 3 → 5 free spins; 4 → 10; 5+ → 15 plus hidden multiplier.
- Maximum 500 free spins per originating paid round.
- Each credited component rounded to nearest 0.01× bet.
- Total paid-round win capped at 25,000× original bet.

## Important limitations

The HTML demo still generates outcomes client-side. This is not the official Stake Engine Math SDK implementation, does not generate official outcome books or lookup tables, and is not connected to Stake RGS. RTP remains unverified. Not for real-money use.

## Local artifact

The complete v0.20 HTML + v0.19 math-core bundle is provided as a ZIP in the project conversation.
