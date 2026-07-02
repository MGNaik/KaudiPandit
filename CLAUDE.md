# KaudiPandit — Project Context for Claude Code

This file gives you (Claude Code) the standing context for the KaudiPandit
project. Read it at the start of each session.

## What this project is

KaudiPandit is a Python engine plus AI agent for **Kauda Baji** (also spelled
Kauda-baji), a traditional Gujarati variant of the cross-and-circle board game
Chowka Bhara. The long-term goal is a complete, unambiguous model of the game
in code, then AI agents that play it well, and eventually (stretch) a physical
robot that plays a human across a real board.

Repo: github.com/MGNaik/KaudiPandit

This is one project (P1) in a larger self-directed 3-year robotics/AI/control
portfolio. Its through-line with the rest of the portfolio: the Bellman
equation / dynamic-programming spine underlies both game-tree search here and
optimal control in the physical projects.

## Working preferences (important)

- **For actual programming/coding: guide, don't hand over code.** Walk me
  through the concept, the design tradeoffs, and the architecture, and let me
  write the implementation myself. I'll ask directly when I'm stuck on syntax.
  This is a strong, standing preference — please respect it even when it would
  be faster to just write the code.
- **Exception — documentation, LaTeX, SVGs, and the rules document:** for those
  I want direct solutions and finished artifacts, not coaching.
- **Design before building.** Reason through architecture collaboratively first;
  write pseudocode and a test list before implementing a class, then write full
  tests.
- **Writing before coding.** I treat docs and blog posts as a way to surface
  ambiguities before they become bugs.
- **Honest, direct assessment.** Push back on my framing when warranted. Flag
  scope inflation against the portfolio's "ship focused projects" principle.

## Environment & tooling

- **OS/hardware:** Ubuntu 24.04 (primary, on a Samsung T7 SSD). Also a Windows
  laptop (i7-11370H, 16GB) and a MacBook reached via RDP/Tailscale.
- **Python stack:** `uv` for dependency management, `pyproject.toml`, `src/`
  layout, `ruff` for linting, `pytest` (fixtures + parametrize).
- **ML/training:** Google Colab (T4-class GPU) for any self-play training.
  Measure CPU speed first; batching required to make the GPU worthwhile.
- **Editors:** Vim (primary), VS Code (debugging). GitHub Copilot is disabled
  by preference.
- **Language mix:** Python primary, C++ background.

## Domain model — current state

The codebase has moved from a mutable OO model toward an **immutable
value-object model** suited to expectimax tree search (flat immutable states
succeeding one another; `apply(board, move)` returns a new board via structural
sharing).

Completed:
- Dice engine (`kaudis.py` with `Kaudi` / `KaudiSet`)
- `Board` (static geometry)
- `Player` (with CCW-rotation-derived path dicts — verified correct for all
  four players by visual inspection)
- `Piece`, `Position` / `Square` NamedTuples, `PlayerID` enum

Key architectural conclusions reached:
- `PieceTuple` is a frozen value object: `(owner: seat_id, position: Square,
  size: int)`.
- The **board is the real state unit**; pieces are not independently
  identified in state.
- Piece IDs are metadata only — excluded from state equality and move
  generation.
- "Kachu" is a derived configuration, not a stored object.

## Game rules — settled

**Board:** 7×7 grid. Four players, one per edge. Each player's pieces start on
the crossed square in the middle of their edge and finish on the centre square.
Safe squares (corner-to-corner cross, no kills possible): the four starting
squares, the four board corners, the four squares diagonally adjacent to
centre, and the centre itself.

**Movement:** all four players follow the same route, rotated per player. A
piece travels the outer ring **anticlockwise**. At the first arrow it turns
inward onto the first inner band and travels **clockwise** around it. At the
second arrow it turns inward again onto the second inner band, still
clockwise. The third and final arrow carries it onto the centre square. (This
supersedes an earlier "go around the outer ring twice" draft — corrected
2026-07-02 against the actual path diagram, which has three concentric paths
joined by three arrows.)

**Capture / kill rules (settled):**
- Landing tuple of size ≥ resident opponent tuple → resident is killed.
- Strictly smaller lander → coexists (shares the square).
- On a shared square, a strictly larger tuple **kills on exit** as it departs;
  a smaller tuple leaving simply escapes.
- Safe squares: no kills ever, any number of tuples coexist.
- Multi-player squares: resolve pairwise-independently (Rules 1–2 applied to
  each opponent separately).
- Equal-size opponent coexistence on an ordinary square is unreachable by
  construction.

## Open questions (not yet settled)

- **Ripeness/kacha-paku status: per-piece or per-tuple?** This determines
  whether the `Piece` class survives or collapses into tuple counts. Resolve
  this before building the move enumerator.
- **Value network output shape:** scalar win-probability conditioned on seat,
  or a four-vector of all players' win-probabilities simultaneously.
- Rules doc "questions for the family" still open: does a kill earn an extra
  throw; must a player make a kill before entering inner rings; do killed
  pieces return as singles or as the tuple they were (my proposal: singles).

## Remaining build sequence

1. Resolve kacha/paku per-piece vs per-tuple.
2. Possible-moves enumerator → legal-action assembly → captures.
3. `PieceTuple` → `Projector` → game loop.
4. Strategy hierarchy → headless play.
5. Visualiser (HTML/SVG, blog-embeddable).
6. `HeuristicStrategy` (this is where domain knowledge gets made explicit; also
   the benchmark for learned agents).
7. State encoding (state object → fixed numeric vector for NN input).
8. Self-play training on Colab.

## AI architecture (planned)

Shallow **expectimax**: one ply of own moves plus chance-node weighting by
kaudi bias, backed by a learned seat-conditioned value function.

Success metrics that matter (not just "beat available humans"): agent-vs-
heuristic win rate, unprompted emergence of anti-leader behaviour, self-play
convergence curves, value-function calibration.

## Repo access note

Prefer direct `git clone` over GitHub web URLs — robots.txt blocks `/tree/`
paths.
