#!/usr/bin/python

import random

SUITS = ['Clubs','Diamonds','Hearts', 'Spades']
NAMED_VALUES = [None, None, 'Two', 'Three' , 'Four', 'Five', 'Six', 'Seven', 'Eight', 'Nine', 'Ten', 'Jack', 'Queen', 'King', 'Ace']

class Error(Exception):
	pass

class CardInitializationError(Error):
	def __init__(self, msg):
		self.msg = msg

class CardComparisonError(Error):
	def __init__(self, msg):
		self.msg = msg

class DeckOfCardsEmptyError(Error):
	def __init__(self, msg):
		self.msg = msg

def generateDeck():
	for suit in SUITS:
		for num in xrange(2,15):
			yield Card(suit,num)

class Card(object):
	
	def __init__(self,suit,value):

		if suit not in SUITS:
			raise CardInitializationError('Expected suit in {0}, observed value: {1}'.format(str(SUITS), str(suit)))

		if value < 2 or value > 14:
			raise CardInitializationError('Expected value to integer between 2 and 14, observed value: {0}'.format(str(value)))

		self.suit = suit
		self.value = value

	def __str__(self):
		if self.value < 11:
			return str(self.value) + self.suit[0]
		else:
			return str(NAMED_VALUES[self.value][0]) + self.suit[0] 

	def __cmp__(self, other):
		if not isinstance(other, Card):
			raise CardComparisonError('Attempted to compare Card to {0}'.format(str(type(other))))

		return -cmp((self.value, self.suit), (other.value, other.suit))


class DeckOfCards(object):

	def __init__(self):
		self.cards_left= [card for card in generateDeck()]

	def num_of_cards(self):
		return len(self.cards_left)

	def draw_card(self):
		if self.num_of_cards():
			new_card = random.choice(self.cards_left)	
			self.cards_left.remove(new_card)
			return new_card
		else:
			raise DeckOfCardsEmptyError('Attempted to draw a card from an empty deck')

	def draw_cards(self, num):
		if self.num_of_cards() >= num:
			new_cards = random.sample(self.cards_left, num)
			for new_card in new_cards:	
				self.cards_left.remove(new_card)
			return new_cards
		else:
			raise DeckOfCardsEmptyError('Attempted to draw {0} card(s) from a deck of {1} card(s)'.format(str(num),  str(self.num_of_cards())))

