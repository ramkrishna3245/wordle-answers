// Refresh the dataset from the official Wordle answer feed.
// Run by .github/workflows/update.yml once a day, and can be run manually.
const fs = require('fs');
const path = require('path');

const DATA_FILE = path.join(__dirname, '..', 'data', 'wordle-answers.json');
const FEED = 'https://www.nytimes.com/svc/wordle/v2/';

function easternDate() {
  const parts = new Intl.DateTimeFormat('en-CA', {
    timeZone: 'America/New_York',
    year: 'numeric', month: '2-digit', day: '2-digit',
  }).formatToParts(new Date());
  const get = (t) => parts.find((p) => p.type === t).value;
  return `${get('year')}-${get('month')}-${get('day')}`;
}

async function fetchAnswer(date) {
  const res = await fetch(FEED + date + '.json');
  if (!res.ok) return null;
  const body = await res.json();
  if (!body || typeof body.solution !== 'string' || body.solution.length !== 5) return null;
  return body.solution.toUpperCase();
}

(async () => {
  const data = JSON.parse(fs.readFileSync(DATA_FILE, 'utf8'));
  const today = easternDate();

  // check the last few days in case a fetch was missed
  const candidates = [];
  const base = new Date(today + 'T12:00:00Z');
  for (let i = 0; i < 5; i++) {
    const d = new Date(base.getTime() - i * 86400000).toISOString().slice(0, 10);
    candidates.push(d);
  }

  let added = 0;
  for (const date of candidates) {
    if (data.answers[date]) continue;
    const answer = await fetchAnswer(date).catch(() => null);
    if (!answer) continue;
    data.answers[date] = answer;
    added++;
    console.log('added', date, answer);
  }

  if (!added) {
    console.log('no new answers - nothing to commit');
    return;
  }

  const sorted = {};
  for (const k of Object.keys(data.answers).sort()) sorted[k] = data.answers[k];
  data.answers = sorted;
  data.meta.count = Object.keys(sorted).length;
  data.meta.last_date = Object.keys(sorted).slice(-1)[0];

  fs.writeFileSync(DATA_FILE, JSON.stringify(data, null, 2) + '\n');
  console.log('updated', added, 'answers; total now', data.meta.count);
})();
