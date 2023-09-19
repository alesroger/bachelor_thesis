class ProductInformation(object):
    """
    A class used to represent Product Information of the distributed product by the publisher

    ...

    Attributes
    ----------
    price_base_product : list[float]
        price over time for base product
    price_upgrade : list[float]
        price over time for upgrade
    price_subscription : list[float]
        price over time for subscription
    product_quality : ProductQuality
        quality of the base product and the upgrade, see ProductQuality
    """

    def __init__(self, price_base_product, price_upgrade, price_subscription, product_quality):
        """
        Parameters
        ----------
         price_base_product : list[float]
            price over time for base product
        price_upgrade : list[float]
            price over time for upgrade
        price_subscription : list[float]
            price over time for subscription
        product_quality : list[float]
            list with length 2, first element defining quality of the base product, second element upgrade quality
        """
        self.price_base_product = price_base_product
        self.price_upgrade = price_upgrade
        self.price_subscription = price_subscription
        self.product_quality = ProductQuality(product_quality[0], product_quality[1])


class ProductQuality(object):
    """
    A class used to represent Product Quality of the distributed product by the publisher

    ...

    Attributes
    ----------
    base_product : float
        quality of base product
    upgrade : float
        quality of the upgrade
    """

    def __init__(self, base_product, upgrade):
        """
        Parameters
        ----------
        base_product : float
            quality of base product
        upgrade : float
            quality of the upgrade
        """
        self.base_product = base_product
        self.upgrade = upgrade
