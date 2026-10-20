const assert = require('assert');
const m = require('./index.js');

assert.ok(Object.keys(m.answers).length > 1900, 'expected ~1,994 answers');
assert.strictEqual(m.getAnswer('2021-06-19'), 'CIGAR');
assert.strictEqual(m.getAnswer('2026-10-18'), 'ADORN');
assert.strictEqual(m.getAnswer('1999-01-01'), undefined);
assert.strictEqual(m.getPuzzleNumber('2021-06-19'), 1);
assert.strictEqual(m.getPuzzleNumber('2024-03-14'), 1000);
assert.strictEqual(m.getPuzzleNumber('2026-10-18'), 1948);

const range = m.getRange('2026-10-16', '2026-10-18');
assert.strictEqual(range.length, 3);
assert.deepStrictEqual(range.map((r) => r.answer), ['SHADY', 'GAFFE', 'ADORN']);

assert.deepStrictEqual(m.stats.letters_never_first, ['X']);
assert.strictEqual(m.stats.distinct_words, 1962);
assert.strictEqual(m.stats.recycled_words.length, 32);
assert.ok(m.getAllWords().length >= 1962);

console.log('all tests passed (' + Object.keys(m.answers).length + ' answers)');
