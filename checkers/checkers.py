from matplotlib import pyplot as plt
from numpy import arange
from matplotlib.pylab import cm
import numpy as np
import sys
import string as s
from random import sample

class piece:
	def __init__(self, x_coor, y_coor, nbr, player, kinged=False):
		self.x = x_coor
		self.y = y_coor
		self.n = nbr
		self.id = player
		self.king = kinged
		self.moves = []

	def move(self,new_x, new_y):
		self.x, self.y = new_x, new_y
		if self.id == 1 and self.y == 8:
			self.king = True
		if self.id == 2 and self.y == 1:
			self.king = True

	def find_moves(self, board):
		moves, jumps = [], []

		p1_dirs, p2_dirs = [(1,1), (-1,1)], [(1,-1), (-1,-1)]

		if self.king:
			dirs = p1_dirs+p2_dirs
		elif self.id == 1:
			dirs = p1_dirs
		elif self.id == 2:
			dirs = p2_dirs

		for d in dirs:
			if (self.x+d[0], self.y+d[1]) in board.layout:
				if board.layout[(self.x+d[0], self.y+d[1])] is None:
					moves.append(d)
				else:
					if (board.layout[(self.x+d[0], self.y+d[1])].id != self.id and
						(self.x+2*d[0], self.y+2*d[1]) in board.layout and
						board.layout[(self.x+2*d[0], self.y+2*d[1])] is None):
						jumps.append((2*d[0],2*d[1]))
		if jumps:
			self.moves = jumps
		else:
			self.moves = moves

	def printme(self):
		print self.x, self.y, self.n


class player:
	def __init__(self, player_nm, player_no):
		self.name = player_nm
		self.id = player_no
		self.p = [ piece for i in range(12) ] #list of pieces
		
		z = 0	
		if player_no == 1:
			for j in range(1, 4):
				for i in range(1, 9):
					if j%2==1:
						if i%2==1:
							self.p[z] = piece(i, j, z+1, 1)
							z+=1
					else:
						if i%2==0:
							self.p[z] = piece(i, j, z+1, 1)
							z+=1
		elif player_no == 2:
			for j in range(6, 9):
				for i in range(1, 9):
					if j%2==0:
						if i%2==0:
							self.p[z] = piece(i, j, z+1, 2)
							z+=1
					else:
						if i%2==1:
							self.p[z] = piece(i, j, z+1, 2)
							z+=1
		else:
			print "Player # must be either 1 or 2."	
			return		

	def get_piece(self, x_coor, y_coor):
		for p in self.p:
			if(p.x == x_coor and p.y == y_coor):
				return p
		return None

	def remove_pc(self, x, y):
		self.p.remove(self.get_piece(x, y))

	def get_xs(self):
		return [ i.x for i in self.p]

	def get_ys(self):
		return [ i.y for i in self.p]

	def move(self, piece_no, new_x, new_y):
		self.p[piece_no-1].move(new_x, new_y)

	def set_moves(self, board):
		for p in self.p:
			p.find_moves(board)

	def print_piece(self, piece_no):
		self.p[piece_no-1].printme()

	def print_all_pieces(self):
		for i in range(len(self.p)):
			self.p[i].printme()	
	

class Board:
	def __init__(self, player1, player2):
		self.p1 = player1.p
		self.p2 = player2.p
		self.layout = {}
		
		for j in range(1, 9):
			for i in range(1, 9):
				self.layout[(i, j)]	= player1.get_piece(i, j) or player2.get_piece(i,j)

	def remove_pc(self, x, y):
		self.layout[(x, y)] = None			

	def print_all_squares(self):
		for j in range(1, 9):
			for i in range(1, 9):
				if self.layout[(i, j)] is None:
					print (i, j), "none"
				else:
					print (i, j), self.layout[(i, j)]

	def show_board(self, player1, player2, turn):
		# make an 8x8 grid...
		nrows, ncols = 8,8
		image = np.zeros(nrows*ncols)

		# set every other cell to 1
		i, j, on = 0, 8, True
		while j < 65:
			for z in range(i, j):
				if on:
					if z%2:
						image[z] = 1
				else:
					if not z%2:
						image[z] = 1

			i += 8
			j += 8
			on = not on
		# reshape  into an 8x8 grid
		image = image.reshape((nrows, ncols))

		row_labels = range(1,nrows+1)
		col_labels = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I']
		plt.matshow(image, cmap=cm.gray, origin='lower')
		plt.gca().xaxis.set_ticks_position('bottom')

		if turn:
			plt.xticks(range(ncols), col_labels)
			plt.yticks(range(nrows), row_labels)
		else:
			plt.xticks(range(ncols)[::-1], col_labels)
			plt.yticks(range(nrows)[::-1], row_labels)
	
		p1_xs, p1_ys = [i-1 for i in player1.get_xs()], [i-1 for i in player1.get_ys()]
		p2_xs, p2_ys = [i-1 for i in player2.get_xs()], [i-1 for i in player2.get_ys()]

		if not turn:
			p1_xs, p1_ys = [7-i for i in p1_xs], [7-i for i in p1_ys]
			p2_xs, p2_ys = [7-i for i in p2_xs], [7-i for i in p2_ys]
		
		plt.scatter(p1_xs, p1_ys, c='red', s=3.14*12**2)
		plt.scatter(p2_xs, p2_ys, c='lightgrey', s=3.14*12**2)

		kings_xs = [p.x-1 for p in player1.p if p.king]	
		kings_xs += [p.x-1 for p in player2.p if p.king]
		kings_ys = [p.y-1 for p in player1.p if p.king]	
		kings_ys += [p.y-1 for p in player2.p if p.king]
		if not turn: 
			kings_xs, kings_ys = [7-i for i in kings_xs], [7-i for i in kings_ys]

		plt.scatter(kings_xs, kings_ys, facecolors='none', edgecolors='w', marker='*', s=3.14*8**2)

		plt.show()

def move_piece(x_loc, y_loc, x_dest, y_dest, player, board, p2, auto):
	pc = player.get_piece(x_loc, y_loc)
	dest_dir = (x_dest-x_loc, y_dest-y_loc)

	if pc is None:
		if auto:
			print "No piece at %s%s." % (rev_alpha[x_loc], y_loc)
		return False

	if dest_dir not in pc.moves:
		if auto:
			print "Invalid move. Please select another move."
		return False
	
	deuces = [(2,2), (-2,2), (-2,-2),(2,-2)]
	if dest_dir in deuces:
		i = (dest_dir[0]/2, dest_dir[1]/2)

	mandatory_jumps = []

	for p in player.p:
		if any([d in p.moves for d in deuces]):
			mandatory_jumps.append(p)
	
	if mandatory_jumps:
		if pc not in mandatory_jumps:
			if auto:
				print "Invalid move. Must jump when possible."
			return False
		else:
			if x_dest == x_loc+2*i[0] and y_dest == y_loc+2*i[1]:
				p2.remove_pc(x_loc+i[0], y_loc+i[1])
				board.remove_pc(x_loc+i[0], y_loc+i[1])
				print "Piece jumped at %s%s." % (rev_alpha[x_loc+i[0]], y_loc+i[1])

			else:
				print "Invalid move. Must jump nearby opponent."
				return False

	pc.move(x_dest, y_dest)
	board.layout[(x_loc, y_loc)] = None
	board.layout[(x_dest, y_dest)] = pc
	player.set_moves(board)
	p2.set_moves(board)
	return True

def init_game(ct):
	if ct == 2:
		p1 = player(raw_input("Who is player 1? "), 1)
		p2 = player(raw_input("Who is player 2? "), 2)
	elif ct == 1:
		p1, p2 = player(raw_input("What is your name? "), 1), player('CPU', 2)
	else:
		print "Can only play with 1 or 2 players."
		sys.exit()

	b = Board(p1, p2)	
	p1.set_moves(b)
	p2.set_moves(b)

	print "Let's play!"
	return (b, p1, p2)

alpha = dict (zip(list(s.uppercase)[:8], range(1,9)))
rev_alpha = dict (zip(alpha.values(), alpha.keys()))


ct = int(raw_input("Welcome to Checkers! Is this a 1 or 2 player game? "))

b, p1, p2 = init_game(ct)
p1_turn = True

while(len(p1.p) > 0 and len(p2.p) > 0 and any([p.moves for p in p1.p]) and any([p.moves for p in p2.p])):

	p1.set_moves(b)
	p2.set_moves(b)

	if ct == 2 or p1_turn:
		b.show_board(p1, p2, p1_turn)
		
		if p1_turn:
			n = 1
		else:
			n = 2
		
		prompt1 = "It's player %s's turn. Enter piece locn and piece dest, comma-separated: " % n
		prompt2 = "Please enter different move: "
		prompt3 = "Would you like to see the board again? Y/N: "

		m = raw_input(prompt1).split(", ")
		if m == ['Q']:
			print "Sorry you had to leave early, play again soon!"
			sys.exit()
	 
		pairs = [] ##list of pairs of moves to support n-jumping
		for i in range(1, len(m)):
			pairs.append([m[i-1], m[i]])

		for pair in pairs:
			m = list(pair[0]) + list(pair[1])
			if p1_turn:
				while(not move_piece(alpha[m[0]], int(m[1]), alpha[m[2]], int(m[3]), p1, b, p2, True)):
					if raw_input(prompt3) == 'Y':
						b.show_board(p1, p2, p1_turn)
					m = raw_input(prompt1).split(", ")
					m = list(m[0]) + list(m[1])

			else:
				while(not move_piece(alpha[m[0]], int(m[1]), alpha[m[2]], int(m[3]), p2, b, p1, True)):
					if raw_input(prompt3) == 'Y':
						b.show_board(p1, p2, p1_turn)
					m = raw_input(prompt1).split(", ")
					m = list(m[0]) + list(m[1])

	else:
		b.show_board(p1, p2, True)
		iters = [x for x in sample(p2.p, len(p2.p))]
		done = False
		for pc in iters:
			if done:
				break
			iters2 = [x for x in sample(pc.moves, len(pc.moves))]
			for move in iters2:
				if not done:
					if not move_piece(pc.x, pc.y, pc.x+move[0], pc.y+move[1], p2, b, p1, True):
						continue
					done = True
					print "CPU moved from %s%s to %s%s." %(rev_alpha[pc.x-move[0]], pc.y-move[1], rev_alpha[pc.x], pc.y)
					break

	p1_turn = not p1_turn

if len(p1.p) > 0:
	winner = p1.name
else:
	winner = p2.name

print "CONGRATULATIONS %s, YOU WIN!!!" % winner