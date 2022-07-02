# Pridel: Wordle

This is a terminal version of Wordle, originally designed for practice, I then
added the "Primel" variant of 5-digit primes, and then a "Britle" variant based
on the British National Corpus (which has yet to be filtered to actual words).
It still gives the "tweetable" printout at the end, though it's marked as Pridel
to differentiate itself from normal Wordle, which was from when I first made the
Primel mode part of it and wanted to suggest the blending of the two. I've also
added the NYT Wordle under the "Nordle" mode, for practicing with the "official"
wordset.

I'll use this for random tests, and naturally it's for me to play with. An
example is the "Britle" mode of British English (so "colour" etc). Another is the
`sim-3b1b.py` file, which is there for me to experiment with computing the
optimal strategies for Britle, mostly as a curiosity at the intersection between
information theory and linguistics.

`primel.py` is mostly intended for interactive usage during Primel play, given
that most people (including myself) don't have a "vocabulary" of primes. I'm not
going to make a version for normal Wordle or such, because that defeats the
point of the game, in my opinion.

## Requirements

- Python 3.7 or later
- [`poetry install`](https://python-poetry.org/), which handles:
  - `wordle.py` uses `colorama` for ensuring terminal output is coloured, such as
    on Windows.
    - If it isn't found, the `ModuleNotFoundError` is suppressed and it just
      carries on assuming your terminal handles ANSI/VT100 colour codes.
  - `sim-3b1b.py` uses `numpy`, `scipy`, `tqdm`, and `rich` (based on [3b1b's code](https://github.com/3b1b/videos/blob/master/_2022/wordle/simulations.py))
  	- These are optional and installed with `poetry install --all-extras`
- `primel.py` has no dependencies
