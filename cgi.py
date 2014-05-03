from wsgiref.handlers import CGIHandler
from pivotal_stocks import app
CGIHandler().run(app)
