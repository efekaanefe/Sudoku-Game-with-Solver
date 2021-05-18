import pygame
import pygame.font
import numpy as np
pygame.init()
pygame.font.init()

# CONSTANTS
GREY = (128, 128, 128)
DARK_GREY = (70, 70, 70)
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
BOARD = [
		[5, 3, 0, 0, 7, 0, 0, 0, 0],
		[6, 0, 0, 1, 9, 5, 0, 0, 0],
		[0, 9, 8, 0, 0, 0, 0, 6, 0],
		[8, 0, 0, 0, 6, 0, 0, 0, 3],
		[4, 0, 0, 8, 0, 3, 0, 0, 1],
		[7, 0, 0, 0, 2, 0, 0, 0, 6],
		[0, 6, 0, 0, 0, 0, 2, 8, 0],
		[0, 0, 0, 4, 1, 9, 0, 0, 5],
		[0, 0, 0, 0, 8, 0, 0, 7, 9]]

WIDTH = HEIGHT = 540
DIMENSION = 9
SQ_SIZE = WIDTH//DIMENSION


ASSIGNED_VALUE_FONT = pygame.font.SysFont("comicsans", 25)
VALID_VALUE_FONT = pygame.font.SysFont("comicsans", 40)


WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Sudoku")
WIN.fill(WHITE)


# CLASSES
class Board:
	def __init__(self, board):
		self.board = board
		self.squares = self.board.copy()
		# self.squares = board

		self.create_squares(True)

	def create_squares(self, first_time_created=False):
		for r in range(DIMENSION):
			for c in range(DIMENSION):
				value = self.board[r][c]
				if value != 0:
					starting_value = first_time_created
					self.squares[r][c] = Square(value, r, c, starting_value)
				else:
					self.squares[r][c] = Square(value, r, c)

	def draw_squares(self):
		for r in range(DIMENSION):
			for c in range(DIMENSION):
				square = self.squares[r][c]
				square.blit_square_surface()

	def draw_grids(self):
		for index in range(1, DIMENSION):
			line_size = 5 if (index % 3 == 0) else 2

			# vertical lines
			x_start = index*SQ_SIZE
			y_start = 0
			x_end = index*SQ_SIZE
			y_end = HEIGHT
			pygame.draw.line(WIN, BLACK, (x_start, y_start), (x_end, y_end), line_size)

			# horizontal lines
			x_start = 0
			y_start = index*SQ_SIZE
			x_end = WIDTH
			y_end = index*SQ_SIZE
			pygame.draw.line(WIN, BLACK, (x_start, y_start), (x_end, y_end), line_size)

	def reset_board_and_squares(self):
		for r in range(DIMENSION):
			for c in range(DIMENSION):
				square = self.squares[r][c]
				if square.starting_value == False:
					self.squares[r][c] = Square(0, r, c)

	def win_condition(self):
		counter = DIMENSION*DIMENSION
		for r in range(DIMENSION):
			for c in range(DIMENSION):
				square = self.squares[r][c]
				if square.valid_value != 0:
					counter -= 1
		if counter == 0:
			return True
		else: return False

	def possible(self, row, col, n):
		board = self.board

		for i in range(9):
			# row-wise
			if board[row][i] == n:
				return False
			# col-wise
			if board[i][col] == n:
				return False
		col0 = (col//3)*3
		row0 = (row//3)*3
		for i in range(0, 3):
			for j in range(0, 3):
				if board[row0+i][col0+j] == n:
					return False
		return True

	def solve(self):
		for r in range(DIMENSION):
			for c in range(DIMENSION):
				if self.board[r][c] == 0:
					for integer in range(1, 10):
						if self.possible(r, c, integer):
							#self.board[r][c] = integer
							self.squares[r][c] = Square(integer, r, c)
							self.draw_squares()
							self.draw_grids()
							pygame.display.update()
							#pygame.time.delay(0)
							self.solve()
							if r != 8 and c !=0:
								#self.board[r][c] = 0
								self.squares[r][c] = Square(0, r, c)
					#print(np.matrix(grid))
					return
		print(np.matrix(self.board))
		#input("More?") # might have find multiple solutions but I couldn´t figure out how to
		input("This is a solution for that board.\nPlease press enter in terminal to quit ")
		pygame.quit()


class Square:
	def __init__(self, valid_value, row, col, starting_value = False):
		self.valid_value = valid_value
		self.row = row
		self.col = col
		self.assigned_values = []
		self.square_surface = None
		self.create_square_surface()
		self.starting_value = starting_value

	def create_square_surface(self):
		square_surface = pygame.Surface((SQ_SIZE, SQ_SIZE))
		square_surface.fill(WHITE)

		# assigned value
		if self.valid_value == 0:
			values_str = ""
			for value in self.assigned_values:
				values_str += str(value)
				if value != self.assigned_values[-1]:
					values_str += ","

			assigned_values = ASSIGNED_VALUE_FONT.render(values_str,1, GREY)
			x = SQ_SIZE-assigned_values.get_width()-5
			y = 5
			square_surface.blit(assigned_values, (x, y))
			self.square_surface = square_surface

		# validated values
		else:
			# if it is starting value given at the beginning, color is dark grey
			try:
				color = DARK_GREY if self.starting_value else BLACK
			except: 
				color = BLACK
			value_str = str(self.valid_value)
			value = VALID_VALUE_FONT.render(value_str, 1, color)
			x = (SQ_SIZE-value.get_width()) // 2
			y = (SQ_SIZE-value.get_height())//2
			square_surface.blit(value, (x, y))
			self.square_surface = square_surface
		

	def blit_square_surface(self):
		self.create_square_surface()
		x = self.col*SQ_SIZE
		y = self.row*SQ_SIZE
		WIN.blit(self.square_surface, (x, y))

	def __eq__(self, other):
		return self.valid_value == other

	def __repr__(self):
		#return str("Square object with valid value {}".format(self.valid_value))
		return str(self.valid_value)


def draw_sq_selected_grid(sq_selected): # (row, col)
	if len(sq_selected) != 0:
		thickness = 5
		row, col = sq_selected
		x, y = col*SQ_SIZE, row*SQ_SIZE
		# top grid
		pygame.draw.line(WIN, RED, (x,y), (x+SQ_SIZE, y), thickness)
		# bottom grid
		pygame.draw.line(WIN, RED, (x,y+SQ_SIZE), (x+SQ_SIZE, y+SQ_SIZE), thickness)
		# left grid
		pygame.draw.line(WIN, RED, (x,y), (x,y+SQ_SIZE), thickness)
		# right grid
		pygame.draw.line(WIN, RED, (x+SQ_SIZE,y), (x+SQ_SIZE, y+SQ_SIZE), thickness)


def main():
	run = True
	board = Board(BOARD)
	sq_selected = ()
	while run:
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				run = False

			# select square with mouse click
			if event.type == pygame.MOUSEBUTTONDOWN:
				x, y = pygame.mouse.get_pos()
				row, col = y//SQ_SIZE, x//SQ_SIZE
				if (row, col) != sq_selected: 
					sq_selected = (row, col)
				else:
					sq_selected = ()

			if event.type == pygame.KEYDOWN:
				if len(sq_selected) != 0:
					row, col = sq_selected

				# select square with keyboard arrow
				# down
				if event.key == pygame.K_DOWN:
					row += 1
					if row>DIMENSION-1:
						row = 0
					sq_selected = (row, col)
				# up
				if event.key == pygame.K_UP:
					row -= 1
					if row<0:
						row = DIMENSION-1
					sq_selected = (row, col)
				# left
				if event.key == pygame.K_LEFT:
					col -= 1
					if col<0:
						col = DIMENSION-1
					sq_selected = (row, col)

				# right
				if event.key == pygame.K_RIGHT:
					col += 1
					if col>DIMENSION-1:
						col = 0
					sq_selected = (row, col)



				# assign values to sq_selected
				if len(sq_selected) != 0:
					square = board.squares[row][col]
					if len(square.assigned_values) < 3:
						if square.valid_value == 0:
							if event.key == pygame.K_KP1:
								if 1 not in square.assigned_values:
									square.assigned_values += [1]
							elif event.key == pygame.K_KP2:
								if 2 not in square.assigned_values:
									square.assigned_values += [2]
							elif event.key == pygame.K_KP3:
								if 3 not in square.assigned_values:
									square.assigned_values += [3]
							elif event.key == pygame.K_KP4:
								if 4 not in square.assigned_values:
									square.assigned_values += [4]
							elif event.key == pygame.K_KP5:
								if 5 not in square.assigned_values:
									square.assigned_values += [5]
							elif event.key == pygame.K_KP6:
								if 6 not in square.assigned_values:
									square.assigned_values += [6]
							elif event.key == pygame.K_KP7:
								if 7 not in square.assigned_values:
									square.assigned_values += [7]
							elif event.key == pygame.K_KP8:
								if 8 not in square.assigned_values:
									square.assigned_values += [8]
							elif event.key == pygame.K_KP9:
								if 9 not in square.assigned_values:
									square.assigned_values += [9]

				# remove last assigned value or valid value
				# player shouldnt be able to remove starting values
				if event.key == pygame.K_BACKSPACE:
					square = board.squares[row][col]
					if len(square.assigned_values) != 0:
						square.assigned_values.pop(-1)
					else:
						if square.starting_value:
							print("It is a starting value, you can´t delete or change its value")
						else:
							square.valid_value = 0

				# enter valid value
				if event.key == pygame.K_RETURN or event.key == pygame.K_KP_ENTER:

					square = board.squares[row][col]
					if len(square.assigned_values) == 1:
						value = square.assigned_values[0]
						if board.possible(row, col, value):
							# board.board[row][col] = value
							board.squares[row][col] = Square(value, row, col, False)
						else:
							square.assigned_values = []
							print("Value: {} is not valid for row: {}, col: {}".format(value, row+1, col+1))
					
					if board.win_condition():
						print("Well done, you won!!")
						input("Press enter in terminal to quit ")
						pygame.quit()

				
				if event.key == pygame.K_SPACE:
					board.reset_board_and_squares()
					board.solve()

				if event.key == pygame.K_SPACE:
					board.solve()

		


		board.draw_squares()
		board.draw_grids()
		draw_sq_selected_grid(sq_selected)
		pygame.display.update()

if __name__ == "__main__":
	main()


