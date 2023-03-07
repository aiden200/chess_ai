# chess_ai
Chess AI


Table of contents
=================

<!--ts-->
* [Installation](#installation)
   * [Usage](#usage)
* [About the Code](#about-the-code)
* [Chess Engine](#chess-engine)
* [Piece-Square Tables](#Piece-Square-Tables)
* [Chess Piece Values](#Chess-Piece-Values)
* [Openers](#openers)
* [Future Implementations](#future-implementations)
* [The Algorithm](#the-algorithm)
<!--te-->


Installation
============

About the Code
============
I do know how to play chess, but not at a competetive level. It is entirely possible that there are factors that experts consider while playing chess that I have no knowledge of.

Chess Engine
============
The chess engine itself is a python library called python-chess. 
You can install is using the command:
```
pip install python-chess
```


Piece Square Tables
============
PSTs are just tables that indicate for each chess piece, how good is it to be on that respective square.
The higher the value is, the better. Since I am not a good chess player, I took these PSTs from online.

For example, this is the PST for a knight:

```
knight_pst = [
    -20, -10,  -10,  -10,  -10,  -10,  -10,  -20,
    -10,  -5,   -5,   -5,   -5,   -5,   -5,  -10,
    -10,  -5,   15,   15,   15,   15,   -5,  -10,
    -10,  -5,   15,   15,   15,   15,   -5,  -10,
    -10,  -5,   15,   15,   15,   15,   -5,  -10,
    -10,  -5,   10,   15,   15,   15,   -5,  -10,
    -10,  -5,   -5,   -5,   -5,   -5,   -5,  -10,
    -20,   0,  -10,  -10,  -10,  -10,    0,  -20
]
```
As you can see, the knights are more favorable to be in positions in the middle. This makes sense, as the knights have less options to move as it goes towards the edge.

These values make sense in the early game, but make less sense as the chess game approaches the endgame. To combat this, tapered evaluation implemented which gives the engine two sets of PST's, one set for the opening/middle-game, and one for the endgame. As the game progresses, the game engine slowly shifts its PST values towards the endgame board.

The code will look something like this:
```
eval = ((opening * (256 - phase)) + (endgame * phase)) / 256
```

Chess Piece Values
============
Found this ratio on the internet. Since i'm not a chess expert, I trust the internet more than myself.

| Piece | Weight |
| --- | --- |
| Pawn | 100 |
| Knight | 300 |
| Bishop | 300 |
| Rook | 500 |
| Queen | 900 |
| King | 100000 |

Openers
============
In the ``` chess_engine/books ``` directory, there are some binary files containig openers that we try to use initially.
Check out [this page](https://github.com/AnshGaikwad/Chess-World/tree/master/books) for more info.



Future Implementations
============
- Have a faster running program. Possibly implementing multiprocessing to speed up the search or switch to a faster programming language like C.
- Have a dictionary of openers to speed up the starting process and start the game off more effectively in playing.



The Algorithm
============
The chess AI uses the [minimax algorithm](https://en.wikipedia.org/wiki/Minimax) to decide its next move. It uses [alpha-beta pruning](https://en.wikipedia.org/wiki/Alpha%E2%80%93beta_pruning) to speed up the process. I will describe these algorithms in detail in this section.

Black pieces have positive weights, and white pieces have negative weights in this game. Therefore, if the AI was playing as the black player, it would want to make the score as big as possible, and vise versa.