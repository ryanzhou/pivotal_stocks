import os
_basedir = os.path.abspath(os.path.dirname(__file__))
DEBUG = False
DATABASE = os.path.join(_basedir, 'db/pivotal_stocks.db')
SECRET_KEY = "mIaAzTQrOV7ph1cc8MFW8hXyeLkVQUMq3LQDMO2BDJBG9hvRIyHyCz83wAyvJNQX"
del os
