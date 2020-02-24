# -*- coding: utf-8 -*-

class CConfigCommon(object):
    # [Basic Options]
    datanum='1'
    datapath_list=[]
    PATH_FASTA = ''
    PATH_RESULT_EXPORT = ''

    # [Advanced Options]
    co_elute='1'
    input_format_list = ['raw', 'ms1', 'mgf']
    input_format='raw'
    isolation_width='2'
    mars_threshold='-0.5'
    ipv_file='.\IPV.txt'
    trainingset='.\TrainingSet.txt'
    
    # [Internal Switches]
    output_mars_y='0'
    delete_msn='0'
    output_mgf='1'
    output_pf='1'
    debug_mode='0'
    check_activationcenter='1'
    output_all_mars_y='0'
    rewrite_files='0'
    export_unchecked_mono='0'
    cut_similiar_mono='1'
    mars_model='4'
    output_trainingdata='0'
    
    # [About pXtract]
    m_z='5'
    Intensity='1'

class CConfigOne(object):
    # Data
    TYPE_MS2 = ''
    PATH_MS2 = ''
    PATH_FASTA = ''
    PATH_FASTA_EXPORT = ''
    PATH_RESULT_EXPORT = ''
    
    # Biology
    NAME_ENZYME_LIST = ['trpysin']
    NAME_ENZYME = 'trpysin'
    TYPE_DIGEST_LIST = ['specific']
    TYPE_DIGEST = 'specific'
    NUMBER_MAX_MISS_CLV = '0'
    NAME_MOD_FIX = []
    NAME_MOD_VAR = []
    NUMBER_MAX_MOD = '0'
    
    UAA_SEQ = ''
    UAA_AA = ''
    UAA_LEN_LOW = '0'
    UAA_LEN_UP = '0'
    UAA_COM = ''
    UAA_LINKED_AA = ''
    
    UAA_NAME_ENZYME = ''
    UAA_TYPE_DIGEST = '0'
    UAA_NUMBER_MAX_MISS_CLV = ''
    
    
    # [mass spectrometry]
    PPM_TOL_PRECURSOR='20ppm'
    PPM_TOL_FRAGMENT='20ppm'
    TYPE_ACTIVATION_LIST=['HCD']
    TYPE_ACTIVATION='HCD'
    
    # [performance]
    NUMBER_THREAD='8'
    
    TYPE_THREAD='0'
    NUMBER_SELECT_PEAK='200'
    NUMBER_SPECTRUM='10000'
    LEN_MAX_PROTEIN='100000'
    MASS_PEP_LOW='400'
    MASS_PEP_UP='10000'
    LEN_PEP_LOW='6'
    LEN_PEP_UP='100'
    INDEX_SPLIT_MASS='100'
    NUMBER_TOP_RESULT='10'
    MULTI_MASS='1'
    TYPE_TASK='0'
    TYPE_FILTER_BETA='1'
    NUMBER_PEAK_BETA='1'
    PATH_PFIND_RESULT=''
    
    # [filter]
    FDR_PSM='0.05'
    
    # [ini]
    PATH_INI_ELEMENT='./ini/element.ini'
    PATH_INI_AA='./ini/aa.ini'
    PATH_INI_MOD='./ini/modification.ini'


class CConfigTwo(object):
    # Data
    TYPE_MS2 = ''
    PATH_MS2 = ''
    PATH_FASTA = ''
    PATH_FASTA_EXPORT = ''
    PATH_RESULT_EXPORT = ''
    

