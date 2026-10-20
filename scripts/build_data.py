# -*- coding: utf-8 -*-
"""Regenerate data/wordle-answers.csv and data/wordle-stats.json from the answers JSON.

Path-independent: works the same on Windows and on GitHub Actions ubuntu.
"""
import json, os, csv, collections, io, sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA = os.path.join(ROOT, "data")
ALPHA = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
VOW = set("AEIOU")

answers = json.load(open(os.path.join(DATA, "wordle-answers.json"), encoding="utf-8"))["answers"]
rows = sorted(answers.items())
words = [w for _, w in rows]
n = len(words)
total_letters = sum(len(w) for w in words)

# ---------- CSV ----------
csv_path = os.path.join(DATA, "wordle-answers.csv")
with open(csv_path, "w", encoding="utf-8", newline="") as f:
    w = csv.writer(f)
    w.writerow(["date", "answer", "puzzle_number", "first_letter", "last_letter", "vowels", "has_repeat"])
    for i, (d, word) in enumerate(rows):
        w.writerow([
            d, word, i + 1, word[0], word[-1],
            sum(1 for c in word if c in VOW),
            "true" if len(set(word)) < len(word) else "false",
        ])

# ---------- stats ----------
lf = collections.Counter("".join(words))
fl = collections.Counter(w[0] for w in words)
ll = collections.Counter(w[-1] for w in words)
vc = collections.Counter(sum(1 for c in w if c in VOW) for w in words)
cnt = collections.Counter(words)


def blk(counter, total):
    return {k: {"count": v, "percent": round(100.0 * v / total, 2)}
            for k, v in sorted(counter.items(), key=lambda kv: (-kv[1], kv[0]))}


letters_never_first = [c for c in ALPHA if fl[c] == 0]
# rare letters: how many ANSWERS contain them, and what share of answers that is
answer_has = collections.Counter()
for w in words:
    for c in set(w):
        answer_has[c] += 1
rare_letters = {
    c: {"count": answer_has[c], "percent": round(100.0 * answer_has[c] / n, 2)}
    for c in sorted(ALPHA, key=lambda c: answer_has[c])[:4]
}

stats = {
    "meta": {"count": n, "total_letters": total_letters},
    "letter_frequency": blk(lf, total_letters),
    "first_letter": blk(fl, n),
    "last_letter": blk(ll, n),
    "vowel_counts": {str(k): {"count": v, "percent": round(100.0 * v / n, 2)} for k, v in sorted(vc.items())},
    "repeated_letter": {
        "count": sum(1 for w in words if len(set(w)) < len(w)),
        "percent": round(100.0 * sum(1 for w in words if len(set(w)) < len(w)) / n, 2),
    },
    "distinct_words": len(cnt),
    "recycled_words": sorted([w for w, c in cnt.items() if c > 1]),
    "letters_never_first": letters_never_first,
    "rare_letters": rare_letters,
}

with open(os.path.join(DATA, "wordle-stats.json"), "w", encoding="utf-8") as f:
    json.dump(stats, f, indent=2)
    f.write("\n")

print("build_data: %d answers, %d letters, %d distinct" % (n, total_letters, len(cnt)))
print("  wrote", csv_path)
print("  wrote", os.path.join(DATA, "wordle-stats.json"))
