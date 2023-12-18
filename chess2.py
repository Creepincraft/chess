import tkinter

class Chessboard(tkinter.Canvas):
    def __init__(self, master=None, **kwargs):
        super().__init__(master, **kwargs)
        self.pieces = {}  # Dictionary to store piece positions
        self.selected_piece = None
        self.current_turn = "white"  # Current turn, starting with white
        self.create_chessboard()
        self.create_pieces()

    def create_chessboard(self):
        # Create the chessboard grid
        for row in range(8):
            for col in range(8):
                color = "#EEEED2" if (row + col) % 2 == 0 else "#769656"
                self.create_rectangle(col * 50, row * 50, (col + 1) * 50, (row + 1) * 50, fill=color)

    def create_pieces(self):
        # Initial positions of chess pieces
        piece_layout = [
            ("R", "black"), ("N", "black"), ("B", "black"), ("Q", "black"), ("K", "black"), ("B", "black"), ("N", "black"), ("R", "black"),
            ("P", "black"), ("P", "black"), ("P", "black"), ("P", "black"), ("P", "black"), ("P", "black"), ("P", "black"), ("P", "black"),
            (" ", ""), (" ", ""), (" ", ""), (" ", ""), (" ", ""), (" ", ""), (" ", ""), (" ", ""),
            (" ", ""), (" ", ""), (" ", ""), (" ", ""), (" ", ""), (" ", ""), (" ", ""), (" ", ""),
            (" ", ""), (" ", ""), (" ", ""), (" ", ""), (" ", ""), (" ", ""), (" ", ""), (" ", ""),
            (" ", ""), (" ", ""), (" ", ""), (" ", ""), (" ", ""), (" ", ""), (" ", ""), (" ", ""),
            ("P", "white"), ("P", "white"), ("P", "white"), ("P", "white"), ("P", "white"), ("P", "white"), ("P", "white"), ("P", "white"),
            ("R", "white"), ("N", "white"), ("B", "white"), ("Q", "white"), ("K", "white"), ("B", "white"), ("N", "white"), ("R", "white")
        ]

        # Place pieces on the board
        for row in range(8):
            for col in range(8):
                index = row * 8 + col
                piece, color = piece_layout[index]
                if piece != " ":
                    self.place_piece(piece, color, col, row)

    def place_piece(self, piece, color, col, row):
        # Draw the piece on the board
        x0, y0 = col * 50 + 5, row * 50 + 5
        x1, y1 = x0 + 40, y0 + 40

        if piece == "K":
            self.create_oval(x0, y0, x1, y1, fill=color, outline="black", width=2, tags="piece")
        elif piece == "Q":
            self.create_rectangle(x0, y0, x1, y1, fill=color, outline="black", width=2, tags="piece")
        elif piece == "R":
            self.create_rectangle(x0, y0, x1, y1, fill=color, outline="black", width=2, tags="piece")
        elif piece == "B":
            self.create_polygon(x0 + 20, y0, x0, y1, x1, y1, outline="black", fill=color, width=2, tags="piece")
        elif piece == "N":
            self.create_polygon(x0, y0 + 20, x0 + 20, y0, x1, y0 + 20, x1 - 20, y1, outline="black", fill=color, width=2, tags="piece")
        elif piece == "P":
            self.create_oval(x0, y0, x1, y1, fill=color, outline="black", width=2, tags="piece")
        self.pieces[(col, row)] = (piece, color)

    def move_piece(self, start_col, start_row, end_col, end_row):
        # Move a piece from start to end position if it's a legal move
        if (end_col, end_row) in self.get_legal_moves(start_col, start_row):
            piece_info = self.pieces.pop((start_col, start_row))
            piece, color = piece_info
            self.place_piece(piece, color, end_col, end_row)
            self.current_turn = "white" if self.current_turn == "black" else "black"

    def delete_piece_at(self, col, row):
        # Delete a piece at a given position
        piece_id = self.find_closest(col * 50 + 25, row * 50 + 25)
        self.delete(piece_id)

    def get_legal_moves(self, start_col, start_row):
        # Returns legal moves for a given piece at start position
        # For simplicity, just returning all empty squares for now
        legal_moves = []
        piece, color = self.pieces[(start_col, start_row)]
        for row in range(8):
            for col in range(8):
                if self.pieces.get((col, row)) is None:
                    legal_moves.append((col, row))
        return legal_moves

    def on_square_click(self, event):
        # Handle click event on a chessboard square
        col = event.x // 50
        row = event.y // 50

        if self.selected_piece:
            start_col, start_row = self.selected_piece
            self.move_piece(start_col, start_row, col, row)
            self.selected_piece = None
            self.delete("selected_square")
        else:
            if (col, row) in self.pieces and self.pieces[(col, row)][1] == self.current_turn:
                self.selected_piece = (col, row)
                self.highlight_square(col, row)

    def highlight_square(self, col, row):
        # Highlight the selected square
        x0, y0 = col * 50, row * 50
        x1, y1 = x0 + 50, y0 + 50
        self.create_rectangle(x0, y0, x1, y1, outline="red", tags="selected_square")


class ChessApp:
    def __init__(self, root):
        self.root = root
        root.title("Chess Game")

        # Create Chessboard widget
        self.chessboard = Chessboard(root, width=400, height=400)
        self.chessboard.pack()

        # Bind square click event
        self.chessboard.bind("<Button-1>", self.chessboard.on_square_click)

# User Manual within comments
'''
    User Manual:
    
    - The game interface displays an 8x8 grid representing a chessboard. Each square represents a possible position for the chess pieces.
    
    - To start the game, run the code in a Python environment.
    
    - Interacting with the game:
        - Click on a piece to select it. The selected piece will be highlighted in red.
        - Click on the square where you want to move the selected piece. If it's a legal move, the piece will move to the selected square.
        - The game follows a turn-based system, starting with white. Only move pieces during your turn.
    
    - Ending the game:
        - This is a basic chess simulation. There is no checkmate or win condition implemented.
    
    - Closing the application:
        - Close the application window to end the game.
    
    - Understanding the code:
        - The code uses Tkinter for the graphical interface and basic logic to handle piece movement and board representation.
        - You can customize the code to enhance the game, implement checkmates, or improve the interface.
'''

if __name__ == "__main__":
    root = tkinter.Tk()
    app = ChessApp(root)
    root.mainloop()
