# REVENUE MAXIMIZER
The REVENUE MAXIMIZER was developed for a BSc thesis at the University of Zurich in 2021 at the Computation and Economics Research Group. The implemented numerical framework in Python lets a software publisher (e.g. a Game-Studio) maximize his revenue in the context of a game theoretic model where the publisher acts in a system with different user types having demand for his product. To claim the right to use the product the users can either buy a perpetual or subscription license.

Details about the model can be found in the **thesis**. See the sections below to get started using the numerical framework for your own calculations.

## What is the thesis investigating?

This is taken from the abstract of the thesis to summarize the research this code was developed for. The thesis investigates the revenue potential of different pricing strategies for a single software distribution. The game-theoretic model presented is tailor-made to analyze software revenue in the domain of consumer software such as video games. A publisher is maximizing his expected revenue in a system with many different user types, each of them responding optimally to the publishers' pricing strategy. The publisher has three choices, to offer perpetual licenses only, subscription licenses only, or both. To attract more users, the publisher can adjust prices over time. The users' equilibrium strategies for this Markov Decision Process are found through backward induction. The publisher's revenue is searched via differential evolution. Numerical analysis finds that although many publishers in practice only provide perpetual licenses, by offering a subscription option they can increase revenue significantly. Revenue can be raised again if both options are offered in parallel. In this last setting, the majority of revenue is attributed to selling subscription licenses.

## The 4 main functions in the REVENUE MAXIMIZER

- DIFFERENTIAL_EVOLUTION finds the optimal prices through differential evolution for a publisher trying to maximize his revenue in a system with multiple user types, each of them acting optimally.
- BACKWARD_INDUCTION works fundamentally different, the chosen prices by the publisher have to be given as input. Then, the optimal actions of every user type in the system are calculated through backward induction to find publisher revenue, user welfare and other details for the chosen prices.

Less importantly, two functions used to explain a theoretical approach in the appendix of the thesis are defined as follows: 

- SINGLE_MAX_REVENUE finds the optimal price vectors for a single user type if only perpetual licenses can be offered by the publisher. (Section B1 of the appendix in the thesis)
- SEARCH_MAX_REVENUE is a hardcoded version of a theoretical search for optimal prices by the publisher in a system with multiple user types if the publisher can only offer perpetual licenses. (Section B2 of the appendix in the thesis)

## Using REVENUE MAXIMIZER

It's important to preserve the file structure within the folder, i.e., you need the **src** folder, the **main.py** file and the **config.ini** file located at the same folder. 

BACKWARD_INDUCTION, SINGLE_MAX_REVENUE and SEARCH_MAX_REVENUE can be run locally in reasonable time. For DIFFERENTIAL_EVOLUTION (at least for cases with many variables (i.e., many timesteps, different ask prices in every timestep etc.)) it is recommended to run the code on a cluster due to longer runtime. 

### Locally
You can run the main file on an IDE such as [PyCharm](https://www.jetbrains.com/de-de/pycharm/) or through command line with "python main.py" at the folder where the main.py file is located. You have to specify the details of the run through the "config.ini" file, located at the same folder.

Prerequisite: Python installed on your device.

### Cluster
The following instructions hold for a cluster accessed through ssh-connection such as [Minion/Kraken Cluster](https://dokuwiki.ifi.uzh.ch/!hpc/doku.php?id=minion_wiki) at IfI at UZH.

Prerequiste: Install the latest 3.x version of the Anaconda distribution of Python. A good tutorial can be found [here](https://problemsolvingwithpython.com/01-Orientation/01.05-Installing-Anaconda-on-Linux/).

You can use the template shell script **revMaxScript.sh** to run the code:

- Edit the revMaxScript.sh and replace the username "ehrensperger" with your own username. 
- command "sbatch revMaxScript.sh" runs the main.py file, specifying the details of the run through the "config.ini" file

## Run specifications
Run specifications are managed through the **config.ini** file. The following table summarizes the different options. For a deeper understanding of the parameters, it would be helpful to read section 3 of the thesis explaining the game-theoretic model.



|parameter name in config.ini                                               |Python datatype                         |parameter name in thesis                       |Further description                                                                                                                                                                  |
|------------------------------------------------|------------------------|------------------------|-------------------------------------------------------------------------------------------------------------------------------------------------------------------|
|**[MAIN]**                                         |                        |                        |                                                                                                                                                                   |
|type                                            |str                     |                        |must be DIFFERENTIAL_EVOLUTION, BACKWARD_INDUCTION,  SINGLE_MAX_REVENUE or SEARCH_MAX_REVENUE to run the corresponding type of operation                           |
|local_path_to_file_folder_differential_evolution|str                     |                        |local file folder for output files of differential evolution                                                                                                       |
|local_path_to_file_folder_backward_induction    |str                     |                        |local file folder for output files of backward induction                                                                                                           |
|local_path_to_file_folder_single_max_revenue    |str                     |                        |local file folder for output files of single max revenue                                                                                                           |
|local_path_to_file_folder_search_max_revenue    |str                     |                        |local file folder for output files of search max revenue                                                                                                           |
|**[GAME INFORMATION]**                             |                        |                        |                                                                                                                                                                   |
|price_strategy_type                             |str                     |$`p_t`$                 |must be BUY, SUB, BOTH or BOTH_BUY                                                                                                                                 |
|n_max                                           |int                     |$`n_{max}`$             |number of timesteps for which users arrive and publisher sets different prices                                                                                     |
|n_upgrade                                       |int                     |$`m`$                   |timestep of upgrade release                                                                                                                                        |
|arrivals_in_first_timestep                      |list of int             |$`x_a`$                 |defines the arrival distribution $`f_a`$ of user types                                                                                                             |
|quality_decay_factors                           |list of floats          |                        |list of length 3, defining the 3 quality decay factors of user types                                                                                               |
|probability_of_second_quality_decay_element     |list of floats          |$`x_\gamma`$            |second quality decay element gets assigned this probability defining the distribution $`f_\gamma`$ of user types                                                   |
|engagement_factor_short_term_user               |list of floats          |$`x_{\delta_s}`$        |                                                                                                                                                                   |
|engagement_factor_long_term_user                |float                   |$`x_{\delta_l}`$        |                                                                                                                                                                   |
|probability_short_term_user                     |float                   |$`P(x_{\delta_s})`$     |                                                                                                                                               |
|valuation range                                 |list of ints (or floats)|                        |list of length 2, defining lower and upper bound of user values                                                                                                    |
|standard_deviation_valuation                    |list of ints (or floats)|$`\sigma`$              |defining normal valuation distribution $`f_v`$                                                                                                                     |
|number_of_user_valuations                       |list of int             |$`x_u`$                 |discrete number of user valuations to approximate the normally distributed user values                                                                             |
|product_quality_base_product                    |int (or float)          |$`q_b`$                 |                                                                                                                                                                   |
|product_quality_base_product                    |int (or float)          |$`q_u`$                 |                                                                                                                                                                   |
|**[DIFFERENTIAL_EVOLUTION]**                        |                        |                        |                                                                                                                                                                   |
|evolution_with_all_user_types_from_game         |bool                    |                        |True: evaluate for settings in [GAME_INFORMATION]                                                                                                                  |
|                                                |                        |                        |False: evaluate for single user type in section [DIFFERENTIAL_EVOLUTION] (parameters starting with user_)                                                          |
|play_different_ask_prices                       |bool                    |                        |True: perpetual price can be set individually for every timestep for base product and upgrade                                                                      |
|                                                |                        |                        |False: allows for price change of base product in timestep m only (Dierks and Seuken (2020))                                                                       |
|is_prices_discounted                            |bool                    |                        |True: first base price and upgrade price are largest                                                                                                               |
|                                                |                        |                        |False: prices can be freely chosen                                                                                                                                 |
|is_subscription_price_variable                  |bool                    |                        |True: subscription price can be lowered in every timestep                                                                                                          |
|                                                |                        |                        |False: subscription price constant                                                                                                                                 |
|first_base_price_fixed                          |float                   |                        |special evaluation option, if first base price is known or wants to be defined. If 0, no base price fixed, if larger, base price is fixed                          |
|first_upgrade_price_fixed                       |float                   |                        |special evaluation option, if first upgrade price is known or wants to be defined. If 0, no upgrade price fixed, if larger, first upgrade price is fixed           |
|price_bounds_base_product                       |list of ints (or floats)|                        |length 2, defining lower and upper bound of base price                                                                                                             |
|price_bounds_upgrade                            |list of ints (or floats)|                        |length 2, defining lower and upper bound of upgrade price                                                                                                          |
|price_bounds_subscription                       |list of ints (or floats)|                        |length 2, defining lower and upper bound of subscription price                                                                                                     |
|base_price                                      |list of floats (or ints)|$`p_b`$                 |only necessary if price_strategy_type = BOTH_BUY, defining the fixed price vector of base product. length n_max.                                                   |
|upgrade_price                                   |list of floats (or ints)|$`p_u`$                 |only necessary if price_strategy_type = BOTH_BUY, defining the fixed price vector of upgrade. length n_max.                                                        |
|user_valuation                                  |int (or float)          |$`v`$                   |single user valuation if evolution_with_all_user_types_from_game = False                                                                                           |
|user_arrival_time                               |int                     |$`n_a`$                 |single user arrival time if evolution_with_all_user_types_from_game = False                                                                                        |
|user_quality_decay_factor                       |float                   |$`\gamma`$              |single user quality decay factor if evolution_with_all_user_types_from_game = False                                                                                |
|user_engagement_factor                          |float                   |$`\delta`$              |single user engagement factor if evolution_with_all_user_types_from_game = False                                                                                   |
|print_result_every_x_iterations                 |int                     |                        |write information about evolution to .txt file to monitor progress                                                                                                 |
|print_result_for_the_first_x_iterations         |int                     |                        |write information about evolution to .txt file to monitor progress                                                                                                 |
|popsizes                                        |list of int             |                        |specification for differential evolution setting the population size                                                                                               |
|                                                |                        |                        |Note: numbers < 15 are set to 15 by default. See: https://docs.scipy.org/doc/scipy/reference/generated/scipy.optimize.differential_evolution.html [August 22, 2021]|
|differential_evolution_strategies               |string                  |                        |specification for differential evolution setting the strategy such as best1bin, rand2bin and many more                                                             |
|                                                |                        |                        |See: https://docs.scipy.org/doc/scipy/reference/generated/scipy.optimize.differential_evolution.html [August 22, 2021]                                             |
|number_of_iterations_per_evolution_type         |int                     |                        |evaluate the same type of evolutions multiple times, especially useful for a best-of-x evolution search                                                            |
|files_diff_evolution_results_are_written_to     |list of str             |                        |csv-files, end result of evolution is written to in folder local_path_to_file_folder_differential_evolution                                                        |
|**[BACKWARD_INDUCTION]**                            |                        |                        |                                                                                                                                                                   |
|induction_with_all_user_types_from_game         |bool                    |                        |True: evaluate for settings in [GAME_INFORMATION]                                                                                                                  |
|                                                |                        |                        |False: evaluate for list of user types in section [BACKWARD_INDUCTION] (parameters starting with user_)                                                            |
|base_price                                      |                        |$`p_b`$                 |length n_max. setting the base prices for the corresponding timesteps                                                                                              |
|upgrade_price                                   |                        |$`p_u`$                 |length n_max. setting the upgrade prices for the corresponding timesteps                                                                                           |
|subscription_price                              |                        |$`p_s`$                 |length n_max. setting the subscription prices for the corresponding timesteps                                                                                      |
|print_user_types_combined                       |bool                    |                        |only if induction_with_all_user_types_from_game = True. result for all user types (i.e., probabilities of user types summed up to 1) is written to csv file        |
|print_single_user_types                         |bool                    |                        |only if induction_with_all_user_types_from_game = True. result for every single user type is written to csv file                                                   |
|user_valuations                                 |list of int (or float)  |$`v`$                   |single user valuations if evolution_with_all_user_types_from_game = False                                                                                          |
|user_arrival_times                              |list of int             |$`n_a`$                 |single user arrival times if evolution_with_all_user_types_from_game = False                                                                                       |
|user_quality_decay_factors                      |list of float           |$`\gamma`$              |single user quality decay factors if evolution_with_all_user_types_from_game = False                                                                               |
|user_engagement_factors                         |list of float           |$`\delta`$              |single user engagement factors if evolution_with_all_user_types_from_game = False                                                                                  |
|files_backward_induction_results_are_written_to |                        |                        |csv-files, result of induction is written to in folder local_path_to_file_folder_backward_induction                                                                |
|**[SINGLE_MAX_REVENUE]**                           |                        |                        |                                                                                                                                                                   |
|user_valuations                                 |list of int (or float)  |$`v`$                   |single user valuations                                                                                                                                             |
|user_arrival_times                              |list of int             |$`n_a`$                 |single user arrival times                                                                                                                                          |
|user_quality_decay_factors                      |list of float           |$`\gamma`$              |single user quality decay factors                                                                                                                                  |
|user_engagement_factors                         |list of float           |$`\delta`$              |single user engagement factors                                                                                                                                     |
|files_single_max_revenue_results_are_written_to |                        |                        |csv-files, result of induction is written to in folder local_path_to_file_folder_single_max_revenue                                                                |


## Output interpretation

- DIFFERENTIAL_EVOLUTION: at the folder defined, a .csv file is created together with a new folder. This folder contains a .txt file for every differential evolution, containing the details of the differential evolution and how the differential evolution found the solution through its evaluations. It depends on the parameters "print_result_every_x_iterations" and "print_result_for_the_first_x_iterations" how often the progress is printed to the .txt file. If you are only interested in the end result of the differential evolution, it is enough to look at the .csv file created at the output folder defined trough the config.ini. This .csv file only contains the end results of the differential evolution, e.g. the publisher revenue, user welfare, price vectors and much more.

- BACKWARD_INDUCTION, SINGLE_MAX_REVENUE, SEARCH_MAX_REVENUE: at the folder defined, a new .csv file is created, containing all end results, displaying publisher revenue, user welfare, price vectors and much more.


## High-level components

- **config.ini** is used to manage a single execution of the code, i.e., all important parameters have to be set there

- **main.py** is the main file which has to be run to execute the code

- **src** is the folder containing the code
    - **model** is the folder containing code defining the theoretical model
    - **numerical framework** is the folder containing code defining the executable numerical operations with the model, e.g. backward induction and differential evolution

- **test** is the folder containing the most important unit tests. Note that there is a **tests_during_execution.py** file in the folder numerical_framework/helpers which covers tests for the probability of the reached states and probability of the user types while the code is executed.

## Roadmap 

The code is written in object-oriented style. It should be easily extendable, e.g. new validators can be added or the result object can be extended with further details. As a new developer you could add the following functionalities, presented in section 6 about Limitations and Future Work of the **thesis**:

- **User with partial information.** The full information assumption is not realistic in practice. An interesting consideration would be the uncertainty about the own user type, i.e. a user will not know his valuation, engagement factor and quality decay factor before playing the game and could learn about his preferences from timestep to timestep. A machine learning model (typically Reinforcement Learning can be used to solve MDPs(Russell & Norvig, 1995)) could be deployed, where users would learn about their optimal actions instead of calculating them deterministically through backward induction as in this thesis.

- **Multiple upgrades.** Many games on Steam allow for multiple upgrades, e.g. games such as Stellaris which are further developed over time. This possible model extension could also help or even be necessary to do an exact model calibration if sales data would be available from a game with multiple upgrades.

- **Duopoly instead of monopoly.** Another setting known from literature would be a duopoly instead of a monopoly, where two publishers are selling a qualitatively identical product and are competing against each other. (Balasubramanian et al., 2015)


## Author and acknowledgement

The REVENUE MAXIMIZER was developed in the framework of the BSc thesis from Tim Ehrensperger (@alesroger) at the chair of Computation and Economics Research Group at the University of Zurich from March to August 2021. If you want to contact me you can reach me at: tim.ehrensperger@uzh.ch.

I want to sincerely thank Dr. Ludwig Dierks, the responsible assistant for my BSc thesis, for his weekly support – even on weekends if necessary. I would like to thank Prof. Dr. Sven Seuken as well for giving me the opportunity to write my bachelor thesis at his institute and his very useful inputs. Furthermore, a big thank you to the whole Computation and Economics Research Group who has stimulated my interest in this area. And lastly, thank you to my family and friends for their support, especially to the ones proofreading the thesis or the code.

