from src.model.game.price_strategy_type import PriceStrategyType
from src.model.user.user_action import UserAction


class UserState(object):
    """
    A class used to represent a User State

    ...

    Attributes
    ----------
    demand : int
        0 if user has no demand, 1 if user has demand
    ownership : Ownership
        defines if base product and/or upgrade were bought. see also in class Ownership
    probability_state_is_reached : float
        number between and including 0 and 1 to define the probability that state is visited
    best_action : UserAction
        optimal action to maximize user utility. found through backward induction
    immediate payment : float
        payment made by user if he plays best_action
    normalized immediate reward : float
        reward for user if he plays best_action if he would have valuation = 1
    immediate reward : float
        reward for user if he plays best_action
    immediate utility : float
        utility for user if he plays best_action
    normalized expected reward : float
        expected reward in future timesteps if user plays best_action and has valuation = 1
    expected_payment_in_future : float
        expected payment in future timesteps if user plays best_action
    expected_utility_in_future : float
        expected utility in future timesteps if user plays best_action
    expected_utility : float
        expected utility (in timestep itself and future timestep) if user plays best_action
    """

    def __init__(self, demand, ownership):
        """
        Parameters
        ----------
        demand : int
            0 if user has no demand, 1 if user has demand
        ownership : List[int]
            First element: base product, second element: upgrade. 1 if product is bought, else 0. Creates Ownership.
        """
        self.demand = demand
        self.ownership = Ownership(ownership[0], ownership[1])
        self.probability_state_is_reached = 0
        self.best_action = UserAction(0, [0, 0])
        self.normalized_immediate_reward = 0
        self.immediate_payment = 0
        self.immediate_utility = 0
        self.expected_payment_in_future = 0
        self.expected_utility_in_future = 0
        self.expected_utility = 0


class Ownership(object):
    """
    A class used to represent the ownership of a UserState

    ...

    Attributes
    ----------
    base_product : int
        1 if user owns (= has bought) base product, else 0
    upgrade : int
        1 if user owns (= has bought) upgrade, else 0
    """

    def __init__(self, base_product, upgrade):
        """
        Parameters
        ----------
        base_product : int
            1 if user owns (= has bought) base product, else 0
        upgrade : int
            1 if user owns (= has bought) upgrade, else 0
        """

        self.base_product = base_product
        self.upgrade = upgrade


def get_max_of_buying_and_ownership(buy_action, ownership):
    """
    Finds the maximum of newly bought and already owned base_product and upgrade

    I.e., a buy_action of [0,1] (buy upgrade) and an ownership of [1,0] (own base_product) returns [1,1[ (own both)

    Parameters
    ----------
    buy_action : BuyAction
        the users buy action in the specific timestep
    ownership : Ownership
        the users ownership in the specific timestep

    Returns
    -------
    Ownership
        newly created Ownership with the max values of buy_action and ownership
    """
    return Ownership(max(buy_action.base_product, ownership.base_product), max(buy_action.upgrade, ownership.upgrade))


def create_all_possible_user_states(price_strategy_type):
    """
    Creates the 8 possible user states

    Parameters
    ----------
    price_strategy_type : PriceStrategyType
        pricing strategy chosen by the publisher

    Returns
    -------
    array
        contains all user states, i.e. the different combinations of demand and ownership and its chosen name
    """
    user_state_1 = UserState(0, [0, 0])
    # not used, still presented for understanding: user_state_2 = UserState(0, [0, 1])
    user_state_3 = UserState(0, [1, 0])
    user_state_4 = UserState(0, [1, 1])
    user_state_5 = UserState(1, [0, 0])
    # not used, still presented for understanding: user_state_6 = UserState(1, [0, 1])
    user_state_7 = UserState(1, [1, 0])
    user_state_8 = UserState(1, [1, 1])

    if price_strategy_type == PriceStrategyType.SUB:
        user_states = [user_state_1, user_state_5]
    else:
        user_states = [user_state_1, user_state_3, user_state_4, user_state_5, user_state_7, user_state_8]
    return user_states
