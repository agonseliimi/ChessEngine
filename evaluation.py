import chess
from tables import *

# Dictionary mapping piece types to their relative material values in centipawns.
# These values are exported for use in search.py for Move Ordering heuristics.
valueOfPiece = {
    chess.PAWN:   100,
    chess.KNIGHT: 300,
    chess.BISHOP: 310,
    chess.ROOK:   500,
    chess.QUEEN:  900,
    chess.KING:     0,
}

# Pre-build lookup tuples for the hot evaluation loop.
# Using tuples instead of dictionaries significantly speeds up the evaluation 
# by avoiding hashing overhead during the millions of iterations in the search tree.
_PIECE_TYPES = (chess.PAWN, chess.KNIGHT, chess.BISHOP, chess.ROOK, chess.QUEEN, chess.KING)
_PIECE_VALUES = (100, 300, 310, 500, 900, 0)

_MG_TABLES = (pawn_mg_table, knight_table, bishop_table, rook_table, queen_table, king_mg_table)
_EG_TABLES = (pawn_eg_table, knight_table, bishop_table, rook_table, queen_table, king_eg_table)


def evaluateBoard(board: chess.Board) -> int:
    """
    Optimized board evaluation using bitboard iteration.
    Returns positive for White advantage, negative for Black.
    """
    # Count the total number of pieces on the board to detect the endgame phase.
    # If the piece count drops to 12 or fewer, we transition from the middlegame (_MG_TABLES)
    # to the endgame (_EG_TABLES) positional piece-square tables, as piece values and optimal
    # placements (especially for the King) shift significantly during the late game.
    piece_count = bin(board.occupied).count('1')
    tables = _EG_TABLES if piece_count <= 12 else _MG_TABLES

    score = 0

    for i in range(6):
        pt = _PIECE_TYPES[i]
        val = _PIECE_VALUES[i]
        tbl = tables[i]

        # We use the bitwise XOR operator (^ 56) to vertically flip the board index for White pieces.
        # Since the piece-square tables are defined from Black's perspective (index 0 is a8, index 63 is h1),
        # XORing the square index with 56 (binary 111000) efficiently maps White's ranks to the correct 
        # mirrored position in the table without requiring a separate set of arrays.
        for sq in board.pieces(pt, chess.WHITE):
            score += val + tbl[sq ^ 56]

        # For Black pieces, we use the square index directly without mirroring, 
        # since the piece-square tables are already oriented from Black's perspective.
        for sq in board.pieces(pt, chess.BLACK):
            score -= val + tbl[sq]

    return score