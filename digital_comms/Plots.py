"""
PLOT FUNCTION
"""

import numpy as np
import matplotlib.pyplot as plt
#import time
#import matplotlib.colors as colors
#from matplotlib.figure import Figure
import os
#from itertools import accumulate


def plot_chart(chart, title, columns, output_path, name, index):
    
#    Based on: https://matplotlib.org/gallery/statistics/barchart_demo.html
    metrics_filename = os.path.join(output_path, 'figures', name + '_' + index)
    
    fig, ax = plt.subplots()
    
    ax.set_xlabel('LADs')
    ax.set_ylabel('Population')
    ax.set_title(title)
    
    x_values = [value[0] for key,value in chart._table.items()]
    y_values = [value[columns[1]] for key,value in chart._table.items()]
    
    step_100_y = max([value[columns[0]] for key,value in chart._table.items()])
        
    step_25_x = [key for key,value in chart._table.items() if value[columns[0]] > (step_100_y * 1 / 4)][0]
    step_50_x = [key for key,value in chart._table.items() if value[columns[0]] > (step_100_y * 2 / 4)][0]
    step_75_x = [key for key,value in chart._table.items() if value[columns[0]] > (step_100_y * 3 / 4)][0]    
    
    ax.title.set_text(title)
    bar_width = 1/1.5
    opacity = 1

    ax.bar(np.arange(len(x_values)), y_values,alpha=opacity, color='b', linewidth=1/3)
    
    ax.annotate('25%', xy=(list(chart._table.keys()).index(step_25_x), max(y_values)/2), xytext=(list(chart._table.keys()).index(step_25_x), max(y_values)/2 + max(y_values)/10),arrowprops=dict(facecolor='black', arrowstyle="->"),) #, shrink=0.05
    ax.annotate('50%', xy=(list(chart._table.keys()).index(step_50_x), max(y_values)/2), xytext=(list(chart._table.keys()).index(step_50_x), max(y_values)/2 + max(y_values)/10),arrowprops=dict(facecolor='black', arrowstyle="->"),)
    ax.annotate('75%', xy=(list(chart._table.keys()).index(step_75_x), max(y_values)/2), xytext=(list(chart._table.keys()).index(step_75_x), max(y_values)/2 + max(y_values)/10),arrowprops=dict(facecolor='black', arrowstyle="->"),)

    ax.set_xticklabels(x_values)
#    fig.tight_layout()
    fig.tight_layout(rect=[0, 0.03, 1, 0.95])
#    fig.subplots_adjust(top=0.85)
    
    fig.savefig(metrics_filename + '.pdf', dpi=1000)
    fig.savefig(metrics_filename + '.svg', format='svg', dpi=1200)
    
#    plt.show()    
    plt.close(fig)
    
    
    
def plot_chart_comparison(chart, title, subtitles, columns, output_path, name, index):
    
#    Based on: https://matplotlib.org/gallery/statistics/barchart_demo.html
    metrics_filename = os.path.join(output_path, 'figures', name + '_' + index)
    
    fig = plt.figure(figsize=(8,8)) # Notice the equal aspect ratio
    fig.suptitle(title)
    axlist = [fig.add_subplot(len(columns)-1,1,i+1) for i in range(len(columns)-1)]
        
    step_100_y = max([value[columns[0]] for key,value in chart._table.items()]) #
        
    step_25_x = [key for key,value in chart._table.items() if value[columns[0]] > (step_100_y * 1 / 4)][0]
    step_50_x = [key for key,value in chart._table.items() if value[columns[0]] > (step_100_y * 2 / 4)][0]
    step_75_x = [key for key,value in chart._table.items() if value[columns[0]] > (step_100_y * 3 / 4)][0]
    
    column_number = 0
    for column in columns[1:]:
        ax = axlist[column_number]

        x_values = [value[0] for key,value in chart._table.items()]
        y_values = [value[column] for key,value in chart._table.items()]
        
        ax.set_xlabel(subtitles[0])
        ax.set_ylabel(subtitles[column_number + 1])
        
        bar_width = 1/1.5
        opacity = 1
        
        ax.plot(np.arange(len(x_values)), y_values,alpha=opacity, color='b', linewidth=1/3)
        
        if column == 6 or column == 7: #Aggregated cost and population
    
            ax.annotate('25%', xy=(list(chart._table.keys()).index(step_25_x), chart.get_value(step_25_x)[column]), xytext=(list(chart._table.keys()).index(step_25_x), chart.get_value(step_25_x)[column] + max(y_values)/10),arrowprops=dict(facecolor='black', arrowstyle="->"),)
            ax.annotate('50%', xy=(list(chart._table.keys()).index(step_50_x), chart.get_value(step_50_x)[column]), xytext=(list(chart._table.keys()).index(step_50_x), chart.get_value(step_50_x)[column] + max(y_values)/10),arrowprops=dict(facecolor='black', arrowstyle="->"),)
            ax.annotate('75%', xy=(list(chart._table.keys()).index(step_75_x), chart.get_value(step_75_x)[column]), xytext=(list(chart._table.keys()).index(step_75_x), chart.get_value(step_75_x)[column] + max(y_values)/10),arrowprops=dict(facecolor='black', arrowstyle="->"),)
        
        else:   
            ax.annotate('25%', xy=(list(chart._table.keys()).index(step_25_x), max(y_values)/2), xytext=(list(chart._table.keys()).index(step_25_x), max(y_values)/2 + max(y_values)/10),arrowprops=dict(facecolor='black', arrowstyle="->"),)
            ax.annotate('50%', xy=(list(chart._table.keys()).index(step_50_x), max(y_values)/2), xytext=(list(chart._table.keys()).index(step_50_x), max(y_values)/2 + max(y_values)/10),arrowprops=dict(facecolor='black', arrowstyle="->"),)
            ax.annotate('75%', xy=(list(chart._table.keys()).index(step_75_x), max(y_values)/2), xytext=(list(chart._table.keys()).index(step_75_x), max(y_values)/2 + max(y_values)/10),arrowprops=dict(facecolor='black', arrowstyle="->"),)
        
        ax.set_xticklabels(x_values)
        column_number += 1
    
#    fig.tight_layout()
    fig.tight_layout(rect=[0, 0.03, 1, 0.95])
#    fig.subplots_adjust(top=0.85)
    
    fig.savefig(metrics_filename + '.pdf', dpi=1000)
    fig.savefig(metrics_filename + '.svg', format='svg', dpi=1200)
    
#    plt.show()    
    plt.close(fig)
    
    
def plot_chart_per_year(chart, title, columns, timesteps, output_path, name, index):
#    start_time = time.time()
#    Based on: https://matplotlib.org/gallery/statistics/barchart_demo.html
    metrics_filename = os.path.join(output_path, 'figures', name + '_' + index)
    
    fig = plt.figure(figsize=(8,8)) # Notice the equal aspect ratio
    fig.suptitle(title)
    axlist = [fig.add_subplot(6,2,i+1) for i in range(len(timesteps))]
    
    titles = ['LADs', 'Population', 'Cost']
    
    step_100_y = max([value[columns[0]] for key,value in chart._table.items()]) #
        
    step_25_x = [key for key,value in chart._table.items() if value[columns[0]] > (step_100_y * 1 / 4)][0]
    step_50_x = [key for key,value in chart._table.items() if value[columns[0]] > (step_100_y * 2 / 4)][0]
    step_75_x = [key for key,value in chart._table.items() if value[columns[0]] > (step_100_y * 3 / 4)][0]
#    
#    time2 = time.time()
#    print (str(time2 - start_time))
    
    x_values = [value[0] for key,value in chart._table.items()]
    x_numbers = np.arange(len(x_values))

    column_number = 0
    for year in timesteps:
#        time2 = time.time()
#        print ("1: " + str(time2))
        ax = axlist[year-timesteps[0]]

        y_values = [value[columns[1]][year] for key,value in chart._table.items()]
        
        ax.set_xlabel(titles[0])
        ax.set_ylabel(str(year))
                
#        time3 = time.time()
#        print ("2: " + str(time3 - time2))
        ax.plot(x_numbers, y_values, color='b', linewidth=1/3)
#        time4 = time.time()
#        print ("3: " + str(time4 - time3))
        if columns[1] == 6 or columns[1] == 7: #Aggregated cost and population
    
            ax.annotate('25%', xy=(list(chart._table.keys()).index(step_25_x), chart.get_value(step_25_x)[columns[1]][year]), xytext=(list(chart._table.keys()).index(step_25_x), chart.get_value(step_25_x)[columns[1]][year] + max(y_values)/10),arrowprops=dict(facecolor='black', arrowstyle="->"),)
            ax.annotate('50%', xy=(list(chart._table.keys()).index(step_50_x), chart.get_value(step_50_x)[columns[1]][year]), xytext=(list(chart._table.keys()).index(step_50_x), chart.get_value(step_50_x)[columns[1]][year] + max(y_values)/10),arrowprops=dict(facecolor='black', arrowstyle="->"),)
            ax.annotate('75%', xy=(list(chart._table.keys()).index(step_75_x), chart.get_value(step_75_x)[columns[1]][year]), xytext=(list(chart._table.keys()).index(step_75_x), chart.get_value(step_75_x)[columns[1]][year] + max(y_values)/10),arrowprops=dict(facecolor='black', arrowstyle="->"),)
        
        else:   
            ax.annotate('25%', xy=(list(chart._table.keys()).index(step_25_x), max(y_values)/2), xytext=(list(chart._table.keys()).index(step_25_x), max(y_values)/2 + max(y_values)/10),arrowprops=dict(facecolor='black', arrowstyle="->"),)
            ax.annotate('50%', xy=(list(chart._table.keys()).index(step_50_x), max(y_values)/2), xytext=(list(chart._table.keys()).index(step_50_x), max(y_values)/2 + max(y_values)/10),arrowprops=dict(facecolor='black', arrowstyle="->"),)
            ax.annotate('75%', xy=(list(chart._table.keys()).index(step_75_x), max(y_values)/2), xytext=(list(chart._table.keys()).index(step_75_x), max(y_values)/2 + max(y_values)/10),arrowprops=dict(facecolor='black', arrowstyle="->"),)
        
        ax.set_xticklabels(x_values)
        column_number += 1
    
#    fig.tight_layout()
    fig.tight_layout(rect=[0, 0.03, 1, 0.95])
#    fig.subplots_adjust(top=0.85)
    
    fig.savefig(metrics_filename + '.pdf', dpi=1000)
    fig.savefig(metrics_filename + '.svg', format='svg')
    
#    plt.show()    
    plt.close(fig)

