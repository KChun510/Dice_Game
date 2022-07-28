"""The Game of Hog."""

from dice import four_sided, six_sided, make_test_dice
from ucb import main, trace, log_current_line, interact

GOAL_SCORE = 100 # The goal of Hog is to score 100 points.

######################
# Phase 1: Simulator #
######################

# Taking turns

def roll_dice(num_rolls, dice):
    """Roll DICE for NUM_ROLLS times.  Return either the sum of the outcomes,
    or 1 if a 1 is rolled (Pig out). This calls DICE exactly NUM_ROLLS times.

    num_rolls:  The number of dice rolls that will be made; at least 1.
    dice:       A zero-argument function that returns an integer outcome.
    """
    # These assert statements ensure that num_rolls is a positive integer.
    assert type(num_rolls) == int, 'num_rolls must be an integer.'
    assert num_rolls > 0, 'Must roll at least once.'
    
    point = 0
    flag = False
    counter = 0
    while num_rolls > 0:
        curr = dice()
        if curr == 1:
            flag = True
        else:
            point += curr
        num_rolls -= 1
    
    if flag:
        return 1
    else:
        return point



def take_turn(num_rolls, opponent_score, dice = six_sided):
    """Simulate a turn rolling NUM_ROLLS dice, which may be 0 (Free bacon).

    num_rolls:       The number of dice rolls that will be made.
    opponent_score:  The total score of the opponent.
    dice:            A function of no args that returns an integer outcome.
    """
    assert type(num_rolls) == int, 'num_rolls must be an integer.'
    assert num_rolls >= 0, 'Cannot roll a negative number of dice.'
    assert num_rolls <= 10, 'Cannot roll more than 10 dice.'
    assert opponent_score < 100, 'The game should be over.'
    "*** YOUR CODE HERE ***"

    if num_rolls == 0:                       #will always be pigout rule for turn 1
        return free_bacon (opponent_score)
    else: 
        return roll_dice (num_rolls, dice)

def swine_swap (score, opponent_score):
    if (score * 2 == opponent_score or opponent_score * 2 == score):
        return opponent_score, score
    else:
        return score, opponent_score 
        
def free_bacon (opponent_score):
    digit_a = opponent_score // 10
    digit_b = opponent_score % 10
    return (max(digit_a, digit_b)+1)
    
    

# Playing a game

def select_dice(score, opponent_score):
    """Select six-sided dice unless the sum of SCORE and OPPONENT_SCORE is a
    multiple of 7, in which case select four-sided dice (Hog wild).

    >>> select_dice(4, 24) == four_sided
    True
    >>> select_dice(16, 64) == six_sided
    True
    >>> select_dice(0, 0) == four_sided
    True
    """
    "*** YOUR CODE HERE ***"

    if ((score + opponent_score) % 7 == 0):    #This is the hogwild appliation.
        a = four_sided
        return a
    else: 
        b = six_sided
        return b

def other(who):
    """Return the other player, for a player WHO numbered 0 or 1.

    >>> other(0)
    1
    >>> other(1)
    0
    """
    return 1 - who

def play(strategy0, strategy1, goal=GOAL_SCORE):
    """Simulate a game and return the final scores of both players, with
    Player 0's score first, and Player 1's score second.

    A strategy is a function that takes two total scores as arguments
    (the current player's score, and the opponent's score), and returns a
    number of dice that the current player will roll this turn.

    strategy0:  The strategy function for Player 0, who plays first.
    strategy1:  The strategy function for Player 1, who plays second.
    """
    who = 0  # Which player is about to take a turn, 0 (first) or 1 (second)
    score0, score1 = 0, 0
    "*** YOUR CODE HERE ***"
    while score0 < goal and score1 < goal:
        if other(who) == 1:
            num_rolls = strategy0(score0, score1)
            score0 += take_turn(num_rolls, score1, dice = select_dice(score0, score1))
            score0, score1 = swine_swap(score0, score1)
            who += 1

        elif other(who) == 0:
            num_rolls = strategy1(score0, score1)
            score1 += take_turn(num_rolls, score0, dice = select_dice(score0, score1))
            score0, score1 = swine_swap(score0, score1)
            who -= 1
        
    return score0, score1   # You may wish to change this line.



#######################
# Phase 2: Strategies #
#######################

# Basic Strategy

BASELINE_NUM_ROLLS = 5
BACON_MARGIN = 8

def always_roll(n):
    """Return a strategy that always rolls N dice.

    A strategy is a function that takes two total scores as arguments
    (the current player's score, and the opponent's score), and returns a
    number of dice that the current player will roll this turn.

    >>> strategy = always_roll(5)
    >>> strategy(0, 0)
    5
    >>> strategy(99, 99)
    5
    """
    def strategy(score, opponent_score):
        return n
    return strategy

# Experiments

def make_averaged(fn, num_samples=1000):
    """Return a function that returns the average_value of FN when called.

    To implement this function, you will have to use *args syntax, a new Python
    feature introduced in this project.  See the project description.

    >>> dice = make_test_dice(3, 1, 5, 6)
    >>> averaged_dice = make_averaged(dice, 1000)
    >>> averaged_dice()
    3.75
    >>> make_averaged(roll_dice, 1000)(2, dice)
    6.0

    In this last example, two different turn scenarios are averaged.
    - In the first, the player rolls a 3 then a 1, receiving a score of 1.
    - In the other, the player rolls a 5 and 6, scoring 11.
    Thus, the average value is 6.0.
    """
    "*** YOUR CODE HERE ***"
    
    def num(*args):
        aver = 0
        i = 0
        while i < num_samples:
            aver += fn(*args)
            i += 1
        return aver / num_samples

    return num

def max_scoring_num_rolls(dice=six_sided):
    """Return the number of dice (1 to 10) that gives the highest average turn
    score by calling roll_dice with the provided DICE.  Print all averages as in
    the doctest below.  Assume that dice always returns positive outcomes.

    >>> dice = make_test_dice(3)
    >>> max_scoring_num_rolls(dice)
    1 dice scores 3.0 on average
    2 dice scores 6.0 on average
    3 dice scores 9.0 on average
    4 dice scores 12.0 on average
    5 dice scores 15.0 on average
    6 dice scores 18.0 on average
    7 dice scores 21.0 on average
    8 dice scores 24.0 on average
    9 dice scores 27.0 on average
    10 dice scores 30.0 on average
    10
    """
    "*** YOUR CODE HERE ***"
    i = 1
    highAv = -1
    dice = 1
    while i <= 10:
       average =  make_averaged(roll_dice, num_samples=1000)(i, dice)
       print (i , " dice scores ", average , " on average ")
       if average > highAv:
        highAv = average
        dice = i

       i += 1
    return dice



def winner(strategy0, strategy1):
    """Return 0 if strategy0 wins against strategy1, and 1 otherwise."""
    score0, score1 = play(strategy0, strategy1)
    if score0 > score1:
        return 0
    else:
        return 1

def average_win_rate(strategy, baseline=always_roll(BASELINE_NUM_ROLLS)):
    """Return the average win rate (0 to 1) of STRATEGY against BASELINE."""
    win_rate_as_player_0 = 1 - make_averaged(winner)(strategy, baseline)
    win_rate_as_player_1 = make_averaged(winner)(baseline, strategy)
    return (win_rate_as_player_0 + win_rate_as_player_1) / 2 # Average results

def run_experiments():
    """Run a series of strategy experiments and report results."""
    if False: # Change to False when done finding max_scoring_num_rolls
        six_sided_max = max_scoring_num_rolls(six_sided)
        print('Max scoring num rolls for six-sided dice:', six_sided_max)
        four_sided_max = max_scoring_num_rolls(four_sided)
        print('Max scoring num rolls for four-sided dice:', four_sided_max)

    if False: # Change to True to test always_roll(8)
        print('always_roll(8) win rate:', average_win_rate(always_roll(8)))

    if False: # Change to True to test bacon_strategy
        print('bacon_strategy win rate:', average_win_rate(bacon_strategy))

    if False: # Change to True to test swap_strategy
        print('swap_strategy win rate:', average_win_rate(swap_strategy))

    if True: # Change to True to test final_strategy
        print('final_strategy win rate:', average_win_rate(final_strategy))

    "*** You may add additional experiments as you wish ***"

# Strategies

def bacon_strategy(score, opponent_score):
    """This strategy rolls 0 dice if that gives at least BACON_MARGIN points,
    and rolls BASELINE_NUM_ROLLS otherwise.

    >>> bacon_strategy(0, 0)
    5
    >>> bacon_strategy(70, 50)
    5
    >>> bacon_strategy(50, 70)
    0
    """
    "*** YOUR CODE HERE ***"
    if free_bacon(opponent_score) >= BACON_MARGIN:
        return 0
    else:
        return BASELINE_NUM_ROLLS


def swap_strategy(score, opponent_score):
    """This strategy rolls 0 dice when it would result in a beneficial swap and
    rolls BASELINE_NUM_ROLLS if it would result in a harmful swap. It also rolls
    0 dice if that gives at least BACON_MARGIN points and rolls
    BASELINE_NUM_ROLLS otherwise.

    >>> swap_strategy(23, 60) # 23 + (1 + max(6, 0)) = 30: Beneficial swap
    0
    >>> swap_strategy(27, 18) # 27 + (1 + max(1, 8)) = 36: Harmful swap
    5
    >>> swap_strategy(50, 80) # (1 + max(8, 0)) = 9: Lots of free bacon
    0
    >>> swap_strategy(12, 12) # Baseline
    5
    """
    "*** YOUR CODE HERE ***"
    a, b = score, opponent_score
    if (free_bacon(b) + a) * 2 == b:
        return 0
    elif (free_bacon(b) + a) != 2*b and free_bacon(b) >= BACON_MARGIN:
        return 0
    else:
        return BASELINE_NUM_ROLLS
    
    return 5 # Replace this statement

def final_strategy(score, opponent_score):
    """Write a brief description of your final strategy."""
    """
    *** YOUR DESCRIPTION HERE ***
    
    if (free_bacon(opponent_score) + score) is a multiple of 7, do freebacon.
    This will cause of hog wild, forcing opponent use 4 side dice.

    elif my score < opponent: try swap_strategy. If swap_strategy is un-benificial and returns num_rolls,
    next try bacon_strategy.

    bacon_stratgy if benificial, will do freebacon.
    if not benificial, bacon_stratgy will return BASELINE_NUM_ROLLS

    """
  
    "*** YOUR CODE HERE ***"
    

    #if hog_wild == true. Do bacon strat, hog_wild decrease chance of roll 1.
    if opponent_score + score % 7 == 0:
        if free_bacon(opponent_score) >= 4:     
            return 0
        else:
            return 3
    
    #losing
    elif score < opponent_score: 
        a = swap_strategy(score, opponent_score)
        
        # swap_strategy, has 2 possible return values
        if a ==  BASELINE_NUM_ROLLS:
            return bacon_strategy(score, opponent_score)

        elif a == 0:
            return 0 
    
        #Forcing swine swop, rolling 10 i.e 1
        elif (score + 1) * 2 == opponent_score:
            return 10

        #Forcing swine swap, through free_bacon
        elif (free_bacon(opponent_score) + score) * 2 == opponent_score:
            return 0


    
    #Winning
    elif score > opponent_score:



        #A check for possible swap, then if none bacon_strategy
        if (opponent_score * 2) != (free_bacon(opponent_score) + score):
            return bacon_strategy(score, opponent_score)

        #if freebacon will cause hogwild, do freebacon.
        elif ((free_bacon(opponent_score) + score) + opponent_score) % 7 == 0:
            return 0

        #if adding 1 to score forces hogwild.
        elif opponent_score + (score + 1) % 7 == 0:
            return 10


    #Taking less rolls, as score gets higher.
    elif score > opponent_score and score > 82:
        a = bacon_strategy(score, opponent_score)
        if a == BASELINE_NUM_ROLLS:
            return 4
    
    elif score > opponent_score and score > 88:
        a = bacon_strategy(score, opponent_score)
        if a == BASELINE_NUM_ROLLS:
            return 3
    
    elif score > opponent_score and score > 93:
        a = bacon_strategy(score, opponent_score)
        if a == BASELINE_NUM_ROLLS:
            return 2

    
    
   


    
    return BASELINE_NUM_ROLLS

##########################
# Command Line Interface #
##########################

# Note: Functions in this section do not need to be changed.  They use features
#       of Python not yet covered in the course.

def get_int(prompt, min):
    """Return an integer greater than or equal to MIN, given by the user."""
    choice = input(prompt)
    while not choice.isnumeric() or int(choice) < min:
        print('Please enter an integer greater than or equal to', min)
        choice = input(prompt)
    return int(choice)

def interactive_dice():
    """A dice where the outcomes are provided by the user."""
    return get_int('Result of dice roll: ', 1)

def make_interactive_strategy(player):
    """Return a strategy for which the user provides the number of rolls."""
    prompt = 'Number of rolls for Player {0}: '.format(player)
    def interactive_strategy(score, opp_score):
        if player == 1:
            score, opp_score = opp_score, score
        print(score, 'vs.', opp_score)
        choice = get_int(prompt, 0)
        return choice
    return interactive_strategy

def roll_dice_interactive():
    """Interactively call roll_dice."""
    num_rolls = get_int('Number of rolls: ', 1)
    turn_total = roll_dice(num_rolls, interactive_dice)
    print('Turn total:', turn_total)

def take_turn_interactive():
    """Interactively call take_turn."""
    num_rolls = get_int('Number of rolls: ', 0)
    opp_score = get_int('Opponent score: ', 0)
    turn_total = take_turn(num_rolls, opp_score, interactive_dice)
    print('Turn total:', turn_total)

def play_interactive():
    """Interactively call play."""
    strategy0 = make_interactive_strategy(0)
    strategy1 = make_interactive_strategy(1)
    score0, score1 = play(strategy0, strategy1)
    print('Final scores:', score0, 'to', score1)

@main
def run(*args):
    """Read in the command-line argument and calls corresponding functions.

    This function uses Python syntax/techniques not yet covered in this course.
    """
    import argparse
    parser = argparse.ArgumentParser(description="Play Hog")
    parser.add_argument('--interactive', '-i', type=str,
                        help='Run interactive tests for the specified question')
    parser.add_argument('--run_experiments', '-r', action='store_true',
                        help='Runs strategy experiments')
    args = parser.parse_args()

    if args.interactive:
        test = args.interactive + '_interactive'
        if test not in globals():
            print('To use the -i option, please choose one of these:')
            print('\troll_dice', '\ttake_turn', '\tplay', sep='\n')
            exit(1)
        try:
            globals()[test]()
        except (KeyboardInterrupt, EOFError):
            print('\nQuitting interactive test')
            exit(0)
    elif args.run_experiments:
        run_experiments()
