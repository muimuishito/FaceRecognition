import configparser

#Method to read config file settings
# def read_camara_config():
#     config = configparser.ConfigParser()
#     config.read(r'..\Configurations\Configs\camara_config.ini', encoding='utf-8')
#     return config




# for Debuging file and compiling
def read_camara_config():
    config = configparser.ConfigParser()
    config.read(r'Configurations\Configs\camara_config.ini', encoding='utf-8')
    return config