from pprint import pprint as pp
from pathlib import Path
from random import sample
from operator import itemgetter
from collections import defaultdict

def sorted_dict(d, key=itemgetter(1), reverse=False): return dict(sorted(d.items(), key=key, reverse=reverse))

words = Path("data/nordle/words.txt").read_text().splitlines()
ws = set(words) # working set

def inverse(): return {c: set() for c in "abcdefghijklmnopqrstuvwxyz"}
by_letter = inverse()
by_column = {i: inverse() for i in range(5)}
by_negate = inverse()

for d in words:
  for i,c in enumerate(d):
    by_letter[c].add(d)
    by_column[i][c].add(d)
  for s in set("abcdefghijklmnopqrstuvwxyz") - set(d):
    by_negate[s].add(d)

aware = []
know = ["?"]*5

def now():
  global aware,know
  print("Contains", *aware)
  print("Known positions", *know)

def stat():
  """
  # commonality of a given letter
  {1: 5672, 3: 5552, 7: 5520, 9: 5484, 2: 3515, 5: 3456, 4: 3412, 6: 3372, 8: 3339, 0: 2493}
  
  # commonality of a given letter in a given column
  {0: {1: 1033, 2: 983, 3: 958, 4: 930, 5: 924, 7: 902, 9: 879, 6: 878, 8: 876},
  4: {7: 2103, 3: 2092, 9: 2087, 1: 2081}}
  """
  letter, column = defaultdict(int), {i:defaultdict(int) for i in range(5)}
  for d in ws:
    for i,c in enumerate(d):
      column[i][c] += 1
      letter[c] += 1
  letter = sorted_dict(letter, reverse=True)
  column = {i:sorted_dict(d, reverse=True) for i,d in column.items()}
  print(len(ws))
  print(letter)
  pp(column, width=120)

def guess(ws=ws):
  if len(ws) > 10:
    print(*sample(ws, 10))
  else:
    print(*ws)

def unique(ws=ws): # guess but all letters different
  guess(list(filter(lambda p: len(set(p))==5, ws)))

def has(ltr: str, col: int): # you know it's there, but that it's not in this column
  global aware, know
  aware.append(ltr)
  ws.difference_update(by_negate[ltr])
  ws.difference_update(by_column[col][ltr])
def no(*letters: list[str]):
  global aware,know
  for ltr in letters:
    ws.difference_update(by_letter[ltr])
def at(ltr: str, col: int):
  global aware,know
  if ltr in aware: aware.remove(ltr)
  know[col] = ltr
  for d, s in by_column[col].items():
    if d != ltr:
      ws.difference_update(s)

def code(*pairs):
  for guess, code in map(str.split, pairs):
    for i,(n,c) in enumerate(zip(guess, code)):
      match c:
        case "n":
          no(n)
        case "g":
          at(n,i)
        case "y":
          has(n,i)

if __name__=="__main__":
  print(*sample(words, 10))
