#######################################################################
# The core code of the Zork game.
# 
# @author Matthew Hager
# @version November 20, 2017
#######################################################################

# Imports monster, and random
from random import randint
from monster import Monster

# Class for what the house needs to function
class House:
	# Current value for most monsters that can fit
	max_monsters = 10

	# Initializer for the house
	def __init__(self, game):
		self.num_monsters = randint(1, self.max_monsters);
		self.clear = False
		self.monsters = []
		self.observers = []
		self.num_people = 0
		for i in range(0, self.num_monsters):
			self.monsters.append(Monster(self))
			if self.monsters[i].get_type() == 'person':
				self.num_monsters = self.num_monsters - 1
				self.num_people = self.num_people + 1
		self.register(game)

	# Returns a list of the monsters in the house
	def list_monsters(self):
		listmon	= "There are {0} monsters, and {1} people.\n".format(self.num_monsters, self.num_people)
		num = 0
		for mon in self.monsters:
			listmon = listmon + "m {0} is a {1}\n".format(num, mon.get_type())
			num = num + 1
		listmon = listmon + "\n"
		return listmon

	# Returns state of the house (Buggy/not yet implemented)
	def get_clear():
		return self.clear		

	# Sets state of the house to clear (Buggy/not yet implemented)
	def clear():
		self.clear = True

	# Returns the number of monsters at the house
	def get_num_monsters(self):
		return self.num_monsters

	#Generic function to attack all monsters at once.
	def attack_monsters(self, weapon, dmg):
		for mon in self.monsters:
			mon.take_damage(weapon, dmg)

	#Future function to allow attacking specific monsters.
	#def attack_monsters(self, weapon_used, dmg_rolled):
	#	for mon in self.monsters:
	#		mon.take_damage(weapon_used, dmg_rolled)

	# Rolls all the values for the monster's attacks on player.
	# Note: Persons will automatically heal the player.
	def monsters_attack_player(self):
		amount = 0
		for mon in self.monsters:
			amount = amount + mon.attack()
		return amount

	# Register and observer
	def register(self, observer):
		if not observer in self.observers:
			self.observers.append(observer)

	# Unregister an Observer
	def unregister(self, observer):
		if observer in self.observers:
			self.observers.remove(observer)

	# Update the values after observing something
	def update_monster(self, monster):
		monster.redeemed()
		self.num_monsters = self.num_monsters - 1
		self.num_people = self.num_people + 1
		self.notify_game()

	# Update observers of an event
	def notify_game(self):
		for observer in self.observers:
			observer.update_house(self)
