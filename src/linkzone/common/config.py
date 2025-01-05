import json
import os
from typing import List
from linkzone.common.data_models import USSDCode


class Config:
    CONFIG_FILE_PATH = os.path.join(os.path.dirname(__file__), "config.json")

    with open(CONFIG_FILE_PATH, "r") as config_file:
        config_data = json.load(config_file)

    ENDPOINT_URL = config_data["ENDPOINT_URL"]
    TIMEOUT_REQUESTS = config_data["TIMEOUT_REQUESTS"]
    BACKOFF_CONSTANT = config_data["BACKOFF_CONSTANT"]
    BACKOFF_EXPONENT_BASE = config_data["BACKOFF_EXPONENT_BASE"]
    NETWORKS_TYPES = config_data["NETWORKS_TYPES"]
    USSD_CODES: List[USSDCode] = [
        USSDCode(**code) for code in config_data["USSD_CODES"]
    ]
