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
`sim3b1b.py` file, which is there for me to experiment with computing the
optimal strategies for Britle, mostly as a curiosity at the intersection between
information theory and linguistics.

`primel.py` is mostly intended for interactive usage during Primel play, given
that most people (including myself) don't have a "vocabulary" of primes. I'm not
going to make a version for normal Wordle or such, because that defeats the
point of the game, in my opinion.

## Requirements
- [`pip install -r requirements.txt`](https://www.python.org/)
  - [regenerate with `uv pip compile pyproject.toml -o requirements.txt`](https://github.com/astral-sh/uv)

- If wanting to use `sim3b1b.py` do `pip install -r requirements-3b1b.txt`
  - based on [3b1b's code](https://github.com/3b1b/videos/blob/master/_2022/wordle/simulations.py)
  - regenerate with `uv pip compile pyproject.toml --extra 3b1b -o requirements-3b1b.txt`
