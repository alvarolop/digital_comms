"""
PLOT FUNCTION
"""
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.ticker as mtick

from collections import OrderedDict
import os


def plot_chart(ict_manager, results, chart, col_pop, col_pop_agg, col_value, col_value_agg, title, ax_names, name, index):
    metrics_filename = os.path.join(results.output_path, 'figures', name + '_' + index)
    
    fig = plt.figure(figsize=(8, 8))  # Notice the equal aspect ratio
    ax = fig.subplots()
    ax.set_title(title)
    ax.set_xlabel(ax_names[0])
    ax.set_ylabel(ax_names[1])
    ax.grid(True)

    x_values, y_values = _get_axis_values(1000, col_pop, col_pop_agg, col_value, col_value_agg, results, chart)
    ax.plot(x_values, y_values)

    # Plot the chart until 100%
    y_values = np.linspace(0, results.population_2020, 1000)
    x_values = np.linspace(0, 100, 1000)
    ax.plot(x_values, y_values, alpha=0)

    ax.xaxis.set_major_formatter(mtick.FormatStrFormatter('%.0f%%'))
    fig.tight_layout(rect=[0, 0.03, 1, 0.95])
    
    fig.savefig(metrics_filename + '.svg', format='svg', dpi=1200)
    plt.close(fig)


def plot_years(ict_manager, results, chart, TIMESTEPS, col_time, col_value, title, ax_names, type, name, index, col_demand=-1):
    metrics_filename = os.path.join(results.output_path, 'figures', name + '_' + index)
    fig = plt.figure()
    ax = plt.subplot(111)

    ax.set_xlabel(ax_names[0])
    ax.set_ylabel(ax_names[1])
    ax.set_title(title)
    ax.grid(True)

    if type == 'Percentage':
        y_values = [value[col_value] * 100 for key, value in chart._table.items()]
        x_values = [value[col_time] for key, value in chart._table.items()]
    # elif type == 'Thi_no_important':
        # x_values, y_values = _get_axis_values(1000, col_pop, col_pop_agg, col_value, col_value_agg, results, chart, coverage_obligation_type)
    else:
        y_values = [value[col_value] for key, value in chart._table.items()]
        x_values = [value[col_time] for key, value in chart._table.items()]

    # Print a vertical line when cover demand starts
    if col_demand > 0:
        year_start_invest_demand = 0
        for key, value in chart._table.items():
            if value[col_demand] == 1:
                year_start_invest_demand = value[col_time]
                break
        if year_start_invest_demand > 0:
            plt.axvline(x=year_start_invest_demand, color='g')

    ax.plot(x_values, y_values)

    if type == 'Cost':
        # Homogenize plotting of costs
        y_values = np.linspace(0, 6 * 10 ** 8, 11)
        x_values = np.linspace(2020, 2030, 11)
        ax.plot(x_values, y_values, alpha=0)

    elif type == 'Percentage':
        ax.yaxis.set_major_formatter(mtick.FormatStrFormatter('%.0f%%'))
        # Homogenize plotting of population covered
        y_values = np.linspace(30, 100, 11)
        x_values = np.linspace(2020, 2030, 11)
        ax.plot(x_values, y_values, alpha=0)
    else:
        # Homogenize plotting of cap margin
        y_values = np.linspace(-50, 150, 11)
        x_values = np.linspace(2020, 2030, 11)
        ax.plot(x_values, y_values, alpha=0)

    fig.savefig(metrics_filename + '.svg', format='svg', dpi=100)
    plt.close(fig)

    
def plot_chart_comparison(ict_manager, results, chart, pop_sum, columns, title, ax_names, name, index):
    
    metrics_filename = os.path.join(results.output_path, 'figures', name + '_' + index)
    
    fig = plt.figure(figsize=(8,8)) # Notice the equal aspect ratio
    fig.suptitle(title)
    axlist = [fig.add_subplot(len(columns), 1, i+1) for i in range(len(columns))]
        
    # TODO: Modify X axis values to fit population increment  
    
    column_number = 0
    for column in columns:
        ax = axlist[column_number]
        ax.grid(True)

        x_elements = [value[0] for key,value in chart._table.items()]
        y_values = [value[column] for key,value in chart._table.items()]
        x_values = np.linspace(0, 100, len(x_elements))
        
        ax.set_xlabel(ax_names[0])
        ax.set_ylabel(ax_names[column_number + 1])
        
        ax.plot(x_values, y_values, color='b', linewidth=1/3)
        column_number += 1
        
    ax.xaxis.set_major_formatter(mtick.FormatStrFormatter('%.0f%%'))
    # fig.tight_layout(rect=[0, 0.03, 1, 0.95])
    
    fig.savefig(metrics_filename + '.svg', format='svg', dpi=1200)
    plt.close(fig)
    
def plot_chart_per_year(ict_manager, results, chart, pop_sum, columns, timesteps, title, ax_names, name, index):
    metrics_filename = os.path.join(results.output_path, 'figures', name + '_' + index)
    
    fig = plt.figure(figsize=(8, 8))  # Notice the equal aspect ratio
    fig.suptitle(title)
    axlist = [fig.add_subplot(6, 2, i+1) for i in range(len(timesteps))]

    column_number = 0
    for year in timesteps:
        ax = axlist[year-timesteps[0]]
        ax.grid(True)
        y_values = [value[columns[0]][year] for key, value in chart._table.items()]
        
        ax.set_xlabel(ax_names[0])
        ax.set_ylabel(str(year))
        
        x_elements = [value[0] for key, value in chart._table.items()]
        x_values = np.linspace(0, 100, len(x_elements))
                
        ax.plot(x_values, y_values, color='b', linewidth=1/3)
        column_number += 1

    ax.xaxis.set_major_formatter(mtick.FormatStrFormatter('%.0f%%'))
    fig.tight_layout(rect=[0, 0.03, 1, 0.95])
    
    fig.savefig(metrics_filename + '.svg', format='svg')
    plt.close(fig)


def plot_chart_detail_per_year(ict_manager, results, chart, pop_sum, columns, timesteps, title, ax_names, name, index):
    for year in timesteps:
        metrics_filename = os.path.join(results.output_path, 'figures/detail_per_year', name + '_' + str(year) + '_' + index)

        fig = plt.figure(figsize=(8, 8))  # Notice the equal aspect ratio
        fig.suptitle(title.format(str(year)))
        ax = fig.subplots()
        ax.set_xlabel(ax_names[0])
        ax.set_ylabel(ax_names[1])
        ax.grid(True)

        y_values = [value[columns[0]][year] for key, value in chart._table.items()]

        x_elements = [value[0] for key, value in chart._table.items()]
        x_values = np.linspace(0, len(x_elements), len(x_elements))

        ax.plot(x_values, y_values, color='b', linewidth=1 / 3)

        fig.tight_layout(rect=[0, 0.03, 1, 0.95])

        fig.savefig(metrics_filename + '.svg', format='svg')
        plt.close(fig)


def plot_histogram(ict_manager, results, chart, TIMESTEPS, cumulative, hist_type, col_value, title, ax_names, name, index):
    metrics_filename = os.path.join(results.output_path, 'figures', name + '_' + index)

    fig = plt.figure(figsize=(8, 8))  # Notice the equal aspect ratio
    ax = fig.subplots()

    ax.set_xlabel(ax_names[0])
    ax.set_ylabel(ax_names[1])
    ax.set_title(title)
    ax.grid(True)

    if cumulative:
        alpha = 1
        linewidth = 2.0
        histtype = 'step'
    else:
        alpha = 1
        linewidth = 2.0
        histtype = 'bar'

    if hist_type == 'Capacity':
        values = [value[col_value][2030] for key, value in chart._table.items()]
        n, bins, patches = plt.hist(values, bins=100, range=(results.cap_margin_bounds_plot[0], results.cap_margin_bounds_plot[1]),
                                density=True, cumulative=cumulative, alpha=alpha, linewidth=linewidth, histtype=histtype)
        if cumulative:
            yformatter = mtick.FuncFormatter(lambda v, pos: '{:3.0f}%'.format(v * 100))
            ax.yaxis.set_major_formatter(yformatter)
        else:
            yformatter = mtick.FuncFormatter(lambda v, pos: '{:3.2f}%'.format(v * 100))
            ax.yaxis.set_major_formatter(yformatter)

    elif hist_type == 'Percentage':
        values = [value[col_value][2030] * 100 for key, value in chart._table.items()]
        n, bins, patches = plt.hist(values, bins=100, range=(0, 100), density=True, cumulative=cumulative, alpha=alpha, linewidth=linewidth, histtype=histtype)
        xformatter = mtick.FormatStrFormatter('%.0f%%')
        ax.xaxis.set_major_formatter(xformatter)
        yformatter = mtick.FuncFormatter(lambda v, pos: '{:3.0f}%'.format(v * 100))
        ax.yaxis.set_major_formatter(yformatter)

    fig.savefig(metrics_filename + '.svg', format='svg', dpi=1200)
    plt.close(fig)


def plot_several_lines_population(ict_manager, results, RUN_OPTIONS, TIMESTEPS, col_pop, col_pop_agg, col_value, col_value_agg, title, ax_names, name):
    metrics_filename = os.path.join(results.output_path, 'figures/summary', name)
    
    # Set Axis and Title
    fig = plt.figure()
    ax = plt.subplot(111)
    
    ax.set_xlabel(ax_names[0])
    ax.set_ylabel(ax_names[1])
    ax.set_title(title)
    ax.grid(True)

    for pop_scenario, throughput_scenario, coverage_scenario, coverage_obligation_type, intervention_strategy  in RUN_OPTIONS:
        index = _get_suffix(coverage_obligation_type, pop_scenario, throughput_scenario, coverage_scenario, intervention_strategy)
        nice_index = _get_nice_index(coverage_obligation_type, pop_scenario, throughput_scenario, coverage_scenario, intervention_strategy, results)
        
        chart = results.chart1_get_table(index)
        x_values, y_values = _get_axis_values(1000, col_pop, col_pop_agg, col_value, col_value_agg, results, chart, coverage_obligation_type)
        ax.plot(x_values, y_values, label=nice_index)
        
    # Plot the chart until 100%
    y_values = np.linspace(0, results.population_2020, 1000)
    x_values = np.linspace(0, 100, 1000)
    ax.plot(x_values, y_values, alpha=0)

    ax.xaxis.set_major_formatter(mtick.FormatStrFormatter('%.0f%%'))
    
    # Shrink current axis's height by 50% on the bottom
    box = ax.get_position()
    ax.set_position([box.x0, box.y0 + box.height * 0.5, box.width, box.height * 0.5])
    
    plt.legend(loc='upper center', bbox_to_anchor=(0.5, -0.20),
           handletextpad=0.0, fancybox=True, shadow=True, fontsize='x-small')

    fig.savefig(metrics_filename + '.svg', format='svg', dpi=1200)
    plt.close(fig)
    
    
def plot_several_lines_years(ict_manager, results, run_options, TIMESTEPS, col_time, col_value, title, ax_names, y_percentage_boolean, name):
    metrics_filename = os.path.join(results.output_path, 'figures/summary', name)
    
    # Set Axis and Title
    fig = plt.figure()
    ax = plt.subplot(111)
    
    ax.set_xlabel(ax_names[0])
    ax.set_ylabel(ax_names[1])
    ax.set_title(title)
    ax.grid(True)
    
    for pop_scenario, throughput_scenario, coverage_scenario, coverage_obligation_type, intervention_strategy  in run_options:
        index = _get_suffix(coverage_obligation_type, pop_scenario, throughput_scenario, coverage_scenario, intervention_strategy)
        nice_index = _get_nice_index(coverage_obligation_type, pop_scenario, throughput_scenario, coverage_scenario, intervention_strategy, results)
        chart = results.chart5_get_table(index)

        if y_percentage_boolean:
            y_values = [value[col_value] * 100 for key, value in chart._table.items()]
        else:
            y_values = [value[col_value] for key, value in chart._table.items()]
        x_values = [value[col_time] for key, value in chart._table.items()]
        ax.plot(x_values, y_values, label=nice_index)
    
    if y_percentage_boolean:
        ax.yaxis.set_major_formatter(mtick.FormatStrFormatter('%.0f%%'))
    
    # Shrink current axis's height by 50% on the bottom
    box = ax.get_position()
    ax.set_position([box.x0, box.y0 + box.height * 0.5, box.width, box.height * 0.5])
    
    plt.legend(loc='upper center', bbox_to_anchor=(0.5, -0.20),
           handletextpad=0.0, fancybox=True, shadow=True, fontsize='x-small')
    
    fig.savefig(metrics_filename + '.svg', format='svg', dpi=1200)
    plt.close(fig)


def _get_axis_values(plot_points, col_pop, col_pop_agg, col_value, col_value_agg, results, chart, c_o_type = None):
    
    y_limits = np.linspace(0,results.population_2020,plot_points)
    y_values = [] # La lista que voy a rellenar con los puntos Y. Tendrá la misma dimensión que y_limits
  
    # Fill with zeros the population covered in 2020
    
#    not_reached = 0
    for pop_limit in y_limits: # Relleno y_values buscando en los límites uno a uno.
        previous_item = None # Cuando me pase en la comparación de población miro el anterior pcd porque ese es el que me interesará.
        for key, value in chart._table.items(): # Miro a ver qué pcd se pasa para coger el anterior
            if (value[col_pop_agg] >= pop_limit and value[col_pop] > 0): # Si con este pcd supero un límite, cojo el pcd anterior(previoues_pcd)
                if previous_item == None:
                    pop_to_limit = pop_limit # Como el primer límite se cumple en el primer pcd, solo hay que coger el limite de población
                    cost = value[col_value] * pop_to_limit / value[col_pop] # %población para llegar al límite por el costePCD [5]
                    y_values.append(cost)
                    break # Solo relleno un y_value cada vez que recorro los pcds. Cuando lo tenga vuelvo a empezar
                else:
                    pop_to_limit = pop_limit - previous_item[col_pop_agg] # Diferencia de población entre el límite y todos los pcd anteriores
                    cost = previous_item[col_value_agg] + value[col_value] * pop_to_limit / value[col_pop] # Agregado[7] del anterior + %población para llegar al límite * costePCD[5]
                    y_values.append(cost)
                    break # Solo relleno un y_value cada vez que recorro los pcds. Cuando lo tenga vuelvo a empezar
            previous_item = value
#                    not_reached += 1
    option = 2 
    if option == 1: # This option keeps the order of the excel. Investment starts in 0%
        y_values_set = list(OrderedDict.fromkeys(y_values))
#        print ("This is the limit: {}, {}, {}".format (len(y_values_set), len(y_values), len(y_limits)))
        x_values = np.linspace(0, 100 * (len(y_values) / len(y_limits)), len(y_values))
    elif option == 2: # This option takes into account the previous capacity 
        y_values_set = list(OrderedDict.fromkeys(y_values))
#        print ("This is the limit: {}, {}, {}".format (len(y_values_set), len(y_values), len(y_limits)))
        number_of_zeros = len(y_values) - len(y_values_set)
        y_values_zeros = [0] * number_of_zeros
        y_values = y_values_zeros + y_values_set
        x_values = np.linspace(0, 100 * (len(y_values) / len(y_limits)), len(y_values))
    return x_values, y_values


# This function is copied in plot.py so when something is modified, it has to be modified there.
def _get_suffix(coverage_obligation_type, pop_scenario, throughput_scenario, coverage_scenario, intervention_strategy):
    suffix = '{}_pop_{}_throughput_{}_coverage_{}_strategy_{}_'.format(coverage_obligation_type, pop_scenario, throughput_scenario, coverage_scenario, intervention_strategy)
    # for length, use 'base' for baseline scenarios
    suffix = suffix.replace('baseline', 'base')
    return suffix


def _get_nice_index(coverage_obligation_type, pop_scenario, throughput_scenario, coverage_scenario, intervention_strategy, results):
    suffix = '{}, Pop: {}, Demand: {}, C.O.: {}mbps, Strategy: {}'.format\
        (results.co_name.get(coverage_obligation_type, 'New obligation'),
         pop_scenario,
         throughput_scenario,
         results.co_coverage_obligation.get(coverage_scenario, 'X'),
         results.strategy_name.get(intervention_strategy, 'New strategy'))

    # For length, use 'base' for baseline scenarios
    suffix = suffix.replace('baseline', 'medium')
    return suffix
