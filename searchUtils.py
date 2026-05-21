import chess
from evaluation import evaluateBoard, valueOfPiece

#This function orders moves by probability, which can improve pruning efficiency
def movesOrder(moves: list[chess.Move], board: chess.Board) -> list[chess.Move]:
    scoredMoves = []
    
    for move in moves:
        score = 0
        
        victimPiece = board.piece_type_at(move.to_square)
        if victimPiece is not None:
            attackPiece = board.piece_type_at(move.from_square)
            # prioritise capturing opponent's most valuable pieces with our least valuable pieces
            score = 10 * valueOfPiece[victimPiece] - valueOfPiece[attackPiece]
        
        #Promoting a pawn is likely to be good
        if move.promotion:
            score += valueOfPiece[move.promotion]
            
        scoredMoves.append((score, move))

    scoredMoves.sort(key=lambda x: x[0], reverse=True)
    return [x[1] for x in scoredMoves]

def quiescence(board: chess.Board, alpha: int, beta: int, maximizingPlayer: bool, q_depth: int = 0) -> int:
    """Quiescence search only considers captures to stabilize the evaluation."""
    # Stand-pat: evaluation of the current position without making a move
    stand_pat = evaluateBoard(board)

    # Hard limit on quiescence depth to prevent infinite explosion in open positions
    if q_depth > 4:
        return stand_pat
    
    if maximizingPlayer:
        if stand_pat >= beta:
            return beta
        alpha = max(alpha, stand_pat)
    else:
        if stand_pat <= alpha:
            return alpha
        beta = min(beta, stand_pat)

    # Only captures
    captures = list(board.generate_legal_captures())
    
    for move in movesOrder(captures, board):
        board.push(move)
        score = quiescence(board, alpha, beta, not maximizingPlayer, q_depth + 1)
        board.pop()

        if maximizingPlayer:
            if score >= beta:
                return beta
            alpha = max(alpha, score)
        else:
            if score <= alpha:
                return alpha
            beta = min(beta, score)

    return alpha if maximizingPlayer else beta
