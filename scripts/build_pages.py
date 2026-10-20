"""Generate a static GitHub Pages browser for the Wordle answer dataset."""
import json, os, html

REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DOCS = os.path.join(REPO, 'docs')
os.makedirs(DOCS, exist_ok=True)

data = json.load(open(os.path.join(REPO, 'data', 'wordle-answers.json'), encoding='utf-8'))
stats = json.load(open(os.path.join(REPO, 'data', 'wordle-stats.json'), encoding='utf-8'))
answers = data['answers']
rows = sorted(answers.items())

first = rows[0]
last = rows[-1]
lf = stats['letter_frequency']
firstl = stats['first_letter']

# rows as JSON for the client-side filter
rows_json = json.dumps([{'d': d, 'a': a, 'p': i + 1} for i, (d, a) in enumerate(rows)])

letter_bars = ''.join(
    '<div class="b"><span class="ch">%s</span><span class="bar" style="width:%.1f%%"></span>'
    '<span class="n">%s (%.2f%%)</span></div>' % (c, v['percent'] * 5, f"{v['count']:,}", v['percent'])
    for c, v in lf.items())

firstl_bars = ''.join(
    '<div class="b"><span class="ch">%s</span><span class="bar" style="width:%.1f%%"></span>'
    '<span class="n">%s (%.2f%%)</span></div>' % (c, v['percent'] * 4, f"{v['count']:,}", v['percent'])
    for c, v in firstl.items())

never = ', '.join(stats['letters_never_first']) or 'none'
recycled = ', '.join(stats['recycled_words'])

page = '''<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Wordle Answers - %(count)s answers by date (live dataset browser)</title>
<meta name="description" content="Browse all %(count)s Wordle answers by date. Search the answer, filter by first letter or year, and see the letter frequency statistics computed from the full dataset.">
<link rel="canonical" href="https://ramkrishna3245.github.io/wordle-answers/">
<style>
  :root { --fg:#1a1a1a; --muted:#6b7280; --bg:#fff; --mut:#f3f4f6; --bd:#e5e7eb; --ac:#2563eb; }
  @media (prefers-color-scheme: dark){ :root { --fg:#e8e8e8; --muted:#9aa0a6; --bg:#14161a; --mut:#1e2126; --bd:#2a2e35; --ac:#6ea8fe; } }
  *{box-sizing:border-box}
  body{margin:0;font:16px/1.65 -apple-system,BlinkMacSystemFont,"Segoe UI",Roboto,Helvetica,Arial,sans-serif;color:var(--fg);background:var(--bg)}
  .wrap{max-width:920px;margin:0 auto;padding:2rem 1.25rem 4rem}
  h1{font-size:1.9rem;line-height:1.25;margin:0 0 .35rem}
  h2{font-size:1.3rem;margin:2.6rem 0 .8rem}
  h3{font-size:1.02rem;margin:1.6rem 0 .5rem}
  .sub{color:var(--muted);margin:0 0 1.6rem}
  a{color:var(--ac)}
  .card{background:var(--mut);border:1px solid var(--bd);border-radius:12px;padding:1.1rem 1.25rem}
  .grid{display:grid;grid-template-columns:repeat(auto-fit,minmax(190px,1fr));gap:.9rem;margin:1rem 0}
  .k{font-size:1.7rem;font-weight:700;letter-spacing:-.02em}
  .kl{color:var(--muted);font-size:.82rem;text-transform:uppercase;letter-spacing:.05em}
  .bar{background:var(--ac);height:.6rem;border-radius:4px;display:inline-block;vertical-align:middle;min-width:2px}
  .b{display:flex;align-items:center;gap:.6rem;margin:.2rem 0;font-size:.86rem}
  .ch{width:1.1rem;font-weight:700;text-align:center}
  .n{margin-left:auto;color:var(--muted);font-variant-numeric:tabular-nums;white-space:nowrap}
  input,select{font:inherit;padding:.55rem .7rem;border:1px solid var(--bd);border-radius:8px;background:var(--bg);color:var(--fg);width:100%%}
  .row{display:grid;grid-template-columns:2fr 1fr 1fr;gap:.6rem;margin:.9rem 0}
  table{width:100%%;border-collapse:collapse;font-size:.9rem}
  th,td{text-align:left;padding:.42rem .6rem;border-bottom:1px solid var(--bd)}
  th{color:var(--muted);font-weight:600;font-size:.78rem;text-transform:uppercase;letter-spacing:.04em;position:sticky;top:0;background:var(--bg)}
  td.a{font-weight:700;letter-spacing:.06em}
  .scroller{max-height:520px;overflow:auto;border:1px solid var(--bd);border-radius:10px}
  .cnt{color:var(--muted);font-size:.86rem;margin:.5rem 0 0}
  code{background:var(--mut);padding:.1rem .35rem;border-radius:5px;font-size:.88em}
  .foot{margin-top:3rem;padding-top:1.2rem;border-top:1px solid var(--bd);color:var(--muted);font-size:.88rem}
  ul{padding-left:1.15rem}
  .tag{display:inline-block;background:var(--mut);border-radius:999px;padding:.15rem .6rem;font-size:.8rem;margin:.15rem .3rem .15rem 0}
</style>
</head>
<body>
<div class="wrap">
  <h1>Wordle answers, by date</h1>
  <p class="sub">All <strong>%(count)s</strong> published answers, %(first)s to %(last)s. Verified against the official feed and refreshed daily.</p>

  <div class="grid">
    <div class="card"><div class="k">%(count)s</div><div class="kl">answers</div></div>
    <div class="card"><div class="k">%(distinct)s</div><div class="kl">distinct words</div></div>
    <div class="card"><div class="k">%(repcount)s</div><div class="kl">words reused</div></div>
    <div class="card"><div class="k">%(xcount)s</div><div class="kl">X never opened one</div></div>
  </div>

  <h2>Look up an answer</h2>
  <div class="row">
    <input id="q" type="search" placeholder="Search answer, e.g. ADORN" autocomplete="off">
    <select id="letter"><option value="">Any first letter</option></select>
    <select id="year"><option value="">Any year</option></select>
  </div>
  <p class="cnt" id="cnt"></p>
  <div class="scroller">
    <table>
      <thead><tr><th style="width:7rem">Date</th><th style="width:4rem">#</th><th>Answer</th></tr></thead>
      <tbody id="tb"></tbody>
    </table>
  </div>

  <h2>What the data says</h2>
  <ul>
    <li><strong>E</strong> is %(etop)s%% of all %(letters)s letters - the most common letter by a wide margin.</li>
    <li><strong>S</strong> starts %(sstart)s%% of all answers (%(scount)s), by far the most common opener.</li>
    <li><strong>%(xletter)s has never once started an answer</strong> - zero out of %(count)s.</li>
    <li>%(repcount)s words have been used more than once. The first repeat was <code>CIGAR</code> on puzzle #1690 (2 Feb 2026) - the same word that opened the game in June 2021.</li>
    <li>%(repct)s%% of answers contain a repeated letter, and %(two)s%% have exactly two vowels.</li>
  </ul>

  <h3>Letter frequency</h3>
  <div class="card">%(letterbars)s</div>

  <h3>First letter of each answer</h3>
  <div class="card">%(firstlbars)s</div>

  <h2>Reused words</h2>
  <div class="card" style="font-size:.92rem">%(recycled)s</div>

  <h2>Use it in code</h2>
  <div class="card">
    <p style="margin-top:0">JSON and CSV are in the <a href="https://github.com/ramkrishna3245/wordle-answers">GitHub repo</a>, and the same data is on npm as <code>wordle-answers</code>.</p>
<pre style="overflow:auto;margin:0"><code>curl -s https://raw.githubusercontent.com/ramkrishna3245/wordle-answers/main/data/wordle-answers.json | jq -r '.answers["2024-03-14"]'</code></pre>
  </div>

  <div class="foot">
    <p><strong>Source:</strong> the official Wordle answer feed, checked date by date. Puzzle numbers count from the first Wordle on %(first)s.</p>
    <p><strong>Original dataset and analysis:</strong>
      <a href="https://github.com/ramkrishna3245/wordle-answers">github.com/ramkrishna3245/wordle-answers</a> &middot;
      <a href="https://anywordsolver.com/wordle-answer-statistics.html">anywordsolver.com/wordle-answer-statistics.html</a></p>
    <p>MIT licensed. Corrections welcome - a scheduled job re-fetches the feed daily.</p>
  </div>
</div>
<script>
var ROWS = %(rows)s;
var letters = %(lettersjs)s;
var tb = document.getElementById('tb');
var q = document.getElementById('q');
var letter = document.getElementById('letter');
var year = document.getElementById('year');
var cnt = document.getElementById('cnt');

Object.keys(letters).forEach(function(c){
  var o = document.createElement('option'); o.value = c; o.textContent = c; letter.appendChild(o);
});
var years = {};
ROWS.forEach(function(r){ years[r.d.slice(0,4)] = 1; });
Object.keys(years).sort().forEach(function(y){
  var o = document.createElement('option'); o.value = y; o.textContent = y; year.appendChild(o);
});

function render(){
  var term = q.value.trim().toUpperCase();
  var L = letter.value, Y = year.value;
  var out = [];
  for (var i=0;i<ROWS.length;i++){
    var r = ROWS[i];
    if (term && r.a.indexOf(term) === -1) continue;
    if (L && r.a[0] !== L) continue;
    if (Y && r.d.slice(0,4) !== Y) continue;
    out.push(r);
  }
  var html = '';
  for (var j=0;j<out.length;j++){
    html += '<tr><td>'+out[j].d+'</td><td>'+out[j].p+'</td><td class="a">'+out[j].a+'</td></tr>';
  }
  tb.innerHTML = html || '<tr><td colspan="3">No answers match that filter.</td></tr>';
  cnt.textContent = 'Showing ' + out.length.toLocaleString() + ' of ' + ROWS.length.toLocaleString() + ' answers';
}
q.addEventListener('input', render);
letter.addEventListener('change', render);
year.addEventListener('change', render);
render();
</script>
</body>
</html>
'''

html_page = page % {
    'count': f"{len(rows):,}",
    'distinct': f"{stats['distinct_words']:,}",
    'repcount': len(stats['recycled_words']),
    'xcount': '0',
    'first': first[0],
    'last': last[0],
    'letters': f"{stats['meta']['total_letters']:,}",
    'etop': lf['E']['percent'],
    'sstart': firstl['S']['percent'],
    'scount': f"{firstl['S']['count']:,}",
    'xletter': stats['letters_never_first'][0] if stats['letters_never_first'] else 'X',
    'repct': stats['repeated_letter']['percent'],
    'two': stats['vowel_counts']['2']['percent'],
    'letterbars': letter_bars,
    'firstlbars': firstl_bars,
    'recycled': recycled,
    'rows': rows_json,
    'lettersjs': json.dumps(lf),
}

with open(os.path.join(DOCS, 'index.html'), 'w', encoding='utf-8') as f:
    f.write(html_page)

# copy the data files so Pages serves them too
import shutil
shutil.copy(os.path.join(REPO, 'data', 'wordle-answers.json'), os.path.join(DOCS, 'wordle-answers.json'))
shutil.copy(os.path.join(REPO, 'data', 'wordle-answers.csv'), os.path.join(DOCS, 'wordle-answers.csv'))
shutil.copy(os.path.join(REPO, 'LICENSE'), os.path.join(DOCS, 'LICENSE'))

print('wrote', os.path.join(DOCS, 'index.html'), os.path.getsize(os.path.join(DOCS, 'index.html')), 'bytes')
print('rows:', len(rows), '| distinct:', stats['distinct_words'], '| recycled:', len(stats['recycled_words']))


