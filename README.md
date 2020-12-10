# Wild Jacks/Sequence Game

This repo contains the implementation of a simple Q-learning with linear approximator to play Wild/Jacks or Sequence game.

Sequence is an abstract strategy game played with a board and 2 decks of cards. The game can be played either individually or in teams of two/three players cooperating without discussing strategies. Each turn player plays a card in hand by placing a chip on the corresponding space on the board. The objective of the game is to form sequences of poker chips. Single eyed Jacks are used to remove opponent's chips and double eyed Jacks are used to place chips in any location. The players need to form strategies to make their sequences and stop the opponents from making sequences.

## Running the code

Run the code using `python sequence.py`

Current implentaion supports only board sizes 5x5 and 9x9.

### References
* https://en.wikipedia.org/wiki/Sequence_(game)
* https://play.google.com/store/apps/details?id=com.sonicgame.jacks
