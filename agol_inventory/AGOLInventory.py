#!/usr/bin/env python
# coding: utf-8


import pandas as pd
from datetime import datetime
from time import sleep
import numpy as np


class Inventory:
    def __init__(self, gis):
        self.__items = gis.content.search("*", max_items=10000)
        self.__isPortal = gis.properties['isPortal']

        self.__items_list = np.array_split(self.__items, 15)

        self.__columns = ["Folder","Propietario", "Título", "Nombre", "Tipo", "Número de vistas",
                "Tamaño (mb)", "Fecha creación", "Fecha modificación", "Item ID", "Uso ultimo anio"]

    def _get_items_info(self):
        self._data = list(map(self.getInventoryItems, self.__items_list))




    def getInventoryItems(self, items):
        datos = []
        for i, item in enumerate(items):
            try:
                usage = item.usage("1Y").Usage.sum() if not self.__isPortal else 0
                datos.append([item.ownerFolder, item.owner, item.title, item.name, item.type, item.numViews, item.size/1048576 ,
                datetime.utcfromtimestamp(item.created/1000).strftime('%Y-%m-%d %H:%M:%S'),
                datetime.utcfromtimestamp(item.modified/1000).strftime('%Y-%m-%d %H:%M:%S'), item.id, usage])

                sleep(5)
            except Exception as e:
                datos.append([item.ownerFolder, "","", "", "", None, None,
                None,
                None, None,""])
        return datos

    @property
    def data(self):
        self._get_items_info()
        data_formating = [item_info for d in self._data for item_info in d]

        df_inventory = pd.DataFrame(data_formating, columns=self.__columns)

        return df_inventory



