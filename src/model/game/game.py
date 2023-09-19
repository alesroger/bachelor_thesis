from src.model.user.user_state import create_all_possible_user_states


class Game(object):
    """
    A class used to represent the "game" between a publisher and a user both acting optimally

    ...

    Attributes
    ----------
    product_information : ProductInformation
        prices over time and product qualities
    user_type : UserType
        type of the user who is acting optimally
    n_max : int
        last timestep where users arrive and publisher can change prices
    n_upgrade : int
        timestep of upgrade release
    price_strategy_type : PriceStrategyType
        type of price strategy chosen by the publisher
    user_states = list[UserState]
        all possible user states
    expected_publisher_revenue : float
        expected revenue for the publisher if user and publisher act optimally
    expected_user_welfare : float
        expected welfare for the user if user and publisher act optimally
    """

    def __init__(self, product_information, user_type, n_max, n_upgrade, price_strategy_type):
        """
        Parameters
        ----------
        product_information : ProductInformation
            prices over time and product qualities
        user_type : UserType
            type of the user who is acting optimally
        n_max : int
            last timestep where users arrive and publisher can change prices
        n_upgrade : int
            timestep of upgrade release
        price_strategy_type : PriceStrategyType
            type of price strategy chosen by the publisher
        """
        self.product_information = product_information
        self.user_type = user_type
        self.user_states = None
        self.price_strategy_type = price_strategy_type
        self.n_max = n_max
        self.n_upgrade = n_upgrade
        self.expected_publisher_revenue = 0
        self.expected_user_welfare = 0


def create_game(product_information, user_type, n_max, n_upgrade, price_strategy_type):
    """
    Creates a game with all possible user states

    Parameters
    ----------
    product_information : ProductInformation
        prices over time and product qualities
    user_type : UserType
        type of the user who is acting optimally
    n_max : int
        last timestep where users arrive and publisher can change prices
    n_upgrade : int
        timestep of upgrade release
    price_strategy_type : PriceStrategyType
        type of price strategy chosen by the publisher

    Returns
    -------
    Game
        contains all important information to play the game, especially all possible user states
    """
    game = Game(product_information, user_type, n_max, n_upgrade, price_strategy_type)
    add_all_user_states(game)

    return game


def add_all_user_states(game):
    """
    Adds all possible user states to every timestep of the game

    Parameters
    ----------
    game : Game
        object holding all important information without user states

    Returns
    -------
    Game
        contains all important information to play the game, including all possible user states
    """
    game.user_states = [None] * game.n_max
    for i in range(0, game.n_max):
        game.user_states[i] = create_all_possible_user_states(game.price_strategy_type)
