"""Model runner to use in place of smif for standalone modelruns
- run over multiple years
- make rule-based intervention decisions at each timestep
"""
# pylint: disable=C0103
import configparser
import csv
import os
import time
import collections
from datetime import timedelta

from digital_comms.ccam import ICTManager
from digital_comms.interventions import decide_interventions
from digital_comms.results import Results
import digital_comms.save_data as save_data


################################################################
# SETUP MODEL RUN CONFIGURATION
# - timesteps, scenarios, strategies
# - data files base path
################################################################

CONFIG = configparser.ConfigParser()
CONFIG.read(os.path.join(os.path.dirname(__file__), 'script_config.ini'))

INPUT_FOLDER = CONFIG['file_locations']['input_folder']
OUTPUT_FOLDER = CONFIG['file_locations']['output_folder']
SHAPEFILE_PATH = os.path.join(INPUT_FOLDER, 'visualization', 'LAD_shapes')

# Create sub-directories for results
if not os.path.exists(os.path.join(OUTPUT_FOLDER, 'csv')):
    os.makedirs(os.path.join(OUTPUT_FOLDER, 'csv'))
if not os.path.exists(os.path.join(OUTPUT_FOLDER, 'figures')):
    os.makedirs(os.path.join(OUTPUT_FOLDER, 'figures'))
if not os.path.exists(os.path.join(OUTPUT_FOLDER, 'figures', 'detail_per_year')):
    os.makedirs(os.path.join(OUTPUT_FOLDER, 'figures', 'detail_per_year'))
if not os.path.exists(os.path.join(OUTPUT_FOLDER, 'figures', 'summary')):
    os.makedirs(os.path.join(OUTPUT_FOLDER, 'figures', 'summary'))
if not os.path.exists(os.path.join(OUTPUT_FOLDER, 'maps')):
    os.makedirs(os.path.join(OUTPUT_FOLDER, 'maps'))
if not os.path.exists(os.path.join(OUTPUT_FOLDER, 'maps', 'detail_per_year')):
    os.makedirs(os.path.join(OUTPUT_FOLDER, 'maps', 'detail_per_year'))
if not os.path.exists(os.path.join(OUTPUT_FOLDER, 'gifs')):
    os.makedirs(os.path.join(OUTPUT_FOLDER, 'gifs'))
if not os.path.exists(os.path.join(OUTPUT_FOLDER, 'figures', 'auxgifs')):
    os.makedirs(os.path.join(OUTPUT_FOLDER, 'figures', 'auxgifs'))
if not os.path.exists(os.path.join(OUTPUT_FOLDER, 'maps', 'auxgifs')):
    os.makedirs(os.path.join(OUTPUT_FOLDER, 'maps', 'auxgifs'))

print('')
print('----------------------------------')
print('Input  folder is: ' + INPUT_FOLDER)
print('Output folder is:   ' + OUTPUT_FOLDER)
print('----------------------------------')

results = Results(OUTPUT_FOLDER, SHAPEFILE_PATH)

BASE_YEAR = 2020
END_YEAR = 2030
TIMESTEP_INCREMENT = 1
TIMESTEPS = range(BASE_YEAR, END_YEAR + 1, TIMESTEP_INCREMENT)

# Annual capital budget constraint for the whole industry, GBP * market share
MARKET_SHARE = 0.3
ANNUAL_BUDGET = (2 * 10 ** 9) * MARKET_SHARE
NETWORKS_TO_INCLUDE = ('A',)

POPULATION_SCENARIOS = [
    "high",
    "baseline",
    "low",
    "static2017",
]
THROUGHPUT_SCENARIOS = [
    "high",
    "baseline",
    "low",
]
INTERVENTION_STRATEGIES = [
    "minimal",
    "macrocell",
    "macrocell_700",
    "small_cell",
    "small_cell_and_spectrum"
]

COVERAGE_OBLIGATION_SCENARIOS = [
    "high",
    "baseline",
    "low",
]

#    for pop_scenario, throughput_scenario, coverage_scenario, intervention_strategy  in RUN_OPTIONS:
# A. Variaciones de capacity expansion strategies
RUN_OPTION_100 = [
    ('baseline', 'baseline', 'low', 'cov_ob_1', 'minimal'),
    ('baseline', 'baseline', 'low', 'cov_ob_1', 'macrocell'),
    ('baseline', 'baseline', 'low', 'cov_ob_1', 'macrocell_700'),
    ('baseline', 'baseline', 'low', 'cov_ob_1', 'small_cell'),
    ('baseline', 'baseline', 'low', 'cov_ob_1', 'small_cell_and_spectrum'),
    ('baseline', 'baseline', 'low', 'cov_ob_1', 'macrocell_only_700')
]


# B. Variaciones de coverage obligations
# Parte 1: Se calcula y se representa. 1 estrategia, todas las obligaciones
RUN_OPTION_200 = [
    ('baseline', 'baseline', 'low', 'cov_ob_1', 'minimal'),
    ('baseline', 'baseline', 'low', 'cov_ob_2', 'minimal'),
    ('baseline', 'baseline', 'low', 'cov_ob_3', 'minimal'),
    ('baseline', 'baseline', 'low', 'cov_ob_4', 'minimal'),
    ('baseline', 'baseline', 'low', 'cov_ob_5', 'minimal')
]
RUN_OPTION_300 = [
    ('baseline', 'baseline', 'low', 'cov_ob_1', 'macrocell'),
    ('baseline', 'baseline', 'low', 'cov_ob_2', 'macrocell'),
    ('baseline', 'baseline', 'low', 'cov_ob_3', 'macrocell'),
    ('baseline', 'baseline', 'low', 'cov_ob_4', 'macrocell'),
    ('baseline', 'baseline', 'low', 'cov_ob_5', 'macrocell')
]
RUN_OPTION_400 = [
    ('baseline', 'baseline', 'low', 'cov_ob_1', 'macrocell_700'),
    ('baseline', 'baseline', 'low', 'cov_ob_2', 'macrocell_700'),
    ('baseline', 'baseline', 'low', 'cov_ob_3', 'macrocell_700'),
    ('baseline', 'baseline', 'low', 'cov_ob_4', 'macrocell_700'),
    ('baseline', 'baseline', 'low', 'cov_ob_5', 'macrocell_700')
]
RUN_OPTION_500 = [
    ('baseline', 'baseline', 'low', 'cov_ob_1', 'small_cell'),
    ('baseline', 'baseline', 'low', 'cov_ob_2', 'small_cell'),
    ('baseline', 'baseline', 'low', 'cov_ob_3', 'small_cell'),
    ('baseline', 'baseline', 'low', 'cov_ob_4', 'small_cell'),
    ('baseline', 'baseline', 'low', 'cov_ob_5', 'small_cell')
]
RUN_OPTION_600 = [
    ('baseline', 'baseline', 'low', 'cov_ob_1', 'small_cell_and_spectrum'),
    ('baseline', 'baseline', 'low', 'cov_ob_2', 'small_cell_and_spectrum'),
    ('baseline', 'baseline', 'low', 'cov_ob_3', 'small_cell_and_spectrum'),
    ('baseline', 'baseline', 'low', 'cov_ob_4', 'small_cell_and_spectrum'),
    ('baseline', 'baseline', 'low', 'cov_ob_5', 'small_cell_and_spectrum')
]

RUN_OPTION_700 = [
    ('baseline', 'baseline', 'low', 'cov_ob_1', 'macrocell_only_700'),
    ('baseline', 'baseline', 'low', 'cov_ob_2', 'macrocell_only_700'),
    ('baseline', 'baseline', 'low', 'cov_ob_3', 'macrocell_only_700'),
    ('baseline', 'baseline', 'low', 'cov_ob_4', 'macrocell_only_700'),
    ('baseline', 'baseline', 'low', 'cov_ob_5', 'macrocell_only_700')
]

# Parte B: Solo se pinta, no se recalcula Representaciones 1 obligacion, todas las estrategias
RUN_OPTION_2100 = [
    ('baseline', 'baseline', 'low', 'cov_ob_2', 'minimal'),
    ('baseline', 'baseline', 'low', 'cov_ob_2', 'macrocell'),
    ('baseline', 'baseline', 'low', 'cov_ob_2', 'macrocell_700'),
    ('baseline', 'baseline', 'low', 'cov_ob_2', 'small_cell'),
    ('baseline', 'baseline', 'low', 'cov_ob_2', 'small_cell_and_spectrum'),
    ('baseline', 'baseline', 'low', 'cov_ob_2', 'macrocell_only_700')
]
RUN_OPTION_3100 = [
    ('baseline', 'baseline', 'low', 'cov_ob_3', 'minimal'),
    ('baseline', 'baseline', 'low', 'cov_ob_3', 'macrocell'),
    ('baseline', 'baseline', 'low', 'cov_ob_3', 'macrocell_700'),
    ('baseline', 'baseline', 'low', 'cov_ob_3', 'small_cell'),
    ('baseline', 'baseline', 'low', 'cov_ob_3', 'small_cell_and_spectrum'),
    ('baseline', 'baseline', 'low', 'cov_ob_3', 'macrocell_only_700')
]
RUN_OPTION_4100 = [
    ('baseline', 'baseline', 'low', 'cov_ob_4', 'minimal'),
    ('baseline', 'baseline', 'low', 'cov_ob_4', 'macrocell'),
    ('baseline', 'baseline', 'low', 'cov_ob_4', 'macrocell_700'),
    ('baseline', 'baseline', 'low', 'cov_ob_4', 'small_cell'),
    ('baseline', 'baseline', 'low', 'cov_ob_4', 'small_cell_and_spectrum'),
    ('baseline', 'baseline', 'low', 'cov_ob_4', 'macrocell_only_700')
]
RUN_OPTION_5100 = [
    ('baseline', 'baseline', 'low', 'cov_ob_5', 'minimal'),
    ('baseline', 'baseline', 'low', 'cov_ob_5', 'macrocell'),
    ('baseline', 'baseline', 'low', 'cov_ob_5', 'macrocell_700'),
    ('baseline', 'baseline', 'low', 'cov_ob_5', 'small_cell'),
    ('baseline', 'baseline', 'low', 'cov_ob_5', 'small_cell_and_spectrum'),
    ('baseline', 'baseline', 'low', 'cov_ob_5', 'macrocell_only_700')
]

# # C. Variaciones de escenarios de población y demanda
# RUN_OPTION_101 = [
#     ('low', 'low', 'low', 'cov_ob_1', 'minimal'),
#     ('low', 'low', 'low', 'cov_ob_1', 'macrocell'),
#     ('low', 'low', 'low', 'cov_ob_1', 'macrocell_700'),
#     ('low', 'low', 'low', 'cov_ob_1', 'small_cell'),
#     ('low', 'low', 'low', 'cov_ob_1', 'small_cell_and_spectrum'),
#     ('low', 'low', 'low', 'cov_ob_1', 'macrocell_only_700')
# ]
# RUN_OPTION_102 = [
#     ('low', 'baseline', 'low', 'cov_ob_1', 'minimal'),
#     ('low', 'baseline', 'low', 'cov_ob_1', 'macrocell'),
#     ('low', 'baseline', 'low', 'cov_ob_1', 'macrocell_700'),
#     ('low', 'baseline', 'low', 'cov_ob_1', 'small_cell'),
#     ('low', 'baseline', 'low', 'cov_ob_1', 'small_cell_and_spectrum'),
#     ('low', 'baseline', 'low', 'cov_ob_1', 'macrocell_only_700')
# ]
# RUN_OPTION_103 = [
#     ('low', 'high', 'low', 'cov_ob_1', 'minimal'),
#     ('low', 'high', 'low', 'cov_ob_1', 'macrocell'),
#     ('low', 'high', 'low', 'cov_ob_1', 'macrocell_700'),
#     ('low', 'high', 'low', 'cov_ob_1', 'small_cell'),
#     ('low', 'high', 'low', 'cov_ob_1', 'small_cell_and_spectrum'),
#     ('low', 'high', 'low', 'cov_ob_1', 'macrocell_only_700')
# ]
# RUN_OPTION_104 = [
#     ('baseline', 'low', 'low', 'cov_ob_1', 'minimal'),
#     ('baseline', 'low', 'low', 'cov_ob_1', 'macrocell'),
#     ('baseline', 'low', 'low', 'cov_ob_1', 'macrocell_700'),
#     ('baseline', 'low', 'low', 'cov_ob_1', 'small_cell'),
#     ('baseline', 'low', 'low', 'cov_ob_1', 'small_cell_and_spectrum'),
#     ('baseline', 'low', 'low', 'cov_ob_1', 'macrocell_only_700')
# ]
# RUN_OPTION_105 = [
#     ('baseline', 'high', 'low', 'cov_ob_1', 'minimal'),
#     ('baseline', 'high', 'low', 'cov_ob_1', 'macrocell'),
#     ('baseline', 'high', 'low', 'cov_ob_1', 'macrocell_700'),
#     ('baseline', 'high', 'low', 'cov_ob_1', 'small_cell'),
#     ('baseline', 'high', 'low', 'cov_ob_1', 'small_cell_and_spectrum'),
#     ('baseline', 'high', 'low', 'cov_ob_1', 'macrocell_only_700')
# ]
# RUN_OPTION_106 = [
#     ('high', 'low', 'low', 'cov_ob_1', 'minimal'),
#     ('high', 'low', 'low', 'cov_ob_1', 'macrocell'),
#     ('high', 'low', 'low', 'cov_ob_1', 'macrocell_700'),
#     ('high', 'low', 'low', 'cov_ob_1', 'small_cell'),
#     ('high', 'low', 'low', 'cov_ob_1', 'small_cell_and_spectrum'),
#     ('high', 'low', 'low', 'cov_ob_1', 'macrocell_only_700')
# ]
# RUN_OPTION_107 = [
#     ('high', 'baseline', 'low', 'cov_ob_1', 'minimal'),
#     ('high', 'baseline', 'low', 'cov_ob_1', 'macrocell'),
#     ('high', 'baseline', 'low', 'cov_ob_1', 'macrocell_700'),
#     ('high', 'baseline', 'low', 'cov_ob_1', 'small_cell'),
#     ('high', 'baseline', 'low', 'cov_ob_1', 'small_cell_and_spectrum'),
#     ('high', 'baseline', 'low', 'cov_ob_1', 'macrocell_only_700')
# ]
# RUN_OPTION_108 = [
#     ('high', 'high', 'low', 'cov_ob_1', 'minimal'),
#     ('high', 'high', 'low', 'cov_ob_1', 'macrocell'),
#     ('high', 'high', 'low', 'cov_ob_1', 'macrocell_700'),
#     ('high', 'high', 'low', 'cov_ob_1', 'small_cell'),
#     ('high', 'high', 'low', 'cov_ob_1', 'small_cell_and_spectrum'),
#     ('high', 'high', 'low', 'cov_ob_1', 'macrocell_only_700')
# ]


# # 0. CUSTOM RUN
# CUSTOM_RUN = [
#     ('baseline', 'baseline', 'low', 'cov_ob_1', 'macrocell_only_700'),
# ]
# RUN_OPTIONS = CUSTOM_RUN
# results.summary_graphs_combinations['000_custom_run'] = CUSTOM_RUN
# RUN_OPTIONS = RUN_OPTION_600
# results.summary_graphs_combinations['000_custom_run'] = RUN_OPTION_100

# # A. Variaciones de capacity expansion strategies
# RUN_OPTIONS = RUN_OPTION_100
# results.summary_graphs_combinations['100_capexpansion'] = RUN_OPTION_100
#
# B. Variaciones de coverage obligations
RUN_OPTIONS = RUN_OPTION_200 + RUN_OPTION_300 + RUN_OPTION_400 + RUN_OPTION_500 + RUN_OPTION_600 + RUN_OPTION_700

# # Gráficas auxiliares para sacar los precios vs población en casos concretos
# results.summary_graphs_combinations['0002_A_'] = [('baseline', 'baseline', 'low', 'cov_ob_2', 'small_cell_and_spectrum')]
# results.summary_graphs_combinations['0002_B_'] = [('baseline', 'baseline', 'low', 'cov_ob_2', 'macrocell_700')]
# results.summary_graphs_combinations['0003_A_'] = [('baseline', 'baseline', 'low', 'cov_ob_3', 'small_cell_and_spectrum')]
# results.summary_graphs_combinations['0003_B_'] = [('baseline', 'baseline', 'low', 'cov_ob_3', 'macrocell_700')]
# results.summary_graphs_combinations['0004_A_'] = [('baseline', 'baseline', 'low', 'cov_ob_4', 'small_cell_and_spectrum')]
# results.summary_graphs_combinations['0004_B_'] = [('baseline', 'baseline', 'low', 'cov_ob_4', 'macrocell_700')]
# results.summary_graphs_combinations['0005_A_'] = [('baseline', 'baseline', 'low', 'cov_ob_5', 'small_cell_and_spectrum')]
# results.summary_graphs_combinations['0005_B_'] = [('baseline', 'baseline', 'low', 'cov_ob_5', 'macrocell_700')]

# Cada grafica tiene: 1 capacity expansion y todas las obligaciones cobertura
results.summary_graphs_combinations['100_capexpansion'] = RUN_OPTION_100
results.summary_graphs_combinations['200_covobligations_minimal'] = RUN_OPTION_200
results.summary_graphs_combinations['300_covobligations_macrocell'] = RUN_OPTION_300
results.summary_graphs_combinations['400_covobligations_macrocell_700'] = RUN_OPTION_400
results.summary_graphs_combinations['500_covobligations_smallcell'] = RUN_OPTION_500
results.summary_graphs_combinations['600_covobligations_smallcell_and_spec'] = RUN_OPTION_600
results.summary_graphs_combinations['700_covobligations_macrocell_only_700'] = RUN_OPTION_700

results.summary_graphs_combinations['000_all'] = RUN_OPTIONS

# Cada gráfica tiene: 1 obligacion de cobertura y todas las capacity expansion
results.summary_graphs_combinations['1100_covobligations_1'] = RUN_OPTION_100
results.summary_graphs_combinations['2100_covobligations_2'] = RUN_OPTION_2100
results.summary_graphs_combinations['3100_covobligations_3'] = RUN_OPTION_3100
results.summary_graphs_combinations['4100_covobligations_4'] = RUN_OPTION_4100
results.summary_graphs_combinations['5100_covobligations_5'] = RUN_OPTION_5100









# # C. Variaciones de escenarios de población y demanda
# RUN_OPTIONS = RUN_OPTION_100 + RUN_OPTION_101 + RUN_OPTION_102 + RUN_OPTION_103 + RUN_OPTION_104 + RUN_OPTION_105 + RUN_OPTION_106 + RUN_OPTION_107 + RUN_OPTION_108
# results.summary_graphs_combinations['000_all'] = RUN_OPTIONS
# results.summary_graphs_combinations['100_scenario_base_base'] = RUN_OPTION_100
# results.summary_graphs_combinations['101_scenario_low_low'] = RUN_OPTION_101
# results.summary_graphs_combinations['102_scenario_low_base'] = RUN_OPTION_102
# results.summary_graphs_combinations['103_scenario_low_high'] = RUN_OPTION_103
# results.summary_graphs_combinations['104_scenario_base_low'] = RUN_OPTION_104
# results.summary_graphs_combinations['105_scenario_base_high'] = RUN_OPTION_105
# results.summary_graphs_combinations['106_scenario_high_low'] = RUN_OPTION_106
# results.summary_graphs_combinations['107_scenario_high_base'] = RUN_OPTION_107
# results.summary_graphs_combinations['108_scenario_high_high'] = RUN_OPTION_108

COVERAGE_OBLIGATIONS = {
    'cov_ob_1': { # ORIGINAL
        'name': 'More profitable first',
        'description': 'This is the original strategy of the code',
        'population_limit_boolean': False,
        'population_limit': None,
        'deploiement_prioritaire': 0,
        'budget_limit': False,
        'descending_order': True,
        'invest_by_demand': True,
        'percentage_covered': 1,
        'coverage_obligation': {
                'low': 2,
                'baseline': 5,
                'high': 8
        },
    },
    'cov_ob_2': { # FRANCE
        'name': 'Priority areas first',
        'description': 'French coverage obligation',
        'population_limit_boolean': False,
        'population_limit': None,
        'deploiement_prioritaire': 0.18,
        'budget_limit': False,
        'descending_order': True,
        'invest_by_demand': True,
        'percentage_covered': 1, # This does not do anything
        'coverage_obligation': {
                'low': 2,
                'baseline': 5,
                'high': 8
        },
    },
    'cov_ob_3': { # GERMANY
        'name': 'Less profitable first',
        'description': 'German coverage obligation',
        'population_limit_boolean': False,
        'population_limit': None,
        'deploiement_prioritaire': 0,
        'budget_limit': False,
        'descending_order': False,
        'invest_by_demand': True,
        'percentage_covered': 0.90,
        'coverage_obligation': {
                'low': 2,
                'baseline': 5,
                'high': 8
        },
    },
    'cov_ob_4': { # SPAIN
        'name': 'Only rural areas',
        'description': 'Spanish coverage obligation',
        'population_limit_boolean': True,
        'population_limit': 800,
        'deploiement_prioritaire': 0,
        'budget_limit': False,
        'descending_order': True,
        'invest_by_demand': True, #
        'percentage_covered': 0.90,
        'coverage_obligation': {
                'low': 2,
                'baseline': 5,
                'high': 8
        },
    },
    'cov_ob_5': { # The UK
        'name': 'Nation-balanced',
        'description': 'UK coverage obligation',
        'population_limit_boolean': False,
        'population_limit': None,
        'deploiement_prioritaire': 0,
        'budget_limit': False,
        'descending_order': True,
        'invest_by_demand': True, #
        'percentage_covered': 0.95,
        'coverage_obligation': {
                'low': 2,
                'baseline': 5,
                'high': 8
        },
    },
}

################################################################
# LOAD REGIONS
# - LADs
# - Postcode Sectors
################################################################
print('Loading regions')
print('-> LADs, OFCOM LADs, PCDs')

# lads = [
# 	{
# 		"id": 1,
# 		"name": "Cambridge"
# 	},
# ]
lads = []
LAD_FILENAME = os.path.join(INPUT_FOLDER, 'initial_system', 'lads.csv')

with open(LAD_FILENAME, 'r') as lad_file:
    reader = csv.reader(lad_file)
    next(reader)  # skip header
    for lad_id, name in reader:
        lads.append({
            "id": lad_id,
            "name": name
        })


ofcom_lads = []
ofcom_380_to_174 = {}
LAD_OFCOM_FILENAME = os.path.join(INPUT_FOLDER, 'ofcom_geography_conversion.csv')

with open(LAD_OFCOM_FILENAME, 'r') as lad_file:
    reader = csv.reader(lad_file)
    next(reader)  # skip header
    for name, oslaua, oscty, gor, code in reader:
        ofcom_lads.append({
            "lad_id": code,
            "name": name
        })
        ofcom_380_to_174[oslaua] = code


#print (repr(ofcom_lads))
# Read in postcode sectors (without population)
# pcd_sectors = [
# 	{
# 		"id": "CB1G",
# 		"lad_id": 1,
# 		"population": 50000,  # to be loaded from scenario data
# 		"area": 2,
# 	},
# ]
pcd_sectors = []
PCD_SECTOR_FILENAME = os.path.join(INPUT_FOLDER, 'initial_system', 'pcd_sectors.csv')
with open(PCD_SECTOR_FILENAME, 'r') as pcd_sector_file:
    reader = csv.reader(pcd_sector_file)
    next(reader)  # skip header
    for lad_id, pcd_sector, _, area in reader:
        pcd_sectors.append({
            "id": pcd_sector.replace(" ", ""),
            "lad_id": lad_id,
            "area": float(area) #area_sq_km
        })

################################################################
# LOAD SCENARIO DATA
# - population by scenario: year, pcd_sector, population
# - user throughput demand by scenario: year, demand per capita (GB/month?)
################################################################
print('Loading scenario data')
print('-> Population, demand in mbps and capacity, coverage obligations')

scenario_files = {
    scenario: os.path.join(INPUT_FOLDER, 'scenario_data', 'population_{}_pcd.csv'.format(scenario))
    for scenario in POPULATION_SCENARIOS
}

# POPULATION
population_by_scenario_year_pcd = {
    scenario: {
        year: {} for year in TIMESTEPS
    }
    for scenario in POPULATION_SCENARIOS
}

for scenario, filename in scenario_files.items():
    # Open file
    with open(filename, 'r') as scenario_file:
        scenario_reader = csv.reader(scenario_file)

        # Put the values in the population dict
        for year, pcd_sector, population in scenario_reader:
            year = int(year)
            if year in TIMESTEPS:
                population_by_scenario_year_pcd[scenario][year][pcd_sector] = int(population)

# DEMAND IN GB
user_throughput_by_scenario_year_GB = {
    scenario: {} for scenario in THROUGHPUT_SCENARIOS
}
THROUGHPUT_GB_FILENAME = os.path.join(INPUT_FOLDER, 'scenario_data', 'monthly_data_growth_scenarios.csv')
with open(THROUGHPUT_GB_FILENAME, 'r') as throughput_file:
    reader = csv.reader(throughput_file)
    next(reader)  # skip header
    for year, low, base, high in reader:
        year = int(year)
        if "high" in THROUGHPUT_SCENARIOS:
            user_throughput_by_scenario_year_GB["high"][year] = float(high)
        if "baseline" in THROUGHPUT_SCENARIOS:
            user_throughput_by_scenario_year_GB["baseline"][year] = float(base)
        if "low" in THROUGHPUT_SCENARIOS:
            user_throughput_by_scenario_year_GB["low"][year] = float(low)
        if "static2017" in THROUGHPUT_SCENARIOS:
            user_throughput_by_scenario_year_GB["baseline"][year] = float(base)


# DEMAND IN MBPS
user_throughput_by_scenario_year_mbps = {
    scenario: {} for scenario in THROUGHPUT_SCENARIOS
}
THROUGHPUT_SPEED_FILENAME = os.path.join(INPUT_FOLDER, 'scenario_data', 'monthly_speed_growth_scenarios.csv')
with open(THROUGHPUT_SPEED_FILENAME, 'r') as throughput_file:
    reader = csv.reader(throughput_file)
    next(reader)  # skip header
    for year, low, base, high in reader:
        year = int(year)
        if "high" in THROUGHPUT_SCENARIOS:
            user_throughput_by_scenario_year_mbps["high"][year] = float(high)
        if "baseline" in THROUGHPUT_SCENARIOS:
            user_throughput_by_scenario_year_mbps["baseline"][year] = float(base)
        if "low" in THROUGHPUT_SCENARIOS:
            user_throughput_by_scenario_year_mbps["low"][year] = float(low)
        if "static2017" in THROUGHPUT_SCENARIOS:
            user_throughput_by_scenario_year_mbps["baseline"][year] = float(base)



# COVERAGE OBLIGATION
coverage_obligations_by_scenario_year = {
    scenario: {} for scenario in COVERAGE_OBLIGATION_SCENARIOS
}
COVERAGE_OBLIGATIONS_FILENAME = os.path.join(INPUT_FOLDER, 'scenario_data', 'per_year_coverage_obligations_scenarios.csv')
with open(COVERAGE_OBLIGATIONS_FILENAME, 'r') as coverage_obligations_file:
    reader = csv.reader(coverage_obligations_file)
    next(reader)  # skip header
    for year, low, base, high in reader:
        year = int(year)
        if "high" in COVERAGE_OBLIGATION_SCENARIOS:
            coverage_obligations_by_scenario_year["high"][year] = float(high)
        if "baseline" in COVERAGE_OBLIGATION_SCENARIOS:
            coverage_obligations_by_scenario_year["baseline"][year] = float(base)
        if "low" in COVERAGE_OBLIGATION_SCENARIOS:
            coverage_obligations_by_scenario_year["low"][year] = float(low)


################################################################
# LOAD INITIAL SYSTEM ASSETS/SITES
################################################################
print('Loading initial system')
print('-> Assets')

# Read in assets (for initial timestep)
# assets = [
# 	{
#       'pcd_sector': 'CB12',
#       'site_ngr': 'EF006234',
#       'build_date': 2015,
#       'technology': 'LTE',
#       'frequency': '800',
#       'bandwidth': '2x10MHz',
# 	}
# ]
SYSTEM_FILENAME = os.path.join(INPUT_FOLDER, 'initial_system', 'initial_system_with_4G.csv')

initial_system = []
pcd_sector_ids = {pcd_sector["id"]: True for pcd_sector in pcd_sectors}
with open(SYSTEM_FILENAME, 'r') as system_file:
    reader = csv.reader(system_file)
    next(reader)  # skip header
    for pcd_sector, site_ngr, build_date, site_type, tech, freq, bandwidth, network in reader:
        # If asset is in a known postcode, go ahead
        if pcd_sector in pcd_sector_ids and network in NETWORKS_TO_INCLUDE:
            initial_system.append({
                'pcd_sector': pcd_sector,
                'site_ngr': site_ngr,
                'type': site_type,
                'build_date': int(build_date),
                'technology': tech,
                'frequency': freq,
                'bandwidth': bandwidth,
            })


################################################################
# IMPORT LOOKUP TABLES
# - mobile capacity, by environment, frequency, bandwidth and site density
# - clutter environment geotype, by population density
################################################################
print('Loading lookup tables')
print('-> Capacity and geotypes')

CAPACITY_LOOKUP_FILENAME = os.path.join(INPUT_FOLDER, 'lookup_tables', 'lookup_table_long.csv')

# create empty dictionary for capacity lookup
capacity_lookup_table = {}

with open(CAPACITY_LOOKUP_FILENAME, 'r') as capacity_lookup_file:
    # set DictReader with file name for 4G rollout data
    reader = csv.DictReader(capacity_lookup_file)

        # populate dictionary - this gives a dict for each row, with each heading as a key
    for row in reader:
        environment = row["type"]
        frequency = row["frequency"].replace(' MHz', '')
        bandwidth = row["bandwidth"].replace(' ', '')
        density = float(row["site_density"])
        capacity = float(row["capacity"])

        if (environment, frequency, bandwidth) not in capacity_lookup_table:
            capacity_lookup_table[(environment, frequency, bandwidth)] = []

        capacity_lookup_table[(environment, frequency, bandwidth)].append((density, capacity, ))

    for key, value_list in capacity_lookup_table.items():
        # sort each environment/frequency/bandwith list by site density
        value_list.sort(key=lambda tup: tup[0])


CLUTTER_GEOTYPE_FILENAME = os.path.join(INPUT_FOLDER, 'lookup_tables', 'lookup_table_geotype.csv')

# Create empty list for clutter geotype lookup
clutter_lookup = []

with open(CLUTTER_GEOTYPE_FILENAME, 'r') as clutter_geotype_file:
    # set DictReader with file name for 4G rollout data
    reader = csv.DictReader(clutter_geotype_file)
    for row in reader:
        geotype = row['geotype']
        population_density = float(row['population_density'])
        clutter_lookup.append((population_density, geotype))

    # sort list by population density (first entry in each tuple)
    clutter_lookup.sort(key=lambda tup: tup[0])


def _print_geotypes():
    my_pcd_type_count = collections.defaultdict(list)
    for pcd in sorted(system.postcode_sectors.values(), key=lambda pcd: -pcd.population_density):
        # print('- ' + str(pcd.id) + ' => '+ pcd.clutter_environment)
        if pcd.clutter_environment in my_pcd_type_count:
            my_pcd_type_count[pcd.clutter_environment] += 1
        else:
            my_pcd_type_count[pcd.clutter_environment] = 1
    print("----------------------")
    print("Here are my geotypes!")
    print("Urban => " + str(my_pcd_type_count["Urban"]))
    print("Suburban => " + str(my_pcd_type_count["Suburban"]))
    print("Rural => " + str(my_pcd_type_count["Rural"]))
    print("----------------------")


def _fill_initial_info_in_results(results, system, chart1, chart2, chart3, chart4, chart1_lads, chart2_lads, chart3_lads, chart4_lads):
    previous_pop1, previous_pop2, previous_pop3, previous_pop4 = 0, 0, 0, 0
    previous_pop1_lad, previous_pop2_lad, previous_pop3_lad, previous_pop4_lad = 0, 0, 0, 0

    list_postcodes = []
    list_lads = []

    if results.co_coverage_obligation_type in ['cov_ob_2']:   # FRANCE
        all_postcodes_inverted = sorted(system.postcode_sectors.values(), key=lambda pcd: pcd.population_density)
        # print("THRES French 1 - Considering {} of {} postcodes".format(len(all_postcodes_inverted), len(system.postcode_sectors.values())))

        priority_postcodes, remaining_postcodes, pop_covered = [], [], 0
        target_pop = system.population * results.co_deploiement_prioritaire

        # Select postcodes of deploiment prioritaire and remove them from the list
        for pcd in all_postcodes_inverted:
            if pop_covered <= target_pop:
                pop_covered += pcd.population
                priority_postcodes.append(pcd)
            else:
                remaining_postcodes.append(pcd)

        # Change the order to start investing in the most profitable ones
        priority_postcodes = sorted(priority_postcodes, key=lambda pcd: -pcd.population_density)
        remaining_postcodes = sorted(remaining_postcodes, key=lambda pcd: -pcd.population_density)

        # print("THRES French 2 - Considering {} of {} postcodes".format(len(priority_postcodes), len(remaining_postcodes)))

        # Add all the postcodes together
        list_postcodes = priority_postcodes + remaining_postcodes
        list_lads = sorted(system.ofcom_lads.values(), key=lambda lad: -lad.population_density)

    elif results.co_coverage_obligation_type in ['cov_ob_4']: # SPAIN
        all_postcodes = sorted(system.postcode_sectors.values(), key=lambda pcd: pcd.population_density)
        priority_postcodes, main_postcodes, remaining_postcodes, pop_covered  = [], [], [], 0

        # Select postcodes according to population
        for pcd in all_postcodes:
            if pcd.population < results.co_population_limit:
                main_postcodes.append(pcd)
            else:
                remaining_postcodes.append(pcd)

        population = sum(pcd.population for pcd in all_postcodes)
        target_pop = population * results.co_percentage_covered

        for pcd in sorted(main_postcodes, key=lambda pcd: -pcd.population_density):
            if pop_covered <= target_pop:
                pop_covered += pcd.population
                priority_postcodes.append(pcd)
            else:
                remaining_postcodes.append(pcd)

        # Change the order to start investing in the most profitable ones
        priority_postcodes = sorted(priority_postcodes, key=lambda pcd: -pcd.population_density)
        remaining_postcodes = sorted(remaining_postcodes, key=lambda pcd: -pcd.population_density)

        # Add all the postcodes together
        list_postcodes = priority_postcodes + remaining_postcodes
        list_lads = sorted(system.ofcom_lads.values(), key=lambda lad: -lad.population_density)

    elif results.co_coverage_obligation_type in ['cov_ob_1', 'cov_ob_5']:
        list_postcodes = sorted(system.postcode_sectors.values(), key=lambda pcd: -pcd.population_density)
        list_lads = sorted(system.ofcom_lads.values(), key=lambda lad: -lad.population_density)

    elif results.co_coverage_obligation_type in ['cov_ob_3']:    # GERMANY
        list_postcodes = sorted(system.postcode_sectors.values(), key=lambda pcd: pcd.population_density)
        list_lads = sorted(system.ofcom_lads.values(), key=lambda lad: lad.population_density)

    for pcd in list_postcodes:
        previous_pop1 = chart1.add_initial_info(pcd.id, pcd.lad_id, pcd.population, pcd.population_density, TIMESTEPS, previous_pop1)
        previous_pop2 = chart2.add_initial_info(pcd.id, pcd.lad_id, pcd.population, pcd.population_density, previous_pop2)
        previous_pop3 = chart3.add_initial_info(pcd.id, pcd.lad_id, pcd.population, pcd.population_density, TIMESTEPS, previous_pop3)
        previous_pop4 = chart4.add_initial_info(pcd.id, pcd.lad_id, pcd.population, pcd.population_density, TIMESTEPS, previous_pop4)

    for lad in list_lads:
        previous_pop1_lad = chart1_lads.add_initial_info(lad.id, lad.name, lad.population, lad.population_density, TIMESTEPS, previous_pop1_lad)
        previous_pop2_lad = chart2_lads.add_initial_info(lad.id, lad.name, lad.population, lad.population_density, previous_pop2_lad)
        previous_pop3_lad = chart3_lads.add_initial_info(lad.id, lad.name, lad.population, lad.population_density, TIMESTEPS, previous_pop3_lad)
        previous_pop4_lad = chart4_lads.add_initial_info(lad.id, lad.name, lad.population, lad.population_density, TIMESTEPS, previous_pop4_lad)


################################################################
# START RUNNING MODEL
# - run from BASE_YEAR to END_YEAR in TIMESTEP_INCREMENT steps
# - run over population scenario / demand scenario / intervention strategy combinations
# - output demand, capacity, opex, energy demand, built interventions, build costs per year
################################################################
SIMULATION_START_TIME = time.time()
for pop_scenario, throughput_scenario, coverage_speed_scenario, coverage_obligation_type, intervention_strategy in RUN_OPTIONS:
    print('----------------------------------')
    print("Running:", coverage_obligation_type, pop_scenario, throughput_scenario, coverage_speed_scenario, intervention_strategy)
    results.current_run_option = [(pop_scenario, throughput_scenario, coverage_speed_scenario, coverage_obligation_type, intervention_strategy)]

    assets = initial_system[:]
    index = save_data._get_suffix(coverage_obligation_type, pop_scenario, throughput_scenario, coverage_speed_scenario, intervention_strategy)

    results.chart1_add_table(index)
    results.chart2_add_table(index)
    results.chart3_add_table(index)
    results.chart4_add_table(index)
    results.chart5_add_table(index)

    results.chart1_lads_add_table(index)
    results.chart2_lads_add_table(index)
    results.chart3_lads_add_table(index)
    results.chart4_lads_add_table(index)
    results.chart5_lads_add_table(index)

    chart1 = results.chart_1[index]
    chart2 = results.chart_2[index]
    chart3 = results.chart_3[index]
    chart4 = results.chart_4[index]
    chart5 = results.chart_5[index]

    chart1_lads = results.chart_1_lads[index]
    chart2_lads = results.chart_2_lads[index]
    chart3_lads = results.chart_3_lads[index]
    chart4_lads = results.chart_4_lads[index]
    chart5_lads = results.chart_5_lads[index]

    # Add information about coverage obligations
    results.co_coverage_obligation_type = coverage_obligation_type
    results.co_name[coverage_obligation_type] = COVERAGE_OBLIGATIONS[coverage_obligation_type]['name']
    results.co_population_limit_boolean = COVERAGE_OBLIGATIONS[coverage_obligation_type]['population_limit_boolean']
    results.co_population_limit = COVERAGE_OBLIGATIONS[coverage_obligation_type]['population_limit']
    results.co_deploiement_prioritaire = COVERAGE_OBLIGATIONS[coverage_obligation_type]['deploiement_prioritaire']
    results.co_budget_limit = COVERAGE_OBLIGATIONS[coverage_obligation_type]['budget_limit']
    results.co_descending_order = COVERAGE_OBLIGATIONS[coverage_obligation_type]['descending_order']
    results.co_percentage_covered = COVERAGE_OBLIGATIONS[coverage_obligation_type]['percentage_covered']
    results.co_invest_by_demand = COVERAGE_OBLIGATIONS[coverage_obligation_type]['invest_by_demand']
    results.co_coverage_obligation = COVERAGE_OBLIGATIONS[coverage_obligation_type]['coverage_obligation']

    results.co_percentage_covered_all[coverage_obligation_type] = results.co_percentage_covered

    for year in TIMESTEPS:
        print("-", year)
#        input ("Press enter")
        # Update population and demand from scenario values
        for pcd_sector in pcd_sectors:
            pcd_sector_id = pcd_sector["id"]
            pcd_sector["population"] = population_by_scenario_year_pcd[pop_scenario][year][pcd_sector_id]
            pcd_sector["user_throughput_GB"] = user_throughput_by_scenario_year_GB[throughput_scenario][year]
            pcd_sector["user_throughput_mbps"] = user_throughput_by_scenario_year_mbps['low'][year] # Fixed to 2 Mbps

        # Decide on new interventions
        budget = ANNUAL_BUDGET
        service_obligation_capacity = COVERAGE_OBLIGATIONS[coverage_obligation_type]['coverage_obligation'][coverage_speed_scenario]

        # simulate first
        if year == BASE_YEAR:
            system = ICTManager(lads, ofcom_lads, ofcom_380_to_174, pcd_sectors, assets, capacity_lookup_table, clutter_lookup, service_obligation_capacity)
            _fill_initial_info_in_results(results, system, chart1, chart2, chart3, chart4, chart1_lads, chart2_lads, chart3_lads, chart4_lads)
            results.population_2020 = system.population
            # _print_geotypes()


        # decide
        interventions_built, budget, spend, results = decide_interventions(intervention_strategy, budget, service_obligation_capacity, system, year, results, index)

        # accumulate decisions
        assets += interventions_built

        # simulate with decisions
        system = ICTManager(lads, ofcom_lads, ofcom_380_to_174, pcd_sectors, assets, capacity_lookup_table, clutter_lookup, service_obligation_capacity)

        # Fill capacity margins per year
        for pcd in sorted(system.postcode_sectors.values(), key=lambda pcd: -pcd.population_density):
            chart2.add_cap_margin(pcd.id, year, pcd.capacity_margin)
            chart4.add_cap_and_demand(pcd.id, year, pcd.capacity, pcd.demand, pcd.threshold_demand)
            chart1.add_population_covered(pcd.id, year, pcd.capacity, pcd.demand, pcd.population, pcd.threshold_demand)

        # Fill capacity margins per year
        for lad in sorted(system.ofcom_lads.values(), key=lambda lad: -lad.population_density):
            chart2_lads.add_cap_margin(lad.id, year, lad.capacity_margin)
            chart4_lads.add_cap_and_demand(lad.id, year, lad.capacity, lad.demand, lad.coverage)

        chart5.add_initial_info(results, system, index, year)

    chart5.calculate_aggregated_elements(results, TIMESTEPS)
    chart5.get_all_values()

    print("Running:", coverage_obligation_type, pop_scenario, throughput_scenario, coverage_speed_scenario, intervention_strategy)

    save_data.write_chart_1(system, coverage_obligation_type, pop_scenario, throughput_scenario, coverage_speed_scenario, intervention_strategy, results, index, TIMESTEPS, OUTPUT_FOLDER)
    save_data.write_chart_2(system, coverage_obligation_type, pop_scenario, throughput_scenario, coverage_speed_scenario, intervention_strategy, results, index, TIMESTEPS, OUTPUT_FOLDER)
    save_data.write_chart_3(system, coverage_obligation_type, pop_scenario, throughput_scenario, coverage_speed_scenario, intervention_strategy, results, index, TIMESTEPS, OUTPUT_FOLDER)
    save_data.write_chart_4(system, coverage_obligation_type, pop_scenario, throughput_scenario, coverage_speed_scenario, intervention_strategy, results, index, TIMESTEPS, OUTPUT_FOLDER)
    save_data.write_chart_5(system, coverage_obligation_type, pop_scenario, throughput_scenario, coverage_speed_scenario, intervention_strategy, results, index, TIMESTEPS, OUTPUT_FOLDER)

    save_data.write_chart_1_lads(system, coverage_obligation_type, pop_scenario, throughput_scenario, coverage_speed_scenario, intervention_strategy, results, index, TIMESTEPS, OUTPUT_FOLDER)
    save_data.write_chart_2_lads(system, coverage_obligation_type, pop_scenario, throughput_scenario, coverage_speed_scenario, intervention_strategy, results, index, TIMESTEPS, OUTPUT_FOLDER)
    save_data.write_chart_3_lads(system, coverage_obligation_type, pop_scenario, throughput_scenario, coverage_speed_scenario, intervention_strategy, results, index, TIMESTEPS, OUTPUT_FOLDER)
    save_data.write_chart_4_lads(system, coverage_obligation_type, pop_scenario, throughput_scenario, coverage_speed_scenario, intervention_strategy, results, index, TIMESTEPS, OUTPUT_FOLDER)

save_data.write_general_charts(system, results, RUN_OPTIONS, TIMESTEPS, OUTPUT_FOLDER)
SIMULATION_END_TIME = time.time()
elapsed_time_secs = SIMULATION_END_TIME - SIMULATION_START_TIME
print("Execution finished")
print("Execution took: %s HH:MM:SS" % timedelta(seconds=round(elapsed_time_secs)))

