import sys
sys.path.append('..')
from Driver import load_data
part, input_type, data_raw, data_lines, data_lines_int = load_data()


# Solution to part 1
def part_1():
    result = 0

    # Get the players' starting positions
    player_1_position = int(data_lines[0].split()[-1])
    player_2_position = int(data_lines[1].split()[-1])

    # Initialize the starting game state
    player_1_points = 0
    player_2_points = 0
    previous_dice_roll = 0

    # Play the game until the first player reaches the points to win the game
    dice_rolls = 0
    points_for_win = 1000
    while True:
        # Roll the dices for player 1
        dice_roll = 0
        for _ in range(3):
            previous_dice_roll += 1
            dice_roll += previous_dice_roll
            dice_rolls += 1
        
        # Update the position of player 1
        player_1_position = (player_1_position + dice_roll - 1)%10 + 1

        # Update the points of player 1 and end this game state in case of a win
        player_1_points += player_1_position
        if player_1_points >= points_for_win:
            break

        # Roll the dices for player 2
        dice_roll = 0
        for _ in range(3):
            previous_dice_roll += 1
            dice_roll += previous_dice_roll
            dice_rolls += 1

        # Update the position of player 2
        player_2_position = (player_2_position + dice_roll - 1)%10 + 1

        # Update the points of player 2 and end this game state in case of a win
        player_2_points += player_2_position
        if player_2_points >= points_for_win:
            break

    # Determine the result
    if player_1_points > player_2_points:
        result = player_2_points*dice_rolls
    else:
        result = player_1_points*dice_rolls

    return result

# Solution to part 2
def part_2():
    result = 0

    # Get the players' starting positions
    player_1_position = int(data_lines[0].split()[-1])
    player_2_position = int(data_lines[1].split()[-1])

    # Initialize the starting game state
    player_1_points = 0
    player_2_points = 0
    game_states = { (player_1_points, player_1_position, player_2_points, player_2_position): 1 }

    # Count the total number of wins for each player
    wins_for_player_1 = 0
    wins_for_player_2 = 0

    # Get all possible sums of three consecutive three-sided dice rolls and their multiplicity
    possible_dice_rolls = [ d1 + d2 + d3 for d1 in range(1,4) for d2 in range(1, 4) for d3 in range(1, 4) ]
    dice_outcomes = {}
    for i in possible_dice_rolls:
        if i not in dice_outcomes:
            dice_outcomes[i] = 1
        else:
            dice_outcomes[i] += 1

    # Play all games in all universes until there are no open games left
    points_for_win = 21
    while len(game_states) > 0:
        # Iterate over all current game states
        new_game_states = {}
        for game_state, game_state_multiplicity in game_states.items():
            
            # Player 1 rolls the dice
            for dice_roll_1, multiplicity_1 in dice_outcomes.items():
                # Update the position of player 1
                player_1_position = (game_state[1] + dice_roll_1 - 1)%10 + 1

                # Update the points of player 1
                player_1_points = game_state[0] + player_1_position

                # End this game state in case of a win
                if player_1_points >= points_for_win:
                    wins_for_player_1 += multiplicity_1*game_state_multiplicity
                    continue
                
                # Player 2 rolls the dice
                for dice_roll_2, multiplicity_2 in dice_outcomes.items():
                    # Update the position of player 2
                    player_2_position = (game_state[3] + dice_roll_2 - 1)%10 + 1
                    
                    # Update the points of player 2
                    player_2_points = game_state[2] + player_2_position

                    # End this game state in case of a win
                    if player_2_points >= points_for_win:
                        wins_for_player_2 += multiplicity_1*multiplicity_2*game_state_multiplicity
                        continue
                    
                    # In case no player wins, add the new game state to the set of open game states
                    curr_game_state = (player_1_points, player_1_position, player_2_points, player_2_position)
                    if curr_game_state in new_game_states:
                        new_game_states[curr_game_state] += multiplicity_1*multiplicity_2*game_state_multiplicity
                    else:
                        new_game_states[curr_game_state] = multiplicity_1*multiplicity_2*game_state_multiplicity

        game_states = new_game_states.copy()

    result = max(wins_for_player_1, wins_for_player_2)

    return result

# Print the result
if part == 1:
    print(part_1())
elif part == 2:
    print(part_2())
