import json
import os

NETWORKS_TYPES = ["NO_SERVICE", "2G", "3G", "3G", "3G+", "4G", "4G+"]


class Config(object):
    ENDPOINT_URL = "http://192.168.1.1/jrd/webapi"
    TIMEOUT_REQUESTS = 300
    BACKOFF_CONSTANT = 0.1
    BACKOFF_EXPONENT_BASE = 1.5

    @staticmethod
    def get_requests_data():
        file_path = os.path.join(os.path.dirname(__file__), "requests_data.json")
        with open(file_path) as file:
            return json.load(file)
