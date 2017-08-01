"""Model runner to use in place of smif for standalone modelruns
- run over multiple years
- make rule-based intervention decisions at each timestep
"""
# pylint disable=C0103
import csv
import itertools
import os
import pprint

from digital_comms.ccam import ICTManager

import digital_comms.interventions

################################################################
# SETUP MODEL RUN CONFIGURATION
# - timesteps, scenarios, strategies
# - data files base path
################################################################

# BASE_PATH = r"C:\Users\EJO31\Dropbox\Digital Comms - Cambridge data"
# BASE_PATH = r"C:\Users\mert2014\Dropbox\Digital Comms - Cambridge data"
BASE_PATH = "/home/tom/Dropbox/Digital Comms - Cambridge data"

BASE_YEAR = 2017
END_YEAR = 2020
TIMESTEP_INCREMENT = 1

POPULATION_SCENARIOS = [
    "high",
    "base",
    "low",
]
THROUGHPUT_SCENARIOS = [
    "high",
    "base",
    "low",
]
INTERVENTION_STRATEGIES = [
    "minimal",
    # "macrocell_no_so",
    # "macrocell_with_so",
    # "small_cell_no_so",
    # "small_cell_with_so",
]


################################################################
# LOAD REGIONS
# - LADs
# - Postcode Sectors
################################################################

# lads = [
# 	{
# 		"id": 1,
# 		"name": "Cambridge"
# 	},
# ]
lads = []
LAD_FILENAME = os.path.join(BASE_PATH, "lads.csv")

with open(LAD_FILENAME, 'r') as lad_file:
    reader = csv.DictReader(lad_file)
    for line in reader:
        lads.append({
            "id": line["id"],
            "name": line["name"],

        })

# Read in postcode sectors (without population)
# pcd_sectors = [
# 	{
# 		"id": "CB1G",
# 		"lad_id": 1,
# 		"population": 50000,
# 		"area": 2,
# 	},
# ]
pcd_sectors = []
PCD_SECTOR_FILENAME = os.path.join(BASE_PATH, "pcd_sectors.csv")
with open(PCD_SECTOR_FILENAME, 'r') as pcd_sector_file:
    reader = csv.DictReader(pcd_sector_file)
    for line in reader:
        pcd_sectors.append({
            "id": line["pcd_sector"].replace(" ", ""),
            "lad_id": line["oslaua"],
            "area": float(line["area_sq_km"])
        })



################################################################
# LOAD SCENARIO DATA
# - population by scenario: year, pcd_sector, population
# - user throughput demand by scenario: year, demand per capita (GB/month?)
################################################################
scenario_files = {
    "high": os.path.join(BASE_PATH, 'scenario_data', 'population_high_cambridge_pcd.csv'),
    "base": os.path.join(BASE_PATH, 'scenario_data', 'population_base_cambridge_pcd.csv'),
    "low": os.path.join(BASE_PATH, 'scenario_data', 'population_low_cambridge_pcd.csv')
}
population_by_scenario_year_pcd = {}

for scenario, filename in scenario_files.items():
    # Open file
    with open(filename, 'r') as scenario_file:
        scenario_reader = csv.reader(scenario_file)
        population_by_scenario_year_pcd[scenario] = {}

        # Put the values in the population dict
        for year, pcd_sector, population in scenario_reader:
            year = int(year)
            if year not in population_by_scenario_year_pcd[scenario]:
                population_by_scenario_year_pcd[scenario][year] = {}

            population_by_scenario_year_pcd[scenario][year][pcd_sector] = int(population)

user_throughput_by_scenario_year = {
    "high": {},
    "base": {},
    "low": {}
}

THROUGHPUT_FILENAME = os.path.join(BASE_PATH, 'scenario_data', 'data_growth_scenarios.csv')
with open(THROUGHPUT_FILENAME, 'r') as throughput_file:
    reader = csv.reader(throughput_file)
    next(reader)  # skip header
    for year, low, base, high in reader:
        year = int(year)
        user_throughput_by_scenario_year["high"][year] = float(high)
        user_throughput_by_scenario_year["base"][year] = float(base)
        user_throughput_by_scenario_year["low"][year] = float(low)



################################################################
# LOAD INITIAL SYSTEM ASSETS/SITES
################################################################
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
SYSTEM_FILENAME = os.path.join(BASE_PATH, 'initial_system_with_4G.csv')

initial_system = []
pcd_sector_ids = [pcd_sector["id"] for pcd_sector in pcd_sectors]
with open(SYSTEM_FILENAME, 'r') as system_file:
    reader = csv.DictReader(system_file)
    for line in reader:
        # If asset is in a known postcode, go ahead
        if line['pcd_sector'] in pcd_sector_ids:
            initial_system.append({
                'pcd_sector': line['pcd_sector'],
                'site_ngr': line['site_ngr'],
                'build_date': int(line['build_date']),
                'technology': line['technology'],
                'frequency': line['frequency'],
                'bandwidth': line['bandwidth'],
            })


################################################################
# IMPORT LOOKUP TABLES
# - mobile capacity, by environment, frequency, bandwidth and site density
# - clutter environment geotype, by population density
################################################################

CAPACITY_LOOKUP_FILENAME = os.path.join(BASE_PATH, 'lookup_tables', 'lookup_table_long.csv')

# create empty dictionary for capacity lookup
capacity_lookup_table = {}

with open(CAPACITY_LOOKUP_FILENAME, 'r') as capacity_lookup_file:
    # set DictReader with file name for 4G rollout data
    reader = csv.DictReader(capacity_lookup_file)

    lookup_keys = ["Environment", "Frequency", "Bandwidth"]

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


CLUTTER_GEOTYPE_FILENAME = os.path.join(BASE_PATH, 'lookup_tables', 'lookup_table_geotype.csv')

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

def write_results(ict_manager, year, pop_scenario, throughput_scenario, intervention_strategy):
    suffix = 'pop_{}_throughput_{}_strategy_{}'.format(
        pop_scenario, throughput_scenario, intervention_strategy)
    metrics_filename = os.path.join(BASE_PATH, 'outputs', 'metrics_{}.csv'.format(suffix))

    if year == BASE_YEAR:
        metrics_file = open(metrics_filename, 'w')
        metrics_writer = csv.writer(metrics_file)
        metrics_writer.writerow(
            ('year', 'area_id', 'area_name', 'cost', 'coverage', 'demand', 'capacity', 'energy_demand'))
    else:
        metrics_file = open(metrics_filename, 'a')
        metrics_writer = csv.writer(metrics_file)

    # output and report results for this timestep
    results = ict_manager.results()

    for lad in ict_manager.lads.values():
        area_id = lad.id
        area_name = lad.name

        # Output metrics
        # year,area,cost,coverage,demand,capacity,energy_demand
        cost = results["cost"][area_name]
        coverage = results["coverage"][area_name]
        demand = results["demand"][area_name]
        capacity = results["capacity"][area_name]
        energy_demand = results["energy_demand"][area_name]

        metrics_writer.writerow(
            (year, area_id, area_name, cost, coverage, demand, capacity, energy_demand))

    metrics_file.close()


################################################################
# START RUNNING MODEL
# - run from BASE_YEAR to END_YEAR in TIMESTEP_INCREMENT steps
# - run over population scenario / demand scenario / intervention strategy combinations
# - output demand, capacity, opex, energy demand, built interventions, build costs per year
################################################################

timesteps = range(BASE_YEAR, END_YEAR + 1, TIMESTEP_INCREMENT)

for pop_scenario, throughput_scenario, intervention_strategy in itertools.product(
        POPULATION_SCENARIOS,
        THROUGHPUT_SCENARIOS,
        INTERVENTION_STRATEGIES):

    assets = initial_system
    for year in timesteps:

        # Update population from scenario values
        for pcd_sector in pcd_sectors:
            pcd_sector_id = pcd_sector["id"]
            pcd_sector["population"] = population_by_scenario_year_pcd[pop_scenario][year][pcd_sector_id]
            pcd_sector["user_throughput"] = user_throughput_by_scenario_year[throughput_scenario][year]

        # Decommission assets
        asset_lifetime = 10
        assets = [asset for asset in assets if asset["build_date"] > year - asset_lifetime]
        decommissioned = [asset for asset in assets if asset["build_date"] <= year - asset_lifetime]

        # Run without intervention in the system
        manager_before = ICTManager(lads, pcd_sectors, assets, capacity_lookup_table, clutter_lookup)

        # Decide on new interventions


        # run model for timestep
        manager_after = ICTManager(lads, pcd_sectors, assets, capacity_lookup_table, clutter_lookup)
        write_results(manager_after, year, pop_scenario, throughput_scenario, intervention_strategy)
