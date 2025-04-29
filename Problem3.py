import tkinter as tk
from tkinter import messagebox
import random
import heapq

N = 8
cell_size = 60

class NQueenGame:
    def __init__(self, root):
        self.root = root
        self.root.title("N-Queen Game (Random Start)")
        self.canvas = tk.Canvas(root, width=N*cell_size, height=N*cell_size)
        self.canvas.pack()

        self.reset_button = tk.Button(root, text="Reset", command=self.reset_game)
        self.reset_button.pack(side=tk.LEFT, padx=10, pady=10)

        self.solve_button = tk.Button(root, text="Solve (Greedy Best-First)", command=self.solve_game)
        self.solve_button.pack(side=tk.LEFT, padx=10, pady=10)

        self.board = [[0 for _ in range(N)] for _ in range(N)]
        self.selected = None

        self.canvas.bind("<Button-1>", self.handle_click)
        self.draw_board()
        self.place_random_queens()
        self.update_status()

    def draw_board(self):
        colors = ["#F0D9B5", "#B58863"]
        for i in range(N):
            for j in range(N):
                color = colors[(i + j) % 2]
                x0, y0 = j*cell_size, i*cell_size
                x1, y1 = x0 + cell_size, y0 + cell_size
                self.canvas.create_rectangle(x0, y0, x1, y1, fill=color, outline="black")

    def place_random_queens(self):
        self.board = [[0 for _ in range(N)] for _ in range(N)]
        positions = list(range(N))
        random.shuffle(positions)
        for row in range(N):
            col = positions[row]
            self.board[row][col] = 1
        self.redraw_queens()

    def redraw_queens(self):
        self.canvas.delete("queen")
        for i in range(N):
            for j in range(N):
                if self.board[i][j] == 1:
                    self.canvas.create_text(j*cell_size + cell_size//2,
                                            i*cell_size + cell_size//2,
                                            text="♛", font=("Arial", 24),
                                            tags="queen", fill="black")

    def handle_click(self, event):
        col = event.x // cell_size
        row = event.y // cell_size

        if self.selected:
            prev_row, prev_col = self.selected
            if (row, col) != self.selected:
                if self.board[row][col] == 0:
                    self.board[prev_row][prev_col] = 0
                    self.board[row][col] = 1
                    self.selected = None
                    self.redraw_queens()
                    self.update_status()
                else:
                    self.selected = (row, col)
            else:
                self.selected = None
        else:
            if self.board[row][col] == 1:
                self.selected = (row, col)

    def is_safe(self, r, c):
        for i in range(N):
            if i != r and self.board[i][c] == 1:
                return False
        for i, j in zip(range(r-1, -1, -1), range(c-1, -1, -1)):
            if self.board[i][j] == 1:
                return False
        for i, j in zip(range(r+1, N), range(c+1, N)):
            if self.board[i][j] == 1:
                return False
        for i, j in zip(range(r-1, -1, -1), range(c+1, N)):
            if self.board[i][j] == 1:
                return False
        for i, j in zip(range(r+1, N), range(c-1, -1, -1)):
            if self.board[i][j] == 1:
                return False
        return True

    def update_status(self):
        conflict = False
        for i in range(N):
            for j in range(N):
                if self.board[i][j] == 1:
                    if not self.is_safe(i, j):
                        conflict = True
                        break
            if conflict:
                break
        if conflict:
            self.root.title("Conflict Detected! 🚫 Fix the Queens.")
        else:
            self.root.title("Good! ✅ No Conflicts.")

    def reset_game(self):
        self.place_random_queens()
        self.update_status()

    def count_conflicts(self, board):
        conflicts = 0
        for i in range(N):
            for j in range(N):
                if board[i][j] == 1:
                    conflicts += self.count_conflicts_at(board, i, j)
        return conflicts // 2  # كل تعارض بيتحسب مرتين

    def count_conflicts_at(self, board, r, c):
        cnt = 0
        for i in range(N):
            if i != r and board[i][c] == 1:
                cnt += 1
        for i, j in zip(range(r-1, -1, -1), range(c-1, -1, -1)):
            if board[i][j] == 1:
                cnt += 1
        for i, j in zip(range(r+1, N), range(c+1, N)):
            if board[i][j] == 1:
                cnt += 1
        for i, j in zip(range(r-1, -1, -1), range(c+1, N)):
            if board[i][j] == 1:
                cnt += 1
        for i, j in zip(range(r+1, N), range(c-1, -1, -1)):
            if board[i][j] == 1:
                cnt += 1
        return cnt

    def solve_game(self):
        heap = []
        heapq.heappush(heap, (self.count_conflicts(self.board), self.board))

        visited = set()

        while heap:
            cost, current_board = heapq.heappop(heap)

            board_tuple = tuple(tuple(row) for row in current_board)
            if board_tuple in visited:
                continue
            visited.add(board_tuple)

            if cost == 0:
                self.board = [row[:] for row in current_board]
                self.redraw_queens()
                self.update_status()
                messagebox.showinfo("Solved!", "✅ Solution Found!")
                return

            for r in range(N):
                for c in range(N):
                    if current_board[r][c] == 1:
                        for new_c in range(N):
                            if new_c != c:
                                new_board = [row[:] for row in current_board]
                                new_board[r][c] = 0
                                new_board[r][new_c] = 1
                                heapq.heappush(heap, (self.count_conflicts(new_board), new_board))

        messagebox.showinfo("Failed", "❌ Couldn't find a solution.")

root = tk.Tk()
game = NQueenGame(root)
root.mainloop()
