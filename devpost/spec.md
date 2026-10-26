---
doc: spec
status: approved
---

# Perceptron — Technical Spec

Concise blueprint. Every PRD behavior has a home below; `5-build` may cite any heading by name.

## How This Works, In Plain Language

Two programs, one link between them.

- **Vue (the front end)** is the part running *in the student's browser*. It draws every screen — welcome, placement, practice, break — and reacts to taps. It does not own any answers or rewards; it only *asks*.
- **Flask (the back end)** is a small Python program running on your machine. It owns the question bank, the correct answers, the hint progression, the honey rules, and one SQLite file where each device's progress lives.
- **How they talk:** every time Vue needs something — a question, a verdict, the honey balance — it sends a **JSON request** with `fetch('/api/...')` and Flask sends back a **JSON response**. That's the whole connection: HTTP calls to a URL, data in, data out. The correct answer is only ever known on the Flask side until the student submits.
- **In development** there are two processes: Vite serves the Vue app on `:5173` (with hot reload), Flask serves the API on `:5000`. Vite's proxy forwards anything starting `/api/` to Flask, so frontend code never sees ports or CORS.
- **For the demo**, Vite builds the Vue app into static files (`frontend/dist`), and Flask serves both those files and the API from one process on one port. The camera points at one URL.

Why this shape: it's exactly the stack you've used, satisfies the PRD's "Flask is the authority" rules, and nothing more — no extra services, no accounts, no libraries beyond Vue, Vite, and Flask.

## The Core Journey Through the System

PRD ref: `prd.md > The Core Journey`.

1. Student opens the app → browser reads its `device_id` from localStorage → `POST /api/session` → server replies with existing progress (or `isNew: true`) → Vue shows Welcome or "Welcome back" + Continue. Refreshing mid-placement resumes the placement check at the next unanswered question with earlier outcomes intact.
2. New student taps Start → `GET /api/placement/questions` (6 questions, fixed order 2/2/2, no correct answers) → each tap on Check is `POST /api/placement/answer` (skip = `null` selection) → server grades and remembers → after the 6th, server applies the placement rule and returns `placedLevel` → "You're starting at Level 2."
3. Practice screen → `GET /api/practice/question` → server picks a not-yet-seen question at that level (recycling when all 8 seen) → Vue renders card + Read aloud (browser speech, server uninvolved) → tap Check → `POST /api/check` → wrong: lavender + next hint step (server advances it); right: soft green + server-awarded honey (5 first try / 3 after hint / 0 revealed, capped at 50/day) → Next repeats from `GET /api/practice/question`.
4. Hint tap without a wrong try → `POST /api/hint` → next step. After 3 steps and a further wrong check → server reveals answer + explanation, awards 0.
5. Take a break / dyslexia toggle → two pure-frontend moments (overlay; CSS variables) except the dyslexia preference which is also `POST /api/preferences` so it survives refresh.
6. Refresh at any point → `POST /api/session` → honey, today's count + date, level, dyslexia setting all come back from SQLite.

## Stack

| Piece | Choice | Rationale / tradeoff |
|---|---|---|
| Frontend framework | **Vue 3** (Composition API) + **Vite** | requested and previously used; Vite build doubles as Flask's static asset source |
| API & serving | **Flask** | requested; serves API and (in demo) the built frontend |
| Persistence | **SQLite** via Python's built-in `sqlite3` | zero infra, satisfies PRD persistence list |
| Styling | hand-written CSS with custom properties (no CSS framework) | exact palette + neubrutalist tokens are simple; dyslexia mode = variable swap |
| State | plain reactive module + composables (no Pinia, no Vue Router) | four screens is too few to justify a router; minimal moving parts |
| Speech | browser **Web Speech API** (`speechSynthesis`) | client-only; no server or keys |

Unverified: current major versions will be pinned at build start (`npm`/`pip` installs), per docs: [Vue](https://vuejs.org/guide/introduction.html), [Vite](https://vite.dev/guide/), [Flask](https://flask.palletsprojects.com/), [Web Speech API](https://developer.mozilla.org/en-US/docs/Web/API/SpeechSynthesis).

**Code conventions (learner-set):** Prettier-formatted frontend; **no code comments** anywhere; small Vue components; Flask split into clear routes vs data/config logic.

## Where It Runs and How Someone Tries It

- Prereqs: Python 3 (+ `pip install -r backend/requirements.txt`), Node.js (+ `npm install` in `frontend/`).
- Dev: terminal 1 `flask run` (or `python app.py`) → API on `:5000`; terminal 2 `npm run dev` in `frontend/` → open **http://localhost:5173** and use the app.
- Demo recording: `npm run build` in `frontend/`, then run Flask alone → open **http://localhost:5000** (one process, static frontend + API). Demo mode: start Flask with `PERCEPTRON_DEMO=1` so the daily cap is 15.
- Submission needs a short demo video and a public GitHub repository. **Deployment is optional** (scope: stretch goal); local recording satisfies the requirement. No API keys or paid services exist.

## Look and Feel

Carried from `prd.md > Look and Feel` verbatim (exact 8-colour palette, Arial 18px default / Open Sans dyslexia mode, thick black outlines + offset shadows, lavender-for-wrong, no red crosses). Implementation form: CSS custom properties in one `base.css`; dyslexia mode flips a `data-dyslexia` attribute on `<html>` which swaps font, spacing, size and sets a motion preference honored by every animation.

## Components

### `NavBar.vue`
Floating rounded navbar: logo, honey counter (live state), dyslexia panel button — visible on every screen. PRD ref: `prd.md > Screens and Layout`.

### `WelcomeScreen.vue`
First-visit welcome + returning-student variant ("Welcome back" / Continue / Start over). Start over calls `POST /api/reset`. PRD refs: `prd.md > The Core Journey` (steps 1, 7), `prd.md > States and Boundaries`.

### `PlacementScreen.vue`
Renders one placement question at a time, progress label "Question n of 6", Skip button (submits `null`), four answer cards, Check answer announces result/level at the end. PRD ref: `prd.md > Placement Check`.

### `PracticeScreen.vue`
The core loop screen: question text + Read aloud button, answer card set, Check, Hint, Take a break. Owns hint-stack display, correct/lavender/revealed card states, Next. Talks to API (`api.js`) and `useSpeech`. PRD ref: `prd.md > Practice and Answering`, `prd.md > Hints and Never Stuck`.

### `AnswerCard.vue`
One multiple-choice option: tap to select, clear selected + focus states, keyboard operable. PRD ref: `prd.md > Practice and Answering`.

### `HintStack.vue`
Shows the hint steps reached so far (nudge → first step → worked example → reveal block with explanation). Pure display; progress is server-owned. PRD ref: `prd.md > Hints and Never Stuck`.

### `DyslexiaPanel.vue`
Panel opening from the navbar button: one switch, clearly on/off; applies immediately app-wide and posts persistence. PRD ref: `prd.md > Dyslexia Panel`.

### `BreakOverlay.vue`
Full-screen soft blue breathing card, no timer, Keep going returns to the exact question. Honors motion preference. PRD ref: `prd.md > Take a Break`.

### `useSpeech` (composable)
All read-aloud logic, isolated from components. PRD ref: `prd.md > Read Aloud`.

### `api.js` / `store.js`
`api.js`: every `fetch('/api/...')` call in one module. `store.js`: reactive app state (screen, honey, level, dyslexia, loading) + actions calling api.js. State updates hand-rolled, no library.

## Speech-Highlighting Strategy

Implements `prd.md > Read Aloud` and `prd.md > Hints` fallback wording.

1. **Primary — deterministic per-word speech (revised at the Slice-3 checkpoint):** each word is spoken as its own short utterance; the word's highlight is set *synchronously before* it is spoken and cleared on utterance end. This works identically in every browser with no event-format assumptions. Tradeoff (accepted in the original decision): slightly robotic pacing between words.
2. **Why the flip:** the spec's own pre-flight rule said verify `onboundary` in the recording browser first and fall back if it fails. Learner evidence at the checkpoint: highlighting failed in both Chrome and Firefox. Evidence over preference — sequential became primary.
3. **Deferred option:** boundary-event highlighting (natural pacing) can return later if a target browser proves reliable; it stays a measured optimization, not a dependency.
4. **Rules:** question text only; highlight clears when speech ends; replay = tap again; tap during speech stops it; speech stops automatically on Check/Next; if `speechSynthesis` is unavailable or the first word fails to utter — friendly message, question fully usable, nothing else blocked.
5. Purely client-side; no browser-specific behavior affects grading or practice.

## API Contracts

All JSON. Frontend always sends its `deviceId` (random UUID kept in localStorage). The student's local date `YYYY-MM-DD` is sent with session calls so the **daily cap uses the student's own midnight** (PRD ref: `prd.md > Honey Economy`). Correct answers never leave the server before submission.

| Endpoint | Request body | Response |
|---|---|---|
| `POST /api/session` | `{deviceId, today, tzOffset}` | `{isNew, totalHoney, honeyToday, level, dyslexia, placement:[{questionId, order, outcome}]}` — `placement` only while the check is unfinished |
| `GET /api/placement/questions` `?deviceId=` | — | `{questions:[{id, level, text, options, order}]}` ×6, no correct answers |
| `POST /api/placement/answer` | `{deviceId, questionId, selected}` (selected=null = skip) | `{done, placedLevel?}` — outcome stored (`correct`/`wrong`/`skipped`, skipped ≠ wrong); level computed on the 6th; re-submitting the same question returns its stored outcome idempotently |
| `GET /api/practice/question` `?deviceId=` | — | `{id, level, text, options, hintStep}` — server picks unseen/recycled, resets attempt tracking |
| `POST /api/hint` | `{deviceId, questionId}` | `{hintStep, hint:{kind, text}}` (1..3; step 4 = reveal block) |
| `POST /api/check` | `{deviceId, questionId, selected}` | wrong: `{correct:false, hintStep, hint:{kind, text}}` (the newly revealed step, per `Revisions`) · right: `{correct:true, honeyAdded:5\|3\|0, honeyToday, totalHoney, capped}` · after 3 hint steps & wrong again: `{correct:false, revealed:true, correctOption, explanation, honeyAdded:0}` · **idempotent:** a repeat check on the same question returns the stored outcome with `duplicate:true, honeyAdded:0` — honey is never awarded twice |
| `POST /api/preferences` | `{deviceId, dyslexia}` | `{dyslexia}` |
| `POST /api/reset` | `{deviceId}` | `{isNew:true}` — clears all state for the device |

Server-side rules (PRD ref: `prd.md > Honey Economy`, `prd.md > Hints`): rewards 5/3/0 enforced here; cap 50/day (or 15 with `PERCEPTRON_DEMO=1`) enforced here — under cap, a correct answer that would exceed it is simply not paid (`capped:true`); wrong answers never remove honey; hint step auto-advances on each wrong check.

**Daily-cap date validation (learner correction #1).** The client-supplied `today` is never trusted blindly. The server accepts a claimed new day as a cap reset only when it is within the legitimate set `{serverUTCdate−1, serverUTCdate, serverUTCdate+1}` — the dates any real UTC offset (−14…+12 h) could produce at that moment. A backwards date, or a date outside that set, is ignored: the stored day and `honey_today` stand, so the cap cannot be reset by changing the date in a request. Accepted tradeoff: a faked clock inside the legitimate window can shift the cap boundary by at most a day — cosmetic, since honey cannot double-count within a stored day.

**Idempotent rewards (learner correction #2).** Grading is keyed to the attempt record, not the request: once an attempt is `solved` or `revealed`, further `POST /api/check` calls for that question return the stored outcome and never touch honey again — regardless of retries, double taps, or network re-sends.

**Consistent error responses (learner correction #4).** Every failing endpoint returns one envelope, `{error:{code, description}}`, with an accurate HTTP status — `bad_request`, `invalid_selection`, `unknown_question`, `unknown_device`, `server_error` — and never a stack trace or internal detail. Failed requests change no state: progress is written only after validation succeeds. `unknown_device` tells the client to re-session. `api.js` maps each code to one friendly message (see `Important Failure Modes`); duplicate submissions are not errors but the idempotent path above.

## Data Model

**SQLite** (`backend/perceptron.db`, auto-created on first run):

```
students            progress + preferences, one row per device
├─ device_id   TEXT PRIMARY KEY
├─ total_honey INTEGER
├─ today_date  TEXT  ('YYYY-MM-DD', client-local date)
├─ honey_today INTEGER
├─ level       INTEGER          (placed level; NULL until placement done)
└─ dyslexia    INTEGER          (0/1)

placement_answers    outcome of each placement question per device
├─ device_id   TEXT
├─ question_id TEXT
├─ order       INTEGER          (1..6, fixed sequence)
└─ outcome     TEXT             ('correct' | 'wrong' | 'skipped' — skipped ≠ wrong)
→ placed level = highest level with ≥1 'correct' among its two; none = Level 1
→ placement progress = rows present; refresh resumes at the first unanswered index

seen_questions      question-cycle memory (recycling rule)
├─ device_id  TEXT
├─ level      INTEGER
└─ question_id TEXT

attempts            state of one practice question being worked on
├─ device_id   TEXT
├─ question_id TEXT
├─ tries       INTEGER
├─ hint_step   INTEGER          (0..3; ≥4 means revealed)
└─ status      TEXT             ('open','solved','revealed')
```

**Question bank** (`backend/data/fractions.json`, hand-authored, no generation): `placement` = 6 questions (2 per level, fixed order); `levels` = 3 × 8 questions. Each question: `{id, level, text, options[4], correct, hints[3], explanation}`. `correct`, `hints`, `explanation` are never included in API responses that precede submission. Hint wording per `prd.md > Open Questions`: short, encouraging, one idea per sentence.

Leave-and-return behavior: everything in `students`/`placement_wins`/`seen_questions` persists across refresh; the *current question* does not — a returning student gets a fresh question at their level (`prd.md > States and Boundaries`).

## File Structure

```
Perceptron/
├── backend/
│   ├── app.py               # Flask app: routes, serves frontend/dist in demo mode
│   ├── questions.py         # loads fractions.json; grading, hint & cycle logic
│   ├── state.py             # sqlite access: students, placement_wins, seen, attempts
│   ├── config.py            # caps (50 / 15 via PERCEPTRON_DEMO), rewards, reads env
│   ├── data/
│   │   └── fractions.json   # 6 placement + 3×8 practice questions, hints, explanations
│   └── requirements.txt     # Flask only
├── frontend/
│   ├── index.html
│   ├── vite.config.js       # dev proxy: /api/* → :5000
│   ├── package.json
│   └── src/
│       ├── main.js          # mount, global styles, dyslexia attribute handling
│       ├── App.vue          # screen switching (welcome/placement/practice + overlays)
│       ├── api.js           # all fetch('/api/...') calls
│       ├── store.js         # reactive state + actions
│       ├── speech.js        # useSpeech composable (boundary events + fallback)
│       ├── styles/base.css  # palette tokens, neubrutalist shapes, dyslexia variables,
│       │                    # reduced-motion rules
│       └── components/      # NavBar, WelcomeScreen, PlacementScreen, PracticeScreen,
│                             AnswerCard, HintStack, DyslexiaPanel, BreakOverlay
├── devpost/                 # learning workspace (scope.md, prd.md, spec.md, …)
└── .gitignore
```

## External Services and Dependencies

None beyond the stack above: no external APIs, no database service, no hosting, no keys, no accounts, no paid plans. All data is local (SQLite file + JSON bank). Speech synthesis is the browser's own.

## Important Failure Modes

- **Speech unavailable or fails to start** → friendly "read-aloud is unavailable in this browser" message; question fully usable; highlighting works whenever speech works. (Implements `prd.md > Read Aloud` fallback.)
- **API call fails / Flask down** → inline plain-language message on the affected screen with a Retry button; the app never shows a raw error or silently swallows the failure. (PRD: "handle loading states and errors clearly.")
- **JSON bank entry malformed / missing** → server skips the bad item rather than breaking the level; a startup sanity check counts 6 + 8×8 questions and reports the count in the terminal.
- **Unknown device / cleared storage** → treated as brand-new (`isNew:true`); nothing crashes, stated behavior per `prd.md > Honey Economy` identity rule.

## What Was Simplified and Why

- **Plain reactive state instead of Pinia/Vue Router** — four screens and one state module; the fuller version adds a router and a store library for no product gain in the PoC. (Derives from "keep Vue components small" + no unnecessary libraries.)
- **SQLite instead of a hosted database** — same shape of data, zero infrastructure.
- **Device-token identity instead of accounts** — exactly the PRD's stated identity model; signup was cut in scope.
- **`PERCEPTRON_DEMO=1` env flag instead of a UI panel** — no accidentally discoverable hidden settings; cap swap is one line of config.
- **Static JSON question bank instead of a DB table for questions** — questions are content, not student data; hand-authored, version-controlled.
- **All placement/practice questions are real content** — the kernel is never faked; the 24+6 questions must be genuinely written with real three-step hints.

## Decisions and Open Issues

**Learner-agreed decisions (from the 4-spec exchange):**
1. **Server-side persistence** (Flask + SQLite, browser-side `device_id`) instead of localStorage-only — chosen to exercise the Vue↔Flask boundary and make the demo show real round-trips. Tradeoff accepted: slightly more moving parts.
2. **Flask as the grading authority** — questions served without answers, `POST /api/check` grades, honey + cap server-enforced; the client genuinely cannot peek.
3. **Demo mode via environment variable** (`PERCEPTRON_DEMO=1`, cap 15) — no user-facing toggle.
4. **Read aloud = deterministic per-word utterances as primary** (revised at the Slice-3 checkpoint after boundary events failed in both the learner's Chrome and Firefox; documented fallback became primary, per the recorded verification-first rule). The app does not depend on one browser for basic maths practice.
5. **Dev = Vite :5173 + Flask :5000 with `/api` proxy; demo = one Flask process serving built static files.** `fetch('/api/...')` everywhere; JSON in/out; no extra libs.
6. **Server-side integrity (four learner corrections at spec review):** cap-reset dates are validated against the server clock; honey rewards are idempotent per question; placement progress is persisted per question with skipped ≠ wrong and refresh-resume; all API errors share one `{error:{code, description}}` envelope that never leaks internals and never mutates progress.
7. **Conventions (learner-set):** Prettier, no code comments, small components, clean Flask separation; corrections preserve the architecture, scope, and no-new-deps stance.

**Derived implementation details (agent conclusions from the above — flag at review if wrong):**
- No Pinia, no Vue Router; screen switching in `App.vue`.
- Daily reset compares the client-sent local date against the stored `today_date`.
- Hint step auto-advances on wrong checks (PRD behavior), `POST /api/hint` only for tap-without-wrong-try.

**Agreed small investigation — resolved:** whether `onboundary` fires reliably with usable `charIndex` in the recording browser. Evidence: it did not (learner report, Chrome + Firefox, Slice-3 checkpoint). Outcome: deterministic sequential per-word speech became primary; see `Speech-Highlighting Strategy`.
