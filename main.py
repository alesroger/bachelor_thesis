import configparser
from datetime import datetime

from src.numerical_framework.backward_induction.backward_induction import backward_induction_over_user_types
from src.numerical_framework.differential_evolution.differential_evolution import \
    differential_evolution_maximize_revenue
from src.numerical_framework.helpers.framework_creators import SearchMaximizeRevenueCreator, \
    get_and_validate_backward_induction_input_from_config_ini, \
    get_and_validate_single_max_revenue_input_from_config_ini, \
    get_and_validate_differential_evolution_input_from_config_ini
from src.numerical_framework.helpers.output_files_helper import create_or_get_file, \
    write_header_line_overview_csv_backward_induction, \
    write_header_line_overview_csv_differential_evolution, write_header_line_overview_csv_single_max_revenue, \
    write_header_line_overview_csv_search_max_revenue
from src.numerical_framework.search_maximize_revenue.search_maximize_revenue import search_maximize_revenue
from src.numerical_framework.single_maximize_revenue.single_maximize_revenue import single_maximize_revenue


def backward_induction(config):
    backward_induction_creator = get_and_validate_backward_induction_input_from_config_ini(config)

    start_time = datetime.now()
    main_file_name = start_time.strftime(
        "%m.%d.%Y_%H.%M.%S") + "_backward_induction_" + backward_induction_creator.price_strategy_type + ".csv"
    path_main_file = create_or_get_file(backward_induction_creator.path_to_folder, main_file_name)
    write_header_line_overview_csv_backward_induction(backward_induction_creator.n_max, path_main_file)

    backward_induction_creator.path_to_main_file = path_main_file
    backward_induction_over_user_types(backward_induction_creator)


def differential_evolution(config):
    differential_evolution_creator = get_and_validate_differential_evolution_input_from_config_ini(config)

    # create main file
    start_time = datetime.now()
    main_file_name_without_csv = start_time.strftime(
        "%m.%d.%Y_%H.%M.%S") + "_" + f"{differential_evolution_creator.price_strategy_type}"
    main_file_name = main_file_name_without_csv + ".csv"
    path_main_file = create_or_get_file(differential_evolution_creator.path_to_folder, main_file_name)
    write_header_line_overview_csv_differential_evolution(differential_evolution_creator.n_max, path_main_file)

    differential_evolution_creator.path_to_main_file = path_main_file
    differential_evolution_creator.name_main_file_without_ending = main_file_name_without_csv

    differential_evolution_maximize_revenue(differential_evolution_creator)


def single_max_revenue(config):
    single_maximize_revenue_creator = get_and_validate_single_max_revenue_input_from_config_ini(config)

    # create main file
    start_time = datetime.now()
    main_file_name = start_time.strftime("%m.%d.%Y_%H.%M.%S") + "_" + "single_max_search.csv"
    path_main_file = create_or_get_file(single_maximize_revenue_creator.path_to_folder, main_file_name)
    write_header_line_overview_csv_single_max_revenue(single_maximize_revenue_creator.n_max, path_main_file)

    single_maximize_revenue_creator.path_to_main_file = path_main_file
    single_maximize_revenue(single_maximize_revenue_creator)


def search_max_revenue(config):
    search_maximize_revenue_creator = SearchMaximizeRevenueCreator()
    try:
        local_path_to_file_folder = config.get('MAIN', 'local_path_to_file_folder_search_max_revenue')
    except ValueError:
        return f'local_path_to_file_folder_search_max_revenue in MAIN must be a valid path but is {config.get("MAIN", "local_path_to_file_folder_search_max_revenue")}.'
    start_time = datetime.now()
    main_file_name = start_time.strftime("%m.%d.%Y_%H.%M.%S") + "_" + "search_maximize_revenue.csv"
    path_main_file = create_or_get_file(local_path_to_file_folder, main_file_name)
    n_max = 2
    write_header_line_overview_csv_search_max_revenue(n_max, path_main_file)
    search_maximize_revenue_creator.path_to_main_file = path_main_file

    search_maximize_revenue(search_maximize_revenue_creator)


if __name__ == '__main__':
    try:
        config = configparser.RawConfigParser()
        config.read('config.ini')
        operation_type = config.get('MAIN', 'type')
        if operation_type == 'BACKWARD_INDUCTION':
            print("Backward induction started")
            backward_induction(config)
            print("Backward induction finished")
        elif operation_type == 'DIFFERENTIAL_EVOLUTION':
            print("Differential evolution started")
            differential_evolution(config)
            print("Differential evolution finished")
        elif operation_type == 'SINGLE_MAX_REVENUE':
            print("Single max revenue started")
            single_max_revenue(config)
            print("Single max revenue finished")
        elif operation_type == 'SEARCH_MAX_REVENUE':
            print("Search max revenue started")
            search_max_revenue(config)
            print("Search max revenue finished")
        else:
            print(
                'type in MAIN in config.ini must be BACKWARD_INDUCTION or DIFFERENTIAL_EVOLUTION or SINGLE_MAX_REVENUE or SEARCH_MAX_REVENUE')

    except ValueError:
        raise Exception(
            'folder where src is located must contain config.ini file with argument type in section MAIN')
