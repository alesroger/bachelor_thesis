import unittest

from src.model.user.user_action import BuyAction
from src.model.user.user_state import get_max_of_buying_and_ownership, Ownership


class TestUserState(unittest.TestCase):
    def test_get_max_of_buying_and_ownership(self):
        self.assertEqual(0, get_max_of_buying_and_ownership(BuyAction(0, 0), Ownership(0, 0)).base_product)
        self.assertEqual(1, get_max_of_buying_and_ownership(BuyAction(1, 0), Ownership(0, 0)).base_product)
        self.assertEqual(1, get_max_of_buying_and_ownership(BuyAction(0, 0), Ownership(1, 0)).base_product)
        self.assertEqual(1, get_max_of_buying_and_ownership(BuyAction(1, 0), Ownership(1, 0)).base_product)

        self.assertEqual(0, get_max_of_buying_and_ownership(BuyAction(0, 0), Ownership(0, 0)).upgrade)
        self.assertEqual(1, get_max_of_buying_and_ownership(BuyAction(0, 1), Ownership(0, 0)).upgrade)
        self.assertEqual(1, get_max_of_buying_and_ownership(BuyAction(0, 0), Ownership(0, 1)).upgrade)
        self.assertEqual(1, get_max_of_buying_and_ownership(BuyAction(0, 1), Ownership(0, 1)).upgrade)


if __name__ == '__main__':
    unittest.main()
