#!flask/bin/python
# -*- coding: utf-8 -*-

from api import app, config

if __name__ == '__main__':
    app.debug = True
    app.secret_key = config.get_api_secret_key()
    app.run(host='0.0.0.0', port=config.get_api_port())

