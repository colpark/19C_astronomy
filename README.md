# 19C astronomy — FM-advantage benchmark, astronomy application

This repo applies the `fm-advantage-benchmark` skill (vendored unchanged under `fm-advantage-benchmark/`) to live time-domain astronomy: the Rubin LSST alert stream plus the ZTF Bright Transient Survey (BTS) label base.

It does two jobs at once:

1. **A supply gauge**, run as a five-agent panel. This is a pre-P1 sketch, not a P4 ruling. The skill refuses a ruling until all seven axes carry numbers taken from full source reads.
2. **An independent-corpus replay.** The skill warns that its replay suite comes from one project. An astronomy run is the out-of-project corpus that warning asks for.

Work lands under `astronomy/`. Start with [`astronomy/SYNTHESIS.md`](astronomy/SYNTHESIS.md), then [`astronomy/replay/RESULT.md`](astronomy/replay/RESULT.md).
