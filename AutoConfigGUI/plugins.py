# -*- coding: utf-8 -*-

from Crypto.Cipher import AES
import wmi
import base64
import os
import configparser
import requests

def config2string(config):
    str = '# [data]\n'
    str += 'TYPE_MS2={}\n'.format(config.TYPE_MS2)
    str += 'PATH_MS2={}\n'.format(config.PATH_MS2)
    str += 'PATH_FASTA={}\n'.format(config.PATH_FASTA)
    str += 'PATH_FASTA_EXPORT={}\n'.format(config.PATH_FASTA_EXPORT)
    str += 'PATH_RESULT_EXPORT={}\n'.format(config.PATH_RESULT_EXPORT)
    return str
    
def txt2config():
    pass

class AutoConfigParser(configparser.ConfigParser):
    def optionxform(self, optionstr):
        return optionstr
        
    def remove_note(self):
        section_list = self.sections()
        for section in section_list:
            for k, v in self.items(section):
                self.set(section, k, v.split('#', 1)[0].strip())

def get_cpu_number():
	c = wmi.WMI()
	cpu = c.Win32_Processor()[0]
	return cpu.ProcessorId.strip()

class License(object):
    def __init__(self, key='26716201@qq.com'):
        if len(key) > 32:
            key = key[:32]
        self.key = self.to_16(key)

    def to_16(self, key):
        key = bytes(key, encoding="utf8")
        while len(key) % 16 != 0:
            key += b'\0'
        return key  # 返回bytes

    def aes(self):
        return AES.new(self.key, AES.MODE_ECB)  # 初始化加密器

    def make_license(self, text):
        aes = self.aes()
        return str(base64.encodebytes(aes.encrypt(self.to_16(text))),
                   encoding='utf8').replace('\n', '')  # 加密

    def valid_license(self, text):
        aes = self.aes()
        return str(aes.decrypt(base64.decodebytes(bytes(
            text, encoding='utf-8'))).rstrip(b'\0').decode("utf-8"))  # 解密


def check_registered(cpu_number):
    result = {'code':0,  'message': 'Already Registered!'}
    conf = configparser.ConfigParser()
    if os.path.exists('cfg.ini'):
        conf.read('cfg.ini',  encoding='utf-8')
        if 'license' in conf.sections():
            properties = [item[0] for item in conf.items('license')]
            if 'key' in properties and 'host' in properties:
                if cpu_number==conf.get('license',  'host'):
                    license = License()
                    key_real = license.make_license(cpu_number)
                    if not key_real==conf.get('license',  'key'):
                        result['code'] = 1
                        result['message'] = 'Not Registered Yet!'
                else:
                    result['code'] = -1
                    result['message'] = 'Error, File cfg.ini has been modified!'
            else:
                result['code'] = -1
                result['message'] = 'Error, File cfg.ini has been modified!'
        else:
            result['code'] = -1
            result['message'] = 'Error, File cfg.ini has been modified!'
    else:
        conf.add_section('license')
        conf.set('license',  'host',  cpu_number)
        conf.set('license',  'key',  '')
        conf.write(open('cfg.ini',  'w'))
        result['code'] = 2
        result['message'] = 'No cfg.ini File, Create it!'
    return result

def update_license(license_number):
    result = {'code':0, 'message': 'Regist and Update License Success!'}
    conf = configparser.ConfigParser()
    try:
        conf.read('cfg.ini',  encoding='utf-8')
        conf.set('license', 'key', license_number)
        conf.write(open('cfg.ini',  'w'))
    except Exception as e:
        result['code'] = -1
        result['message'] = 'Update License Error: {}'.format(e)
    return result

def register(pay_load):
    result = {'code':0, 'message':'Regist Success!'}
    try:
        response = requests.get('http://localhost/regist', params=pay_load, timeout=2)
        result['message'] = response.json()
    except Exception as e:
        result = {'code':-1, 'message': '{}'.format(e)}
    return result

if __name__=='__main__':
    license = License()
    # print(license.make_license(get_cpu_number()))
    pay_load = {'sn': license.make_license(get_cpu_number()), 'username': 'polly', 'email': 'test@test.com'}
    print(register(pay_load))
