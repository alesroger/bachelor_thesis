import unittest

from src.model.game.price_strategy_type import PriceStrategyType
from src.model.publisher.productinformation import ProductInformation
from src.model.user.user_action import create_all_possible_user_actions, UserAction
from src.model.user.user_functions import get_transition_probability, get_preferred_action_if_deliver_equal_utility, \
    get_normalized_immediate_reward, get_immediate_payment
from src.model.user.user_state import create_all_possible_user_states, UserState
from src.model.user.user_type import UserType


class TestUserFunctions(unittest.TestCase):
    def setUp(self):
        self.user_actions = create_all_possible_user_actions(PriceStrategyType.BOTH)
        self.user_states = create_all_possible_user_states(PriceStrategyType.BOTH)
        self.user_type = UserType(3, 0.9, 0.95, 25)
        self.n_upgrade = 7

    # this includes testing get_realized_quality(timestep, n_upgrade, ownership, quality_decay_factor, product_quality)
    def test_normalized_immediate_reward(self):
        user_action_1 = UserAction(0, [0, 0])
        user_action_2 = UserAction(0, [0, 1])
        user_action_3 = UserAction(0, [1, 0])
        user_action_4 = UserAction(0, [1, 1])
        user_action_5 = UserAction(1, [0, 0])
        user_action_6 = UserAction(1, [0, 1])
        user_action_7 = UserAction(1, [1, 0])

        user_state_1 = UserState(0, [0, 0])
        user_state_3 = UserState(0, [1, 0])
        user_state_4 = UserState(0, [1, 1])
        user_state_5 = UserState(1, [0, 0])
        user_state_7 = UserState(1, [1, 0])
        user_state_8 = UserState(1, [1, 1])

        base_price = [10]
        upgrade_price = [3]
        subscription_price = [5]

        product_information = ProductInformation(base_price, upgrade_price, subscription_price, [1, 0.5])
        n_upgrade = 1

        # no demand: reward 0
        for user_action in [user_action_1, user_action_2, user_action_3, user_action_4, user_action_5, user_action_6,
                            user_action_7]:
            for user_state in [user_state_1, user_state_3, user_state_4]:
                for timestep in range(1, 15):
                    self.assertEqual(
                        get_normalized_immediate_reward(timestep, n_upgrade, user_action, self.user_type, user_state,
                                                        product_information), 0)

        timestep = 1
        # complete ownership leads to highest possible normalized immedate reward
        for user_action in [user_action_1, user_action_2, user_action_3, user_action_4, user_action_5, user_action_6,
                            user_action_7]:
            for user_state in [user_state_8]:
                self.assertEqual(
                    get_normalized_immediate_reward(timestep, n_upgrade, user_action, self.user_type, user_state,
                                                    product_information), 1.5)

        # subscription leads to highest possible normalized immediate reward
        for user_action in [user_action_5, user_action_6, user_action_7]:
            for user_state in [user_state_5, user_state_7, user_state_8]:
                self.assertEqual(
                    get_normalized_immediate_reward(timestep, n_upgrade, user_action, self.user_type, user_state,
                                                    product_information), 1.5)

        # ownership of just upgrade leads to no reward
        for user_action in [user_action_2]:
            for user_state in [user_state_5]:
                self.assertEqual(
                    get_normalized_immediate_reward(timestep, n_upgrade, user_action, self.user_type, user_state,
                                                    product_information), 0)

        n_upgrade = 4
        # complete ownership leads to highest possible normalized immedate reward
        for user_action in [user_action_1, user_action_2, user_action_3, user_action_4, user_action_5, user_action_6,
                            user_action_7]:
            for user_state in [user_state_8]:
                self.assertEqual(
                    get_normalized_immediate_reward(timestep, n_upgrade, user_action, self.user_type, user_state,
                                                    product_information), 1)

        # subscription leads to highest possible normalized immediate reward
        for user_action in [user_action_5, user_action_6, user_action_7]:
            for user_state in [user_state_5, user_state_7, user_state_8]:
                self.assertEqual(
                    get_normalized_immediate_reward(timestep, n_upgrade, user_action, self.user_type, user_state,
                                                    product_information), 1)

        # test reward over time for different ownership cases
        base_immediate_reward = [1, 0.95, 0.9025, 0.857375, 0.81450625, 0.7737809375, 0.735091890625, 0.69833729609375,
                                 0.663420431289062, 0.630249409724609, 0.598736939238379, 0.56880009227646,
                                 0.540360087662637, 0.513342083279505, 0.487674979115529]
        base_and_upgrade_immediate_reward = [1, 0.95, 0.9025, 1.357375, 1.28950625, 1.2250309375, 1.163779390625,
                                             1.10559042109375, 1.05031090003906, 0.997795355037109, 0.947905587285253,
                                             0.900510307920991, 0.855484792524941, 0.812710552898694, 0.772075025253759]
        for user_action in [user_action_1]:
            for user_state in [user_state_7]:
                for timestep in range(1, 16):
                    self.assertEqual(
                        round(get_normalized_immediate_reward(timestep, n_upgrade, user_action, self.user_type,
                                                              user_state,
                                                              product_information), 5),
                        round(base_immediate_reward[timestep - 1], 5))
        for user_action in [user_action_1]:
            for user_state in [user_state_8]:
                for timestep in range(1, 16):
                    self.assertEqual(
                        round(get_normalized_immediate_reward(timestep, n_upgrade, user_action, self.user_type,
                                                              user_state,
                                                              product_information), 5),
                        round(base_and_upgrade_immediate_reward[timestep - 1], 5))

    def test_get_immediate_payment(self):
        user_action_1 = UserAction(0, [0, 0])
        user_action_2 = UserAction(0, [0, 1])
        user_action_3 = UserAction(0, [1, 0])
        user_action_4 = UserAction(0, [1, 1])
        user_action_5 = UserAction(1, [0, 0])
        user_action_6 = UserAction(1, [0, 1])
        user_action_7 = UserAction(1, [1, 0])

        base_price = [10, 8]
        upgrade_price = [3, 7]
        subscription_price = [5, 9]

        product_information = ProductInformation(base_price, upgrade_price, subscription_price, [1, 0.5])

        # subscription leads to highest possible normalized immediate reward

        buy_base_and_upgrade = [13, 15]
        buy_base_and_subscribe = [15, 17]
        buy_upgrade_and_subscribe = [8, 16]

        # pay nothing
        for user_action in [user_action_1]:
            for timestep in range(1, 3):
                self.assertEqual(
                    get_immediate_payment(timestep, user_action, product_information), 0)

        # buy base
        for user_action in [user_action_3]:
            for timestep in range(1, 3):
                self.assertEqual(
                    get_immediate_payment(timestep, user_action, product_information), base_price[timestep - 1])

        # buy upgrade
        for user_action in [user_action_2]:
            for timestep in range(1, 3):
                self.assertEqual(
                    get_immediate_payment(timestep, user_action, product_information), upgrade_price[timestep - 1])

        # subscribe
        for user_action in [user_action_5]:
            for timestep in range(1, 3):
                self.assertEqual(
                    get_immediate_payment(timestep, user_action, product_information), subscription_price[timestep - 1])

        # buy both
        for user_action in [user_action_4]:
            for timestep in range(1, 3):
                self.assertEqual(
                    get_immediate_payment(timestep, user_action, product_information),
                    buy_base_and_upgrade[timestep - 1])

        # buy base and subscribe
        for user_action in [user_action_7]:
            for timestep in range(1, 3):
                self.assertEqual(
                    get_immediate_payment(timestep, user_action, product_information),
                    buy_base_and_subscribe[timestep - 1])

        # buy upgrade and subscribe
        for user_action in [user_action_6]:
            for timestep in range(1, 3):
                self.assertEqual(
                    get_immediate_payment(timestep, user_action, product_information),
                    buy_upgrade_and_subscribe[timestep - 1])

    def test_transition_probability(self):
        timestep = 4

        # from state 5 to state 5 -> subscription doesn't change ownership but demand decreases prob. of demand in next step
        self.assertEqual(self.user_type.engagement_factor,
                         get_transition_probability(timestep, self.n_upgrade, self.user_states[3], self.user_states[3],
                                                    self.user_actions[4], self.user_type, 0.5))
        self.assertEqual(1 - self.user_type.engagement_factor,
                         get_transition_probability(timestep, self.n_upgrade, self.user_states[0], self.user_states[3],
                                                    self.user_actions[4], self.user_type, 0.5))
        self.assertEqual(self.user_type.engagement_factor,
                         get_transition_probability(timestep, self.n_upgrade, self.user_states[4], self.user_states[3],
                                                    self.user_actions[2], self.user_type, 0.5))
        self.assertEqual(0,
                         get_transition_probability(timestep, self.n_upgrade, self.user_states[5], self.user_states[3],
                                                    self.user_actions[2], self.user_type, 0.5))

    def test_transition_probability_upgrade_timestep(self):
        timestep = 7
        # get interest back in timestep of upgrade
        self.assertEqual(self.user_type.engagement_factor,
                         get_transition_probability(timestep, self.n_upgrade, self.user_states[3], self.user_states[0],
                                                    self.user_actions[0], self.user_type, 0.5))

    def test_get_preferred_action_if_deliver_equal_utility(self):
        user_action_1 = UserAction(0, [0, 0])
        user_action_2 = UserAction(0, [0, 1])
        user_action_3 = UserAction(0, [1, 0])
        user_action_4 = UserAction(0, [1, 1])
        user_action_5 = UserAction(1, [0, 0])
        user_action_6 = UserAction(1, [0, 1])
        user_action_7 = UserAction(1, [1, 0])

        # action 1 looses everytime
        for action in [user_action_2, user_action_3, user_action_4, user_action_5, user_action_6, user_action_7]:
            self.assertEqual(get_preferred_action_if_deliver_equal_utility(user_action_1, action), action)

        # action 2
        # wins
        for action in [user_action_1, user_action_5]:
            self.assertEqual(get_preferred_action_if_deliver_equal_utility(user_action_2, action), user_action_2)
        # looses
        for action in [user_action_3, user_action_4, user_action_6, user_action_7]:
            self.assertEqual(get_preferred_action_if_deliver_equal_utility(user_action_2, action), action)

            # action 3
            # wins
            for action in [user_action_1, user_action_2, user_action_5]:
                self.assertEqual(get_preferred_action_if_deliver_equal_utility(user_action_3, action), user_action_3)
            # looses
            for action in [user_action_4, user_action_6, user_action_7]:
                self.assertEqual(get_preferred_action_if_deliver_equal_utility(user_action_3, action), action)

        # action 4 wins everytime
        for action in [user_action_1, user_action_2, user_action_3, user_action_5, user_action_6, user_action_7]:
            self.assertEqual(get_preferred_action_if_deliver_equal_utility(user_action_4, action), user_action_4)

        # action 5
        # wins
        for action in [user_action_1]:
            self.assertEqual(get_preferred_action_if_deliver_equal_utility(user_action_5, action), user_action_5)
        # looses
        for action in [user_action_2, user_action_3, user_action_6, user_action_7]:
            self.assertEqual(get_preferred_action_if_deliver_equal_utility(user_action_5, action), action)

        # action 6
        # wins
        for action in [user_action_1, user_action_2, user_action_3, user_action_5]:
            self.assertEqual(get_preferred_action_if_deliver_equal_utility(user_action_6, action), user_action_6)
        # looses
        for action in [user_action_4, user_action_7]:
            self.assertEqual(get_preferred_action_if_deliver_equal_utility(user_action_6, action), action)

        # action 7
        # wins
        for action in [user_action_1, user_action_2, user_action_3, user_action_5, user_action_6]:
            self.assertEqual(get_preferred_action_if_deliver_equal_utility(user_action_7, action), user_action_7)
        # looses
        for action in [user_action_4]:
            self.assertEqual(get_preferred_action_if_deliver_equal_utility(user_action_7, action), action)


if __name__ == '__main__':
    unittest.main()
