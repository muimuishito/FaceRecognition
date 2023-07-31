import configparser
import os

# CREATE OBJECT
config_file = configparser.ConfigParser()

# ADD SECTION
config_file.add_section("CamaraConfig")
# ADD SETTINGS TO SECTION
config_file.set("CamaraConfig", "Camara", "0")

# SAVE CONFIG FILE
with open(os.path.abspath(os.path.join(os.path.dirname(__file__), os.pardir)) + '\\Configs\\camara_config.ini', 'w', encoding='utf-8') as configfileObj:
    config_file.write(configfileObj)
    configfileObj.flush()
    configfileObj.close()
    

# read_file = open(r"Configurations\Configs\config.ini", "r", encoding='utf-8')
# content = read_file.read()
# print("Content of the config file are:\n")
# print(content)
# read_file.flush()
# read_file.close()    