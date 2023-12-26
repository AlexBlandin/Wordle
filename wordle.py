from os import system
from pathlib import Path
from random import choice
from sys import platform


def readlines(fp: str, encoding="utf8"):
  return list(map(str.upper, map(str.strip, Path(fp).read_text(encoding).splitlines())))


def colour(guess: str, word: str):
  """Colours a guess for the given word, returns (terminal, tweetable) versions"""
  plain, green, yellow = "\033[0m", "\033[0;32m", "\033[0;33m"
  letters = [f"{green}{c}" if c == word[i] else f"{plain}{c}" for i, c in enumerate(guess)] + [plain]
  colours = ["🟩" if c == word[i] else "⬛" for i, c in enumerate(guess)]

  upto = {c: word.count(c) for c in guess}
  used = {c: sum(c == c_ == w for c_, w in zip(guess, word, strict=False)) for c in guess}

  for i, b in enumerate(c in word for c in guess):
    c = guess[i]
    if b and c != word[i] and used[c] < upto[c]:
      letters[i], colours[i] = f"{yellow}{c}", "🟨"
      used[c] += 1
  return "".join(letters), "".join(colours)


def wordle(kind: str, words: list[str], valid: set[str], N=6):
  """Generic Text-Mode Wordle, say what kind, the possible words, the valid inputs, and how many guesses they get"""
  day, word = choice(list(enumerate(words)))

  def display(turn):
    system("clear" if platform != "nt" else "cls")
    print("Pridel:", kind)
    for ts, g, _ in turn:
      print(ts, g)
    print()

  turn = [(f"{i + 1}/{N}:", "_____", "") for i in range(N)]
  for t in range(N):
    guess = ""
    while guess not in valid:
      display(turn)
      guess = input("> ").upper()

    turn[t] = (f"{t + 1}/{N}:", *colour(guess, word))  # type: ignore
    if guess == word:
      display(turn)
      break
  else:
    display(turn)
    print("Was:", word)
    print()

  print(f"Pridel ({kind}) {day + 1} {t + 1}/{N}")  # type: ignore
  for _, _, cs in turn:
    print(cs)


def main():
  """Pridel
  Generates random Wordle picks, not the daily one, so you can practice. Choose the Classic and NYT wordlist.
  Has some extras, such as the prototype "British" mode, or the Prime number variant Primel (hence the name)!
  """
  games = {"wordle": set("classic wordle"), "primel": set("primel primes"), "britle": set("british britle"), "nordle": set("nyt nordle")}
  games = {k: g.difference(*[g_ for g_ in games.values() if g_ != g]) for k, g in games.items()}
  print("Which mode would you like to play?", *games)
  # we test whether it contains any of the unique letters from each option, which should mean it tolerates some degree of error

  game = set(input("Classic Wordle, Primes, NYT Wordle, or British Wordle? ").lower())
  if len(game & games["wordle"]):
    words = readlines("data/wordle/words.txt")
    valid = set(readlines("data/wordle/valid.txt"))
    valid |= set(words)
    wordle("Wordle mode", words, valid)
  elif len(game & games["nordle"]):
    words = readlines("data/nordle/words.txt")
    valid = set(readlines("data/nordle/valid.txt"))
    valid |= set(words)
    wordle("Nordle mode", words, valid)
  elif len(game & games["primel"]):

    def ctz(v):
      return (v & -v).bit_length() - 1  # count trailing zeroes

    def prime(n):  # compressed Miller primality for 5 digit prime tests
      if not (n & 1) or not (n % 3) or not (n % 5) or not (n % 7):
        return False
      d = n - 1
      s = ctz(d)
      d >>= s

      def witness(a):
        if pow(a, d, n) == 1:
          return False
        return all(pow(a, 2**i * d, n) != n - 1 for i in range(s))

      return not (witness(2) or witness(3))

    primes = list(map(str, filter(prime, range(10000, 100000))))
    wordle("Primes mode", primes, set(primes))
  elif len(game & games["britle"]):
    words = readlines("data/britle/words.txt")
    valid = set(readlines("data/britle/valid.txt"))
    valid |= set(words)

    input(
      "Warning! This list may contain non-words, as I just pulled it from the British National Corpus and filtered to anything with 5 letters, considering it contains various lengths of repeating aaaaa and genetic code, as well as strange entries like 'zzyzx', this is more a logical exercise than an actual, authoritative 'British' version of Wordle. There's also about 30k possible words, so this isn't quite as viable in 6 guesses like usual. Press <ENTER> to continue."  # noqa: E501
    )
    wordle("British mode", words, valid)


if __name__ == "__main__":
  try:
    from colorama import init

    init()
  except Exception:
    pass
  if False:  # test colouring is correct (it is)
    for w in "abide erase steal crepe ester".split():
      print(*colour("speed", w), "when", w)
  print(main.__doc__)
  print()
  main()
