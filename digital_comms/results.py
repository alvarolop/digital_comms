import collections
#from itertools import accumulate

class Results:
    """
    This class contains all the tables with results to paint after executing the code.

    """
    def __init__(self, output_path, shapefile_path):
        self._chart_1 = collections.OrderedDict() # One table for each population-demand-coverage_obligation scenario
        self._chart_2 = collections.OrderedDict() # One table for each population-demand-coverage_obligation scenario
        self._chart_3 = collections.OrderedDict() # One table for each population-demand-coverage_obligation scenario
        self._chart_4 = collections.OrderedDict() # One table for each population-demand-coverage_obligation scenario
        self._chart_5 = collections.OrderedDict() # One table for each population-demand-coverage_obligation scenario

        self._chart_1_lads = collections.OrderedDict() # One table for each population-demand-coverage_obligation scenario
        self._chart_2_lads = collections.OrderedDict() # One table for each population-demand-coverage_obligation scenario
        self._chart_3_lads = collections.OrderedDict() # One table for each population-demand-coverage_obligation scenario
        self._chart_4_lads = collections.OrderedDict() # One table for each population-demand-coverage_obligation scenario
        self._chart_5_lads = collections.OrderedDict() # One table for each population-demand-coverage_obligation scenario


        # Coverage obligation strategy
        #
        # Coverage obligations apply only to towns smaller than self.co_population_limit inhabitants
        self.co_name = {}
        self.co_coverage_obligation_type = None #= ''
        self.co_percentage_covered = None #= 0
        self.co_population_limit_boolean = None #= False
        self.co_population_limit = None #= 5000
        self.co_deploiement_prioritaire = None # This percentage only applies to France
        self.co_budget_limit = None # True is the default value
        self.co_descending_order = None # True is the default value, investing in higher valuable pcds first
        self.co_invest_by_demand = None
        self.co_coverage_obligation = None
        self.co_percentage_covered_all = {}

        # self.covered_real = {}

        self.output_path = output_path
        self.shapefile_path = shapefile_path
        self.population_2020 = 0

        self.gifs_filenames = collections.defaultdict(list)
        self.cap_margin_bounds_plot = [-6000,6000]
        self.cap_margin_bounds_maps = [-100, 100]
        self.summary_graphs_combinations = {}

# CHARTS FOR PCDs
    @property
    def chart_1(self):
        return self._chart_1
    @chart_1.setter
    def chart_1(self, value):
        self._chart_1 = value

    @property
    def chart_2(self):
        return self._chart_2
    @chart_2.setter
    def chart_2(self, value):
        self._chart_2 = value

    @property
    def chart_3(self):
        return self._chart_3
    @chart_3.setter
    def chart_3(self, value):
        self._chart_3 = value

    @property
    def chart_4(self):
        return self._chart_4
    @chart_4.setter
    def chart_4(self, value):
        self._chart_4 = value

    @property
    def chart_5(self):
        return self._chart_5
    @chart_5.setter
    def chart_5(self, value):
        self._chart_5 = value

#CHARTS FOR LADs
    @property
    def chart_1_lads(self):
        return self._chart_1_lads
    @chart_1_lads.setter
    def chart_1_lads(self, value):
        self._chart_1_lads = value

    @property
    def chart_2_lads(self):
        return self._chart_2_lads
    @chart_2_lads.setter
    def chart_2_lads(self, value):
        self._chart_2_lads = value

    @property
    def chart_3_lads(self):
        return self._chart_3_lads
    @chart_3_lads.setter
    def chart_3_lads(self, value):
        self._chart_3_lads = value

    @property
    def chart_4_lads(self):
        return self._chart_4_lads
    @chart_4_lads.setter
    def chart_4_lads(self, value):
        self._chart_4_lads = value

    @property
    def chart_5_lads(self):
        return self._chart_5_lads
    @chart_5_lads.setter
    def chart_5_lads(self, value):
        self._chart_5_lads = value

# CHARTS FOR PCDs
    def chart1_add_table(self, key):
        self._chart_1[key] = Chart1()

    def chart1_get_table(self, key):
        return self._chart_1[key]

    def chart2_add_table(self, key):
        self._chart_2[key] = Chart2()

    def chart2_get_table(self, key):
        return self._chart_2[key]

    def chart3_add_table(self, key):
        self._chart_3[key] = Chart3()

    def chart3_get_table(self, key):
        return self._chart_3[key]

    def chart4_add_table(self, key):
        self._chart_4[key] = Chart4()

    def chart4_get_table(self, key):
        return self._chart_4[key]

    def chart5_add_table(self, key):
        self._chart_5[key] = Chart5()

    def chart5_get_table(self, key):
        return self._chart_5[key]

#CHARTS FOR LADs
    def chart1_lads_add_table(self, key):
        self._chart_1_lads[key] = Chart1_LADS()

    def chart1_lads_get_table(self, key):
        return self._chart_1_lads[key]

    def chart2_lads_add_table(self, key):
        self._chart_2_lads[key] = Chart2_LADS()

    def chart2_lads_get_table(self, key):
        return self._chart_2_lads[key]

    def chart3_lads_add_table(self, key):
        self._chart_3_lads[key] = Chart3_LADS()

    def chart3_lads_get_table(self, key):
        return self._chart_3_lads[key]

    def chart4_lads_add_table(self, key):
        self._chart_4_lads[key] = Chart4_LADS()

    def chart4_lads_get_table(self, key):
        return self._chart_4_lads[key]

    def chart5_lads_add_table(self, key):
        self._chart_5_lads[key] = Chart5_LADS()

    def chart5_lads_get_table(self, key):
        return self._chart_5_lads[key]

class Chart1(object):
    """
    This class contains the information related to the PCD-COST-POPULATION chart.
    All the information to create the graph is in the element "table" and it can be accessed using the following commands:
    http://www.pythonforbeginners.com/dictionary/how-to-use-dictionaries-in-python
    https://docs.python.org/3.6/library/collections.html#collections.OrderedDict
    http://www.physics.nyu.edu/pine/pymanual/html/chap3/chap3_arrays.html

    [pcd_id, pcd_lad_id, pcd_population, pcd_population_density, {costs per year}, cost, population_sum, cost_sum, pop_covered_2030, pop_covered_agg_2030, {pop_covered_per_year}]
    """
    def __init__(self):
        self._table = collections.OrderedDict()

    def _get_table(self):
        return self._table

    def _set_table(self, value):
        self._table = value

    table = property(_get_table, _set_table)

    def add_value(self, key, value):
        self._table[key] = value

    def get_value(self, key):
        return self._table[key]

    def get_all_values(self):
        for key,val in self._table.items():
            print (key, "=>", val)
        print("----")

    def add_initial_info(self, pcd_id, pcd_lad_id, pcd_population, pcd_population_density, timesteps, previous_pop):
        self._table[pcd_id] = [pcd_id, pcd_lad_id, pcd_population, pcd_population_density, {}, 0, 0, 0, 0, 0, {}]
#        self._table[pcd_id][6] += sum([value[2] for key,value in self._table.items()])
        self._table[pcd_id][6] = pcd_population + previous_pop

        for year in timesteps:
            self._table[pcd_id][4][year] = 0
            self._table[pcd_id][10][year] = 0
        return self._table[pcd_id][6]

    def add_cost(self, key, year, value):
        if key in self._table:
            self._table[key][4][year] += value
            self._table[key][5] += value
        else:
            print ("Error: {} key was not there!", key)

    def add_aggregated_cost(self, key, value):
        if key in self._table:
            self._table[key][7] += value
        else:
            print ("Error: {} key was not there!", key)

    def add_population_covered(self, key, year, capacity, demand, population, coverage_obligation):
#        self._table[key][8] += min (capacity / demand, 1) * population
        if year == 2030:
            self._table[key][8] += min (capacity / coverage_obligation, 1) * population
        self._table[key][10][year] += min (capacity / coverage_obligation, 1) * population
        
    def add_aggregated_population_covered(self, key, value):
        self._table[key][9] += value


class Chart1_LADS(object):
    """
    This class contains the information related to the LAD-COST-POPULATION chart with LADS
    [lad_id, lad_name, lad_population, lad_population_density, {costs per year}, cost]
    [pcd_id, pcd_lad_id, pcd_population, pcd_population_density, {costs per year}, cost, population_sum, cost_sum]
    """
    def __init__(self):
        self._table = collections.OrderedDict()

    def _get_table(self):
        return self._table

    def _set_table(self, value):
        self._table = value

    table = property(_get_table, _set_table)

    def add_value(self, key, value):
        self._table[key] = value

    def get_value(self, key):
        return self._table[key]

    def add_initial_info(self, lad_id, lad_name, lad_population, lad_population_density, timesteps, previous_pop):
        self._table[lad_id] = [lad_id, lad_name, lad_population, lad_population_density, {}, 0, 0, 0]
        self._table[lad_id][6] = lad_population + previous_pop

        for year in timesteps:
            self._table[lad_id][4][year] = 0
        return self._table[lad_id][6]


    def add_cost(self, key, year, value):
        if key in self._table:
            self._table[key][4][year] += value
            self._table[key][5] += value
        else:
            raise KeyError("Error: {} key was not there!", key)

    def add_aggregated_cost(self, key, value):
        if key in self._table:
            self._table[key][7] += value
        else:
            print ("Error: {} key was not there!", key)
            



class Chart2(object):
    """
    This class contains the information related to the PCD-Capacity Margin chart.
    [pcd_id, pcd_lad_id, pcd_population, pcd_population_density, {timesteps}, 0, 0, population_sum, cost_sum]
    """
    def __init__(self):
        self._table = collections.OrderedDict()

    def _get_table(self):
        return self._table

    def _set_table(self, value):
        self._table = value

    table = property(_get_table, _set_table)

    def add_initial_info(self, pcd_id, pcd_lad_id, pcd_population, pcd_population_density, previous_pop):
        self._table[pcd_id] = [pcd_id, pcd_lad_id, pcd_population, pcd_population_density, {}, 0, 0]
        self._table[pcd_id][5] = pcd_population + previous_pop

        return self._table[pcd_id][5]

    def add_cap_margin(self, key, year, cap_margin):
        self._table[key][4][year] = cap_margin

    def get_value(self, key):
        return self._table[key]

    def get_all_values(self):
        for key,val in self._table.items():
            print (key, "=>", val)
        print("----")



class Chart2_LADS(object):
    """
    This class contains the information related to the LAD-Capacity Margin chart.
    [lad_id, lad_name, pcd_population, pcd_population_density, {timesteps}, population_sum, cost_sum]

    """
    def __init__(self):
        self._table = collections.OrderedDict()

    def _get_table(self):
        return self._table

    def _set_table(self, value):
        self._table = value

    table = property(_get_table, _set_table)

    def add_initial_info(self, lad_id, lad_name, lad_population, lad_population_density, previous_pop):
        self._table[lad_id] = [lad_id, lad_name, lad_population, lad_population_density, {}, 0, 0]
        self._table[lad_id][5] = lad_population + previous_pop

        return self._table[lad_id][5]

    def add_cap_margin(self, key, year, cap_margin):
        self._table[key][4][year] = cap_margin

    def get_value(self, key):
        return self._table[key]

    def get_all_values(self):
        for key,val in self._table.items():
            print (key, "=>", val)
        print("----")


class Chart3(object):
    """
    This class contains the information related to the PCD-Spectrum Integration chart.
    [pcd_id, pcd_lad_id, pcd_population, pcd_population_density, {LTE}, {700MHz}, LTE_sum, 700MHz_sum, population_sum, cost_sum ]
    """

    def __init__(self):
        self._table = collections.OrderedDict()

    def _get_table(self):
        return self._table

    def _set_table(self, value):
        self._table = value

    table = property(_get_table, _set_table)

    def add_initial_info(self, pcd_id, pcd_lad_id, pcd_population, pcd_population_density, timesteps, previous_pop):
        self._table[pcd_id] = [pcd_id, pcd_lad_id, pcd_population, pcd_population_density, {}, {}, 0, 0, 0, 0]
        self._table[pcd_id][8] = pcd_population + previous_pop

        for year in timesteps:
            self._table[pcd_id][4][year] = 0
            self._table[pcd_id][5][year] = 0
        return self._table[pcd_id][8]

    def add_tech(self, key, year, technology):
        if technology is 'LTE':
            self._table[key][4][year] += 1
            self._table[key][6] += 1
        elif technology is 'carrier_700':
            self._table[key][5][year] += 1
            self._table[key][7] += 1
#        else:
#            raise KeyError("Alvaro: Technology not allowed for upgrade")

    def get_value(self, key):
        return self._table[key]

    def get_all_values(self):
        for key,val in self._table.items():
            print (key, "=>", val)
        print("----")


class Chart3_LADS(object):
    """
    This class contains the information related to the LAD-Spectrum Integration chart.
    [lad_id, lad_name, lad_population, lad_population_density, {LTE}, {700MHz}, LTE_sum, 700MHz_sum, population_sum, cost_sum]
    """

    def __init__(self):
        self._table = collections.OrderedDict()

    def _get_table(self):
        return self._table

    def _set_table(self, value):
        self._table = value

    table = property(_get_table, _set_table)

    def add_initial_info(self, lad_id, lad_name, lad_population, lad_population_density, timesteps, previous_pop):
        self._table[lad_id] = [lad_id, lad_name, lad_population, lad_population_density, {}, {}, 0, 0, 0, 0]
        self._table[lad_id][8] = lad_population + previous_pop

        for year in timesteps:
            self._table[lad_id][4][year] = 0
            self._table[lad_id][5][year] = 0
        return self._table[lad_id][8]

    def add_tech(self, key, year, technology):
        if technology is 'LTE':
            self._table[key][4][year] += 1
            self._table[key][6] += 1
        elif technology is 'carrier_700':
            self._table[key][5][year] += 1
            self._table[key][7] += 1
#        else:
#            raise KeyError("Alvaro: Technology not allowed for upgrade")

    def get_value(self, key):
        return self._table[key]


class Chart4(object):
    """
    This class contains the information related to the PCD-Population covered chart.
    [pcd_id, pcd_lad_id, pcd_population, pcd_population_density, {Cap_pcd}, {Demand_pcd}, {Pop_covered}, Cap_covered, population_sum, cost_sum, {coverage_obligation_pcd}]
    """

    def __init__(self):
        self._table = collections.OrderedDict()

    def _get_table(self):
        return self._table

    def _set_table(self, value):
        self._table = value

    table = property(_get_table, _set_table)

    def add_initial_info(self, pcd_id, pcd_lad_id, pcd_population, pcd_population_density, timesteps, previous_pop):
        self._table[pcd_id] = [pcd_id, pcd_lad_id, pcd_population, pcd_population_density, {}, {}, {}, 0, 0, 0, {}]
        self._table[pcd_id][8] = pcd_population + previous_pop

        for year in timesteps:
            self._table[pcd_id][4][year] = 0
            self._table[pcd_id][5][year] = 0
            self._table[pcd_id][6][year] = 0
            self._table[pcd_id][10][year] = 0
        return self._table[pcd_id][8]

    def add_cap_and_demand(self, key, year, capacity, demand, coverage_ob):
        self._table[key][4][year] = capacity
        self._table[key][5][year] = demand
        self._table[key][6][year] = min(capacity / demand, 1)
        self._table[key][10][year] = min(capacity / coverage_ob, 1)
        if (capacity >= coverage_ob):
            self._table[key][7] += 1

    def get_value(self, key):
        return self._table[key]

    def get_all_values(self):
        for key,val in self._table.items():
            print (key, "=>", val)
        print("----")



class Chart4_LADS(object):
    """
    This class contains the information related to the LAD-Population covered chart.
    [pcd_id, pcd_lad_id, pcd_population, pcd_population_density, {Cap_pcd}, {Demand_pcd}, {Pop_covered}, Cap_covered, population_sum, cost_sum ]
    """

    def __init__(self):
        self._table = collections.OrderedDict()

    def _get_table(self):
        return self._table

    def _set_table(self, value):
        self._table = value

    table = property(_get_table, _set_table)

    def add_initial_info(self, lad_id, lad_name, lad_population, lad_population_density, timesteps, previous_pop):
        self._table[lad_id] = [lad_id, lad_name, lad_population, lad_population_density, {}, {}, {}, 0, 0, 0]
        self._table[lad_id][8] = lad_population + previous_pop

        for year in timesteps:
            self._table[lad_id][4][year] = 0
            self._table[lad_id][5][year] = 0
            self._table[lad_id][6][year] = 0
        return self._table[lad_id][8]

    def add_cap_and_demand(self, key, year, capacity, demand, coverage):
        self._table[key][4][year] = capacity
        self._table[key][5][year] = demand
        self._table[key][6][year] = coverage

        if capacity >= demand:
            self._table[key][7] += 1

    def get_value(self, key):
        return self._table[key]




class Chart5(object):
    """
    This class contains the information related to the Year-Summary data chart.
    [year, population, cost, aggregated_cost, pop_covered, #pcds_covered, cap_margin, bool_invest_demand]
    """

    def __init__(self):
        self._table = collections.OrderedDict()
        self.invest_to_meet_demand_boolean = 0

    def _get_table(self):
        return self._table

    def _set_table(self, value):
        self._table = value

    table = property(_get_table, _set_table)


    def add_initial_info(self, results, system, index, year):

        # Initialize the dictionary adding the key, the first column and the population
        self._table[year] = [year, system.population, 0, 0, 0, 0, 0, 0, 0, 0]

        # Add the cost of all pcds this year
        self._table[year][2] = sum (value[4][year]     for key, value in results.chart1_get_table(index)._table.items())

        # Add the % population covered each year
        # %total_pop = sum(%pob_pcd * pob_pcd) / total_pop
        percentage_sum = sum(value[10][year] * value[2] for key, value in results.chart4_get_table(index)._table.items())
        self._table[year][4] = percentage_sum / results.population_2020

        # Number of pcds that fullfil the coverage obligations
        self._table[year][5] = sum(value[10][year]      for key, value in results.chart4_get_table(index)._table.items() if value[6][year] == 1)

        # Add the capacity margin per year
        # %total_pop = sum(%pob_pcd * pob_pcd) / total_pop
        cap_margin_sum = sum(value[4][year] * value[2] for key, value in results.chart2_get_table(index)._table.items())
        self._table[year][6] = cap_margin_sum / results.population_2020

        # Fill the meet demand column
        self._table[year][7] = self.invest_to_meet_demand_boolean

        # Add the cost of all pcds this year
        self._table[year][8] = sum(value[4][year] for key, value in results.chart4_get_table(index)._table.items())
        # Add the cost of all pcds this year
        self._table[year][9] = sum(value[5][year] for key, value in results.chart4_get_table(index)._table.items())
        # Add the cost of all pcds this year
        # self._table[year][9] = sum(value[5][year] for key, value in results.chart4_get_table(index)._table.items())

    def calculate_aggregated_elements(self, results, timesteps):
        previous_cost = 0
        # Fill the aggregated cost column
        for year in timesteps:
            self._table[year][3] = self._table[year][2] + previous_cost
            previous_cost = self._table[year][3]

    def invest_to_meet_demand (self, year):
#        self.get_all_values()
        self.invest_to_meet_demand_boolean = 1

    def get_value(self, key):
        return self._table[key]

    def get_all_values(self):
        print ("('Year', 'Population', 'Cost', 'Aggregated cost', '% Population covered', '# PCDs covered', 'Capacity margin', 'Invest by demand', 'Capacity', 'Demand')")
        for key,val in self._table.items():
            print (key, "=>", val)
        print("----")


class Chart5_LADS(object):
    """
    This class contains the information related to the Year-Summary data chart.
    [pcd_id, pcd_lad_id, pcd_population, pcd_population_density, {Cap_pcd}, {Demand_pcd}, {Pop_covered}, Cap_covered, population_sum, cost_sum ]
    """

    def __init__(self):
        self._table = collections.OrderedDict()

    def _get_table(self):
        return self._table

    def _set_table(self, value):
        self._table = value

    table = property(_get_table, _set_table)

    def add_initial_info(self, lad_id, lad_name, lad_population, lad_population_density, timesteps, previous_pop):
        self._table[lad_id] = [lad_id, lad_name, lad_population, lad_population_density, {}, {}, {}, 0, 0, 0]
        self._table[lad_id][8] = lad_population + previous_pop

        for year in timesteps:
            self._table[lad_id][4][year] = 0
            self._table[lad_id][5][year] = 0
            self._table[lad_id][6][year] = 0
        return self._table[lad_id][8]

    def add_cap_and_demand(self, key, year, capacity, demand, coverage):
        self._table[key][4][year] = capacity
        self._table[key][5][year] = demand
        self._table[key][6][year] = coverage

        if capacity >= coverage:
            self._table[key][7] += 1

    def get_value(self, key):
        return self._table[key]
