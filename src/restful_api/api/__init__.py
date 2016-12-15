# -*- coding: utf-8 -*-
from config import Config
from flask import Flask

app = Flask(__name__)
config = Config()

from api import main