"""Cambridge Communications Assessment Model
"""
# pylint: disable=W0312


class ICTManager(object):
    """Model controller class
    """
    def __init__(self, lads, pcd_sectors, assets):
        """Create an instance of the model

        Parameters
        ----------
        areas: list of dicts
            Each area is an LAD, expect the dictionary to have values for
            - ID
            - name
            - population
            - area (km^2)
            - penetration
            - user demand
        """
        # Area ID (integer?) => Area
        self.lads = {}

        # pcd_sector id =? LAD id
        lad_id_by_pcd_sector = {}
        # {
        # 	"pcd_sector_1": "lad_0",
        # 	"pcd_sector_2": "lad_0"
        # }

        for lad_data in lads:  # lad_data in lads <-'lads' is the list of dicts of lad data
            id = lad_data["id"]  # find ID out of lads list of dicts
            self.lads[id] = LAD(lad_data)  # create LAD object using lad_data and put in self.lads dict

        for pcd_sector_data in pcd_sectors:
            lad_id = pcd_sector_data["lad_id"]
            pcd_sector_id = pcd_sector_data["id"]
            # add PostcodeSector to LAD
            pcd_sector = PostcodeSector(pcd_sector_data)
            lad_containing_pcd_sector = self.lads[lad_id]
            lad_containing_pcd_sector.add_pcd_sector(pcd_sector)
            # add LAD id to lookup by pcd_sector_id
            lad_id_by_pcd_sector[pcd_sector_id] = lad_id

        for asset_data in assets:
            asset = Asset(asset_data)
            lad_id = lad_id_by_pcd_sector[asset.pcd_sector_id]
            area_for_asset = self.lads[lad_id]
            area_for_asset.add_asset(asset)

    def apply_interventions(self, interventions):
        pass

    def results(self):
        return {
            "system": {area.name: area.system() for area in self.lads.values()},
            "capacity": {area.name: area.capacity() for area in self.lads.values()},
            "coverage": {area.name: area.coverage() for area in self.lads.values()},
            "demand": {area.name: area.demand() for area in self.lads.values()},
            "cost": {area.name: area.cost() for area in self.lads.values()},
            "energy_demand": {area.name: area.energy_demand() for area in self.lads.values()}
        }

class LAD(object):
    """Represents an area to be modelled, contains
    data for demand characterisation and assets for
    supply assessment
    """
    def __init__(self, data):
        self.id = data["id"]
        self.name = data["name"]
        self.user_demand = data["user_demand"]
        self._pcd_sectors = {}

    def __repr__(self):
        return "<LAD id:{} name:{}>".format(self.id, self.name)

    def add_pcd_sector(self, pcd_sector):
        self._pcd_sectors[pcd_sector.id] = pcd_sector

    def add_asset(self, asset):
        pcd_sector_id = asset.pcd_sector_id
        self._pcd_sectors[pcd_sector_id].add_asset(asset)

    def system(self):
        system = {}
        for pcd_sector in self._pcd_sectors.values():
            pcd_system = pcd_sector.system()
            for tech, cells in pcd_system.items():
                # check tech is in system
                if tech not in system:
                    system[tech] = 0
                # add number of cells to tech in area
                system[tech] += cells
        return system

    def capacity(self):
        """returning the value from the method in pcd_sector object"""
        return sum([pcd_sector.capacity() for pcd_sector in self._pcd_sectors.values()])

    def demand(self):
        """returning the value from the method in pcd_sector object"""
        return sum([pcd_sector.demand() for pcd_sector in self._pcd_sectors.values()]) / len(self._pcd_sectors)

    def coverage(self):
        threshold = 2
        population_with_coverage = sum([pcd_sector.population for pcd_sector in self._pcd_sectors.values() if pcd_sector.capacity() >= threshold])
        total_pop = sum([pcd_sector.population for pcd_sector in self._pcd_sectors.values()])
        return float(population_with_coverage) / total_pop

    def cost(self):
        '''returning the value from the method in pcd_sector object'''
        return sum([pcd_sector.cost() for pcd_sector in self._pcd_sectors.values()])

    def energy_demand(self):
        '''returning the value from the method in pcd_sector object'''
        return sum([pcd_sector.energy_demand() for pcd_sector in self._pcd_sectors.values()])

class PostcodeSector(object):
    """Represents a pcd_sector to be modelled
    """
    def __init__(self, data):
        self.id = data["id"]
        self.lad_id = ["lad_id"]
        self.name = data["name"]
        self.population = data["population"]
        self.area = data["area"]
        # TODO: replace hard-coded parameters

        # clarify the busy hour user demand parameters ###
        # does this need to be bit/s or mbp/second? check with Zoraida
        self.user_demand = 2 * 1024 * 8 / 30 / 12 / 3600
        self.penetration = 0.8
        self._assets = []
        # I've turned assets from a list of dictionaries, to an explicit list per asset type

    def add_asset(self, asset):  # is asset an object? Should it be capitalised?
        self._assets.append(asset)

    def demand(self):
        users = self.population * self.penetration
        user_throughput = users * self.user_demand
        capacity_per_kmsq = user_throughput / self.area
        return capacity_per_kmsq

    def system(self):
        system = {
            "GSM": 0,
            "UMTS": 0,
            "LTE": 0,
            "LTE-Advanced": 0,
            "5G": 0
        }
        print(self._assets)
        for asset in self._assets:
            tech = asset.technology
            cells = asset.cells
            # check tech is in area
            if tech not in system:
                system[tech] = 0
            # add number of cells to tech in area
            system[tech] += cells
        print(system)
        return system

    def capacity(self):
        # sites : count how many assets are sites
        sites = len(list(filter(lambda asset: asset.type == "site", self._assets)))
        # sites/km^2 : divide num_sites/area
        site_density = float(sites) / self.area
        # for a given site density and spectrum band, look up capacity
        capacity = lookup_capacity(site_density)
        return capacity

    def capacity_margin(self):
        capacity_margin = self.capacity() - self.demand()
        return capacity_margin

    def cost(self):
        # sites : count how many assets are sites
        sites = len(list(filter(lambda asset: asset.type == "site", self._assets)))
        # for a given number of sites, what is the total cost?
        cost = (sites * 10)  # TODO replace hardcoded value
        return cost

    def energy_demand(self):
        # cells : count how many cells there are in the assets database
        cells = sum([asset.cells for asset in self._assets])
        # for a given number of cells, what is the total cost?
        energy_demand = (cells * 5)  # TODO replace hardcoded value
        return energy_demand


class Asset(object):
    """Element of the communication infrastructure system,
    e.g. base station or distribution-point unit.
    """
    def __init__(self, data):
        self.type = data["type"]
        self.pcd_sector_id = data["pcd_sector_id"]
        self.cells = data["cells"]
        self.technology = data["technology"]

    def __repr__(self):
        fmt = "Asset(type={}, pcd_sector_id={}, cells={}, technology={})"
        return fmt.format(self.type, self.pcd_sector_id, self.cells, self.technology)


def lookup_capacity(lookup_table, environment, frequency, bandwidth, site_density):
    """Use lookup table to find capacity by geotype, frequency, bandwidth and
    site density

    TODO:
    - neat handling of loaded lookup_table
    """
    if environment not in lookup_table:
        raise KeyError("Environment %s not found in lookup table", environment)
    if frequency not in lookup_table[environment]:
        raise KeyError("Frequency %s not found in lookup table", frequency)
    if bandwidth not in lookup_table[environment][frequency]:
        raise KeyError("Bandwidth %s not found in lookup table", bandwidth)

    density_capacities = lookup_table[environment][frequency][bandwidth]
    for i, (lower_bound, capacity) in enumerate(density_capacities):
        if site_density < lower_bound:
            if i == 0:
                raise ValueError("Site density %s less than lowest in lookup table", site_density)
            else:
                _, lower_value = density_capacities[i - 1]
                return lower_value
        elif site_density == lower_bound:
            return capacity
        else:
            pass  # site_density is greater than lower bound

    # got to end of list, so return maximum value from last item
    _, lower_value = density_capacities[-1]
    return lower_value


# __name__ == '__main__' means that the module is bring run in standalone by the user
if __name__ == '__main__':
    lads = [
        {
            "id": 1,
            "name": "Cambridge",
            "population": 250000,
            "area": 10,
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
        },
        {
            "id": 2,
            "name": "Oxford",
            "population": 220000,
            "area": 10,
            "user_demand": 1,
            "spectrum_available": {
                "GSM 900": True,
                "GSM 1800": True,
                "UMTS 900": True,
                "UMTS 2100": True,
                "LTE 800": False,
                "LTE 1800": False,
                "LTE 2600": False,
                "5G 700": False,
                "5G 3400": False,
                "5G 3600": False,
                "5G 26000": False,
            }
        }
    ]
    pcd_sectors = [
        {
            "id": 1,
            "lad_id": 1,
            "name": "CB1G",
            "population": 50000,
            "area": 2,
        },
        {
            "id": 2,
            "lad_id": 1,
            "name": "CB1H",
            "population": 50000,
            "area": 2,
        },
        {
            "id": 3,
            "lad_id": 2,
            "name": "OX1A",
            "population": 50000,
            "area": 4,
        },
        {
            "id": 4,
            "lad_id": 2,
            "name": "OX1B",
            "population": 50000,
            "area": 4
        }
    ]
    assets = [
        {
            "type": "site",
            "pcd_sector_id": 1,
            "cells": 3,
            "technology": "UMTS",
            "year": 2017
        },
        {
            "type": "site",
            "pcd_sector_id": 1,
            "cells": 3,
            "technology": "LTE",
            "year": 2017
        },
        {
            "type": "site",
            "pcd_sector_id": 1,
            "cells": 5,
            "technology": "LTE-Advanced",
            "year": 2018
        },
        {
            "type": "site",
            "pcd_sector_id": 2,
            "cells": 3,
            "technology": "UMTS",
            "year": 2017
        },
        {
            "type": "site",
            "pcd_sector_id": 2,
            "cells": 3,
            "technology": "LTE",
            "year": 2017
        },
        {
            "type": "site",
            "pcd_sector_id": 2,
            "cells": 6,
            "technology": "LTE-Advanced",
            "year": 2018
        },
        {
            "type": "site",
            "pcd_sector_id": 3,
            "cells": 3,
            "technology": "UMTS",
            "year": 2017
        },
        {
            "type": "site",
            "pcd_sector_id": 3,
            "cells": 3,
            "technology": "LTE",
            "year": 2017
        },
        {
            "type": "site",
            "pcd_sector_id": 3,
            "cells": 2,
            "technology": "LTE-Advanced",
            "year": 2018
        },
        {
            "type": "site",
            "pcd_sector_id": 4,
            "cells": 1,
            "technology": "UMTS",
            "year": 2017
        },
        {
            "type": "site",
            "pcd_sector_id": 4,
            "cells": 1,
            "technology": "LTE",
            "year": 2017
        },
        {
            "type": "site",
            "pcd_sector_id": 4,
            "cells": 3,
            "technology": "LTE-Advanced",
            "year": 2018
        }
    ]


    manager = ICTManager(lads, pcd_sectors, assets)
    import pprint
    pprint.pprint(manager.results())

    print(manager.lads)
    for lad in manager.lads.values():
        print(lad.name)
        print(lad._pcd_sectors)

