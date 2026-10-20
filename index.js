/**
 * wordle-answers
 * Zero-dependency helper for the Wordle answer dataset.
 *
 *   const { answers, getAnswer, getRange, getPuzzleNumber, stats } = require('wordle-answers');
 */

const data = require('./data/wordle-answers.json');
const stats = require('./data/wordle-stats.json');

const answers = data.answers;

/** Answer for a given date ("2024-03-15"), or undefined. */
function getAnswer(date) {
  return answers[date];
}

/** Puzzle number counted from the first Wordle (19 June 2021). */
function getPuzzleNumber(date) {
  const first = Date.UTC(
    Number(data.meta.first_date.slice(0, 4)),
    Number(data.meta.first_date.slice(5, 7)) - 1,
    Number(data.meta.first_date.slice(8, 10))
  );
  const parts = String(date).split('-');
  const target = Date.UTC(Number(parts[0]), Number(parts[1]) - 1, Number(parts[2]));
  return Math.round((target - first) / 86400000) + 1;
}

/** All answers between two dates inclusive, as { date, answer, puzzleNumber } rows. */
function getRange(startDate, endDate) {
  const out = [];
  for (const date of Object.keys(answers).sort()) {
    if (date >= startDate && date <= endDate) {
      out.push({ date, answer: answers[date], puzzleNumber: getPuzzleNumber(date) });
    }
  }
  return out;
}

/** Every distinct answer word, alphabetically. */
function getAllWords() {
  return Object.values(answers).sort();
}

module.exports = {
  answers,
  meta: data.meta,
  stats,
  getAnswer,
  getPuzzleNumber,
  getRange,
  getAllWords,
};
