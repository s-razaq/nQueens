__author__ = 'Saqib Razaq'


"""
Using a regular chess board, the challenge is to place eight queens on the board such that no queen is attacking any of
the others. (For those not familiar with chess pieces, the queen is able to attack any square on the same row, any
square on the same column, and also any square on either of the diagonals).
"""

from time import time
import Tkinter
import ttk
import tkMessageBox
import itertools


__version__ = '0.9'


class NQueens():

    def __init__(self, master):
        self.num_queens = 8
        self.queens = [0 for _ in range(self.num_queens)]
        self.index = 0
        self.solutions = None

        self.master = master
        self.master.title('NQueens')
        self.master.configure(background='#e1d8b9')
        self.master.minsize(400, 470)
        self.master.resizable(True, True)
        self.master.bind('<Configure>', lambda e: self.draw_board())

        self.style = ttk.Style()
        self.style.configure('TFrame', background='#eld8b9')
        self.style.configure('TButton', background='#e1d8b9')
        self.style.configure('TLabel', background='#e1d8b9')

        self.board_canvas = Tkinter.Canvas(self.master)
        self.board_canvas.pack()

        self.controls_frame = ttk.Frame(self.master)
        self.controls_frame.pack(side=Tkinter.TOP, pady=10)

        ttk.Label(self.controls_frame, text='Number of Queens',
                  font='Verdana 10 bold').grid(row=0, column=0)
        self.num_queens_var = Tkinter.StringVar()
        self.num_queens_var.set(self.num_queens)
        Tkinter.Spinbox(self.controls_frame, from_=4, to=99, width=2,
                        font='Verdana 10 bold', textvariable=self.num_queens_var).grid(row=0, column=1)
        ttk.Button(self.controls_frame, text='Get Next Solution',
                   command=self.solution_callback).grid(row=1, column=0, columnspan=2)
        ttk.Label(self.controls_frame).grid(row=0, column=2, padx=10)

        self.solution_var = Tkinter.StringVar()
        self.time_var = Tkinter.StringVar()
        self.solution_var.set('--')
        self.time_var.set('--')
        ttk.Label(self.controls_frame, text='Solution:',
                  font='Verdana 10 bold').grid(row=0, column=3, sticky=(Tkinter.E))
        ttk.Label(self.controls_frame, textvariable=self.solution_var,
                  font='Verdana 10').grid(row=0, column=4, sticky=(Tkinter.W))
        ttk.Label(self.controls_frame, text='Elapsed Time:',
                  font='Verdana 10 bold').grid(row=1, column=3, sticky=(Tkinter.E))
        ttk.Label(self.controls_frame, textvariable=self.time_var,
                  font='Verdana 10').grid(row=1, column=4, sticky=(Tkinter.W))

        self.solution_callback()  # begin by showing first solution to 8 queens

    def draw_board(self):
        maxboardsize = min(self.master.winfo_height() - 70, self.master.winfo_width())
        cellsize = maxboardsize // self.num_queens
        self.board_canvas.config(height=self.num_queens*cellsize, width=self.num_queens*cellsize)
        self.board_canvas.delete('all')

        # color in black board cells
        for i in range(self.num_queens):
            for j in range(self.num_queens):
                if(i+j+self.num_queens) % 2:  # black cell
                    self.board_canvas.create_rectangle(i*cellsize, j*cellsize,
                                                       i*cellsize+cellsize, j*cellsize+cellsize,
                                                       fill='black')
            # draw a queen
            self.board_canvas.create_text(i*cellsize+cellsize//2, self.queens[i]*cellsize+cellsize//2,
                                          text=u'\u265B', font=('Arial', cellsize//2),
                                          fill='orange')


    def solution_callback(self):
        try:
            input_val = int(self.num_queens_var.get())
        except:
            tkMessageBox.showerror(title='Invalid Input',
                                   message='Must enter a number for N.')
            return

        # check if N has changed or if this is first run
        if self.num_queens != input_val or self.solutions is None:
            if 4 > input_val:
                tkMessageBox.showerror(title='Invalid Value for N',
                                       message='N must be greater than 4')
            else:
                self.num_queens = input_val
                self.index = 0
                self.solutions = []

                start_time = time()

                # calculate new list of solutions
                columns = range(self.num_queens)
                for perm in itertools.permutations(columns):
                    diag1 = set()
                    diag2 = set()
                    for i in columns:
                        diag1.add(perm[i]+i)  # check / diagonal
                        diag2.add(perm[i]-i)  # check } diagonal
                    if self.num_queens == len(diag1) == len(diag2):
                        self.solutions.append(perm)

                elapsed_time = time() - start_time
                self.time_var.set('{0:.3f}s'.format(elapsed_time))
        else:
            self.index += 1

        self.queens = self.solutions[self.index % len(self.solutions)]
        self.solution_var.set('{}/{}'.format(self.index % len(self.solutions) + 1, len(self.solutions)))
        self.draw_board()


def main():
    root = Tkinter.Tk()
    gui = NQueens(root)
    root.mainloop()

if __name__ == '__main__':
    main()


