#######################################################################
# The core code of the Zork game.
# 
# @author Matthew Hager
# @version November 20, 2017
#######################################################################

# Imports for ranomizing
from random import randint

# Class for the monsters/persons
class Monster:
	# Universal Monster variables to hold stats.
	monster_health = { 'person':(100, 100), 'zombie':(50, 100), 'vampire':(100, 200), 'ghoul':(40, 80), 'werewolf':(200, 200) }
	monster_dmg = { 'person':(-20, -1), 'zombie':(0, 10), 'vampire':(10, 20), 'ghoul':(15, 30), 'werewolf':(0, 40) }

	# Initializer
	def __init__ (self, house):
		self.health = 0.0
		self.monster_type = ''
		self.observers = []
		self.randomize_monster()
		self.register(house)

	# Returns monster type (string)
	def get_type(self):
		return self.monster_type

	# Return monster's health
	def get_hp(self):
		return self.health

	# Randomize a value of an attack towards a player
	def attack(self):
		dmg = randint(self.monster_dmg[self.monster_type][0], self.monster_dmg[self.monster_type][1])
		return dmg

	# Damage incoming from the player, adjusted based on weapon type
	def take_damage(self, weapon_used, dmg_rolled):
		if self.monster_type == 'person':
			pass
		elif self.monster_type == 'zombie':
			self.health = self.health - dmg_rolled
			if weapon_used == 'sourstraws':
				self.health = self.health - dmg_rolled
		elif self.monster_type == 'vampire':
			if weapon_used == 'chocolatebar':
				pass
			else:
				self.health = self.health - dmg_rolled
		elif self.monster_type == 'ghoul':
			self.health = self.health - dmg_rolled
			if weapon_used == 'nerdbomb':
				self.health = self.health - (4 * dmg_rolled)
		elif self.monster_type == 'werewolf':
			if weapon_used == 'chocolatebar' or weapon_used == 'sourstraws':
				pass
			else:
				self.health = self.health - dmg_rolled
		
		#Notifies the house when a monster dies.
		if self.health <= 0:
			self.notify_house()

	# Function call to redeem a monster that was killed
	def redeemed(self):
		self.monster_type = 'person'
		self.health = 100.0

	# Randomizes a monster's stats (Inefficent, but left alone for now)
	def randomize_monster(self):
		type_of_monster = randint(0, 4)
		if type_of_monster == 0:
			self.monster_type = 'person'
			self.health = randint(self.monster_health[self.monster_type][0], self.monster_health[self.monster_type][1])
		if type_of_monster == 1:
			self.monster_type = 'zombie'
			self.health = randint(self.monster_health[self.monster_type][0], self.monster_health[self.monster_type][1])
		if type_of_monster == 2:
			self.monster_type = 'vampire'
			self.health = randint(self.monster_health[self.monster_type][0], self.monster_health[self.monster_type][1])
		if type_of_monster == 3:
			self.monster_type = 'ghoul'
			self.health = randint(self.monster_health[self.monster_type][0], self.monster_health[self.monster_type][1])
		if type_of_monster == 4:
			self.monster_type = 'werewolf'
			self.health = randint(self.monster_health[self.monster_type][0], self.monster_health[self.monster_type][1])

	# Registers an observer
	def register(self, observer):
		if not observer in self.observers:
			self.observers.append(observer)

	# Unregisters an observer
	def unregister(self, observer):
		if observer in self.observers:
			self.observers.remove(observer)

	# Notifies observers of event
	def notify_house(self): #Notify method
		for observer in self.observers:
			observer.update_monster(self)
