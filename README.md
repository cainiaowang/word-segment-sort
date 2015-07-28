This program is an attempt to solve the following puzzle.

Take a sentence, strip the spaces, unify the case, cut the sentence up into segments that are of either length 2 or 3, finally shuffle these segments

The puzzle is thus to attempt to rearange these segments, such that they form the original sentence.


Example:

======================== Setup work ======================== 

"This is an example sentence that I am going to shuffle"

Stripped of spaces, cut up into segments, and then suffled becomes:

['ILL', 'ES', 'SHU', 'MPL', 'CEW', 'IS', 'EN', 'FF', 'EXA', 'TEN', 'LED', 'TH', 'BE']

(this process is completed by the python program shuffle.py)


======================== Main Puzzle ======================== 
The following are the solutions that have been found by 
the algorithm dictTree.py

SHUFFLEDEXAMPLESENTENCEWILLTHISBE
SHUFFLEDEXAMPLESENTENCEWILLBETHIS
SHUFFLEDTHISEXAMPLESENTENCEWILLBE
SHUFFLEDTHISBEEXAMPLESENTENCEWILL
SHUFFLEDBEEXAMPLESENTENCEWILLTHIS
SHUFFLEDBETHISEXAMPLESENTENCEWILL
EXAMPLESENTENCEWILLSHUFFLEDTHISBE
EXAMPLESENTENCEWILLSHUFFLEDBETHIS
EXAMPLESENTENCEWILLTHISSHUFFLEDBE
EXAMPLESENTENCEWILLTHISBESHUFFLED
EXAMPLESENTENCEWILLBESHUFFLEDTHIS
EXAMPLESENTENCEWILLBETHISSHUFFLED
THISSHUFFLEDEXAMPLESENTENCEWILLBE
THISSHUFFLEDBEEXAMPLESENTENCEWILL
THISEXAMPLESENTENCEWILLSHUFFLEDBE
THISEXAMPLESENTENCEWILLBESHUFFLED  <= Solution
THISBESHUFFLEDEXAMPLESENTENCEWILL
THISBEEXAMPLESENTENCEWILLSHUFFLED
BESHUFFLEDEXAMPLESENTENCEWILLTHIS
BESHUFFLEDTHISEXAMPLESENTENCEWILL
BEEXAMPLESENTENCEWILLSHUFFLEDTHIS


