import chess
import chess.polyglot
from .piece_values import *
import os

path = os.path.dirname(os.path.abspath(__file__))

class Chess_game:
    def __init__(self, plies) -> None:
        self.board = chess.Board()
        self.winner = None
        self.turn = 1 # white, min player
        self.plies = plies #depth of looking, deeper the better but slower
        self.counts = 0 #prevents inf loops


    def auto_play_game(self):

        while True:
            self.counts += 1
            if self.turn:
                print("White Turn")
            else:
                print("Black Turn")
            move = self.make_move()
            if self.winner != None or not move or self.counts > 1000:
                break
            self.board.push(move)
            if self.turn:
                self.turn = 0
            else:
                self.turn = 1
            board_string = str(self.board)
            temp_string = ''
            number = 1
            for i in range(len(board_string)):
                if board_string[i] == '\n':
                    temp_string = f"{temp_string} {str(number)}\n{str(number+1)} "
                    number += 1
                else:
                    temp_string = temp_string + board_string[i]
            temp_string = f"1 {temp_string} 8"
            board_string = f"  a b c d e f g h  \n{temp_string}\n  a b c d e f g h   \n{'='*20}"
            print(board_string)

        
        return self.winner
        


    def make_move(self):
        #check win first
        if self.board.is_checkmate():
            if self.turn:
                self.winner = "White"
            else:
                self.winner = "Black"
            return 0
        if self.board.is_stalemate():
            self.winner = "Stalemate"
            return 0
        if self.board.is_insufficient_material():
            self.winner = "Stalemate"
            return 0
        try:
            #Reading from openers
            move = chess.polyglot.MemoryMappedReader(f"{path}/books/human.bin").weighted_choice(self.board).move
            return move
        except:
            #minimax alpha beta
            if self.turn == 1:
                move = self.min_value( self.plies, float('-inf'),float('inf'))[1]
            else:
                move = self.max_value( self.plies, float('-inf'),float('inf'))[1]
            return move
    
    def min_value(self, plies : int, alpha : int, beta : int):
        if plies == 0:
            return self.evaluate_board(), None
        if self.board.is_checkmate():
            return 9999, None
        if self.board.is_stalemate():
            return 0, None
        if self.board.is_insufficient_material():
            return 0, None
        best : int = float('inf')
        final_move = None
        # get all legal moves and search to find best one for min player
        legal_moves = self.board.legal_moves
        for move in legal_moves:
            self.board.push(move)
            value = self.max_value(plies-1, alpha, beta)[0]
            self.board.pop()
            if value < best:
                best = value
                beta = min(beta, value)
                final_move = move
            if value <= alpha:
                return value, final_move
        return best, final_move
    
    
    def max_value(self, plies : int, alpha : int, beta : int):
        if plies == 0:
            return self.evaluate_board(), None
        if self.board.is_checkmate():
            return -9999, None
        if self.board.is_stalemate():
            return 0, None
        if self.board.is_insufficient_material():
            return 0, None
        best : int = float('-inf')
        final_move = None
        # get all legal moves and search to find best one for max player
        legal_moves = self.board.legal_moves
        for move in legal_moves:
            self.board.push(move)
            value = self.min_value(plies-1, alpha, beta)[0]
            self.board.pop()
            if value > best:
                best = value
                alpha = max(alpha, value)
                final_move = move
            if value >= beta:
                return value, final_move
        return best, final_move
    


    def evaluate_board(self):
        '''
        White wants to have a lower score
        '''
        if self.board.is_checkmate():
            if self.turn:
                return -9999
            else:
                return 9999
        if self.board.is_stalemate():
                return 0
        if self.board.is_insufficient_material():
                return 0
        counts = {'num_wp':len(self.board.pieces(chess.PAWN, chess.WHITE)),
        'num_bp':len(self.board.pieces(chess.PAWN, chess.BLACK)),
        'num_wn':len(self.board.pieces(chess.KNIGHT, chess.WHITE)),
        'num_bn':len(self.board.pieces(chess.KNIGHT, chess.BLACK)),
        'num_wb':len(self.board.pieces(chess.BISHOP, chess.WHITE)),
        'num_bb':len(self.board.pieces(chess.BISHOP, chess.BLACK)),
        'num_wr':len(self.board.pieces(chess.ROOK, chess.WHITE)),
        'num_br':len(self.board.pieces(chess.ROOK, chess.BLACK)),
        'num_wq':len(self.board.pieces(chess.QUEEN, chess.WHITE)),
        'num_bq':len(self.board.pieces(chess.QUEEN, chess.BLACK)),
        'num_bk':len(self.board.pieces(chess.KING, chess.BLACK)),
        'num_wk':len(self.board.pieces(chess.KING, chess.WHITE))}
        piece_score = 0
        for key in counts:
            multiplier = 1
            if key[-2] == 'w':
                multiplier = -1
            piece_score += individual_piece_values[key[-1]]*counts[key]*multiplier
        
        pst_score = 0
        pst_score += -sum([pawntable[i] for i in self.board.pieces(chess.PAWN, chess.WHITE)]) + sum([pawntable[chess.square_mirror(i)]for i in self.board.pieces(chess.PAWN, chess.BLACK)])

        pst_score += -sum([knightstable[i] for i in self.board.pieces(chess.KNIGHT, chess.WHITE)])+ sum([knightstable[chess.square_mirror(i)]
                                for i in self.board.pieces(chess.KNIGHT, chess.BLACK)])
        pst_score += -sum([bishopstable[i] for i in self.board.pieces(chess.BISHOP, chess.WHITE)])+ sum([bishopstable[chess.square_mirror(i)]
                                for i in self.board.pieces(chess.BISHOP, chess.BLACK)])
        pst_score += -sum([rookstable[i] for i in self.board.pieces(chess.ROOK, chess.WHITE)]) + sum([rookstable[chess.square_mirror(i)]
                            for i in self.board.pieces(chess.ROOK, chess.BLACK)])
        pst_score += -sum([queenstable[i] for i in self.board.pieces(chess.QUEEN, chess.WHITE)]) + sum([queenstable[chess.square_mirror(i)]
                                for i in self.board.pieces(chess.QUEEN, chess.BLACK)])
        #Future implementation the second kings square
        pst_score += -sum([kingstable[i] for i in self.board.pieces(chess.KING, chess.WHITE)]) + sum([kingstable[chess.square_mirror(i)]
                            for i in self.board.pieces(chess.KING, chess.BLACK)])
        
        return piece_score + pst_score