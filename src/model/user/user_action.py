from src.model.game.price_strategy_type import PriceStrategyType


class UserAction(object):
    """
    A class used to represent a User Action

    ...

    Attributes
    ----------
    subscribe_action : int
        1 if subscribe, else 0
    buy_action : BuyAction
        see BuyAction
    """

    def __init__(self, subscribe_action, buy_action):
        """
        Parameters
        ----------
         subscribe_action : int
            1 if subscribe, else 0
        buy_action : List[int]
            First element: base product, Second element: Upgrade. 1 if buy, else 0
        """
        self.subscribe_action = subscribe_action
        self.buy_action = BuyAction(buy_action[0], buy_action[1])


class BuyAction(object):
    """
    A class used to represent a Buy Action

    ...

    Attributes
    ----------
    base_product : int
        1 if buy base product, else 0
    upgrade : int
        1 if buy upgrade, else 0
    """

    def __init__(self, base_product, upgrade):
        """
        Parameters
        ----------
        base_product : int
            1 if buy base product, else 0
        upgrade : int
            1 if buy upgrade, else 0
        """
        self.base_product = base_product
        self.upgrade = upgrade


def create_all_possible_user_actions(price_strategy_type):
    """
    Creates the 8 possible user actions

    Parameters
    ----------
    price_strategy_type : PriceStrategyType
        pricing strategy chosen by the publisher

    Returns
    -------
    array
        contains all possible user actions for the corresponding price strategy type
    """
    user_action_1 = UserAction(0, [0, 0])
    user_action_2 = UserAction(0, [0, 1])
    user_action_3 = UserAction(0, [1, 0])
    user_action_4 = UserAction(0, [1, 1])
    user_action_5 = UserAction(1, [0, 0])
    user_action_6 = UserAction(1, [0, 1])
    user_action_7 = UserAction(1, [1, 0])
    # not used, still presented for understanding: user_action_8 = UserAction(1, [1, 1])

    user_actions = []
    if price_strategy_type == PriceStrategyType.SUB:
        user_actions = [user_action_1, user_action_5]

    elif price_strategy_type == PriceStrategyType.BUY:
        user_actions = [user_action_1, user_action_2, user_action_3, user_action_4]

    elif price_strategy_type in [PriceStrategyType.BOTH, PriceStrategyType.BOTH_BUY]:
        user_actions = [user_action_1, user_action_2, user_action_3, user_action_4, user_action_5, user_action_6,
                        user_action_7]
    return user_actions
