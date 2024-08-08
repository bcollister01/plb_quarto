"""
This is a working tic tac toe implementation that is playable as its own game by running
this script.

Created by Ben Collister and Christine Cartwright
Using the guide https://realpython.com/tic-tac-toe-python/

Selection_grid is where we select our pieces and is pre-filled in at the start with all of the pieces and action on this grid should trigger the player switch.
Play_grid is where we put down a selected piece.
Ideal is to have chosen_grid which shows the chosen piece.
Can we move the board so that it is side by side with a space?
We have commented out _highlight_cells when someone has won as this was leading to a pyimage not found error.
Pack is putting them all side by side - workable.
Alternative is grid - but it’s making every row column the same width and we need them to find a way to make it closer together.
create_board_display is just the message at the top so it does not need a play and selection version.

Next time: prefill one board with all of the pieces.
"""

## Issue with buttons collapsing if a row or column is completed

import tkinter as tk #Currently 8.6
from tkinter import font
from itertools import cycle
from typing import NamedTuple

class Player(NamedTuple):
    # How to do as a 3D shape rather than flat shape
    label: str
    image: tk.PhotoImage
    color: str

class Move(NamedTuple):
    row: int
    col: int
    label: str = ""

# root = tk.Tk()
BOARD_SIZE = 4
#Need to change default player - technically one person doesn't have label

    
class QuartoGame:
    def __init__(self, board_size=BOARD_SIZE):
        self.board_size = board_size
        self.winner_combo = []
        self._current_moves = []
        self._has_winner = False
        self._winning_combos = []
        self._setup_board()
    
    def _setup_board(self):
        self._current_moves = [
            [Move(row, col) for col in range(self.board_size)]
            for row in range(self.board_size)
        ]
        self._winning_combos = self._get_winning_combos()
        
    def _get_winning_combos(self):
        rows = [
            [(move.row, move.col) for move in row]
            for row in self._current_moves
        ]
        columns = [list(col) for col in zip(*rows)]
        first_diagonal = [row[i] for i, row in enumerate(rows)]
        second_diagonal = [col[j] for j, col in enumerate(reversed(columns))]
        return rows + columns + [first_diagonal, second_diagonal]
    
    def is_valid_move(self, move):
        """Return True if move is valid, and False otherwise."""
        row, col = move.row, move.col
        move_was_not_played = self._current_moves[row][col].label == ""
        no_winner = not self._has_winner
        return no_winner and move_was_not_played
    
    def process_move(self, move):
        """Process the current move and check if it's a win."""
        row, col = move.row, move.col
        self._current_moves[row][col] = move
        for combo in self._winning_combos:
            #Set logic may not work for ours
            # [1,1,0,0], [0,1,0,1],...
            # Sum the arrays in the line
            # Check for any element being 0 or 4 (min/max statement on array)
            # Pascal 1,4,6,4,1 in terms of shared attributes (0 up to 4)
            results = set(
                self._current_moves[n][m].label
                for n, m in combo
            )
            is_win = (len(results) == 1) and ("" not in results)
            if is_win:
                self._has_winner = True
                self.winner_combo = combo
                break
                
    def has_winner(self):
        """Return True if the game has a winner, and False otherwise."""
        return self._has_winner
    
    def is_tied(self):
        """Return True if the game is tied, and False otherwise."""
        no_winner = not self._has_winner
        played_moves = (
            # Has the label of every cell been updated from empty i.e. piece played
            move.label for row in self._current_moves for move in row
        )
        return no_winner and all(played_moves)

    def reset_game(self):
        """Reset the game state to play again."""
        for row, row_content in enumerate(self._current_moves):
            for col, _ in enumerate(row_content):
                row_content[col] = Move(row, col)
        self._has_winner = False
        self.winner_combo = []

# Maybe second board for pieces - takes a piece off and sets it to empty
# Labels above each board
# Messages which tell user which board they must press button on at each stage
# For very first move, potentially already have randomly chosen piece selected
# for player 1 to put down
    
class QuartoBoard(tk.Tk):
    def __init__(self, game):
        super().__init__()
        self.title("Quarto Game")
        img = tk.PhotoImage(file="pieces/cyan_cuboid_small_striped.png").subsample(5)
        img2 = tk.PhotoImage(file="pieces/orange_cuboid_small_striped.png").subsample(5)
        players = (
            Player(label="X", image = img, color="blue"),
            Player(label="O", image = img2, color="green"),
        )
        self._players = cycle(players)
        self._cells = {}
        self._game = game
        self.current_player = next(self._players)
        self._create_menu()
        self._create_text_display()
        selection_board = self._create_selection_board_grid()
        # play_board = self._create_play_board_display()
        play_board = self._create_play_board_grid()
        # self.blank = tk.PhotoImage()

    def _create_text_display(self):
        display_frame = tk.Frame(master=self)
        # display_frame.pack(side=tk.TOP) #.pack(side=tk.LEFT)#frame fills width if window resized
        display_frame.grid(row=0, column=0, rowspan=1)
        self.display = tk.Label(
              master=display_frame, #label needs to live in frame
              text="Ready?",
              font=font.Font(size=28, weight="bold"),
        )
        self.display.pack()

    # def _create_play_board_display(self):
    #     display_frame = tk.Frame(master=self)
    #     display_frame.pack(side=tk.RIGHT) #frame fills width if window resized
    #     self.display = tk.Label(
    #           master=display_frame, #label needs to live in frame
    #           text="Test",
    #           font=font.Font(size=28, weight="bold"),
    #     )
    #     self.display.pack()


    def _create_selection_board_grid(self):
        grid_frame = tk.Frame(master=self) #Hold the game grid cells
        # grid_frame.pack(side=tk.LEFT)
        grid_frame.grid(row=1, column=0, rowspan=3)
        grid_frame.pack_propagate(0)
        for row in range(self._game.board_size):
            self.rowconfigure(row, weight=1, minsize=50, uniform='row')
            self.columnconfigure(row, weight=1, minsize=75, uniform='row')
            for col in range(self._game.board_size):
                button = tk.Button(
                    master=grid_frame,
                    image=tk.PhotoImage(), #self.blank_image,
                    font=font.Font(size=36, weight="bold"),
                    fg="black",
                    width=100,
                    height=100,
                    highlightbackground="lightblue",
                )
                self._cells[button] = (row, col)
                button.bind("<ButtonPress-1>", self.play)
                button.grid(
                    row=row,
                    column=col,
                    padx=5,
                    pady=5,
                    sticky="nsew"
                )
                button.grid_propagate(False)
                
    def _create_play_board_grid(self):
        grid_frame = tk.Frame(master=self) #Hold the game grid cells
        # grid_frame.pack(side=tk.RIGHT)
        grid_frame.grid(row=1, column=2, rowspan=3)
        grid_frame.pack_propagate(0)
        for row in range(self._game.board_size):
            self.rowconfigure(row, weight=1, minsize=50, uniform='row')
            self.columnconfigure(row, weight=1, minsize=75, uniform='row')
            for col in range(self._game.board_size):
                button = tk.Button(
                    master=grid_frame,
                    image=tk.PhotoImage(), #self.blank_image,
                    font=font.Font(size=36, weight="bold"),
                    fg="black",
                    width=100,
                    height=100,
                    highlightbackground="lightblue",
                )
                self._cells[button] = (row, col)
                button.bind("<ButtonPress-1>", self.play)
                button.grid(
                    row=row,
                    column=col,
                    padx=5,
                    pady=5,
                    sticky="nsew"
                )
                button.grid_propagate(False)

    def toggle_player(self):
        """Return a toggled player."""
        self.current_player = next(self._players)
    
    # The .mainloop() method on the Tk class runs what’s known as the application’s 
    # main loop or event loop. This is an infinite loop in which all the GUI events happen.
    def play(self, event):
        """Handle a player's move."""
        clicked_btn = event.widget
        row, col = self._cells[clicked_btn]
        move = Move(row, col, self.current_player.label)
        if self._game.is_valid_move(move): # Maybe show error message to user if False?
            self._update_button(clicked_btn)
            self._game.process_move(move)
            # Maybe check winner first rather than tied
            # Maybe only check winner after row/col/diagonal was filled
            # Technically first board_size - 1 moves don't need check
            if self._game.is_tied():
                self._update_display(msg="Tied game!", color="red")
            elif self._game.has_winner():
                # self._highlight_cells()
                msg = f'Player "{self.current_player.label}" won!'
                color = self.current_player.color
                self._update_display(msg, color)
            else:
                self.toggle_player()
                msg = f"{self.current_player.label}'s turn"
                self._update_display(msg)
                
    def _update_button(self, clicked_btn):
        # Need to set to a 3D image for us
        clicked_btn.config(image=self.current_player.image)
        #clicked_btn.config(text=self.current_player.label)
        #clicked_btn.config(fg=self.current_player.color)
        
    def _update_display(self, msg, color="black"):
        self.display["text"] = msg
        self.display["fg"] = color
        
    def _highlight_cells(self):
        for button, coordinates in self._cells.items():
            if coordinates in self._game.winner_combo:
                button.config(highlightbackground="red")
                
    def _create_menu(self):
        menu_bar = tk.Menu(master=self)
        self.config(menu=menu_bar)
        file_menu = tk.Menu(master=menu_bar)
        file_menu.add_command(
            label="Play Again",
            command=self.reset_board
        )
        file_menu.add_separator()
        file_menu.add_command(label="Exit", command=quit)
        menu_bar.add_cascade(label="File", menu=file_menu)
        
    def reset_board(self):
        """Reset the game's board to play again."""
        self._game.reset_game()
        self._update_display(msg="Ready?")
        # Reset all the buttons
        for button in self._cells.keys():
            button.config(highlightbackground="lightblue")
            button.config(text="")
            button.config(fg="black")

def main():
    """Create the game's board and run its main loop."""
    game = QuartoGame()
    board = QuartoBoard(game)
    board.resizable(False, False)
    board.mainloop()

if __name__ == "__main__":
    main()