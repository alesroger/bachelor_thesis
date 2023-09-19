import unittest

from src.model.game.game import create_game
from src.model.game.price_strategy_type import PriceStrategyType
from src.model.publisher.productinformation import ProductInformation
from src.model.user.user_type import UserType
from src.numerical_framework.backward_induction.backward_induction import calculate_optimal_user_actions, \
    calculate_probabilities_states_are_reached_and_publisher_revenue_and_user_welfare


class MyTestCase(unittest.TestCase):

    def test_strategy_buy(self):
        # product information from Dierks and Seuken (2020) optimal cases
        # cross-checked with results from Dierks and Seuken (2020)

        base_price = [45.82, 45.82, 45.82, 45.82, 45.82, 45.82, 21.8, 21.8, 21.8, 21.8, 21.8, 21.8]
        upgrade_price = [18.06, 18.06, 18.06, 18.06, 18.06, 18.06, 18.06, 18.06, 18.06, 18.06, 18.06, 18.06]
        subscription_price = [10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10]
        quality = [1, 0.5]
        product_information = ProductInformation(base_price, upgrade_price, subscription_price, quality)
        n_max = 12
        n_upgrade = 7
        price_strategy = PriceStrategyType.BUY
        # compare hand calculated revenue and welfare to backward induction calculations
        expected_revenue = [54.99109375, 55.1321875, 39.86, 39.86, 39.86, 39.86, 39.86, 39.86, 39.86, 39.86, 39.86,
                            39.86]
        expected_welfare = [21.9474438650948, 19.337937953404, 18.9538995535714, 18.9538995535714, 18.9538995535714,
                            18.9538995535714, 18.9538995535714, 16.0132045758928, 13.2195443470982, 10.5655671297432,
                            8.04428877325612, 5.64907433459331]

        for arrival_time in range(1, 13):
            user_type = UserType(arrival_time, 0.5, 0.95, 25)
            game = create_game(product_information,
                               user_type, n_max,
                               n_upgrade,
                               price_strategy)

            self.compare_calculated_with_expected_values(game, expected_revenue, expected_welfare, arrival_time)

        # upgrade available from first timestep on
        n_upgrade = 1

        expected_revenue = [39.86, 21.8, 21.8, 21.8, 21.8, 21.8, 21.8, 21.8, 21.8, 21.8, 0, 0]
        expected_welfare = [14.4257142857142, 12.5809523809523, 10.8619047619047, 9.22880952380951, 7.67736904761903,
                            6.20350059523808, 4.80332556547618, 3.47315928720236, 2.20950132284225, 1.00902625670013, 0,
                            0]

        base_price = [21.8, 21.8, 21.8, 21.8, 21.8, 21.8, 21.8, 21.8, 21.8, 21.8, 21.8, 21.8]
        product_information = ProductInformation(base_price, upgrade_price, subscription_price, quality)

        for arrival_time in range(1, 13):
            user_type = UserType(arrival_time, 0.5, 0.95, 19)
            game = create_game(product_information,
                               user_type, n_max,
                               n_upgrade,
                               price_strategy)

            self.compare_calculated_with_expected_values(game, expected_revenue, expected_welfare, arrival_time)

        # upgrade quality = 0
        quality = [1.7, 0]
        product_information = ProductInformation(base_price, upgrade_price, subscription_price, quality)

        expected_revenue = [21.8, 21.8, 21.8, 21.8, 21.8, 21.8, 21.8, 21.8, 0, 0, 0, 0]
        expected_welfare = [10.5809523809523, 8.96190476190475, 7.42380952380952, 5.96261904761904, 4.57448809523808,
                            3.25576369047618, 2.00297550595237, 0.812826730654754, 0, 0, 0, 0]
        for arrival_time in range(1, 13):
            for n_upgrade in [1, 4, 6, 12]:
                user_type = UserType(arrival_time, 0.5, 0.95, 10)
                game = create_game(product_information,
                                   user_type, n_max,
                                   n_upgrade,
                                   price_strategy)

                self.compare_calculated_with_expected_values(game, expected_revenue, expected_welfare, arrival_time)

        # upgrade in last timestep, different engagement factor and quality decay factor
        quality = [1, 0.5]
        base_price = [45.82, 45.82, 45.82, 45.82, 45.82, 45.82, 45.82, 45.82, 45.82, 45.82, 45.82, 21.8]
        product_information = ProductInformation(base_price, upgrade_price, subscription_price, quality)

        expected_revenue = [62.6407419365385, 62.7037132628206, 62.773681403134, 62.8514237812599, 62.9378042014,
                            63.033782446, 63.14042494, 63.2589166, 39.86, 39.86, 39.86, 39.86]
        expected_welfare = [144.338577236553, 124.025612296435, 106.622317918526, 91.6769908319607, 78.8039885135543,
                            67.6736317708805, 58.0036010151319, 49.5515998455502, 48.1725129973533, 48.1725129973533,
                            48.1725129973533, 48.1725129973533]
        n_upgrade = 12
        for arrival_time in range(1, 13):
            user_type = UserType(arrival_time, 0.9, 0.85, 31)
            game = create_game(product_information,
                               user_type, n_max,
                               n_upgrade,
                               price_strategy)

            self.compare_calculated_with_expected_values(game, expected_revenue, expected_welfare, arrival_time)

    def test_strategy_sub(self):
        # product information from Dierks and Seuken (2020) optimal cases
        # cross-checked with results from Dierks and Seuken (2020)

        base_price = [45.82, 45.82, 45.82, 45.82, 45.82, 45.82, 21.8, 21.8, 21.8, 21.8, 21.8, 21.8]
        upgrade_price = [18.06, 18.06, 18.06, 18.06, 18.06, 18.06, 18.06, 18.06, 18.06, 18.06, 18.06, 18.06]
        subscription_price = [14.66, 14.66, 14.66, 14.66, 14.66, 14.66, 14.66, 14.66, 14.66, 14.66, 14.66, 14.66]
        quality = [1, 0.5]
        product_information = ProductInformation(base_price, upgrade_price, subscription_price, quality)
        n_max = 12
        n_upgrade = 7
        price_strategy = PriceStrategyType.SUB
        # compare hand calculated revenue and welfare to backward induction calculations

        expected_revenue = [43.5144931030273, 43.0561444091796, 42.1394470214843, 40.3060522460937, 36.6392626953125,
                            29.30568359375, 29.30568359375, 29.2913671875, 29.262734375, 29.20546875, 29.0909375,
                            28.861875]
        expected_welfare = [72.0467857317359, 64.690154996334, 58.3768935255301, 53.3103705839223, 49.9813247007068,
                            49.4468329342757, 49.4468329342757, 41.5726218685515, 34.4883041371031, 28.1173626342063,
                            22.3934041924126, 17.2616194164252]

        for arrival_time in range(1, 13):
            user_type = UserType(arrival_time, 0.5, 0.9, 42)
            game = create_game(product_information,
                               user_type, n_max,
                               n_upgrade,
                               price_strategy)
            self.compare_calculated_with_expected_values(game, expected_revenue, expected_welfare, arrival_time)

        # upgrade quality = 0
        quality = [1, 0]
        product_information = ProductInformation(base_price, upgrade_price, subscription_price, quality)

        expected_revenue = [105.195829951885, 100.595366613206, 95.48374068134, 89.8041563126, 83.493507014,
                            76.48167446, 68.6907494, 60.034166, 50.41574, 39.7286, 27.854, 14.66]
        expected_welfare = [132.127561044079, 108.652845604532, 88.0142728939247, 69.9825254376942,
                            54.3572504863268, 40.9648338736965, 29.6564709707739, 20.3065133008599,
                            12.8110724453999, 7.08686572822211, 3.070290852469, 0.716719208410003]
        for arrival_time in range(1, 13):
            # n_upgrade has no effect
            for n_upgrade in [1]:
                user_type = UserType(arrival_time, 0.9, 0.9, 49)
                game = create_game(product_information,
                                   user_type, n_max,
                                   n_upgrade,
                                   price_strategy)

                self.compare_calculated_with_expected_values(game, expected_revenue, expected_welfare, arrival_time)

        # upgrade released in last timestep
        quality = [1, 0.5]
        product_information = ProductInformation(base_price, upgrade_price, subscription_price, quality)

        n_upgrade = 12
        expected_revenue = [98.1358401014, 88.778073446, 78.38055494, 66.8277566, 53.991314, 39.7286, 39.7286, 39.7286,
                            39.7286, 39.7286, 39.7286, 39.7286]
        expected_welfare = [30.3304092644336, 22.4788850140397, 16.4216358469353, 12.0913589945971, 9.43994026977697,
                            8.43791946442118, 8.43791946442118, 8.43791946442118, 8.43791946442118, 8.43791946442118,
                            8.43791946442118, 8.43791946442118]

        for arrival_time in range(1, 13):
            user_type = UserType(arrival_time, 0.9, 0.9, 24)
            game = create_game(product_information,
                               user_type, n_max,
                               n_upgrade,
                               price_strategy)
            self.compare_calculated_with_expected_values(game, expected_revenue, expected_welfare, arrival_time)

        # upgrade released in first timestep
        quality = [1, 0.5]
        product_information = ProductInformation(base_price, upgrade_price, subscription_price, quality)

        n_upgrade = 1
        expected_revenue = [109.336246956696, 105.195829951885, 100.595366613206, 95.48374068134, 89.8041563126,
                            83.493507014, 76.48167446, 68.6907494, 60.034166, 50.41574, 39.7286, 27.854]
        expected_welfare = [61.5684903244446, 53.0316559160496, 45.1296176844996, 37.8537418716662,
                            31.1983937462958,
                            25.1610729125509, 19.7425735486676, 14.9471718509502, 10.7828432358648,
                            7.26151216014061,
                            4.39933775887694, 2.21703887842573]

        for arrival_time in range(1, 13):
            user_type = UserType(arrival_time, 0.9, 0.95, 19)
            game = create_game(product_information,
                               user_type, n_max,
                               n_upgrade,
                               price_strategy)
            self.compare_calculated_with_expected_values(game, expected_revenue, expected_welfare, arrival_time)

    def compare_calculated_with_expected_values(self, game, expected_revenue, expected_welfare, arrival_time):
        calculate_optimal_user_actions(game)
        calculate_probabilities_states_are_reached_and_publisher_revenue_and_user_welfare(game)
        self.assertEqual(round(game.expected_publisher_revenue, 5),
                         round(expected_revenue[arrival_time - 1], 5))
        self.assertEqual(round(game.expected_user_welfare, 5), round(expected_welfare[arrival_time - 1], 5))


if __name__ == '__main__':
    unittest.main()
