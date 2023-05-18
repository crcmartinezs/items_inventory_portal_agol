from arcgis import GIS

def connect_to_gis (url, username, password):
    gis = GIS(
        url=url,
        username=username,
        password=password,
        verify_cert=False
    )