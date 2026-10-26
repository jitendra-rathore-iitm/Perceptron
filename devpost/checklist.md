---
doc: checklist
status: approved
---

# Build Checklist

Build mode: learn (learner asked for step-by-step building with verification and Vue–Flask explanations as we go)

## Slices

- [x] **1. Ask and answer one fraction question, end to end**
  Becomes usable: The app runs from two processes; one fraction question displays as four answer cards; tapping an option and Check answer gets a graded verdict from Flask; the navbar honey counter updates on a correct answer (in memory only, for now).
  Why now: Proves the whole Vue→fetch→Flask→JSON→Vue path on slice one, with project bootstrapping folded in. The kernel can't sit anywhere until this spine exists.
  PRD ref: `prd.md > The Core Journey` (steps 1, 4), `prd.md > Practice and Answering`
  Spec ref: `spec.md > How This Works, In Plain Language`, `spec.md > API Contracts`, `spec.md > File Structure`
  Build: Scaffold both processes exactly per the spec tree — Flask app with `GET /api/practice/question` + `POST /api/check` (the 5/3/0 reward rules live server-side even now; honey rewards are already idempotent per question via in-memory attempt tracking, replaced by SQLite in Slice 4), `fractions.json` seeded with fully-authored Level 1 questions, Vue app with `styles/base.css` tokens (full palette, neubrutalist shapes), `NavBar` with honey counter, `PracticeScreen` + `AnswerCard` with selection state. Creates: `api.js`, `store.js`, first components. Levels, hints, and persistence deliberately later — smallest complete Vue → fetch → Flask → JSON → Vue interaction only.
  Verify (mechanical): `npm install` + `pip install -r requirements.txt` succeed; both dev servers start clean; `curl` shows `GET /api/practice/question` returns options but no correct answer, and `POST /api/check` grades a known right/wrong selection correctly, with a repeated check of the same question awarding honey only once.
  Learner check: Open localhost:5173, answer a question right and one wrong, and watch the honey counter and card colours.
  Commit: `Slice 1: practice loop asks and grades, honey counter live`

- [x] **2. Read aloud with word-by-word highlighting (the kernel)**
  Becomes usable: Tapping Read aloud speaks the question text while the currently-spoken word highlights; the highlight clears when speech ends; replay, stop-mid-speech, and stop-on-submit all behave per the PRD.
  Why now: The unique kernel, one slice after the first usable loop. Its known uncertainty (boundary events) should surface as early as possible.
  PRD ref: `prd.md > Read Aloud`
  Spec ref: `spec.md > Speech-Highlighting Strategy`
  Build: `speech.js` composable — word/offset map, primary `onboundary` path, pre-flight check, sequential per-word fallback, stop/clear/replay rules; wire the Read aloud button beside the question text.
  Verify (mechanical): run the pre-flight: confirm boundary events fire in the recording browser; confirm stop-on-Check via a scripted speech session followed by a check submission.
  Learner check: Tap Read aloud and watch the word trail the voice; tap mid-speech to stop; replay; and submit while speaking to see speech stop.
  Commit: `Slice 2: read aloud with word highlighting (kernel)`

- [x] **3. Gentle hints: the student is never stuck**
  Becomes usable: A wrong answer turns the card lavender, reveals the next hint step, and retries are free; Hint can be tapped to see steps without a wrong try; after all three steps and a further wrong check, the app reveals the answer + explanation and grants 0 honey. Nothing is ever taken away.
  Why now: Completes the practice loop's emotional heart — kernel + kindness — which makes the whole product tryable end to end before infrastructure work.
  PRD ref: `prd.md > Hints and Never Stuck`, `prd.md > Practice and Answering`
  Spec ref: `spec.md > API Contracts` (`POST /api/hint`, check responses), `spec.md > Components > HintStack.vue`
  Build: Server-side attempt tracking (`tries`, `hint_step`, `status` transition to `revealed`), hint auto-advance on wrong checks, idempotent per-question reward memo; `HintStack.vue` display; lavender/non-red styling; celebration on correct + Next.
  Verify (mechanical): scripted `curl` walk: one question wrong ×3, tap-hint twice, wrong again → reveal response with `honeyAdded:0`; double-check the same question → `duplicate:true` with no honey change.
  Learner check: Deliberately fail a question and read each step; try to be still-wrong after step 3; confirm honey never decreases and no red appears anywhere.
  Commit: `Slice 3: three-step hints, reveal, never stuck`

- [x] **4. Everything survives a refresh**
  Becomes usable: Honey, today's count, level, and the dyslexia preference come back after a reload via `POST /api/session` with a persistent `device_id`; daily cap 50/day with validated dates; `PERCEPTRON_DEMO=1` drops the cap to 15.
  Why now: Persistence is where the data model can be wrong, and the four integrity corrections land here where they're cheapest.
  PRD ref: `prd.md > States and Boundaries`, `prd.md > Honey Economy`
  Spec ref: `spec.md > Data Model`, `spec.md > API Contracts` (session, date validation, idempotent rewards, error envelope)
  Build: `state.py` SQLite layer with all four spec tables — `students`, `attempts`, `seen_questions`, and `placement_answers` (created now per the approved data model, used by Slice 5) — plus `config.py` cap/reward constants, session endpoint with device bootstrap, client-date validation against the server clock, `store.js` persistent `device_id` in localStorage, error envelope + `api.js` friendly messages, `PERCEPTRON_DEMO` env handling. In-memory attempt tracking from Slice 1 is replaced by the persistent `attempts` table.
  Verify (mechanical): earn honey → restart Flask → session call returns all values; replay a check → duplicate, no double-award; request with a forged backwards date → ignored; bad selection/unknown question/unknown device → the exact envelope, no state change.
  Learner check: Answer a question, refresh the page, and see your honey still there; then (in demo mode, if started so) hit the cap and read "Done for today."
  Commit: `Slice 4: persistent state, capped honey, validated dates, error envelope`

- [x] **5. The placement check**
  Becomes usable: New devices run six skippable questions (2/2/2, fixed order), progress label reads "Question n of 6," the result is the highest level with ≥1 correct, skips are never wrong, refresh mid-placement resumes exactly, and Start over clears everything.
  Why now: Levels gate every remaining behavior; placement is the adaptive spine of the demo's first minute. Builds directly on the `placement_answers` table created in Slice 4 — no new data model.
  PRD ref: `prd.md > Placement Check`, `prd.md > The Core Journey` (steps 2-3, 7)
  Spec ref: `spec.md > API Contracts` (placement rows), `spec.md > Data Model` (`placement_answers`)
  Build: placement endpoints with per-outcome persistence, resume logic, authoring of the six placement questions (2 per level, needed to test), placement UI (`PlacementScreen` with Skip), result moment "You're starting at Level n," start-over flow.
  Verify (mechanical): scripted curl placements: all-skip → Level 1; one correct in L2 only → Level 2; resumable mid-check after a simulated restart; re-skip returns stored outcome.
  Learner check: Take the placement check fresh, skip strategically, and read your result; refresh mid-check and confirm you land where you left off.
  Commit: `Slice 5: placement check with resume and result`

- [x] **6. Full question banks: 24 + 6, genuinely written**
  Becomes usable: All 3 levels have 8 real practice questions each, every question carries its three authored hint steps and explanation, the bank recycles shuffled without empty screens, and the startup count check prints 6 + 24.
  Why now: The demo says "one subject done well" — content quality is the product, and authoring as its own slice keeps it honest rather than skimmed mid-slice.
  PRD ref: `prd.md > Question Banks`, `prd.md > Open Questions` (hint wording direction)
  Spec ref: `spec.md > Data Model`, `spec.md > Important Failure Modes` (malformed entry skip, startup check)
  Build: Author the remaining 16 practice questions — 8 each for L2 (equivalent fractions, same-denominator add/subtract) and L3 (different denominators, multiplication) — each with nudge/first-step/worked-example hints and a short explanation (L1 + placement already exist); shuffle-recycle shim; malformed-entry skip.
  Verify (mechanical): startup sanity pass; scripted walk of every question id through grading paths; recycling: 9 consecutive fetches at one level, all unique, no repeats.
  Learner check: Play through a few questions at each level and grade their clarity, hint quality, and tooth-fairness as a student would.
  Commit: `Slice 6: complete authored question banks`

- [x] **7. Dyslexia panel + breathing break**
  Becomes usable: One tap in the panel flips font/spacing/size/motion app-wide immediately (and it survives refresh); the break overlay shows the still, calm breathing card with Keep going back to the exact question; reduced motion removes all animation.
  Why now: Both are always-available accessibility surfaces named in the kernel; with backends done, this polish is safe.
  PRD ref: `prd.md > Dyslexia Panel`, `prd.md > Take a Break`
  Spec ref: `spec.md > Components > DyslexiaPanel.vue / BreakOverlay.vue`, `spec.md > Look and Feel`
  Build: `DyslexiaPanel.vue` + `data-dyslexia` attribute + `POST /api/preferences` persistence; `BreakOverlay.vue` + state pause/resume; OS `prefers-reduced-motion` respect; decorative-floating-elements behavior.
  Verify (mechanical): computed-style assertions toggled via DOM: font family, letter-spacing, line-height, size change with the panel; regex sweep confirming no persistent animation runs in reduced mode.
  Learner check: Toggle the panel and feel the whole app change; open the break screen while mid-question, keep something honeyed going on, and return to the exact same question.
  Commit: `Slice 7: dyslexia panel and breathing break`

- [x] **8. Demo build: one process, camera-ready**
  Becomes usable: `npm run build` outputs `frontend/dist`; Flask serves the built app + API from one process on :5000; error envelope polish is consistent everywhere; the whole 60-second demo script runs start to finish.
  Why now: This converts dev-mode scaffolding into the recorded demo path and sweeps the acceptance criteria before final review.
  PRD ref: `prd.md > What "Working" Looks Like`, `prd.md > Acceptance criteria`
  Spec ref: `spec.md > Where It Runs and How Someone Tries It`, `spec.md > Important Failure Modes`
  Build: Vite build wiring, Flask static serving of `dist`, speech-unavailable friendly message, retry-on-API-failure paths, mobile/responsive pass, keyboard/-focus states, final acceptance-sweep fixes.
  Verify (mechanical): build succeeds; one-process serve returns the app on :5000; scripted acceptance sweep of the 11 criteria (with `PERCEPTRON_DEMO=1`); keyboard-only placement + practice walk with visible focus.
  Learner check: Start the single-process demo yourself, run your 60-second script out loud once, and tell me where it drags.
  Commit: `Slice 8: demo-ready single-process build`

## Hands-on Checkpoints

- [x] Early usable behavior explored — after Slice 3: try the full practice experience (question, answers, read-aloud, hints, reveal) and give feedback before infrastructure work (Slice 4+) continues. (Evidence: Revisions record the slice-3 checkpoint feedback — NeoFlux visual pass, navbar copy, speech-strategy flip.)
- [ ] Final kick-the-tires exploration and feedback completed — after Slice 8, before revision work. (Agent-side automated acceptance sweep complete — 25/25 against the single-process demo build — but the learner's own eyes-on pass is still owed; fold it into the demo-video recording session.)

## Final Review

- [ ] Final review complete — feedback resolved and learner confirms ready to ship (blocked on the learner: code review and security sweep done agent-side; see final report — learner confirms after their kick-the-tires pass)

## Code Tour and App Map

- [ ] Learning activity complete — guided route, focused alternative, prior practice connected, or brief recap
- [ ] Optional edit and transfer reflection addressed — offered/declined/already covered/not applicable as appropriate
- [x] `devpost/app-map.html` generated from finished code, checked, and shown, including a project-grounded practice to reuse

Activity and evidence: agent-generated app map from the finished code; guided-tour conversation still owed to the learner (learner-profile.md absent from devpost/ — desired-learning-outcome conversation never recorded).
Route and stops: index.html → main.js (data-dyslexia watcher) → App.vue (screens) → store.js (actions) → api.js (fetch) → Flask app.py (routes/validation) → questions.py (grading) → state.py (SQLite); speech.js and the Vue components as the client-side kernel.
Edit outcome: not attempted agent-side — offered to learner at wrap-up.
Reflection: pending learner.
Activity mode: recap map generated; hands-on tour deferred to learner.

## Revisions

- [`POST /api/check` wrong-answer responses now include the newly revealed `hint` object directly] — the original contract returned only `hintStep`, which left the auto-advanced step's text unfetchable without double-advancing via `POST /api/hint`. Preserves the PRD behavior exactly (one shared ladder; wrong tries and Hint taps both advance it).
- [Speech highlighting switched to deterministic per-word utterances as primary] — learner checkpoint evidence: highlight failed in both Chrome and Firefox, which fails the spec's pre-flight rule ("verify boundary events; fall back if not"). The documented fallback became primary; spec's Speech-Highlighting Strategy and decision 4 updated to match.
- [Visual pass guided by NeoFlux reference (inspiration, not copy): lavender-tinted page background with fine black grid pattern, button press-down physics (hover lift / active press), card entrance animation replayed per question, honey-counter bump on reward, distinct button colours (yellow check / sky read-aloud / orange hint)] — learner checkpoint feedback asked for a completed page look with grid background; learner's exact palette and all PRD behavior preserved; `prefers-reduced-motion` gating kept.
- [Navbar copy made self-explanatory ("Honey: N" instead of "N drops"; "Dyslexia" button instead of the cryptic "aA" glyph), logo underline removed, speech rate raised to 1.15] — learner checkpoint feedback; copy clarity matters for the 12–18 audience.
- [Slice 6 question banks pulled forward: 4 more Level 1 questions and the full Level 2 (8) and Level 3 (8) banks authored] — learner wanted more questions now; full hints and explanations included; Slice 6 keeps its shuffle-recycle shim and counting checks.
- [Deployment pulled forward from its stretch-goal slot at the learner's request: Vercel frontend + Render free-tier API, connected by a `vercel.json` rewrite so the frontend's relative `/api` addresses work unchanged in every environment] — verified against vercel.com/docs/rewrites and render.com/docs/free; no plan-level scope change (the stretch goal is simply being used), and the SQLite spin-down reset on Render free tier is recorded in spec.md instead of silently accepted.
- [Slice 6 recycle check adapted: the "9 fetches all unique" test runs on Level 1 (12 questions after the pull-forward); the 8-question levels prove recycling by repeating only after the full pool is seen (8 unique + 1 repeat)] — an 8-question bank cannot yield 9 consecutive unique questions; the shuffle-recycle rule itself is unchanged.
- [Startup count check reports the real bank (6 placement + 28 practice: L1 12, L2 8, L3 8) and warns below 6 + 8-per-level rather than asserting exactly 6 + 24] — the earlier pull-forward added 4 Level 1 questions, so a hard 24 assertion would fail on a healthy bank.
- [Local demo port default changed 10000 → 5000 to match the spec's "open localhost:5000"; Render still binds the PORT env var it injects] — the 10000 default was a Render-ism that leaked into local dev; the env var wins wherever the platform sets one.
- [Read-aloud word-highlight criterion verified via its fallback path in the automated sweep: headless Chrome has no TTS voices, so the sweep asserts the friendly "not available" note appears and the question stays fully usable] — per the spec's fallback rule; the highlight itself was learner-verified at the Slice 2/3 checkpoints and needs one eyes-on pass on real hardware before recording.
