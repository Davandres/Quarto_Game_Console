from ..models.board import Board
from ..models.ai import AI_level1, AI_level2
from ..utils.display import display_boards
from ..utils.file_io import export_history_to_csv
from colorama import Fore, Back, Style

class QuartoGame:
    PLAYER1 = "Player 1"
    PLAYER2 = "Player 2"
    TIE = "Tie"
    
    def __init__(self, player1_type="ai1", player2_type="ai2"):
        self.selected_piece = None
        self.game_board = Board("Game Board", False, 4, 4)
        self.storage_board = Board("Storage Board", True, 2, 8)
        self.turn = True  # True for player 1, False for player 2
        self.pick = True  # True for picking phase, False for placing phase
        self.move_history = []

        # Configuración de jugadores
        if player1_type == "ai1":
            self.player1 = AI_level1("AI Level 1 (Player 1)")
        elif player1_type == "ai2":
            self.player1 = AI_level2("AI Level 2 (Player 1)")
        
        if player2_type == "ai1":
            self.player2 = AI_level1("AI Level 1 (Player 2)")
        elif player2_type == "ai2":
            self.player2 = AI_level2("AI Level 2 (Player 2)")
            
        self.winner_name = None
        self.valid_moves = []

    def get_current_player(self):
        return self.player1 if self.turn else self.player2


    def play_ai_turn(self):
            current_player = self.get_current_player()
            
            try:
                if self.pick:
                    print(f"\n{Fore.YELLOW}{current_player.name} está seleccionando una pieza...")
                    
                    row, col = current_player.select(self)
                    if row == -1 or col == -1:
                        raise ValueError("Invalid selection")
                    
                    self.selected_piece = self.storage_board.get_piece(row, col)
                    print(f"{Fore.GREEN}Seleccionó la pieza en posición ({row}, {col}): {self.selected_piece.__repr__(verbose=True)}")
                    
                    self.storage_board.put_piece(0, row, col)
                    self.valid_moves = self.game_board.get_valid_moves()
                    
                    move_info = {
                        "player": current_player.name,
                        "action": "selected",
                        "piece": self.selected_piece.__repr__(verbose=True),
                        "position": None
                    }
                    self.move_history.append(move_info)
                else:
                    print(f"\n{Fore.YELLOW}{current_player.name} está colocando la pieza seleccionada...")
                    
                    row, col = current_player.select(self)
                    print(f"{Fore.GREEN}Colocó la pieza en posición ({row}, {col})")
                    
                    self.game_board.put_piece(self.selected_piece, row, col)
                    
                    move_info = {
                        "player": current_player.name,
                        "action": "placed",
                        "piece": self.selected_piece.__repr__(verbose=True),
                        "position": (row, col)
                    }
                    self.move_history.append(move_info)
                    
                    # Verificar ganador
                    if self.game_board.winner():
                        self.winner_name = current_player.name
                        print(f"\n{Back.GREEN}{Fore.WHITE} ¡{current_player.name} GANA LA PARTIDA! {Style.RESET_ALL}")
                    elif self.game_board.is_full():
                        self.winner_name = self.TIE
                        print(f"\n{Back.YELLOW}{Fore.BLACK} ¡EMPATE! {Style.RESET_ALL}")
                    
                    self.selected_piece = None
                
                # Cambiar turno
                self.pick = not self.pick
                if self.pick:
                    self.turn = not self.turn
                    
            except Exception as e:
                print(f"{Back.RED}Error durante el turno: {str(e)}{Style.RESET_ALL}")
                raise    


    def select_piece(self, row, col):
        if not (0 <= row < self.storage_board.rows and 0 <= col < self.storage_board.cols):
            print("Posición inválida. Intente nuevamente.")
            return False

        piece = self.storage_board.get_piece(row, col)
        if piece == 0:
            print("No hay pieza en esa posición. Intente nuevamente.")
            return False

        self.selected_piece = piece
        self.storage_board.put_piece(0, row, col)
        self.valid_moves = self.game_board.get_valid_moves()
        return True

    def place_piece(self, row, col):
        if not (0 <= row < self.game_board.rows and 0 <= col < self.game_board.cols):
            print("Posición inválida. Intente nuevamente.")
            return False

        if self.game_board.get_piece(row, col) != 0:
            print("Ya hay una pieza en esa posición. Intente nuevamente.")
            return False

        self.game_board.put_piece(self.selected_piece, row, col)
        
        # Registrar movimiento
        move_info = {
            "jugador": self.PLAYER1 if self.turn else self.PLAYER2,
            "pieza": self.selected_piece.__repr__(verbose=True),
            "posicion": (row, col)
        }
        self.move_history.append(move_info)
        
        # Check for winner
        if self.game_board.winner():
            self.winner_name = self.PLAYER1 if self.turn else self.PLAYER2
        elif self.game_board.is_full():
            self.winner_name = self.TIE
        
        self.selected_piece = None
        return True
    

    def change_turn(self):
        self.turn = not self.turn

    def change_pick_move(self):
        self.pick = not self.pick

    def winner(self):
        return self.winner_name

    def copy(self):
        """Crea una copia profunda del juego"""
        # Crear nueva instancia con los mismos tipos de jugador
        player1_type = "ai1" if isinstance(self.player1, AI_level1) else "ai2"
        player2_type = "ai1" if isinstance(self.player2, AI_level1) else "ai2"
        
        new_game = QuartoGame(player1_type, player2_type)
        new_game.selected_piece = self.selected_piece.copy() if self.selected_piece else None
        new_game.game_board = self.game_board.copy()
        new_game.storage_board = self.storage_board.copy()
        new_game.turn = self.turn
        new_game.pick = self.pick
        new_game.move_history = [move for move in self.move_history]
        new_game.winner_name = self.winner_name
        new_game.valid_moves = [move for move in self.valid_moves]
        return new_game
    
    def show_history(self):
        """Muestra el historial de movimientos formateado en una tabla"""
        if not hasattr(self, 'move_history') or not self.move_history:
            print("No hay historial de movimientos disponible")
            return
        
        try:
            # Encabezado
            print("\nHistorial de Movimientos:")
            print("-" * 80)
            print(f"{'Mov.':<6} | {'Jugador':<15} | {'Acción':<10} | {'Pieza':<40} | {'Posición'}")
            print("-" * 80)
            
            # Filas
            for i, move in enumerate(self.move_history, start=1):
                pieza = str(move.get('piece', 'N/A')).replace(", ", " | ")
                pos = (f"({move['position'][0]}, {move['position'][1]})" 
                    if move.get('position') else "N/A")
                print(f"{i:<6} | {move.get('player', 'N/A'):<15} | "
                    f"{move.get('action', 'N/A'):<10} | {pieza:<40} | {pos}")
        
        except Exception as e:
            print(f"Error mostrando historial: {str(e)}")

    def export_history_to_csv(self, match_number=None):
        """Exporta el historial a CSV"""
        from ..utils.file_io import export_history_to_csv
        return export_history_to_csv(self, match_number)

    def reset(self):
        self.__init__(self.ai1.name, self.ai2.name)

    