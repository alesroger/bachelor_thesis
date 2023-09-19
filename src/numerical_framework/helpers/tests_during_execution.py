def test_reached_probabilities(game):
    """
    Tests if the reached probabilities for all states of a timestep sum up to 1

    Parameters
    ----------
    game : Game
        object containing all details when a publisher and a user are playing optimally against each other

    Raises
    -------
    Exception
        if reached probabilities for all states of a timestep don't sum up to 1
    """
    t = game.n_max - 1
    while t >= game.user_type.arrival_time - 1:
        total_prob_reached_in_timestep = 0
        for user_state in game.user_states[t]:
            total_prob_reached_in_timestep += user_state.probability_state_is_reached
        if round(total_prob_reached_in_timestep, 4) != 1:
            raise Exception(
                f'Error detected. The summed probability for states in a timestep is {str(total_prob_reached_in_timestep)} instead of 1.')
        t -= 1


def test_if_value_equal_one(total_value, name_of_total_value):
    """
    Tests if a value (rounded) is equal to 1

    Parameters
    ----------
    total_value : float
        total value to be tested
    name_of_total_value : String
        name of the value to be tested

    Raises
    -------
    Exception
        if total_value is not equal to 1, displaying also the name_of_total_value
    """
    if round(total_value, 4) != 1:
        raise Exception(
            f'Error detected. The {name_of_total_value} is {round(total_value, 6)} instead of 1.')
