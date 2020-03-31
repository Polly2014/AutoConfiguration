# -*- coding: utf-8 -*-

from MSConfig import *
from plugins import AutoConfigParser

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

class CConfigFileOne():
    def config2file(self, path, config):
        c = AutoConfigParser()
        # [Basic Options]
        c.add_section('Basic Options')
        c.set('Basic Options', 'datanum', str(config.datanum))
        for i in range(len(config.datapath_list)):
            c.set('Basic Options', 'datapath'+str(i+1), config.datapath_list[i])
        # [Advanced Options]
        c.add_section('Advanced Options')
        c.set('Advanced Options', 'co-elute', str(config.co_elute))
        c.set('Advanced Options', 'input_format', str(config.input_format))
        c.set('Advanced Options', 'isolation_width', str(config.isolation_width))
        c.set('Advanced Options', 'mars_threshold', str(config.mars_threshold))
        c.set('Advanced Options', 'ipv_file', str(config.ipv_file))
        c.set('Advanced Options', 'trainingset', str(config.trainingset))
        # [Internal Switches]
        c.add_section('Internal Switches')
        c.set('Internal Switches', 'output_mars_y', str(config.output_mars_y))
        c.set('Internal Switches', 'delete_msn', str(config.delete_msn))
        c.set('Internal Switches', 'output_mgf', str(config.output_mgf))
        c.set('Internal Switches', 'output_pf', str(config.output_pf))
        c.set('Internal Switches', 'debug_mode', str(config.debug_mode))
        c.set('Internal Switches', 'check_activationcenter', str(config.check_activationcenter))
        c.set('Internal Switches', 'output_all_mars_y', str(config.output_all_mars_y))
        c.set('Internal Switches', 'rewrite_files', str(config.rewrite_files))
        c.set('Internal Switches', 'export_unchecked_mono', str(config.export_unchecked_mono))
        c.set('Internal Switches', 'cut_similiar_mono', str(config.cut_similiar_mono))
        c.set('Internal Switches', 'mars_model', str(config.mars_model))
        c.set('Internal Switches', 'output_trainingdata', str(config.output_trainingdata))
        # [About pXtract]
        c.add_section('About pXtract')
        c.set('About pXtract', 'm/z', str(config.m_z))
        c.set('About pXtract', 'Intensity', str(config.Intensity))
        with open(path,  'w') as f:
            c.write(f)

    def file2config(self, path, config):
        c = AutoConfigParser()
        c.read(path, encoding='utf-8')
        c.remove_note()
        # [Advanced Options] Update
        config.TYPE_MS2 = c.get('Advanced Options',  'input_format')
        # [Basic Options] Update
        file_list = c.items('Basic Options')
        file_list = list(filter(lambda x: x[0][:-1]=='datapath', file_list))
        config.datapath_list = [x[1] for x in file_list]
        # [About pXtract] Update
        config.m_z = c.get('About pXtract',  'm/z')
        return config

class CConfigFileTwo():
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
        c.set('biology', 'NUMBER_MAX_MISS_CLV', config.NUMBER_MAX_MISS_CLV)
        c.set('biology', 'NAME_MOD_FIX', '|'.join(config.NAME_MOD_FIX))
        c.set('biology', 'NAME_MOD_VAR',  '|'.join(config.NAME_MOD_VAR))
        c.set('biology', 'NUMBER_MAX_MOD', config.NUMBER_MAX_MOD)
        c.set('biology', 'UAA_SEQ', config.UAA_SEQ)
        c.set('biology', 'UAA_AA', config.UAA_AA)
        c.set('biology', 'UAA_LEN_LOW', config.UAA_LEN_LOW)
        c.set('biology', 'UAA_LEN_UP', config.UAA_LEN_UP)
        c.set('biology', 'UAA_COM', config.UAA_COM)
        c.set('biology', 'UAA_NAME_ENZYME', config.UAA_NAME_ENZYME)
        c.set('biology', 'UAA_TYPE_DIGEST', config.UAA_TYPE_DIGEST)
        c.set('biology', 'UAA_NUMBER_MAX_MISS_CLV', config.UAA_NUMBER_MAX_MISS_CLV)
        c.set('biology', 'UAA_LINKED_AA', config.UAA_LINKED_AA)
        # [mass]
        c.add_section('mass spectrometry')
        c.set('mass spectrometry', 'PPM_TOL_PRECURSOR', config.PPM_TOL_PRECURSOR)
        c.set('mass spectrometry', 'PPM_TOL_FRAGMENT', config.PPM_TOL_FRAGMENT)
        c.set('mass spectrometry', 'TYPE_ACTIVATION', config.TYPE_ACTIVATION)
        # [performance]
        c.add_section('performance')
        c.set('performance', 'NUMBER_THREAD', config.NUMBER_THREAD)
        c.set('performance', 'TYPE_THREAD', config.TYPE_THREAD)
        c.set('performance', 'NUMBER_SELECT_PEAK', config.NUMBER_SELECT_PEAK)
        c.set('performance', 'NUMBER_SPECTRUM', config.NUMBER_SPECTRUM)
        c.set('performance', 'LEN_MAX_PROTEIN', config.LEN_MAX_PROTEIN)
        c.set('performance', 'MASS_PEP_LOW', config.MASS_PEP_LOW)
        c.set('performance', 'MASS_PEP_UP', config.MASS_PEP_UP)
        c.set('performance', 'LEN_PEP_LOW', config.LEN_PEP_LOW)
        c.set('performance', 'LEN_PEP_UP', config.LEN_PEP_UP)
        c.set('performance', 'INDEX_SPLIT_MASS', config.INDEX_SPLIT_MASS)
        c.set('performance', 'NUMBER_TOP_RESULT', config.NUMBER_TOP_RESULT)
        c.set('performance', 'MULTI_MASS', config.MULTI_MASS)
        c.set('performance', 'TYPE_TASK', config.TYPE_TASK)
        c.set('performance', 'TYPE_FILTER_BETA', config.TYPE_FILTER_BETA)
        c.set('performance', 'NUMBER_PEAK_BETA', config.NUMBER_PEAK_BETA)
        c.set('performance', 'PATH_PFIND_RESULT', config.PATH_PFIND_RESULT)
        # [filter]
        c.add_section('filter')
        c.set('filter', 'FDR_PSM', config.FDR_PSM)
        # [filter]
        c.add_section('ini')
        c.set('ini', 'PATH_INI_ELEMENT', config.PATH_INI_ELEMENT)
        c.set('ini', 'PATH_INI_AA', config.PATH_INI_AA)
        c.set('ini', 'PATH_INI_MOD', config.PATH_INI_MOD)
        
        with open(path,  'w') as f:
            c.write(f)
        
    def file2config(self, path, config):
        c = AutoConfigParser()
        c.read(path, encoding='utf-8')
        c.remove_note()
        
        # [data]
        config.TYPE_MS2 = c.get('data',  'TYPE_MS2')
        config.PATH_MS2 = c.get('data',  'PATH_MS2')
        config.PATH_FASTA = c.get('data',  'PATH_FASTA')
        config.PATH_FASTA_EXPORT = c.get('data',  'PATH_FASTA_EXPORT')
        config.PATH_RESULT_EXPORT = c.get('data',  'PATH_RESULT_EXPORT')
        
        # [biology]
        config.NAME_ENZYME = c.get('biology',  'NAME_ENZYME')
        config.TYPE_DIGEST = c.get('biology',  'TYPE_DIGEST')
        config.NUMBER_MAX_MISS_CLV = int(c.get('biology', 'NUMBER_MAX_MISS_CLV'))
        config.NAME_MOD_FIX = c.get('biology', 'NAME_MOD_FIX').split('|')
        config.NAME_MOD_VAR = c.get('biology', 'NAME_MOD_VAR').split('|')
        config.NUMBER_MAX_MOD = int(c.get('biology', 'NUMBER_MAX_MOD'))
        
        config.UAA_SEQ = c.get('biology', 'UAA_SEQ')
        config.UAA_AA = c.get('biology', 'UAA_AA')
        config.UAA_LEN_LOW = int(c.get('biology', 'UAA_LEN_LOW'))
        config.UAA_LEN_UP = int(c.get('biology', 'UAA_LEN_UP'))
        config.UAA_COM = c.get('biology', 'UAA_COM')
        config.UAA_LINKED_AA = c.get('biology', 'UAA_LINKED_AA')
        
        # [mass spectrometry]
        config.PPM_TOL_PRECURSOR = c.get('mass spectrometry', 'PPM_TOL_PRECURSOR')
        config.PPM_TOL_FRAGMENT = c.get('mass spectrometry', 'PPM_TOL_FRAGMENT')
        config.TYPE_ACTIVATION = c.get('mass spectrometry', 'TYPE_ACTIVATION')
        
        # [performance]
        config.NUMBER_THREAD = int(c.get('performance', 'NUMBER_THREAD'))
        
        # [filter]
        config.FDR_PSM = float(c.get('filter', 'FDR_PSM'))
        return config
        
    def test(self):
        print('Ha')
        
class CConfigFileThree():
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
        c = CConfigOne()
        cf = CConfigFileOne()
        s = cf.file2config('..\\Program\\params\\config_1.txt',  c)
        print('----------')
    except Exception as e:
        print(e)
