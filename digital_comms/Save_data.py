# -*- coding: utf-8 -*-
import digital_comms.Maps as maps
import digital_comms.Plots as plots
import matlab.engine

import csv
import os

#CONFIG = configparser.ConfigParser()
#CONFIG.read(os.path.join(os.path.dirname(__file__), 'script_config.ini'))
#OUTPUT_FOLDER = CONFIG['file_locations']['output_folder']


#    eng = matlab.engine.start_matlab() # ("-desktop") para abrir la GUI
#    MATLAB_FOLDER = "D:\Dropbox\00TFM\git\digital_comms\matlab_scripts"
#    eng.addpath(MATLAB_FOLDER,nargout=0)
#    eng.plot_chart_2(metrics_filename, suffix, nargout=0)

def write_lad_results(ict_manager, year, BASE_YEAR, pop_scenario, throughput_scenario, coverage_scenario,
                      intervention_strategy, cost_by_lad, OUTPUT_FOLDER):
    suffix = _get_suffix(pop_scenario, throughput_scenario, coverage_scenario, intervention_strategy)
    metrics_filename = os.path.join(OUTPUT_FOLDER, 'csv', 'metrics_{}.csv'.format(suffix))

    if year == BASE_YEAR:
        metrics_file = open(metrics_filename, 'w', newline='')
        metrics_writer = csv.writer(metrics_file)
        metrics_writer.writerow(
            ('year', 'area_id', 'area_name', 'cost', 'demand', 'capacity', 'capacity_deficit', 'population', 'pop_density'))
    else:
        metrics_file = open(metrics_filename, 'a', newline='')
        metrics_writer = csv.writer(metrics_file)

    # output and report results for this timestep
    for lad in ict_manager.lads.values():
        # year,area,name,cost,demand,capacity,capacity_deficit,population,population_density
        area_id = lad.id
        area_name = lad.name
        cost = cost_by_lad[lad.id]
        demand = lad.demand()
        capacity = lad.capacity()
        capacity_deficit = capacity - demand
        pop = lad.population
        pop_d = lad.population_density

        metrics_writer.writerow(
            (year, area_id, area_name, cost, demand, capacity, capacity_deficit, pop, pop_d))

    metrics_file.close()

def write_pcd_results(ict_manager, year, BASE_YEAR, pop_scenario, throughput_scenario, coverage_scenario,
                      intervention_strategy, cost_by_pcd, OUTPUT_FOLDER):
    suffix = _get_suffix(pop_scenario, throughput_scenario, coverage_scenario, intervention_strategy)
    metrics_filename = os.path.join(OUTPUT_FOLDER, 'csv', 'pcd_metrics_{}.csv'.format(suffix))

    if year == BASE_YEAR:
        metrics_file = open(metrics_filename, 'w', newline='')
        metrics_writer = csv.writer(metrics_file)
        metrics_writer.writerow(
            ('year', 'postcode', 'cost', 'demand', 'capacity', 'capacity_deficit', 'population', 'pop_density'))
    else:
        metrics_file = open(metrics_filename, 'a', newline='')
        metrics_writer = csv.writer(metrics_file)

    # output and report results for this timestep
    for pcd in ict_manager.postcode_sectors.values():
        # Output metrics
        # year,postcode,demand,capacity,capacity_deficit
        demand = pcd.demand
        capacity = pcd.capacity
        capacity_deficit = capacity - demand
        pop = pcd.population
        pop_d = pcd.population_density
        cost = cost_by_pcd[pcd.id]

        metrics_writer.writerow(
            (year, pcd.id, cost, demand, capacity, capacity_deficit, pop, pop_d))

    metrics_file.close()

def write_decisions(decisions, year, BASE_YEAR, pop_scenario, throughput_scenario, coverage_scenario, intervention_strategy, OUTPUT_FOLDER):
    suffix = _get_suffix(pop_scenario, throughput_scenario, coverage_scenario, intervention_strategy)
    decisions_filename = os.path.join(OUTPUT_FOLDER, 'csv', 'decisions_{}.csv'.format(suffix))

    if year == BASE_YEAR:
        decisions_file = open(decisions_filename, 'w', newline='')
        decisions_writer = csv.writer(decisions_file)
        decisions_writer.writerow(
            ('year', 'pcd_sector', 'site_ngr', 'build_date', 'type', 'technology', 'frequency', 'bandwidth'))
    else:
        decisions_file = open(decisions_filename, 'a', newline='')
        decisions_writer = csv.writer(decisions_file)

    # output and report results for this timestep
    for intervention in decisions:
        # Output decisions
        pcd_sector = intervention['pcd_sector']
        site_ngr = intervention['site_ngr']
        build_date = intervention['build_date']
        intervention_type = intervention['type']
        technology = intervention['technology']
        frequency = intervention['frequency']
        bandwidth = intervention['bandwidth']

        decisions_writer.writerow(
            (year, pcd_sector, site_ngr, build_date, intervention_type, technology, frequency, bandwidth))

    decisions_file.close()

def write_spend(spend, year, BASE_YEAR, pop_scenario, throughput_scenario, coverage_scenario, intervention_strategy, OUTPUT_FOLDER):
    suffix = _get_suffix(pop_scenario, throughput_scenario, coverage_scenario, intervention_strategy)
    spend_filename = os.path.join(OUTPUT_FOLDER, 'csv', 'spend_{}.csv'.format(suffix))

    if year == BASE_YEAR:
        spend_file = open(spend_filename, 'w', newline='')
        spend_writer = csv.writer(spend_file)
        spend_writer.writerow(
            ('year', 'pcd_sector', 'lad', 'item', 'cost', 'reason'))
    else:
        spend_file = open(spend_filename, 'a', newline='')
        spend_writer = csv.writer(spend_file)

    # output and report results for this timestep
    for pcd_sector, lad, item, cost in spend:
        spend_writer.writerow(
            (year, pcd_sector, lad, item, cost))

    spend_file.close()



def write_chart_1(ict_manager, pop_scenario, throughput_scenario, coverage_scenario, intervention_strategy, results, index, TIMESTEPS, OUTPUT_FOLDER):
    print('-> Chart 1 PCDs...')
    chart = results.chart1_get_table(index)
    
    # Saving numerical data
    suffix = _get_suffix(pop_scenario, throughput_scenario, coverage_scenario, intervention_strategy)
    metrics_filename = os.path.join(OUTPUT_FOLDER, 'csv', 'chart_1_{}.csv'.format(suffix))

    metrics_file = open(metrics_filename, 'w', newline='')
    metrics_writer = csv.writer(metrics_file)
    metrics_writer.writerow(('postcode', 'postcode_lad', 'population', 'population_density', 'population_sum', 'cost', 'cost_sum', 'cost_year_2020', 'cost_year_2021', 'cost_year_2022', 'cost_year_2023', 'cost_year_2024', 'cost_year_2025', 'cost_year_2026', 'cost_year_2027', 'cost_year_2028', 'cost_year_2029', 'cost_year_2030'))

    previous_cost = 0;
    for key, value in chart._table.items():
        previous_cost += value[5];
        metrics_writer.writerow((value[0], value[1], value[2], value[3], value[6], value[5], previous_cost, value[4][2020],value[4][2021],value[4][2022],value[4][2023], value[4][2024],value[4][2025],value[4][2026],value[4][2027],value[4][2028],value[4][2029],value[4][2030]))
        chart.add_aggregated_cost(value[0], previous_cost)
    metrics_file.close()
    
    # Plotting
    print('- Ploting Chart 1 PCDs...Total population and cost')
    plots.plot_chart_comparison(chart, "Total population and cost per PCD", ['PCDs', 'Population', 'Cost'], [6,2,5], OUTPUT_FOLDER, 'pcd_chart_1_population_cost', suffix)
    print('- Ploting Chart 1 PCDs...Total population and cost aggregated')
    plots.plot_chart_comparison(chart, "Total population and cost aggregated", ['PCDs', 'Population', 'Cost'], [6,6,7], OUTPUT_FOLDER, 'pcd_chart_1_aggregated_population_cost', suffix)
    print('- Ploting Chart 1 PCDs...Total cost per year')
    plots.plot_chart_per_year(chart, "Total cost per year", [6,4], TIMESTEPS, OUTPUT_FOLDER, 'pcd_chart_1_cost_per_year_all', suffix)  
    
    
    
    
def write_chart_2(ict_manager, pop_scenario, throughput_scenario, coverage_scenario, intervention_strategy, results, index, TIMESTEPS, OUTPUT_FOLDER):
    print('-> Chart 2 PCDs...')
    chart = results.chart2_get_table(index)
    
    # Saving numerical data
    suffix = _get_suffix(pop_scenario, throughput_scenario, coverage_scenario, intervention_strategy)
    metrics_filename = os.path.join(OUTPUT_FOLDER, 'csv', 'chart_2_{}.csv'.format(suffix))

    metrics_file = open(metrics_filename, 'w', newline='')
    metrics_writer = csv.writer(metrics_file)
    metrics_writer.writerow(('postcode', 'postcode_lad', 'population', 'population_density', 'population_sum', 'cap_margin_year_2020', 'cap_margin_year_2021', 'cap_margin_year_2022', 'cap_margin_year_2023', 'cap_margin_year_2024', 'cap_margin_year_2025', 'cap_margin_year_2026', 'cap_margin_year_2027', 'cap_margin_year_2028', 'cap_margin_year_2029', 'cap_margin_year_2030'))
    
    for key, value in chart._table.items():
        metrics_writer.writerow((value[0], value[1], value[2], value[3], value[5], value[4][2020],value[4][2021],value[4][2022],value[4][2023], value[4][2024],value[4][2025],value[4][2026],value[4][2027],value[4][2028],value[4][2029],value[4][2030]))
        
    metrics_file.close()
    
    # Plotting
#    print('- Ploting Chart 1 PCDs...Total population and cost')
#    plots.plot_chart_comparison(chart, "Total population and cost per PCD", ['PCDs', 'Population', 'Cost'], [6,2,5], OUTPUT_FOLDER, 'pcd_chart_1_population_cost', suffix)
#    print('- Ploting Chart 1 PCDs...Total population and cost aggregated')
#    plots.plot_chart_comparison(chart, "Total population and cost aggregated", ['PCDs', 'Population', 'Cost'], [6,6,7], OUTPUT_FOLDER, 'pcd_chart_1_aggregated_population_cost', suffix)
    print('- Ploting Chart 2 PCDs...Capacity margin per year')
    plots.plot_chart_per_year(chart, "Capacity margin per year", [5,4], TIMESTEPS, OUTPUT_FOLDER, 'pcd_chart_2_cap_margin_per_year_all', suffix)  
    

    
    
    
def write_chart_3(ict_manager, pop_scenario, throughput_scenario, coverage_scenario, intervention_strategy, results, index, TIMESTEPS, OUTPUT_FOLDER):
    print('-> Chart 3 PCDs...')
    chart = results.chart3_get_table(index)
    
    # Saving numerical data
    suffix = _get_suffix(pop_scenario, throughput_scenario, coverage_scenario, intervention_strategy)
    metrics_filename = os.path.join(OUTPUT_FOLDER, 'csv', 'chart_3_{}.csv'.format(suffix))
    
    prefix1 = 'Upg_LTE_'
    prefix2 = 'Upg_700_'

    metrics_file = open(metrics_filename, 'w', newline='')
    metrics_writer = csv.writer(metrics_file)
    metrics_writer.writerow(('postcode', 'postcode_lad', 'population', 'population_density', 'population_sum', prefix1 + 'year_2020', prefix2 + 'year_2020', prefix1 + 'year_2021', prefix2 + 'year_2021', prefix1 + 'year_2022', prefix2 + 'year_2022', prefix1 + 'year_2023', prefix2 + 'year_2023', prefix1 + 'year_2024', prefix2 + 'year_2024', prefix1 + 'year_2025', prefix2 + 'year_2025', prefix1 + 'year_2026', prefix2 + 'year_2026', prefix1 + 'year_2027', prefix2 + 'year_2027', prefix1 + 'year_2028', prefix2 + 'year_2028', prefix1 + 'year_2029', prefix2 + 'year_2029', prefix1 + 'year_2030', prefix2 + 'year_2030', prefix1 + 'all', prefix2 + 'all' ))
    
    for key, value in chart._table.items():
        metrics_writer.writerow((value[0], value[1], value[2], value[3], value[8], value[4][2020], value[5][2020], value[4][2021], value[5][2021], value[4][2022], value[5][2022], value[4][2023], value[5][2023], value[4][2024], value[5][2024], value[4][2025], value[5][2025], value[4][2026], value[5][2026], value[4][2027], value[5][2027], value[4][2028], value[5][2028], value[4][2029], value[5][2029], value[4][2030], value[5][2030], value[6], value[7]))

    metrics_file.close()
    
    # Plotting
    print('- Ploting Chart 3 PCDs...Total technology upgrades')
    plots.plot_chart_comparison(chart, "Total technology upgrades per PCD", ['PCDs', 'LTE', '700MHz'], [8,6,7], OUTPUT_FOLDER, 'pcd_chart_3_tech_upgrades', suffix)
#    print('- Ploting Chart 3 PCDs...Total technology upgrades aggregated')
#    plots.plot_chart_comparison(chart, "Total technology upgrades aggregated", ['PCDs', 'Population', 'Cost'], [8,8,7], OUTPUT_FOLDER, 'pcd_chart_3_aggregated_tech_upgrades', suffix)
    print('- Ploting Chart 3 PCDs...Total LTE technology upgrades per year')
    plots.plot_chart_per_year(chart, "Total LTE technology upgrades per year", [8,4], TIMESTEPS, OUTPUT_FOLDER, 'pcd_chart_3_lte_tech_upgrades_per_year_all', suffix)  
    print('- Ploting Chart 3 PCDs...Total 700MHz technology upgrades per year')
    plots.plot_chart_per_year(chart, "Total 700 MHz technology upgrades per year", [8,5], TIMESTEPS, OUTPUT_FOLDER, 'pcd_chart_3_700_tech_upgrades_per_year_all', suffix)  
    
   
    
def write_chart_1_LADs(ict_manager, pop_scenario, throughput_scenario, coverage_scenario, intervention_strategy, results, index, TIMESTEPS, OUTPUT_FOLDER):
    print('-> Chart 1 LADs...')
    chart = results.chart1_lads_get_table(index)
    
    # Saving data
    suffix = _get_suffix(pop_scenario, throughput_scenario, coverage_scenario, intervention_strategy)
    metrics_filename = os.path.join(OUTPUT_FOLDER, 'csv', 'chart_1_lads_{}.csv'.format(suffix))

    metrics_file = open(metrics_filename, 'w', newline='')
    metrics_writer = csv.writer(metrics_file)
    metrics_writer.writerow(('lad_id', 'name', 'population', 'population_density', 'population_sum', 'cost', 'cost_sum', 'cost_year_2020', 'cost_year_2021', 'cost_year_2022', 'cost_year_2023', 'cost_year_2024', 'cost_year_2025', 'cost_year_2026', 'cost_year_2027', 'cost_year_2028', 'cost_year_2029', 'cost_year_2030'))

    previous_cost = 0;
    for key, value in chart._table.items():
        previous_cost += value[5];
        metrics_writer.writerow((value[0], value[1], value[2], value[3], value[6], value[5], previous_cost, value[4][2020],value[4][2021],value[4][2022],value[4][2023], value[4][2024],value[4][2025],value[4][2026],value[4][2027],value[4][2028],value[4][2029],value[4][2030]))
        chart.add_aggregated_cost(value[0], previous_cost)
    metrics_file.close()

    
    # Plotting
    print('- Ploting Chart 1 LADs...Total population')
    plots.plot_chart(chart, "Total population", [6,2], OUTPUT_FOLDER, 'chart_1_aggregated_population', suffix)
    print('- Ploting Chart 1 LADs...Total population and cost')
    plots.plot_chart_comparison(chart, "Total population and cost per LAD", ['LADs', 'Population', 'Cost'], [6,2,5], OUTPUT_FOLDER, 'lad_chart_1_population_cost', suffix)
    print('- Ploting Chart 1 LADs...Total population and cost aggregated')
    plots.plot_chart_comparison(chart, "Total population and cost aggregated", ['LADs', 'Population', 'Cost'], [6,6,7], OUTPUT_FOLDER, 'lad_chart_1_aggregated_population_cost', suffix)
    print('- Ploting Chart 1 LADs...Total cost per year')
    plots.plot_chart_per_year(chart, "Total cost per year", [6,4], TIMESTEPS, OUTPUT_FOLDER, 'lad_chart_1_cost_per_year_all', suffix)  
    
    # Maps
    print('- Drawing Chart 1 LADs...Total population')
    maps.print_map(chart, "Total population", 2, OUTPUT_FOLDER, 'lad_chart_1_aggregated_population', suffix)
    print('- Drawing Chart 1 LADs...Total cost')
    maps.print_map(chart, "Total cost", 5, OUTPUT_FOLDER, 'lad_chart_1_aggregated_cost', suffix)
    print('- Drawing Chart 1 LADs...Total cost during all years')
    maps.print_map_year_all(chart, "Total cost per year", 4, TIMESTEPS, OUTPUT_FOLDER, 'lad_chart_1_cost_per_year', suffix)
    print('- Drawing Chart 1 LADs...Total cost per year')
    maps.print_map_per_year(chart, "Total cost year", 4, TIMESTEPS, OUTPUT_FOLDER, 'lad_chart_1_cost_year', suffix)

    
    
    
def write_chart_2_LADs(ict_manager, pop_scenario, throughput_scenario, coverage_scenario, intervention_strategy, results, index, TIMESTEPS, OUTPUT_FOLDER):
    print('-> Chart 2 LADs...')
    chart = results.chart2_lads_get_table(index)
    
    # Saving data
    suffix = _get_suffix(pop_scenario, throughput_scenario, coverage_scenario, intervention_strategy)
    metrics_filename = os.path.join(OUTPUT_FOLDER, 'csv', 'chart_2_lads_{}.csv'.format(suffix))

    metrics_file = open(metrics_filename, 'w', newline='')
    metrics_writer = csv.writer(metrics_file)
    metrics_writer.writerow(('lad_id', 'name', 'population', 'population_density', 'population_sum', 'cap_margin_year_2020', 'cap_margin_year_2021', 'cap_margin_year_2022', 'cap_margin_year_2023', 'cap_margin_year_2024', 'cap_margin_year_2025', 'cap_margin_year_2026', 'cap_margin_year_2027', 'cap_margin_year_2028', 'cap_margin_year_2029', 'cap_margin_year_2030'))
    
    for key, value in chart._table.items():
        metrics_writer.writerow((value[0], value[1], value[2], value[3], value[5], value[4][2020],value[4][2021],value[4][2022],value[4][2023], value[4][2024],value[4][2025],value[4][2026],value[4][2027],value[4][2028],value[4][2029],value[4][2030]))

    metrics_file.close()

    # Plotting
    print('- Ploting Chart 2 LADs...Capacity margin per year')
    plots.plot_chart_per_year(chart, "Capacity margin per year", [5,4], TIMESTEPS, OUTPUT_FOLDER, 'lad_chart_2_cap_margin_per_year_all', suffix)  

    # Maps
    print('- Drawing Chart 2 LADs...Capacity margin during all years')
    maps.print_map_year_all(chart, "Capacity margin per year", 4, TIMESTEPS, OUTPUT_FOLDER, 'lad_chart_2_cap_margin_per_year', suffix)
    print('- Drawing Chart 2 LADs...Capacity margin per year')
    maps.print_map_per_year(chart, "Capacity margin year", 4, TIMESTEPS, OUTPUT_FOLDER, 'lad_chart_2_cap_margin_year', suffix)
    
    
    
def write_chart_3_LADs(ict_manager, pop_scenario, throughput_scenario, coverage_scenario, intervention_strategy, results, index, TIMESTEPS, OUTPUT_FOLDER):
    print('-> Chart 3 LADs...')
    chart = results.chart3_lads_get_table(index)
    
    # Saving data
    suffix = _get_suffix(pop_scenario, throughput_scenario, coverage_scenario, intervention_strategy)
    metrics_filename = os.path.join(OUTPUT_FOLDER, 'csv', 'chart_3_lads_{}.csv'.format(suffix))
    
    prefix1 = 'Upg_LTE_'
    prefix2 = 'Upg_700_'

    metrics_file = open(metrics_filename, 'w', newline='')
    metrics_writer = csv.writer(metrics_file)
    metrics_writer.writerow(('lad_id', 'name', 'population', 'population_density', 'population_sum', prefix1 + 'year_2020', prefix2 + 'year_2020', prefix1 + 'year_2021', prefix2 + 'year_2021', prefix1 + 'year_2022', prefix2 + 'year_2022', prefix1 + 'year_2023', prefix2 + 'year_2023', prefix1 + 'year_2024', prefix2 + 'year_2024', prefix1 + 'year_2025', prefix2 + 'year_2025', prefix1 + 'year_2026', prefix2 + 'year_2026', prefix1 + 'year_2027', prefix2 + 'year_2027', prefix1 + 'year_2028', prefix2 + 'year_2028', prefix1 + 'year_2029', prefix2 + 'year_2029', prefix1 + 'year_2030', prefix2 + 'year_2030', prefix1 + 'all_years', prefix2 + 'all_years'))
    
    for key, value in chart._table.items():
        metrics_writer.writerow((value[0], value[1], value[2], value[3], value[8], value[4][2020], value[5][2020], value[4][2021], value[5][2021], value[4][2022], value[5][2022], value[4][2023], value[5][2023], value[4][2024], value[5][2024], value[4][2025], value[5][2025], value[4][2026], value[5][2026], value[4][2027], value[5][2027], value[4][2028], value[5][2028], value[4][2029], value[5][2029], value[4][2030], value[5][2030], value[6], value[7]))

    metrics_file.close()

    # Plotting
#    print('- Ploting Chart 1 LADs...Total population')
#    plots.plot_chart(chart, "Total population", [6,2], OUTPUT_FOLDER, 'chart_1_aggregated_population', suffix)
    print('- Ploting Chart 3 LADs...Total technology upgrades')
    plots.plot_chart_comparison(chart, "Total technology upgrades per LAD", ['LADs', 'LTE upgrades', '700MHz upgrades'], [8,6,7], OUTPUT_FOLDER, 'lad_chart_3_tech_upgrades', suffix)
#    print('- Ploting Chart 3 LADs...Total technology upgrades aggregated')
#    plots.plot_chart_comparison(chart, "Total technology upgrades aggregated", ['LADs', 'LTE upgrades', '700MHz upgrades'], [8,6,7], OUTPUT_FOLDER, 'chart_3_aggregated_tech_upgrades', suffix)
    print('- Ploting Chart 3 LADs...Total LTE technology upgrades per year')
    plots.plot_chart_per_year(chart, "Total LTE technology upgrades per year", [8,4], TIMESTEPS, OUTPUT_FOLDER, 'lad_chart_3_lte_tech_upgrades_per_year_all', suffix)  
    print('- Ploting Chart 3 LADs...Total 700MHz technology upgrades per year')
    plots.plot_chart_per_year(chart, "Total 700MHz technology upgrades per year", [8,5], TIMESTEPS, OUTPUT_FOLDER, 'lad_chart_3_700_tech_upgrades_per_year_all', suffix)  
    
    # Maps
    print('- Drawing Chart 3 LADs...Total technology upgrades')
    maps.print_tech_map_aggregated(chart, "Total technology upgrades", [6,7], OUTPUT_FOLDER, 'lad_chart_3_aggregated_tech_upgrades', suffix)
#    print('- Drawing Chart 3 LADs...Technology upgrades during all years')
#    maps.print_map_year_all(chart, "Technology upgrades per year", [4,5], TIMESTEPS, OUTPUT_FOLDER, 'chart_3_tech_upgrades_per_year', suffix)
    print('- Drawing Chart 3 LADs...Technology upgrades per year')
    maps.print_tech_map_per_year(chart, "Technology upgrades year", [4,5], TIMESTEPS, OUTPUT_FOLDER, 'lad_chart_3_tech_upgrades_year', suffix)
    
    
def _get_suffix(pop_scenario, throughput_scenario, coverage_scenario, intervention_strategy):
    suffix = 'pop_{}_throughput_{}_coverage_{}_strategy_{}_'.format(
        pop_scenario, throughput_scenario, coverage_scenario, intervention_strategy)
    # for length, use 'base' for baseline scenarios
    suffix = suffix.replace('baseline', 'base')
    return suffix
