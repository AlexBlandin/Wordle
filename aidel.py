from collections import defaultdict
from functools import partial
from operator import itemgetter
from pathlib import Path
from random import sample


def sorted_dict(d, key=itemgetter(1), reverse=False):
  return dict(sorted(d.items(), key=key, reverse=reverse))


data = Path(__file__).parent / "data"
words = (data / "nordle" / "words.txt").read_text().splitlines()
ws = set(words)  # working set


def inverse():
  return {c: set() for c in "abcdefghijklmnopqrstuvwxyz"}


by_letter = inverse()
by_column = {i: inverse() for i in range(5)}
by_negate = inverse()

for d in words:
  for i, c in enumerate(d):
    by_letter[c].add(d)
    by_column[i][c].add(d)
  for s in set("abcdefghijklmnopqrstuvwxyz") - set(d):
    by_negate[s].add(d)

aware = []
know = ["?"] * 5


def now():
  print("Contains", *aware)
  print("Known positions", *know)


def stat():
  """Stats for 2309 NYT Wordle words.

  # commonality of a given letter
  {"e": 1230, "a": 975, "r": 897, "o": 753, "t": 729, "l": 716, "i": 670, "s": 668, "n": 573, "c": 475, "u": 466, "y": 424, "d": 393, "h": 387, "p": 365, "m": 316, "g": 310, "b": 280, "f": 229, "k": 210, "w": 194, "v": 152, "z": 40, "x": 37, "q": 29, "j": 27}

  # commonality of a given letter in a given column
  {0: {"s": 365, "c": 198, "b": 173, "t": 149, "p": 141, "a": 140, "f": 135, "g": 115, "d": 111, "m": 107, "r": 105, "l": 87, "w": 82, "e": 72, "h": 69, "v": 43, "o": 41, "n": 37, "i": 34, "u": 33, "q": 23, "j": 20, "k": 20, "y": 6, "z": 3},
  1: {"a": 304, "o": 279, "r": 267, "e": 241, "i": 201, "l": 200, "u": 185, "h": 144, "n": 87, "t": 77, "p": 61, "w": 44, "c": 40, "m": 38, "y": 22, "d": 20, "s": 16, "b": 16, "v": 15, "x": 14, "g": 11, "k": 10, "f": 8, "q": 5, "z": 2, "j": 2},
  2: {"a": 306, "i": 266, "o": 243, "e": 177, "u": 165, "r": 163, "n": 137, "l": 112, "t": 111, "s": 80, "d": 75, "g": 67, "m": 61, "p": 57, "b": 56, "c": 56, "v": 49, "y": 29, "w": 26, "f": 25, "k": 12, "x": 12, "z": 11, "h": 9, "j": 3, "q": 1},
  3: {"e": 318, "n": 182, "s": 171, "a": 162, "l": 162, "i": 158, "c": 150, "r": 150, "t": 139, "o": 132, "u": 82, "g": 76, "d": 69, "m": 68, "k": 55, "p": 50, "v": 45, "f": 35, "h": 28, "w": 25, "b": 24, "z": 20, "y": 3, "x": 3, "j": 2},
  4: {"e": 422, "y": 364, "t": 253, "r": 212, "l": 155, "h": 137, "n": 130, "d": 118, "k": 113, "a": 63, "o": 58, "p": 56, "m": 42, "g": 41, "s": 36, "c": 31, "f": 26, "w": 17, "i": 11, "b": 11, "x": 8, "z": 4, "u": 1}}
  """  # noqa: E501
  letter, column = defaultdict(int), {i: defaultdict(int) for i in range(5)}
  for d in ws:
    for i, c in enumerate(d):
      column[i][c] += 1
      letter[c] += 1
  letter = sorted_dict(letter, reverse=True)
  column = {i: sorted_dict(d, reverse=True) for i, d in column.items()}
  print(len(ws))
  print(letter)
  for col, letters in column.items():
    print(f"{col}: {letters}")


def guess(ws=ws):
  if len(ws) > 10:
    print(*sample(sorted(ws), 10))
  else:
    print(*ws)


def unique(ws=ws):  # guess but all letters different
  guess(list(filter(lambda p: len(set(p)) == 5, ws)))  # type: ignore


def has(ltr: str, col: int):  # you know it's there, but that it's not in this column
  aware.append(ltr)
  ws.difference_update(by_negate[ltr])
  ws.difference_update(by_column[col][ltr])


def no(*letters: list[str]):
  for ltr in letters:
    ws.difference_update(by_letter[ltr])  # type: ignore


def at(ltr: str, col: int):
  if ltr in aware:
    aware.remove(ltr)
  know[col] = ltr
  for d, s in by_column[col].items():
    if d != ltr:
      ws.difference_update(s)


def code(*pairs):
  two_words = partial(str.split, maxsplit=1)
  for guess, code in map(two_words, pairs):
    for col, (letter, colour) in enumerate(zip(guess, code, strict=False)):
      if colour == "g":
        at(letter, col)
      elif colour == "y":
        has(letter, col)
      else:
        no(letter)  # type: ignore


if __name__ == "__main__":
  while 1:
    pair = input("Guess and colours[gyn]: ")
    code(pair)
    stat()
    guess()
