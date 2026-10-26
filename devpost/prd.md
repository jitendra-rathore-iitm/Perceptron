---
doc: prd
status: approved
---

# Perceptron — Product Requirements

One line: Perceptron is a web app where students aged 12–18 with ADHD and dyslexia practise maths one question at a time — read aloud with word-by-word highlighting, gentle hints, rewards that are never taken away.
Source: `scope.md > One line`, `scope.md > The Unique Kernel`.

## The Core Journey

1. **First visit.** A welcome screen: the Perceptron name, one line — "Maths that goes at your pace" — and a big yellow Start button. A floating rounded navbar sits top-centre with the logo, the honey counter, and the dyslexia panel button. No signup. The screen states plainly that honey belongs to the same browser on the same device. (Source: `scope.md > The Core Loop`, scope interview.)
2. **Placement (new student).** Start runs a six-question placement check, two questions per level, one at a time, in order Level 1 → 3. A progress label reads "Question 2 of 6." Every question has a Skip button. Each question is multiple choice: four large answer cards, tap to select, then a separate Check answer button. Selection is never judged before submission.
3. **Placement result.** A result moment says "You're starting at Level 2." No score, no fail message.
4. **Practice, the core loop.** One fraction question at a time in a centred thick-outlined card: question text in large type with a Read aloud button beside it; four answer cards; a Check answer button; a Hint button and a Take a break button at the bottom. Correct → soft green, "Nice work," honey drops fly into the navbar counter, Next appears. Wrong → lavender card (not red), "Not quite. Try again," the next hint step appears, input stays open, nothing is removed.
5. **Always available.** Take a break (calm full-screen blue card), Read aloud (on the question text), and the dyslexia panel (one tap, whole app) work at any point.
6. **Daily close.** At the 50-drop cap: "Done for today. Come back tomorrow." Practice continues; honey simply stops being added.
7. **Returning visit.** A "Welcome back" screen with Continue (goes to a fresh question at their placed level) and Start over (clears everything and reruns placement).

## Screens and Layout

One product, four surfaces, plus one persistent element. No invented screens.

- **Floating navbar (persistent):** rounded, top-centre, ~50% width on desktop, adaptive on mobile without covering content. Contains: Perceptron logo, honey counter, dyslexia panel button.
- **Welcome screen:** also serves returning students ("Welcome back" variant with Continue + Start over).
- **Placement screen:** one question at a time, progress label, Skip button, answer card set, Check answer.
- **Practice screen:** as described in Core Journey step 4.
- **Break overlay:** full-screen soft blue calm card over whatever is underneath.

## Look and Feel

- **Neubrutalist:** thick black outlines, rounded corners, solid backgrounds, bold offset shadows. No excessive gradients, no clutter, no unnecessary decoration.
- **Exact palette** — Black `#000000`, Off-white `#FFFDF5`, Yellow `#FFD23F` (Start, primary accent), Coral pink `#FF6B6B`, Sky blue `#74B9FF`, Soft green `#88D498` (success), Orange `#FFA552`, Lavender `#B8A9FA` (wrong answer / hints).
- **Typography:** plain sans-serif. Arial default, 18px base. Question text large and bold.
- **Dyslexia-friendly mode:** Open Sans, increased letter and line spacing, larger text, reduced motion — applied consistently across the entire app.
- **Animation:** smooth and subtle; every animation serves a purpose (progress, celebration). When motion is reduced, unnecessary movement becomes simple static changes.
- **Non-negotiables:** accessibility and readability before visual effects. Sufficient contrast, clear button labels, visible focus states, keyboard-accessible answer cards, screen-reader support, works on mobile and desktop.
- **Never used:** red crosses, negative scores, countdowns, punishment animations.

## Features and Behavior

### Placement Check
Source: `scope.md > The POC Boundary`.

Three levels:
- **Level 1:** understanding fractions — reading a fraction, comparing simple ones.
- **Level 2:** equivalent fractions; adding/subtracting with the same denominator.
- **Level 3:** adding/subtracting with different denominators; multiplying fractions.

- Six questions, two per level, shown in level order; progress label "Question n of 6"; Skip on every question.
- **Result rule:** the student starts at the highest level where they got at least one of that level's two questions right. Skipped = "not answered," not wrong. Skipping everything → Level 1.
- Result moment states the level with no score or fail framing.

### Practice and Answering
Source: `scope.md > The Core Loop`.

- Multiple choice everywhere in the PoC: four displayed answer cards, one tap to select, thick outlines, palette colours, clearly separated with good spacing; selected option visibly highlighted; a separate **Check answer** button submits.
- Nothing indicates correctness before submission.
- Correct: card turns soft green, "Nice work," honey animation, Next button.
- Incorrect: card turns lavender, "Not quite. Try again.", the next hint step is revealed, selection stays available, retry costs nothing.
- After a correct answer the Next button moves to a fresh question at the student's level.

### Hints and Never Stuck
Source: `scope.md > The Unique Kernel`; hint shape decided in the 2-scope review.

Three hint steps per question, escalating; a new step appears after each wrong try, and tapping Hint reveals the next step without needing a wrong try:
1. **A nudge** — one short sentence pointing at where to look.
2. **First step shown** — the student finishes the rest.
3. **Worked example** — same method, different numbers.

If the student is still wrong after step 3, the app shows the correct answer with a short explanation, then Next. No honey is given for a revealed question — and none taken away. The skill returns later in a fresh question. **The student is never stuck.**

### Read Aloud
Source: `scope.md > The Unique Kernel`.

- Reads the question text only — not inputs or buttons.
- The word currently being spoken is highlighted; the highlight clears when speech ends.
- Replayable (tap again to restart); tapping during speech stops it.
- Stops automatically on submit or Next.
- **Fallback:** if the browser doesn't support speech synthesis, or speech fails to start, the question stays fully usable. A friendly message explains that read-aloud is unavailable in the current browser. Nothing else is blocked; word highlighting applies whenever speech synthesis works.

### Honey Economy
Source: `scope.md > The Core Loop`, scope interview (Exchange 3).

- First-try correct: **5 drops**. Correct after any hint/retry: **3 drops**. Revealed answer: **0**. Harder levels don't pay more — no reward for being placed higher.
- Cap: **50 drops per calendar day**, resetting at midnight in the student's own time zone.
- At the cap: "Done for today. Come back tomorrow." Practice continues; honey stops.
- **Demo mode:** a hidden setting lowers the cap to **15** drops so the cap message shows quickly on video.
- Identity: no signup — honey belongs to the same browser on the same device; clearing data or changing device starts fresh, which the welcome screen says plainly.

### Question Banks
Source: scope interview (Exchange 3).

- 8 fixed questions per level, written for fractions. No generation.
- Random order; no repeats until all 8 in the level are seen, then reshuffled and reused. The student never sees an empty screen.

### Take a Break
Source: scope interview (Exchange 2).

- Pauses the session; opens a calm full-screen soft-blue card: slow breathing circle, "Breathe in. Breathe out." No timer, no countdown.
- Honey and the current question are saved. A single Keep going button returns to the exact question.
- With reduced motion, the circle is static and only the text changes.

### Dyslexia Panel
Source: `scope.md > The Unique Kernel`.

- One toggle switches all four things together: font (→ Open Sans), spacing (↑ letter/line), text size (↑), motion (↓).
- Default is the ordinary mode; dyslexia-friendly mode is always one tap away, and the panel shows clearly whether it's on or off.
- Changes apply immediately across the entire app — cards, buttons, hints, all text.
- The preference persists across refreshes.
- **Motion governs all animations:** honey rewards, page/question transitions, button/card animations, the breathing circle, decorative floating elements. Reduced motion also respects the operating system's own reduced-motion preference where applicable.

## States and Boundaries

- **First use:** placement check follows the welcome screen's Start.
- **Returning visit:** "Welcome back" + Continue (fresh question at placed level) or Start over (clears everything, reruns placement).
- **Selected, not submitted:** answer choice is visible but unjudged until Check answer.
- **Wrong answer:** lavender state + escalating hints, unlimited retries, nothing lost.
- **Revealed answer:** explanation shown, 0 honey, Next; the skill reappears later in a fresh question.
- **Daily cap reached:** "Done for today" message; practice continues without earning.
- **Break active:** session paused underneath; exact state restored on Keep going.
- **Read aloud in progress:** replay/stop behaviour as defined; stops on submit/Next.
- **Persists across refresh:** total honey, today's count + today's date, placed level, dyslexia-panel setting. **Does not persist:** the current question (fresh question at level on return).
- **Device boundary:** honey and progress live in one browser on one device only — stated on the welcome screen.

### Acceptance criteria (from the demo script, `scope.md > What "Working" Looks Like`)

- [ ] A fresh visitor can reach a placed level in under ~2 minutes without any signup.
- [ ] Skipping all six placement questions results in Level 1, with the level announced and no fail framing.
- [ ] The highlighted word follows the actual speech; the highlight clears when speech ends.
- [ ] A wrong answer shows a lavender (never red) card, a hint step, and no honey change on the counter.
- [ ] A correct first-try answer adds 5 drops (visible in the counter); correct-after-hint adds 3.
- [ ] Honey survives a page refresh; today's cap progress survives a refresh too.
- [ ] With the demo cap (15), earning past it shows "Done for today. Come back tomorrow." while questions still work.
- [ ] One tap on the dyslexia panel visibly changes font, spacing, size, and motion at once, app-wide, and survives a refresh.
- [ ] Reduced motion removes the breathing-circle animation, honey fly-in, and transitions.
- [ ] Answer cards are keyboard-operable with visible focus; the layout works on mobile.
- [ ] No red crosses, countdowns, scores, or punishment animations anywhere.

## Product Decisions

- **Multiple choice with a separate Check answer** — gentlest input for this audience; typed answers deferred.
- **Lavender, not red** for wrong answers — the app's emotional signature; nothing is ever punished.
- **Flat 5/3/0 honey, not level-scaled** — no reward for being placed higher.
- **Revealed answer pays 0 but costs nothing** — the skill returns later in a fresh question; never stuck.
- **Skipped placement = not answered** — placement can only place you, never demote or fail you.
- **8-question banks, recycled shuffled** — guarantees no empty screens without generation.
- **Browser/device identity, stated plainly** — no signup; the tradeoff is said out loud on the welcome screen.
- **Single-toggle dyslexia mode, ordinary by default** — one tap, everything together; the switch is visible and reversible.
- **Motion setting governs every animation** — plus OS reduced-motion respect where applicable.
- **Break screen has no timer** — pausing is genuinely calm, not a regulated pause.
- **Demo cap setting (15)** — makes the cap provable on video quickly.

## What We're Building

Everything above within the PoC boundary: welcome (incl. Welcome back), placement, three fraction levels with 24 banked multiple-choice questions and their three-step hints, practice loop with read-aloud word highlighting, honey economy with cap and demo setting, break overlay, single-toggle dyslexia panel with persistence, neubrutalist look, Vue + Flask, running locally. Proof demoable in ~60 seconds.

## Deferred From the POC

- **Typed-answer practice mode** — implied by "answer input"; deferred in favour of multiple choice.
- **Deployment to a public URL** — stretch goal per `scope.md > Explicitly Cut`; localhost demo suffices.
- **Percentages and algebra subjects** — the data structure keeps them cheap to add later (`scope.md > Later`).

## Possible Later Enhancements

Subject expansion (percentages, algebra), typed-answer mode, richer hint wording, question bank growth, more granular dyslexia panel controls (independent toggles), deployment.

## Non-Goals

- **No accounts, signups, or server-side identity** — browser/device-local by design.
- **No scores, streaks, leaderboards, or any loss mechanic** — contradicts the kernel.
- **No red crosses, countdowns, or punishment animations** — same reason.
- **No question generation** — fixed, hand-written banks.
- **No reading of inputs or buttons aloud** — question text only.
- **No timer anywhere** — including the break screen.

## Open Questions

None blocking `4-spec`. Both items raised at draft were resolved at approval:

- **Speech fallback (resolved):** defined above — question stays usable, friendly unavailability message, nothing else blocked.
- **Hint wording (resolved as direction):** three-step structure stands; wording is short, encouraging, one idea per sentence — nudge, then first step, then method shown with different numbers, then answer + explanation for anyone still stuck. Exact text is authored with the 24 banked questions during build.
