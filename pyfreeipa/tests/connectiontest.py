"""
Test connection to FreeIPA server
"""
import json
import yaml

with open('pyfreeipa.conf.yaml', 'r') as configfile:
    CONFIG = yaml.load(configfile)

print(json.dumps(CONFIG, indent=4, sort_keys=True))
