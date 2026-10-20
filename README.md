# wordle-answers

**Every Wordle answer, by date, as JSON and CSV.** 1,994 answers covering 19 June 2021 → 5 December 2026, verified against the official feed and refreshed daily.

No API key. No rate limit. No tracking. Just the data.

```json
{
  "2021-06-19": "CIGAR",
  "2021-06-20": "REBUT",
  "2024-03-15": "RETRO",
  "2026-10-18": "ADORN"
}
```

---

## What's in here

| File | What it is |
|---|---|
| [`data/wordle-answers.json`](data/wordle-answers.json) | `{"YYYY-MM-DD": "ANSWER"}` map, plus a `meta` block |
| [`data/wordle-answers.csv`](data/wordle-answers.csv) | One row per puzzle: date, answer, puzzle number, first/last letter, vowel count, repeat flag |
| [`data/wordle-stats.json`](data/wordle-stats.json) | Computed statistics: letter frequency, first/last letter distribution, vowel counts, rare letters, recycled words |
| [`index.js`](index.js) | Zero-dependency Node helper for lookups and range queries |

## Quick start

**Node**
```js
const { answers, getAnswer, getRange, stats } = require('wordle-answers');

answers['2024-03-15'];        // 'RETRO'
getAnswer('2024-03-15');       // 'RETRO'
getRange('2026-10-14', '2026-10-20');
// [ { date: '2026-10-14', answer: '...' }, ... ]
```

**Python**
```python
import json, urllib.request

data = json.load(urllib.request.urlopen(
    "https://raw.githubusercontent.com/ramkrishna3245/wordle-answers/main/data/wordle-answers.json"))

data["answers"]["2024-03-15"]     # 'RETRO'
data["meta"]["count"]              # 1994
```

**curl + jq**
```bash
curl -s https://raw.githubusercontent.com/ramkrishna3245/wordle-answers/main/data/wordle-answers.json \
  | jq -r '.answers["2024-03-15"]'
```

**CSV**
```bash
curl -s https://raw.githubusercontent.com/ramkrishna3245/wordle-answers/main/data/wordle-answers.csv
```

## Use it for

- **Puzzle solvers and clones** — filter a candidate word list by date
- **Analytics and charts** — "how often does each letter appear in a Wordle answer?"
- **Data science and NLP** — a clean, correctly-formatted 1,994-word corpus
- **Games** — "what was the answer on 14 March 2024?"

---

## The data says some interesting things

These are computed from the dataset itself, and are also in [`data/wordle-stats.json`](data/wordle-stats.json).

**E is the most common letter**, at 10.83% of all 9,970 letters.

**S starts 15% of all answers** (300 of 1,994) — by a wide margin over C at 8.58%.

**X has never once started an answer.** Zero out of 1,994. (It still appears mid-word in 34 answers.)

**E ends 19.81% of answers and Y ends 14.29%.** Nearly one answer in five ends in E.

**31% of answers contain a repeated letter** (619 of 1,994) — 633 double-letter occurrences and 14 triples.

**58% of answers have exactly two vowels** (1,158 of 1,994). Only 8 answers in the entire history have no vowels, and only 3 have four.

**"Wordle never repeats words" is not true.** There are 1,962 distinct words across 1,994 answers. 32 words have been used more than once — the first repeat was puzzle #1,690 on 2 February 2026, and the word was `CIGAR`, the same word that opened the game in June 2021.

The full analysis, with charts, is here: **[anywordsolver.com/wordle-answer-statistics.html](https://anywordsolver.com/wordle-answer-statistics.html)**

---

## Data format

### `data/wordle-answers.json`
```json
{
  "meta": {
    "description": "Every Wordle answer by date, verified against the official feed.",
    "count": 1994,
    "first_date": "2021-06-19",
    "last_date": "2026-12-05",
    "puzzle_number_first": 1,
    "source": "https://anywordsolver.com/wordle-answer-statistics.html"
  },
  "answers": { "2021-06-19": "CIGAR", "...": "..." }
}
```

### `data/wordle-answers.csv`
| date | answer | puzzle_number | first_letter | last_letter | vowels | has_repeat |
|---|---|---|---|---|---|---|
| 2021-06-19 | CIGAR | 1 | C | R | 2 | false |
| 2026-10-18 | ADORN | 1948 | A | N | 2 | false |

`puzzle_number` is the puzzle index counted from the first Wordle on 19 June 2021.

---

## How it stays current

A scheduled GitHub Action re-fetches the source feed once a day and commits any new answers. If a new answer appears, the repo updates itself within 24 hours — no pull request needed.

The workflow is in [`.github/workflows/update.yml`](.github/workflows/update.yml). You can also [trigger it manually](https://github.com/ramkrishna3245/wordle-answers/actions).

## Data source and accuracy

Every entry was fetched from the official Wordle answer feed and checked against the date it belongs to. Puzzle numbers are derived from the launch date, 19 June 2021, and match the published numbering.

If you find a wrong entry, please [open an issue](https://github.com/ramkrishna3245/wordle-answers/issues) — corrections are welcome and will be merged by the scheduled job.

## Related

- **Live archive and analysis:** https://anywordsolver.com/wordle-answer-statistics.html
- **Full answer archive by date:** https://anywordsolver.com/wordle-answer-archive.html
- **Free Wordle solver:** https://anywordsolver.com/wordle-solver.html

## License

MIT — see [`LICENSE`](LICENSE). Use it anywhere, no attribution required (though a link back is appreciated).
