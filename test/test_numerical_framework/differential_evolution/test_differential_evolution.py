import unittest

from src.model.game.price_strategy_type import PriceStrategyType
from src.numerical_framework.differential_evolution.differential_evolution import create_bounds, get_price_vectors
from src.numerical_framework.helpers.framework_creators import DifferentialEvolutionCreator
from src.numerical_framework.helpers.high_price import HighPrice


class TestBoundsAndPriceVectorCreation(unittest.TestCase):
    def test_bound_creation_buy_cases(self):
        differential_evolution_creator = DifferentialEvolutionCreator()
        differential_evolution_creator.price_strategy_type = PriceStrategyType.BUY

        bounds = create_bounds(differential_evolution_creator)
        self.assertEqual(18, len(bounds))

        differential_evolution_creator.is_prices_discounted = True
        bounds = create_bounds(differential_evolution_creator)
        self.assertEqual(18, len(bounds))

        differential_evolution_creator.first_base_price_fixed = 100
        bounds = create_bounds(differential_evolution_creator)
        self.assertEqual(17, len(bounds))
        differential_evolution_creator.first_base_price_fixed = None

        differential_evolution_creator.first_base_price_fixed = 100
        differential_evolution_creator.first_upgrade_price_fixed = 100
        bounds = create_bounds(differential_evolution_creator)
        self.assertEqual(16, len(bounds))
        differential_evolution_creator.first_base_price_fixed = None
        differential_evolution_creator.first_upgrade_price_fixed = None

        differential_evolution_creator.first_base_price_fixed = 100
        differential_evolution_creator.first_upgrade_price_fixed = 100
        differential_evolution_creator.is_prices_discounted = True
        bounds = create_bounds(differential_evolution_creator)
        self.assertEqual(16, len(bounds))
        differential_evolution_creator.first_base_price_fixed = None
        differential_evolution_creator.first_upgrade_price_fixed = None

        differential_evolution_creator.n_upgrade = 4
        bounds = create_bounds(differential_evolution_creator)
        self.assertEqual(21, len(bounds))

        differential_evolution_creator.n_max = 7
        differential_evolution_creator.n_upgrade = 4
        bounds = create_bounds(differential_evolution_creator)
        self.assertEqual(11, len(bounds))

        differential_evolution_creator.play_different_ask_prices = False
        bounds = create_bounds(differential_evolution_creator)
        self.assertEqual(3, len(bounds))

    def test_bound_creation_both_cases(self):
        differential_evolution_creator = DifferentialEvolutionCreator()
        differential_evolution_creator.price_strategy_type = PriceStrategyType.BOTH

        bounds = create_bounds(differential_evolution_creator)
        self.assertEqual(19, len(bounds))

        differential_evolution_creator = DifferentialEvolutionCreator()
        differential_evolution_creator.price_strategy_type = PriceStrategyType.BOTH
        differential_evolution_creator.is_prices_discounted = True
        bounds = create_bounds(differential_evolution_creator)
        self.assertEqual(19, len(bounds))

        differential_evolution_creator = DifferentialEvolutionCreator()
        differential_evolution_creator.price_strategy_type = PriceStrategyType.BOTH
        differential_evolution_creator.first_base_price_fixed = 100
        bounds = create_bounds(differential_evolution_creator)
        self.assertEqual(18, len(bounds))

        differential_evolution_creator = DifferentialEvolutionCreator()
        differential_evolution_creator.price_strategy_type = PriceStrategyType.BOTH
        differential_evolution_creator.first_base_price_fixed = 100
        differential_evolution_creator.first_upgrade_price_fixed = 100
        bounds = create_bounds(differential_evolution_creator)
        self.assertEqual(17, len(bounds))

        differential_evolution_creator = DifferentialEvolutionCreator()
        differential_evolution_creator.price_strategy_type = PriceStrategyType.BOTH
        differential_evolution_creator.first_base_price_fixed = 100
        differential_evolution_creator.first_upgrade_price_fixed = 100
        differential_evolution_creator.is_prices_discounted = True
        bounds = create_bounds(differential_evolution_creator)
        self.assertEqual(17, len(bounds))

        differential_evolution_creator = DifferentialEvolutionCreator()
        differential_evolution_creator.price_strategy_type = PriceStrategyType.BOTH
        differential_evolution_creator.is_subscription_price_variable = True
        bounds = create_bounds(differential_evolution_creator)
        self.assertEqual(30, len(bounds))

        differential_evolution_creator = DifferentialEvolutionCreator()
        differential_evolution_creator.price_strategy_type = PriceStrategyType.BOTH
        differential_evolution_creator.play_different_ask_prices = False
        bounds = create_bounds(differential_evolution_creator)
        self.assertEqual(4, len(bounds))

    def test_bound_creation_sub_cases(self):
        differential_evolution_creator = DifferentialEvolutionCreator()
        differential_evolution_creator.price_strategy_type = PriceStrategyType.SUB
        bounds = create_bounds(differential_evolution_creator)
        self.assertEqual(1, len(bounds))

        differential_evolution_creator = DifferentialEvolutionCreator()
        differential_evolution_creator.price_strategy_type = PriceStrategyType.SUB
        differential_evolution_creator.is_subscription_price_variable = True
        bounds = create_bounds(differential_evolution_creator)
        self.assertEqual(12, len(bounds))

        differential_evolution_creator = DifferentialEvolutionCreator()
        differential_evolution_creator.price_strategy_type = PriceStrategyType.SUB
        differential_evolution_creator.n_max = 10
        differential_evolution_creator.n_upgrade = 3
        bounds = create_bounds(differential_evolution_creator)
        self.assertEqual(1, len(bounds))

    def test_price_vector_creation_buy_case(self):
        differential_evolution_creator = DifferentialEvolutionCreator()
        differential_evolution_creator.price_strategy_type = PriceStrategyType.BUY

        differential_evolution_creator.is_prices_discounted = False
        prices = [10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 5, 5, 5, 5, 5, 5]
        price_base_product, price_upgrade, price_subscription = get_price_vectors(prices,
                                                                                  differential_evolution_creator)
        for i in range(0, 12):
            self.assertEqual(price_base_product[i], 10)
        for i in range(0, 6):
            self.assertEqual(price_upgrade[i], HighPrice)
        for i in range(6, 12):
            self.assertEqual(price_upgrade[i], 5)

        differential_evolution_creator = DifferentialEvolutionCreator()
        differential_evolution_creator.price_strategy_type = PriceStrategyType.BUY
        differential_evolution_creator.n_max = 4
        differential_evolution_creator.n_upgrade = 2
        differential_evolution_creator.is_prices_discounted = False
        prices = [10, 10, 10, 10, 5, 5, 5]
        price_base_product, price_upgrade, price_subscription = get_price_vectors(prices,
                                                                                  differential_evolution_creator)
        for i in range(0, 4):
            self.assertEqual(price_base_product[i], 10)
        for i in range(0, 1):
            self.assertEqual(price_upgrade[i], HighPrice)
        for i in range(1, 4):
            self.assertEqual(price_upgrade[i], 5)

        differential_evolution_creator = DifferentialEvolutionCreator()
        differential_evolution_creator.price_strategy_type = PriceStrategyType.BUY
        differential_evolution_creator.is_prices_discounted = True
        prices = [10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 5, 5, 5, 5, 5, 5]
        price_base_product, price_upgrade, price_subscription = get_price_vectors(prices,
                                                                                  differential_evolution_creator)
        self.assertEqual(price_base_product[0], 10)
        for i in range(1, 12):
            self.assertEqual(price_base_product[i], 100)
        for i in range(0, 6):
            self.assertEqual(price_upgrade[i], HighPrice)
        self.assertEqual(price_upgrade[6], 5)
        for i in range(7, 12):
            self.assertEqual(price_upgrade[i], 25)

        differential_evolution_creator = DifferentialEvolutionCreator()
        differential_evolution_creator.price_strategy_type = PriceStrategyType.BUY
        differential_evolution_creator.is_prices_discounted = True
        differential_evolution_creator.first_base_price_fixed = 20
        differential_evolution_creator.first_upgrade_price_fixed = 10
        prices = [10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 5, 5, 5, 5, 5]
        price_base_product, price_upgrade, price_subscription = get_price_vectors(prices,
                                                                                  differential_evolution_creator)
        self.assertEqual(price_base_product[0], 20)
        for i in range(1, 12):
            self.assertEqual(price_base_product[i], 200)
        for i in range(0, 6):
            self.assertEqual(price_upgrade[i], HighPrice)
        self.assertEqual(price_upgrade[6], 10)
        for i in range(7, 12):
            self.assertEqual(price_upgrade[i], 50)

        # case play_different_ask_prices = False
        differential_evolution_creator = DifferentialEvolutionCreator()
        differential_evolution_creator.price_strategy_type = PriceStrategyType.BUY
        differential_evolution_creator.play_different_ask_prices = False
        prices = [10, 8, 5]
        price_base_product, price_upgrade, price_subscription = get_price_vectors(prices,
                                                                                  differential_evolution_creator)
        for i in range(0, 6):
            self.assertEqual(price_base_product[i], 10)
        for i in range(6, 12):
            self.assertEqual(price_base_product[i], 8)
        for i in range(0, 6):
            self.assertEqual(price_upgrade[i], HighPrice)
        for i in range(6, 12):
            self.assertEqual(price_upgrade[i], 5)


if __name__ == '__main__':
    unittest.main()
