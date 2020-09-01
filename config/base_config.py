class Config(object):
    DEBUG = True
    TESTING = False
    
class DockerDevelopmentConfig(Config):
    DEBUG = True
    
    MONGODB_SETTINGS = {
        'db': 'employee',
        'host': 'mongodb',
        'port': 27017
    }

    MARIA_CONFIG = {
        'host': 'db',
        'port': 3306,
        'user': 'ahmedsamir',
        'password': 'password1',
        'database': 'employees'
    }

class LocalDevelopmentConfig(Config):
    DEBUG = True

    MONGODB_SETTINGS = {
        'db': 'employee',
        'host': 'localhost',
        'port': 27017
    }

    MARIA_CONFIG = {
        'host': '127.0.0.1',
        'port': 3306,
        'user': 'ahmedsamir',
        'password': 'password1',
        'database': 'employees'
    }

class TestingConfig(Config):
    TESTING = True