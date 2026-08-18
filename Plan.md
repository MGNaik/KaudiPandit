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

**Broken:**
- `src/board.py`, `src/players.py`, and every file in `tests/` import from
  `docs.Rules.src.*`, which doesn't exist. Should be `src.*`. Nothing
  imports, `pytest` fails at collection for all four test files.

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
`seat_id`. The refactor toward the value-object model above is tracked as
build sequence step 3 below.

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

- [ ] Fix the `docs.Rules.src.*` → `src.*` import paths (`src/board.py`,
      `src/players.py`, all of `tests/`) so the existing test suite runs
      again. Nothing below is meaningfully gradeable until this is fixed.

## Open design questions

- [ ] **Kacha/paku (ripeness): per-piece or per-tuple?** Determines whether
      `Piece` survives as a class or collapses into tuple counts. Resolve
      before building the move enumerator. Needs more thinking (2026-08-18).
- [x] Do killed pieces return as singles or as the tuple they were? —
      **Resolved: singles** (decided 2026-08-18). Intentionally left implicit
      in `Rules.tex` (human-facing doc) — but the implementation must apply
      it explicitly. See build sequence step 2/3: kill resolution must split
      a killed tuple into `size` individual 1-tuples at the owner's starting
      square, not preserve it as an intact tuple.

(Value-network output shape dropped for now — it's a later-stage question,
resurfaces at build-sequence step 8, state encoding.)

## Build sequence

- [ ] **1. Resolve kacha/paku** — per-piece vs per-tuple (see open questions)
- [ ] **2. Move enumerator** — possible-moves → legal-action assembly →
      captures. Kill resolution must explicitly split a killed tuple into
      `size` singles at the owner's starting square (decided open question
      above) — don't let it silently fall out as "return the tuple intact."
- [ ] **3. Domain model refactor** — `Piece`/`PieceTuple`/`Player` currently
      mutable OO classes with object references (`Piece.owner` holds a live
      `Player`, not a `seat_id`). Target is the immutable value-object model:
      `PieceTuple` as a frozen `(owner: seat_id, position: Square, size: int)`,
      board as the real state unit, piece IDs excluded from state
      equality/move generation. Do this alongside step 2, since the
      enumerator's shape depends on it.
- [ ] **4. `Projector` → game loop** — `src/game.py`
- [ ] **5. Strategy hierarchy → headless play** — `src/strategy.py`
- [ ] **6. Visualiser** — HTML/SVG, blog-embeddable
- [ ] **7. `HeuristicStrategy`** — domain knowledge made explicit; benchmark
      for learned agents
- [ ] **8. State encoding** — state object → fixed numeric vector for NN
      input
- [ ] **9. Self-play training** — Colab (T4-class GPU); measure CPU speed
      first, batch to make the GPU worthwhile

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
