import yaml

__config = None

def config():
    global __config
    if not __config:
        with open(r'config.yaml', encoding='utf8') as file:
            __config = yaml.load(file, Loader=yaml.FullLoader)
    return __config
