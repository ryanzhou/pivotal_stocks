import sys, os
# Add /vendor and /lib to python PATH
sys.path.append(os.path.join(os.path.dirname(__file__), "../vendor"))
sys.path.append(os.path.join(os.path.dirname(__file__), "../lib"))

from flask import Flask, g
app = Flask(__name__)
app.config.from_object('config')

import pivotal_stocks.database
import pivotal_stocks.views
import pivotal_stocks.filters
import pivotal_stocks.context_processors
