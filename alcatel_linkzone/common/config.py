import os
import json


class Config(object):
    @staticmethod
    def get_requests_data():
        return json.loads(
            open(os.path.join(os.path.dirname(__file__), "requests_data.json")).read()
        )
