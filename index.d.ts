export interface WordleMeta {
  description: string;
  count: number;
  first_date: string;
  last_date: string;
  puzzle_number_first: number;
  source: string;
}

export interface WordleRow {
  date: string;
  answer: string;
  puzzleNumber: number;
}

export interface LetterStat {
  count: number;
  percent: number;
}

export interface WordleStats {
  meta: { count: number; total_letters: number };
  letter_frequency: Record<string, LetterStat>;
  first_letter: Record<string, LetterStat>;
  last_letter: Record<string, LetterStat>;
  vowel_counts: Record<string, LetterStat>;
  repeated_letter: { count: number; percent: number };
  distinct_words: number;
  recycled_words: string[];
  letters_never_first: string[];
  rare_letters: Record<string, LetterStat>;
}

/** Every Wordle answer, keyed by date ("2024-03-15"). */
export const answers: Record<string, string>;

/** Dataset metadata. */
export const meta: WordleMeta;

/** Computed statistics over the full dataset. */
export const stats: WordleStats;

/** Answer for a given date, or undefined if that date is not in the dataset. */
export function getAnswer(date: string): string | undefined;

/** Puzzle number counted from the first Wordle on 19 June 2021. */
export function getPuzzleNumber(date: string): number;

/** All answers between two dates inclusive. */
export function getRange(startDate: string, endDate: string): WordleRow[];

/** Every distinct answer word, alphabetically. */
export function getAllWords(): string[];
