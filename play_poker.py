#!/usr/bin/python

from deck_of_cards import *
from poker_hand import *

def play_poker():
	deck_of_cards = DeckOfCards()
	player_1_hand = deck_of_cards.draw_cards(2)
	player_2_hand = deck_of_cards.draw_cards(2)
	table = deck_of_cards.draw_cards(5)

	print "Player 1's hand: "
	for card in player_1_hand:
		print(card)

	print "Player 2's hand: "
	for card in player_2_hand:
		print(card)

	print "The table: "
	for card in table:
		print(card)

	player_1_full_hand = table[:]
	player_1_full_hand.append(player_1_hand[0])
	player_1_full_hand.append(player_1_hand[1])

	player_2_full_hand = table[:]
	player_2_full_hand.append(player_2_hand[0])
	player_2_full_hand.append(player_2_hand[1])

	player_1_scored_hand = ScoredPokerHand(player_1_full_hand)
	player_2_scored_hand = ScoredPokerHand(player_2_full_hand)

	print "Player 1's score:", player_1_scored_hand.score_message()
	print "Player 2's score:", player_2_scored_hand.score_message()

	if player_1_scored_hand > player_2_scored_hand:
		print "Player 1 wins!"
	elif player_1_scored_hand < player_2_scored_hand:
		print "Player 2 wins!"
	else:
		print "Tie Game"
	
	
		

	
play_poker();
	





