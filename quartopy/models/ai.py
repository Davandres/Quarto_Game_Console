import random

class AI_level1:
    def __init__(self, name):
        self.name = name

    def select(self, game):
        if game.pick:
            # Pick a random piece from storage
            valid_moves = game.storage_board.get_valid_moves()
            if not valid_moves:
                return (0, 0)
            return random.choice(valid_moves)
        else:
            # Place the piece randomly on the game board
            valid_moves = game.game_board.get_valid_moves()
            return random.choice(valid_moves) if valid_moves else (0, 0)

class AI_level2:
    def __init__(self, name):
        self.name = name

    def select(self, game):
        if game.pick:
            # Try to pick a piece that doesn't give the opponent an immediate win
            valid_moves = game.storage_board.get_valid_moves()
            
            # Try to find a safe piece (one that won't give opponent a win)
            safe_moves = []
            for row, col in valid_moves:
                piece = game.storage_board.get_piece(row, col)
                game_copy = game.copy()
                game_copy.selected_piece = piece.copy()
                game_copy.pick = False  # Now it's opponent's turn to place
                
                # Check if opponent can win with this piece
                opponent_can_win = False
                for r in range(game_copy.game_board.rows):
                    for c in range(game_copy.game_board.cols):
                        if game_copy.game_board.get_piece(r, c) == 0:
                            temp_game = game_copy.copy()
                            temp_game.game_board.put_piece(temp_game.selected_piece.copy(), r, c)
                            if temp_game.game_board.winner():
                                opponent_can_win = True
                                break
                    if opponent_can_win:
                        break
                
                if not opponent_can_win:
                    safe_moves.append((row, col))
            
            # If safe moves exist, choose randomly from them
            if safe_moves:
                return random.choice(safe_moves)
            
            # Otherwise, choose randomly from all valid moves
            return random.choice(valid_moves) if valid_moves else (0, 0)
        else:
            # First check for winning moves
            for row in range(game.game_board.rows):
                for col in range(game.game_board.cols):
                    if game.game_board.get_piece(row, col) == 0:
                        game_copy = game.copy()
                        game_copy.game_board.put_piece(game_copy.selected_piece.copy(), row, col)
                        if game_copy.game_board.winner():
                            return (row, col)
            
            # No winning move, place randomly
            valid_moves = game.game_board.get_valid_moves()
            return random.choice(valid_moves) if valid_moves else (0, 0)