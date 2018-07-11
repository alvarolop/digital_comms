"""
MAP FUNCTION
This code is based on this links:
    https://chrishavlin.wordpress.com/2016/11/16/shapefiles-tutorial/
    https://pythonhosted.org/Python%20Shapefile%20Library/
    https://matplotlib.org/api/_as_gen/matplotlib.pyplot.fill.html


Color palette code:
    https://stackoverflow.com/questions/15968762/shapefile-and-matplotlib-plot-polygon-collection-of-shapefile-coordinates

All the color palettes:
    https://matplotlib.org/1.4.3/examples/color/colormaps_reference.html

This is another way of doing it:
    http://basemaptutorial.readthedocs.io/en/latest/shapefile.html
"""
import shapefile
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.colors as colors
import os
import collections


def print_map(chart, title, column, results, name, index, colormap):
    sf = shapefile.Reader(results.shapefile_path)
    metrics_filename = os.path.join(results.output_path, 'maps', name + '_' + index)

#    print(repr(chart._table.keys()))
    if not results.co_descending_order:
        chart._table = collections.OrderedDict(reversed(list(chart._table.items())))
    else:
        chart._table = chart._table
#    print(repr(results.co_descending_order) + repr(chart.keys()))

    fig = plt.figure()
    ax = fig.add_subplot(1, 1, 1)

    ax.set_aspect('equal')
    ax.title.set_text(title)
    ax.get_xaxis().set_visible(False)
    ax.get_yaxis().set_visible(False)

    # Select the color map from: https://matplotlib.org/examples/color/colormaps_reference.html
    palette = plt.get_cmap(colormap) #Add _r at the end to get the inverse color map (autumn)

    # Get max and min value for the color map:
    max_value = max([i[column] for i in chart.table.values()])
    min_value = min([i[column] for i in chart.table.values()])
    norm = colors.Normalize(vmin=min_value, vmax=max_value)

    for sr in sf.iterShapeRecords(): #For each LAD of the shapefile: shape (geometry) and record (information)
        color = palette(norm(chart.get_value(sr.record[0])[column]))
        _paint_region(ax, sr.shape,color)

#    Colorbar is coded based on this link: https://stackoverflow.com/questions/8342549/matplotlib-add-colorbar-to-a-sequence-of-line-plots
#    Colorbar API: https://matplotlib.org/api/colorbar_api.html
    sm = plt.cm.ScalarMappable(cmap=palette, norm=plt.Normalize(vmin=min_value, vmax=max_value))
    # fake up the array of the scalar mappable. Urgh...
    sm._A = []
    fig.colorbar(sm) # colorbar(sm, orientation= 'horizontal')
#    fig.savefig(metrics_filename + '.pdf', dpi=1000)
    fig.savefig(metrics_filename + '.svg', format='svg', dpi=1200)
#    plt.show()
    plt.close(fig)


def print_map_year_all(chart, title, column, timesteps, value_type, results, name, index, colormap):
    sf = shapefile.Reader(results.shapefile_path)
    metrics_filename = os.path.join(results.output_path, 'maps', name + '_' + index)
    metrics_filename_pdf = os.path.join(results.output_path, 'maps', 'auxgifs', name + '_' + index)

    fig = plt.figure(figsize=(8, 8)) # Notice the equal aspect ratio
    axlist = [fig.add_subplot(3, 4, i+1) for i in range(12)]

    # Get max and min value for the color map:
    if value_type == 'Percentage':
        max_value = 1
        min_value = 0
    elif value_type == 'Margin':
        max_value = max(abs(max([i[column][year] for i in chart.table.values() for year in timesteps])),
                        abs(min([i[column][year] for i in chart.table.values() for year in timesteps])))
        min_value = -max_value
    else:
        max_value = max([i[column][year] for i in chart.table.values() for year in timesteps])
        min_value = min([i[column][year] for i in chart.table.values() for year in timesteps])

    for year in timesteps:
        ax = axlist[year-2020]

        fig.suptitle(title, fontsize=16)
        ax.set_aspect('equal')
        ax.title.set_text(str(year))
        ax.get_xaxis().set_visible(False)
        ax.get_yaxis().set_visible(False)

        # Select the color map from: https://matplotlib.org/examples/color/colormaps_reference.html
        palette = plt.get_cmap(colormap) #Add _r at the end to get the inverse color map
        norm = colors.Normalize(vmin=min_value, vmax=max_value)

        for sr in sf.iterShapeRecords(): #For each LAD of the shapefile: shape (geometry) and record (information)
            color = palette(norm(chart.get_value(sr.record[0])[column][year]))
            _paint_region(ax, sr.shape , color)

    fig.subplots_adjust(wspace=0, hspace=0.200)
    axlist[11].axis('off')
    #    Colorbar is coded based on this link: https://stackoverflow.com/questions/8342549/matplotlib-add-colorbar-to-a-sequence-of-line-plots
    #    Colorbar API: https://matplotlib.org/api/colorbar_api.html
    sm = plt.cm.ScalarMappable(cmap=palette, norm=plt.Normalize(vmin=min_value, vmax=max_value))
    # fake up the array of the scalar mappable. Urgh...
    sm._A = []
    fig.colorbar(sm, ax=axlist)  # colorbar(sm, orientation= 'horizontal')

    fig.savefig(metrics_filename_pdf + '.jpg', dpi=1000)
    fig.savefig(metrics_filename + '.svg', format='svg', dpi=1200)
    results.gifs_filenames[name].append(os.path.join(metrics_filename, 'auxgifs') + '.jpg')

#    plt.show()
    plt.close(fig)


def print_map_per_year(chart, title, column, timesteps, results, name, index, colormap):
    sf = shapefile.Reader(results.shapefile_path)

    for year in timesteps:
        metrics_filename = os.path.join(results.output_path, 'maps/detail_per_year', name + '_' + str(year) + '_' + index)

        fig = plt.figure()
        ax = fig.add_subplot(1, 1, 1)
        ax.set_aspect('equal')
        ax.title.set_text(title + ' in ' + str(year))
        ax.get_xaxis().set_visible(False)
        ax.get_yaxis().set_visible(False)

        # Select the color map from: https://matplotlib.org/examples/color/colormaps_reference.html
        palette = plt.get_cmap(colormap) #Add _r at the end to get the inverse color map

        # Get max and min value for the color map:
        max_value = max([i[column][year] for i in chart.table.values()])
        min_value = min([i[column][year] for i in chart.table.values()])
        norm = colors.Normalize(vmin=min_value, vmax=max_value)

        for sr in sf.iterShapeRecords(): #For each LAD of the shapefile: shape (geometry) and record (information)
            color = palette(norm(chart.get_value(sr.record[0])[column][year]))
            _paint_region(ax, sr.shape, color)

    #    Colorbar is coded based on this link: https://stackoverflow.com/questions/8342549/matplotlib-add-colorbar-to-a-sequence-of-line-plots
    #    Colorbar API: https://matplotlib.org/api/colorbar_api.html
        sm = plt.cm.ScalarMappable(cmap=palette, norm=plt.Normalize(vmin=min_value, vmax=max_value))
        # fake up the array of the scalar mappable. Urgh...
        sm._A = []
        fig.colorbar(sm)  # colorbar(sm, orientation= 'horizontal')
        fig.savefig(metrics_filename + '.svg', format='svg', dpi=1200)
        plt.close(fig)


def print_tech_map_aggregated(chart, title, columns, results, name, index, colormap):

    sf = shapefile.Reader(results.shapefile_path)
    metrics_filename = os.path.join(results.output_path, 'maps', name + '_' + index)
    titles = ['LTE', '700 MHz']

    # fig = plt.figure(figsize=(8, 8))  # Notice the equal aspect ratio
    # fig.suptitle(title, fontsize=16)
    fig = plt.figure()  # Notice the equal aspect ratio
    fig.suptitle(title)
    axlist = [fig.add_subplot(1, len(columns), i+1) for i in range(len(columns))]

    # Get max and min value for the color map:

    max_value = max([i[column] for i in chart.table.values() for column in columns])
    min_value = min([i[column] for i in chart.table.values() for column in columns])

    # Get max and min value for the color map:


    column_number = 0
    for column in columns:
#        print('COLUMN ' + str(column))
        ax = axlist[column_number]

        ax.set_aspect('equal')
        ax.title.set_text(titles[column_number])
        column_number += 1

        ax.get_xaxis().set_visible(False)
        ax.get_yaxis().set_visible(False)

        # Select the color map from: https://matplotlib.org/examples/color/colormaps_reference.html
        palette = plt.get_cmap(colormap) #Add _r at the end to get the inverse color map
        norm = colors.Normalize(vmin=min_value, vmax=max_value)

        for sr in sf.iterShapeRecords(): #For each LAD of the shapefile: shape (geometry) and record (information)
            color = palette(norm(chart.get_value(sr.record[0])[column]))
#            print(str(chart.get_value(sr.record[0])[column]))
            _paint_region(ax, sr.shape, color)

    #fig.subplots_adjust(wspace=0, hspace=0.200)
    #    Colorbar is coded based on this link: https://stackoverflow.com/questions/8342549/matplotlib-add-colorbar-to-a-sequence-of-line-plots
    #    Colorbar API: https://matplotlib.org/api/colorbar_api.html
    sm = plt.cm.ScalarMappable(cmap=palette, norm=plt.Normalize(vmin=min_value, vmax=max_value))
    # fake up the array of the scalar mappable. Urgh...
    sm._A = []
    fig.colorbar(sm,ax=axlist) # colorbar(sm, orientation= 'horizontal')

    fig.savefig(metrics_filename + '.svg', format='svg', dpi=1200)
    plt.close(fig)


def print_tech_map_per_year(chart, title, columns, timesteps, results, name, index, colormap):
    sf = shapefile.Reader(results.shapefile_path)
    for year in timesteps:
        metrics_filename = os.path.join(results.output_path, 'maps/detail_per_year', name + '_' + str(year) + '_' + index)
        titles = ['LTE', '700 MHz']

        fig = plt.figure(figsize=(8, 8)) # Notice the equal aspect ratio
        fig.suptitle(title + " " + str(year), fontsize=16)
        axlist = [fig.add_subplot(1, len(columns), i+1) for i in range(len(columns))]

        # Get max and min value for the color map:
        max_value = max([i[column][year] for i in chart.table.values() for column in columns])
        min_value = min([i[column][year] for i in chart.table.values() for column in columns])

        column_number = 0
        for column in columns:
            ax = axlist[column_number]

            ax.set_aspect('equal')
            ax.title.set_text(titles[column_number])
            column_number += 1

            ax.get_xaxis().set_visible(False)
            ax.get_yaxis().set_visible(False)

            # Select the color map from: https://matplotlib.org/examples/color/colormaps_reference.html
            palette = plt.get_cmap(colormap) #Add _r at the end to get the inverse color map
            norm = colors.Normalize(vmin=min_value, vmax=max_value)

            for sr in sf.iterShapeRecords(): #For each LAD of the shapefile: shape (geometry) and record (information)
                color = palette(norm(chart.get_value(sr.record[0])[column][year]))
                _paint_region(ax, sr.shape, color)

        fig.subplots_adjust(wspace=0, hspace=0.200)
        #    Colorbar is coded based on this link: https://stackoverflow.com/questions/8342549/matplotlib-add-colorbar-to-a-sequence-of-line-plots
        #    Colorbar API: https://matplotlib.org/api/colorbar_api.html
        sm = plt.cm.ScalarMappable(cmap=palette, norm=plt.Normalize(vmin=min_value, vmax=max_value))
        # fake up the array of the scalar mappable. Urgh...
        sm._A = []
        fig.colorbar(sm, ax=axlist)  # colorbar(sm, orientation= 'horizontal')

        fig.savefig(metrics_filename + '.svg', format='svg', dpi=1200)
        plt.close(fig)


def _paint_region(ax, shape, color):
    # PAINT THE REGION
    npoints = len(shape.points)  # total points
    nparts  = len(shape.parts)   # total parts

    if nparts == 1:
        x_lon = np.zeros((len(shape.points), 1))
        y_lat = np.zeros((len(shape.points), 1))
        for ip in range(len(shape.points)):
            x_lon[ip] = shape.points[ip][0]
            y_lat[ip] = shape.points[ip][1]
        ax.plot(x_lon, y_lat, 'k', linewidth=0.3)
        ax.fill(x_lon, y_lat, facecolor=color)

    else:  # loop over parts of each shape, plot separately
        for ip in range(nparts):  # loop over parts, plot separately
            i0 = shape.parts[ip]
            if ip < nparts-1:
                i1 = shape.parts[ip+1]-1
            else:
                i1 = npoints

            seg = shape.points[i0:i1+1]
            x_lon = np.zeros((len(seg), 1))
            y_lat = np.zeros((len(seg), 1))
            for ip in range(len(seg)):
                x_lon[ip] = seg[ip][0]
                y_lat[ip] = seg[ip][1]

            ax.plot(x_lon, y_lat, 'k', linewidth=0.3)
            ax.fill(x_lon, y_lat, facecolor=color)

###########
# USEFUL CODE
###########
# Simulation the color bar
#    Z = [[i[column] for i in chart.table.values()]]
#    levels = range(min_value,max_value+100,100)
#    CS3 = plt.contour(Z, cmap=palette)
#    plt.clf()
#    plt.colorbar(CS3) # using the colorbar info I got from contourf

#    plt.contourf(ax, 50, cmap=palette) # expect 50 levels

#    plt.contourf([i[column] for i in chart.table.values()], 50, cmap=palette) # expect 50 levels


#    fig.colorbar(fig, ticks=[-1, 0, 1], orientation='horizontal')
#    cbar.ax.set_xticklabels(['Low', 'Medium', 'High'])  # horizontal colorbar
#    plt.colorbar(ax)
