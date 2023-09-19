import csv
import os

from src.numerical_framework.helpers.high_price import HighPrice

PARTITION_LINE = "-------------------------------------"


def count_rows_in_csv(file_name):
    """
    Counts the rows in a given .csv file

    Parameters
    ----------
    file_name : String
        file name with path

    Returns
    -------
    int
        number of rows in the csv
    """
    file = open(file_name)
    reader = csv.reader(file)
    return len(list(reader))


def write_csv_row(file_name, row):
    """
    Write a row to a given .csv file

    Parameters
    ----------
    file_name : String
        file name with path

    row : list[String]
        one element in the list per column which shall be written
    """
    with open(file_name, 'a+', encoding='UTF8', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(row)


def create_or_get_file(save_path, file_name):
    """
    Create or get a file at given location

    Parameters
    ----------
    save_path : String
        path to folder location where file shall be saved
    file_name : String
        file name with path
    """
    complete_name = os.path.join(save_path, file_name)
    if not os.path.exists(save_path):
        os.makedirs(save_path)
    if not os.path.exists(complete_name):
        file = open(complete_name, "w+")
        file.close()
    return complete_name


def add_first_line_to_document(file_name, line):
    """
    Insert given string as a new line at the beginning of a .txt file

    Parameters
    ----------
    file_name : String
        file name with path
    line : String
        object containing the information which are written to the file
    """
    # define name of temporary dummy file
    dummy_file = file_name + '.dummy'
    # open original file in read mode and dummy file in write mode
    with open(file_name, 'r') as read_obj, open(dummy_file, 'w') as write_obj:
        # Write given line to the dummy file
        write_obj.write(line + '\n')
        # Read lines from original file one by one and append them to the dummy file
        for line in read_obj:
            write_obj.write(line)
    # remove original file
    os.remove(file_name)
    # Rename dummy file as the original file
    os.rename(dummy_file, file_name)


def add_line_to_document(file_name, line):
    """
    Insert given string as a new line at the end of a .txt file

    Parameters
    ----------
    file_name : String
        file name with path
    line : String
        object containing the information which are written to the file
    """
    with open(file_name, 'a+') as write_obj:
        # Write new line to file
        write_obj.write(line + '\n')


def write_header_line_overview_csv_differential_evolution(n_max, path_main_file):
    """
    Write the header line to a .csv file for differential evolution results

    Parameters
    ----------
    n_max : int
        number of timesteps users arrive to the system and publisher can change prices
    path_main_file : String
        file name with path
    """
    header_row = ['Start time', 'Runtime', 'File Name', 'DE Strat.', 'Optimization Type', 'Number of evaluations',
                  'Bound base prod', 'Bound upgrade prod', 'Bound subscription', 'Num. user valuations', 'Popsize',
                  'Revenue', 'Welfare', 'Overall welf.', 'Base product']
    for i in range(1, n_max):
        header_row.append(' ')
    header_row.append('Upgrade')
    for i in range(1, n_max):
        header_row.append(' ')
    header_row.append('Subscription')
    for i in range(0, n_max - 1):
        header_row.append(' ')

    header_row.append('Revenue base product')
    for i in range(1, n_max):
        header_row.append(' ')
    header_row.append('Revenue upgrade')
    for i in range(1, n_max):
        header_row.append(' ')
    header_row.append('Revenue subscription')
    for i in range(0, n_max - 1):
        header_row.append(' ')
    header_row.append('Total revenue')
    header_row.append('Base price revenue')
    header_row.append('Upgrade revenue')
    header_row.append('Subscription revenue')
    header_row.append('n_max')
    header_row.append('n_upgrade')
    header_row.append('engagement_factor_short_term_user')
    header_row.append('engagement_factor_long_term_user')
    header_row.append('probability_short_term_user')
    header_row.append('quality_decay_factors')
    header_row.append('probability_of_second_quality_decay_element')
    header_row.append('valuation_range')
    header_row.append('standard_deviation_valuation')
    header_row.append('arrivals_in_first_timestep')
    header_row.append('product_quality_base_product')
    header_row.append('product_quality_upgrade')
    header_row.append('is_prices_discounted')
    header_row.append('is_subscription_price_variable')
    header_row.append('first_base_price_fixed')
    header_row.append('first_upgrade_price_fixed')
    header_row.append('user_arrival_time')
    header_row.append('user_valuation')
    header_row.append('user_engagement_factor')
    header_row.append('user_quality_decay_factor')

    write_csv_row(path_main_file, header_row)


def write_header_line_overview_csv_backward_induction(n_max, path_main_file):
    """
    Write the header line to a .csv file for backward induction results

    Parameters
    ----------
    n_max : int
        number of timesteps users arrive to the system and publisher can change prices
    path_main_file : String
        file name with path
    """
    header_row = ['Timestamp', 'File name', 'Num. user valuations', 'Prob. user type', 'user_arrival_time',
                  'user_valuation', 'user_engagement_factor', 'user_quality_decay_factor', 'Price Strategy Type',
                  'Revenue', 'Welfare', 'Overall welf.', 'Base product']
    for i in range(1, n_max):
        header_row.append(' ')
    header_row.append('Upgrade')
    for i in range(1, n_max):
        header_row.append(' ')
    header_row.append('Subscription')
    for i in range(0, n_max - 1):
        header_row.append(' ')
    header_row.append('Revenue base product')
    for i in range(1, n_max):
        header_row.append(' ')
    header_row.append('Revenue upgrade')
    for i in range(1, n_max):
        header_row.append(' ')
    header_row.append('Revenue subscription')
    for i in range(0, n_max - 1):
        header_row.append(' ')
    header_row.append('Total revenue')
    header_row.append('Base price revenue')
    header_row.append('Upgrade revenue')
    header_row.append('Subscription revenue')
    header_row.append('n_max')
    header_row.append('n_upgrade')
    header_row.append('engagement_factor_short_term_user')
    header_row.append('engagement_factor_long_term_user')
    header_row.append('probability_short_term_user')
    header_row.append('quality_decay_factors')
    header_row.append('probability_of_second_quality_decay_element')
    header_row.append('valuation_range')
    header_row.append('standard_deviation_valuation')
    header_row.append('arrivals_in_first_timestep')
    header_row.append('product_quality_base_product')
    header_row.append('product_quality_upgrade')

    write_csv_row(path_main_file, header_row)


def write_header_line_overview_csv_single_max_revenue(n_max, path_main_file):
    """
    Write the header line to a .csv file for single max revenue results

    Parameters
    ----------
    n_max : int
        number of timesteps users arrive to the system and publisher can change prices
    path_main_file : String
        file name with path
    """
    header_row = ['Timestamp', 'User valuation', 'User Arrival time', 'User Engagement factor',
                  'User Quality decay factor', 'Revenue', 'Welfare', 'Overall welf.', 'Optimal base product']
    for i in range(1, n_max):
        header_row.append(' ')
    header_row.append('Optimal upgrade')
    for i in range(1, n_max):
        header_row.append(' ')
    header_row.append('Subscription')
    for i in range(0, n_max - 1):
        header_row.append(' ')

    header_row.append('Revenue base product')
    for i in range(1, n_max):
        header_row.append(' ')
    header_row.append('Revenue upgrade')
    for i in range(1, n_max):
        header_row.append(' ')
    header_row.append('Revenue subscription')
    for i in range(0, n_max - 1):
        header_row.append(' ')
    header_row.append('Total revenue')
    header_row.append('Base price revenue')
    header_row.append('Upgrade revenue')
    header_row.append('Subscription revenue')
    header_row.append('n_max')
    header_row.append('n_upgrade')
    header_row.append('product_quality_base_product')
    header_row.append('product_quality_upgrade')

    write_csv_row(path_main_file, header_row)


def write_header_line_overview_csv_search_max_revenue(n_max, path_main_file):
    """
    Write the header line to a .csv file for search max revenue results

    Parameters
    ----------
    n_max : int
        number of timesteps users arrive to the system and publisher can change prices
    path_main_file : String
        file name with path
    """
    header_row = ['Timestamp', 'User valuation', 'User Arrival time', 'User Engagement factor',
                  'User Quality decay factor', 'Revenue', 'Welfare', 'Overall welf.', 'Optimal base product']
    for i in range(1, n_max):
        header_row.append(' ')
    header_row.append('Optimal upgrade')
    for i in range(1, n_max):
        header_row.append(' ')
    header_row.append('Subscription')
    for i in range(0, n_max - 1):
        header_row.append(' ')
    header_row.append('n_max')
    header_row.append('n_upgrade')
    header_row.append('product_quality_base_product')
    header_row.append('product_quality_upgrade')

    write_csv_row(path_main_file, header_row)


def fill_text_file_with_basic_information(differential_evolution_creator, file_path):
    """
    Write the basic information of differential evolution to the .txt file

    Parameters
    ----------
    differential_evolution_creator : DifferentialEvolutionCreator
        object containing all details about differential evolution specifics
    file_path : String
        file name with path
    """
    if differential_evolution_creator.price_bounds is not None:
        price_bounds = differential_evolution_creator.price_bounds
        price_bound_string = "Price Bounds:" + "buy: " + str(price_bounds.buy_min) + ", " + str(
            price_bounds.buy_max) + ", upgrade: " + str(
            price_bounds.upgrade_min) + ", " + str(price_bounds.upgrade_max) + ", subscription: " + str(
            price_bounds.subscription_min) + ", " + str(price_bounds.subscription_max)
        add_line_to_document(file_path, price_bound_string)

    number_of_user_types_string = "Number of user valuations: " + str(
        differential_evolution_creator.number_of_user_valuations)
    add_line_to_document(file_path, number_of_user_types_string)


def write_backward_induction_result(backward_induction_result):
    """
    Writes the results from backward induction into .csv files

    Parameters
    ----------
    backward_induction_result : BackwardInductionResult
        object containing all results about backward induction solution
    """
    information_row = [backward_induction_result.timestamp,
                       str(backward_induction_result.path_to_main_file),
                       str(backward_induction_result.number_of_user_valuations),
                       str(backward_induction_result.probability_user_type),
                       str(backward_induction_result.arrival_time),
                       str(backward_induction_result.valuation),
                       str(backward_induction_result.engagement_factor),
                       str(backward_induction_result.quality_decay_factor),
                       str(backward_induction_result.price_strategy_type),
                       str(backward_induction_result.expected_publisher_revenue),
                       str(backward_induction_result.expected_user_welfare),
                       str(backward_induction_result.expected_total_welfare)]

    for i in range(0, backward_induction_result.n_max):
        information_row.append(str(backward_induction_result.price_base_product[i]))
    for i in range(0, backward_induction_result.n_max):
        information_row.append(str(backward_induction_result.price_upgrade[i]))
    for i in range(0, backward_induction_result.n_max):
        information_row.append(str(backward_induction_result.price_subscription[i]))
    for i in range(0, backward_induction_result.n_max):
        information_row.append(str(backward_induction_result.revenue_base_product[i]))
    for i in range(0, backward_induction_result.n_max):
        information_row.append(str(backward_induction_result.revenue_upgrade[i]))
    for i in range(0, backward_induction_result.n_max):
        information_row.append(str(backward_induction_result.revenue_subscription[i]))

    information_row.append(backward_induction_result.expected_publisher_revenue)
    information_row.append(sum(backward_induction_result.revenue_base_product))
    information_row.append(sum(backward_induction_result.revenue_upgrade))
    information_row.append(sum(backward_induction_result.revenue_subscription))
    information_row.append(backward_induction_result.n_max)
    information_row.append(backward_induction_result.n_upgrade)
    information_row.append(backward_induction_result.engagement_factor_short_term_user)
    information_row.append(backward_induction_result.engagement_factor_long_term_user)
    information_row.append(backward_induction_result.probability_short_term_user)
    information_row.append(backward_induction_result.quality_decay_factors)
    information_row.append(backward_induction_result.probability_of_second_quality_decay_factor)
    information_row.append(backward_induction_result.valuation_range)
    information_row.append(backward_induction_result.standard_deviation_valuation)
    information_row.append(backward_induction_result.arrivals_in_first_timestep)
    information_row.append(backward_induction_result.product_quality_base_product)
    information_row.append(backward_induction_result.product_quality_upgrade)

    write_csv_row(backward_induction_result.path_to_main_file, information_row)

    if backward_induction_result.files_results_are_written_to is not None:
        for file in backward_induction_result.files_results_are_written_to:
            try:
                file_name = create_or_get_file(
                    backward_induction_result.path_to_folder, file)
                if count_rows_in_csv(file_name) == 0:
                    write_header_line_overview_csv_backward_induction(
                        backward_induction_result.n_max,
                        file_name)
                write_csv_row(file_name, information_row)
            except:
                raise Exception(
                    f"Error when creating {file} for backward induction.")


def write_differential_evolution_result(differential_evolution_result):
    """
    Writes the results from differential evolution into a row at .csv files

    Parameters
    ----------
    differential_evolution_result : DifferentialEvolutionResult
        object containing all results about differential evolution solution
    """
    information_row = [differential_evolution_result.start_time,
                       differential_evolution_result.runtime,
                       differential_evolution_result.path_to_main_file,
                       differential_evolution_result.differential_evolution_strategy,
                       differential_evolution_result.price_strategy_type,
                       differential_evolution_result.number_of_evaluations]
    if differential_evolution_result.price_bounds is not None:
        information_row.append(
            str(differential_evolution_result.price_bounds.buy_min) + "," + str(
                differential_evolution_result.price_bounds.buy_max))
        information_row.append(
            str(differential_evolution_result.price_bounds.upgrade_min) + ", " + str(
                differential_evolution_result.price_bounds.upgrade_max))
        information_row.append(
            str(
                differential_evolution_result.price_bounds.subscription_min) + ", " + str(
                differential_evolution_result.price_bounds.subscription_max))
    else:
        for i in range(0, 3):
            information_row.append('-')
    information_row.append(differential_evolution_result.number_of_user_valuations)
    information_row.append(differential_evolution_result.popsize)
    information_row.append(differential_evolution_result.expected_publisher_revenue)
    information_row.append(differential_evolution_result.expected_user_welfare)
    information_row.append(differential_evolution_result.expected_total_welfare)
    for i in range(0, differential_evolution_result.n_max):
        information_row.append(str(differential_evolution_result.price_base_product[i]))
    for i in range(0, differential_evolution_result.n_max):
        information_row.append(str(differential_evolution_result.price_upgrade[i]))
    for i in range(0, differential_evolution_result.n_max):
        information_row.append(str(differential_evolution_result.price_subscription[i]))
    for i in range(0, differential_evolution_result.n_max):
        information_row.append(str(differential_evolution_result.revenue_base_product[i]))
    for i in range(0, differential_evolution_result.n_max):
        information_row.append(str(differential_evolution_result.revenue_upgrade[i]))
    for i in range(0, differential_evolution_result.n_max):
        information_row.append(str(differential_evolution_result.revenue_subscription[i]))
    information_row.append(differential_evolution_result.expected_publisher_revenue)
    information_row.append(sum(differential_evolution_result.revenue_base_product))
    information_row.append(sum(differential_evolution_result.revenue_upgrade))
    information_row.append(sum(differential_evolution_result.revenue_subscription))
    information_row.append(str(differential_evolution_result.n_max))
    information_row.append(str(differential_evolution_result.n_upgrade))
    information_row.append(
        str(differential_evolution_result.engagement_factor_short_term_user))
    information_row.append(
        str(differential_evolution_result.engagement_factor_long_term_user))
    information_row.append(str(differential_evolution_result.probability_short_term_user))
    information_row.append(str(differential_evolution_result.quality_decay_factors))
    information_row.append(str(differential_evolution_result.probability_of_second_quality_decay_factor))
    information_row.append(str(differential_evolution_result.valuation_range))
    information_row.append(str(differential_evolution_result.standard_deviation_valuation))
    information_row.append(str(differential_evolution_result.arrivals_in_first_timestep))
    information_row.append(
        str(differential_evolution_result.product_quality_base_product))
    information_row.append(str(differential_evolution_result.product_quality_upgrade))
    information_row.append(str(differential_evolution_result.is_prices_discounted))
    information_row.append(
        str(differential_evolution_result.is_subscription_price_variable))
    information_row.append(str(differential_evolution_result.first_base_price_fixed))
    information_row.append(
        str(differential_evolution_result.first_upgrade_price_fixed))

    if not differential_evolution_result.evolution_with_all_user_types_from_game:
        information_row.append(str(differential_evolution_result.user_arrival_time))
        information_row.append(str(differential_evolution_result.user_valuation))
        information_row.append(
            str(differential_evolution_result.user_engagement_factor))
        information_row.append(
            str(differential_evolution_result.user_quality_decay_factor))

    else:
        information_row.append("-")
        information_row.append("-")
        information_row.append("-")
        information_row.append("-")

    write_csv_row(differential_evolution_result.path_to_main_file, information_row)

    if differential_evolution_result.files_results_are_written_to is not None:
        for file in differential_evolution_result.files_results_are_written_to:
            try:
                file_name = create_or_get_file(
                    differential_evolution_result.path_to_folder, file)
                if count_rows_in_csv(file_name) == 0:
                    write_header_line_overview_csv_differential_evolution(
                        differential_evolution_result.n_max,
                        file_name)
                write_csv_row(file_name, information_row)
            except:
                raise Exception(f"Error when creating {file} for backward induction.")


def write_single_maximize_revenue_result(single_maximize_revenue_result):
    """
    Writes the results from single maximize revenue into .csv files

    Parameters
    ----------
    single_maximize_revenue_result : SingleMaximizeRevenueResult
        object containing all results about single maximize revenue solution
    """
    information_row = [single_maximize_revenue_result.timestamp, single_maximize_revenue_result.user_valuation,
                       single_maximize_revenue_result.user_arrival_time,
                       str(single_maximize_revenue_result.user_engagement_factor),
                       str(single_maximize_revenue_result.user_quality_decay_factor),
                       str(single_maximize_revenue_result.expected_publisher_revenue),
                       str(single_maximize_revenue_result.expected_user_welfare),
                       str(single_maximize_revenue_result.expected_total_welfare)]

    # optimal base product prices
    for i in range(1, single_maximize_revenue_result.n_max + 1):
        information_row.append(str(single_maximize_revenue_result.price_base_product[i - 1]))

    # optimal upgrade prices
    for i in range(1, single_maximize_revenue_result.n_max + 1):
        information_row.append(str(single_maximize_revenue_result.price_upgrade[i - 1]))

    # optimal subscription prices
    for i in range(1, single_maximize_revenue_result.n_max + 1):
        information_row.append(str(single_maximize_revenue_result.price_subscription[i - 1]))

    # revenue information
    for i in range(0, single_maximize_revenue_result.n_max):
        information_row.append(str(single_maximize_revenue_result.revenue_base_product[i]))
    for i in range(0, single_maximize_revenue_result.n_max):
        information_row.append(str(single_maximize_revenue_result.revenue_upgrade[i]))
    for i in range(0, single_maximize_revenue_result.n_max):
        information_row.append(str(single_maximize_revenue_result.revenue_subscription[i]))
    information_row.append(str(single_maximize_revenue_result.expected_publisher_revenue))
    information_row.append(str(sum(single_maximize_revenue_result.revenue_base_product)))
    information_row.append(str(sum(single_maximize_revenue_result.revenue_upgrade)))
    information_row.append(sum(single_maximize_revenue_result.revenue_subscription))
    information_row.append(str(single_maximize_revenue_result.n_max))
    information_row.append(str(single_maximize_revenue_result.n_upgrade))
    information_row.append(str(single_maximize_revenue_result.product_quality_base_product))
    information_row.append(str(single_maximize_revenue_result.product_quality_upgrade))
    write_csv_row(single_maximize_revenue_result.path_to_main_file, information_row)

    if single_maximize_revenue_result.files_results_are_written_to is not None:
        for file in single_maximize_revenue_result.files_results_are_written_to:
            try:
                file_name = create_or_get_file(single_maximize_revenue_result.path_to_folder, file)
                if count_rows_in_csv(file_name) == 0:
                    write_header_line_overview_csv_single_max_revenue(
                        single_maximize_revenue_result.n_max,
                        file_name)
                write_csv_row(file_name, information_row)
            except:
                raise Exception(f"Error when creating {file} for single max search.")


def write_search_maximize_revenue_result(search_maximize_revenue_result):
    """
    Writes the results from search maximize revenue into .csv files

    Parameters
    ----------
    search_maximize_revenue_result : SearchMaximizeRevenueResult
        object containing all results about search maximize revenue solution
    """
    information_row = [search_maximize_revenue_result.timestamp, search_maximize_revenue_result.user_valuation,
                       search_maximize_revenue_result.user_arrival_time,
                       search_maximize_revenue_result.user_engagement_factor,
                       search_maximize_revenue_result.user_quality_decay_factor,
                       search_maximize_revenue_result.expected_publisher_revenue,
                       search_maximize_revenue_result.expected_user_welfare,
                       search_maximize_revenue_result.expected_total_welfare]

    # optimal base product prices
    for i in range(0, search_maximize_revenue_result.n_max):
        information_row.append(search_maximize_revenue_result.price_base_product[i])

    # optimal upgrade prices
    for i in range(0, search_maximize_revenue_result.n_max):
        information_row.append(search_maximize_revenue_result.price_upgrade[i])

    # subscription prices
    for i in range(0, search_maximize_revenue_result.n_max):
        information_row.append(HighPrice)

    # general information
    information_row.append(search_maximize_revenue_result.n_max)
    information_row.append(search_maximize_revenue_result.n_upgrade)
    information_row.append(search_maximize_revenue_result.product_quality_base_product)
    information_row.append(search_maximize_revenue_result.product_quality_upgrade)
    write_csv_row(search_maximize_revenue_result.path_to_main_file, information_row)
