"""
PLOT FUNCTION
"""
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.ticker as mtick
import os

def plot_chart(ict_manager, results, chart, col_pop, col_pop_agg, col_value, col_value_agg, title, ax_names, name, index):
    metrics_filename = os.path.join(results.output_path, 'figures', name + '_' + index)
    
    fig = plt.figure(figsize=(8,8)) # Notice the equal aspect ratio
    fig.suptitle(title)
    ax = fig.subplots()
    ax.set_xlabel(ax_names[0])
    ax.set_ylabel(ax_names[1])
    
    if(True): 
        x_values, y_values = _get_axis_values(1000, col_pop, col_pop_agg, col_value, col_value_agg, results, chart)
        ax.plot(x_values, y_values)
    else:
        x_values = [value[0] for key,value in chart._table.items()]
        y_values = [value[col_value_agg] for key,value in chart._table.items()]
        ax.plot(np.arange(len(x_values)), y_values)
        ax.set_xticklabels(x_values)

    fmt = '%.0f%%' # Format you want the ticks, e.g. '40%'
    xticks = mtick.FormatStrFormatter(fmt)
    ax.xaxis.set_major_formatter(xticks)
    
    fig.tight_layout(rect=[0, 0.03, 1, 0.95])
    
#    fig.savefig(metrics_filename + '.pdf', dpi=1000)
    fig.savefig(metrics_filename + '.svg', format='svg', dpi=1200)
    
#    plt.show()    
    plt.close(fig)

    
def plot_chart_comparison(ict_manager, results, chart, pop_sum, columns, title, ax_names, name, index):
    
    metrics_filename = os.path.join(results.output_path, 'figures', name + '_' + index)
    
    fig = plt.figure(figsize=(8,8)) # Notice the equal aspect ratio
    fig.suptitle(title)
    axlist = [fig.add_subplot(len(columns),1,i+1) for i in range(len(columns))]
        
    # TODO: Modify X axis values to fit population increment  
    
    column_number = 0
    for column in columns:
        ax = axlist[column_number]

        x_elements = [value[0] for key,value in chart._table.items()]
        y_values = [value[column] for key,value in chart._table.items()]
        x_values = np.linspace(0,100,len(x_elements))
        
        ax.set_xlabel(ax_names[0])
        ax.set_ylabel(ax_names[column_number + 1])
        
        ax.plot(x_values, y_values, color='b', linewidth=1/3)

#        ax.set_xticklabels(x_values)
        column_number += 1
        
    fmt = '%.0f%%' # Format you want the ticks, e.g. '40%'
    xticks = mtick.FormatStrFormatter(fmt)
    ax.xaxis.set_major_formatter(xticks) 
    
    fig.tight_layout(rect=[0, 0.03, 1, 0.95])
    
#    fig.savefig(metrics_filename + '.pdf', dpi=1000)
    fig.savefig(metrics_filename + '.svg', format='svg', dpi=1200)
    
#    plt.show()    
    plt.close(fig)
    
def plot_chart_per_year(ict_manager, results, chart, pop_sum, columns, timesteps, title, ax_names, name, index):
    metrics_filename = os.path.join(results.output_path, 'figures', name + '_' + index)
    
    fig = plt.figure(figsize=(8,8)) # Notice the equal aspect ratio
    fig.suptitle(title)
    axlist = [fig.add_subplot(6,2,i+1) for i in range(len(timesteps))]
        
    column_number = 0
    for year in timesteps:
        ax = axlist[year-timesteps[0]]

        y_values = [value[columns[0]][year] for key,value in chart._table.items()]
        
        ax.set_xlabel(ax_names[0])
        ax.set_ylabel(str(year))
        
        x_elements = [value[0] for key,value in chart._table.items()]  
        x_values = np.linspace(0,100,len(x_elements))
                
        ax.plot(x_values, y_values, color='b', linewidth=1/3)

#        ax.set_xticklabels(x_values)
        column_number += 1
    
    fmt = '%.0f%%' # Format you want the ticks, e.g. '40%'
    xticks = mtick.FormatStrFormatter(fmt)
    ax.xaxis.set_major_formatter(xticks)
    
    fig.tight_layout(rect=[0, 0.03, 1, 0.95])
    
#    fig.savefig(metrics_filename + '.pdf', dpi=1000)
    fig.savefig(metrics_filename + '.svg', format='svg')
    
#    plt.show()    
    plt.close(fig)
    
    
def plot_several_lines(ict_manager, results, RUN_OPTIONS, TIMESTEPS, table_name, col_pop, col_pop_agg, col_value, col_value_agg, title, ax_names, name):
    metrics_filename = os.path.join(results.output_path, 'figures/summary', name)
    
    # Set Axis and Title
    fig = plt.figure()
    ax = plt.subplot(111)
    
    ax.set_xlabel(ax_names[0])
    ax.set_ylabel(ax_names[1])
    ax.set_title(title)
    
    # Create the X axis according to the population of the first option
#    if(table_name == 'chart1_pcd'):
    chart = results.chart1_get_table(_get_suffix(RUN_OPTIONS[0][3],RUN_OPTIONS[0][0],RUN_OPTIONS[0][1],RUN_OPTIONS[0][2],RUN_OPTIONS[0][4]))
#    elif (table_name == 'chart1_lad'):
#        chart = results.chart1_lads_get_table(_get_suffix(RUN_OPTIONS[0][3],RUN_OPTIONS[0][0],RUN_OPTIONS[0][1],RUN_OPTIONS[0][2],RUN_OPTIONS[0][4]))
#    else:
#        chart = results.chart1_get_table(_get_suffix(RUN_OPTIONS[0][3],RUN_OPTIONS[0][0],RUN_OPTIONS[0][1],RUN_OPTIONS[0][2],RUN_OPTIONS[0][4]))

    
    for pop_scenario, throughput_scenario, coverage_scenario, coverage_obligation_type, intervention_strategy  in RUN_OPTIONS:
        index = _get_suffix(coverage_obligation_type, pop_scenario, throughput_scenario, coverage_scenario, intervention_strategy)
        nice_index = _get_nice_index(coverage_obligation_type, pop_scenario, throughput_scenario, coverage_scenario, intervention_strategy)
#        if(table_name == 'chart1_pcd'):
        chart = results.chart1_get_table(index)
#        elif (table_name == 'chart1_lad'):
#            chart = results.chart1_lads_get_table(index)
#        else:
#            chart = results.chart1_get_table(index)
        
#        y_values = [value[7] for key,value in chart._table.items()]
        
        x_values, y_values = _get_axis_values(1000, col_pop, col_pop_agg, col_value, col_value_agg, results, chart, coverage_obligation_type)

        ax.plot(x_values, y_values, label=nice_index)
        
        
    # Plot the chart until 100%
    y_values = np.linspace(0,results.population_2020,1000)
    x_values = np.linspace(0,100,1000)
    ax.plot(x_values, y_values, alpha=0)
        
    fmt = '%.0f%%' # Format you want the ticks, e.g. '40%'
    xticks = mtick.FormatStrFormatter(fmt)
    ax.xaxis.set_major_formatter(xticks)
#    fig.tight_layout()
#    fig.tight_layout(rect=[0, 0.03, 1, 0.95])
#    fig.subplots_adjust(top=0.85)
    
    # Shrink current axis's height by 50% on the bottom
    box = ax.get_position()
    ax.set_position([box.x0, box.y0 + box.height * 0.5, box.width, box.height * 0.5])
    
#    ax.legend(bbox_to_anchor=(1.05, 1), loc=2, borderaxespad=0.)
    plt.legend(loc='upper center', bbox_to_anchor=(0.5, -0.20),
           handletextpad=0.0, fancybox=True, shadow=True, fontsize='small')
#    fig.savefig(metrics_filename + '.pdf', dpi=1000)
    fig.savefig(metrics_filename + '.svg', format='svg', dpi=1200)
    
#    plt.show()    
    plt.close(fig)


def _get_axis_values(plot_points, col_pop, col_pop_agg, col_value, col_value_agg, results, chart, c_o_type = None):
    
    y_limits = np.linspace(0,results.population_2020,plot_points)
    y_values = [] # La lista que voy a rellenar con los puntos Y. Tendrá la misma dimensión que y_limits
  
    
    
#    not_reached = 0
    for pop_limit in y_limits: # Relleno y_values buscando en los límites uno a uno.
        previous_item = None # Cuando me pase en la comparación de población miro el anterior pcd porque ese es el que me interesará.
        for key, value in chart._table.items(): # Miro a ver qué pcd se pasa para coger el anterior
            if value[col_pop_agg] >= pop_limit: # Si con este pcd supero un límite, cojo el pcd anterior(previoues_pcd)
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
    print ("This is the limit: {}, {}".format (len(y_values),len(y_limits)))
    
    x_values = np.linspace(0, 100 * (len(y_values) / len(y_limits)), len(y_values))
    
    return x_values, y_values


# This function is copied in plot.py so when something is modified, it has to be modified there.
def _get_suffix(coverage_obligation_type, pop_scenario, throughput_scenario, coverage_scenario, intervention_strategy):
    suffix = '{}_pop_{}_throughput_{}_coverage_{}_strategy_{}_'.format(coverage_obligation_type, pop_scenario, throughput_scenario, coverage_scenario, intervention_strategy)
    # for length, use 'base' for baseline scenarios
    suffix = suffix.replace('baseline', 'base')
    return suffix

def _get_nice_index(coverage_obligation_type, pop_scenario, throughput_scenario, coverage_scenario, intervention_strategy):
    
    dict_cov_ob = {'cov_ob_1': 'Custom', 'cov_ob_2': 'France', 'cov_ob_3': 'Germany', 'cov_ob_4': 'Spain', 'cov_ob_5': 'The UK'}
    dict_cov_ob_speed = {'low': '2 mbps', 'baseline': '5 mbps', 'high': '8 mbps'}
    suffix = '{}, Pop: {}, Throughput: {}, C.O.: {}, Strategy: {}'.format(dict_cov_ob.get(coverage_obligation_type,'new obligation'), pop_scenario, throughput_scenario, dict_cov_ob_speed.get(coverage_scenario, 'X mbps'), intervention_strategy)
    # for length, use 'base' for baseline scenarios
    suffix = suffix.replace('baseline', 'medium')
    return suffix
    