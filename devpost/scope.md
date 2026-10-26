---
doc: scope
status: draft
---

# Perceptron

One line: a maths practice web app that adapts to students aged 12–18 with ADHD and dyslexia — one question at a time, read aloud with word-by-word highlighting, gentle hints, and rewards that are never taken away.

## The Unique Kernel
Accessibility-first practice loop: the question is read aloud with each word lighting up in sync, wrong answers get a gentle hint, and **nothing is ever taken away** — no streaks, no penalties, no losses. The dyslexia panel is part of the identity: font, spacing, text size, and motion change together in one tap. Other apps have maths drills; this combination is what makes Perceptron different.

## Who It's For
A teenager, 12–18, with ADHD or dyslexia, who wants to practise maths but gets overwhelmed or discouraged by dense question screens and loss-based gamification. Today they either avoid maths apps or push through ones that punish mistakes with streak resets and red crosses.

## The Core Loop
Open the app (no signup) → six-question skippable placement check sets a starting fraction level → then one fraction question at a time: tap "Read aloud" and watch words light up as spoken, answer, get a gentle hint if wrong, earn honey when right (cap 50 drops/day, rate-limited). Honey persists across refreshes. Dyslexia panel adjusts the layout whenever the student wants.

## Inspiration & Identity
- Neubrutalist look: thick black outlines, flat shadows, bright colours.
- ADHD-friendly: one question at a time, nothing taken away, quick successes.
- Dyslexia-friendly: read-aloud with word highlight; one-tap typography and motion adjustment.
- No external design references named yet; `3-prd` may ask 1–2 questions here.

## Why This Matters to the Learner
Accessibility is the point: a maths app that treats students with ADHD and dyslexia as the primary user, not an afterthought. The learner also explicitly wants to practise plan-first building and to understand how Vue and Flask connect.

## What "Working" Looks Like
Demo day, ~60 seconds from localhost, no signup:
- **USP (15s):** state the problem and what makes Perceptron different — read-aloud word highlighting, gentle no-penalty hints, one-tap dyslexia layout.
- **Proof (45s):** start the six-question placement check and skip one → see the starting level. Tap "Read aloud" → each word lights up in sync with the speech. Give a wrong answer → a gentle hint appears, nothing is taken away. Give a correct answer → honey is added to the counter. Tap the dyslexia panel once → font, spacing, size, and motion visibly change together.
- "It's alive" evidence: honey persists after a refresh; the highlighted word follows the speech; the layout visibly changes on panel tap.
- The "oh, that's cool" beat: the word lighting up exactly as it is spoken, with the layout reflowed for dyslexia in one tap.

## The POC Boundary
In:
- Fractions only (one subject, done well), question data in a simple structure so more subjects can be added later.
- Six-question skippable placement check (small) → starting level.
- One-question-at-a-time practice with gentle hints; incorrect answer = hint, no penalty.
- "Read aloud" with word-by-word highlighting.
- Dyslexia panel: spacing, font, text size, motion — one tap.
- Honey counter with a 50/day cap; for the demo, a setting lowers the cap so "Done for today" is quick to show.
- No signup; anonymous persistence so honey and level survive a refresh.
- Neubrutalist visual treatment.
- Vue front end, Flask back end; demo runs on localhost.
Out of PoC: signup/accounts, percentages, algebra, deployment.

## Later
- Percentages and algebra subjects (data structure already supports them).
- Deployment to a public URL — the stretch goal, only if the build finishes with time to spare.

## Explicitly Cut
- **Deployment (for now):** demo from localhost satisfies the hackathon; deployment adds time the 2–4 hour budget doesn't have. Revisit as a stretch goal after the build is done.
- **Percentages and algebra:** one subject done well beats three done thinly.
- **Daily honey cap above demo needs:** the 50/day rule stays in, but only takes effect beyond what the demo shows; "cut" order is deployment → honey cap → extra levels if time runs short.
- **Signup/accounts:** anonymous persistence is enough to prove the loop.
