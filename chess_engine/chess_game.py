import chess
import chess.polygot
from piece_values import *


class Chess_game:
    def __init__(self) -> None:
        self.board = chess.Board()
        self.winner = None
        self.turn = 1
    def start_game(self):

        
        return self.winner

    def make_move(self):
        try:
            
            move = chess.polyglot.MemoryMappedReader("./books/human.bin").weighted_choice(self.board).move
            return move
        except:
            
            pass
    
    def evaluate_board(self):
        '''
        White wants to have a lower score
        '''
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
        pst_score += -sum([pawntable[i] for i in self.board.pieces(chess.PAWN, chess.WHITE)]) + sum([-pawntable[chess.square_mirror(i)]for i in self.board.pieces(chess.PAWN, chess.BLACK)])

        pst_score += -sum([knightstable[i] for i in self.board.pieces(chess.KNIGHT, chess.WHITE)])+ sum([-knightstable[chess.square_mirror(i)]
                                for i in self.board.pieces(chess.KNIGHT, chess.BLACK)])
        pst_score += -sum([bishopstable[i] for i in self.board.pieces(chess.BISHOP, chess.WHITE)])+ sum([-bishopstable[chess.square_mirror(i)]
                                for i in self.board.pieces(chess.BISHOP, chess.BLACK)])
        pst_score += -sum([rookstable[i] for i in self.board.pieces(chess.ROOK, chess.WHITE)]) + sum([-rookstable[chess.square_mirror(i)]
                            for i in self.board.pieces(chess.ROOK, chess.BLACK)])
        pst_score += -sum([queenstable[i] for i in self.board.pieces(chess.QUEEN, chess.WHITE)]) + sum([-queenstable[chess.square_mirror(i)]
                                for i in self.board.pieces(chess.QUEEN, chess.BLACK)])
        #Future implementation the second kings square
        pst_score += -sum([kingstable[i] for i in self.board.pieces(chess.KING, chess.WHITE)]) + sum([-kingstable[chess.square_mirror(i)]
                            for i in self.board.pieces(chess.KING, chess.BLACK)])
        
        return piece_score + pst_score