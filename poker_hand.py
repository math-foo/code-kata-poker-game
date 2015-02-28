#!/usr/bin/python

from collections import defaultdict
from deck_of_cards import Card, DeckOfCards, SUITS, NAMED_VALUES


class Error(Exception):
	pass

class ScoredPokerHandInitializationCardNumberError(Error):
	def __init__(self, msg):
		self.msg = msg

class ScoredPokerHandInitializationCardTypeError(Error):
	def __init__(self, msg):
		self.msg = msg

class ScoredPokerHandInitializationCardUniquenessError(Error):
	def __init__(self, msg):
		self.msg = msg

class PokerHandScoreInitializationRangeError(Error):
	def __init__(self, msg):
		self.msg = msg

class PokerHandScoreInitializationSideCardError(Error):
	def __init__(self, msg):
		self.msg = msg

class PokerHandScoreInitializationScoreClassError(Error):
	def __init__(self, msg):
		self.msg = msg

def cardValueName(value):
	return NAMED_VALUES[value]

def createHistograms(list_of_values):
	histogram = defaultdict(int)
	for value in list_of_values:
		histogram[value] += 1

	inverse_histogram = defaultdict(list)
	for key,val in histogram.items():
		inverse_histogram[val].append(key)

	return histogram, inverse_histogram

class PokerHandScore(object):
	SCORE_CLASS = ["High Card", "Pair", "Two pair", "Three", "Straight", "Flush", "Full house", "Four", "Straight flush", "Royal flush"]

	def __init__(self, score_class, value=0, secondary_value=0, side_cards=[]):
		if score_class < 0 or score_class > 9:
			raise PokerHandScoreInitializationRangeError("score_class must be between 0 and 9, actual value: " + str(score_class))
		self.score_class = score_class

		
		if value < 0 or value > 14 or value == 1:
			raise PokerHandScoreInitializationRangeError("value must be 0 or between 2 and 14, actual value: " + str(value))
		self.value = value


		if secondary_value < 0 or secondary_value > 14 or secondary_value == 1:
			raise PokerHandScoreInitializationRangeError("secondary_value must be 0 or between 2 and 14, actual value: " + str(secondary_value))
		self.secondary_value = secondary_value
		
		num_of_side_cards = len(side_cards)

		if num_of_side_cards > 5 or num_of_side_cards == 4:
			raise PokerHandScoreInitializationSideCardError("There must be, 0,1,2,3 or 5 side cards, found " + str(len(side_cards)) + " side_cards")
		for card in side_cards:
			if not isinstance(card, Card):
				raise PokerHandScoreInitializationSideCardError("All side_cards must be of type Card, found element of type " + str(type(card)))
		self.side_cards = side_cards

		if num_of_side_cards == 5:
			if self.score_class not in [5,0]:
				raise PokerHandScoreInitializationScoreClassError("5 side cards can only occur with " + SCORE_CLASS[0] + " and " + SCORE_CLASS[5] +
										  " hands, seen with a " + SCORE_CALSSS[self.score_class] + " hand")
		elif num_of_side_cards == 3:
			if self.score_class != 1:
				raise PokerHandScoreInitializationScoreClassError("3 side cards can only occur with a " + SCORE_CLASS[1] +
										  " hand, seen with a " + SCORE_CALSSS[self.score_class] + " hand")
		elif num_of_side_cards == 2:
			if self.score_class != 3:
				raise PokerHandScoreInitializationScoreClassError("2 side cards can only occur with a " + SCORE_CLASS[3] +
										  " of a kind hand, seen with a " + SCORE_CALSSS[self.score_class] + " hand")
		elif num_of_side_cards == 1:
			if self.score_class not in [7,2]:
				raise PokerHandScoreInitializationScoreClassError("1 side card can only occur with a " + SCORE_CLASS[7] + " of a kind and " +
										  SCORE_CLASS[2] + " hands, seen with a " + SCORE_CALSSS[self.score_class] + " hand")
		elif num_of_side_cards == 0:
			if self.score_class not in [4,6,8,9]:
				raise PokerHandScoreInitializationScoreClassError("No side cards cannot occur with a " + SCORE_CLASS[self.core_class] + " hand")

		if value > 0 and secondary_value > 0:
			if self.score_class not in [2,6]:
				raise PokerHandScoreInitializationScoreClassError("value > 0 and secondary_value> 0 can only occur with " + SCORE_CLASS[2] + " and " + SCORE_CLASS[6] +
										  " hands, seen with a " + SCORE_CALSSS[self.score_class] + " hand")
		elif secondary_value > 0:
			raise PokerHandScoreInitializationScoreClassError("secondary_value should not be non-zero with value equal to 0")
		elif value > 0:
			if self.score_class in [2,6]:
				raise PokerHandScoreInitializationScoreClassError("secondary_value must be non-zero for a " + SCORE_CLASS[self.core_class] + " hand")
			elif self.score_class == 9:
				raise PokerHandScoreInitializationScoreClassError("value must be zero for a " + SCORE_CLASS[self.core_class] + " hand")
		else:
			if self.score_class != 9:
				raise PokerHandScoreInitializationScoreClassError("value can only be 0 with " + SCORE_CLASS[9] + " hand, seen with a " +
										  SCORE_CALSSS[self.score_class] + " hand")
				
		

	def score_tuple(self):
		return (self.score_class, self.value, self.secondary_value) + tuple( card.value for card in self.side_cards )

	def __cmp__(self, other):
		return cmp( self.score_tuple(), other.score_tuple )

	def score_message(self, suit=None):
		# add checks that suit is a suit
		# add checks that classes that need suits get them

		# All messages start with the score class name
		message = self.SCORE_CLASS[self.score_class]
		if self.score_class == 9:
			message += " in " + suit
		elif self.score_class == 8:
			message += " in " + suit + ", " + cardValueName(self.value) + " high"
		elif self.score_class == 7:
			message += " " + cardValueName(self.value) + "s, "
		elif self.score_class == 6:
			message += ": " + cardValueName(self.value) + "s full of " + cardValueName(self.secondary_value) + "s"
		elif self.score_class == 5:
			message += " in " + suit + ", " + cardValueName(self.value) + " high, "
		elif self.score_class == 4:
			message += ", " + cardValueName(self.value) + " high"
		elif self.score_class == 3:
			message += " " + cardValueName(self.value) + "s, "
		elif self.score_class == 2:
			message += ": " + cardValueName(self.value) + "s over " + cardValueName(self.secondary_value) + "s, "
		elif self.score_class == 1:
			message += " of " + cardValueName(self.value) + "s, "
		elif self.score_class == 0:
			message += ": " + cardValueName(self.value) + " high, "

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
			raise ScoredPokerHandInitializationCardNumberError('Expected 7 cards, was given {}'.format( len(list_of_cards)))
		for card in list_of_cards:
			if not isinstance(card, Card):
				raise ScoredPokerHandInitializationCardTypeError('Expected elements of type Card, found element of type ' + str(type(card)))

		self.played_cards = []
		self.unplayed_cards = []

		list_of_cards = self.list_of_cards = sorted( list_of_cards )

		for card in list_of_cards:
			if list_of_cards.count(card) > 1:
				raise ScoredPokerHandInitializationCardUniquenessError('Expected all cards unique, found two instance of ' + str(card))
		
		value_histogram, inverse_value_histogram = createHistograms([card.value for card in list_of_cards])
		suit_histogram, inverse_suit_histogram = createHistograms([card.suit for card in list_of_cards])

		self.score = None
		self.flush_suit = None
		flush = False

		if any(x in inverse_suit_histogram for x in xrange(5,8)):
			flush = True
			self.flush_suit = [inverse_suit_histogram[x][0] for x in xrange(5,8) if x in inverse_suit_histogram][0]

		straight_high = 0

		list_of_values = value_histogram.keys()

		for value in value_histogram.keys():
			if all( v in value_histogram.keys() for v in xrange(value+1, value+4) ):
				if (value == 2 and 14 in list_of_values):
					straight_high = value + 3
				elif (value+4 in list_of_values):
					straight_high = value + 4

		if straight_high > 0 and flush:
			for value in xrange(straight_high-2, straight_high+1):
				possible_straight_flush = [card for card in list_of_cards
							   if card.suit == self.flush_suit and card.value in xrange(value-4,value+1)]

				if value == 5:
					possible_straight_flush += [card for card in list_of_cards
							   	    if card.suit == self.flush_suit and card.value == 14]

				if len(possible_straight_flush) == 5:
					straight_high = value
					self.played_cards = possible_straight_flush[:]
					self.unplayed_cards = [card for card in list_of_cards if card not in possible_straight_flush]

					if straight_high == 14:
						self.score = PokerHandScore(9)
					else:
						self.score = PokerHandScore(8, value=straight_high)
			if self.score:
				return

		if 4 in inverse_value_histogram:
			value = inverse_value_histogram[4][-1]

			self.played_cards = [card for card in list_of_cards if card.value == value]
			self.unplayed_cards = [card for card in list_of_cards if card not in self.played_cards]
			high_card = self.unplayed_cards[0:1]

			self.played_cards.append(high_card[0])
			self.unplayed_cards = self.unplayed_cards[1:]
			self.score = PokerHandScore(7, value=value, side_cards=high_card)
		elif 3 in inverse_value_histogram and 2 in inverse_value_histogram:
			three_value = inverse_value_histogram[3][-1]
			pair_value = inverse_value_histogram[2][-1]
			self.unplayed_cards = [card for card in list_of_cards if card.value != three_value and card.value != pair_value]
			self.played_cards = [card for card in list_of_cards if card.value == three_value]
			self.played_cards += [card for card in list_of_cards if card.value == pair_value]
			self.score = PokerHandScore(6, value=three_value, secondary_value=pair_value)

		elif flush:
			flush_cards = [card for card in list_of_cards if card.suit == self.flush_suit]

			self.played_cards = flush_cards[0:5]
			self.unplayed_cards = [card for card in list_of_cards if card not in self.played_cards]
			self.score = PokerHandScore(5, value=self.played_cards[0].value, side_cards=self.played_cards)

		elif straight_high > 0:
			self.played_cards = [card for card in list_of_cards
					     if card.value <= straight_high and card.value > straight_high-5]

			if straight_high == 5:
				self.unplayed_cards = [card for card in list_of_cards if card not in self.played_cards]
				self.played_cards += self.unplayed_cards[0:1]
				self.unplayed_cards = self.unplayed_cards[1:]

			while len(self.played_cards) > 5:
				card_to_remove = None
				straight_values = [card.value for card in self.played_cards]
				for i in xrange(straight_high-4,straight_high+1):
					if straight_values.count(i) > 1:
						card_to_remove = self.played_cards[straight_values.index(i)]
						break

				self.played_cards.remove(card_to_remove)

			self.unplayed_cards = [card for card in list_of_cards if card not in self.played_cards]
			self.score = PokerHandScore(4, value=straight_high)

		elif 3 in inverse_value_histogram > 0:
			value = inverse_value_histogram[3][-1]

			self.played_cards = [card for card in list_of_cards if card.value == value]
			self.unplayed_cards = [card for card in list_of_cards if card not in self.played_cards]
			side_cards = self.unplayed_cards[0:2]
			self.played_cards += side_cards
			self.unplayed_cards = self.unplayed_cards[2:]			
			self.score = PokerHandScore(3, value=value, side_cards=side_cards)

		elif 2 in inverse_value_histogram and len(inverse_value_histogram[2]) > 1:
			pair_value = inverse_value_histogram[2][-1]
			second_pair_value = inverse_value_histogram[2][-2]

			self.played_cards = [card for card in list_of_cards if card.value == second_pair_value or card.value == pair_value]
			self.unplayed_cards = [card for card in list_of_cards if card not in self.played_cards]
			side_cards = self.unplayed_cards[0:1]
			self.played_cards += side_cards
			self.unplayed_cards = self.unplayed_cards[1:]			
			self.score = PokerHandScore(2, value=pair_value, secondary_value=second_pair_value, side_cards=side_cards)	

		elif 2 in inverse_value_histogram:
			value = inverse_value_histogram[2][-1]

			self.played_cards = [card for card in list_of_cards if card.value == value]
			self.unplayed_cards = [card for card in list_of_cards if card not in self.played_cards]
			side_cards = self.unplayed_cards[0:3]
			self.played_cards += side_cards
			self.unplayed_cards = self.unplayed_cards[3:]			
			self.score = PokerHandScore(1, value=value, side_cards=side_cards)

		else:
			self.played_cards = list_of_cards[0:5]
			self.unplayed_cards = [card for card in list_of_cards if card not in self.played_cards]
			self.score = PokerHandScore(0, value=self.played_cards[0].value, side_cards=self.played_cards)

	def score_message(self):
		return self.score.score_message(suit=self.flush_suit)

	def __cmp__(self, scored_poker_hand):
		return cmp(self.score, scored_poker_hand.score)
