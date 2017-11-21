#######################################################################
# The core code of the Zork game.
# 
# @author Matthew Hager
# @version November 20, 2017
#######################################################################

# Imports for randomizing, and imports the weapons.
from random import uniform
from random import randint
from weapon import Weapon

# The player class; what the player needs to function
class Player:
	# Variables that are the same for all Players.
	max_num_weapons = 10
	attack_power = (10, 20)

	# Initializer for Player, and adds the game as an observer
	def __init__(self, game):
		self.health = 1000
		self.weapons = []
		self.observers = []
		self.randomize_weapons()
		self.register(game)

	# Returns the health of the player
	def get_hp(self):
		return self.health

	# Makes the player take passed in damage
	def take_damage(self, amount):
		self.health = self.health - amount
		if self.health < 0:
			self.notify_game()
	
	# Set hp for godmode/debug purposes.
	def set_hp(self, hp):
		self.health = hp

	# Returns a list of the weapons a player has
	def list_weapons(self):
		list_of_weapons = ""
		for item in self.weapons:
			list_of_weapons = list_of_weapons + item.info()
		return list_of_weapons

	# Randomize the weapons a player starts with, all players have 
	# infinite hershykiss's
	def randomize_weapons(self):
		self.weapons.append(Weapon('hershykiss'))
		for i in range(1,self.max_num_weapons):
			weapon_to_add = randint(1, 3)
			if weapon_to_add == 3:
				self.weapons.append(Weapon('nerdbomb'))
			if weapon_to_add == 2:
				self.weapons.append(Weapon('sourstraws'))
			if weapon_to_add == 1:
				self.weapons.append(Weapon('chocolatebar'))

	# Not used, but if we wanted to add a weapon to the player
	def add_weapon(self):
		if len[weapons] < self.max_num_weapons:
			weapon_to_add = randint(1, 3)
			if weapon_to_add == 3:
				self.weapons.append(Weapon('nerdbomb'))
			if weapon_to_add == 2:
				self.weapons.append(Weapon('sourstraws'))
			if weapon_to_add == 1:
				self.weapons.append(Weapon('chocolatebar'))

	# Uses a weapon, and checks to make sure we have it.
	def use_weapon(self, weapon_type):
		found = False
		attack_roll = randint(self.attack_power[0], self.attack_power[1])
		weapon_dmg = 0.0
		for item in self.weapons:
			if found == False and item.get_type() == weapon_type:
				weapon_dmg = item.roll_damage()
				item.use()
				if item.get_uses() == 0:
					self.weapons.remove(item)
				found = True
		if found == False:
			return -1
		return weapon_dmg * attack_roll

	# Registers an observer
	def register(self, observer):
		if not observer in self.observers:
			self.observers.append(observer)

	# Unregisters an observer
	def unregister(self, observer):
		if observer in self.observers:
			self.observers.remove(observer)

	# Function to notify the observers of an event.
	def notify_game(self):
		for observer in self.observers:
			observer.update_player(self)

