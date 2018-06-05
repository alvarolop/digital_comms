# -*- coding: utf-8 -*-
import digital_comms.maps as maps
import digital_comms.plots as plots
import csv
import os
import imageio

ENABLE_SUB_PLOTS = True


def write_chart_1(ict_manager, coverage_obligation_type, pop_scenario, throughput_scenario, coverage_scenario, intervention_strategy, results, index, TIMESTEPS, OUTPUT_FOLDER):
    print('-> Chart 1 PCDs...')
    chart = results.chart1_get_table(index)
    
    # Saving numerical data
    suffix = _get_suffix(coverage_obligation_type, pop_scenario, throughput_scenario, coverage_scenario, intervention_strategy)
    metrics_filename = os.path.join(OUTPUT_FOLDER, 'csv', 'pcd_chart_1_{}.csv'.format(suffix))

    prefix = "cost_"

    metrics_file = open(metrics_filename, 'w', newline='')
    metrics_writer = csv.writer(metrics_file)
    metrics_writer.writerow(('postcode', 'postcode_lad', 'population', 'population_density', 'population_sum',
                             'population_covered', 'population_covered_sum', 'cost', 'cost_sum', prefix + 'year_2020',
                             prefix + 'year_2021', prefix + 'year_2022', prefix + 'year_2023', prefix + 'year_2024',
                             prefix + 'year_2025', prefix + 'year_2026', prefix + 'year_2027', prefix + 'year_2028',
                             prefix + 'year_2029', prefix + 'year_2030'))

    previous_cost = 0
    previous_pop_covered = 0
    for key, value in chart._table.items():
        previous_cost += value[5]
        previous_pop_covered += value[8]
        metrics_writer.writerow((value[0], value[1], value[2], value[3], value[6], value[8], previous_pop_covered, value[5], previous_cost, value[4][2020],value[4][2021],value[4][2022],value[4][2023], value[4][2024],value[4][2025],value[4][2026],value[4][2027],value[4][2028],value[4][2029],value[4][2030]))
        chart.add_aggregated_cost(value[0], previous_cost)
        chart.add_aggregated_population_covered(value[0], previous_pop_covered)
    metrics_file.close()

    if ENABLE_SUB_PLOTS:
        # Plotting
        print('- Plotting Chart 1 PCDs...Total population and cost aggregated')
        plots.plot_chart(ict_manager, results, chart, 2, 6, 5, 7, "Cost", ['% Population covered', 'Cost (£)'], '1_1_cost', suffix)
        
    #    print('- Plotting Chart 1 PCDs...Total population and cost')
    #    plots.plot_chart_comparison(ict_manager, results, chart, 6, [2,5], "Total population and cost per PCD", ['PCDs', 'Population', 'Cost'], 'pcd_chart_1_population_cost', suffix)
    #    print('- Plotting Chart 1 PCDs...Total population and cost aggregated')
    #    plots.plot_chart_comparison(ict_manager, results, chart, 6, [6,7], "Total population and cost aggregated", ['PCDs', 'Population', 'Cost'], 'pcd_chart_1_aggregated_population_cost', suffix)

        print('- Plotting Chart 1 PCDs...Total cost per year')
        plots.plot_chart_per_year(ict_manager, results, chart, 6, [4], TIMESTEPS, "Total cost per year", ['PCDs'], '1_2_cost_per_year_all', suffix)

    
def write_chart_2(ict_manager, coverage_obligation_type, pop_scenario, throughput_scenario, coverage_scenario, intervention_strategy, results, index, TIMESTEPS, OUTPUT_FOLDER):
    print('-> Chart 2 PCDs...')
    chart = results.chart2_get_table(index)
    
    # Saving numerical data
    suffix = _get_suffix(coverage_obligation_type, pop_scenario, throughput_scenario, coverage_scenario, intervention_strategy)
    metrics_filename = os.path.join(OUTPUT_FOLDER, 'csv', 'pcd_chart_2_{}.csv'.format(suffix))
    
    prefix = "cap_margin_"

    metrics_file = open(metrics_filename, 'w', newline='')
    metrics_writer = csv.writer(metrics_file)
    metrics_writer.writerow(('postcode', 'postcode_lad', 'population', 'population_density', 'population_sum', prefix + 'year_2020', prefix + 'year_2021', prefix + 'year_2022', prefix + 'year_2023', prefix + 'year_2024', prefix + 'year_2025', prefix + 'year_2026', prefix + 'year_2027', prefix + 'year_2028', prefix + 'year_2029', prefix + 'year_2030'))
    
    for key, value in chart._table.items():
        metrics_writer.writerow((value[0], value[1], value[2], value[3], value[5], value[4][2020],value[4][2021],value[4][2022],value[4][2023], value[4][2024],value[4][2025],value[4][2026],value[4][2027],value[4][2028],value[4][2029],value[4][2030]))
        
    metrics_file.close()
    
    if ENABLE_SUB_PLOTS:
        # Plotting
        print('- Plotting Chart 2 PCDs...Capacity margin per year')
        plots.plot_chart_per_year(ict_manager, results, chart, 5, [4], TIMESTEPS, "Capacity margin per year", ['PCDs'],
                                  '2_1_cap_margin_per_year_all', suffix)
        # print('- Plotting Chart 2 PCDs...Capacity margin each year')
        plots.plot_chart_detail_per_year(ict_manager, results, chart, 5, [4], TIMESTEPS,
                                         "Capacity margin in {} per PCD", ['PCD ID', "Capacity margin"],
                                         '2_cap_margin_per_year_all', suffix)

        print('- Plotting Chart 2 PCDs...capacity margin histogram')
        plots.plot_histogram(ict_manager, results, chart, TIMESTEPS, False, 'Capacity', 4, "Capacity margin histogram",
                                        ['Capacity margin', 'Frequency'], '2_2_cap_margin_histogram', suffix)
        print('- Plotting Chart 2 PCDs...capacity margin cumulative histogram CDF')
        plots.plot_histogram(ict_manager, results, chart, TIMESTEPS, True, 'Capacity', 4, "Capacity margin histogram",
                                        ['Capacity margin', 'Frequency'], '2_2_cap_margin_CDF_histogram', suffix)


def write_chart_3(ict_manager, coverage_obligation_type, pop_scenario, throughput_scenario, coverage_scenario, intervention_strategy, results, index, TIMESTEPS, OUTPUT_FOLDER):
    print('-> Chart 3 PCDs...')
    chart = results.chart3_get_table(index)
    
    # Saving numerical data
    suffix = _get_suffix(coverage_obligation_type, pop_scenario, throughput_scenario, coverage_scenario, intervention_strategy)
    metrics_filename = os.path.join(OUTPUT_FOLDER, 'csv', 'pcd_chart_3_{}.csv'.format(suffix))
    
    prefix1 = 'Upg_LTE_'
    prefix2 = 'Upg_700_'

    metrics_file = open(metrics_filename, 'w', newline='')
    metrics_writer = csv.writer(metrics_file)
    metrics_writer.writerow(('postcode', 'postcode_lad', 'population', 'population_density', 'population_sum', prefix1 + 'year_2020', prefix2 + 'year_2020', prefix1 + 'year_2021', prefix2 + 'year_2021', prefix1 + 'year_2022', prefix2 + 'year_2022', prefix1 + 'year_2023', prefix2 + 'year_2023', prefix1 + 'year_2024', prefix2 + 'year_2024', prefix1 + 'year_2025', prefix2 + 'year_2025', prefix1 + 'year_2026', prefix2 + 'year_2026', prefix1 + 'year_2027', prefix2 + 'year_2027', prefix1 + 'year_2028', prefix2 + 'year_2028', prefix1 + 'year_2029', prefix2 + 'year_2029', prefix1 + 'year_2030', prefix2 + 'year_2030', prefix1 + 'all', prefix2 + 'all' ))
    
    for key, value in chart._table.items():
        metrics_writer.writerow((value[0], value[1], value[2], value[3], value[8], value[4][2020], value[5][2020], value[4][2021], value[5][2021], value[4][2022], value[5][2022], value[4][2023], value[5][2023], value[4][2024], value[5][2024], value[4][2025], value[5][2025], value[4][2026], value[5][2026], value[4][2027], value[5][2027], value[4][2028], value[5][2028], value[4][2029], value[5][2029], value[4][2030], value[5][2030], value[6], value[7]))

    metrics_file.close()

    if ENABLE_SUB_PLOTS:
        # Plotting
        print('- Plotting Chart 3 PCDs...Total technology upgrades')
        plots.plot_chart_comparison(ict_manager, results, chart, 8, [6,7], "Total technology upgrades per PCD", ['PCDs', 'LTE', '700MHz'], '3_1_tech_upgrades', suffix)
        print('- Plotting Chart 3 PCDs...Total LTE technology upgrades per year')
        plots.plot_chart_per_year(ict_manager, results, chart, 8, [4], TIMESTEPS, "Total LTE technology upgrades per year", ['PCDs'], '3_2_lte_tech_upgrades_per_year_all', suffix)
        print('- Plotting Chart 3 PCDs...Total 700MHz technology upgrades per year')
        plots.plot_chart_per_year(ict_manager, results, chart, 8, [5], TIMESTEPS, "Total 700 MHz technology upgrades per year", ['PCDs'], '3_3_700_tech_upgrades_per_year_all', suffix)


def write_chart_4(ict_manager, coverage_obligation_type, pop_scenario, throughput_scenario, coverage_scenario, intervention_strategy, results, index, TIMESTEPS, OUTPUT_FOLDER):
    print('-> Chart 4 PCDs...')
    chart = results.chart4_get_table(index)
    
    # Saving numerical data
    suffix = _get_suffix(coverage_obligation_type, pop_scenario, throughput_scenario, coverage_scenario, intervention_strategy)
    metrics_filename = os.path.join(OUTPUT_FOLDER, 'csv', 'pcd_chart_4_{}.csv'.format(suffix))
    
    prefix1 = "capacity_"
    prefix2 = "demand_"
    prefix3 = "pop_covered_"

    metrics_file = open(metrics_filename, 'w', newline='')
    metrics_writer = csv.writer(metrics_file)
    metrics_writer.writerow(('postcode', 'postcode_lad', 'population', 'population_density', 'population_sum', prefix1 + 'year_2020', prefix2 + 'year_2020', prefix3 + 'year_2020', prefix1 + 'year_2021', prefix2 + 'year_2021', prefix3 + 'year_2021', prefix1 + 'year_2022', prefix2 + 'year_2022', prefix3 + 'year_2022', prefix1 + 'year_2023', prefix2 + 'year_2023', prefix3 + 'year_2023', prefix1 + 'year_2024', prefix2 + 'year_2024', prefix3 + 'year_2024', prefix1 + 'year_2025', prefix2 + 'year_2025', prefix3 + 'year_2025', prefix1 + 'year_2026', prefix2 + 'year_2026', prefix3 + 'year_2026', prefix1 + 'year_2027', prefix2 + 'year_2027', prefix3 + 'year_2027', prefix1 + 'year_2028', prefix2 + 'year_2028', prefix3 + 'year_2028', prefix1 + 'year_2029', prefix2 + 'year_2029', prefix3 + 'year_2029', prefix1 + 'year_2030', prefix2 + 'year_2030', prefix3 + 'year_2030'))

    for key, value in chart._table.items():
        metrics_writer.writerow((value[0], value[1], value[2], value[3], value[8], value[4][2020], value[5][2020], value[6][2020], value[4][2021], value[5][2021], value[6][2021], value[4][2022], value[5][2022], value[6][2022], value[4][2023], value[5][2023], value[6][2023], value[4][2024], value[5][2024], value[6][2024], value[4][2025], value[5][2025], value[6][2025], value[4][2026], value[5][2026], value[6][2026], value[4][2027], value[5][2027], value[6][2027], value[4][2028], value[5][2028], value[6][2028], value[4][2029], value[5][2029], value[6][2029], value[4][2030], value[5][2030], value[6][2030]))
    metrics_file.close()

    if ENABLE_SUB_PLOTS:
        # Plotting
        print('- Plotting Chart 4 PCDs...Total capacity per year')
        plots.plot_chart_per_year(ict_manager, results, chart, 8, [4], TIMESTEPS, "Total capacity per year", ['PCDs'],
                                  '4_1_capacity_per_year_all', suffix)
        print('- Plotting Chart 4 PCDs...Total demand per year')
        plots.plot_chart_per_year(ict_manager, results, chart, 8, [5], TIMESTEPS, "Total demand per year", ['PCDs'],
                                  '4_2_demand_per_year_all', suffix)

        print('- Plotting Chart 4 PCDs...Total capacity each year')
        plots.plot_chart_detail_per_year(ict_manager, results, chart, 8, [4], TIMESTEPS, "Capacity in {} per PCD",
                                         ['PCD ID', "Capacity"], '4_1_capacity_per_year_all', suffix)
        print('- Plotting Chart 4 PCDs...Total demand each year')
        plots.plot_chart_detail_per_year(ict_manager, results, chart, 8, [5], TIMESTEPS, "Demand in {} per PCD",
                                         ['PCD ID', "Demand"], '4_2_demand_per_year_all', suffix)

        print('- Plotting Chart 4 PCDs...Total population covered per year')
        plots.plot_chart_per_year(ict_manager, results, chart, 8, [6], TIMESTEPS, "Total population covered per year",
                                        ['PCDs'], '4_3_pop_covered_per_year_all', suffix)
        print('- Plotting Chart 4 PCDs...Population covered histogram')
        plots.plot_histogram(ict_manager, results, chart, TIMESTEPS, False, 'Percentage', 6, "Population covered histogram",
                                        ['% Population covered', 'Frequency'], '4_4_pop_covered_histogram', suffix)
        print('- Plotting Chart 4 PCDs...Population covered cumulative histogram CDF')
        plots.plot_histogram(ict_manager, results, chart, TIMESTEPS, True, 'Percentage', 6, "Population covered histogram",
                                        ['% Population covered', 'Frequency'], '4_4_pop_covered_CDF_histogram', suffix)


def write_chart_5(ict_manager, coverage_obligation_type, pop_scenario, throughput_scenario, coverage_scenario,
                  intervention_strategy, results, index, TIMESTEPS, OUTPUT_FOLDER):
    print('-> Chart 5 PCDs...')
    chart = results.chart5_get_table(index)

    # Saving numerical data
    suffix = _get_suffix(coverage_obligation_type, pop_scenario, throughput_scenario, coverage_scenario,
                         intervention_strategy)
    metrics_filename = os.path.join(OUTPUT_FOLDER, 'csv', 'pcd_chart_5_{}.csv'.format(suffix))

    metrics_file = open(metrics_filename, 'w', newline='')
    metrics_writer = csv.writer(metrics_file)
    metrics_writer.writerow(('Year', 'Population', 'Cost', 'Aggregated cost', '% Population covered', '# PCDs covered',
                             'Capacity margin', 'Invest by demand'))

    for key, value in chart._table.items():
        metrics_writer.writerow((value[0], value[1], value[2], value[3], value[4], value[5], value[6], value[7]))
    metrics_file.close()

    if ENABLE_SUB_PLOTS:
        # Plotting
        # print('- Plotting Chart 5 PCDs... Costs per year')
        # plots.plot_years(ict_manager, results, chart, TIMESTEPS, 8, 9, 5, 7, "Total cost", ['Population Covered', 'Cost (£)'], '5_1_cost_per_year', suffix)
        print('- Plotting Chart 5 PCDs... %Costs per year')
        plots.plot_years(ict_manager, results, chart, TIMESTEPS, 0, 2, "Investment", ['Time', 'Cost (£)'], 'Cost', '5_1_cost_per_year', suffix, 7)
        print('- Plotting Chart 5 PCDs... % population covered per year')
        plots.plot_years(ict_manager, results, chart, TIMESTEPS, 0, 4, "Population covered", ['Time', 'Population percentage'], 'Percentage', '5_2_pop_covered_per_year', suffix, 7)
        print('- Plotting Chart 5 PCDs... Capacity margin per year')
        plots.plot_years(ict_manager, results, chart, TIMESTEPS, 0, 6, "Capacity margin", ['Time', 'Capacity margin'], 'Capacity', '5_3_cap_margin_per_year', suffix, 7)


def write_chart_1_lads(ict_manager, coverage_obligation_type, pop_scenario, throughput_scenario, coverage_scenario, intervention_strategy, results, index, TIMESTEPS, OUTPUT_FOLDER):
    print('-> Chart 1 LADs...')
    chart = results.chart1_lads_get_table(index)
    
    # Saving data
    suffix = _get_suffix(coverage_obligation_type, pop_scenario, throughput_scenario, coverage_scenario, intervention_strategy)
    metrics_filename = os.path.join(OUTPUT_FOLDER, 'csv', 'lad_chart_1_{}.csv'.format(suffix))

    metrics_file = open(metrics_filename, 'w', newline='')
    metrics_writer = csv.writer(metrics_file)
    metrics_writer.writerow(('lad_id', 'name', 'population', 'population_density', 'population_sum', 'cost', 'cost_sum', 'cost_year_2020', 'cost_year_2021', 'cost_year_2022', 'cost_year_2023', 'cost_year_2024', 'cost_year_2025', 'cost_year_2026', 'cost_year_2027', 'cost_year_2028', 'cost_year_2029', 'cost_year_2030'))

    previous_cost = 0
    for key, value in chart._table.items():
        previous_cost += value[5]
        metrics_writer.writerow((value[0], value[1], value[2], value[3], value[6], value[5], previous_cost, value[4][2020],value[4][2021],value[4][2022],value[4][2023], value[4][2024],value[4][2025],value[4][2026],value[4][2027],value[4][2028],value[4][2029],value[4][2030]))
        chart.add_aggregated_cost(value[0], previous_cost)
    metrics_file.close()

    if ENABLE_SUB_PLOTS:
        # Maps
        print('- Drawing Chart 1 LADs...Population')
        maps.print_map(chart, "Population", 2, results, '1_1_population', suffix, 'Blues')
        print('- Drawing Chart 1 LADs...Population density')
        maps.print_map(chart, "Population density", 3, results, '1_2_population_density', suffix, 'Blues')
        print('- Drawing Chart 1 LADs...Total cost')
        maps.print_map(chart, "Total cost", 5, results, '1_3_aggregated_cost', suffix, 'OrRd')
        print('- Drawing Chart 1 LADs...Total cost during all years')
        maps.print_map_year_all(chart, "Total cost per year", 4, TIMESTEPS, False, results, '1_4_cost_per_year', suffix, 'OrRd')
        print('- Drawing Chart 1 LADs...Total cost per year')
        maps.print_map_per_year(chart, "Total cost year", 4, TIMESTEPS, results, 'lad_chart_1_cost_year', suffix, 'OrRd')
    
    
def write_chart_2_lads(ict_manager, coverage_obligation_type, pop_scenario, throughput_scenario, coverage_scenario, intervention_strategy, results, index, TIMESTEPS, OUTPUT_FOLDER):
    print('-> Chart 2 LADs...')
    chart = results.chart2_lads_get_table(index)
    
    # Saving data
    suffix = _get_suffix(coverage_obligation_type, pop_scenario, throughput_scenario, coverage_scenario, intervention_strategy)
    metrics_filename = os.path.join(OUTPUT_FOLDER, 'csv', 'lad_chart_2_{}.csv'.format(suffix))

    metrics_file = open(metrics_filename, 'w', newline='')
    metrics_writer = csv.writer(metrics_file)
    metrics_writer.writerow(('lad_id', 'name', 'population', 'population_density', 'population_sum', 'cap_margin_year_2020', 'cap_margin_year_2021', 'cap_margin_year_2022', 'cap_margin_year_2023', 'cap_margin_year_2024', 'cap_margin_year_2025', 'cap_margin_year_2026', 'cap_margin_year_2027', 'cap_margin_year_2028', 'cap_margin_year_2029', 'cap_margin_year_2030'))
    
    for key, value in chart._table.items():
        metrics_writer.writerow((value[0], value[1], value[2], value[3], value[5], value[4][2020],value[4][2021],value[4][2022],value[4][2023], value[4][2024],value[4][2025],value[4][2026],value[4][2027],value[4][2028],value[4][2029],value[4][2030]))

    metrics_file.close()

    if ENABLE_SUB_PLOTS:
        # Maps
        print('- Drawing Chart 2 LADs...Capacity margin during all years')
        maps.print_map_year_all(chart, "Capacity margin per year", 4, TIMESTEPS, False, results, '2_1_cap_margin_per_year', suffix, 'RdYlGn')
        print('- Drawing Chart 2 LADs...Capacity margin per year')
        maps.print_map_per_year(chart, "Capacity margin year", 4, TIMESTEPS, results, '2_1_cap_margin_year', suffix, 'RdYlGn') # OrRd

    
def write_chart_3_lads(ict_manager, coverage_obligation_type, pop_scenario, throughput_scenario, coverage_scenario, intervention_strategy, results, index, TIMESTEPS, OUTPUT_FOLDER):
    print('-> Chart 3 LADs...')
    chart = results.chart3_lads_get_table(index)
    
    # Saving data
    suffix = _get_suffix(coverage_obligation_type, pop_scenario, throughput_scenario, coverage_scenario, intervention_strategy)
    metrics_filename = os.path.join(OUTPUT_FOLDER, 'csv', 'lad_chart_3_{}.csv'.format(suffix))
    
    prefix1 = 'Upg_LTE_'
    prefix2 = 'Upg_700_'

    metrics_file = open(metrics_filename, 'w', newline='')
    metrics_writer = csv.writer(metrics_file)
    metrics_writer.writerow(('lad_id', 'name', 'population', 'population_density', 'population_sum', prefix1 + 'year_2020', prefix2 + 'year_2020', prefix1 + 'year_2021', prefix2 + 'year_2021', prefix1 + 'year_2022', prefix2 + 'year_2022', prefix1 + 'year_2023', prefix2 + 'year_2023', prefix1 + 'year_2024', prefix2 + 'year_2024', prefix1 + 'year_2025', prefix2 + 'year_2025', prefix1 + 'year_2026', prefix2 + 'year_2026', prefix1 + 'year_2027', prefix2 + 'year_2027', prefix1 + 'year_2028', prefix2 + 'year_2028', prefix1 + 'year_2029', prefix2 + 'year_2029', prefix1 + 'year_2030', prefix2 + 'year_2030', prefix1 + 'all_years', prefix2 + 'all_years'))
    
    for key, value in chart._table.items():
        metrics_writer.writerow((value[0], value[1], value[2], value[3], value[8], value[4][2020], value[5][2020], value[4][2021], value[5][2021], value[4][2022], value[5][2022], value[4][2023], value[5][2023], value[4][2024], value[5][2024], value[4][2025], value[5][2025], value[4][2026], value[5][2026], value[4][2027], value[5][2027], value[4][2028], value[5][2028], value[4][2029], value[5][2029], value[4][2030], value[5][2030], value[6], value[7]))

    metrics_file.close()

    if ENABLE_SUB_PLOTS:
        # Maps
        print('- Drawing Chart 3 LADs...Total technology upgrades')
        maps.print_tech_map_aggregated(chart, "Total technology upgrades", [6, 7], results, '3_1_aggregated_tech_upgrades', suffix, 'Blues')
        print('- Drawing Chart 3 LADs...Technology upgrades per year')
        maps.print_tech_map_per_year(chart, "Technology upgrades", [4, 5], TIMESTEPS, results, '3_1_tech_upgrades_year', suffix, 'Blues') # OrRd
        print('- Drawing Chart 3 LADs...Technology upgrades per year')
        maps.print_tech_map_per_year(chart, "Technology upgrades", [4, 5], TIMESTEPS, results, '3_1_tech_upgrades_year',
                                     suffix, 'Blues')  # OrRd

        print('- Drawing Chart 3 LADs...Total LTE upgrades during all years')
        maps.print_map_year_all(chart, "LTE upgrades", 4, TIMESTEPS, False, results, '3_3_lte_upgrades_per_year', suffix, 'Blues')
        print('- Drawing Chart 3 LADs...Total 700 MHz upgrades during all years')
        maps.print_map_year_all(chart, "700 MHz upgrades", 5, TIMESTEPS, False, results, '3_3_700_upgrades_per_year', suffix, 'Blues')


def write_chart_4_lads(ict_manager, coverage_obligation_type, pop_scenario, throughput_scenario, coverage_scenario, intervention_strategy, results, index, TIMESTEPS, OUTPUT_FOLDER):
    print('-> Chart 4 LADs...')
    chart = results.chart4_lads_get_table(index)
    
    # Saving data
    suffix = _get_suffix(coverage_obligation_type, pop_scenario, throughput_scenario, coverage_scenario, intervention_strategy)
    metrics_filename = os.path.join(OUTPUT_FOLDER, 'csv', 'lad_chart_4_{}.csv'.format(suffix))

    prefix1 = "capacity_"
    prefix2 = "demand_"
    prefix3 = "pop_covered_"
    
    metrics_file = open(metrics_filename, 'w', newline='')
    metrics_writer = csv.writer(metrics_file)
    metrics_writer.writerow(('lad_id', 'name', 'population', 'population_density', 'population_sum', prefix1 + 'year_2020', prefix2 + 'year_2020', prefix3 + 'year_2020', prefix1 + 'year_2021', prefix2 + 'year_2021', prefix3 + 'year_2021', prefix1 + 'year_2022', prefix2 + 'year_2022', prefix3 + 'year_2022', prefix1 + 'year_2023', prefix2 + 'year_2023', prefix3 + 'year_2023', prefix1 + 'year_2024', prefix2 + 'year_2024', prefix3 + 'year_2024', prefix1 + 'year_2025', prefix2 + 'year_2025', prefix3 + 'year_2025', prefix1 + 'year_2026', prefix2 + 'year_2026', prefix3 + 'year_2026', prefix1 + 'year_2027', prefix2 + 'year_2027', prefix3 + 'year_2027', prefix1 + 'year_2028', prefix2 + 'year_2028', prefix3 + 'year_2028', prefix1 + 'year_2029', prefix2 + 'year_2029', prefix3 + 'year_2029', prefix1 + 'year_2030', prefix2 + 'year_2030', prefix3 + 'year_2030'))

    for key, value in chart._table.items():
        metrics_writer.writerow((value[0], value[1], value[2], value[3], value[8], value[4][2020], value[5][2020], value[6][2020], value[4][2021], value[5][2021], value[6][2021], value[4][2022], value[5][2022], value[6][2022], value[4][2023], value[5][2023], value[6][2023], value[4][2024], value[5][2024], value[6][2024], value[4][2025], value[5][2025], value[6][2025], value[4][2026], value[5][2026], value[6][2026], value[4][2027], value[5][2027], value[6][2027], value[4][2028], value[5][2028], value[6][2028], value[4][2029], value[5][2029], value[6][2029], value[4][2030], value[5][2030], value[6][2030]))
    metrics_file.close()

    if ENABLE_SUB_PLOTS:
        # Maps
        print('- Drawing Chart 4 LADs...Total capacity during all years')
        maps.print_map_year_all(chart, "Total capacity per year", 4, TIMESTEPS, False, results, '4_1_capacity_per_year', suffix, 'Greens')
        print('- Drawing Chart 4 LADs...Total demand during all years')
        maps.print_map_year_all(chart, "Total demand per year", 5, TIMESTEPS, False, results, '4_2_demand_per_year', suffix, 'Reds')
        print('- Drawing Chart 4 LADs...Total population covered during all years')
        maps.print_map_year_all(chart, "Total population covered per year", 6, TIMESTEPS, True, results, '4_3_pop_covered_per_year', suffix, 'Greens')

   
def write_general_charts(ict_manager, results, RUN_OPTIONS, TIMESTEPS, OUTPUT_FOLDER):
    print('')
    print('GENERAL CHARTS PCDs...')

    option_number = 1
    for key, option in results.summary_graphs_combinations.items():
        print('')
        print('-> Printing option {}: {}'.format(option_number, key))
        print('- Plotting cost comparison per strategy')
        plots.plot_several_lines_population(ict_manager, results, option, TIMESTEPS, 8, 9, 5, 7, "Total cost", ['Population Covered', 'Cost (£)'], '{}_1_cost_comparison_per_strategy'.format(key))
        print('- Plotting % population covered comparison per strategy and year')
        plots.plot_several_lines_years(ict_manager, results, option, TIMESTEPS, 0, 4, "Population covered", ['Time', 'Population percentage'], True, '{}_2_population_covered_per_strategy'.format(key))
        print('- Plotting Capacity margin per strategy and year')
        plots.plot_several_lines_years(ict_manager, results, option, TIMESTEPS, 0, 6, "Capacity margin", ['Time', 'Capacity margin'], False, '{}_3_capacity_margin_per_strategy'.format(key))
        option_number += 1

    # print('- Saving gifs')
    # _save_gifs(results.gifs_filenames, results.output_path, 3)


def _save_gifs(filenames, output_path, duration):
    for key, values in filenames.items():
        metrics_filename = os.path.join(output_path, 'gifs', key + '.gif')
        images = []
        for filename in values:
            images.append(imageio.imread(filename))
        imageio.mimsave(metrics_filename, images, duration=duration)


# This function is copied in plot.py so when something is modified, it has to be modified there.
def _get_suffix(coverage_obligation_type, pop_scenario, throughput_scenario, coverage_scenario, intervention_strategy):
    suffix = '{}_pop_{}_throughput_{}_coverage_{}_strategy_{}_'.format(coverage_obligation_type, pop_scenario, throughput_scenario, coverage_scenario, intervention_strategy)
    # for length, use 'base' for baseline scenarios
    suffix = suffix.replace('baseline', 'base')
    return suffix
