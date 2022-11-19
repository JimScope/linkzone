import json

class Config(object):
    
    @staticmethod
    def get_requests_data():
        return json.loads(open('requests_data.json').read())