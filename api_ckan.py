""" 
API CKAN Loader
"""

import json
import urllib.request

####################################################################
######## API URLs ##################################################
####################################################################

API_BASE_URL = "/api/3/action/"
API_GROUP_LIST = "group_list"
API_PACKAGE_LIST = "package_list"
API_PACKAGE_SHOW = "package_show?id=" # + id_package

####################################################################
####### Várias de controle para impressão de arquivos ##############
####################################################################

print_portal_categories_file = False
print_portal_packages_file = False
print_portal_package_metadata = False

def obter_categorias(name_portal, url_portal):
    ####################################################################
    ######## Obtendo as categorias do portal ###########################
    ######## O CKAN chama categorias de grupos #########################
    ####################################################################

    urlGroupList = url_portal + API_BASE_URL + API_GROUP_LIST

    try:
        group_list_request = urllib.request.urlopen(urlGroupList).read()
    except:
        return None

    group_list_json = json.loads(group_list_request)

    if print_portal_categories_file : 
        filename = "Categories " + name_portal + ".json"
        with open(filename, 'w') as outfile:
            json.dump(group_list_json, outfile, indent=4)
    
    return group_list_json

def obter_metadados_datasets(name_portal, url_portal):

    """
    Lê os metadados de todos os datasets do portal e retorna um dicionário,
    com o nome do dataset como chave e os metadados como valor.
    """

    ####### Obtendo os datasets do portal ############################
    ####### O CKAN chama os datasets de package ######################
    ####### Recursos são todos os arquivos contidos nos packages #####
    ####### Na verdade os recursos são os datasets, ##################
    #######  mas o que interessa são os metadados dos packages #######

    urlPackageList = url_portal + API_BASE_URL + API_PACKAGE_LIST

    try:
        package_list_request = urllib.request.urlopen(urlPackageList).read()
    except:
        return None

    package_list_json = json.loads(package_list_request)

    if print_portal_packages_file : 
        filename = "Packages " + name_portal + ".json"
        with open(filename, 'w') as outfile:
            json.dump(package_list_json, outfile, indent=4)

    #################################################################
    ####### Iterando nos packages e extraindo metadados #############
    #################################################################
    #################################################################

    ### a variável 'result' contém a lista de ids dos packages ######
    lst_id_packages = package_list_json['result']

    #### criando um dicionário para armazenar os metadados ##########
    dict_package_metadata = {}

    for id_package in lst_id_packages:

        urlPackageShow = url_portal + API_BASE_URL + API_PACKAGE_SHOW + id_package

        ##### pode acontecer de um package listado estar com visibilidade privada
        ##### é precisa testar se conseguimos acesso ao package
        try:
            package_show_request = urllib.request.urlopen(urlPackageShow).read()
        except:
            continue 

        package_show_json = json.loads(package_show_request)

        #### a variável 'result' contém a lista de metadados do package ######
        package_metadata = package_show_json['result']

        dict_package_metadata[id_package] = package_metadata

    if print_portal_package_metadata:
        filename = "Packages Metadata " + name_portal + ".json"
        with open(filename, 'a') as outfile: ### append no final do arquivo
            json.dump(dict_package_metadata, outfile, indent=4)

    return dict_package_metadata



