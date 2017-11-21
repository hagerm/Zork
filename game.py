#######################################################################
# The core code of the Zork game.
# 
# @author Matthew Hager
# @version November 20, 2017
#######################################################################

# Imports what is observed, and things for random.
from house import House
from player import Player
import sys	#Don't think I need, but something I eperimented with.
from random import randint
import os 	#Used for clearing terminal while running game.

# Note: https://codereview.stackexchange.com/questions/20938/the-observer-design-pattern-in-python-in-a-more-pythonic-way-plus-unit-testing
# was used as a resource to understand/learn the Observer Pattern

# Class for the game, is called by zork.py
class Game:

	# Initializer for the game
	def __init__(self):
		self.gm_active = False
		self.neighborhood_height = randint(1, 5)
		self.neighborhood_width = randint(1, 5)
		self.houses_left = (self.neighborhood_height) * (self.neighborhood_width)
		self.saved_hp = 0
		self.num_monsters = 0
		self.player_x_loc = 0
		self.player_y_loc = 0
		self.neighborhood = [[House(self) for i in range(0, self.neighborhood_height)] for j in range(0, self.neighborhood_width)]
		#self.init_houses()
		self.player = Player(self)

	# The main code of the game that runs
	def the_game(self):
		os.system('cls' if os.name == 'nt' else 'clear')
		print("Welcome to Zork.\nThis version has been created by Matthew Hager.\n")
		print("Commands are accepted in lowercase only (for now). You can type 'help' for\n" + 
			  "a list of basic commands, but the rest is on you to figure out.\n")
		print("\nEnjoy.\n\n")

		# Dummy variable that never changes value.
		value = 0
		
		# Try to look for a case were the code needs to break from a function.
		try:
			# While to keep the game going forever unless told otherwise.
			while value < 1:
				var = input(": ")
				os.system('cls' if os.name == 'nt' else 'clear')

				# Prints help message				
				if var == 'help':
					print("This is a list of basic commands:")
					print("\thelp:\tLists commands.")
					print("\tloc:\tGive you current location, and information about where you can go. ")
					print("\tview:\tView the monsters at the current house.")
					print("\tnorth:\tAttempts to go North.")
					print("\tsouth:\tAttempts to go South.")
					print("\teast:\tAttempts to go East.")
					print("\twest:\tAttempts to go West.")
					print("\tattack:\tRolls to attack monsters at location, they will attack back unless 'redeemed'.\n" + 
						  "\t\tNote that persons will automatically heal you when attacked, and cannot be harmed.")
					print("\tnumleft:\tLists the number of monsters left in the game.")
					print("\thealth:\tLists your current HP. Game over if you go below 0.")
					#print("\thleft:\tHouses left to clear.") # I could not get this to function for some reason.
					print("\tlistw:\tLists weapons you have.")
					#print("\thelp: \n")	# These are left in for future expansion of code.
					#print("\thelp: \n")
					#print("\thelp: \n")
					#print("\thelp: \n")
					print("\tquit: Prompt for quiting the game.\n\n")

				# Prints information about the current location.
				elif var == 'loc':
					self.loc()

				# Views information about the house at the cur location.
				elif var == 'view':
					print(self.neighborhood[self.player_x_loc][self.player_y_loc].list_monsters())

				# Attempts to move North
				elif var == 'north':
					self.move_player('north')

				# Attempts to move South
				elif var == 'south':
					self.move_player('south')

				# Attempts to move East
				elif var == 'east':
					self.move_player('east')

				# Attempts to move West
				elif var == 'west':
					self.move_player('west')

				# Attacks monsters who then attack back (assuming no errors)
				# Currently uses a secondary command for type of weapon to use.
				# Not the ideal methodology, but gets the job done for now.
				# Stay tuned for updates.
				elif var == 'attack':
					print("What do you want to attack with?")
					var2 = input(": ")
					output = 0
					if var2 == 'nerdbomb':
						output = self.player.use_weapon('nerdbomb')
						if output < 0:
							print("You do not have that type of weapon.\n\n")
					elif var2 == 'hershykiss':
						output = self.player.use_weapon('hershykiss')
						if output < 0:
							print("You do not have that type of weapon.\n\n")
					elif var2 == 'sourstraws':
						output = self.player.use_weapon('sourstraws')
						if output < 0:
							print("You do not have that type of weapon.\n\n")
					elif var2 == 'chocolatebar':
						output = self.player.use_weapon('chocolatebar')
						if output < 0:
							print("You do not have that type of weapon.\n\n")
					else:
						print("That is an invalid weapon name.\nYour options are:\thershykiss, nerdbomb, sourstraws, chocolatebar\n")					
					if output > 0:	
						self.neighborhood[self.player_x_loc][self.player_y_loc].attack_monsters(var, output)
						damage = self.neighborhood[self.player_x_loc][self.player_y_loc].monsters_attack_player()
						self.player.take_damage(damage)
						print("Playered attacked with {0:10.0f} damage.".format(output))
						print("Monsters dealt {0} damage back.".format(damage))

				# Prints the number of monsters left to kill.
				elif var == 'numleft':
					total = 0
					for i in range(0, self.neighborhood_width):
						for j in range(0, self.neighborhood_height):
							total = total + self.neighborhood[i][j].get_num_monsters()
					print("There are {0} Monsters left.\n".format(total))
				
				# I couldn't get this to work for some reason for the initial release.
				#elif var == 'hleft':
				#	print("There are {0} houses left to clear.\n\n".format(self.houses_left))

				# Prints the player's remaining health.
				elif var == 'health':
					print(self.player.get_hp())

				# Debug to set player hp to 1
				elif var == 'pkill':
					self.player.set_hp(1)

				# Prints a list of the player's weapons.
				elif var == 'listw':
					print(self.player.list_weapons())

				# Gives player essentially infinite hp
				elif var == 'gmode':
					if self.gm_active == False:
						self.gm_active = True
						self.saved_hp = self.player.get_hp()
						self.player.set_hp(1000000000000)

				# Undos God Mode
				elif var == 'nmode':
					if self.gm_active == True:
						self.gm_active = False
						self.player.set_hp(self.saved_hp)

				# Method to quit
				elif var == 'quit':
					varQ = self.quit()
					if varQ == 'y':
						os.system('cls' if os.name == 'nt' else 'clear')
						break

				# What to do with an unknown command
				else:
					print("Sorry, that command wasn't recongized.\n\n")

		except AdventureDone:
			pass

	# Method to check info about the current location. Then Prints it.
	def loc(self):
		string = ""
		print("You are currently at house address: {0}{1}\tThe max address is:{2}{3}\n".format(self.player_x_loc, self.player_y_loc, self.neighborhood_width - 1, self.neighborhood_height - 1))
		string = "You can go in these directions: "				
		if(self.player_x_loc > 0):
			string = string + "West "
		if(self.player_y_loc > 0):
			string = string + "North "
		if(self.player_x_loc < self.neighborhood_width - 1):
			string = string + "East "
		if(self.player_y_loc < self.neighborhood_height - 1):
			string = string + "South "
		print(string + "\n")

	# Method to move the player and make checks.
	def move_player(self, direction):
		if direction == 'north':
			if( self.player_y_loc > 0 ):
				self.player_y_loc = self.player_y_loc - 1
			else:
				print("You cannot go North.\n")
		elif direction == 'south':
			if( self.player_y_loc < self.neighborhood_height - 1 ):
				self.player_y_loc = self.player_y_loc + 1
			else:
				print("You cannot go South.\n")
		elif direction == 'east':
			if( self.player_x_loc < self.neighborhood_width - 1):
				self.player_x_loc = self.player_x_loc + 1
			else:
				print("You cannot go East.\n")
		elif direction == 'west':
			if( self.player_x_loc > 0 ):
				self.player_x_loc = self.player_x_loc - 1
			else:
				print("You cannot go West.\n")
		else:
			print("That is an invalid direction.\n")

	# Quit method
	def quit(self):
		print("Are you sure you want to quit? (y / n)")
		var = input(": ")
		return var

	# Updates the game if player has died.
	def update_player(self, player):
		print("YOU HAVE DIED!\nGAME OVER\n")
		raise AdventureDone

	# Updates if the house has lost a monster
	# This seems buggy, and will call corretly, but not all If's are working?
	def update_house(self, house):
		self.num_monsters = self.num_monsters - 1
		if(self.neighborhood[self.player_x_loc][self.player_y_loc].get_num_monsters == 0 and self.neighborhood[self.player_x_loc][self.player_y_loc].get_clear() == False):
			self.neighborhood[self.player_x_loc][self.player_y_loc].clear()
			self.houses_left = self.houses_left - 1

		#Even if I get the numleft to say 0, this won't always return?
		if(self.num_monsters == 0): 
			print("Congratuations, you have survived and saved the Neighborhood!\n")
			print("credit to Prof. Woodring for project inspiration")
			print("credit to the OG Zork for exististing.")
			print("created by Matthew Hager, with minor help from various sources (Stack Exchange).\n\n")
			raise AdventureDone

#Class from https://stackoverflow.com/questions/16073396/breaking-while-loop-with-function 
#to break a loop from within a function.
class AdventureDone(Exception): pass
