# Chess AI

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
## How to run the code

Clone the github repository, install and activate python venv. 

Install a python virtual environment (Optional):
```
python3 -m venv [path to virtual environment]
```

To start virtual environment and install required packages:
```
cd [path to virtual environment]
source bin/activate
pip install -r requirements.txt
```

### Usages:
Simulate the AI going against itself by typing in:
```
python3 simulate.py
```
The AI will battle against itelf with a [plie](#the-algorithm) value of 3.


Play against the AI using a GUI interface by typing in:
```
python3 app.py
```
In the user input, first type in the location of the piece you want to move then its destination.
If the move is not legal, the text message that says "human move" will change to "illegal move".
For example, if I want to move a piece from e6 to e5, I would type in "e6e5".
> **Warning**
> There is a known bug with the undo button, please only use the reset button and the human move


Activate the discord chess bot by typing in:
```
python3 discord_bot_activate
```
> **Warning**
> Functionality not implemented yet



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

> **Note**
> tapered evaluation not implemented yet

The code will look something like this:
```
eval = ((opening * (256 - phase)) + (endgame * phase)) / 256
```

Chess Piece Values
============
Found this ratio on the internet. Since i'm not a chess expert, I trust the internet more than myself.

| Piece | Weight(Black) | Weight(White) | 
| --- | --- | --- |
| Pawn | 100 | -100 |
| Knight | 300 | -300 |
| Bishop | 300 | -300 |
| Rook | 500 | -500 |
| Queen | 900 | -900 |
| King | 100000 | -100000 |

Openers
============
In the ``` chess_engine/books ``` directory, there are some binary files containig openers that we try to use initially.
Check out [this page](https://github.com/AnshGaikwad/Chess-World/tree/master/books) for more info.



Future Implementations
============
- Have a faster running program. Possibly implementing multiprocessing to speed up the search or switch to a faster programming language like C.
- ~~Have a dictionary of openers to speed up the starting process and start the game off more effectively in playing.~~
- Tapered evaluation



The Algorithm
============
The chess AI uses the [minimax algorithm](https://en.wikipedia.org/wiki/Minimax) to decide its next move. It uses [alpha-beta pruning](https://en.wikipedia.org/wiki/Alpha%E2%80%93beta_pruning) to speed up the process. I will describe these algorithms in detail in this section.

Black pieces have positive weights, and white pieces have negative weights in this game. Therefore, if the AI was playing as the black player, it would want to make the score as big as possible, and vise versa.

In this example, our AI will be the black player. This means the AI will try to maximize his score.
At any given state of the board, we can ask the total value of the board. 
To find the total value of the board, we will sum up all the [values of the pieces](#chess-piece-values) alive and add that to the total PST value for each piece.

- for every piece alive on the board $p_i$ and its respective value $v_i$, total_piece_value = $\sum p_i*v_i$
- for every black piece alive on the board $pb_i$, total_pst_value_black = $\sum pst[pb_i]$
- Similarly for white, for every white piece alive on the board $pb_i$, total_pst_value_black = $-\sum pst[pb_i]$

So the total value of the board can be represented as:
```total_value = total_piece_value + total_pst_value_black + total_pst_value_black```



