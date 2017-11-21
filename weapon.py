#######################################################################
# The weapon code for the Zork game.
# 
# @author Matthew Hager
# @version November 20, 2017
#######################################################################

# Imports uniform for random floats
from random import uniform

# The Weapon class, everything that a weapon needs relevant to Zork.
class Weapon:
	weapon_types = {'hershykiss':(1.0, 1.0), 'nerdbomb':(3.5, 5.0), 'sourstraws':(1.0, 1.75), 'chocolatebar':(2.0, 2.4)} 
	def __init__(self, weapon_type):
		self.weapon_type = weapon_type
		self.num_uses = -1
		if weapon_type == 'nerdbomb':
			self.num_uses = 1
		if weapon_type == 'sourstraws':
			self.num_uses = 2
		if weapon_type == 'chocolatebar':
			self.num_uses = 4

	# Returns the random damage multiplier for an attack.
	def roll_damage(self):
		dmg = uniform(self.weapon_types[self.weapon_type][0], self.weapon_types[self.weapon_type][1])
		return dmg

	# Returns a string that is the info of the weapon.
	def info(self):
		info_string = ""		
		if self.weapon_type == 'hershykiss':
			info_string = "{0} Has multipliers between {1} and {2}.\n".format(self.weapon_type, self.weapon_types[self.weapon_type][0], self.weapon_types[self.weapon_type][1])
			return info_string 
		info_string = "{0} Has multipliers between {1} and {2}.\n\t\tthis has {3} uses left.\n".format(self.weapon_type, self.weapon_types[self.weapon_type][0], self.weapon_types[self.weapon_type][1], self.num_uses)
		return info_string

	# Returns the weapon type.
	def get_type(self):
		return self.weapon_type

	# Returns number of uses a weapon has left.
	def get_uses(self):
		return self.num_uses

	# Decrements the number of uses when used.
	def use(self):
		self.num_uses = self.num_uses - 1
