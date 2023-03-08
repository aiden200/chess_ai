import traceback
from flask import Flask, Response, request
import webbrowser
import time
import chess
import chess.svg
from chess_engine.chess_game import Chess_game

game = Chess_game(4)
game_over = False
message = ''


app = Flask(__name__)
# Front Page of the Flask Web Page
@app.route("/")
def main():
    global count, game, message, game_over
    if game.winner != None:
        game_over = True
        message = game.winner
    try:
        if game.turn and (not game_over):
            move = game.make_move()
            game.board.push(move)
            message = "Human Turn"
            game.turn = 0
    except Exception as e:
        print(f"crashed in AI turn with exception {e}")
    if game.winner != None:
        game_over = True
        message = game.winner

    ret = '<html><head>'
    ret += '<style>input {font-size: 20px; } button { font-size: 20px; }</style>'
    ret += '</head><body>'
    ret += f'<p></a>{message}<a></p>'
    ret += '<img width=510 height=510 src="/board.svg?%f"></img></br></br>' % time.time()
    ret += '<form action="/game/" method="post"><button name="New Game" type="submit">New Game</button></form>'
    ret += '<form action="/undo/" method="post"><button name="Undo" type="submit">Undo Last Move</button></form>'
    ret += '<form action="/move/"><input type="submit" value="Make Human Move:"><input name="move" type="text"></input></form>'
    return ret

# Display Board
@app.route("/board.svg/")
def board():
    return Response(chess.svg.board(board=game.board, size=700), mimetype='image/svg+xml')


# Human Move
@app.route("/move/")
def move():
    print("ji")
    global message
    try:
        if (not game.turn) and (not game_over):
            move = request.args.get('move', default="")
            game.board.push_san(move)
            game.turn = 1
            message = "AI Turn"
    except Exception:
        traceback.print_exc()
        message = "Illegal Move"
    return main()


# # Make Ai’s Move
# @app.route("/dev/", methods=['POST'])
# def dev():
#     try:
#         aimove()
#     except Exception:
#         traceback.print_exc()
#     return main()



# New Game
@app.route("/game/", methods=['POST'])
def game_reset():
    game.board.reset()
    game.turn = 1
    return main()


# Undo
@app.route("/undo/", methods=['POST'])
def undo():
    try:
        game.board.pop()
    except Exception:
        traceback.print_exc()
    return main()

if __name__ == '__main__':
    server = "127.0.0.1"
    port_num = 5001
    webbrowser.open(f"http://{server}:{str(port_num)}/")
    app.run(host=server, port = port_num)