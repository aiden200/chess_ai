# chess_ai
Chess AI


Table of contents
=================

<!--ts-->
   * [Installation](#installation)
   * [About the Code](#about-the-code)
        * [Chess Engine](#chess-engine)
        * [The Algorithm](#the-algorithm)
        * [Piece-Square Tables](#Piece-Square-Tables)
   * [Usage](#usage)
      * [STDIN](#stdin)
      * [Local files](#local-files)
   * [Tests](#tests)
   * [Dependency](#dependency)
   * [Docker](#docker)
     * [Local](#local)
<!--te-->


Installation
============

About the Code
============
This code was developed by Aiden Chang.

Chess Engine
============
The chess engine itself is a python library called python-chess. 
You can install is using the command:
```
pip install python-chess
```

The Algorithm
============
The algorithm uses minimax and alpha beta pruning to speed up the process. 

Piece Square Tables
============
PSTs are just tables that indicate for each chess piece, how good is it to be on that respective square.
The higher the value is, the better.

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
