import os

SECRET_KEY = 'KLDSKakI@!dkajSKDJdkjkJ@KkdjKJSAdj932ujdKLDJ'
JWT_ALGORITHM = 'HS256'
ACCESS_TOKEN_EXPIRE_MINUTES = 60 * 60 * 3

SQL_USER = os.environ.get('SQL_USER')
SQL_PASSWORD = os.environ.get('SQL_PASSWORD')
SQL_HOST = os.environ.get('SQL_HOST')
SQL_DATABASE = os.environ.get('SQL_DATABASE')
