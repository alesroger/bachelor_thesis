from scipy.stats import truncnorm


class UserType(object):
    """
    A class used to represent a User Type

    ...

    Attributes
    ----------
    arrival_time : int
        timestep user arrives to the system
    engagement_factor : float
        the probability of not loosing demand in the next timestep
    quality_decay_factor : float
        rate with which product looses quality in each timestep
    valuation : int
        value has for a product of quality 1
    """

    def __init__(self, arrival_time, engagement_factor, quality_decay_factor, valuation):
        """
        Parameters

        ....


        ----------
        arrival_time : int
            timestep user arrives to the system
        engagement_factor : float
            the probability of not loosing demand in the next timestep
        quality_decay_factor : float
            rate with which product looses quality in each timestep
        valuation : int
            value has for a product of quality 1
        """
        self.arrival_time = arrival_time
        self.engagement_factor = engagement_factor
        self.quality_decay_factor = quality_decay_factor
        self.valuation = valuation


def get_probability_user_type(user_type, creator, single_arrivals_in_first_timestep,
                              single_probability_of_second_quality_decay_element,
                              single_engagement_factor_short_term_user):
    """
    Calculates the Probability of User Type (except valuation)

    Parameters
    ----------
    user_type : UserType
        user type to be analyzed

    creator: AbstractGameCreator
        creator defined through config.ini

    single_arrivals_in_first_timestep: int
        x_a from thesis defining arrival distribution

    single_probability_of_second_quality_decay_element: float
        x_gamma from thesis defining quality decay distribution

    single_engagement_factor_short_term_user: float
        x_delta from thesis defining engagement factor distribution

    Returns
    -------
    float
        probability of user type
    """

    probability_arrival_time = get_probability_arrival_time(user_type.arrival_time,
                                                            single_arrivals_in_first_timestep,
                                                            creator.n_max)
    probability_quality_decay_factor = get_probability_quality_decay_factor(user_type.quality_decay_factor,
                                                                            creator.quality_decay_factors,
                                                                            single_probability_of_second_quality_decay_element)
    probability_engagement_factor = get_probability_engagement_factor(user_type.engagement_factor,
                                                                      single_engagement_factor_short_term_user,
                                                                      creator.engagement_factor_long_term_user,
                                                                      creator.probability_short_term_user)
    return probability_arrival_time * probability_quality_decay_factor * probability_engagement_factor


def get_probability_arrival_time(arrival_time, arrivals_in_first_timestep, n_max):
    """
    Calculates the Probability of Arrival Time

    Parameters
    ----------
    arrival_time : int
        arrival time of user type

    arrivals_in_first_timestep: int
        x_a from thesis defining arrival distribution

    n_max: int
        last timesteps user arrive to the system

    Returns
    -------
    float
        probability arrival time
    """
    if arrival_time == 1:
        return arrivals_in_first_timestep / (arrivals_in_first_timestep + n_max - 1)
    else:
        return 1 / (arrivals_in_first_timestep + n_max - 1)


def get_probability_quality_decay_factor(quality_decay_factor, quality_decay_factors_game,
                                         probability_second_quality_decay_element):
    """
    Calculates the Probability of Quality Decay Factor


    Parameters
    ----------
    quality_decay_factor : float
        quality decay factor of user type

    quality_decay_factors_game: List[float]
        the three quality decay factors defining the user types

    probability_second_quality_decay_element: float
        x_gamma from thesis defining quality decay distribution

    Returns
    -------
    float
        probability quality decay factor
    """
    if quality_decay_factor == quality_decay_factors_game[0] or \
            quality_decay_factor == quality_decay_factors_game[2]:
        return 0.5 * (1 - probability_second_quality_decay_element)
    else:
        return probability_second_quality_decay_element


def get_probability_engagement_factor(engagement_factor, engagement_factor_short_term_user,
                                      engagement_factor_long_term_user, probability_short_term_user):
    """
    Calculates the Probability of Engagement Factor

    Parameters
    ----------
    engagement_factor : float
        engagement factor of user type

    engagement_factor_short_term_user: float
        engagement factor of short term user

    engagement_factor_long_term_user: float
        engagement factor long term user

    probability_short_term_user: float
        x_delta from thesis defining engagement factor distribution

    Returns
    -------
    float
        probability engagement factor
    """
    if engagement_factor_short_term_user != engagement_factor_long_term_user:
        if engagement_factor == engagement_factor_long_term_user:
            return 1 - probability_short_term_user
        elif engagement_factor == engagement_factor_short_term_user:
            return probability_short_term_user
    else:
        return 0.5


# source: https://stackoverflow.com/questions/18441779/how-to-specify-upper-and-lower-limits-when-using-numpy-random-normal [August, 6, 2021]
def get_truncated_normal(mean, sd, low, upp):
    """
    Creates the Truncated Normal Distribution for User Valuations

    Parameters
    ----------
    mean : int
        mean of valuation range

    sd: int
        standard deviation of normal distribution

    low: int
        lower bound of normal distribution

    upp: int
        upper bound of normal distribution

    Returns
    -------
    truncnorm
        normal distribution for user valuations
    """
    return truncnorm(
        (low - mean) / sd, (upp - mean) / sd, loc=mean, scale=sd)
