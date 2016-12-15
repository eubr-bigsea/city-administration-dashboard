# -*- coding: utf-8 -*-
import ConfigParser
import os

config = ConfigParser.RawConfigParser()
config_filename = 'config.ini'

db_section = 'Database'
api_section = 'REST'

# TODO: describe config structure into a third part file.
# TODO: automatic generation of config parser class using ast

# Database
config.add_section(db_section)

config.set(db_section, 'host', 'put_host_here')
config.set(db_section, 'port', 'put_port_here')
config.set(db_section, 'user', 'put_user_here')
config.set(db_section, 'passwd', 'put_password_here')
config.set(db_section, 'db_name', 'put_dbname_here')

# REST
config.add_section(api_section)
config.set(api_section, 'port', 'put_port_here')
config.set(api_section, 'secret_key', repr(os.urandom(24)))

with open(config_filename, 'wb') as configfile:
    config.write(configfile)
    print "New configuration file has created: '" + config_filename + "'"