import json
import os

NETWORKS_TYPES = ['NO_SERVICE', '2G', '3G', '3G', '3G+', '4G', '4G+']

class Config(object):
    @staticmethod
    def get_requests_data():
        return json.loads(
            open(os.path.join(os.path.dirname(__file__), "requests_data.json")).read()
        )
