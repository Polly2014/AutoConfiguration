# -*- coding: utf-8 -*-

from Config import *
import configparser
from plugins import AutoConfigParser

class ConfigOptionData():
    def config2string(self, config_data):
        config_string = '# [data]\n'
        config_string += 'TYPE_MS2={}\n'.format(config_data.TYPE_MS2)
        config_string += 'PATH_MS2={}\n'.format(config_data.PATH_MS2)
        config_string += 'PATH_FASTA={}\n'.format(config_data.PATH_FASTA)
        config_string += 'PATH_FASTA_EXPORT={}\n'.format(config_data.PATH_FASTA_EXPORT)
        config_string += 'PATH_RESULT_EXPORT={}\n'.format(config_data.PATH_RESULT_EXPORT)
        return config_string
        
    def string2config(self, config_string):
        config_data = ConfigData()
        config_data.TYPE_MS2 = config_string.get('data',  'TYPE_MS2')
        config_data.PATH_MS2 = config_string.get('data',  'PATH_MS2')
        config_data.PATH_FASTA = config_string.get('data',  'PATH_FASTA')
        config_data.PATH_FASTA_EXPORT = config_string.get('data',  'PATH_FASTA_EXPORT')
        config_data.PATH_RESULT_EXPORT = config_string.get('data',  'PATH_RESULT_EXPORT')
        return config_data
        '''
        for config_string in config_string_list:
            if config_string.startswith('#'):
                continue
        config_data = ConfigData()
        return config_data
        '''
class configFileBase():
    def file2config(self, path, config):
        c = AutoConfigParser()
        c.read(path, encoding='utf-8')
        section_list = c.sections()
        for section in section_list:
            item_list = c.items(section)
            for k, v in item_list:
               setattr(config, k, v)
        return config 

class ConfigFileOne():
    def config2file(self, path, config):
        c = AutoConfigParser()
        # [data]
        c.add_section('data')
        c.set('data', 'TYPE_MS2', config.TYPE_MS2)
        c.set('data', 'PATH_MS2', config.PATH_MS2)
        c.set('data', 'PATH_FASTA', config.PATH_FASTA)
        c.set('data', 'PATH_FASTA_EXPORT', config.PATH_FASTA_EXPORT)
        c.set('data', 'PATH_RESULT_EXPORT', config.PATH_RESULT_EXPORT)
        # [biology]
        c.add_section('biology')
        c.set('biology', 'NAME_ENZYME', config.NAME_ENZYME)
        c.set('biology', 'TYPE_DIGEST', config.TYPE_DIGEST)
        c.set('biology', 'PATH_TEMP', config.PATH_TEMP)
        # [mass]
        c.add_section('mass')
        c.set('mass', 'LIST_SELECTED', ';'.join(config.LIST_SELECTED))
        c.set('mass', 'LIST_UNSELECT', ';'.join(config.LIST_UNSELECT))
        
        with open(path,  'w') as f:
            c.write(f)
        
    def file2config(self, path, config):
        c = AutoConfigParser()
        c.read(path, encoding='utf-8')
        # [data]
        config.TYPE_MS2 = c.get('data',  'TYPE_MS2')
        config.PATH_MS2 = c.get('data',  'PATH_MS2')
        config.PATH_FASTA = c.get('data',  'PATH_FASTA')
        config.PATH_FASTA_EXPORT = c.get('data',  'PATH_FASTA_EXPORT')
        config.PATH_RESULT_EXPORT = c.get('data',  'PATH_RESULT_EXPORT')
        # [biology]
        config.NAME_ENZYME = c.get('biology',  'NAME_ENZYME')
        config.TYPE_DIGEST = c.get('biology',  'TYPE_DIGEST')
        config.PATH_TEMP = c.get('biology',  'PATH_TEMP')
        # [mass]
        config.LIST_SELECTED = c.get('mass',  'LIST_SELECTED').split(';')
        config.LIST_UNSELECT = c.get('mass',  'LIST_UNSELECT').split(';')
        return config
        
    def test(self):
        print('Ha')
        
class ConfigFileTwo():
    def config2file(self, path, config):
        with open(path,  'w') as f:
            config.write(f)
        
    def file2config(self, path, config):
        c = AutoConfigParser()
        c.read(path, encoding='utf-8')
        section_list = c.sections()
        for section in section_list:
            item_list = c.items(section)
            for k, v in item_list:
                setattr(config, k, v)
        return config
        
if __name__=='__main__':
    try:
        c = ConfigOne()
        cf = ConfigFileOne()
        s = cf.file2config('..\\Program\\params\\config_1.txt',  c)
        print('----------')
        print(dir(c))
        print(c.PATH_RESULT_EXPORT)
    except Exception as e:
        print(e)
