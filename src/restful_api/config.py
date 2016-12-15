# -*- coding: utf-8 -*-
import ConfigParser


class Config():
    __default_config_filename = 'config.ini'
    __db_section = 'Database'
    __api_section = 'REST'

    def __init__(self, config_filename=__default_config_filename):
        self.__config = ConfigParser.RawConfigParser()
        self.__config.read(config_filename)
        self.__load_config()

    def __load_config(self):
        self.__db_host = self.__config.get(self.__db_section, 'host')
        self.__db_port = self.__config.getint(self.__db_section, 'port')
        self.__db_user = self.__config.get(self.__db_section, 'user')
        self.__db_passwd = self.__config.get(self.__db_section, 'passwd')
        self.__db_name = self.__config.get(self.__db_section, 'db_name')
        self.__api_port = self.__config.getint(self.__api_section, 'port')
        self.__api_secret_key = self.__config.get(self.__api_section, 'secret_key')

    def get_db_host(self):
        return self.__db_host

    def get_db_port(self):
        return self.__db_port

    def get_db_user(self):
        return self.__db_user

    def get_db_passwd(self):
        return self.__db_passwd

    def get_db_name(self):
        return self.__db_name

    def get_api_port(self):
        return self.__api_port

    def get_api_secret_key(self):
        return self.__api_secret_key