"""Decide on interventions
"""
# pylint: disable=C0103
from digital_comms.ccam import PostcodeSector

import copy
#import pprint

################################################################
# EXAMPLE COST LOOKUP TABLE
# - TODO come back to net present value or total cost of ownership for costs
################################################################

# Postcode-sector level individual interventions
INTERVENTIONS = {
    'upgrade_to_lte': {
        'name': 'Upgrade site to LTE',
        'description': 'If a site has only 2G/3G',
        'result': '800 and 2600 bands available',
        'cost': 142446,
        'assets_to_build': [
            {
                # site_ngr to match upgraded
                'site_ngr': None,
                'frequency': '800',
                'technology': 'LTE',
                'type': 'macrocell_site',
                'bandwidth': '2x10MHz',
                # set build date when deciding
                'build_date': None,
            },
            {
                # site_ngr to match upgraded
                'site_ngr': None,
                'frequency': '2600',
                'technology': 'LTE',
                'type': 'macrocell_site',
                'bandwidth': '2x10MHz',
                # set build date when deciding
                'build_date': None,
            },
        ]
    },
    'carrier_700': {
        'name': 'Build 700 MHz carrier',
        'description': 'Available if a site has LTE',
        'result': '700 band available',
        'cost': 50917,
        'assets_to_build': [
            {
                # site_ngr to match upgraded
                'site_ngr': None,
                'frequency': '700',
                'technology': 'LTE',
                'type': 'macrocell_site',
                'bandwidth': '2x10MHz',
                # set build date when deciding
                'build_date': None,
            },
        ]
    },
    'new_site_carrier_700': {
        'name': 'Build 700 MHz carrier',
        'description': 'Deployment of a new BS with 700MHz',
        'result': '700 band available',
        'cost': 142446,
        'assets_to_build': [
            {
                # site_ngr to match upgraded
                'site_ngr': None,
                'frequency': '700',
                'technology': 'LTE',
                'type': 'macrocell_site',
                'bandwidth': '2x10MHz',
                # set build date when deciding
                'build_date': None,
            },
        ]
    },
    'carrier_3500': {
        'name': 'Build 3500 MHz carrier',
        'description': 'Available if a site has LTE',
        'result': '3500 band available',
        'cost': 50917,
        'assets_to_build': [
            {
                # site_ngr to match upgraded
                'site_ngr': None,
                'frequency': '3500',
                'technology': 'LTE',
                'type': 'macrocell_site',
                'bandwidth': '2x10MHz',
                # set build date when deciding
                'build_date': None,
            },
        ]
    },
    'small_cell': {
        'name': 'Build a small cell',
        'description': 'Must be deployed at preset densities to be modelled',
        'result': '2x25 MHz small cells available at given density',
        'cost': 40220,
        'assets_to_build': [
            {
                # site_ngr not used
                'site_ngr': 'small_cell_sites',
                'frequency': '3700',
                'technology': '5G',
                'type': 'small_cell',
                'bandwidth': '2x25MHz',
                # set build date when deciding
                'build_date': None,
            },
        ]
    }
}

AVAILABLE_STRATEGY_INTERVENTIONS = {
    # Intervention Strategy 1
    # Minimal Intervention 'Do Nothing Scenario'
    # Build no more additional sites -> will lead to a capacity margin deficit
    # The cost will be the replacement of existing units annually based on the
    # (decommissioning rate of 10%) common asset lifetime of 10 years
    # Capacity will be the sum of 800 and 2600 MHz
    'minimal': (),

    # Intervention Strategy 2
    # Integrate 700 and 3500 MHz on to the macrocellular layer
    # The cost will be the addtion of another carrier on each basestation ~£15k
    # (providing thre is 4G already)
    # If 4G isn't present, the site will need major upgrades.
    'macrocell': ('upgrade_to_lte', 'carrier_700',
                  'carrier_3500'),
     # Intervention Strategy 2.
     # Integrate 700
    'macrocell_700': ('upgrade_to_lte', 'carrier_700'),

    # Intervention Strategy 3
    # Deploy a small cell layer at 3700 MHz
    # The cost will include the small cell unit and the civil works per cell
    'small_cell': ('upgrade_to_lte', 'small_cell'),

    # Intervention Strategy 4
    # Deploy a small cell layer at 3700 MHz
    # The cost will include the small cell unit and the civil works per cell
    'small_cell_and_spectrum': ('upgrade_to_lte', 'carrier_700',
                   'carrier_3500', 'small_cell'),
                                
    # Intervention Strategy 5: Alvaro
     # Integrate 700
    'macrocell_only_700': ('only_700'),
}


def decide_interventions(strategy, budget, service_obligation_capacity, system, timestep, results, index):
    """Given strategy parameters and a system return some next best intervention

    Parameters
    ----------
    strategy : str
        One of 'minimal', 'macrocell', 'small_cell' intervention strategies
    budget : int
        Annual budget in GBP
    service_obligation_capacity : float
        Threshold for universal mobile service, in Mbps/km^2
    system : ICTManager
        Gives areas (postcode sectors) with population density, demand

    Returns
    -------
    tuple
        0: `obj`:`list` of `obj`:`dict`  
            Details of the assets that were built

            Each containing the keys

                site_ngr: str
                    Unique site reference number
                frequency: str
                    Asset frequency ("700", ..)
                technology: str
                    Asset technology ("LTE", ..)
                bandwidth: str
                    Asset bandwith ("2x10MHz", ..)
                build_date: int
                    Timestep when the asset was built
                pcd_sector: int
                    Id of the postcode sector where asset is located
        1: int
            Remaining budget
        2: int
            Total costs of intervention build step
    """
    available_interventions = AVAILABLE_STRATEGY_INTERVENTIONS[strategy]

    # 1. Coverage obligations
    if service_obligation_capacity > 0:
        service_built, budget, service_spend, results = meet_service_obligation(budget, available_interventions, timestep, system, results, index)
    else:
        service_built, service_spend = [], []

    # 2. Demand
    if budget > 40000 or not results.co_budget_limit:
        built, budget, spend, results = meet_demand(budget, available_interventions, timestep, system, results, index)
        results.chart_5[index].invest_to_meet_demand(timestep)
    else:
        print("DEMAN Considering {} of {} postcodes, no more budget".format(0, len(system.postcode_sectors.values())))
        built, budget, spend, results = [], budget, [], results
    print("Service", len(service_built))
    print("Demand", len(built))

    return built + service_built, budget, spend + service_spend, results


def meet_service_obligation(budget, available_interventions, timestep, system, results, index):
    areas = _suggest_target_postcodes_coverage_obligations(system, results)
    return _suggest_interventions(system, budget, available_interventions, areas, timestep, index, results, True)


def meet_demand(budget, available_interventions, timestep, system, results, index):
    areas = _suggest_target_postcodes_demand(system, results)
    return _suggest_interventions(system, budget, available_interventions, areas, timestep, index, results, False)


def _suggest_interventions(system, budget, available_interventions, areas, timestep, index, results, service_obligation_boolean):
    built_interventions, spend = [], []
    chart1, chart3 = results.chart_1[index], results.chart_3[index]
    chart1_lads, chart3_lads = results.chart_1_lads[index], results.chart_3_lads[index]

    for area in areas:
        area_interventions = []
        if results.co_budget_limit and budget < 0:
            break
#        if (area.id == "SG175" or area.id == "WC2B4" or area.id == "M607"):
#            print ("Area = {},  Assets = {}, New assets = {}, Cap = {}, Cov. Oblig = {}, Demand = {}".format(area.id, len(list(area.assets)), len(area_interventions), area.capacity, area.threshold_demand, area.demand))
#                    
        if _area_satisfied(area, area_interventions, system, results, service_obligation_boolean):
            continue

        # group assets by site
        assets_by_site = {}
        for asset in area.assets:
            if asset['site_ngr'] not in assets_by_site:
                assets_by_site[asset['site_ngr']] = [asset]
            else:
                assets_by_site[asset['site_ngr']].append(asset)

        # integrate_800 and integrate_2.6
        if 'upgrade_to_lte' in available_interventions:
            build_option = INTERVENTIONS['upgrade_to_lte']['assets_to_build']
            cost = INTERVENTIONS['upgrade_to_lte']['cost']
            
            previous_capacity = _get_new_capacity(area, area_interventions)
            for site_ngr, site_assets in assets_by_site.items():
                if site_ngr == 'small_cell_sites': 
                    continue
                if 'LTE' not in [asset['technology'] for asset in site_assets]:                   
                    # set both assets to this site_ngr
                    for option in build_option:                       
                        to_build = copy.copy(option)
                        to_build['site_ngr'] = site_ngr
                        to_build['pcd_sector'] = area.id
                        to_build['build_date'] = timestep
                        area_interventions.append(to_build)
                        
                        # Get capacity with the new asset
                        new_capacity = _get_new_capacity(area, area_interventions)
                        
                        # If capacity hasn´t grown, then break for this PCD
                        if(new_capacity <= previous_capacity):
#                            if (area.id == "SG175" or area.id == "WC2B4" or area.id == "M607"):
#                                print (area.id + " => Break")
                            break
                                        
#                        if (area.id == "SG175" or area.id == "WC2B4" or area.id == "M607"):
#                            print ("Area = {},  Assets = {}, New assets = {}, Previous cap = {}, Current cap = {}, Cov. Oblig = {}, Demand = {}".format(area.id, len(list(area.assets)), len(area_interventions), previous_capacity, new_capacity, area.threshold_demand, area.demand))
                        # If capacity can grow, then new loop
                        previous_capacity = new_capacity
                        
                        built_interventions.append(to_build)
                        chart3.add_tech(area.id, timestep, 'LTE')
                        chart3_lads.add_tech(area.ofcom_lad_id, timestep, 'LTE')
                    
                    budget -= cost
                    spend.append((area.id, area.lad_id, 'upgrade_to_lte', cost))
                    chart1.add_cost(area.id, timestep, cost)
                    chart1_lads.add_cost(area.ofcom_lad_id, timestep, cost)
                    if results.co_budget_limit and budget < 0:
                        break

        if results.co_budget_limit and budget < 0:
            break

        # integrate_700
        if 'carrier_700' in available_interventions and timestep >= 2020:
            if _area_satisfied(area, area_interventions, system, results, service_obligation_boolean):
                continue
            
            build_option = INTERVENTIONS['carrier_700']['assets_to_build']
            cost = INTERVENTIONS['carrier_700']['cost']
            
            previous_capacity = _get_new_capacity(area, area_interventions)
            for site_ngr, site_assets in assets_by_site.items():
                if site_ngr == 'small_cell_sites':
                    continue
                if 'LTE' in [asset['technology'] for asset in site_assets] and \
                        '700' not in [asset['frequency'] for asset in site_assets]:
                            
#                    if (area.id == "SG175" or area.id == "WC2B4" or area.id == "M607"):
#                        print ("Area = {},  Assets = {}, New assets = {}, Cap = {}, Cov. Oblig = {}, Demand = {}".format(area.id, len(list(area.assets)), len(area_interventions), _get_new_capacity(area, area_interventions), area.threshold_demand, area.demand))
                    # set both assets to this site_ngr
                    for option in build_option:
                        to_build = copy.copy(option)
                        to_build['site_ngr'] = site_ngr
                        to_build['pcd_sector'] = area.id
                        to_build['build_date'] = timestep
                        area_interventions.append(to_build)
                        
                        # Get capacity with the new asset
                        new_capacity = _get_new_capacity(area, area_interventions)
                        
                        # If capacity hasn´t grown, then break for this PCD
                        if(new_capacity <= previous_capacity):
#                            if (area.id == "SG175" or area.id == "WC2B4" or area.id == "M607"):
#                                print (area.id + " => Break")
                            break
                                        
#                        if (area.id == "SG175" or area.id == "WC2B4" or area.id == "M607"):
#                            print ("Area = {},  Assets = {}, New assets = {}, Cap = {}, Cov. Oblig = {}, Demand = {}".format(area.id, len(list(area.assets)), len(area_interventions), _get_new_capacity(area, area_interventions), area.threshold_demand, area.demand))
                        # If capacity can grow, then new loop
                        previous_capacity = new_capacity
                
                        built_interventions.append(to_build)
                        chart3.add_tech(area.id, timestep, 'carrier_700')
                        chart3_lads.add_tech(area.ofcom_lad_id, timestep, 'carrier_700')
                        
                    spend.append((area.id, area.lad_id, 'carrier_700', cost))
                    chart1.add_cost(area.id, timestep, cost)
                    chart1_lads.add_cost(area.ofcom_lad_id, timestep, cost)
                    budget -= cost
                    if results.co_budget_limit and budget < 0:
                        break

        if results.co_budget_limit and budget < 0:
            break
        
        

        # only_integrate_700
        if 'only_700' in available_interventions:
            if _area_satisfied(area, area_interventions, system, results, service_obligation_boolean):
                continue
            
            previous_capacity = _get_new_capacity(area, area_interventions)              
            while True:
                current_assets = area.assets + area_interventions
                assets_lte = len([asset for asset in current_assets if asset['frequency'] == "800"])
                assets_700 = len([asset for asset in current_assets if asset['frequency'] == "700"])

                if (assets_lte > assets_700):
                    build_option = INTERVENTIONS['carrier_700']['assets_to_build']
                    cost = INTERVENTIONS['carrier_700']['cost']
                else:
                    build_option = INTERVENTIONS['new_site_carrier_700']['assets_to_build']
                    cost = INTERVENTIONS['new_site_carrier_700']['cost']
                    
                to_build = copy.deepcopy(build_option)
                to_build[0]['build_date'] = timestep
                to_build[0]['pcd_sector'] = area.id
                area_interventions += to_build # This is for all the upgrades of this area
                
                # Get capacity with the new asset
                new_capacity = _get_new_capacity(area, area_interventions)
                
                # If capacity hasn´t grown, then break for this PCD
                if(new_capacity <= previous_capacity):
#                    if (area.id == "SG175" or area.id == "WC2B4" or area.id == "M607"):
#                        print (area.id + " => Break")
                    break
                                
#                if (area.id == "SG175" or area.id == "WC2B4" or area.id == "M607"):
#                    print ("Area = {},  Assets = {}, New assets = {}, LTE assets = {}, 700 assets = {}, Cost = {}, Previous cap = {}, Current cap = {}, Cov. Oblig = {}, Demand = {}".format(area.id, len(list(area.assets)), len(area_interventions), assets_lte, assets_700, cost, previous_capacity, new_capacity, area.threshold_demand, area.demand))
                
                # If capacity can grow, then new loop
                previous_capacity = new_capacity
                built_interventions += to_build #This is for the whole year
                
                spend.append((area.id, area.lad_id, 'carrier_700', cost))
                chart1.add_cost(area.id, timestep, cost)
                chart1_lads.add_cost(area.ofcom_lad_id, timestep, cost)
                chart3.add_tech(area.id, timestep, 'carrier_700')
                chart3_lads.add_tech(area.ofcom_lad_id, timestep, 'carrier_700')
                budget -= cost                
                
                if (results.co_budget_limit and budget < 0) or _area_satisfied(area, area_interventions, system, results, service_obligation_boolean):
#                    if (area.id == "SG175" or area.id == "WC2B4" or area.id == "M607"):
#                        print ("The demand/coverage obligation of {} is {}".format(area.id, "satisfied"))
                    break
                       
        
        # integrate_3.5
        if 'carrier_3500' in available_interventions and timestep >= 2020:
            if _area_satisfied(area, area_interventions, system, results, service_obligation_boolean):
                continue

            build_option = INTERVENTIONS['carrier_3500']['assets_to_build']
            cost = INTERVENTIONS['carrier_3500']['cost']
            for site_ngr, site_assets in assets_by_site.items():
                if site_ngr == 'small_cell_sites':
                    continue
                if 'LTE' in [asset['technology'] for asset in site_assets] and \
                        '3500' not in [asset['frequency'] for asset in site_assets]:
                    # set both assets to this site_ngr
                    for option in build_option:
                        to_build = copy.copy(option)
                        to_build['site_ngr'] = site_ngr
                        to_build['pcd_sector'] = area.id
                        to_build['build_date'] = timestep
                        area_interventions.append(to_build)
                        built_interventions.append(to_build)
                        chart3.add_tech(area.id, timestep, 'carrier_3500')
                        chart3_lads.add_tech(area.ofcom_lad_id, timestep, 'carrier_3500')
                        
                    spend.append((area.id, area.lad_id, 'carrier_3500', cost))
                    chart1.add_cost(area.id, timestep, cost)
                    chart1_lads.add_cost(area.ofcom_lad_id, timestep, cost)
                    budget -= cost
                    if results.co_budget_limit and budget < 0:
                        break

        if results.co_budget_limit and budget < 0:
            break

        # build small cells to next density
        if 'small_cell' in available_interventions and timestep >= 2020:
            if _area_satisfied(area, area_interventions, system, results, service_obligation_boolean):
                continue
            build_option = INTERVENTIONS['small_cell']['assets_to_build']
            cost = INTERVENTIONS['small_cell']['cost']
            
            previous_capacity = _get_new_capacity(area, area_interventions) 
            
            while True:
                to_build = copy.deepcopy(build_option)
                to_build[0]['build_date'] = timestep
                to_build[0]['pcd_sector'] = area.id

                area_interventions += to_build
                
                # Get capacity with the new asset
                new_capacity = _get_new_capacity(area, area_interventions)
                
                # If capacity hasn´t grown, then break for this PCD
                if(new_capacity <= previous_capacity):
#                    if (area.id == "SG175" or area.id == "WC2B4" or area.id == "M607"):
#                        print (area.id + " => Break")
                    break
                                
#                if (area.id == "SG175" or area.id == "WC2B4" or area.id == "M607"):
#                    print ("Area = {},  Assets = {}, New assets = {}, Previous cap = {}, Current cap = {}, Cov. Oblig = {}, Demand = {}".format(area.id, len(list(area.assets)), len(area_interventions), previous_capacity, new_capacity, area.threshold_demand, area.demand))
                
                # If capacity can grow, then new loop
                previous_capacity = new_capacity
                
                built_interventions += to_build
                spend.append((area.id, area.lad_id, 'small_cells', cost))
                chart1.add_cost(area.id, timestep, cost)
                chart1_lads.add_cost(area.ofcom_lad_id, timestep, cost)
                chart3.add_tech(area.id, timestep, 'small_cells')
                chart3_lads.add_tech(area.ofcom_lad_id, timestep, 'small_cells')
                budget -= cost

                if (results.co_budget_limit and budget < 0) or _area_satisfied(area, area_interventions, system, results, service_obligation_boolean):
                    break

    return built_interventions, budget, spend, results

def _suggest_target_postcodes_coverage_obligations(system, results):
    """Suggest postcodes to cover COVERAGE OBLIGATIONS
    """
    all_postcodes = system.postcode_sectors.values()
    postcodes = []
                
    # FRENCH strategy
    if results.co_coverage_obligation_type in ['cov_ob_2']:
        all_postcodes_inverted = sorted(all_postcodes, key=lambda pcd: pcd.population_density)

        priority_postcodes, remaining_postcodes, pop_covered = [], [], 0
        target_pop = system.population * results.co_deploiement_prioritaire
        
        # Part 1: Select postcodes of deploiment prioritaire and remove them from the list
        for pcd in all_postcodes_inverted:
            if pop_covered <= target_pop:
                pop_covered += pcd.population
                priority_postcodes.append(pcd)
            else:
                remaining_postcodes.append(pcd)
        
        # Part 2: 
        # Change the order to start investing in the most profitable ones
        priority_postcodes = sorted(priority_postcodes, key=lambda pcd: -pcd.population_density)
        remaining_postcodes = sorted(remaining_postcodes, key=lambda pcd: -pcd.population_density)
        # Add all postcodes together
        postcodes = priority_postcodes + remaining_postcodes


    # GERMAN strategy
    elif results.co_coverage_obligation_type in ['cov_ob_3']:
        pop_covered = 0
        target_pop = system.population * results.co_percentage_covered
        # Select postcodes in the whole UK
        for pcd in all_postcodes:
            if pop_covered >= target_pop:
                break
            pop_covered += pcd.population
            postcodes.append(pcd)
            
            
    # SPANISH strategy
    elif results.co_coverage_obligation_type in ['cov_ob_4']:
        # Select postcodes according to population
        if results.co_population_limit_boolean:
            all_postcodes = [pcd for pcd in all_postcodes if (pcd.population < results.co_population_limit)]
            
        pop_covered = 0
        population = sum(pcd.population for pcd in all_postcodes)
        target_pop = population * results.co_percentage_covered
        # Select postcodes in the whole UK
        for pcd in all_postcodes:
            if pop_covered >= target_pop:
                break
            pop_covered += pcd.population
            postcodes.append(pcd)
            
            
    # ENGLISH strategy
    elif results.co_coverage_obligation_type in ['cov_ob_1', 'cov_ob_5']: 
        # Set amount of population that has to be covered per country
        pop_covered_per_country = {'E': 0, 'S': 0, 'W': 0}
        target_pop_covered_per_country = {'E': system.pop_per_country['E'] * results.co_percentage_covered, 'S': system.pop_per_country['S'] * results.co_percentage_covered, 'W': system.pop_per_country['W'] * results.co_percentage_covered}
        
        # Select postcodes per country 
        for pcd in all_postcodes:
            if pop_covered_per_country[pcd.lad_id[0]] <= target_pop_covered_per_country[pcd.lad_id[0]]:
                pop_covered_per_country[pcd.lad_id[0]] += pcd.population
                postcodes.append(pcd)
            
    # OTHER strategies
    else:
        postcodes = [p for p in all_postcodes]
        
  
    # Select postcodes that dont cover obligations
    considered_postcodes = [pcd for pcd in postcodes ]  # if pcd.capacity < pcd.threshold_demand
    print("THRES Considering {} of {} postcodes".format(len(considered_postcodes), len(postcodes)))
        
    if results.co_coverage_obligation_type in ['cov_ob_2', 'cov_ob_4']:
        return considered_postcodes
    
    # Orden PCDs according to the coverage obligation order
    if results.co_descending_order:
        return sorted(considered_postcodes, key=lambda pcd: -pcd.population_density)
    else:
        return sorted(considered_postcodes, key=lambda pcd: pcd.population_density)


def _suggest_target_postcodes_demand(system, results):
    """Suggest postcodes to cover DEMAND
    """
    if results.co_invest_by_demand:
        considered_postcodes = [p for p in system.postcode_sectors.values()]
    else:
        considered_postcodes = []

    print("DEMAN Considering {} of {} postcodes".format(len(considered_postcodes), len(system.postcode_sectors.values())))
    return sorted(considered_postcodes, key=lambda pcd: -pcd.population_density)


def _area_satisfied(area, area_interventions, system, results, service_obligation_boolean):
    if service_obligation_boolean is True:
        target_capacity = area.threshold_demand
    else:
        target_capacity = area.demand

    data = {
        "id": area.id,
        "lad_id": area.lad_id,
        "population": area.population,
        "area": area.area,
        "user_throughput_GB": area.user_throughput_GB,
        "user_throughput_mbps": area.user_throughput_mbps,
    }
    assets = area.assets + area_interventions

    test_area = PostcodeSector(
        data,
        area.ofcom_lad_id,
        assets,
        area._capacity_lookup_table,
        area._clutter_lookup,
        0
    )
    reached_capacity = test_area.capacity
    return reached_capacity >= target_capacity


def _get_new_capacity(area, built_interventions):
    data = {
        "id": area.id,
        "lad_id": area.lad_id,
        "population": area.population,
        "area": area.area,
        "user_throughput_GB": area.user_throughput_GB,
        "user_throughput_mbps": area.user_throughput_mbps,
    }
    test_assets = area.assets + built_interventions
    
    test_area = PostcodeSector(
        data,
        area.ofcom_lad_id,
        test_assets,
        area._capacity_lookup_table,
        area._clutter_lookup,
        0
    )
    return test_area.capacity
