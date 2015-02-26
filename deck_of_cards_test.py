#!/usr/bin/python

import deck_of_cards
import unittest

class testGenerateDeck(unittest.TestCase):

	def setUp(self):
		self.deck = [card for card in deck_of_cards.generateDeck()]

	def test_length(self):
		self.assertEqual(52, len(self.deck))

	def test_unique(self):
		while self.deck:
			drawn_card = self.deck.pop()
			self.assertFalse(any([card.value == drawn_card.value and card.suit == drawn_card.suit for card in self.deck]))

class testCard(unittest.TestCase):

	def test_init(self):
		card = deck_of_cards.Card('Clubs', 4)

		self.assertEqual(card.suit, 'Clubs')
		self.assertEqual(card.value, 4)

	def test_initLowValueNegative(self):
		self.assertRaises(deck_of_cards.CardInitializationError, deck_of_cards.Card, 'Hearts', -3)

	def test_initLowValueZero(self):
		self.assertRaises(deck_of_cards.CardInitializationError, deck_of_cards.Card, 'Diamonds', 0)

	def test_initLowValueOne(self):
		self.assertRaises(deck_of_cards.CardInitializationError, deck_of_cards.Card, 'Spades', 1)

	def test_initHighValue(self):
		self.assertRaises(deck_of_cards.CardInitializationError, deck_of_cards.Card, 'Clubs', 15)

	def test_initBadSuit(self):
		self.assertRaises(deck_of_cards.CardInitializationError, deck_of_cards.Card, 'Wands', 7)

	def test_strClubs(self):
		card = deck_of_cards.Card('Clubs', 4)
		self.assertEquals('4C', str(card))

	def test_strDiamonds(self):
		card = deck_of_cards.Card('Diamonds', 2)
		self.assertEquals('2D', str(card))

	def test_strHearts(self):
		card = deck_of_cards.Card('Hearts', 7)
		self.assertEquals('7H', str(card))

	def test_strSpades(self):
		card = deck_of_cards.Card('Spades', 9)
		self.assertEquals('9S', str(card))

	def test_strAce(self):
		card = deck_of_cards.Card('Clubs', 14)
		self.assertEquals('AC', str(card))

	def test_strKing(self):
		card = deck_of_cards.Card('Diamonds', 13)
		self.assertEquals('KD', str(card))

	def test_strQueen(self):
		card = deck_of_cards.Card('Hearts', 12)
		self.assertEquals('QH', str(card))

	def test_strJack(self):
		card = deck_of_cards.Card('Spades', 11)
		self.assertEquals('JS', str(card))

	def test_strTen(self):
		card = deck_of_cards.Card('Spades', 10)
		self.assertEquals('10S', str(card))

	def test_cmpError(self):
		card_1 = deck_of_cards.Card('Hearts', 3)

		self.assertRaises(deck_of_cards.CardComparisonError, card_1.__cmp__, "foo")

	def test_cmpEqual(self):
		card_1 = deck_of_cards.Card('Hearts', 3)
		card_2 = deck_of_cards.Card('Hearts', 3)

		self.assertEquals(card_1, card_2)

	def test_cmpSuitBigger(self):
		card_1 = deck_of_cards.Card('Hearts', 3)
		card_2 = deck_of_cards.Card('Diamonds', 3)

		self.assertTrue(card_1 < card_2)

	def test_cmpSuitSmaller(self):
		card_1 = deck_of_cards.Card('Hearts', 3)
		card_2 = deck_of_cards.Card('Spades', 3)

		self.assertTrue(card_1 > card_2)

	def test_cmpValueBigger(self):
		card_1 = deck_of_cards.Card('Hearts', 3)
		card_2 = deck_of_cards.Card('Hearts', 2)

		self.assertTrue(card_1 < card_2)

	def test_cmpValueSmaller(self):
		card_1 = deck_of_cards.Card('Hearts', 3)
		card_2 = deck_of_cards.Card('Hearts', 10)

		self.assertTrue(card_1 > card_2)

	def test_cmpValueSmallerSuitBigger(self):
		card_1 = deck_of_cards.Card('Hearts', 3)
		card_2 = deck_of_cards.Card('Clubs', 10)

		self.assertTrue(card_1 > card_2)

	def test_cmpVlueBiggerSuitSmaller(self):
		card_1 = deck_of_cards.Card('Hearts', 3)
		card_2 = deck_of_cards.Card('Spades', 2)

		self.assertTrue(card_1 < card_2)


class testDeckOfCard(unittest.TestCase):
	def setUp(self):
		self.deck_of_cards = deck_of_cards.DeckOfCards()

	def test_init(self):
		self.assertEquals(len(self.deck_of_cards.cards_left), 52)

	def test_numOfCardsInit(self):
		self.assertEquals(self.deck_of_cards.num_of_cards(), 52)

	def test_numOfCardsFewer(self):
		self.deck_of_cards.cards_left = self.deck_of_cards.cards_left[10:20]
		self.assertEquals(self.deck_of_cards.num_of_cards(), 10)

	def test_numOfCardsNone(self):
		self.deck_of_cards.cards_left = []
		self.assertEquals(self.deck_of_cards.num_of_cards(), 0)

	def test_drawCardNum(self):
		card = self.deck_of_cards.draw_card()

		self.assertEquals(self.deck_of_cards.num_of_cards(), 51)

	def test_drawCardRemoved(self):
		drawn_card = self.deck_of_cards.draw_card()

		self.assertFalse(any(card.value == drawn_card.value and card.suit == drawn_card.suit
				     for card in self.deck_of_cards.cards_left))

	def test_drawCardEmptyDeck(self):
		self.deck_of_cards.cards_left = []
		self.assertRaises(deck_of_cards.DeckOfCardsEmptyError, self.deck_of_cards.draw_card)

	def test_drawCardsNum(self):
		drawn_cards = self.deck_of_cards.draw_cards(10)

		self.assertEquals(len(drawn_cards), 10)
		self.assertEquals(self.deck_of_cards.num_of_cards(), 42)

	def test_drawCardsRemoved(self):
		drawn_cards = self.deck_of_cards.draw_cards(10)

		for drawn_card in drawn_cards:
			self.assertFalse(any(drawn_card.value == card.value and drawn_card.suit == card.suit
					     for card in self.deck_of_cards.cards_left))

	def test_drawCardsNegative(self):
		self.assertRaises(ValueError, self.deck_of_cards.draw_cards, -3)

	def test_drawCardsEmptyDeck(self):
		self.deck_of_cards.cards_left = self.deck_of_cards.cards_left[10:20]
		self.assertRaises(deck_of_cards.DeckOfCardsEmptyError, self.deck_of_cards.draw_cards, 12)


if __name__ == '__main__':
    unittest.main()
