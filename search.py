import chess
from searchUtils import quiescence, movesOrder


transposition_table = {}
# This function computes the score assuming that both White and Black play the best moves
def alphaBeta(board: chess.Board, depth: int, alpha: int, beta: int, maximizing_player: bool):
    # Transposition Table Lookup
    board_hash = board._transposition_key()
    if board_hash in transposition_table:
        tt_depth, tt_score, tt_flag = transposition_table[board_hash]
        if tt_depth >= depth:
            if tt_flag == 'EXACT':
                return tt_score
            elif tt_flag == 'LOWERBOUND' and tt_score >= beta:
                return tt_score
            elif tt_flag == 'UPPERBOUND' and tt_score <= alpha:
                return tt_score

    # Base case: checkmate
    if board.is_checkmate():
        return -9999 if board.turn == chess.WHITE else 9999

    # Base case: stalemate, insufficient material, or repetition/draw
    if board.is_stalemate() or board.is_insufficient_material() or \
       board.can_claim_draw() or board.is_repetition(2) or \
       (hasattr(board, 'is_halfmoves') and board.is_halfmoves()):
        return 0

    # Base case: depth reached, evaluate the position
    if depth == 0:
        return quiescence(board, alpha, beta, maximizing_player)
        
    legalMoves = list(board.legal_moves)
    # Alpha is the best score of the moves for White
    original_alpha = alpha
    # Beta is the bes score of the moves for Black
    original_beta = beta

    if maximizing_player: # White
        max_eval = -9999
        for move in movesOrder(legalMoves, board):
            board.push(move)
            eval = alphaBeta(board, depth - 1, alpha, beta, False)
            board.pop()

            max_eval = max(max_eval, eval)
            alpha = max(alpha, eval)
            if beta <= alpha:
                break  # Alpha-Beta Pruning
                
        # TT Store
        flag = 'EXACT'
        if max_eval <= original_alpha:
            flag = 'UPPERBOUND'
        elif max_eval >= beta:
            flag = 'LOWERBOUND'
        transposition_table[board_hash] = (depth, max_eval, flag)
        
        return max_eval
    else: #Black
        min_eval = 9999
        for move in movesOrder(legalMoves, board):
            board.push(move)
            eval = alphaBeta(board, depth - 1, alpha, beta, True)
            board.pop()

            min_eval = min(min_eval, eval)
            beta = min(beta, eval)
            if beta <= alpha:
                break  # Alpha-Beta Pruning
                
        # TT Store
        flag = 'EXACT'
        if min_eval <= alpha:  # wait, min_eval <= original_alpha for upperbound? 
            flag = 'UPPERBOUND'
        elif min_eval >= original_beta:
            flag = 'LOWERBOUND'
        transposition_table[board_hash] = (depth, min_eval, flag)
        
        return min_eval

# This function allows the bot to choose the best move using the alphaBeta algorithm to evaluate moves
def getBestMove(board: chess.Board, depth: int):
    transposition_table.clear()  # Prevent memory bloat across turns
    bestMove = None
    whiteMove = board.turn == chess.WHITE 
    alpha = -9999
    beta = 9999

    if whiteMove:
        bestScore = -9999
        for move in movesOrder(list(board.legal_moves), board):
            board.push(move)
            score = alphaBeta(board, depth - 1, alpha, beta, False)
            board.pop()

            if score > bestScore:
                bestScore = score
                bestMove = move
            alpha = max(alpha, bestScore)
            if beta <= alpha:
                break
    else:
        bestScore = 9999
        for move in movesOrder(list(board.legal_moves), board):
            board.push(move)
            score = alphaBeta(board, depth - 1, alpha, beta, True)
            board.pop()

            if score < bestScore:
                bestScore = score
                bestMove = move
            beta = min(beta, bestScore)
            if beta <= alpha:
                break

    if bestMove:
        return bestMove.uci()
    return None
     

