# KaudiPandit — Plan

Single source of truth for project context and progress. `CLAUDE.md` is now
just a pointer to this file. `docs/Rules/Rules.tex` remains the rules source
of truth — this file only summarizes settled rules, it doesn't restate them.

Last reconciled against actual repo state: 2026-08-18.

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
  layout, `ruff` for linting, `pytest` (fixtures + parametrize). Target
  tooling — actual `pyproject.toml` currently configures `black`/`isort`/
  `mypy` instead, has no `[project]` section, and dependencies are tracked
  via `requirements.txt`, not a `uv.lock`. Not yet aligned to the above.
- **ML/training:** Google Colab (T4-class GPU) for any self-play training.
  Measure CPU speed first; batching required to make the GPU worthwhile.
- **Editors:** Vim (primary), VS Code (debugging). GitHub Copilot is disabled
  by preference.
- **Language mix:** Python primary, C++ background.

## Status snapshot

**Built and present:**
- Dice engine — `src/kaudis.py` (`Kaudi`, `KaudiSet`, `KaudiState`)
- `Board` — `src/board.py` (static geometry, safe/final positions)
- `Player` — `src/players.py` (per-seat CCW-rotated starting square + path,
  verified correct for all four players by visual inspection)
- `Piece`, `Position`/`Square` (NamedTuples), `PlayerID` — `src/types.py`,
  `src/pieces.py`

**Stubbed, not wired in:**
- `PieceTuple` — `src/pieces.py` (plain mutable class, correct fields, never
  instantiated; `Player.piece_tuples` is always `[]`)
- `src/game.py`, `src/strategy.py` — empty files, no content yet

Imports are fixed and `pytest` passes all 29 tests clean (verified
2026-08-18) — see item 0 below.

## Domain model — target vs actual

**Target design** (not yet implemented): move from the current mutable OO
model toward an **immutable value-object model** suited to expectimax tree
search (flat immutable states succeeding one another; `apply(board, move)`
returns a new board via structural sharing).

Key architectural conclusions reached (target, to be built toward):
- `PieceTuple` is a frozen value object: `(owner: seat_id, position: Square,
  size: int)`.
- The **board is the real state unit**; pieces are not independently
  identified in state.
- Piece IDs are metadata only — excluded from state equality and move
  generation.
- "Kachu" is a derived configuration, not a stored object.

**Actual current code** (`src/pieces.py`, `src/players.py`) is still the
earlier mutable OO style: `Piece` and `PieceTuple` are plain mutable classes,
and `Piece.owner` holds a live `Player` object reference rather than a
`seat_id`. This is intentionally fine for Phase 1/2 below (random play,
heuristic strategy — neither branches, so mutation is safe). The refactor
toward the value-object model above is tracked in build sequence Phase 3,
gated behind starting search-based agents.

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

Full rule text (all 16 rules) lives in `docs/Rules/Rules.tex`.

## 0. Immediate blocker

- [x] Fix the `docs.Rules.src.*` → `src.*` import paths (`src/board.py`,
      `src/players.py`, all of `tests/`) so the existing test suite runs
      again. **Done (2026-08-18)** — `pytest` collects and passes all 29
      tests clean.

## Open design questions

- [x] **Kacha/paku (ripeness): per-piece or per-tuple?** — **Resolved
      (2026-08-18): it's a per-tuple concept, not per-piece.** "Kacha" is a
      piece not currently bound into a formed tuple (Rule 7); "paku" is a
      formed tuple, which per Rule 8 must move and be killed as one unit
      until it next reaches a safe square. This state doesn't need its own
      stored field — it falls out of the representation directly: a lone
      piece is always kacha (it's a `PieceTuple` of size 1), and a group is
      paku for as long as it's represented as one merged `PieceTuple` of
      size ≥ 2 rather than several separate size-1 tuples sharing a square.
      Confirms `Piece` can safely collapse into tuple counts — no individual
      per-piece identity needed to represent kacha/paku status.
- [x] Do killed pieces return as singles or as the tuple they were? —
      **Resolved: singles** (decided 2026-08-18). Intentionally left implicit
      in `Rules.tex` (human-facing doc) — but the implementation must apply
      it explicitly. See build sequence Phase 1 (move enumerator): kill
      resolution must split a killed tuple into `size` individual 1-tuples
      at the owner's starting square, not preserve it as an intact tuple.

(Value-network output shape dropped for now — it's a later-stage question,
resurfaces at build-sequence Phase 4, state encoding.)

## Build sequence

Grouped by dependency phase, not a strict task order within a phase (adapted
2026-08-18). The key insight driving the grouping: the immutable value-object
refactor and `Projector` are motivated specifically by tree search needing to
generate and discard many hypothetical branch states cheaply and safely —
plain random play and heuristic play never branch, so neither needs it. That
pushes the refactor to a single later gate instead of upfront.

- [x] **Resolve kacha/paku** — per-tuple, not per-piece; no dedicated state
      field needed (see open questions)

**Phase 1 — random play** (current mutable OO model; no refactor needed)
- [ ] Move enumerator — given a turn's banked throw values (Rules 2/3/6
      chaining: bonus throws from 6s/12s and from kills) and the current
      board, produce the full set of legal (value → piece/tuple)
      assignments, not just single-value reachability. Includes capture
      resolution (Rules 11–15) and divide-rule filtering (Rule 9). Kill
      resolution must explicitly split a killed tuple into `size` singles
      at the owner's starting square (resolved open question above) — don't
      let it silently fall out as "return the tuple intact."
- [ ] Single-step apply — `apply(state, move) -> next_state`, one move, no
      recursion or branch management. Mutation on the current model is fine
      here; this is not `Projector`.
- [ ] Game loop (`src/game.py`) — initiate, turn cycle (whose turn, throw,
      enumerate, apply, kill/bonus-throw chaining, completion check), win
      condition.
- [ ] Trivial placeholder strategy (random, or first-legal-choice) — just
      enough decision-making to drive the loop through a full game; not the
      real strategy hierarchy.

**Phase 1 (parallel) — visualiser**
- [ ] Visualiser — build alongside Phase 1 so random games can be watched
      and sanity-checked as the loop is developed, not only after.
      **Approach locked in (2026-08-18): CSS 3D-tilt / pseudo-isometric
      board** — plain SVG/HTML/CSS, no 3D engine. A `perspective` +
      `rotateX` transform tilts the board into an angled tabletop view, with
      `box-shadow` layering to fake piece height and tuple stacking; motion
      via CSS transitions. Reuses the visual style already established by
      the ~25 hand-done SVG figures in `docs/Rules/figures/`, stays
      blog-embeddable, and needs no new toolchain. True 3D (Three.js/WebGL)
      stayed off the table for now — real scope-inflation risk for a v1 —
      but is an explicit stretch goal once the game loop and this version
      are proven out.

**Phase 2 — heuristic strategy** (still no refactor needed)
- [ ] `HeuristicStrategy` (`src/strategy.py`) — domain knowledge made
      explicit (e.g. prefer kills, avoid exposure). Plugs into the same
      enumerator output as the placeholder strategy; still no search, still
      fine on the current mutable model.

**Gate — assess before search-based agents**
- [ ] Assess whether the mutable → immutable refactor is actually needed
      before starting expectimax. Expected answer: yes, for the branching
      reason above — but decide this with real move-enumerator/game-loop
      code in hand rather than upfront.

**Phase 3 — search-based agents**
- [ ] Domain model refactor — `Piece`/`PieceTuple`/`Player` (currently
      mutable OO classes; `Piece.owner` holds a live `Player`, not a
      `seat_id`) → immutable value-object model: `PieceTuple` as a frozen
      `(owner: seat_id, position: Square, size: int)`, board as the real
      state unit, piece IDs excluded from state equality/move generation.
- [ ] `Projector` — the recursive move-application system that lets
      expectimax explore many hypothetical future states per decision,
      built on the immutable model's cheap structural sharing.
- [ ] Expectimax agent using `Projector` — one ply of own moves plus
      chance-node weighting by kaudi bias, backed by a learned
      seat-conditioned value function.

**Phase 4 — learning**
- [ ] State encoding — state object → fixed numeric vector for NN input
      (feeds the value function expectimax queries).
- [ ] Self-play training — Colab (T4-class GPU); measure CPU speed first,
      batch to make the GPU worthwhile.

## AI architecture (planned)

Shallow **expectimax**: one ply of own moves plus chance-node weighting by
kaudi bias, backed by a learned seat-conditioned value function.

## Success metrics (what "done" looks like)

Not just "beat available humans":
- Agent-vs-heuristic win rate
- Unprompted emergence of anti-leader behaviour
- Self-play convergence curves
- Value-function calibration

## Repo access note

Prefer direct `git clone` over GitHub web URLs — robots.txt blocks `/tree/`
paths.
