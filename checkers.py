from matplotlib import pyplot as plt
from numpy import arange
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

	def move(self,new_x, new_y):
		self.x, self.y = new_x, new_y
		if self.id == 1 and self.y == 8:
			self.king = True
		if self.id == 2 and self.y == 1:
			self.king = True

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
		x = arange(.5, 8.5, 1)
		y = x

		fig = plt.figure()
		ax = fig.gca()

		ax.set_xticks(x, minor=True)
		ax.set_xticks([i+.5 for i in x], minor=False)
		ax.set_yticks(y, minor=True)
		ax.set_yticks([i+.5 for i in y], minor=False)

		xlabels = list(s.uppercase)[:8]
		ylabels = range(1,9)
		if turn:
			ax.set_xticklabels(xlabels)
			ax.set_yticklabels(ylabels)
		else:
			ax.set_xticklabels(xlabels[::-1])
			ax.set_yticklabels(ylabels[::-1])

		ax.xaxis.grid(True, which='minor')
		ax.yaxis.grid(True, which='minor')
		plt.axis([0.5,8.5, 0.5,8.5])
		

		p1_xs, p1_ys = player1.get_xs(), player1.get_ys()
		p2_xs, p2_ys = player2.get_xs(), player2.get_ys()

		if not turn:
			p1_xs, p1_ys = [9-i for i in p1_xs], [9-i for i in p1_ys]
			p2_xs, p2_ys = [9-i for i in p2_xs], [9-i for i in p2_ys]
		
		plt.scatter(p1_xs, p1_ys, c='red', s=3.14*12**2)
		plt.scatter(p2_xs, p2_ys, c='black', s=3.14*12**2)

		kings_xs = [p.x for p in player1.p if p.king]	
		kings_xs += [p.x for p in player2.p if p.king]
		kings_ys = [p.y for p in player1.p if p.king]	
		kings_ys += [p.y for p in player2.p if p.king]
		if not turn: 
			kings_xs, kings_ys = [9-i for i in kings_xs], [9-i for i in kings_ys]

		plt.scatter(kings_xs, kings_ys, facecolors='none', edgecolors='w', marker='*', s=3.14*8**2)

		plt.show()


def legal_checks(x_loc, y_loc, x_dest, y_dest, player, board, pc, auto):
	
	if pc is None:
		if auto:
			print "No piece at %s%s." % (rev_alpha[x_loc], y_loc)
		return False

	if (x_dest, y_dest) not in board.layout:
		if auto:
			print "Invalid move. %s, %s is not on the board." (x_dest, y_dest)
		return False

	if board.layout[(x_dest, y_dest)] is not None:
		if auto:
			print "Cannot move to %s%s. There's already a piece there." % (rev_alpha[x_dest], y_dest)
		return False

	if (player.id == 1 and y_dest not in [y_loc+1, y_loc+2] and pc.king == False):
		if auto:
			print "Invalid move. Player 1 must move up."
		return False

	if (player.id == 2 and y_dest not in [y_loc-1, y_loc-2] and pc.king == False):
		if auto:
			print "Invalid move. Player 2 must move down."
		return False

	if x_dest not in [x_loc+1, x_loc-1, x_loc+2, x_loc-2]:
		if auto:
			print "Invalid move. Can only move left or right by 1 or 2 squares."
		return False

	if not abs(x_loc-x_dest)==abs(y_loc-y_dest):
		if auto:
			print "Invalid move. Horizontal & vertical distance must be the same."
		return False 

	if abs(x_loc-x_dest)==2 and abs(y_loc-y_dest)==2 and ((x_dest-x_loc)/2, (y_dest-y_loc)/2) not in nearby_opponent(pc, player, b):
		if auto:
			print (x_dest-x_loc, y_dest-y_loc)
			print nearby_opponent(pc, player, b)
			print "Invalid move. Can only move 2 squares when jumping opponent."
		return False

	p1_dirs, p2_dirs = [(1,1), (-1,1)], [(1,-1), (-1,-1)]

	if pc.king:
		dirs = p1_dirs+p2_dirs
	elif player.id == 1:
		dirs = p1_dirs
	elif player.id == 2:
		dirs = p2_dirs

	for d in dirs:
		if ((x_dest == x_loc+2*d[0] and y_dest == y_loc+2*d[1]) and
			(pc.x+d[0], pc.y+d[1]) in board.layout and 
			board.layout[(pc.x+d[0], pc.y+d[1])] is not None and
			board.layout[(pc.x+d[0], pc.y+d[1])].id == player.id):
			if auto:
				print "Invalid move. Cannot jump your own piece."
			return False

	return True

def move_piece(x_loc, y_loc, x_dest, y_dest, player, board, p2, auto):
	p = player.get_piece(x_loc, y_loc)
	
	if not legal_checks(x_loc, y_loc, x_dest, y_dest, player, board, p, auto):
		return False

	check = nearby_opponent(p, player, board)	
	if check:
		j=jump(player, check, x_loc, y_loc, x_dest, y_dest, p2, board)
		if j==False:
			return j

	p.move(x_dest, y_dest)
	board.layout[(x_loc, y_loc)] = None
	board.layout[(x_dest, y_dest)] = p
	return True

def jump(player, check, x_loc, y_loc, x_dest, y_dest, p2, board):

	for i in check:
		if x_dest == x_loc+2*i[0] and y_dest == y_loc+2*i[1]:
			p2.remove_pc(x_loc+i[0], y_loc+i[1])
			board.remove_pc(x_loc+i[0], y_loc+i[1])
			return True

	else:
		print "Invalid move. Must jump nearby opponent."
		return False


def nearby_opponent(pc, player, board):
	neighbors = []
	p1_dirs, p2_dirs = [(1,1), (-1,1)], [(1,-1), (-1,-1)]

	if pc.king:
		dirs = p1_dirs+p2_dirs
	elif player.id == 1:
		dirs = p1_dirs
	elif player.id == 2:
		dirs = p2_dirs

	for d in dirs:
		if ((pc.x+d[0], pc.y+d[1]) in board.layout and 
			board.layout[(pc.x+d[0], pc.y+d[1])] is not None and
			board.layout[(pc.x+d[0], pc.y+d[1])].id != player.id and
			(pc.x+2*d[0], pc.y+2*d[1]) in board.layout and
			board.layout[(pc.x+2*d[0], pc.y+2*d[1])] is None):

			neighbors.append(d)

	return neighbors

def legals(pc, player, board):
	legals = []
	p1_dirs = [(1,1), (2,2), (-1,1), (-2,2)]
	p2_dirs = [(1,-1), (2,-2), (-1,-1), (-2,-2)]

	if pc.king:
		dirs = p1_dirs+p2_dirs
	elif player.id == 1:
		dirs = p1_dirs
	elif player.id == 2:
		dirs = p2_dirs

	for d in dirs:
		if ((pc.x+d[0], pc.y+d[1]) in board.layout and 
			board.layout[(pc.x+d[0], pc.y+d[1])] is None):

			legals.append(d)
	
	return legals

ct = int(raw_input("Welcome to Checkers! Is this a 1 or 2 player game? "))

def init_game():
	p1 = player(raw_input("Who is player 1? "), 1)
	p2 = player(raw_input("Who is player 2? "), 2)

	print "Let's play!"
	return (Board(p1, p2), p1, p2)

if ct == 2:
	b, p1, p2 = init_game()
else:
	p1, p2 = player(raw_input("What is your name? "), 1), player('CPU', 2)
	b = Board(p1,p2)

p1_turn = True

alpha = dict (zip(list(s.uppercase)[:8], range(1,9)))
rev_alpha = dict (zip(alpha.values(), alpha.keys()))

while(len(p1.p) > 0 and len(p2.p) > 0):
	b.show_board(p1, p2, p1_turn)

	if ct == 2 or p1_turn:
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
		iters = [x for x in sample(p2.p, len(p2.p))]
		done = False
		for pc in iters:
			if done:
				break
			moves = legals(pc, p2, b)
			for move in moves:
				if (not legal_checks(pc.x, pc.y, pc.x+move[0], pc.y+move[1], p2, b, pc, False) or
					(move in [(2,2),(-2,-2)] and move not in nearby_opponent(pc, p2, b))):
					moves.remove(move)
			iters2 = [x for x in sample(moves, len(moves))]
			for move in iters2:
				if not done:
					if not move_piece(pc.x, pc.y, pc.x+move[0], pc.y+move[1], p2, b, p1, False):
						continue
					else:
						done = True
						print "CPU moved from %s%s to %s%s." %(rev_alpha[pc.x-move[0]], pc.y-move[1], rev_alpha[pc.x], pc.y)
						break

	p1_turn = not p1_turn

if len(p1.p) > 0:
	winner = p1.name
else:
	winner = p2.name

print "CONGRATULATIONS %s, YOU WIN!!!" % winner