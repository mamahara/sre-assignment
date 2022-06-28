import json

from flask import current_app


class City:
    def __init__(self, city_name, population_count):
        self.city_name = city_name
        self.population_count = population_count

        self.json = {}

        try:
            self.json = {
                "_index": current_app.config['INDEX_NAME'],
                "_id": self.id,
                "_type": "City",
                "_source": self.source,
            }
        except Exception as error:
            print("Document JSON instance ERROR:", error)

    def json_str(self):
        try:
            doc = json.dumps(self.source, indent=4)
        except Exception as error:
            doc = "{}"
            print("Document json_string() ERROR:", error)
        return doc