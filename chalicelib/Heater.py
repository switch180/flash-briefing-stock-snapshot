import os
import logging
import requests
logger = logging.getLogger('my-app')

class Heater():
    chalice_stage = 'dev'
    chalice_config = '.chalice/config.json'
    endpoint_variable = 'PROD_API'
    def __init__(self):
        self.load_prod_endpoint()
    def heat_warm(self):
        req =  requests.get("{}warm".format(self.prod_endpoint))
        return req
    def load_prod_endpoint(self):
        try:
            self.prod_endpoint = os.environ[self.endpoint_variable]
        except KeyError as err:
            import json
            from chalice.config import Config
            with open(self.chalice_config, 'r') as config_json:
                self.environment_variables = Config(
                    chalice_stage = self.chalice_stage,
                    config_from_disk = json.loads(config_json.read())
                ).environment_variables
                self.prod_endpoint =  self.environment_variables[self.endpoint_variable]
