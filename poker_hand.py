#!/usr/bin/python

from deck_of_cards import Card, DeckOfCards, SUITS, NAMED_VALUES
import random


class Error(Exception):
	pass

class ScoredPokerHandInitializationCardNumberError(Error):
	def __init__(self, msg):
		self.msg = msg

class ScoredPokerHandInitializationCardTypeError(Error):
	def __init__(self, msg):
		self.msg = msg

def cardValueName(value):
	return NAMED_VALUES[value]

class PokerHandScore(object):
	SCORE_CLASS = ["High Card", "Pair", "Two pair", "Three", "Straight", "Flush", "Full house", "Four", "Straight flush", "Royal flush"]

	def __init__(self, score_class, value=0, secondary_value=0, side_cards=[]):
		self.score_class = score_class
		self.value = value
		self.secondary_value = secondary_value
		self.side_cards = side_cards

	def score_tuple(self):
		return (self.score_class, self.value, self.secondary_value) + tuple( card.value for card in self.side_cards )

	def __cmp__(self, other):
		return cmp( self.score_tuple(), other.score_tuple )

	def score_message(self, suit=None):
		message = ""
		if self.score_class == 9:
			message = self.SCORE_CLASS[self.score_class] + " in " + suit
		elif self.score_class == 8:
			message = self.SCORE_CLASS[self.score_class] + " in " + suit + ", " + cardValueName(self.value) + " high"
		elif self.score_class == 7:
			message = self.SCORE_CLASS[self.score_class] + " " + cardValueName(self.value) + "s, "
		elif self.score_class == 6:
			message = self.SCORE_CLASS[self.score_class] + ": " + cardValueName(self.value) + "s full of " + cardValueName(self.secondary_value) + "s"
		elif self.score_class == 5:
			message = self.SCORE_CLASS[self.score_class] + " in " + suit + ", " + cardValueName(self.value) + " high, "
		elif self.score_class == 4:
			message = self.SCORE_CLASS[self.score_class] + ", " + cardValueName(self.value) + " high"
		elif self.score_class == 3:
			message = self.SCORE_CLASS[self.score_class] + " " + cardValueName(self.value) + "s, "
		elif self.score_class == 2:
			message = self.SCORE_CLASS[self.score_class] + ": " + cardValueName(self.value) + "s over " + cardValueName(self.secondary_value) + "s, "
		elif self.score_class == 1:
			message = self.SCORE_CLASS[self.score_class] + " of " + cardValueName(self.value) + "s, "
		elif self.score_class == 0:
			message = self.SCORE_CLASS[self.score_class] + ": " + cardValueName(self.value) + " high, "

		if len(self.side_cards) == 1:
			message += cardValueName(self.side_cards[0].value) + " kicker"
		elif len(self.side_cards) > 1:
			if len(self.side_cards) == 5:
				for card in self.side_cards[1:]:	
					message += cardValueName(card.value) + ", "
			else:
				for card in self.side_cards:	
					message += cardValueName(card.value) + ", "

			message = message[0:-2] + " side cards"

		return message
			
				

class ScoredPokerHand(object):

	def __init__(self, list_of_cards):
		if len(list_of_cards) != 7:
			raise ScoredPokerHandInitializationCardNumberError('Expected 7 cards, was given ' + str(len(list_of_cards)))
		for card in list_of_cards:
			if not isinstance(card, Card):
				raise ScoredPokerHandInitializationCardTypeError('Expected elements of type Card, found element of type ' + str(type(card)))

		self.played_cards = []
		self.unplayed_cards = []

		list_of_cards.sort()
		self.list_of_cards = list_of_cards
		list_of_suits = [card.suit for card in list_of_cards]
		list_of_values = [card.value for card in list_of_cards]
		list_of_values.sort()		

		self.score = None

		# scoring variables
		flush = False
		straight = 0
		pair = 0
		second_pair = 0
		three_kind = 0
		four_kind = 0
		full_house = False
		self.high_card = list_of_cards[0].value
		self.second_high_card = list_of_cards[1].value
		self.third_high_card = list_of_cards[2].value
		self.fourth_high_card = list_of_cards[3].value
		self.fifth_high_card = list_of_cards[4].value
		self.flush_suit = None

		for suit in SUITS:
			if list_of_suits.count(suit) > 4:
				flush = True
				self.flush_suit = suit
		
		for value in xrange(2,15):
			if list_of_values.count(value) == 4:
				four_kind = value
			if list_of_values.count(value) == 3:
				three_kind = value
			if list_of_values.count(value) == 2:
				second_pair = pair
				pair = value

		for value in list_of_values:
			if (value+1 in list_of_values and value+2 in list_of_values and value+3 in list_of_values):
				if (value == 2 and 15 in list_of_values):
					straight = value + 3
				elif (value+4 in list_of_values):
					straight = value + 4

		if three_kind > 0 and pair > 0:
			full_house = True

		if straight > 0 and flush:
			for value in xrange(straight-2, straight+1):
				possible_straight_flush = [card for card in list_of_cards
							   if card.suit == self.flush_suit and card.value in range(value-4,value+1)]

				if len(possible_straight_flush) == 5:
					possible_straight_flush.sort()
					straight = value
					self.played_cards = possible_straight_flush[:]
					self.unplayed_cards = [card for card in list_of_cards if card not in possible_straight_flush]

					if straight == 14:
						self.score = PokerHandScore(9)
					else:
						self.score = PokerHandScore(8, value=straight)
			if self.score:
				return

		if four_kind > 0:
			if self.high_card == four_kind:
				self.high_card = self.fifth_high_card

			high_card = [card for card in list_of_cards if card.value == self.high_card][0:1]
			
			self.played_cards = [card for card in list_of_cards if card.value == four_kind]
			self.played_cards.append(high_card[0])
			self.unplayed_cards = [card for card in list_of_cards if card not in self.played_cards]
			self.score = PokerHandScore(7, value=four_kind, side_cards=high_card)
		elif full_house:
			self.unplayed_cards = [card for card in list_of_cards if card.value != three_kind and card.value != pair]
			self.played_cards = [card for card in list_of_cards if card.value == three_kind]
			self.played_cards += [card for card in list_of_cards if card.value == pair]
			self.score = PokerHandScore(6, value=three_kind, secondary_value=pair)

		elif flush:
			flush_cards = [card for card in list_of_cards if card.suit == self.flush_suit]
			flush_cards.sort()

			self.played_cards = flush_cards[0:5]
			self.unplayed_cards = [card for card in list_of_cards if card not in self.played_cards]
			self.score = PokerHandScore(5, value=self.played_cards[0].value, side_cards=self.played_cards)

		elif straight > 0:
			self.played_cards = [card for card in list_of_cards if card.value <= straight and card.value > straight-5]

			while len(self.played_cards) > 5:
				card_to_remove = None
				straight_values = [card.value for card in self.played_cards]
				for i in xrange(straight-4,straight+1):
					if straight_values.count(i) > 1:
						card_to_remove = self.played_cards[straight_values.index(i)]
						break

				self.played_cards.remove(card_to_remove)

			self.unplayed_cards = [card for card in list_of_cards if card not in self.played_cards]
			self.score = PokerHandScore(4, value=straight)

		elif three_kind > 0:
			self.played_cards = [card for card in list_of_cards if card.value == three_kind]
			self.unplayed_cards = [card for card in list_of_cards if card not in self.played_cards]
			side_cards = self.unplayed_cards[0:2]
			self.played_cards += side_cards
			self.unplayed_cards = self.unplayed_cards[2:]			
			self.score = PokerHandScore(3, value=three_kind, side_cards=side_cards)

		elif second_pair > 0:
			self.played_cards = [card for card in list_of_cards if card.value == second_pair or card.value == pair]
			self.unplayed_cards = [card for card in list_of_cards if card not in self.played_cards]
			side_cards = self.unplayed_cards[0:1]
			self.played_cards += side_cards
			self.unplayed_cards = self.unplayed_cards[1:]			
			self.score = PokerHandScore(2, value=pair, secondary_value=second_pair, side_cards=side_cards)	

		elif pair > 0:
			self.played_cards = [card for card in list_of_cards if card.value == pair]
			self.unplayed_cards = [card for card in list_of_cards if card not in self.played_cards]
			side_cards = self.unplayed_cards[0:3]
			self.played_cards += side_cards
			self.unplayed_cards = self.unplayed_cards[3:]			
			self.score = PokerHandScore(1, value=pair, secondary_value=second_pair, side_cards=side_cards)

		else:
			self.played_cards = list_of_cards[0:5]
			self.unplayed_cards = [card for card in list_of_cards if card not in self.played_cards]
			self.score = PokerHandScore(0, value=self.played_cards[0].value, side_cards=self.played_cards)

	def score_message(self):
		return self.score.score_message(suit=self.flush_suit)

	def compare(self, scored_poker_hand):
		return cmp(self.score, scored_poker_hand.score)
