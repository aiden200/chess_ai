import discord
from discord_token import *
from chess_engine.chess_game import Chess_game
import time
import chess, chess.svg


in_game = False
game_player = None
start_time = None
game = None

def activate_bot():

    intents = discord.Intents.default()
    intents.message_content = True
    # intents = discord.Intents.all()

    client = discord.Client(intents=intents)

    @client.event
    async def on_ready():
        print(f'We have logged in as {client.user}')

    @client.event
    async def on_message(message):
        global in_game, game_player, end_time, game

        chess_channel = client.get_channel(1083081699363139774)
        if message.channel == chess_channel and message.content[0] == "!":

            command = message.content
            player = message.author


            if command == "!help":
                help_text = '''
                    Instructions:\n
                    Only one player can play against the bot. There will be 10 minutes worth of gametime.\n
                    to make a move, type in ![move]. For example, if you want to move a pawn from e2 to e4, type "!e2e4".'''
                await chess_channel.send(help_text)



            if in_game and end_time-time.time() < 0:
                await chess_channel.send(f'ran out of time with player {game_player}')
                game_player = None
                in_game = False

            if command[:6] == "!start" and not in_game:
                try:
                    plies = 4
                    if len(command) == 8 and int(command[7]) <= 4:
                        plies = int(command[7])
                    await chess_channel.send(f'Starting chess game with {player} with difficulty at {plies}')
                    end_time = time.time() + 600
                    game = Chess_game(plies)
                    # embed = discord.Embed()
                    # a = chess.svg.board(board=game.board, size=700)
                    # embed.description = a
                    # await chess_channel.send(a)
                    game_player = player
                    in_game = True

                except Exception:
                    await chess_channel.send("Incorrect input, please type in correct input to start game. Ex: '!start 4'")
            else:
                await chess_channel.send(f'Currently in game with {game_player}. {round(end_time - time.time(), 0)} seconds remainig')
            

            if in_game and message.author == game_player:
                if command == "!moves":
                    await chess_channel.send(game.board.legal_moves)
                send_string = f'\nTime remaning: {round(end_time - time.time(), 0)}\n'
                try:
                    game.board.push_san(command[1:])
                    if game.board.is_checkmate():
                        send_string = f"You won!"
                        in_game = False
                    if game.board.is_stalemate():
                        send_string = "Stalemate"
                    if game.board.is_insufficient_material():
                        send_string = "Stalemate"
                    if game.turn == 1:
                        game.turn = 0
                    else:
                        game.turn = 1
                    move = game.make_move()
                    if game.turn == 1:
                        game.turn = 0
                    else:
                        game.turn = 1
                    if move == 0:
                        send_string = f"Winner is {game.winner}!"
                        in_game = False
                    else:
                        game.board.push(move)
                        send_string = f"{send_string}Your move: {command[1:]}\nAI move: {move}\n"
                        number = 8
                        board_string = str(game.board)
                        temp_string = ''
                        for i in range(len(board_string)):
                            if board_string[i] == '\n':
                                temp_string = f"{temp_string} {str(number)}\n{str(number-1)} "
                                number -= 1
                            else:
                                temp_string = temp_string + board_string[i]
                        temp_string = f"8 {temp_string} 1"
                        board_string = f"`  a b c d e f g h  \n{temp_string}\n  a b c d e f g h   `\n{'='*20}"
                        board_string = board_string.replace(".","-")
                        send_string = f"{send_string}{board_string}"
                    await chess_channel.send(send_string)
                except Exception as e:
                    number = 8
                    board_string = str(game.board)
                    temp_string = ''
                    for i in range(len(board_string)):
                        if board_string[i] == '\n':
                            temp_string = f"{temp_string} {str(number)}\n{str(number-1)} "
                            number -= 1
                        else:
                            temp_string = temp_string + board_string[i]
                    temp_string = f"8 {temp_string} 1"
                    board_string = f"`  a b c d e f g h  \n{temp_string}\n  a b c d e f g h   `\n{'='*20}"
                    board_string = board_string.replace(".","-")
                    print(f"Failed to move in chess with exception {e}")
                    await chess_channel.send(f"{send_string}Illegal move, try again.\n{board_string}")







    

    client.run(token)


activate_bot()