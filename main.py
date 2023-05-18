from arcgis import GIS
import pandas as pd
import os

from agol_inventory.AGOLInventory import Inventory
from children_services.children_services import ChildrenServices
from utilities.utils import df_to_excel

from common import config

#Portal/AGOL Accesss
config_data = config()
items_types = config_data['items_types']
gis_access = config_data['gis_data_access']

#Output info
outputs = config_data['output_workspace']
folder_path = outputs['output_folder_path'] 
inventory_output = outputs['inventory_output']
children_output = outputs['children_output']
children_details_output = outputs['children_details_output']


gis = GIS(
    url=gis_access['url'], 
    username=gis_access['username'], 
    password=gis_access['password'],
    verify_cert=False
    )

df_inventory = Inventory(gis).data

df_inventory_type_filter = df_inventory.loc[df_inventory['Tipo'].isin(items_types)]
items_ids = df_inventory_type_filter['Item ID'].to_list()

df_children = ChildrenServices(gis, items_ids).apps_and_maps

df_children_agg = pd.merge(
    left=df_children,
    right=df_inventory,
    left_on='Title',
    right_on='Título'
)

df_children_agg.drop_duplicates('Item ID_x', inplace=True)

df_to_excel(df_inventory, os.path.join(folder_path, inventory_output))
df_to_excel(df_children, os.path.join(folder_path, children_output))
df_to_excel(df_children_agg, os.path.join(folder_path, children_details_output))
