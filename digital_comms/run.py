"""Model runner to use in place of smif for standalone modelruns
- run over multiple years
- make rule-based intervention decisions at each timestep
"""
import csv
import os
import pprint
from digital_comms.ccam import ICTManager

BASE_YEAR = 2017
END_YEAR = 2020
TIMESTEP_INCREMENT = 1

# BASE_PATH = r"C:\Users\EJO31\Dropbox\Digital Comms - Cambridge data"
# BASE_PATH = r"C:\Users\mert2014\Dropbox\Digital Comms - Cambridge data"
BASE_PATH = "/home/tom/Dropbox/Digital Comms - Cambridge data"


################################################################
# LOAD REGIONS
# - LADs
# - Postcode Sectors
################################################################

# lads = [
# 	{
# 		"id": 1,
# 		"name": "Cambridge",
# 		"area": 10,
# 		"user_demand": 1,
# 		"spectrum_available": {
# 			"GSM 900": True,
# 			"GSM 1800": True,
# 			"UMTS 900": True,
# 			"UMTS 2100": True,
# 			"LTE 800": True,
# 			"LTE 1800": True,
# 			"LTE 2600": True,
# 			"5G 700": False,
# 			"5G 3400": False,
# 			"5G 3600": False,
# 			"5G 26000": False,
# 		}
# 	},
# ]
lads = []
lad_filename = os.path.join(BASE_PATH, "lads.csv")

with open(lad_filename, 'r') as lad_file:
    reader = csv.DictReader(lad_file)
    for line in reader:
        lads.append({
            "id": line["id"],
            "name": line["name"],
            "user_demand": 1,
            "spectrum_available": {
                "GSM 900": True,
                "GSM 1800": True,
                "UMTS 900": True,
                "UMTS 2100": True,
                "LTE 800": True,
                "LTE 1800": True,
                "LTE 2600": True,
                "5G 700": False,
                "5G 3400": False,
                "5G 3600": False,
                "5G 26000": False,
            }
        })

# Read in postcode sectors (without population)
# pcd_sectors = [
# 	{
# 		"id": 1,
# 		"lad_id": 1,
# 		"name": "CB1G",
# 		"population": 50000,
# 		"area": 2,
# 	},
# ]
pcd_sectors = []
pcd_sector_filename = os.path.join(BASE_PATH, "pcd_sectors.csv")
with open(pcd_sector_filename, 'r') as pcd_sector_file:
    reader = csv.DictReader(pcd_sector_file)
    for line in reader:
        pcd_sectors.append({
            "id": line["pcd_sector"],
            "lad_id": line["oslaua"],
            "name": line["pcd_sector"].replace(" ", ""),
            "area": float(line["area_sq_km"])
        })



################################################################
# LOAD SCENARIO DATA
# - population by scenario: year, pcd_sector, population
# - user throughput demand by scenario: year, demand per capita (GB/month?)
################################################################
scenario_files = {
    "high": os.path.join(BASE_PATH, "population_high_cambridge_pcd.csv"),
    "base": os.path.join(BASE_PATH, "population_base_cambridge_pcd.csv"),
    "low": os.path.join(BASE_PATH, "population_low_cambridge_pcd.csv")
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



################################################################
# LOAD INITIAL SYSTEM ASSETS/SITES
# -
################################################################
# Read in assets (for initial timestep)
# assets = [
# 	{
# 		"type": "site",
# 		"pcd_sector_id": 1,
# 		"cells": 3,
# 		"technology": "UMTS",
# 		"year": 2017
# 	}
# ]
sites_by_postcode = {}
pcd_sector_ids = [pcd_sector["id"] for pcd_sector in pcd_sectors]

assets_filename = os.path.join(base_path, "sitefinder_asset_data.csv")
with open(assets_filename, 'r') as assets_file:
    reader = csv.DictReader(assets_file)
    for line in reader:
        postcode = line["pcd.sector"].replace(" ", "")
        technology = line["Transtype"]
        site_ngr = line["Sitengr"]
        # ignore assets from non-matching postcodes
        if postcode not in pcd_sector_ids:
            continue

        # otherwise add site
        if postcode not in sites_by_postcode:
            sites_by_postcode[postcode] = {
                "pcd_sector_id": postcode,
                "technology": {}
            }

        if technology not in sites_by_postcode[postcode]["technology"]:
            sites_by_postcode[postcode]["technology"][technology] = set()

        sites_by_postcode[postcode]["technology"][technology].add(site_ngr)

assets = []
for asset_mix in sites_by_postcode.values():
    pcd_sector_id = asset_mix["pcd_sector_id"]
    for tech, sites in asset_mix["technology"].items():
        num_sites = len(sites)
        asset = {
            "type": "site",
            "pcd_sector_id": pcd_sector_id,
            "technology": tech,
            "cells": num_sites * 3,  # Assuming three cells per sitengr #####################
            "year": 2010  # Assuming at least as old as sitefinder data ###########################
        }
        assets.append(asset)


################################################################
# IMPORT LOOKUP TABLES
# - mobile capacity, by environment, frequency, bandwidth and site density
# - clutter environment geotype, by population density
################################################################

CAPACITY_LOOKUP_FILENAME = os.path.join(BASE_PATH, 'lookup_table_long.csv')

# create empty dictionary
capacity_lookup_table = {}

with open(CAPACITY_LOOKUP_FILENAME, 'r') as capacity_lookup_file:
    # set DictReader with file name for 4G rollout data
    reader = csv.DictReader(capacity_lookup_file)

    lookup_keys = ["Environment", "Frequency", "Bandwidth"]

    # populate dictionary - this gives a dict for each row, with each heading as a key
    for row in reader:
        environment = row["type"]
        frequency = row["frequency"]
        bandwidth = row["bandwidth"]
        density = row["density"]
        capacity = row["capacity"]

        if (environment, frequency, bandwidth) not in capacity_lookup_table:
            capacity_lookup_table[(environment, frequency, bandwidth)] = []

        capacity_lookup_table[(environment, frequency, bandwidth)].append((density, capacity))

    for key, value_list in capacity_lookup_table.items()
        value_list.sort(key=lambda tup: tup[0])

# lookup_capacity(lookup_table, "Urban", "700 MHz", "2x10 MHz", 50)

################################################################
# START RUNNING MODEL
# - run from BASE_YEAR to END_YEAR in TIMESTEP_INCREMENT steps
# - run over population scenario / demand scenario / intervention strategy combinations
# - output demand, capacity, opex, energy demand, built interventions, build costs per year
################################################################

timesteps = range(BASE_YEAR, END_YEAR, TIMESTEP_INCREMENT)

metrics_filename = 'Data/outputs/metrics.csv'
system_filename = 'Data/outputs/system.csv'

pop_scenario = "high"

with open(metrics_filename, 'w', newline='') as metrics_file:
    with open(system_filename, 'w', newline='') as system_file:
        metrics_writer = csv.writer(metrics_file)
        metrics_writer.writerow(('year', 'area_id', 'area_name', 'cost', 'coverage', 'demand', 'capacity', 'energy_demand'))
        system_writer = csv.writer(system_file)
        system_writer.writerow(('year', 'area_id', 'area_name', 'GSM', 'UMTS', 'LTE', 'LTE-A', '5G'))

        for year in timesteps:
            # Update population from scenario values
            for pcd_sector in pcd_sectors:
                pcd_sector_id = pcd_sector["id"]
                pcd_sector["population"] = population_by_scenario_year_pcd[pop_scenario][year][pcd_sector_id]

            # decide which new interventions to apply
            # add new interventions to assets
            # simply filter from total pipeline list for now
            timestep_assets = [asset for asset in assets if asset["year"] <= year]

            # run model for timestep
            manager = ICTManager(lads, pcd_sectors, timestep_assets)

            # output and report results for this timestep
            timestep_results = manager.results()
            print("Running model for", year)
            pprint.pprint(timestep_results)

            for lad in manager.lads.values():
                area_id = lad.id
                area_name = lad.name

                # Output metrics
                # year,area,cost,coverage,demand,capacity,energy_demand
                cost = timestep_results["cost"][area_name]
                coverage = timestep_results["coverage"][area_name]
                demand = timestep_results["demand"][area_name]
                capacity = timestep_results["capacity"][area_name]
                energy_demand = timestep_results["energy_demand"][area_name]

                metrics_writer.writerow((year, area_id, area_name, cost, coverage, demand, capacity, energy_demand))

                # Output system
                # year,area,GSM,UMTS,LTE,LTE-A,5G
                GSM = timestep_results['system'][area_name]['GSM']
                UMTS = timestep_results['system'][area_name]['UMTS']
                LTE = timestep_results['system'][area_name]['LTE']
                LTE_A = timestep_results['system'][area_name]['LTE-Advanced']
                FIVE_G = timestep_results['system'][area_name]['5G']

                system_writer.writerow((year, area_id, area_name, GSM, UMTS, LTE, LTE_A, FIVE_G))
