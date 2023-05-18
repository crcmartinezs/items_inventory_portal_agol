
from arcgis import GIS
from arcgis.gis import Item
import pandas as pd



class ChildrenServices:
    def __init__(self, gis, items_ids) -> None:
        self._data = []
        self.gis = gis
        self.items_ids = items_ids
    
    def getServicesFromWebMap(self, itemId, appID):
        """_summary_

        Args:
            itemId (_type_): _description_
            appID (_type_): _description_
        """

        data = self._data
        gis = self.gis
        
        try:
            item = gis.content.get(itemId)
            data.append([item.title, item.itemid, appID])
            itemProp = item.get_data()
            for lyr in itemProp["operationalLayers"]:
                
                values = list(lyr.keys())
                if "url" in values and "itemId" in values:
                    serviceI2 = lyr["itemId"]
                elif "url" in values :
                    serviceI2 = lyr["url"]
                else:
                    serviceI2 = ("Cargada directamente")


                data.append([lyr["title"], serviceI2, appID])
        except: 
            print(itemId, "Not have services")

    def getMapsFromApps(self, item, appTitle, appID):
        try:
            keywords = item.typeKeywords
            if "Dashboard" in keywords:
                maps = [mapWidget for mapWidget in item.get_data()["widgets"] if mapWidget["type"] == "mapWidget"]
                for webMaps in maps:    
                    itemId = webMaps["itemId"]
                    self.getServicesFromWebMap(itemId, appTitle, appID)
            elif "Web AppBuilder" in keywords:
                itemId = item.get_data()["map"]["itemId"]
                self.getServicesFromWebMap(itemId, appTitle, appID)
            elif "Story Map" in keywords:
                for content in item.get_data()["values"]["story"]["entries"]:
                    itemId = content["media"]["webmap"]["id"]
                    self.getServicesFromWebMap(itemId, appTitle, appID)                    
            else:
                itemId = item.get_data()["values"]["webmap"]
                self.getServicesFromWebMap(itemId, appTitle, appID)
        except:
            print(item.id, "App not have map")
            
    @property
    def apps_and_maps(self): 
        data = self._data  
        gis = self.gis
        item_ids = self.items_ids
         
        for item_id in item_ids:
            print(item_id)
            item = gis.content.get(item_id)
            try:
                if item.type in ["Dashboard", "Web Mapping Application"]:
                    data.append([item.title, item.itemid, item.itemid])
                    self.getMapsFromApps(item, item.title, item.itemid)
            except:
                pass
        columns = ["Title", 'Item ID', 'App Group']
        df = pd.DataFrame(data, columns=columns)
        return df
