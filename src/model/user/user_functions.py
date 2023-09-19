from src.model.user.user_state import get_max_of_buying_and_ownership, Ownership


def get_immediate_utility(timestep, n_upgrade, user_action, user_type, user_state, product_information):
    """
    Calculates the immediate utility for a user type, user action, and user state

    Parameters
    ----------
    timestep : int
        in thesis: n, the timestep the action is executed
    n_upgrade : int
        in thesis: m, timestep of upgrade release
    user_action : UserAction
        subscription and buy action
    user_type : UserType
        user type
    user_state : UserState
        user state
    product_information : Product Information
        prices and quality of product

    Returns
    -------
    float
        immediate utility
    """
    return get_normalized_immediate_reward(timestep, n_upgrade, user_action, user_type, user_state,
                                           product_information) * user_type.valuation - \
           get_immediate_payment(timestep, user_action, product_information)


def get_normalized_immediate_reward(timestep, n_upgrade, user_action, user_type, user_state,
                                    product_information):
    """
    Calculates the normalized immediate reward for a user type, user action, and user state

    Parameters
    ----------
    timestep : int
        in thesis: n, the timestep the action is executed
    n_upgrade : int
        in thesis: m, timestep of upgrade release
    user_action : UserAction
        subscription and buy action
    user_type : UserType
        user type
    user_state : UserState
        user state
    product_information : Product Information
        prices and quality of product

    Returns
    -------
    float
        immediate reward
    """
    reward_if_subscribed = user_action.subscribe_action * get_realized_quality(timestep, n_upgrade,
                                                                               Ownership(1, 1),
                                                                               user_type.quality_decay_factor,
                                                                               product_information.product_quality)

    max_of_buying_and_ownership = get_max_of_buying_and_ownership(user_action.buy_action,
                                                                  user_state.ownership)
    reward_if_not_subscribed = (1 - user_action.subscribe_action) * \
                               get_realized_quality(timestep, n_upgrade,
                                                    max_of_buying_and_ownership,
                                                    user_type.quality_decay_factor,
                                                    product_information.product_quality)
    return user_state.demand * (reward_if_subscribed + reward_if_not_subscribed)


def get_realized_quality(timestep, n_upgrade, ownership, quality_decay_factor, product_quality):
    """
    Calculates the realized quality for an ownership vector at a specific timestep

    Parameters
    ----------
    timestep : int
        in thesis: n, the timestep the action is executed
    n_upgrade : int
        in thesis: m, timestep of upgrade release
    ownership : Ownership
        ownership of base product and upgrade
    quality_decay_factor : float
        in thesis: x_gamma of user type
    product_quality : List[float]
        first element: base product, second element: upgrade

    Returns
    -------
    float
        realized quality
    """

    if timestep >= n_upgrade:
        realized_quality_for_base_product = ownership.base_product * quality_decay_factor ** (
                timestep - 1) * product_quality.base_product
        realized_quality_for_upgrade = (
                                           ownership.upgrade if ownership.base_product == 1 else 0) * \
                                       quality_decay_factor ** (timestep - n_upgrade) * product_quality.upgrade

    else:
        realized_quality_for_base_product = ownership.base_product * quality_decay_factor ** (
                timestep - 1) * product_quality.base_product
        realized_quality_for_upgrade = 0

    return realized_quality_for_base_product + realized_quality_for_upgrade


def get_immediate_payment(timestep, user_action, product_information):
    """
    Calculates the immediate payment for a user action

    Parameters
    ----------
    timestep : int
        in thesis: n, the timestep the action is executed
    user_action : UserAction
        subscription and buy action
    product_information : Product Information
        prices and quality of product

    Returns
    -------
    float
        immediate payment
    """
    immediate_subscription_price = product_information.price_subscription[timestep - 1] * user_action.subscribe_action
    immediate_buy_price = product_information.price_base_product[timestep - 1] * user_action.buy_action.base_product + \
                          product_information.price_upgrade[timestep - 1] * user_action.buy_action.upgrade

    return immediate_subscription_price + immediate_buy_price


def get_expected_utility_and_payment_in_future(timestep, current_user_state, user_action, game):
    """
    Calculates the expected payment and utility for a user type, user action, and user state

    Parameters
    ----------
    timestep : int
        in thesis: n, the timestep the action is executed
    current_user_state : UserState
        current user state
    user_action : UserAction
        subscription and buy action
    game : Game
        collecting all information (i.e., states, best actions etc.)

    Returns
    -------
    float, float
        expected utility in future, expected payment in future
    """
    if timestep == game.n_max:
        expected_utility_in_future = 0
        expected_future_payment_with_subscription = 0
        # case 1 from thesis
        if user_action.subscribe_action == 0:
            utility_now = get_normalized_immediate_reward(timestep, game.n_upgrade, user_action,
                                                          game.user_type, current_user_state,
                                                          game.product_information) * game.user_type.valuation
            # geometric series with ownership
            expected_utility_in_future = utility_now / (
                    1 - game.user_type.quality_decay_factor * game.user_type.engagement_factor) - utility_now
        # subscribe_action == 1
        else:
            ownership_after_action = get_max_of_buying_and_ownership(user_action.buy_action,
                                                                     current_user_state.ownership)

            # case 2 from thesis
            if ownership_after_action.base_product == 0 and ownership_after_action.upgrade == 0:
                expected_future_utility_with_subscription, expected_future_payment_with_subscription = \
                    get_expected_future_utility_and_payment_with_subscription(game, current_user_state)

                expected_utility_in_future = expected_future_utility_with_subscription

            # case 3 from thesis
            elif ownership_after_action.base_product == 1 and ownership_after_action.upgrade == 0:
                expected_future_utility_with_subscription, expected_future_payment_with_subscription = \
                    get_expected_future_utility_and_payment_for_upgrade_with_subscription(game, current_user_state)

                utility_now_with_ownership = get_normalized_immediate_utility_with_ownership(timestep,
                                                                                             game.n_upgrade,
                                                                                             current_user_state,
                                                                                             ownership_after_action,
                                                                                             game.user_type,
                                                                                             game.product_information) * game.user_type.valuation
                # geometric series with ownership
                expected_utility_through_ownership_in_future = utility_now_with_ownership / (
                        1 - game.user_type.quality_decay_factor * game.user_type.engagement_factor) - \
                                                               utility_now_with_ownership

                expected_utility_in_future = expected_utility_through_ownership_in_future + \
                                             expected_future_utility_with_subscription

            # case 4 from thesis is already handled as subscription is never optimal if o = [1,1]

        return expected_utility_in_future, expected_future_payment_with_subscription
    # timesteps before n_max
    else:
        sum_of_expected_utilities = 0
        sum_of_expected_payments = 0
        next_user_states = game.user_states[timestep]
        for next_user_state in next_user_states:
            transition_probability = get_transition_probability(timestep, game.n_upgrade, next_user_state,
                                                                current_user_state, user_action,
                                                                game.user_type,
                                                                game.product_information.product_quality.upgrade,
                                                                is_calculating_future_expectancy=True)
            sum_of_expected_utilities += transition_probability * next_user_state.expected_utility
            sum_of_expected_payments += transition_probability * (
                    next_user_state.expected_payment_in_future + next_user_state.immediate_payment)
        return sum_of_expected_utilities, sum_of_expected_payments


def get_is_product_used(current_user_state, subscribe_action, ownership_with_action):
    """
    Displays if a product is used

    Parameters
    ----------
    current_user_state : UserState
        current user state
    subscribe_action : int
        1 if subscribe, else 0
    ownership_with_action : Ownership
        states if base product and upgrade are owned

    Returns
    -------
    bool
        true if product is used, else false
    """
    if current_user_state.demand == 1:
        if subscribe_action == 1:
            return True
        elif ownership_with_action.base_product == 1:
            return True
    return False


def get_normalized_immediate_utility_with_ownership(timestep, n_upgrade, user_state, ownership_after_action, user_type,
                                                    product_information):
    """
    Calculates the normalized immediate utility after an action, i.e. without payment

    Parameters
    ----------
    timestep : int
        in thesis: n, the timestep the action is executed
    n_upgrade : int
        in thesis: m, timestep of upgrade release
    user_state : UserState
        current user state
    ownership_after_action : Ownership
        ownership of base product and upgrade after an action
    user_type : UserType
        user type
    product_information : Product Information
        prices and quality of products

    Returns
    -------
    float
        normalized immediate utility with ownership
    """
    return user_state.demand * get_realized_quality(timestep, n_upgrade,
                                                    ownership_after_action,
                                                    user_type.quality_decay_factor,
                                                    product_information.product_quality)


def get_expected_future_utility_and_payment_with_subscription(game, current_user_state):
    """
    Calculates the expected future utility and payment with subscription

    Parameters
    ----------
    game : Game
        collects all important information such as states, best actions etc.
    current_user_state : UserState
        current user state

    Returns
    -------
    float, float
        expected future utility, expected future payment
    """
    if current_user_state.demand == 0:
        return 0, 0
    future_utility = 0
    future_payment = 0
    immediate_utility = 1
    timestep = game.n_max + 1
    while immediate_utility > 0:
        quality_factor_base_product = game.user_type.quality_decay_factor ** (timestep - 1)
        quality_factor_upgrade = game.user_type.quality_decay_factor ** (timestep - game.n_upgrade)
        quality_factor = quality_factor_base_product * game.product_information.product_quality.base_product + \
                         quality_factor_upgrade * game.product_information.product_quality.upgrade
        immediate_utility = quality_factor * game.user_type.valuation - game.product_information.price_subscription[
            game.n_max - 1]
        if immediate_utility >= 0:
            probability_reached = game.user_type.engagement_factor ** (timestep - game.n_max)
            future_utility += immediate_utility * probability_reached
            future_payment += game.product_information.price_subscription[game.n_max - 1] * probability_reached
        timestep += 1
    return future_utility, future_payment


def get_expected_future_utility_and_payment_for_upgrade_with_subscription(game, current_user_state):
    """
    Calculates the expected future utility and payment with subscription and ownership of base product

    Parameters
    ----------
    game : Game
        collects all important information such as states, best actions etc.
    current_user_state : UserState
        current user state

    Returns
    -------
    float, float
        expected future utility, expected future payment
    """
    if current_user_state.demand == 0:
        return 0, 0
    future_utility = 0
    future_payment = 0
    immediate_utility = 1
    timestep = game.n_max + 1
    while immediate_utility > 0:
        quality_factor_upgrade = game.user_type.quality_decay_factor ** (timestep - game.n_upgrade)
        quality_factor = quality_factor_upgrade * game.product_information.product_quality.upgrade
        immediate_utility = quality_factor * game.user_type.valuation - game.product_information.price_subscription[
            game.n_max - 1]
        if immediate_utility >= 0:
            probability_reached = game.user_type.engagement_factor ** (timestep - game.n_max)
            future_utility += immediate_utility * probability_reached
            future_payment += game.product_information.price_subscription[game.n_max - 1] * probability_reached
        timestep += 1
    return future_utility, future_payment


def get_preferred_action_if_deliver_equal_utility(first_action, second_action):
    """
    Returns the preferred action defined through fixed rules if utility is equal

    I.e., buy and subscribe as much as you can (instead of not buy or subscribe) and prefer buying before subscription


    Parameters
    ----------
    first_action : UserAction
        first action compared
    second_action : UserAction
        second action compared

    Returns
    -------
    float
        transition probability
    """
    first_action_total_actions = first_action.subscribe_action + first_action.buy_action.base_product + \
                                 first_action.buy_action.upgrade
    second_action_total_actions = second_action.subscribe_action + second_action.buy_action.base_product + \
                                  second_action.buy_action.upgrade
    first_action_total_buy_actions = first_action.buy_action.base_product + first_action.buy_action.upgrade
    second_action_total_buy_actions = second_action.buy_action.base_product + second_action.buy_action.upgrade

    if first_action_total_actions < second_action_total_actions:
        return second_action
    elif second_action_total_actions < first_action_total_actions:
        return first_action
    else:
        if first_action_total_buy_actions < second_action_total_buy_actions:
            return second_action
        elif second_action_total_buy_actions < first_action_total_buy_actions:
            return first_action
        else:
            if first_action.buy_action.base_product < second_action.buy_action.base_product:
                return second_action
            elif second_action.buy_action.base_product < first_action.buy_action.base_product:
                return first_action
    # fallback if actions are the same, i.e., first_action is not preferred and second_action is returned
    return second_action


def get_transition_probability(timestep, n_upgrade, next_user_state, current_user_state, user_action, user_type,
                               quality_upgrade, is_calculating_future_expectancy=False):
    """
    Calculates the transition probability from one state to another state

    Parameters
    ----------
    timestep : int
        in thesis: n, the timestep the action is executed
    n_upgrade : int
        in thesis: m, timestep of upgrade release
    next_user_state : UserState
        state to which transition probability is calculated
    current_user_state : UserState
        state from which transition probability is calculated
    user_action : UserAction
        action for which transition probability is calculated
    user_type : UserType
        user type
    quality_upgrade : float
        quality of upgrade
    is_calculating_future_expectancy : bool, optional
        true if forward induction is executed, false if backward induction is executed, default: False
    Returns
    -------
    float
        transition probability
    """

    if is_calculating_future_expectancy:
        timestep += 1
    ownership_with_action = get_max_of_buying_and_ownership(user_action.buy_action, current_user_state.ownership)
    product_is_used_in_current_user_state = get_is_product_used(current_user_state, user_action.subscribe_action,
                                                                ownership_with_action)

    if ownership_with_action.base_product == next_user_state.ownership.base_product and \
            ownership_with_action.upgrade == next_user_state.ownership.upgrade:
        # upgrade timestep has different effect if quality of upgrade is greater 0
        if timestep == n_upgrade and quality_upgrade > 0:
            if not product_is_used_in_current_user_state:
                if next_user_state.demand == 1 and current_user_state.demand == 1:
                    return 1
                elif next_user_state.demand == 0 and current_user_state.demand == 1:
                    return 0
            if next_user_state.demand == 1 and current_user_state.demand == 1:
                return user_type.engagement_factor + (1 - user_type.engagement_factor) * user_type.engagement_factor
            elif next_user_state.demand == 1 and current_user_state.demand == 0:
                return user_type.engagement_factor
            elif next_user_state.demand == 0 and current_user_state.demand == 1:
                return (1 - user_type.engagement_factor) * (1 - user_type.engagement_factor)
            elif next_user_state.demand == 0 and current_user_state.demand == 0:
                return 1 - user_type.engagement_factor

        else:
            if current_user_state.demand == 0 and next_user_state.demand == 0:
                return 1
            elif current_user_state.demand == 0:
                return 0
            if product_is_used_in_current_user_state:
                if next_user_state.demand == 1:  # and current_user_state.demand == 1
                    return user_type.engagement_factor
                elif next_user_state.demand == 0:  # and current_user_state.demand == 1
                    return 1 - user_type.engagement_factor
            else:
                if next_user_state.demand == 1:  # and current_user_state.demand == 1
                    return 1
                elif next_user_state.demand == 0:  # and current_user_state.demand == 1
                    return 0
    return 0
