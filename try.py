from dice import six_sided, four_sided, make_test_dice, make_fair_dice
from ucb import main, trace, interact

GOAL_SCORE = 100  # The goal of Hog is to score 100 points.


######################
# Phase 1: Simulator #
######################


def roll_dice(num_rolls, dice=six_sided):
    """Simulate rolling the DICE exactly NUM_ROLLS > 0 times. Return the sum of
    the outcomes unless any of the outcomes is 1. In that case, return 1.

    num_rolls:  The number of dice rolls that will be made.
    dice:       A function that simulates a single dice roll outcome.
    """
    # These assert statements ensure that num_rolls is a positive integer.
    assert type(num_rolls) == int, 'num_rolls must be an integer.'
    assert num_rolls > 0, 'Must roll at least once.'
    # BEGIN PROBLEM 1
    total = 0
    pig_out = 0
    while num_rolls > 0:
        dice_value = dice()
        if dice_value == 1: pig_out = 1
        total = total + dice_value
        num_rolls -= 1
    return 1 if pig_out == 1 else total
    # END PROBLEM 1


def free_bacon(score):
    """Return the points scored from rolling 0 dice (Free Bacon).

    score:  The opponent's current score.
    """
    assert score < 100, 'The game should be over.'
    # BEGIN PROBLEM 2
    cube = score ** 3
    total = 0
    if len(str(cube)) == 1:
        return 1 + cube
    else:
        index = 1
        for i in str(cube):
            if index % 2 == 0:
                # perform subtraction
                total = total - int(i)
            else:
                # perform addition
                total = total + int(i)
            index += 1
        return 1 + abs(total)
    # END PROBLEM 2


def is_swap(player_score, opponent_score):
    """
    Return whether the two scores should be swapped
    """
    # BEGIN PROBLEM 4
    sum_of_scores = player_score + opponent_score
    total = 3 ** sum_of_scores
    return True if str(total)[0] == str(total)[-1] else False
    # END PROBLEM 4


def take_turn(num_rolls, opponent_score, dice=six_sided):
    """Simulate a turn rolling NUM_ROLLS dice, which may be 0 (Free Bacon).
    Return the points scored for the turn by the current player.

    num_rolls:       The number of dice rolls that will be made.
    opponent_score:  The total score of the opponent.
    dice:            A function that simulates a single dice roll outcome.
    """
    # Leave these assert statements here; they help check for errors.
    assert type(num_rolls) == int, 'num_rolls must be an integer.'
    assert num_rolls >= 0, 'Cannot roll a negative number of dice in take_turn.'
    assert num_rolls <= 10, 'Cannot roll more than 10 dice.'
    assert opponent_score < 100, 'The game should be over.'
    # BEGIN PROBLEM 3
    "*** YOUR CODE HERE ***"

    if num_rolls == 0:
        return free_bacon(opponent_score)
    else:
        return roll_dice(num_rolls, dice)

    # END PROBLEM 3


def other(who):
    """Return the other player, for a player WHO numbered 0 or 1.

    >>> other(0)
    1
    >>> other(1)
    0
    """
    return 1 - who


def silence(score0, score1):
    """Announce nothing (see Phase 2)."""
    return silence


def play(strategy0, strategy1, score0=0, score1=0, dice=six_sided,
         goal=GOAL_SCORE, say=silence, feral_hogs=True):
    """Simulate a game and return the final scores of both players, with Player
    0's score first, and Player (2, 0)1's score second.

    A strategy is a function that takes two total scores as arguments (the
    current player's score, and the opponent's score), and returns a number of
    dice that the current player will roll this turn.

    strategy0:  The strategy function for Player 0, who plays first.
    strategy1:  The strategy function for Player 1, who plays second.
    score0:     Starting score for Player 0
    score1:     Starting score for Player 1
    dice:       A function of zero arguments that simulates a dice roll.
    goal:       The game ends and someone wins when this score is reached.
    say:        The commentary function to call at the end of the first turn.
    feral_hogs: A boolean indicating whether the feral hogs rule should be active.
    """
    who = 1  # Who is about to take a turn, 0 (first) or 1 (second)
    previous_score0 = score0
    previous_score01 = score1
    # BEGIN PROBLEM 5,6
    # while score0 <= goal and score1 <= goal:
    if who == 0:
        score, opponent_score, strategy, previous_score = score0, score1, strategy0, previous_score0
    elif who == 1:
        score, opponent_score, strategy, previous_score = score1, score0, strategy1, previous_score01

    num_rolls = 0 # strategy(score, opponent_score)
    add_score = take_turn(num_rolls, opponent_score, dice)

    score += add_score
    # previous_score = score  # Maintaining previous score of player

    if is_swap(score, opponent_score):
        previous_score = score
        score, opponent_score = opponent_score, score

    if feral_hogs:
        if abs(previous_score - num_rolls) == 2:
            previous_score = score
            score += 3

    if who == 0:
        score0, score1, strategy0, previous_score0 = score, opponent_score, strategy, previous_score
    elif who == 1:
        score1, score0, strategy1, previous_score1 = score, opponent_score, strategy, previous_score
    # say = say(score0, score1)
    # who = other(who)

    # END PROBLEM 5,6
    return score0, score1


print(play(lambda x: print(x), lambda x: print(x), 0, 1, 6, 100, silence, True))
