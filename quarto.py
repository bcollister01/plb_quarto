import tkinter as tk #Currently 8.6
from tkinter import font

class QuartoBoard(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Quarto Game")
        self._cells = {}
        self._create_board_display()
        self._create_board_grid()

    def _create_board_display(self):
        display_frame = tk.Frame(master=self)
        display_frame.pack(fill=tk.X) #frame fills width if window resized
        self.display = tk.Label(
              master=display_frame, #label needs to live in frame
              text="Ready?",
              font=font.Font(size=28, weight="bold"),
        )
        self.display.pack()

    def _create_board_grid(self):
        grid_frame = tk.Frame(master=self) #Hold the game grid cells
        grid_frame.pack()
        for row in range(4): 
            self.rowconfigure(row, weight=1, minsize=50)
            self.columnconfigure(row, weight=1, minsize=75)
            for col in range(4):
                button = tk.Button(
                    master=grid_frame,
                    text="",
                    font=font.Font(size=36, weight="bold"),
                    fg="black",
                    width=3,
                    height=2,
                    highlightbackground="lightblue",
                )
                self._cells[button] = (row, col)
                button.grid(
                    row=row,
                    column=col,
                    padx=5,
                    pady=5,
                    sticky="nsew"
                )

def main():
    """Create the game's board and run its main loop."""
    board = QuartoBoard()
    board.mainloop()

if __name__ == "__main__":
    main()