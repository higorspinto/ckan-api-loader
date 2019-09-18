###################################

import json

from portal import Portal
from api_ckan import obter_metadados_datasets

#####################################################################
########## Lendo todos os portais do arquivo portals.json ###########
#####################################################################

lstPortals = []
portalsFile = "portals.json" 

with open(portalsFile, 'r') as json_file:  
    data = json.load(json_file)
    for p in data:
        portal = Portal()
        portal.setCity(p["city"])
        portal.setUrl(p["url"])
        portal.setCoord(p["coord"])
        portal.setCategorization(p["categorization"])
        portal.setPlatform(p["platform"])
        portal.setCategories(p['categories'])
        
        lstPortals.append(portal)

####################################################################
###### Obtendo portais que utilizam o CKAN como plataforma #########
####################################################################

ckan_portals = []
for portal in lstPortals:
    if portal.getPlatform() == "CKAN":
        ckan_portals.append(portal)

####################################################################
#### Itera nos portais obtendo os metadados de todos os datasets ###
####################################################################

dict_portal_metadata = {}

for portal in ckan_portals:
    dict_package_metadata = obter_metadados_datasets(portal.getCity(), portal.getUrl())
    dict_portal_metadata[portal.getCity()] = dict_package_metadata

filename = "portals_datasets_metadata" + ".json"
with open(filename, 'w') as outfile:
    json.dump(dict_portal_metadata, outfile, indent=4)


