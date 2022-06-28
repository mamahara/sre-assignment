import json
import logging
import elasticsearch
from flask import Flask, render_template, request, url_for, flash, redirect, jsonify, current_app
from flask_cors import CORS, cross_origin

from es import ElasticRepository

app = Flask(__name__)
app.config.from_object('settings.ProductionConfig')


@app.route('/')
@cross_origin()
def index():
    try:
        esRepo = ElasticRepository()
        es = esRepo.get_elasticsearch_connection()
        all_city = esRepo.get_all_city(es=es, index_name=current_app.config['CITIES_INDEX_NAME'], document_type=current_app.config['CITIES_DOCUMENT_TYPE'])
    except Exception as e:
        print(e)
        error = {""}
        return jsonify(error), 500
    return render_template('index.html', title='G42 SRE Assignment',
                           cities=all_city)


@app.route('/api/v1/healthcheck', methods=['GET'])
@cross_origin()
def app_health_check():
    try:
        app.logger.debug("Checking healthcheck endpoint")
        es = ElasticRepository().get_elasticsearch_connection()
        if es.cluster.health()["status"] == "green" or es.cluster.health()["status"] == "yellow":
            app.logger.debug("elasticsearch endpoint" + es.cluster.health()["status"])
            return jsonify({"health": 'OK'})
        else:
            app.logger.debug("elasticsearch endpoint" + "not available")
            return jsonify({"health": 'ES still Unavailable'})
    except elasticsearch.ElasticsearchException as es1:
        return jsonify({"health": 'ES still Unavailable'}), 200


@app.route('/api/v1/addOrUpdateCityPopulation', methods=['POST'])
@cross_origin()
def app_update_city_population():
    try:
        esRepo = ElasticRepository()
        es = esRepo.get_elasticsearch_connection()
        content_type = request.headers.get('Content-Type')
        if content_type == 'application/json':
            city_data = json.loads(request.data)
            es_response = esRepo.insert_or_update_city(es=es, index_name=current_app.config['CITIES_INDEX_NAME'], document_type=current_app.config['CITIES_DOCUMENT_TYPE'], city=city_data)
        else:
            return 'Content-Type not supported!'
    except Exception as e:
        print(e)
    return es_response, 200


@app.route('/api/v1/getCityPopulation', methods=['POST'])
@cross_origin()
def get_city_population():
    try:
        esRepo = ElasticRepository()
        es = esRepo.get_elasticsearch_connection()
        content_type = request.headers.get('Content-Type')
        if content_type == 'application/json':
            city_name = json.loads(request.data)['city_name']
            print(city_name)
            population_count = esRepo.get_city_population(es=es, index_name=current_app.config['CITIES_INDEX_NAME'], document_type=current_app.config['CITIES_DOCUMENT_TYPE'], city_name=city_name)
        else:
            return 'Content-Type not supported!'
    except elasticsearch.exceptions.NotFoundError as e:
        print(e)
        error = {"city_name": f'{city_name}'.format(city_name=city_name), "population_count": "City Not Found"}
        return jsonify(error), 404
    except Exception as ex:
        print(ex)
        return ex;
    return population_count, 200


@app.route('/api/v1/getCityPopulation/<string:city_name>', methods=['GET'])
@cross_origin()
def get_population_from_name(city_name):
    try:
        esRepo = ElasticRepository()
        es = esRepo.get_elasticsearch_connection()
        print(city_name)
        population_count = esRepo.get_city_population(es=es, index_name=current_app.config['CITIES_INDEX_NAME'], document_type=current_app.config['CITIES_DOCUMENT_TYPE'], city_name=city_name)
    except elasticsearch.exceptions.NotFoundError as e:
        print(e)
        error = {"city_name": f'{city_name}'.format(city_name=city_name), "population_count": "City Not Found"}
        return jsonify(error), 404
    except Exception as ex:
        print(ex)
        return ex
    return population_count, 200


@app.route('/api/v1/getAllCity', methods=['GET'])
@cross_origin()
def get_all_city():
    try:
        esRepo = ElasticRepository()
        es = esRepo.get_elasticsearch_connection()
        all_city = esRepo.get_all_city(es=es, index_name=current_app.config['CITIES_INDEX_NAME'], document_type=current_app.config['CITIES_DOCUMENT_TYPE'])
    except Exception as e:
        print(e)
        error = {""}
        return jsonify(error), 500
    return json.dumps(all_city), 200


if __name__ == '__main__':
    app.run(host='0.0.0.0', port="5000", debug=app.config.from_envvar("LOG_LEVEL"))
    cors = CORS(app)
