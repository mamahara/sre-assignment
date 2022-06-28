import os


class Config(object):
    DEBUG = False
    TESTING = False


class ProductionConfig(Config):
    try:
        DEBUG = os.environ.get('LOG_LEVEL', default='True')
        CITIES_INDEX_NAME = "cities_population"
        CITIES_DOCUMENT_TYPE = "cities"
        ES_SCHEME = os.environ.get('ES_SCHEME', default='http')
        if os.environ['ES_HOST']:
            ES_HOST = os.environ['ES_HOST']
        if os.environ['ES_PORT']:
            ES_PORT = os.environ['ES_PORT']
    except KeyError as ke:
        print(str(ke) + " is not set")


class DevelopmentConfig(Config):
    DEBUG = True


class TestingConfig(Config):
    TESTING = True
