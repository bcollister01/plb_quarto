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
Piece indexing:
colour, shape, size, design
cyan=0, orange=1,
cuboid=0, cylinder=1, 
small=0, tall=1, 
plain=0, striped=1, 

Grid positions:
0 1 2 3
4 5 6 7 
8 9 10 11
12 13 14 15

0000 0001 0010 0011
0100

_tkinter.TclError: couldn't recognize data in image file "pieces/.ipynb_checkpoints" - 
just make sure this file is deleted, may have been accidentally created, use ls -al to check

Next time: 
Working out opening: randomly selecting piece to start.

Select from left board to put into right board. Need a one square grid in the middle to show
piece selected and remove from left board.

Don't know if it will handle last move right where player only plays piece and doesn't select
- end game functions may handle it automatically? Should work but not 100%

The middle grid (selection made board_grid) does not have to be a button as users should not interact with it.
It should update as part of the logic when selection grid is clicked.

Start game function maybe not needed - play function should switch player after turn 1

Later extensions: Work out how to reimplement reset game again.

"""

## Issue with buttons collapsing if a row or column is completed

import os
import tkinter as tk #Currently 8.6
from tkinter import font
from itertools import cycle
from typing import NamedTuple
import random

class Player(NamedTuple):
    # How to do as a 3D shape rather than flat shape
    label: str
    color: str
    #image: tk.PhotoImage

class Move(NamedTuple):
    row: int
    col: int
    board: int #1 for selection board, 2 for play board
    label: str = "" #Can we put 0000, 0001, .... here?

# root = tk.Tk()
BOARD_SIZE = 4
#Need to change default player - technically one person doesn't have label

    
class QuartoGame:
    def __init__(self, board_size=BOARD_SIZE):
        self.board_size = board_size
        self.winner_combo = []
        self._selection_grid_current_moves = []
        self.total_selections = 0
        self.total_plays = 0
        self._play_grid_current_moves = []
        self._has_winner = False
        self._winning_combos = []
        self._setup_selection_board()
        self._setup_play_board()
    
    def _setup_selection_board(self):
        self._selection_grid_current_moves = [
            [Move(row, col, 1) for col in range(self.board_size)]
            for row in range(self.board_size)
        ]

    def _setup_play_board(self):
        self._play_grid_current_moves = [
            [Move(row, col, 2) for col in range(self.board_size)]
            for row in range(self.board_size)
        ]
        self._winning_combos = self._get_winning_combos()
        
    def _get_winning_combos(self):
        rows = [
            [(move.row, move.col) for move in row]
            for row in self._play_grid_current_moves
        ]
        columns = [list(col) for col in zip(*rows)]
        first_diagonal = [row[i] for i, row in enumerate(rows)]
        second_diagonal = [col[j] for j, col in enumerate(reversed(columns))]
        return rows + columns + [first_diagonal, second_diagonal]
    
    def is_valid_move_selection_grid(self, move):
        """Return True if move is valid, and False otherwise."""
        row, col = move.row, move.col
        move_was_not_played = self._selection_grid_current_moves[row][col].label == ""
        return move_was_not_played

    def is_valid_move_play_grid(self, move):
        """Return True if move is valid, and False otherwise."""
        row, col = move.row, move.col
        move_was_not_played = self._play_grid_current_moves[row][col].label == ""
        no_winner = not self._has_winner
        return no_winner and move_was_not_played

    def is_valid_grid_selected(self, move):
        """Return True if right board selected, return False if wrong board"""
        if self.total_selections == self.total_plays:
            if move.board == 1:
                return True
            else:
                return False         
        else:
            if move.board == 2:
                return True
            else:
                return False
    
    def process_selection_move(self, move):
        """Process the current selection move.
        """
        row, col = move.row, move.col
        self._selection_grid_current_moves[row][col] = move
        self.total_selections = self.total_selections + 1
    
    def process_play_move(self, move, piece_number):
        """Process the current move and check if it's a win."""
        row, col = move.row, move.col
        self._play_grid_current_moves[row][col] = move
        self.total_plays = self.total_plays + 1
        for combo in self._winning_combos:
            #Set logic may not work for ours
            # [1,1,0,0], [0,1,0,1],...
            # Sum the arrays in the line
            # Check for any element being 0 or 4 (min/max statement on array)
            # Pascal 1,4,6,4,1 in terms of shared attributes (0 up to 4)
            results = set(
                self._play_grid_current_moves[n][m].label
                for n, m in combo
            )
            # now checking if there is a matching characeristic on pieces
            if (len(results) == 4) and ("" not in results):
                results2 = []
                for i in range(4):
                    count = 0 
                    for n, m in combo:
                        count = count + int(str(self._play_grid_current_moves[n][m].label)[i])
                    results2.append(count)
            else:
                continue
                    
                
            is_win = (0 in results2 or 4 in results2)
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
            move.label for row in self._play_grid_current_moves for move in row
        )
        return no_winner and all(played_moves)

    # def reset_game(self):
    #     """Reset the game state to play again."""
    #     for row, row_content in enumerate(self._current_moves):
    #         for col, _ in enumerate(row_content):
    #             row_content[col] = Move(row, col)
    #     self._has_winner = False
    #     self.winner_combo = []

# Maybe second board for pieces - takes a piece off and sets it to empty
# Labels above each board
# Messages which tell user which board they must press button on at each stage
# For very first move, potentially already have randomly chosen piece selected
# for player 1 to put down
    
class QuartoBoard(tk.Tk):
    def __init__(self, game):
        super().__init__()
        self.title("Quarto Game")

        path = os.getcwd()
        files = os.listdir(os.path.join(path, 'pieces/'))
        file_list = sorted([f"pieces/{f}" for f in files if f.endswith('.png')])
        img_list = []
        # subsample affects image size - small numbers make it bigger
        for i in file_list:
            img_list.append(tk.PhotoImage(file=i).subsample(10))
            
        img = tk.PhotoImage(file="pieces/cyan_cuboid_small_striped.png").subsample(5)
        img2 = tk.PhotoImage(file="pieces/orange_cuboid_small_striped.png").subsample(5)
        players = (
            #Player(label="X", image = img_list[0], color="blue"),
            #Player(label="O", image = img2, color="green"),
            Player(label="X", color="blue"),
            Player(label="O", color="green"),
        )
        self._players = cycle(players)
        self._cells = {}
        self._game = game
        self.current_player = next(self._players)
        self._create_menu()
        self._create_text_display()
        self.img_list = img_list
        selection_board = self._create_selection_board_grid()
        selection_made_board = self._create_selection_made_board_grid()
        # play_board = self._create_play_board_display()
        play_board = self._create_play_board_grid()
      

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
                    image=self.img_list[row * 4 + col], #self.blank_image,
                    font=font.Font(size=36, weight="bold"),
                    fg="black",
                    width=100,
                    height=100,
                    highlightbackground="lightblue",
                )
                self._cells[button] = (row, col, 1)
                button.bind("<ButtonPress-1>", self.play)
                button.grid(
                    row=row,
                    column=col,
                    padx=5,
                    pady=5,
                    sticky="nsew"
                )
                button.grid_propagate(False)

    def _create_selection_made_board_grid(self):
        """1x1 grid to hold piece selected by player from left board to put in right board"""
        grid_frame = tk.Frame(master=self) #Hold the game grid cells
        # grid_frame.pack(side=tk.LEFT)
        grid_frame.grid(row=1, column=1, columnspan=1)
        grid_frame.pack_propagate(0)
        for row in range(1):
            self.rowconfigure(row, weight=1, minsize=50, uniform='row')
            self.columnconfigure(row, weight=1, minsize=75, uniform='row')
            for col in range(1):
                self.selection_made_button = tk.Button(
                    master=grid_frame,
                    image=tk.PhotoImage(),
                    font=font.Font(size=36, weight="bold"),
                    fg="black",
                    width=100,
                    height=100,
                    highlightbackground="lightblue",
                )
                # Calling this 1x1 grid board 3 for now
                self._cells[self.selection_made_button] = (row, col, 3)
                self.selection_made_button.bind("<ButtonPress-1>", self.play)
                self.selection_made_button.grid(
                    row=row,
                    column=col,
                    padx=5,
                    pady=5,
                    sticky="nsew"
                )
                self.selection_made_button.grid_propagate(False)
                
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
                # testing expanding the array to have a board marker in the third position of array.
                self._cells[button] = (row, col, 2)
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

    # def start_game(self):
    #     """Select the first piece that will be played."""
    #     starting_piece = random.randrange(0,16)
    #     # Then do selection of piece and populate middle
    #     perform_selection(starting_piece)
        

    # def perform_selection(selected_piece):
    #     #work out row and column
        
        
    
    
    # The .mainloop() method on the Tk class runs what’s known as the application’s 
    # main loop or event loop. This is an infinite loop in which all the GUI events happen.
    # The tkinter main loop is an infinite loop used to run the application, wait for an event to occur, and process the event
    # as long as the window is not closed.
    def play(self, event):
        """Handle a player's move.

        Need to do:
        Selecting only from left grid first.
        That populating middle.
        Then putting image in right grid. 
        """
        clicked_btn = event.widget
        row, col, board = self._cells[clicked_btn]
        move = Move(row, col, board, self.current_player.label)
        # Validate if the right grid has been 
        if self._game.is_valid_grid_selected(move):
            # Now we need to check which board was selected and condition next steps on it
            if move.board == 1:
                # Select
                if self._game.is_valid_move_selection_grid(move):
                    # Do selection steps
                    self.piece_number = move.row * 4 + move.col
                    move = Move(row, col, board, '{0:04b}'.format(self.piece_number))
                    self._update_selection_button(clicked_btn)
                    self._game.process_selection_move(move)
                    self.selection_made_button.config(image=self.img_list[self.piece_number])
                    self.toggle_player()
                    msg = f"{self.current_player.label}'s turn"
                    self._update_display(msg)
            # To Do: make this part of the logic

            if move.board == 2:
            # Play
                if self._game.is_valid_move_play_grid(move): # Maybe show error message to user if False?
                    move = Move(row, col, board, '{0:04b}'.format(self.piece_number))
                    self._update_play_button(clicked_btn, self.piece_number)
                    self.selection_made_button.config(image=tk.PhotoImage())
                    self._game.process_play_move(move, self.piece_number)
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
                    # else: probably can delete at this point
                    #     self.toggle_player()
                    #     msg = f"{self.current_player.label}'s turn"
                    #     self._update_display(msg)
        else:
            msg = f"You must select the other board."
            self._update_display(msg)
                
                
    def _update_selection_button(self, clicked_btn):
        # Need to set to a 3D image for us
        clicked_btn.config(image=tk.PhotoImage())
        #clicked_btn.config(text=self.current_player.label)
        #clicked_btn.config(fg=self.current_player.color)
    
    def _update_play_button(self, clicked_btn, piece_number):
        # Need to set to a 3D image for us
        clicked_btn.config(image=self.img_list[piece_number])
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
        # file_menu.add_command(
        #     label="Play Again",
        #     command=self.reset_board
        # )
        file_menu.add_separator()
        file_menu.add_command(label="Exit", command=quit)
        menu_bar.add_cascade(label="File", menu=file_menu)
        
    # def reset_board(self):
    #     """Reset the game's board to play again."""
    #     self._game.reset_game()
    #     self._update_display(msg="Ready?")
    #     # Reset all the buttons
    #     for button in self._cells.keys():
    #         button.config(highlightbackground="lightblue")
    #         button.config(text="")
    #         button.config(fg="black")

def main():
    """Create the game's board and run its main loop."""
    game = QuartoGame()
    board = QuartoBoard(game)
    board.resizable(False, False)
    board.mainloop()

if __name__ == "__main__":
    main()