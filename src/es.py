import hashlib

import elasticsearch
from elasticsearch import Elasticsearch, NotFoundError
from flask import current_app, jsonify


class ElasticRepository:
    def __init__(self):
        self.ES_SCHEME = current_app.config['ES_SCHEME']
        self.ES_HOST = current_app.config['ES_HOST']
        self.ES_PORT = current_app.config['ES_PORT']

        try:
            es = Elasticsearch([{'scheme': self.ES_SCHEME,
                                 'host': self.ES_HOST,
                                 'port': self.ES_PORT,
                                 'use_ssl': False}])
            es.indices.create(index=current_app.config['CITIES_INDEX_NAME'], ignore=400)
        except elasticsearch.exceptions as ex:
            print(ex)
        finally:
            es.close()

    def get_elasticsearch_connection(self):
        try:
            es = Elasticsearch([{'scheme': self.ES_SCHEME,
                                 'host': self.ES_HOST,
                                 'port': self.ES_PORT}])
        except elasticsearch.ElasticsearchException as es1:
            print(es1)
            raise
        return es

    def insert_or_update_city(self, es, index_name, document_type, city):
        try:
            es_response = es.get(index=index_name, doc_type=document_type,
                                 id=hashlib.md5(city['city_name'].upper().encode()).hexdigest())
            if es_response['found']:
                es_response = es.update(index=index_name, doc_type=document_type, body={"doc": city},
                                        id=hashlib.md5(city['city_name'].upper().encode()).hexdigest())
        except elasticsearch.exceptions.NotFoundError:
            es_response = es.index(index=index_name, doc_type=document_type, body=city,
                                   id=hashlib.md5(city['city_name'].upper().encode()).hexdigest())
        except Exception as ex:
            print('Error in indexing data')
            print(str(ex))

        return es_response

    def get_city_population(self, es, index_name, document_type, city_name):
        try:
            es_response = es.get(index=index_name, doc_type=document_type,
                                 id=hashlib.md5(city_name.upper().encode()).hexdigest())
            if es_response['found']:
                print(str(es_response['_source']))
                return es_response['_source']
        except Exception as ex:
            print('Error in getting data, Not Found')
            print(str(ex))
            raise ex

    def get_all_city(self, es, index_name, document_type):
        try:
            match_all = {
                "size": 1000,
                "query": {
                    "match_all": {}
                }
            }
            resp = es.search(index=index_name, body=match_all, scroll='1m')
            responseJsonList = []
            for doc in resp['hits']['hits']:
                if doc['_type'] == current_app.config['CITIES_DOCUMENT_TYPE']:
                    responseJsonList.append(doc['_source'])
            print(responseJsonList)
        except Exception as ex:
            print('Error in getting data')
            print(str(ex))
            raise ex
        return responseJsonList
