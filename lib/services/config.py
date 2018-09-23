import yaml
import os
''' Contains Paths of the program'''

MAIN_DIRECTORY = os.path.dirname(os.path.realpath(__file__ + '/../..')) + '/'
CONFIG_NAME = 'config.yml'


def get_root_dir():
    return MAIN_DIRECTORY + ''  # + 'project\\' #change it for the compiled version remove 'project'


def get_directory(section):
    with open(MAIN_DIRECTORY + CONFIG_NAME) as ymlfile:
        cfg = yaml.load(ymlfile)
    path = ''.join(cfg['directories'][section])
    return path


def get_const(section):
    with open(MAIN_DIRECTORY + CONFIG_NAME) as ymlfile:
        cfg = yaml.load(ymlfile)
    const = cfg['constants'][section]
    return const
