# Open ECG Trainer: web prototype

React + Vite + Tailwind, static, with no backend. Progress and the response log live in this browser's
localStorage, and can be exported as CSV or JSON from the overview screen.

```bash
npm install
npm run dev      # http://localhost:5173
npm run build    # static site in dist/ (relative paths, GitHub Pages ready)
```

The item bank is generated, not hand-edited. Run `python scripts/build_items.py` from the project root
with the `.venv`. It writes `public/ecgs/*.png`, `public/data/items.json` and `public/data/classes.json`.

How a session works (`src/scheduler.ts`):
- **Spaced set:** due FSRS reviews, plus up to 10 new items, interleaved.
- **Massed set:** the next unfinished class, served as one contiguous block.
- **Normal ECGs:** two per session as foils, outside the spaced/massed contrast.
- **FSRS grade:** a wrong answer is Again. A right answer is Hard at confidence 1-2, Good at 3-4 and
  Easy at 5. ts-fsrs runs with default v6 parameters.

The prototype does not yet have:
- a server-side log;
- trial calendar dates for the massed blocks;
- a pre-test or post-test mode;
- participant enrolment.
