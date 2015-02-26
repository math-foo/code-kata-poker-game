#!/usr/bin/python

import deck_of_cards
import poker_hand
import unittest

def cardCreator(suit, value):
	return deck_of_cards.Card(deck_of_cards.SUITS[suit], value)

def cardListCreator(list_suit_value_tuples):
	return [cardCreator(suit, value) for (suit, value) in list_suit_value_tuples]

class testScoredPokerHandInit(unittest.TestCase):
	def setUp(self):
		self.list_of_cards = cardListCreator([(0,2),(1,4),(2,6),(3,8),(0,10),(1,12),(2,14)])

	def test_initCardNumLow(self):
		self.list_of_cards.pop()
		self.assertRaises(poker_hand.ScoredPokerHandInitializationCardNumberError, poker_hand.ScoredPokerHand, self.list_of_cards)

	def test_initCardNumHigh(self):
		self.list_of_cards.append(cardCreator(3, 3))
		self.assertRaises(poker_hand.ScoredPokerHandInitializationCardNumberError, poker_hand.ScoredPokerHand, self.list_of_cards)

	def test_initCardTypeError(self):
		self.list_of_cards.pop()
		self.list_of_cards.append("Not a card")
		self.assertRaises(poker_hand.ScoredPokerHandInitializationCardTypeError, poker_hand.ScoredPokerHand, self.list_of_cards)

	def test_initSuccessful(self):
		scored_poker_hand = poker_hand.ScoredPokerHand(self.list_of_cards)
		self.assertEquals(scored_poker_hand.high_card, 14)


class testScoredPokerHand(unittest.TestCase):
	def test_RoyalFlush(self):
		royal_flush = cardListCreator([(0,14),(0,13),(0,12),(0,11),(0,10),(1,2),(2,3)])
		royal_flush_hand = poker_hand.ScoredPokerHand(royal_flush)

		self.assertEquals(9, royal_flush_hand.score.score_class)

		expected_played_cards = cardListCreator([(0,14),(0,13),(0,12),(0,11),(0,10)])
		expected_unplayed_cards = cardListCreator([(2,3),(1,2)])

		self.assertEquals(expected_played_cards, royal_flush_hand.played_cards)
		self.assertEquals(expected_unplayed_cards, royal_flush_hand.unplayed_cards)

	def test_StraightFlush(self):
		straight_flush = cardListCreator([(2,13),(2,12),(2,11),(2,10),(2,9),(1,2),(0,3)])
		straight_flush_hand = poker_hand.ScoredPokerHand(straight_flush)

		self.assertEquals(8, straight_flush_hand.score.score_class)
		self.assertEquals(13, straight_flush_hand.score.value)

		expected_played_cards = cardListCreator([(2,13),(2,12),(2,11),(2,10),(2,9)])
		expected_unplayed_cards = cardListCreator([(0,3),(1,2)])

		self.assertEquals(expected_played_cards, straight_flush_hand.played_cards)
		self.assertEquals(expected_unplayed_cards, straight_flush_hand.unplayed_cards)

	def test_LoweredStraightFlush(self):
		straight_flush = cardListCreator([(0,14),(1,13),(1,12),(1,11),(1,10),(1,9),(1,8)])
		straight_flush_hand = poker_hand.ScoredPokerHand(straight_flush)

		self.assertEquals(8, straight_flush_hand.score.score_class)
		self.assertEquals(13, straight_flush_hand.score.value)

		expected_played_cards = cardListCreator([(1,13),(1,12),(1,11),(1,10),(1,9)])
		expected_unplayed_cards = cardListCreator([(0,14),(1,8)])

		self.assertEquals(expected_played_cards, straight_flush_hand.played_cards)
		self.assertEquals(expected_unplayed_cards, straight_flush_hand.unplayed_cards)

	def test_FourOfAKind(self):
		four_of_a_kind = cardListCreator([(3,7),(3,13),(3,2),(1,11),(0,11),(2,11),(3,11)])
		four_hand = poker_hand.ScoredPokerHand(four_of_a_kind)

		expected_side_cards =  cardListCreator([(3,13)])
		
		self.assertEquals(7, four_hand.score.score_class)
		self.assertEquals(11, four_hand.score.value)
		self.assertEquals(expected_side_cards, four_hand.score.side_cards)

		expected_played_cards =  cardListCreator([(3,11),(2,11),(1,11),(0,11),(3,13)])
		expected_unplayed_cards =  cardListCreator([(3,7),(3,2)])

		self.assertEquals(expected_played_cards, four_hand.played_cards)
		self.assertEquals(expected_unplayed_cards, four_hand.unplayed_cards)

	def test_FourOfAKindLowKicker(self):
		four_of_a_kind = cardListCreator([(3,7),(3,8),(3,2),(1,11),(0,11),(2,11),(3,11)])
		four_hand = poker_hand.ScoredPokerHand(four_of_a_kind)

		expected_side_cards =  cardListCreator([(3,8)])
		
		self.assertEquals(7, four_hand.score.score_class)
		self.assertEquals(11, four_hand.score.value)
		self.assertEquals(expected_side_cards, four_hand.score.side_cards)

		expected_played_cards =  cardListCreator([(3,11),(2,11),(1,11),(0,11),(3,8)])
		expected_unplayed_cards =  cardListCreator([(3,7),(3,2)])

		self.assertEquals(expected_played_cards, four_hand.played_cards)
		self.assertEquals(expected_unplayed_cards, four_hand.unplayed_cards)

	def test_FullHouse(self):
		full_house = cardListCreator([(3,7),(0,7),(3,2),(1,7),(0,6),(2,2),(3,5)])
		full_house_hand = poker_hand.ScoredPokerHand(full_house)

		self.assertEquals(6, full_house_hand.score.score_class)
		self.assertEquals(7, full_house_hand.score.value)
		self.assertEquals(2, full_house_hand.score.secondary_value)

		expected_played_cards = cardListCreator([(3,7),(1,7),(0,7),(3,2),(2,2)])
		expected_unplayed_cards = cardListCreator([(0,6),(3,5)])

		self.assertEquals(expected_played_cards, full_house_hand.played_cards)
		self.assertEquals(expected_unplayed_cards, full_house_hand.unplayed_cards)

	def test_Flush(self):
		flush = cardListCreator([(3,7),(0,7),(3,2),(3,11),(3,6),(2,2),(3,5)])
		flush_hand = poker_hand.ScoredPokerHand(flush)

		expected_side_cards = cardListCreator([(3,11),(3,7),(3,6),(3,5),(3,2)])
		
		self.assertEquals(5, flush_hand.score.score_class)
		self.assertEquals(11, flush_hand.score.value)
		self.assertEquals(expected_side_cards, flush_hand.score.side_cards)

		expected_played_cards =  cardListCreator([(3,11),(3,7),(3,6),(3,5),(3,2)])
		expected_unplayed_cards =  cardListCreator([(0,7),(2,2)])

		self.assertEquals(expected_played_cards, flush_hand.played_cards)
		self.assertEquals(expected_unplayed_cards, flush_hand.unplayed_cards)

	def test_AllFlush(self):
		flush = cardListCreator([(3,7),(3,4),(3,2),(3,11),(3,8),(3,3),(3,5)])
		flush_hand = poker_hand.ScoredPokerHand(flush)

		expected_side_cards = cardListCreator([(3,11),(3,8),(3,7),(3,5),(3,4)])
		
		self.assertEquals(5, flush_hand.score.score_class)
		self.assertEquals(11, flush_hand.score.value)
		self.assertEquals(expected_side_cards, flush_hand.score.side_cards)

		expected_played_cards =  cardListCreator([(3,11),(3,8),(3,7),(3,5),(3,4)])
		expected_unplayed_cards =  cardListCreator([(3,3),(3,2)])

		self.assertEquals(expected_played_cards, flush_hand.played_cards)
		self.assertEquals(expected_unplayed_cards, flush_hand.unplayed_cards)

	def test_Straight(self):
		straight = cardListCreator([(2,10),(2,9),(1,8),(0,7),(2,6),(3,4),(2,2)])
		straight_hand = poker_hand.ScoredPokerHand(straight)

		self.assertEquals(4, straight_hand.score.score_class)
		self.assertEquals(10, straight_hand.score.value)

		expected_played_cards =  cardListCreator([(2,10),(2,9),(1,8),(0,7),(2,6)])
		expected_unplayed_cards = cardListCreator([(3,4),(2,2)])

		self.assertEquals(expected_played_cards, straight_hand.played_cards)
		self.assertEquals(expected_unplayed_cards, straight_hand.unplayed_cards)

	def test_StraightOnePair(self):
		straight = cardListCreator([(2,10),(2,9),(1,8),(0,7),(2,6),(3,9),(2,2)])
		straight_hand = poker_hand.ScoredPokerHand(straight)

		self.assertEquals(4, straight_hand.score.score_class)
		self.assertEquals(10, straight_hand.score.value)

		expected_played_cards =  cardListCreator([(2,10),(2,9),(1,8),(0,7),(2,6)])
		expected_unplayed_cards = cardListCreator([(3,9),(2,2)])

		self.assertEquals(expected_played_cards, straight_hand.played_cards)
		self.assertEquals(expected_unplayed_cards, straight_hand.unplayed_cards)

	def test_StraightThree(self):
		straight = cardListCreator([(2,10),(2,9),(1,8),(0,7),(2,6),(3,9),(1,9)])
		straight_hand = poker_hand.ScoredPokerHand(straight)

		self.assertEquals(4, straight_hand.score.score_class)
		self.assertEquals(10, straight_hand.score.value)

		expected_played_cards =  cardListCreator([(2,10),(1,9),(1,8),(0,7),(2,6)])
		expected_unplayed_cards = cardListCreator([(3,9),(2,9)])

		self.assertEquals(expected_played_cards, straight_hand.played_cards)
		self.assertEquals(expected_unplayed_cards, straight_hand.unplayed_cards)

	def test_StraightTwoPair(self):
		straight = cardListCreator([(2,10),(2,9),(1,8),(0,7),(2,6),(3,10),(1,9)])
		straight_hand = poker_hand.ScoredPokerHand(straight)

		self.assertEquals(4, straight_hand.score.score_class)
		self.assertEquals(10, straight_hand.score.value)

		expected_played_cards =  cardListCreator([(2,10),(1,9),(1,8),(0,7),(2,6)])
		expected_unplayed_cards = cardListCreator([(3,10),(2,9)])

		self.assertEquals(expected_played_cards, straight_hand.played_cards)
		self.assertEquals(expected_unplayed_cards, straight_hand.unplayed_cards)

	def test_ThreeOfAKindHighSide(self):
		three_of_a_kind = cardListCreator([(1,2),(3,13),(3,2),(1,11),(2,2),(2,9),(3,6)])
		three_hand = poker_hand.ScoredPokerHand(three_of_a_kind)

		expected_side_cards =  cardListCreator([(3,13),(1,11)])
		
		self.assertEquals(3, three_hand.score.score_class)
		self.assertEquals(2, three_hand.score.value)
		self.assertEquals(expected_side_cards, three_hand.score.side_cards)

		expected_played_cards =  cardListCreator([(3,2),(2,2),(1,2),(3,13),(1,11)])
		expected_unplayed_cards =  cardListCreator([(2,9),(3,6)])

		self.assertEquals(expected_played_cards, three_hand.played_cards)
		self.assertEquals(expected_unplayed_cards, three_hand.unplayed_cards)

	def test_ThreeOfAKindLowSide(self):
		three_of_a_kind = cardListCreator([(1,13),(3,13),(3,2),(1,11),(2,13),(2,9),(3,6)])
		three_hand = poker_hand.ScoredPokerHand(three_of_a_kind)

		expected_side_cards =  cardListCreator([(1,11),(2,9)])
		
		self.assertEquals(3, three_hand.score.score_class)
		self.assertEquals(13, three_hand.score.value)
		self.assertEquals(expected_side_cards, three_hand.score.side_cards)

		expected_played_cards =  cardListCreator([(3,13),(2,13),(1,13),(1,11),(2,9)])
		expected_unplayed_cards =  cardListCreator([(3,6),(3,2)])

		self.assertEquals(expected_played_cards, three_hand.played_cards)
		self.assertEquals(expected_unplayed_cards, three_hand.unplayed_cards)

	def test_ThreeOfAKindMixedSide(self):
		three_of_a_kind = cardListCreator([(3,13),(3,11),(2,7),(1,11),(0,11),(2,9),(3,6)])
		three_hand = poker_hand.ScoredPokerHand(three_of_a_kind)

		expected_side_cards =  cardListCreator([(3,13),(2,9)])
		
		self.assertEquals(3, three_hand.score.score_class)
		self.assertEquals(11, three_hand.score.value)
		self.assertEquals(expected_side_cards, three_hand.score.side_cards)

		expected_played_cards =  cardListCreator([(3,11),(1,11),(0,11),(3,13),(2,9)])
		expected_unplayed_cards =  cardListCreator([(2,7),(3,6)])

		self.assertEquals(expected_played_cards, three_hand.played_cards)
		self.assertEquals(expected_unplayed_cards, three_hand.unplayed_cards)

	def test_TwoPairHighKicker(self):
		two_pair = cardListCreator([(3,2),(3,8),(3,5),(1,5),(2,7),(2,9),(3,7)])
		two_pair_hand = poker_hand.ScoredPokerHand(two_pair)

		expected_side_cards =  cardListCreator([(2,9)])
		
		self.assertEquals(2, two_pair_hand.score.score_class)
		self.assertEquals(7, two_pair_hand.score.value)
		self.assertEquals(5, two_pair_hand.score.secondary_value)
		self.assertEquals(expected_side_cards, two_pair_hand.score.side_cards)

		expected_played_cards =  cardListCreator([(3,7),(2,7),(3,5),(1,5),(2,9)])
		expected_unplayed_cards =  cardListCreator([(3,8),(3,2)])

		self.assertEquals(expected_played_cards, two_pair_hand.played_cards)
		self.assertEquals(expected_unplayed_cards, two_pair_hand.unplayed_cards)

	def test_TwoPairMidKicker(self):
		two_pair = cardListCreator([(3,2),(3,4),(3,5),(1,5),(2,7),(2,6),(3,7)])
		two_pair_hand = poker_hand.ScoredPokerHand(two_pair)

		expected_side_cards =  cardListCreator([(2,6)])
		
		self.assertEquals(2, two_pair_hand.score.score_class)
		self.assertEquals(7, two_pair_hand.score.value)
		self.assertEquals(5, two_pair_hand.score.secondary_value)
		self.assertEquals(expected_side_cards, two_pair_hand.score.side_cards)

		expected_played_cards =  cardListCreator([(3,7),(2,7),(3,5),(1,5),(2,6)])
		expected_unplayed_cards =  cardListCreator([(3,4),(3,2)])

		self.assertEquals(expected_played_cards, two_pair_hand.played_cards)
		self.assertEquals(expected_unplayed_cards, two_pair_hand.unplayed_cards)

	def test_TwoPairLowKicker(self):
		two_pair = cardListCreator([(3,2),(3,4),(3,10),(1,10),(2,12),(2,6),(3,12)])
		two_pair_hand = poker_hand.ScoredPokerHand(two_pair)

		expected_side_cards =  cardListCreator([(2,6)])
		
		self.assertEquals(2, two_pair_hand.score.score_class)
		self.assertEquals(12, two_pair_hand.score.value)
		self.assertEquals(10, two_pair_hand.score.secondary_value)
		self.assertEquals(expected_side_cards, two_pair_hand.score.side_cards)

		expected_played_cards =  cardListCreator([(3,12),(2,12),(3,10),(1,10),(2,6)])
		expected_unplayed_cards =  cardListCreator([(3,4),(3,2)])

		self.assertEquals(expected_played_cards, two_pair_hand.played_cards)
		self.assertEquals(expected_unplayed_cards, two_pair_hand.unplayed_cards)

	def test_Pair(self):
		pair = cardListCreator([(3,2),(3,8),(3,5),(1,4),(2,8),(2,9),(3,7)])
		pair_hand = poker_hand.ScoredPokerHand(pair)

		expected_side_cards =  cardListCreator([(2,9),(3,7),(3,5)])
		
		self.assertEquals(1, pair_hand.score.score_class)
		self.assertEquals(8, pair_hand.score.value)
		self.assertEquals(expected_side_cards, pair_hand.score.side_cards)

		expected_played_cards =  cardListCreator([(3,8),(2,8),(2,9),(3,7),(3,5)])
		expected_unplayed_cards =  cardListCreator([(1,4),(3,2)])
		self.assertEquals(expected_played_cards, pair_hand.played_cards)
		self.assertEquals(expected_unplayed_cards, pair_hand.unplayed_cards)

	def test_HighCard(self):
		ace_high = cardListCreator([(3,2),(0,14),(0,5),(1,4),(2,8),(2,9),(3,7)])
		ace_high_hand = poker_hand.ScoredPokerHand(ace_high)

		expected_side_cards = cardListCreator([(0,14),(2,9),(2,8),(3,7),(0,5)])
		
		self.assertEquals(0, ace_high_hand.score.score_class)
		self.assertEquals(14, ace_high_hand.score.value)
		self.assertEquals(expected_side_cards, ace_high_hand.score.side_cards)

		expected_played_cards =  cardListCreator([(0,14),(2,9),(2,8),(3,7),(0,5)])
		expected_unplayed_cards =  cardListCreator([(1,4),(3,2)])

		self.assertEquals(expected_played_cards, ace_high_hand.played_cards)
		self.assertEquals(expected_unplayed_cards, ace_high_hand.unplayed_cards)


class testScoredPokerHandScoreMessage(unittest.TestCase):
	def test_RoyalFlush(self):
		royal_flush = cardListCreator([(0,14),(0,13),(0,12),(0,11),(0,10),(1,2),(2,3)])
		royal_flush_hand = poker_hand.ScoredPokerHand(royal_flush)

		self.assertEquals("Royal flush in Clubs", royal_flush_hand.score_message())

	def test_StraightFlush(self):
		straight_flush = cardListCreator([(2,13),(2,12),(2,11),(2,10),(2,9),(1,2),(0,3)])
		straight_flush_hand = poker_hand.ScoredPokerHand(straight_flush)

		self.assertEquals("Straight flush in Hearts, King high", straight_flush_hand.score_message())

	def test_LowerStraightFlush(self):
		straight_flush = cardListCreator([(0,14),(1,13),(1,12),(1,11),(1,10),(1,9),(1,8)])
		straight_flush_hand = poker_hand.ScoredPokerHand(straight_flush)

		self.assertEquals("Straight flush in Diamonds, King high", straight_flush_hand.score_message())

	def test_FourOfAKind(self):
		four_of_a_kind = cardListCreator([(3,7),(3,13),(3,2),(1,11),(0,11),(2,11),(3,11)])
		four_hand = poker_hand.ScoredPokerHand(four_of_a_kind)

		self.assertEquals("Four Jacks, King kicker", four_hand.score_message())

	def test_FullHouse(self):
		full_house = cardListCreator([(3,7),(0,7),(3,2),(1,7),(0,6),(2,2),(3,5)])
		full_house_hand = poker_hand.ScoredPokerHand(full_house)

		self.assertEquals("Full house: Sevens full of Twos", full_house_hand.score_message())

	def test_Flush(self):
		flush = cardListCreator([(3,7),(0,7),(3,2),(3,11),(3,6),(2,2),(3,5)])
		flush_hand = poker_hand.ScoredPokerHand(flush)

		self.assertEquals("Flush in Spades, Jack high, Seven, Six, Five, Two side cards", flush_hand.score_message())

	def test_Straight(self):
		straight = cardListCreator([(2,10),(2,9),(1,8),(0,7),(2,6),(3,4),(2,2)])
		straight_hand = poker_hand.ScoredPokerHand(straight)

		self.assertEquals("Straight, Ten high", straight_hand.score_message())

	def test_ThreeOfAKind(self):
		three_of_a_kind = cardListCreator([(1,2),(3,13),(3,2),(1,11),(2,2),(2,9),(3,6)])
		three_hand = poker_hand.ScoredPokerHand(three_of_a_kind)

		self.assertEquals("Three Twos, King, Jack side cards", three_hand.score_message())

	def test_TwoPair(self):
		two_pair = cardListCreator([(3,2),(3,8),(3,5),(1,5),(2,7),(2,9),(3,7)])
		two_pair_hand = poker_hand.ScoredPokerHand(two_pair)

		self.assertEquals("Two pair: Sevens over Fives, Nine kicker", two_pair_hand.score_message())

	def test_Pair(self):
		pair = cardListCreator([(3,2),(3,8),(3,5),(1,4),(2,8),(2,9),(3,7)])
		pair_hand = poker_hand.ScoredPokerHand(pair)

		self.assertEquals("Pair of Eights, Nine, Seven, Five side cards", pair_hand.score_message())

	def test_HighCard(self):
		ace_high = cardListCreator([(3,2),(3,14),(3,5),(1,4),(2,8),(2,9),(3,7)])
		ace_high_hand = poker_hand.ScoredPokerHand(ace_high)

		self.assertEquals("High Card: Ace high, Nine, Eight, Seven, Five side cards", ace_high_hand.score_message())



if __name__ == '__main__':
    unittest.main()
