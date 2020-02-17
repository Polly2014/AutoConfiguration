# -*- coding:utf-8 -*-
import configparser
import tempfile

with open('tmp.txt', 'r') as f:
	config_string = f.read().replace('# ', '')
# tmp = tempfile.NamedTemporaryFile(delete=False)
# tmp.write(config_string.encode())
# tmp.close()
with tempfile.NamedTemporaryFile(delete=False) as tmp:
	tmp.write(config_string.encode())
conf = configparser.ConfigParser()
conf.read(tmp.name, encoding='utf-8')
print(tmp.name)
print(conf.sections())

