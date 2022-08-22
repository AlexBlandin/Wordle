from collections import defaultdict
from operator import itemgetter
from random import sample
from pprint import pprint as pp

def sorted_dict(d, key=itemgetter(1), reverse=False): return dict(sorted(d.items(), key=key, reverse=reverse))
def ctz(v): return (v & -v).bit_length() - 1
def prime(n): # compressed Miller primality for 5 digit prime tests
  if not (n & 1) or not (n % 3) or not (n % 5) or not (n % 7): return False
  d = n-1
  s = ctz(d)
  d >>= s
  
  def witness(a):
    if pow(a, d, n) == 1: return False
    for i in range(s):
      if pow(a, 2**i * d, n) == n-1: return False
    return True
  
  return not (witness(2) or witness(3))

FDPs = list(filter(prime, range(10000,100000)))
ws = set(FDPs) # working set

by_digit = {0: set(), 1: set(), 2: set(), 3: set(), 4: set(), 5: set(), 6: set(), 7: set(), 8: set(), 9: set()}
by_column = {0: {1: set(), 2: set(), 3: set(), 4: set(), 5: set(), 6: set(), 7: set(), 8: set(), 9: set()}, 1: {0: set(), 1: set(), 2: set(), 3: set(), 4: set(), 5: set(), 6: set(), 7: set(), 8: set(), 9: set()}, 2: {0: set(), 1: set(), 2: set(), 3: set(), 4: set(), 5: set(), 6: set(), 7: set(), 8: set(), 9: set()}, 3: {0: set(), 1: set(), 2: set(), 3: set(), 4: set(), 5: set(), 6: set(), 7: set(), 8: set(), 9: set()}, 4: {1: set(), 3: set(), 7: set(), 9: set()}}
by_negate = {0: set(), 1: set(), 2: set(), 3: set(), 4: set(), 5: set(), 6: set(), 7: set(), 8: set(), 9: set()}

for d in FDPs:
  for i,c in enumerate(map(int,str(d))):
    by_digit[c].add(d)
    by_column[i][c].add(d)
  for s in {1,2,3,4,5,6,7,8,9,0} - set(map(int,str(d))):
    by_negate[s].add(d)

aware = []
know = ["?"]*5

def now():
  global aware,know
  print("Contains", *aware)
  print("Known positions", *know)

def stat():
  """
  # commonality of a given digit
  {1: 5672, 3: 5552, 7: 5520, 9: 5484, 2: 3515, 5: 3456, 4: 3412, 6: 3372, 8: 3339, 0: 2493}
  
  # commonality of a given digit in a given column (by default only 0 and 4 are interesting)
  {0: {1: 1033, 2: 983, 3: 958, 4: 930, 5: 924, 7: 902, 9: 879, 6: 878, 8: 876},
  4: {7: 2103, 3: 2092, 9: 2087, 1: 2081}}
  """
  digit, column = defaultdict(int), {i:defaultdict(int) for i in range(5)}
  for d in ws:
    for i,c in enumerate(map(int, str(d))):
      column[i][c] += 1
      digit[c] += 1
  digit = sorted_dict(digit, reverse=True)
  column = {i:sorted_dict(d, reverse=True) for i,d in column.items()}
  print(len(ws))
  print(digit)
  pp(column, width=120)

def guess(ws=ws):
  if len(ws) > 10:
    print(*sample(ws, 10))
  else:
    print(*ws)

def unique(ws=ws): # guess but all digits different
  guess(list(filter(lambda p: len(set(str(p)))==5, ws)))

def has(x: int, c: int): # you know it's there, but that it's not in this column
  global aware,know
  aware.append(x)
  ws.difference_update(by_negate[x])
  ws.difference_update(by_column[c][x])
def no(*xs: list[int]):
  global aware,know
  for x in xs:
    ws.difference_update(by_digit[x])
def at(x: int, c: int):
  global aware,know
  if x in aware: aware.remove(x)
  know[c]=x
  for d, s in by_column[c].items():
    if d != x:
      ws.difference_update(s)

def code(number, code):
  for i,(n,c) in enumerate(zip(str(number), code)):
    n=int(n)
    match c:
      case "n":
        no(n)
      case "g":
        at(n,i)
      case "y":
        has(n,i)

if __name__=="__main__":
  print(*sample(FDPs, 10))
